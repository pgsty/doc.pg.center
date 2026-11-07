---
title: 导入和修改数据（DML）
description: 介绍如何使用 Citus 的数据修改语言（DML）导入和修改数据。
weight: 70
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/reference-dml?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

以下各节介绍如何在 Citus 中使用数据修改语言（DML）导入和修改数据。

## 插入数据 {#inserting-data}

可以使用标准的 PostgreSQL [INSERT](http://www.postgresql.org/docs/current/static/sql-insert.html) 命令向分布式表插入数据。下面从 GitHub Archive 数据集中随机选取两行作为示例。

```sql
/*
CREATE TABLE github_events
(
  event_id bigint,
  event_type text,
  event_public boolean,
  repo_id bigint,
  payload jsonb,
  repo jsonb,
  actor jsonb,
  org jsonb,
  created_at timestamp
);
*/

INSERT INTO github_events VALUES (2489373118,'PublicEvent','t',24509048,'{}','{"id": 24509048, "url": "https://api.github.com/repos/SabinaS/csee6868", "name": "SabinaS/csee6868"}','{"id": 2955009, "url": "https://api.github.com/users/SabinaS", "login": "SabinaS", "avatar_url": "https://avatars.githubusercontent.com/u/2955009?", "gravatar_id": ""}',NULL,'2015-01-01 00:09:13');

INSERT INTO github_events VALUES (2489368389,'WatchEvent','t',28229924,'{"action": "started"}','{"id": 28229924, "url": "https://api.github.com/repos/inf0rmer/blanket", "name": "inf0rmer/blanket"}','{"id": 1405427, "url": "https://api.github.com/users/tategakibunko", "login": "tategakibunko", "avatar_url": "https://avatars.githubusercontent.com/u/1405427?", "gravatar_id": ""}',NULL,'2015-01-01 00:00:24');
```

向分布式表插入行时，必须指定该行的分布列。Citus 根据分布列确定应将插入操作路由到哪个分片，然后将查询转发到该分片，在其所有副本上执行远程插入命令。

有时将多个插入语句合并成一条多行插入语句会更方便，也可能比反复向数据库发起查询更高效。例如，上一节的数据可以这样一次性加载：

```sql
INSERT INTO github_events VALUES
  (
    2489373118,'PublicEvent','t',24509048,'{}','{"id": 24509048, "url": "https://api.github.com/repos/SabinaS/csee6868", "name": "SabinaS/csee6868"}','{"id": 2955009, "url": "https://api.github.com/users/SabinaS", "login": "SabinaS", "avatar_url": "https://avatars.githubusercontent.com/u/2955009?", "gravatar_id": ""}',NULL,'2015-01-01 00:09:13'
  ), (
    2489368389,'WatchEvent','t',28229924,'{"action": "started"}','{"id": 28229924, "url": "https://api.github.com/repos/inf0rmer/blanket", "name": "inf0rmer/blanket"}','{"id": 1405427, "url": "https://api.github.com/users/tategakibunko", "login": "tategakibunko", "avatar_url": "https://avatars.githubusercontent.com/u/1405427?", "gravatar_id": ""}',NULL,'2015-01-01 00:00:24'
  );
```

### “From Select”子句（分布式汇总） {#from-select-clause-distributed-rollups}

Citus 也支持 `INSERT ... SELECT` 语句，根据查询结果插入行。这种语句便于填充表，还能配合 `ON CONFLICT` 子句进行*插入或更新（upsert）*，是实现分布式汇总最简单的方式。

Citus 有三种执行 `INSERT ... SELECT` 语句的方式。第一种适用于源表与目标表共置，且查询和插入语句都包含分布列的情况。此时 Citus 可以将 `INSERT ... SELECT` 语句下推到所有节点并行执行。

执行 `INSERT ... SELECT` 的第二种方式是将结果集重新分区为多个数据块，在工作节点之间发送这些数据块，将它们送到匹配的目标表分片。每个工作节点随后将数据插入本地目标分片。

只有 SELECT 查询不需要在协调节点上进行合并时，才能采用重新分区优化。以下 SQL 功能需要合并步骤，因此不适用：

- ORDER BY
- LIMIT
- OFFSET
- GROUP BY 的分组键不包含分布列。
- 窗口函数按源表中的非分布列分区。
- 非共置表之间的连接，即重分区连接。

如果源表与目标表不共置，而且无法应用重新分区优化，Citus 就采用第三种方式：从工作节点查询结果并将数据拉取到协调节点，再由协调节点将各行转发到相应分片。所有数据都必须经过一个节点，因此这种方式效率较低。

如果不确定 Citus 使用了哪种方式，可以使用 EXPLAIN 命令查看。目标表分片数过多时，禁用重新分区可能更合适，参见 [`citus.enable_repartitioned_insert_select (boolean)`](/citus/reference/api-guc/)。

### COPY 命令（批量加载） {#copy-command-bulk-load}

要从文件批量加载数据，可以直接使用 PostgreSQL 的 [\COPY 命令](http://www.postgresql.org/docs/current/static/app-psql.html#APP-PSQL-META-COMMANDS-COPY)。

首先运行以下命令下载示例 github_events 数据集：

```bash
wget http://examples.citusdata.com/github_archive/github_events-2015-01-01-{0..5}.csv.gz
gzip -d github_events-2015-01-01-*.gz
```

然后使用 psql 复制数据。注意，这些数据要求数据库使用 UTF8 编码。

```psql
\COPY github_events FROM 'github_events-2015-01-01-0.csv' WITH (format CSV)
```

> [!NOTE]
> 分片之间没有快照隔离，因此与 COPY 并发运行的多分片 SELECT 可能看到部分分片上已提交的数据，而其他分片上尚未提交。如果存储的是事件数据，最近的数据中可能偶尔出现小段缺失。如果这会造成问题，应用需要自行处理，例如在查询中排除最新数据，或使用某种锁。
> 
> 如果 COPY 无法为某个分片放置建立连接，它的行为与 INSERT 相同：将该放置标记为非活动，除非这样会导致不再有活动放置。如果连接建立后发生其他故障，事务会回滚，因此不会修改元数据。

## 通过汇总缓存聚合结果 {#caching-aggregations-with-rollups}

事件数据流水线、实时仪表盘等应用需要在大量数据上实现亚秒级查询。一种加快查询的方法是预先计算并保存聚合结果。这称为数据*汇总（rollup）*，可以避免运行时处理原始数据的开销。将时序数据汇总为每小时或每天的统计值还可以节省空间：当不再需要完整明细、聚合结果已足够时，就可以删除旧数据。

例如，下面这个分布式表按 URL 跟踪页面浏览量：

```sql
CREATE TABLE page_views (
  site_id int,
  url text,
  host_ip inet,
  view_time timestamp default now(),

  PRIMARY KEY (site_id, url)
);

SELECT create_distributed_table('page_views', 'site_id');
```

填入数据后，可以运行聚合查询，在指定站点和年份范围内，按 URL 和日期统计页面浏览量。

```sql
-- how many views per url per day on site 5?
SELECT view_time::date AS day, site_id, url, count(*) AS view_count
  FROM page_views
  WHERE site_id = 5 AND
    view_time >= date '2016-01-01' AND view_time < date '2017-01-01'
  GROUP BY view_time::date, site_id, url;
```

这种做法可行，但有两个缺点。首先，每次运行聚合查询，都必须遍历所有相关行并重新计算整个数据集的结果。若用它来展示仪表盘，将聚合结果保存在每日页面浏览量表中，再查询该表，会更快。其次，存储成本随数据量和可查询历史的长度成比例增长。实际应用中，可能只需短期保留原始事件，却希望查看更长时间范围的历史图表。

为获得这些好处，可以创建 `daily_page_views` 表，存储每日统计信息。

```sql
CREATE TABLE daily_page_views (
  site_id int,
  day date,
  url text,
  view_count bigint,
  PRIMARY KEY (site_id, day, url)
);

SELECT create_distributed_table('daily_page_views', 'site_id');
```

本例中，`page_views` 和 `daily_page_views` 都按 `site_id` 列分布，保证同一站点的数据共置在同一个节点上。将两个表的相关行保存在同一节点，可以最大限度地减少节点间的网络流量，并实现高度并行的执行。

创建新的分布式表后，就可以运行 `INSERT INTO ... SELECT`，将原始页面浏览记录汇总到聚合表中。下面的示例按天聚合浏览量。Citus 用户通常会在一天结束后再等待一段时间才运行这类查询，以容纳迟到的数据。

```sql
-- roll up yesterday's data
INSERT INTO daily_page_views (day, site_id, url, view_count)
  SELECT view_time::date AS day, site_id, url, count(*) AS view_count
  FROM page_views
  WHERE view_time >= date '2017-01-01' AND view_time < date '2017-01-02'
  GROUP BY view_time::date, site_id, url;

-- now the results are available right out of the table
SELECT day, site_id, url, view_count
  FROM daily_page_views
  WHERE site_id = 5 AND
    day >= date '2016-01-01' AND day < date '2017-01-01';
```

此汇总查询聚合前一天的数据并插入 `daily_page_views`。每天运行一次就无需更新汇总表中已有的行，因为新一天的数据不会影响以前的行。

如果存在迟到数据，或者每天执行多次汇总查询，情况就不同了。当新行的日期已经存在于汇总表中时，相应计数应该增加。PostgreSQL 可以通过 `ON CONFLICT` 处理这种情况，这也是它实现[插入或更新（upsert）](https://www.postgresql.org/docs/current/static/sql-insert.html#SQL-ON-CONFLICT)的方式。示例如下。

```sql
-- roll up from a given date onward,
-- updating daily page views when necessary
INSERT INTO daily_page_views (day, site_id, url, view_count)
  SELECT view_time::date AS day, site_id, url, count(*) AS view_count
  FROM page_views
  WHERE view_time >= date '2017-01-01'
  GROUP BY view_time::date, site_id, url
  ON CONFLICT (day, url, site_id) DO UPDATE SET
    view_count = daily_page_views.view_count + EXCLUDED.view_count;
```

## 更新和删除 {#updates-and-deletion}

可以使用标准 PostgreSQL [UPDATE](http://www.postgresql.org/docs/current/static/sql-update.html) 和 [DELETE](http://www.postgresql.org/docs/current/static/sql-delete.html) 命令更新或删除分布式表中的行。

```sql
DELETE FROM github_events
WHERE repo_id IN (24509048, 24509049);

UPDATE github_events
SET event_public = TRUE
WHERE (org->>'id')::int = 5430905;
```

如果更新或删除像上例一样涉及多个分片，Citus 默认使用一阶段提交协议。为提高安全性，可以通过以下设置启用两阶段提交：

```sql
SET citus.multi_shard_commit_protocol = '2pc';
```

如果更新或删除只影响一个分片，就会在单个工作节点内执行，此时无需启用两阶段提交（2PC）。按表的分布列过滤更新或删除操作时，经常会出现这种情况：

```sql
-- since github_events is distributed by repo_id,
-- this will execute in a single worker node

DELETE FROM github_events
WHERE repo_id = 206084;
```

此外，处理单个分片时，Citus 支持 `SELECT ... FOR UPDATE`。对象关系映射器（ORM）有时使用这种方式安全地完成以下步骤：

1. 加载行。
2. 在应用代码中进行计算。
3. 根据计算结果更新行。

选择待更新行时会对这些行加写锁，防止其他进程造成*丢失更新*异常。

```sql
BEGIN;

  -- select events for a repo, but
  -- lock them for writing
  SELECT *
  FROM github_events
  WHERE repo_id = 206084
  FOR UPDATE;

  -- calculate a desired value event_public using
  -- application logic that uses those rows...

  -- now make the update
  UPDATE github_events
  SET event_public = :our_new_value
  WHERE repo_id = 206084;

COMMIT;
```

此功能仅支持哈希分布表和参考表。

## 最大化写入性能 {#maximizing-write-performance}

在大型机器上，INSERT 和 UPDATE/DELETE 语句都可以扩展到每秒约 50,000 次查询。不过，要达到这一速率，需要使用大量并行的长连接，并考虑如何处理锁竞争。更多信息参见性能文档中的[横向扩展数据导入](/citus/operations/performance-tuning/)部分。

## 相关内容 {#related-content}

- [数据定义语言（DDL）操作参考](/citus/reference/reference-ddl/)
- [SQL 参考](/citus/reference/reference-sql/)
- [Citus SQL 参考概述](/citus/reference/)
