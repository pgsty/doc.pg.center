---
title: 具有半结构化数据的分片 PostgreSQL 及其性能影响
description: 了解如何使用 Citus 为 PostgreSQL 分片半结构化数据，以便优化性能和可伸缩性。
weight: 100
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/semi-structured-data?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: JSONB 与分片
---

**原始文章：** [Craig Kerstiens · 2016 年 7 月 25 日](https://www.citusdata.com/blog/2016/07/25/sharding-json-in-postgres-and-performance/)。中文整理：[PGSTY](https://pgsty.com/)。

Citus 可以帮助你突破单节点数据库的限制。数据量低于 100 GB 时，单个 PostgreSQL 实例通常就能很好地工作。规模更大时，Citus 可以提供帮助，但数据建模方式会影响系统性能。

有些应用天然适合横向扩展的模型，有些则需要调整应用。你选择的模型决定了哪些查询能够高效执行。可以从两个方面着手：

- 检查当前数据已经采用了怎样的模型。
- 分析希望运行的查询及其性能需求，以此判断哪种数据模型最合适。

## 一张大表，无需连接 {#one-large-table-without-joins}

用 JSONB 存储半结构化数据，有助于减少所需的表数量，提高可扩展性。例如，传统的 Web 分析数据通常用一张事件表保存最少的信息，再用查找表关联事件并记录额外信息。有些事件的附加信息比其他事件更多。将这些查找表替换为 JSONB 列后，仍然可以高效地查询和筛选。例如：

```sql
CREATE TABLE visits AS (
  id UUID,
  site_id uuid,
  visited_at TIMESTAMPTZ,
  session_id UUID,
  page TEXT,
  url_params JSONB
)
```

事件的 URL 参数是不固定的，不能保证任何参数一定存在。常见的“utm”参数，如 `utm_source`、`utm_medium`、`utm_campaign`，也并非总是出现。使用 [JSONB](https://www.citusdata.com/blog/2016/07/14/choosing-nosql-hstore-json-jsonb/) 类型的 `url_params` 列，比为每个参数单独创建列更方便。JSONB 提供了灵活的模式；再配合 [GIN 索引](https://www.postgresql.org/docs/current/static/gin.html)，就能高效查询所有键和值，无需逐一为它们建立索引。

## Citus 如何支持扩展 {#how-citus-supports-scaling}

如果确实需要突破单节点的限制，[Citus](https://www.citusdata.com/product/) 可以帮助你横向扩展处理能力、内存和存储。开始使用 Citus 时，先创建模式，再告诉系统希望如何对数据进行分片。

要确定理想的分片键，需要检查查询负载和计划执行的操作类型。如果存储的是聚合数据，且所有查询都按客户进行，那么 `customer_id` 或 `tenant_id` 这样的分片键就很合适。即使数据按分钟汇总、报表按天生成，这种方式也能很好地工作。查询可以只路由到该客户对应的分片。将查询路由到单个分片，也能支持更高的并发量。

如果存储的是原始数据，每个客户的数据量都很大，那么在不进一步并行化单个客户查询的情况下，要实现亚秒级响应就会更困难。客户数量较少，或者 80% 的数据来自同一客户时，也可能难以稳定获得亚秒级响应。在这些情况下，选择比客户或租户 ID 粒度更细的分片键，可能更合适。

数据分布和查询负载，在很大程度上决定了哪种键适合你。

在前面的例子中，如果所有站点的流量相当，`site_id` 可能是合理选择。但如果存在上述任一种情况，`session_id` 这样的分布键就更理想。

## 查询负载 {#the-query-workload}

以 `session_id` 作为分片键，可以方便地执行许多查询，例如：

查询指定站点过去七天访问量最高的页面：

```sql
SELECT page,
       count(*)
FROM visits
WHERE site_id = 'foo'
  AND visited_at > now() - '7 days'::interval
GROUP BY page
ORDER BY 2 DESC;
```

查询今天的去重会话数：

```sql
SELECT distinct(session_id)
FROM visits
WHERE site_id = 'foo'
  AND visited_at > date_trunc('date', now())
```

如果在 `url_params` 上建立了索引，就可以方便地执行各种汇总，例如找出过去 30 天带来最多流量的营销活动，以及从中受益最多的页面：

```sql
SELECT url_params ->> 'utm_campaign',
       page,
       count(*)
FROM visits
WHERE url_params ? 'utm_campaign'
  AND visited_at >= now() - '30 days'::interval
  AND site_id = 'foo'
GROUP BY url_params ->> 'utm_campaign',
         page
ORDER BY 3 DESC;
```

## 优化数据分布 {#optimizing-distribution}

如果目标是充分发挥数据库的并行能力，让分片数与核心数相匹配，可以确保每个查询都能利用这些资源。相反，如果目标是提高读取并发量，那么让查询只访问单个分片，就能同时运行更多查询，尽管单个查询的并行度会较低。

## 带 COLUMNS 的 JSON_TABLE()（PostgreSQL 18） {#json_table-with-columns-postgresql-18}

PostgreSQL 18 通过 `JSON_TABLE(... COLUMNS ...)` 扩展了 SQL/JSON，允许一次从 JSON 文档中提取多个具有指定类型的字段。Citus 14 在分布式查询中完整支持这一语法。

```sql
CREATE TABLE pg18_json_test (id serial PRIMARY KEY, data json);
SELECT create_distributed_table('pg18_json_test', 'id');

INSERT INTO pg18_json_test (data) VALUES
  ('{"user": {"name": "Alice",   "age": 30, "city": "San Diego"}}'),
  ('{"user": {"name": "Bob",     "age": 25, "city": "Los Angeles"}}'),
  ('{"user": {"name": "Charlie", "age": 35, "city": "Los Angeles"}}');

SELECT jt.name, jt.age
FROM pg18_json_test,
     JSON_TABLE(
       data,
       '$.user'
       COLUMNS (
         age  INT  PATH '$.age',
         name TEXT PATH '$.name'
       )
     ) AS jt
WHERE jt.age BETWEEN 25 AND 35
ORDER BY jt.age, jt.name;
```

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [可扩展的实时产品搜索](/citus/articles/faceted-search/)
