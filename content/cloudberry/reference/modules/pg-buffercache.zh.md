---
title: pg_buffercache
description: pg_buffercache 用于实时检查共享缓冲区缓存的状态。
weight: 190
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/pg-buffercache.md
---

`pg_buffercache` 模块用于实时检查共享缓冲区缓存的状态。

Apache Cloudberry 的 `pg_buffercache` 模块基于 PostgreSQL 的 `pg_buffercache` 模块。除报告当前连接实例信息的 PostgreSQL 视图和函数外，它还提供以 `gp_` 为前缀的视图，从 Coordinator 和所有主 Segment 收集相同的信息。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `pg_buffercache`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION pg_buffercache;
```

默认情况下，只有超级用户和 `pg_monitor` 角色的成员可以访问此模块的视图和函数。

## 单个实例的视图和函数 {#views-and-functions-for-a-single-instance}

这些对象报告执行查询的实例的共享缓冲区信息。在普通会话中查询时，该实例就是 Coordinator。

| 对象 | 说明 |
|--------|-------------|
| `pg_buffercache` 视图、`pg_buffercache_pages()` 函数 | 每个共享缓冲区返回一行。 |
| `pg_buffercache_summary` 视图、`pg_buffercache_summary()` 函数 | 返回一行，汇总共享缓冲区缓存状态。 |
| `pg_buffercache_usage_counts` 视图、`pg_buffercache_usage_counts()` 函数 | 每个使用计数值返回一行。 |

`pg_buffercache` 视图包含以下列：

| 列 | 类型 | 说明 |
|--------|------|-------------|
| `bufferid` | `integer` | 缓冲区 ID，范围为 1 到 `shared_buffers`。 |
| `relfilenode` | `oid` | 关系的文件节点编号。 |
| `reltablespace` | `oid` | 关系的表空间 OID。 |
| `reldatabase` | `oid` | 关系的数据库 OID。 |
| `relforknumber` | `smallint` | 关系内的分支编号。 |
| `relblocknumber` | `bigint` | 关系内的页面编号。 |
| `isdirty` | `boolean` | 页面是否为脏页。 |
| `usagecount` | `smallint` | 时钟扫描算法的访问计数。 |
| `pinning_backends` | `integer` | 固定此缓冲区的后端数。 |

`pg_buffercache_summary` 视图包含以下列：

| 列 | 类型 | 说明 |
|--------|------|-------------|
| `buffers_used` | `integer` | 已用共享缓冲区数。 |
| `buffers_unused` | `integer` | 未用共享缓冲区数。 |
| `buffers_dirty` | `integer` | 脏共享缓冲区数。 |
| `buffers_pinned` | `integer` | 已固定共享缓冲区数。 |
| `usagecount_avg` | `double precision` | 已用共享缓冲区的平均使用计数。 |

`pg_buffercache_usage_counts` 视图包含以下列：

| 列 | 类型 | 说明 |
|--------|------|-------------|
| `usage_count` | `integer` | 缓冲区可能的使用计数值。 |
| `buffers` | `integer` | 具有此使用计数的缓冲区数。 |
| `dirty` | `integer` | 具有此使用计数的脏缓冲区数。 |
| `pinned` | `integer` | 具有此使用计数的已固定缓冲区数。 |

查询汇总视图和使用计数视图的开销远低于查询 `pg_buffercache`。

## 集群范围的视图 {#cluster-wide-views}

| 视图 | 说明 |
|------|-------------|
| `gp_buffercache` | Coordinator 和每个主 Segment 的 `pg_buffercache` 行。 |
| `gp_buffercache_summary` | Coordinator 和每个主 Segment 的 `pg_buffercache_summary` 行，每个实例一行。 |
| `gp_buffercache_usage_counts` | Coordinator 和每个主 Segment 的 `pg_buffercache_usage_counts` 行。 |
| `gp_buffercache_summary_aggregated` | 将所有实例的 `gp_buffercache_summary` 汇总为一行：各缓冲区计数器之和，以及 `usagecount_avg` 的平均值。 |
| `gp_buffercache_usage_counts_aggregated` | 返回一行，包含 `gp_buffercache_usage_counts` 各列之和，其中也包括 `usage_count` 列本身；它不是按使用计数分组的明细。 |

前三个视图在对应 `pg_` 视图的列之前增加 `gp_segment_id` 列。Coordinator 的 `gp_segment_id` 值为 `-1`。

## 示例 {#examples}

显示每个实例的缓冲区缓存摘要：

```sql
SELECT * FROM gp_buffercache_summary;
```

显示整个集群的合计：

```sql
SELECT * FROM gp_buffercache_summary_aggregated;
```

统计每个实例上的脏缓冲区数：

```sql
SELECT gp_segment_id, count(*) AS dirty_buffers
FROM gp_buffercache
WHERE isdirty
GROUP BY gp_segment_id
ORDER BY gp_segment_id;
```

## 模块文档 {#module-documentation}

`pg_buffercache` 视图的更多信息，参见 PostgreSQL 文档中的 [pg_buffercache](https://www.postgresql.org/docs/14/pgbuffercache.html)。汇总和使用计数函数在 PostgreSQL 16 中加入，说明见 [PostgreSQL 16 文档](https://www.postgresql.org/docs/16/pgbuffercache.html)。
