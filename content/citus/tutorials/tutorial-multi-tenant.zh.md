---
title: 多租户应用
description: 在 Citus 上为多租户 SaaS 负载建模、分布数据、高效加载查询并进行集群运维。
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/tutorial-multi-tenant?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

本指南将原来的概念页（“multitenant”）与教程页（“tutorial-multi-tenant”）合并为一份端到端资源，介绍如何：（1）设计并分布 SaaS 模式；（2）高效加载和查询数据；（3）在生产规模下运维。运维内容包括模式变更、共享数据、再平衡、租户隔离和 JSONB 定制。

> [!NOTE]
> 本文假定你已经有一个 Citus 集群（Azure Database for PostgreSQL 弹性集群或自建集群），并能通过 `psql` 访问协调节点。如果还没有本地环境，请先阅读[快速入门](/citus/installation/getting-started/)。

## 1. 了解多租户设计模式 {#1-understand-the-pattern}

多租户 SaaS 应用在共享数据库中保存多个客户（租户）的数据，同时为每个租户提供隔离视图。Citus 保留普通 PostgreSQL 的语义——模式、连接、约束和事务——并通过将表分片到多个工作节点实现横向扩展。

目标：

| 目标 | Citus 的帮助 |
| --- | --- |
| 快速执行按租户的 OLTP 与分析 | 将租户数据共置在同一节点，避免跨节点通信。 |
| 简化运维 | 使用单一逻辑 PostgreSQL 端点、标准 SQL 和驱动。 |
| 弹性增长 | 添加节点，在线再平衡分片。 |
| 处理租户数据倾斜 | 将大租户隔离到专用分片与节点。 |
| 每租户自定义字段 | 通过 JSONB 和部分/GIN 索引实现。 |

## 2. 示例广告分析模式 {#2-sample-ad-analytics-schema}

使用广告分析负载（公司 → 广告活动 → 广告，以及点击和展示事实表）。先建立简化的单机风格初始模式，再进行分布调整：

```sql
CREATE TABLE companies (
  id bigserial PRIMARY KEY,
  name text NOT NULL,
  image_url text,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
CREATE TABLE campaigns (
  id bigserial PRIMARY KEY,
  company_id bigint REFERENCES companies(id),
  name text NOT NULL,
  cost_model text NOT NULL,
  state text NOT NULL,
  monthly_budget bigint,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
CREATE TABLE ads (
  id bigserial PRIMARY KEY,
  campaign_id bigint REFERENCES campaigns(id),
  name text NOT NULL,
  image_url text,
  target_url text,
  impressions_count bigint DEFAULT 0,
  clicks_count bigint DEFAULT 0,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
```

> [!NOTE] 示例范围
> 上游教程省略了部分表定义，包括 `clicks` 和 `impressions`，并展示了 `ads` 的不同版本。这些片段用于说明建模方法，不能作为同一个脚本从头到尾执行。已有应用需要如何调整分布键与约束，请参阅[模式迁移](/citus/migration/migration-schema/)。

### 分布原则 {#distribution-principle}

选择一个租户标识（这里是 `company_id`），并确保每张表都直接包含该列，或可以通过包含该列的外键链连接。为增强约束与路由性能，可将分布列放入复合主键和外键对中。

## 3. 让模式适合分布 {#3-make-the-schema-distribution-friendly}

调整表结构，使主键和外键包含 `company_id`（或等价列）。下面是事实表的最终形式示例：

```sql
CREATE TABLE ads (
  id bigserial,
  company_id bigint,
  campaign_id bigint,
  name text NOT NULL,
  image_url text,
  target_url text,
  impressions_count bigint DEFAULT 0,
  clicks_count bigint DEFAULT 0,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  PRIMARY KEY (company_id, id),
  FOREIGN KEY (company_id, campaign_id) REFERENCES campaigns(company_id, id)
);
```

对其他表重复这一过程（参见原概念示例），使每个租户值对应的分布式连接和约束都能在一个工作节点上本地执行。

## 4. 创建并分布表 {#4-create-and-distribute-tables}

> [!NOTE] 示例端口
> 上游示例使用本地协调节点的 **9700** 端口，而软件包安装指南使用 PostgreSQL 默认的 **5432** 端口。请连接自己协调节点配置的端口；以下命令保留上游示例端口。

连接到协调节点（原生安装使用 9700 端口；下面展示 Docker 示例）：

```bash
docker exec -it citus psql -U postgres
```

创建调整后的表，再将其分片：

```sql
SELECT create_distributed_table('companies',   'id');        -- small dimension; distributing by id ok
SELECT create_distributed_table('campaigns',   'company_id');
SELECT create_distributed_table('ads',         'company_id');
SELECT create_distributed_table('clicks',      'company_id');
SELECT create_distributed_table('impressions', 'company_id');
```

为什么 `companies` 使用 `id`，而其他表使用 `company_id`？公司行数较少，使用主键可以避免额外反规范化。下游表仍会通过 `company_id` 实现共置。

## 5. 加载示例数据 {#5-load-sample-data}

下载 CSV：

```bash
for f in companies campaigns ads clicks impressions geo_ips; do \
  curl -O https://examples.citusdata.com/mt_ref_arch/${f}.csv; \
done
```

如果使用 Docker，将文件复制到容器中：

```bash
for f in companies campaigns ads clicks impressions geo_ips; do \
  docker cp ${f}.csv citus:. ; \
done
```

在 psql 中执行：

```psql
\copy companies   from 'companies.csv'   with csv
\copy campaigns   from 'campaigns.csv'   with csv
\copy ads         from 'ads.csv'         with csv
\copy clicks      from 'clicks.csv'      with csv
\copy impressions from 'impressions.csv' with csv
```

## 6. 按租户查询与事务 {#6-per-tenant-queries-and-transactions}

带有 `WHERE company_id = ?` 的查询（以及受约束的连接）会路由到单个工作节点。所有 SQL 功能仍可使用，包括连接、窗口函数和事务：

```sql
SELECT name, cost_model, state, monthly_budget
FROM campaigns
WHERE company_id = 5
ORDER BY monthly_budget DESC
LIMIT 10;

UPDATE campaigns
SET monthly_budget = monthly_budget - 2
WHERE company_id = 5;

BEGIN;
UPDATE campaigns SET monthly_budget = monthly_budget + 1000 WHERE company_id = 5 AND id = 40;
UPDATE campaigns SET monthly_budget = monthly_budget - 1000 WHERE company_id = 5 AND id = 41;
COMMIT;
```

### 分布式函数，减少往返 {#distributed-functions-reduce-round-trips}

将按租户执行的多条语句封装进函数，并将其标记为分布式：

```sql
CREATE OR REPLACE FUNCTION delete_campaign(company_id int, campaign_id int)
RETURNS void LANGUAGE plpgsql AS $fn$
BEGIN
  DELETE FROM ads       WHERE campaign_id = delete_campaign.campaign_id AND company_id = delete_campaign.company_id;
  DELETE FROM campaigns WHERE id = campaign_id AND company_id = delete_campaign.company_id;
END; $fn$;

SELECT create_distributed_function('delete_campaign(int,int)', 'company_id', colocate_with := 'campaigns');
SELECT delete_campaign(5, 46);
```

### 丰富的分析示例 {#rich-analytics-example}

```sql
SELECT a.campaign_id,
       RANK() OVER (PARTITION BY a.campaign_id ORDER BY count(*) DESC) AS rnk,
       count(*) AS n_impressions,
       a.id
FROM ads a
JOIN impressions i
  ON i.company_id = a.company_id
 AND i.ad_id      = a.id
WHERE a.company_id = 5
GROUP BY a.campaign_id, a.id
ORDER BY a.campaign_id, n_impressions DESC;
```

## 7. 共享参考表 {#7-shared-reference-tables}

有些查找数据应对所有租户可见，但不应重复保存。使用参考表，每个工作节点都会保留一份同步的完整副本：

```sql
CREATE TABLE geo_ips (
  addrs cidr PRIMARY KEY,
  latlon point NOT NULL CHECK (-90 <= latlon[0] AND latlon[0] <= 90 AND -180 <= latlon[1] AND latlon[1] <= 180)
);
CREATE INDEX ON geo_ips USING gist(addrs inet_ops);
SELECT create_reference_table('geo_ips');
\copy geo_ips from 'geo_ips.csv' with csv
```

查询时，参考表已复制，因此按租户连接仍可在本地完成：

```sql
SELECT c.id, clicked_at, latlon
FROM geo_ips, clicks c
WHERE addrs >> c.user_ip
  AND c.company_id = 5
  AND c.ad_id = 290;
```

## 8. 在线模式变更 {#8-online-schema-changes}

在协调节点上执行的 DDL 会通过两阶段提交原子地传播到工作节点：

```sql
ALTER TABLE ads ADD COLUMN caption text;
```

详情与限制见[创建和修改分布式对象（DDL）](/citus/reference/reference-ddl/)。

## 9. 用 JSONB 实现每租户定制 {#9-per-tenant-customization-with-jsonb}

将可变属性存入 JSONB，并按需建立索引：

```sql
SELECT user_data->>'is_mobile' AS is_mobile, count(*)
FROM clicks
WHERE company_id = 5
GROUP BY user_data->>'is_mobile'
ORDER BY count DESC;

CREATE INDEX click_user_data_is_mobile ON clicks ((user_data->>'is_mobile')) WHERE company_id = 5;
CREATE INDEX click_user_data ON clicks USING gin(user_data);
```

## 10. 横向扩容与再平衡 {#10-scaling-out-and-rebalancing}

添加工作节点（通过门户或 `citus_add_node`），再重新平衡分片：

```sql
SELECT citus_rebalance_start();
```

再平衡期间读取仍可继续。具体取决于发行方式和版本：正在移动的分片可能短暂阻塞写入（社区版本），也可能允许写入继续进行（云服务文章或较新的版本所述行为）。

## 11. 处理大型热点租户 {#11-handling-large-hot-tenants}

租户规模通常呈 Zipf 分布：少数租户占据大部分容量和流量。可将大型租户隔离到专用分片（以及可选的专用节点）：

```sql
SELECT isolate_tenant_to_new_shard('companies', 5, 'CASCADE') AS shard_id;  -- returns shard id
```

随后将该分片（及级联的相关分片）移动到指定节点。请确保 `wal_level >= logical`：

```sql
SELECT citus_move_shard_placement(
  <shard_id>,
  'source_host', source_port,
  'dest_host',   dest_port
);
```

通过查询 `pg_dist_placement` 验证结果。

## 12. 下一步 {#12-next-steps}

你已经在 Citus 上构建了可横向扩展的多租户应用，保留丰富的 SQL 语义并支持租户隔离。接下来可阅读迁移指南、框架集成和高级运维模式：

- 迁移现有模式：[识别分布策略](/citus/migration/migration-schema/)。
- 添加框架集成：[Django](https://docs.citusdata.com/en/v8.1/develop/migration_mt_django.html) 或 [ASP.NET](/citus/migration/migration-asp/)。
- 使用 [Citus 工具函数](/citus/reference/api-udf/)，例如 `isolate_tenant_to_new_shard`。
- 在 Azure 上体验：[Azure Database for PostgreSQL Flexible server 弹性集群](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508)。

本文取代了此前分开的概念与教程页面。

## 相关内容 {#related-content}

- [分析与仪表盘教程](/citus/tutorials/tutorial-analytics/)
- [时序数据教程](/citus/tutorials/tutorial-time-series/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
