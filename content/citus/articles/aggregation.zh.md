---
title: 使用 PostgreSQL 搭配 Citus 实现大规模实时事件聚合
description: 了解如何使用 PostgreSQL 和 Citus 大规模实现实时事件聚合，以便高效处理大量数据。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/aggregation?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: 事件聚合
---

**原始文章：** [Marco Slot · 2016 年 11 月 29 日](https://www.citusdata.com/blog/2016/11/29/event-aggregation-at-scale-with-postgresql/)。中文整理：[PGSTY](https://pgsty.com/)。

> [!NOTE]
> 本文提到了 Citus Cloud 服务。Amazon Web Service（AWS）上的 Citus Cloud 已不再接受新用户注册。如果你刚开始使用 Citus，仍然可以使用它：Citus 是开源软件，也作为 Azure Database for PostgreSQL 中完全集成的部署选项在 Microsoft Azure 云上提供。
>
> 更多信息请参阅[托管服务](/citus/installation/citus-cloud/)。

Citus 常用于横向扩展基于 PostgreSQL 的事件数据管道。它能透明地对数据进行分片，并在多台机器上并行执行查询，因此即便数据量达到数 TB，也可以实现实时响应。数据量大的用户通常会保存预聚合数据，以避免查询时处理原始数据的开销。对于大型数据集，查询预先计算好的聚合表，可能比按需查询事实表快几个数量级。

为了对分布式表进行聚合，文章发表时最新版本的 Citus 为使用相同分布列的表提供了 `INSERT .. SELECT` 支持。Citus 会自动将分布式表的分片“共置”，使相同分布列值的数据始终落在同一工作节点上。这样，只要保持分布列的值不变，就能在表之间传输数据。利用共置的一种常见方式是采用多租户数据模型，按 `tenant_id` 或 `customer_id` 对所有表进行分片。即使不采用这种模型，只要各表使用相同的分布列，也可以使用 `INSERT .. SELECT` 语法。

这里支持的是能够下推到工作节点的 `INSERT .. SELECT` 查询，因此不包括限制结果数量、合并结果集等某些 SQL 功能。查询结果会插入目标表中共置的分片。因此，必须确保聚合保留分布列（例如 tenant_id），并在连接中包含该列。分布式表上的 `INSERT .. SELECT` 命令通常如下：

```sql
INSERT INTO aggregation_table (tenant_id, ...)
SELECT tenant_id, ... FROM facts_table ...
```

下面以页面访问记录这一典型的海量数据场景，演示创建聚合的步骤。先建立一个 [Citus Cloud](https://www.citusdata.com/product/cloud/) 集群，包含 4 个工作节点，每个节点 4 个核心，然后创建一张带有多个索引的分布式事实表：

```sql
CREATE TABLE page_views (
    tenant_id int,
    page_id int,
    host_ip inet,
    view_time timestamp default now()
);
CREATE INDEX view_tenant_idx ON page_views (tenant_id);
CREATE INDEX view_time_idx ON page_views USING BRIN (view_time);

SELECT create_distributed_table('page_views', 'tenant_id');
```

接下来生成 1 亿行模拟数据（需要几分钟），并将其加载到数据库中：

```psql
\COPY (SELECT s % 307, (random()*5000)::int, '203.0.113.' || (s % 251), now() + random() * interval '60 seconds' FROM generate_series(1,100000000) s) TO '/tmp/views.csv' WITH CSV

\COPY page_views FROM '/tmp/views.csv' WITH CSV
```

现在可以对事实表执行 SQL 查询，在查询时进行聚合：

```sql
-- Most views in the past week
SELECT page_id, count(*) AS view_count
FROM page_views
WHERE tenant_id = 5 AND view_time >= date '2016-11-23'
GROUP BY tenant_id, page_id
ORDER BY view_count DESC LIMIT 3;
 page_id | view_count
---------+------------
    2375 |         99
    4538 |         95
    1417 |         93
(3 rows)

Time: 269.125 ms
```

为了改进性能，可以创建一张预计算的聚合表，同样按 `tenant_id` 分布。Citus 会自动将它与 `page_views` 表共置：

```sql
CREATE TABLE daily_page_views (
    tenant_id int,
    day date,
    page_id int,
    view_count bigint,
    primary key (tenant_id, day, page_id)
);

SELECT create_distributed_table('daily_page_views', 'tenant_id');
```

现在用一条简单的 `INSERT..SELECT` 命令就能填充聚合表。该命令会在工作节点的各个核心上并行执行，每秒处理约 1,000 万个事件，生成 170 万条聚合记录：

```sql
INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
  SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
  FROM page_views
  GROUP BY tenant_id, view_time::date, page_id;

INSERT 0 1690649

Time: 10649.870 ms
```

创建聚合后，从聚合表获取结果所需的时间就只占原查询耗时的一小部分：

```sql
-- Most views in the past week
SELECT page_id, view_count
FROM daily_page_views
WHERE tenant_id = 5 AND day >= date '2016-11-23'
ORDER BY view_count DESC LIMIT 3;
 page_id | view_count
---------+------------
    2375 |         99
    4538 |         95
    1417 |         93
(3 rows)

Time: 4.528 ms
```

通常，即使当天仍有数据不断进入，你也希望聚合结果保持最新。为此，可以扩展原来的命令，使其只处理新增行，并使用 [ON CONFLICT](https://www.postgresql.org/docs/current/static/sql-insert.html#SQL-ON-CONFLICT) 更新已有行，把新增数据计入其中。如果待插入数据的主键（`tenant_id`、`day`、`page_id`）已存在于聚合表中，就将计数累加到已有值上。

```sql
INSERT INTO page_views VALUES (5, 10, '203.0.113.1');

INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
  SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
  FROM page_views
  WHERE view_time >= '2016-11-23 23:00:00' AND view_time < '2016-11-24 00:00:00'
  GROUP BY tenant_id, view_time::date, page_id
  ON CONFLICT (tenant_id, day, page_id) DO UPDATE SET
  view_count = daily_page_views.view_count + EXCLUDED.view_count;

INSERT 0 1

Time: 2787.081 ms
```

要定期更新聚合，必须记录事实表中哪些行已经处理，以免重复计数。基本方法是聚合到当前时间，将时间戳存入表中，下次运行时从该时间戳继续。但要注意，可能仍有时间戳更早的请求尚未完成，尤其是通过 COPY 批量导入时。因此，应只汇总到略早于当前时间的某个时间点，并假定此前的请求都已完成。可以很容易地将这套逻辑写成 PL/pgSQL 函数：

```sql
CREATE TABLE aggregations (name regclass primary key, last_update timestamp);
INSERT INTO aggregations VALUES ('daily_page_views', now());

CREATE OR REPLACE FUNCTION compute_daily_view_counts()
RETURNS void LANGUAGE plpgsql AS $function$
DECLARE
  start_time timestamp;
  end_time timestamp := now() - interval '1 minute'; -- exclude in-flight requests
BEGIN
  SELECT last_update INTO start_time FROM aggregations WHERE name = 'daily_page_views'::regclass;
  UPDATE aggregations SET last_update = end_time WHERE name = 'daily_page_views'::regclass;

  EXECUTE $$
    INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
      SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
      FROM page_views
      WHERE view_time >= $1 AND view_time < $2
      GROUP BY tenant_id, view_time::date, page_id
      ON CONFLICT (tenant_id, day, page_id) DO UPDATE SET
      view_count = daily_page_views.view_count + EXCLUDED.view_count$$
  USING start_time, end_time;
END;
$function$;
```

创建函数后，定期调用 `SELECT compute_daily_view_counts()`，即可持续更新聚合，延迟约 1–2 分钟。更高级的方法可以将延迟降到几秒。

本例仅使用一个由数据库生成的时间列。不过，最好区分事件在源端发生的时间，以及由数据库生成的摄取时间；后者用于判断事件是否已经处理。

使用 `page_id` 而不是 URL，可以避免为每次页面访问都存储 URL 的开销，让性能数据更好看。借助 Citus，通常可以避免那些不支持连接的分布式数据库所带来的反规范化开销。你可以将页面的静态详情放在另一张表中，再进行连接：

```sql
CREATE TABLE pages (
    tenant_id int,
    page_id int,
    url text,
    language varchar(2),
    primary key (tenant_id, page_id)
);

SELECT create_distributed_table('pages', 'tenant_id');

... insert pages ...

-- Most views in the past week
SELECT url, view_count
FROM daily_page_views JOIN pages USING (tenant_id, page_id)
WHERE tenant_id = 5 AND day >= date '2016-11-23'
ORDER BY view_count DESC LIMIT 3;
   url    | view_count
----------+------------
 /home    |         99
 /contact |         95
 /product |         93
(3 rows)

Time: 7.042 ms
```

也可以在 `INSERT..SELECT` 命令中执行连接，创建更细致的聚合，例如按语言聚合。

分布式聚合为 Citus 应对大数据问题的工具箱又添了一件工具。借助并行 `INSERT .. SELECT`、并行索引创建、并行查询等诸多功能，Citus 不仅能横向扩展多租户数据库，还能将数据管道中的多个不同环节统一到一个平台上。

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
