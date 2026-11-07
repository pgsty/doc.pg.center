---
title: 有用的诊断查询
description: 了解用于查找 Citus 节点、分片、表和连接的诊断信息的有用查询。
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/diagnostic-queries?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

## 查找哪个分片包含特定租户的数据 {#finding-which-shard-contains-data-for-a-specific-tenant}

分布式表的行被划分为分片，每个分片放置在 Citus 集群的工作节点上。在多租户场景中，结合两项信息即可确定特定租户的数据位于哪个工作节点：与租户 ID 关联的 [分片 ID](/citus/reference/api-udf/#get_shard_id_for_distribution_column)，以及分片在工作节点上的放置位置。这两项信息可以通过一条查询同时获得。假设多租户应用的租户是商店，我们要查找保存 Gap.com 数据（例如 `id=4`）的工作节点。

要找到保存商店 `id=4` 数据的工作节点，查询分布列值为 4 的行所在的分片放置：

```sql
SELECT shardid, shardstate, shardlength, nodename, nodeport, placementid
  FROM pg_dist_placement AS placement,
       pg_dist_node AS node
 WHERE placement.groupid = node.groupid
   AND node.noderole = 'primary'
   AND shardid = (
     SELECT get_shard_id_for_distribution_column('stores', 4)
   );
```

输出将包含工作节点数据库的主机和端口。

```text
┌─────────┬────────────┬─────────────┬───────────┬──────────┬─────────────┐
│ shardid │ shardstate │ shardlength │ nodename  │ nodeport │ placementid │
├─────────┼────────────┼─────────────┼───────────┼──────────┼─────────────┤
│ 102009  │          1 │           0 │ localhost │     5433 │           2 │
└─────────┴────────────┴─────────────┴───────────┴──────────┴─────────────┘
```

## 查找分布式模式所在的节点 {#finding-which-node-hosts-a-distributed-schema}

分布式模式会自动关联各自的共置组，使得在这些模式中创建的表自动转换为无需分片键的共置分布式表。连接 `citus_shards` 和 `citus_schemas` 即可查找分布式模式的位置：

```sql
select schema_name, nodename, nodeport
  from citus_shards
  join citus_schemas cs
    on cs.colocation_id = citus_shards.colocation_id
 group by 1,2,3;
```

```text
schema_name | nodename  | nodeport
-------------+-----------+----------
a           | localhost |     9701
b           | localhost |     9702
with_data   | localhost |     9702
```

也可以直接查询 `citus_shards`，筛选表类型为 *schema* 的记录，获取所有表的详细列表。

```sql
select * from citus_shards where citus_table_type = 'schema';
```

## 查找表的分布列 {#finding-the-distribution-column-for-a-table}

Citus 中的每个分布式表都有分布列。有关分布列及其工作原理，请参阅“分布式数据建模”。许多操作需要知道分布列是哪一列。例如，有些操作要求在分布列上连接或过滤，相关错误消息可能会提示“在分布列上添加过滤条件”。

协调节点上的 `pg_dist_*` 表保存分布式数据库的各类元数据。其中，`pg_dist_partition` 保存每张表的分布列信息（分布列以前称为*分区列*）。可以使用便捷的辅助函数，从底层元数据中查询分布列名称。示例及输出如下：

```sql
-- create example table

CREATE TABLE products (
  store_id bigint,
  product_id bigint,
  name text,
  price money,

  CONSTRAINT products_pkey PRIMARY KEY (store_id, product_id)
);

-- pick store_id as distribution column

SELECT create_distributed_table('products', 'store_id');

-- get distribution column name for products table

SELECT column_to_column_name(logicalrelid, partkey) AS dist_col_name
  FROM pg_dist_partition
 WHERE logicalrelid='products'::regclass;
```

示例输出：

```text
┌───────────────┐
│ dist_col_name │
├───────────────┤
│ store_id      │
└───────────────┘
```

## 检测锁 {#detecting-locks}

此查询在所有工作节点上运行，找出锁、持锁时长以及引发问题的查询：

```sql
SELECT * FROM citus_lock_waits;
```

有关详细信息，请参阅 `dist_query_activity`。

## 查询分片的大小 {#querying-the-size-of-your-shards}

此查询提供给定分布式表的每个分片的大小，此处由占位符 `my_table`指定：

```sql
SELECT shardid, table_name, shard_size
FROM citus_shards
WHERE table_name = 'my_table';
```

示例输出：

```text
 shardid | table_name | shard_size
---------+------------+------------
  102170 | my_table   |   90177536
  102171 | my_table   |   90177536
  102172 | my_table   |   91226112
  102173 | my_table   |   90177536
```

此查询使用 `citus_shards`。

## 查询所有分布式表的大小 {#querying-the-size-of-all-distributed-tables}

此查询获取每个分布式表的大小及其索引大小的列表。

```sql
SELECT table_name, table_size
  FROM citus_tables;
```

示例输出：

```text
┌───────────────┬────────────┐
│ table_name    │ table_size │
├───────────────┼────────────┤
│ github_users  │ 39 MB      │
│ github_events │ 98 MB      │
└───────────────┴────────────┘
```

可通过其他方法来度量分布式表大小。 有关详细信息，请参阅 `table_size`。

## 识别未使用的索引 {#identifying-unused-indices}

此查询在所有工作节点上运行，并标识给定分布式表的任何未使用的索引。 将占位符 `my_distributed_table` 替换为分布式表的名称。

```sql
SELECT *
FROM run_command_on_shards('my_distributed_table', $cmd$
  SELECT array_agg(a) as infos
  FROM (
    SELECT (
      schemaname || '.' || relname || '##' || indexrelname || '##'
                 || pg_size_pretty(pg_relation_size(i.indexrelid))::text
                 || '##' || idx_scan::text
    ) AS a
    FROM  pg_stat_user_indexes ui
    JOIN  pg_index i
    ON    ui.indexrelid = i.indexrelid
    WHERE NOT indisunique
    AND   idx_scan < 50
    AND   pg_relation_size(relid) > 5 * 8192
    AND   (schemaname || '.' || relname)::regclass = '%s'::regclass
    ORDER BY
      pg_relation_size(i.indexrelid) / NULLIF(idx_scan, 0) DESC nulls first,
      pg_relation_size(i.indexrelid) DESC
  ) sub
$cmd$);
```

示例输出：

```text
┌─────────┬─────────┬───────────────────────────────────────────────────────────────────────┐
│ shardid │ success │                            result                                     │
├─────────┼─────────┼───────────────────────────────────────────────────────────────────────┤
│ 102008  │ t       │                                                                       │
│ 102009  │ t       │ {"public.my_distributed_table_102009##stupid_index_102009##28 MB##0"} │
│ 102010  │ t       │                                                                       │
│ 102011  │ t       │                                                                       │
└─────────┴─────────┴───────────────────────────────────────────────────────────────────────┘
```

## 监控客户端连接数 {#monitoring-client-connection-count}

此查询按类型统计协调节点上当前打开的连接数。

```sql
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;
```

示例输出：

```text
┌────────┬───────┐
│ state  │ count │
├────────┼───────┤
│ active │     3 │
│ ∅      │     1 │
└────────┴───────┘
```

## 查看系统查询 {#viewing-system-queries}

### 活动查询 {#active-queries}

`citus_stat_activity` 视图显示当前正在执行的查询。 可以筛选视图以查找正在执行的查询及其后端的进程 ID：

```sql
SELECT global_pid, query, state
  FROM citus_stat_activity
 WHERE state != 'idle';
```

### 为什么查询正在等待 {#why-queries-are-waiting}

还可以通过查询视图来查看非空闲查询正在等待的最常见原因。 有关原因的说明，请参阅 [PostgreSQL 文档](https://www.postgresql.org/docs/current/monitoring-stats.html#WAIT-EVENT-TABLE)。

```sql
SELECT wait_event || ':' || wait_event_type AS type, count(*) AS number_of_occurences
  FROM pg_stat_activity
 WHERE state != 'idle'
GROUP BY wait_event, wait_event_type
ORDER BY number_of_occurences DESC;
```

在单独的查询中并发运行 `pg_sleep` 时，下面是示例输出：

```text
┌─────────────────┬──────────────────────┐
│      type       │ number_of_occurences │
├─────────────────┼──────────────────────┤
│ ∅               │                    1 │
│ PgSleep:Timeout │                    1 │
└─────────────────┴──────────────────────┘
```

## 索引命中率 {#index-hit-rate}

此查询提供所有节点的索引命中率。 索引命中率可用于确定查询时索引的使用频率：

```sql
-- on coordinator
SELECT 100 * (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) AS index_hit_rate
  FROM pg_statio_user_indexes;

-- on workers
SELECT nodename, result as index_hit_rate
FROM run_command_on_workers($cmd$
  SELECT 100 * (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) AS index_hit_rate
    FROM pg_statio_user_indexes;
$cmd$);
```

示例输出：

```text
┌───────────┬────────────────┐
│ nodename  │ index_hit_rate │
├───────────┼────────────────┤
│ 10.0.0.16 │ 96.0           │
│ 10.0.0.20 │ 98.0           │
└───────────┴────────────────┘
```

## 缓存命中率 {#cache-hit-rate}

大多数应用程序通常每次只访问全部数据的一小部分。PostgreSQL 将常用数据保存在内存中，避免缓慢的磁盘读取。可以在 [pg_statio_user_tables](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STATIO-ALL-TABLES-VIEW) 视图中查看相关统计信息。

一项重要指标是：工作负载读取的数据中，有多大比例来自内存缓存，而不是磁盘：

```sql
-- on coordinator
SELECT
  sum(heap_blks_read) AS heap_read,
  sum(heap_blks_hit)  AS heap_hit,
  100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_rate
FROM
  pg_statio_user_tables;

-- on workers
SELECT nodename, result as cache_hit_rate
FROM run_command_on_workers($cmd$
  SELECT
    100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_rate
  FROM
    pg_statio_user_tables;
$cmd$);
```

示例输出：

```text
┌───────────┬──────────┬─────────────────────┐
│ heap_read │ heap_hit │   cache_hit_rate    │
├───────────┼──────────┼─────────────────────┤
│         1 │      132 │ 99.2481203007518796 │
└───────────┴──────────┴─────────────────────┘
```

如果发现比率明显低于 99%，请考虑增加数据库可用的缓存。

## 相关内容 {#related-content}

- [Citus 中的集群管理](/citus/operations/cluster-management/)
- [Citus 表管理](/citus/operations/table-management/)
- [Citus 的性能优化](/citus/operations/performance-tuning/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
