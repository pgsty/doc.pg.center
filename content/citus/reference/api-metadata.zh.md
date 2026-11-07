---
title: Citus 集群元数据参考
description: 介绍 Citus 协调节点用于跟踪逻辑分片信息和统计数据的元数据表及其结构。
weight: 50
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/api-metadata?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

Citus 为 PostgreSQL 增加分布式数据库能力，并提供元数据表和视图来管理、监控分布式集群。本文介绍 Citus 用于跟踪分布式表、分片、节点配置和查询统计信息的表与视图。了解这些元数据结构，有助于监控集群健康状况、排查故障并优化分布式查询性能。

## 协调节点元数据 {#coordinator-metadata}

Citus 根据分布列将每个分布式表划分为多个逻辑分片。协调节点维护元数据表，记录这些分片的统计信息、健康状态和位置。本节介绍各元数据表及其结构。连接协调节点后，可以使用 SQL 查看和查询这些表。

### 分区表 {#partition-table}

`pg_dist_partition` 保存数据库中哪些表是分布式表的元数据。对于每个分布式表，还记录其分布方式和分布列的详细信息。

```sql
SELECT * from pg_dist_partition;
```

```text
 logicalrelid  | partmethod | partkey | colocationid | repmodel
---------------+------------+---------+--------------+----------
 github_events | h          | {VAR...}  |            2 | s
(1 row)
```

### 分片表 {#shard-table}

`pg_dist_shard` 保存每个分片的元数据，包括所属分布式表以及该分片分布列的统计信息。对于哈希分布表，元数据记录分配给分片的哈希令牌范围。协调节点在执行 `SELECT` 时，利用这些信息剪除无关分片。

```sql
SELECT * from pg_dist_shard;
```

```text
  logicalrelid | shardid | shardstorage | shardminvalue | shardmaxvalue
 --------------+---------+--------------+---------------+---------------
  github_events | 102026 | t            | 268435456     | 402653183
  github_events | 102027 | t            | 402653184     | 536870911
  github_events | 102028 | t            | 536870912     | 671088639
  github_events | 102029 | t            | 671088640     | 805306367
  (4 rows)
```

#### 分片存储类型 {#shard-storage-types}

`pg_dist_shard` 中的 `shardstorage` 列表示分片的存储类型。下表概述各种类型及其表示方式。

| 存储类型 | `shardstorage` 值 | 说明 |
| --- | --- | --- |
| TABLE | `t` | 分片存储普通分布式表的数据。 |
| COLUMNAR | `c` | 分片存储列式数据，供分布式 `cstore_fdw` 表使用。 |
| FOREIGN | `f` | 分片存储外部数据，供分布式 `file_fdw` 表使用。 |

### 分片信息视图 {#shard-information-view}

除上述底层分片元数据表外，Citus 还提供 `citus_shards` 视图，便于查看：

- 每个分片的位置，即节点和端口；
- 所属表的类型；
- 分片大小。

此视图可用于检查分片，例如查找节点间的大小不均衡问题。

```sql
SELECT * FROM citus_shards;
```

```text
 table_name | shardid | shard_name   | citus_table_type | colocation_id | nodename | nodeport | shard_size
------------+---------+--------------+------------------+---------------+----------+----------+------------
 dist       | 102170  | dist_102170  | distributed      |            34 | localhost |     9701 |   90677248
 dist       | 102171  | dist_102171  | distributed      |            34 | localhost |     9702 |   90619904
 dist       | 102172  | dist_102172  | distributed      |            34 | localhost |     9701 |   90701824
 dist       | 102173  | dist_102173  | distributed      |            34 | localhost |     9702 |   90693632
 ref        | 102174  | ref_102174   | reference        |             2 | localhost |     9701 |       8192
 ref        | 102174  | ref_102174   | reference        |             2 | localhost |     9702 |       8192
 dist2      | 102175  | dist2_102175 | distributed      |            34 | localhost |     9701 |     933888
 dist2      | 102176  | dist2_102176 | distributed      |            34 | localhost |     9702 |     950272
 dist2      | 102177  | dist2_102177 | distributed      |            34 | localhost |     9701 |     942080
 dist2      | 102178  | dist2_102178 | distributed      |            34 | localhost |     9702 |     933888
```

`colocation_id` 表示共置组。有关 `citus_table_type` 和共置组的更多信息，参见 [Citus 表视图](#citus-tables-view)和[共置组表](#colocation-group-table)。

### 分片放置表 {#shard-placement-table}

`pg_dist_placement` 跟踪分片在工作节点上的位置。一个分片在特定节点上的实例称为*分片放置*。该表记录每个分片放置的健康状态和位置。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `placementid` | bigint | 自动生成的每个放置的唯一标识符。 |
| `shardid` | bigint | 与此放置关联的分片标识符，引用 `pg_dist_shard` 目录表的 `shardid` 列。 |
| `shardstate` | int | 此放置的状态，下一节介绍不同的分片状态。 |
| `shardlength` | bigint | 对于哈希分布表，该值为零。 |
| `groupid` | int | 标识一个由一个主服务器及零个或多个备用服务器组成的组。 |

```sql
SELECT * from pg_dist_placement;
```

```text
 placementid | shardid | shardstate | shardlength | groupid
-------------+---------+------------+-------------+---------
           1 | 102008  |          1 |           0 |       1
           2 | 102008  |          1 |           0 |       2
           3 | 102009  |          1 |           0 |       2
           4 | 102009  |          1 |           0 |       3
           5 | 102010  |          1 |           0 |       3
           6 | 102010  |          1 |           0 |       4
           7 | 102011  |          1 |           0 |       4
```

> [!NOTE]
> 从 Citus 7.0 开始，类似的 `pg_dist_shard_placement` 表已弃用。该表包含每个放置的节点名称和端口：
> 
> ```sql
> SELECT * from pg_dist_shard_placement;
> ```
> 
> 现在可以通过 `groupid` 连接 `pg_dist_placement` 与 [pg_dist_node](/citus/reference/api-metadata/#worker-node-table)，获取这些信息。为保持兼容，Citus 仍提供 `pg_dist_shard_placement` 视图，但应尽可能使用新的、更加规范化的表。

### 工作节点表 {#worker-node-table}

`pg_dist_node` 包含集群中工作节点的信息。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `nodeid` | int | 自动生成的节点标识符。 |
| `groupid` | int | 标识一个由一个主服务器及零个或多个备用服务器组成的组，默认与 `nodeid` 相同。 |
| `nodename` | text | PostgreSQL 工作节点的主机名或 IP 地址。 |
| `nodeport` | int | PostgreSQL 工作节点监听的端口号。 |
| `noderack` | text | （可选）工作节点的机架位置信息。 |
| `hasmetadata` | boolean | 保留供内部使用。 |
| `isactive` | boolean | 节点是否处于活动状态并接受分片放置。 |
| `noderole` | text | 节点是主节点还是备用节点。 |
| `nodecluster` | text | （可选）工作节点的机架位置信息。 |
| `metadatasynced` | boolean | 保留供内部使用。 |
| `shouldhaveshards` | boolean | 如果为 `false`，再平衡时会迁出节点上的分片，将其排空。新分布式表的分片也不会放到此节点，除非需要与该节点已有分片共置。 |

```sql
SELECT * from pg_dist_node;
```

```text
 nodeid | groupid | nodename | nodeport | noderack | hasmetadata | isactive | noderole | nodecluster | metadatasynced | shouldhaveshards
--------+---------+-----------+----------+----------+-------------+----------+----------+-------------+----------------+------------------
      1 |       1 | localhost |    12345 | default | f           | t        | primary | default     | f              | t
      2 |       2 | localhost |    12346 | default | f           | t        | primary | default     | f              | t
      3 |       3 | localhost |    12347 | default | f           | t        | primary | default     | f              | t
(3 rows)
```

### Citus 节点视图 {#citus-nodes-view}

`citus_nodes` 视图展示 `pg_dist_node` 中的节点信息，无需超级用户权限即可访问。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `nodename` | text | 节点的主机名或 IP 地址。 |
| `nodeport` | int | 节点监听的端口号。 |
| `role` | text | 节点角色：`coordinator` 或 `worker`。 |
| `active` | boolean | 节点是否处于活动状态。 |

```sql
SELECT * from citus_nodes;
```

```text
 nodename  | nodeport |    role     | active
-----------+----------+-------------+--------
 localhost |    57637 | worker      | t
 localhost |    57638 | worker      | f
 localhost |    57636 | coordinator | t
(3 rows)
```

### 分布式对象表 {#distributed-object-table}

`citus.pg_dist_object` 记录在协调节点创建并传播到工作节点的类型、函数等对象。管理员向集群添加新工作节点时，Citus 会自动按正确顺序在新节点创建这些对象的副本，以满足对象依赖关系。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `classid` | oid | 分布式对象的类别 |
| `objid` | oid | 分布式对象的对象 ID |
| `objsubid` | integer | 分布式对象的子对象 ID，例如 attnum |
| `type` | text | PostgreSQL 升级时使用的稳定地址的一部分 |
| `object_names` | text[] | PostgreSQL 升级时使用的稳定地址的一部分 |
| `object_args` | text[] | PostgreSQL 升级时使用的稳定地址的一部分 |
| `distribution_argument_index` | integer | 仅对分布式函数或过程有效 |
| `colocationid` | integer | 仅对分布式函数或过程有效 |

“稳定地址”不依赖特定服务器，能够唯一标识对象。Citus 使用 [pg_identify_object_as_address()](https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-OBJECT-TABLE) 创建的稳定地址，在 PostgreSQL 升级期间跟踪对象。

以下示例展示 `create_distributed_function()` 如何向 `citus.pg_dist_object` 添加条目：

```psql
CREATE TYPE stoplight AS enum ('green', 'yellow', 'red');

CREATE OR REPLACE FUNCTION intersection()
RETURNS stoplight AS $$
DECLARE
        color stoplight;
BEGIN
        SELECT *
          FROM unnest(enum_range(NULL::stoplight)) INTO color
         ORDER BY random() LIMIT 1;
        RETURN color;
END;
$$ LANGUAGE plpgsql VOLATILE;

SELECT create_distributed_function('intersection()');

-- will have two rows, one for the TYPE and one for the FUNCTION
TABLE citus.pg_dist_object;
```

```text
-[ RECORD 1 ]---------------+------
classid                     | 1247
objid                       | 16780
objsubid                    | 0
type                        |
object_names                |
object_args                 |
distribution_argument_index |
colocationid                |
-[ RECORD 2 ]---------------+------
classid                     | 1255
objid                       | 16788
objsubid                    | 0
type                        |
object_names                |
object_args                 |
distribution_argument_index |
colocationid                |
```

### Citus 模式视图 {#citus-schemas-view}

Citus 12.0 引入了 `schema_based_sharding` 概念和 `citus_schemas` 视图。此视图展示系统中的分布式模式，只列出分布式模式，不显示本地模式。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| schema_name | regnamespace | 分布式模式的名称 |
| colocation_id | integer | 分布式模式的共置 ID |
| schema_size | text | 模式内所有对象的总大小，以便于阅读的格式显示 |
| schema_owner | name | 拥有该模式的角色 |

示例：

```sql
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 0 bytes     | user_service
time_service |             2 | 0 bytes     | time_service
ping_service |             3 | 632 kB      | ping_service
```

### Citus 表视图 {#citus-tables-view}

`citus_tables` 视图汇总 Citus 管理的所有表（分布式表和参考表）。它整合元数据表的信息，以便于阅读的形式展示以下属性：

- 表类型
- 分布列
- 共置组 ID
- 便于阅读的大小
- 分片数
- 所有者（数据库用户）
- 访问方法（堆或列式）

示例：

```sql
SELECT * FROM citus_tables;
```

```text
┌────────────┬──────────────────┬─────────────────────┬───────────────┬────────────┬─────────────┬─────────────┬───────────────┐
│ table_name │ citus_table_type │ distribution_column │ colocation_id │ table_size │ shard_count │ table_owner │ access_method │
├────────────┼──────────────────┼─────────────────────┼───────────────┼────────────┼─────────────┼─────────────┼───────────────┤
│ foo.test   │ distributed      │ test_column         │             1 │ 0 bytes    │          32 │ citus       │ heap          │
│ ref        │ reference        │ <none>              │             2 │ 24 GB      │           1 │ citus       │ heap          │
│ test       │ distributed      │ id                  │             1 │ 248 TB     │          32 │ citus       │ heap          │
└────────────┴──────────────────┴─────────────────────┴───────────────┴────────────┴─────────────┴─────────────┴───────────────┘
```

### 时间分区视图 {#time-partitions-view}

Citus 提供用户定义函数来管理[时序数据](/citus/tutorials/tutorial-time-series/)场景中的分区，并维护 `time_partitions` 视图，以便检查这些分区。

列说明：

- **parent_table**：进行分区的父表。
- **partition_column**：父表的分区列。
- **partition**：分区表名。
- **from_value**：此分区中数据行的时间下界。
- **to_value**：此分区中数据行的时间上界。
- **access_method**：`heap` 表示行式存储，`columnar` 表示列式存储。

```sql
SELECT * FROM time_partitions;
```

```text
┌────────────────────────┬──────────────────┬─────────────────────────────────────────┬─────────────────────┬─────────────────────┬───────────────┐
│      parent_table      │ partition_column │                partition                │     from_value      │      to_value       │ access_method │
├────────────────────────┼──────────────────┼─────────────────────────────────────────┼─────────────────────┼─────────────────────┼───────────────┤
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0000 │ 2015-01-01 00:00:00 │ 2015-01-01 02:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0200 │ 2015-01-01 02:00:00 │ 2015-01-01 04:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0400 │ 2015-01-01 04:00:00 │ 2015-01-01 06:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0600 │ 2015-01-01 06:00:00 │ 2015-01-01 08:00:00 │ heap          │
└────────────────────────┴──────────────────┴─────────────────────────────────────────┴─────────────────────┴─────────────────────┴───────────────┘
```

### 共置组表 {#colocation-group-table}

`pg_dist_colocation` 记录哪些表的分片应放在一起，即共置。当两个表属于同一个共置组时，Citus 保证具有相同分区值的分片位于相同的工作节点上，从而支持连接优化、部分分布式汇总和外键。当两个表的分片数与分区列类型均一致时，Citus 会推断其分片应共置；也可以在创建分布式表时指定自定义共置组。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `colocationid` | int | 此行对应的共置组的唯一标识符。 |
| `shardcount` | int | 此共置组中所有表的分片数。 |
| `replicationfactor` | int | 此共置组中所有表的复制因子。 |
| `distributioncolumntype` | oid | 此共置组中所有表的分布列类型。 |
| `distributioncolumncollation` | oid | 此共置组中所有表的分布列排序规则。 |

```sql
SELECT * from pg_dist_colocation;
```

```text
 colocationid | shardcount | replicationfactor | distributioncolumntype | distributioncolumncollation
--------------+------------+-------------------+------------------------+-----------------------------
            2 |         32 |                 1 |                     20 |                           0
(1 row)
```

### 再平衡策略表 {#rebalancer-strategy-table}

此表定义 `citus_rebalance_start` 决定分片移动位置时可采用的策略。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `name` | name | 策略的唯一名称。 |
| `default_strategy` | boolean | `citus_rebalance_start` 是否默认选择此策略。使用 `citus_set_default_rebalance_strategy` 更新此列。 |
| `shard_cost_function` | regproc | 代价函数的标识符。该函数必须接收 bigint 类型的 `shardid`，返回 real 类型的代价值。 |
| `node_capacity_function` | regproc | 容量函数的标识符。该函数必须接收 int 类型的 `nodeid`，返回 real 类型的节点容量。 |
| `shard_allowed_on_node_function` | regproc | 函数标识符。给定 bigint 类型的 `shardid` 和 int 类型的 `nodeidarg`，返回一个布尔值，表示是否允许在该节点存储此分片。 |
| `default_threshold` | float4 | 判定节点过满或过空的阈值，决定 `citus_rebalance_start` 何时尝试移动分片。 |
| `minimum_threshold` | float4 | 防止 `citus_rebalance_start()` 的 threshold 参数设置过低的保护下限。 |
| `improvement_threshold` | float4 | 决定再平衡时是否值得移动一个分片。当移动该分片带来的改善与不移动时的改善之比超过此阈值，再平衡器才会移动它。此值对 `by_disk_size strategy` 尤其有用。 |

Citus 安装时，该表包含以下策略：

```sql
SELECT * FROM pg_dist_rebalance_strategy;
```

```text
-[ RECORD 1 ]------------------+---------------------------------
name                           | by_shard_count
default_strategy               | f
shard_cost_function            | citus_shard_cost_1
node_capacity_function         | citus_node_capacity_1
shard_allowed_on_node_function | citus_shard_allowed_on_node_true
default_threshold              | 0
minimum_threshold              | 0
improvement_threshold          | 0
-[ RECORD 2 ]------------------+---------------------------------
name                           | by_disk_size
default_strategy               | t
shard_cost_function            | citus_shard_cost_by_disk_size
node_capacity_function         | citus_node_capacity_1
shard_allowed_on_node_function | citus_shard_allowed_on_node_true
default_threshold              | 0.1
minimum_threshold              | 0.01
improvement_threshold          | 0.5
```

`by_shard_count` 将所有分片视为相同代价，以使各节点的分片数相等。默认策略 `by_disk_size` 则以分片的磁盘字节数加上其共置分片的磁盘字节数作为代价。磁盘大小使用 `pg_total_relation_size` 计算，因此包括索引。该策略力求让每个节点占用相同的磁盘空间。默认阈值为 0.1，可以避免因细微的磁盘占用差异而进行无谓的分片移动。

#### 创建自定义再平衡策略 {#creating-custom-rebalancer-strategies}

以下示例中的函数可用于新的分片再平衡策略。使用 `citus_add_rebalance_strategy` 将这些函数注册到 `pg_dist_rebalance_strategy` 表中。

- 根据主机名模式，为特定节点设置不同的容量：

  ```sql
  -- example of node_capacity_function
  
  CREATE FUNCTION v2_node_double_capacity(nodeidarg int)
      RETURNS real AS $$
      SELECT
          (CASE WHEN nodename LIKE '%.v2.worker.citusdata.com' THEN 2.0::float4 ELSE 1.0::float4 END)
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;
  ```
- 根据 `citus_stat_statements` 记录的分片查询次数进行再平衡：

  ```sql
  -- example of shard_cost_function
  
  CREATE FUNCTION cost_of_shard_by_number_of_queries(shardid bigint)
      RETURNS real AS $$
      SELECT coalesce(sum(calls)::real, 0.001) as shard_total_queries
      FROM citus_stat_statements
      WHERE partition_key is not null
          AND get_shard_id_for_distribution_column('tab', partition_key) = shardid;
  $$ LANGUAGE sql;
  ```
- 将特定分片（10000）隔离到指定节点（地址为 '10.0.0.1'）：

  ```sql
  -- example of shard_allowed_on_node_function
  
  CREATE FUNCTION isolate_shard_10000_on_10_0_0_1(shardid bigint, nodeidarg int)
      RETURNS boolean AS $$
      SELECT
          (CASE WHEN nodename = '10.0.0.1' THEN shardid = 10000 ELSE shardid != 10000 END)
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;
  
  -- The next two definitions are recommended in combination with the above function.
  -- This way the average utilization of nodes is not impacted by the isolated shard.
  CREATE FUNCTION no_capacity_for_10_0_0_1(nodeidarg int)
      RETURNS real AS $$
      SELECT
          (CASE WHEN nodename = '10.0.0.1' THEN 0 ELSE 1 END)::real
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;
  CREATE FUNCTION no_cost_for_10000(shardid bigint)
      RETURNS real AS $$
      SELECT
          (CASE WHEN shardid = 10000 THEN 0 ELSE 1 END)::real
      $$ LANGUAGE sql;
  ```

### 查询统计表 {#query-statistics-table}

> [!NOTE]
> 从 11.0 版本开始，`citus_stat_statements` 视图属于 Citus 社区版。

Citus 提供 `citus_stat_statements`，统计查询如何执行以及由谁执行。它类似于 PostgreSQL 中记录查询速度统计信息的 [pg_stat_statements](https://www.postgresql.org/docs/current/static/pgstatstatements.html) 视图。可以将 `citus_stat_statements` 与 `pg_stat_statements` 连接查询。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `queryid` | bigint | 查询标识符，适合用于连接 pg_stat_statements |
| `userid` | oid | 执行查询的用户 |
| `dbid` | oid | 协调节点的数据库实例 |
| `query` | text | 匿名化的查询字符串 |
| `executor` | text | 使用的 Citus [执行器](/citus/reference/reference-processing/)：adaptive 或 insert-select |
| `partition_key` | text | 路由执行查询中的分布列值，否则为 NULL |
| `calls` | bigint | 查询执行次数 |

```sql
-- create and populate distributed table
create table foo ( id int );
select create_distributed_table('foo', 'id');
insert into foo select generate_series(1,100);

-- enable stats
-- pg_stat_statements must be in shared_preload libraries
create extension pg_stat_statements;

select count(*) from foo;
select * from foo where id = 42;

select * from citus_stat_statements;
```

结果：

```text
-[ RECORD 1 ]-+----------------------------------------------
queryid       | -909556869173432820
userid        | 10
dbid          | 13340
query         | insert into foo select generate_series($1,$2)
executor      | insert-select
partition_key |
calls         | 1
-[ RECORD 2 ]-+----------------------------------------------
queryid       | 3919808845681956665
userid        | 10
dbid          | 13340
query         | select count(*) from foo;
executor      | adaptive
partition_key |
calls         | 1
-[ RECORD 3 ]-+----------------------------------------------
queryid       | 5351346905785208738
userid        | 10
dbid          | 13340
query         | select * from foo where id = $1
executor      | adaptive
partition_key | 42
calls         | 1
```

注意事项：

- 统计数据不会复制，数据库崩溃或故障切换后无法保留。
- 跟踪的查询数量有限，由全局用户配置（GUC）`pg_stat_statements.max` 控制，默认值为 5,000。
- 使用 `citus_stat_statements_reset()` 清空该表。

### citus_stats 视图 {#citus_stats-view}

> [!NOTE]
> `citus_stats` 视图从 Citus 13.2 开始可用。

`citus_stats` 汇总各工作节点上分布式表、参考表和 Citus 本地表的 `pg_stats` 信息，提供集群范围的列统计信息。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `tablename` | text | Citus 表名 |
| `attname` | name | 列名 |
| `null_frac` | real | NULL 值所占比例（0.0–1.0） |
| `most_common_vals` | anyarray | 最常见值组成的数组 |
| `most_common_freqs` | real[] | 与 `most_common_vals` 各值对应的频率 |

> [!TIP]
> 查询 `citus_stats` 前，请先对表执行 `ANALYZE`，填充工作节点上的 `pg_stats`。

示例：

```sql
SELECT tablename, attname, null_frac, most_common_vals, most_common_freqs
FROM citus_stats
WHERE tablename = 'dist_user_payloads';
```

### Citus 统计计数器视图 {#citus-stat-counters-view}

`citus_stat_counters` 展示本地节点各数据库的汇总统计信息，包括连接管理和分布式查询执行指标。未安装 Citus 的数据库也会返回一行，但计数器为零。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `database_id` | oid | 数据库 OID。 |
| `name` | name | 数据库名称；数据库已删除时为 NULL。 |
| `connection_establishment_succeeded` | bigint | 本节点成功发起的节点间连接数。 |
| `connection_establishment_failed` | bigint | 失败的连接尝试数，例如节点不可达、超时或配置错误。因限流（`citus.max_shared_pool_size`、`citus.local_shared_pool_size`）而跳过的可选连接不计为失败。参见[配置参考](/citus/reference/api-guc/#citusmax_shared_pool_size-integer)中的限流 GUC。 |
| `connection_reused` | bigint | 复用缓存连接而非新建连接的次数（`citus.max_cached_conns_per_worker`、`citus.max_cached_connection_lifetime`）。 |
| `query_execution_single_shard` | bigint | 执行的单分片查询和子计划数。 |
| `query_execution_multi_shard` | bigint | 执行的多分片查询和子计划数。 |
| `stats_reset` | timestamptz | 上次重置统计信息的时间戳；从未重置时为 NULL。 |

**连接管理指标**

- `connection_establishment_succeeded`：本节点成功建立的节点间连接数。
- `connection_establishment_failed`：失败的连接尝试数，包括超时，参见 `citus.node_connection_timeout`。
- `connection_reused`：复用已有缓存连接而非新建连接的次数。

**查询执行指标**

顶层查询*以及*子计划、子查询都会增加这些计数器，例如 `INSERT ... SELECT`、`MERGE` 和递归规划步骤。

- `query_execution_single_shard`：访问单个分片的查询数。
- `query_execution_multi_shard`：访问多个分片的查询数。

```sql
SELECT * FROM citus_stat_counters;
```

```text
 database_id |    name    | connection_establishment_succeeded | connection_establishment_failed | connection_reused | query_execution_single_shard | query_execution_multi_shard |          stats_reset
-------------+------------+------------------------------------+---------------------------------+-------------------+------------------------------+-----------------------------+-------------------------------+
       16384 | dist_db_1  |                               1897 |                               2 |              6213 |                         4449 |                         292 |
       17216 | dist_db_2  |                                422 |                               0 |              2060 |                          731 |                         256 | 2025-09-12 11:44:39.186173+03
           5 | postgres   |                                  0 |                               0 |                 0 |                            0 |                           0 |
(3 rows)
```

说明：

- 统计信息不持久化，服务器重启后会清空。
- 由 `citus.enable_stat_counters` 控制采集，默认值为 **false**。可在 `postgresql.conf` 中全局设置，也可通过 `ALTER ROLE ... SET` 或 `ALTER DATABASE ... SET` 按角色或数据库设置。
- 使用 `citus_stat_counters(<db_oid>)` 查询特定数据库；省略参数或传入 `0` 则查询所有数据库。函数可以返回已删除数据库的统计信息，而视图会过滤掉这些记录（name 为 NULL）。
- 使用 `citus_stat_counters_reset(<db_oid>)` 重置特定数据库的计数器；省略参数或传入 `0` 则重置当前数据库。

### 租户级查询统计视图 {#tenant-level-query-statistics-view}

`citus_stat_tenants` 为 `citus_stat_statements` 补充每个租户的查询次数信息。将查询追溯到发起租户，有助于判断何时采用 `tenant_isolation`。

该视图统计可配置时间段内近期执行的单租户查询。在当前周期内，只读查询数和总查询数持续累加；周期结束后，计数转入上一周期统计，并保持不变直至过期。使用 `citus.stats_tenants_period` 设置周期长度，单位为秒，默认 60 秒。

视图最多显示 `citus.stat_tenants_limit` 行，默认 100 行。只统计过滤到单个租户的查询，忽略同时涉及多个租户的查询。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `nodeid` | int | 来自 `pg_dist_node` 的节点 ID |
| `colocation_id` | int | [共置组](/citus/reference/api-metadata/#colocation-group-table) ID |
| `tenant_attribute` | text | 分布列中标识租户的值 |
| `read_count_in_this_period` | int | 本周期内该租户的读取（SELECT）查询数 |
| `read_count_in_last_period` | int | 上一周期的读取查询数 |
| `query_count_in_this_period` | int | 本周期内该租户的读写查询数 |
| `query_count_in_last_period` | int | 上一周期的读写查询数 |
| `cpu_usage_in_this_period` | double | 本周期内该租户消耗的 CPU 时间，单位为秒 |
| `cpu_usage_in_last_period` | double | 上一周期该租户消耗的 CPU 时间，单位为秒 |

跟踪租户级统计会增加开销，因此默认禁用。将 `citus.stat_tenants_track` 设为 `'all'` 可启用。

**示例：**

假设有一个按 `tenant_id` 分布的表 `dist_table`，然后执行以下查询：

```sql
INSERT INTO dist_table(tenant_id) VALUES (1);
INSERT INTO dist_table(tenant_id) VALUES (1);
INSERT INTO dist_table(tenant_id) VALUES (2);

SELECT count(*) FROM dist_table WHERE tenant_id = 1;
```

租户级统计会反映刚才执行的查询：

```sql
SELECT tenant_attribute, read_count_in_this_period,
       query_count_in_this_period, cpu_usage_in_this_period
  FROM citus_stat_tenants;
```

```text
 tenant_attribute | read_count_in_this_period | query_count_in_this_period | cpu_usage_in_this_period
------------------+---------------------------+----------------------------+--------------------------
 1                |                         1 |                          3 |                 0.000883
 2                |                         0 |                          1 |                 0.000144
```

### 分布式查询活动 {#distributed-query-activity}

有时，查询会阻塞在工作节点某个分片上的行级锁上。这类查询不会出现在 Citus 协调节点的 [pg_locks](https://www.postgresql.org/docs/current/static/view-pg-locks.html) 中。

Citus 提供专用视图来观察整个集群的查询和锁，包括内部用于生成分布式查询结果的分片查询。

- **citus_stat_activity**：显示所有节点正在执行的分布式查询。它是 `pg_stat_activity` 的超集，可用于后者适用的所有场景。
- **citus_dist_stat_activity**：与 `citus_stat_activity` 类似，但仅包含分布式查询，排除 Citus 查询片段。
- **citus_lock_waits**：显示整个集群中被阻塞的查询。

前两个视图包含 [pg_stat_activity](https://www.postgresql.org/docs/current/static/monitoring-stats.html#PG-STAT-ACTIVITY-VIEW) 的所有列，还包含发起查询的工作节点的全局 PID。

例如，统计分布式表中的行数：

```sql
-- run in one session
-- (with a pg_sleep so we can see it)

SELECT count(*), pg_sleep(3) FROM users_table;
```

可以在 `citus_dist_stat_activity` 中看到该查询：

```sql
-- run in another session

SELECT * FROM citus_dist_stat_activity;

-[ RECORD 1 ]----+-------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | f
datid            | 13724
datname          | postgres
pid              | 12199
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | psql
client_addr      |
client_hostname  |
client_port      | -1
backend_start    | 2022-03-23 11:30:00.533991-05
xact_start       | 2022-03-23 19:35:28.095546-05
query_start      | 2022-03-23 19:35:28.095546-05
state_change     | 2022-03-23 19:35:28.09564-05
wait_event_type  | Timeout
wait_event       | PgSleep
state            | active
backend_xid      |
backend_xmin     | 777
query_id         |
query            | SELECT count(*), pg_sleep(3) FROM users_table;
backend_type     | client backend
```

`citus_dist_stat_activity` 隐藏内部的 Citus 查询片段。要查看这些片段，可以使用更详细的 `citus_stat_activity`。例如，前面的 `count(*)` 需要所有分片的信息，其中一部分来自 `users_table_102039` 分片，可通过以下查询看到。

```sql
SELECT * FROM citus_stat_activity;

-[ RECORD 1 ]----+-----------------------------------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | f
datid            | 13724
datname          | postgres
pid              | 12199
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | psql
client_addr      |
client_hostname  |
client_port      | -1
backend_start    | 2022-03-23 11:30:00.533991-05
xact_start       | 2022-03-23 19:32:18.260803-05
query_start      | 2022-03-23 19:32:18.260803-05
state_change     | 2022-03-23 19:32:18.260821-05
wait_event_type  | Timeout
wait_event       | PgSleep
state            | active
backend_xid      |
backend_xmin     | 777
query_id         |
query            | SELECT count(*), pg_sleep(3) FROM users_table;
backend_type     | client backend
-[ RECORD 2 ]----------+-----------------------------------------------------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | t
datid            | 13724
datname          | postgres
pid              | 12725
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | citus_internal gpid=10000012199
client_addr      | 127.0.0.1
client_hostname  |
client_port      | 44106
backend_start    | 2022-03-23 19:29:53.377573-05
xact_start       |
query_start      | 2022-03-23 19:32:18.278121-05
state_change     | 2022-03-23 19:32:18.278281-05
wait_event_type  | Client
wait_event       | ClientRead
state            | idle
backend_xid      |
backend_xmin     |
query_id         |
query            | SELECT count(*) AS count FROM public.users_table_102039 users WHERE true
backend_type     | client backend
```

`query` 字段显示正在统计分片 102039 中的行。

以下是使用 `citus_stat_activity` 编写的实用查询示例：

```sql
-- active queries' wait events

SELECT query, wait_event_type, wait_event
  FROM citus_stat_activity
 WHERE state='active';

-- active queries' top wait events

SELECT wait_event, wait_event_type, count(*)
  FROM citus_stat_activity
 WHERE state='active'
 GROUP BY wait_event, wait_event_type
 ORDER BY count(*) desc;

-- total internal connections generated per node by Citus

SELECT nodeid, count(*)
  FROM citus_stat_activity
 WHERE is_worker_query
 GROUP BY nodeid;
```

接下来是 `citus_lock_waits`。为了解其用法，先手动构造一个锁等待场景。在协调节点创建测试表：

```sql
CREATE TABLE numbers AS
  SELECT i, 0 AS j FROM generate_series(1,10) AS i;
SELECT create_distributed_table('numbers', 'i');
```

然后在协调节点的两个会话中，按以下顺序执行语句：

```sql
-- session 1                           -- session 2
-------------------------------------  -------------------------------------
BEGIN;
UPDATE numbers SET j = 2 WHERE i = 1;
                                       BEGIN;
                                       UPDATE numbers SET j = 3 WHERE i = 1;
                                       -- (this blocks)
```

`citus_lock_waits` 视图会显示这一情况。

```sql
SELECT * FROM citus_lock_waits;

-[ RECORD 1 ]-------------------------+--------------------------------------
waiting_gpid                          | 10000011981
blocking_gpid                         | 10000011979
blocked_statement                     | UPDATE numbers SET j = 3 WHERE i = 1;
current_statement_in_blocking_process | UPDATE numbers SET j = 2 WHERE i = 1;
waiting_nodeid                        | 1
blocking_nodeid                       | 1
```

本例中的查询由协调节点发起，但该视图也能列出工作节点所发起查询之间的锁。

## 所有节点上的表 {#tables-on-all-nodes}

Citus 还有一些信息表和视图，可以在所有节点上访问，而不仅限于协调节点。

### 连接凭据表 {#connection-credentials-table}

> [!NOTE]
> 从 11.0 版本开始，此表属于 Citus 社区版。

`pg_dist_authinfo` 保存 Citus 节点互相连接时使用的认证参数。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `nodeid` | integer | 来自 `pg_dist_node` 的节点 ID，或 0、-1 |
| `rolename` | name | PostgreSQL 角色 |
| `authinfo` | text | 以空格分隔的 libpq 连接参数 |

建立连接时，节点会检查表中是否存在目标 `nodeid` 与所需 `rolename` 对应的行。如果存在，就在 libpq 连接中使用相应的 `authinfo` 字符串。常见用途是保存密码，例如 `'password=abc123'`。可用参数参见[完整列表](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)。

`authinfo` 中的参数以空格分隔，形式为 `key=val`。空值或包含空格的值必须用单引号括起，例如 `keyword='a value'`。值中的单引号和反斜杠必须用反斜杠转义，例如 `\'` 和 `\\`。

`nodeid` 还可以取特殊值 0 和 -1，分别表示*所有节点*和*回环连接*。如果某节点同时匹配专用规则和所有节点规则，专用规则优先。

```postgres
SELECT * FROM pg_dist_authinfo;

 nodeid | rolename | authinfo
--------+----------+-----------------
    123 | jdoe     | password=abc123
(1 row)
```

### 连接池凭据 {#connection-pooling-credentials}

> [!NOTE]
> 从 11.0 版本开始，此表属于 Citus 社区版。

要通过连接池连接节点，请使用 `pg_dist_poolinfo` 指定连接池选项。该元数据表保存 Citus 通过连接池连接节点时所用的主机、端口和数据库名。

添加连接池信息后，Citus 会尝试使用这些值而非直接连接。`pg_dist_poolinfo` 的信息优先于 `pg_dist_node`。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `nodeid` | integer | 来自 `pg_dist_node` 的节点 ID |
| `poolinfo` | text | 以空格分隔的参数：host、port 或 dbname |

> [!NOTE]
> 某些情况下 Citus 会忽略 `pg_dist_poolinfo`。例如，分片再平衡与 PgBouncer 等连接池不兼容，此时会使用直接连接。

```sql
-- how to connect to node 1 (as identified in pg_dist_node)

INSERT INTO pg_dist_poolinfo (nodeid, poolinfo)
     VALUES (1, 'host=127.0.0.1 port=5433');
```

## 相关内容 {#related-content}

- [用户定义函数](/citus/reference/api-udf/)
- [配置参数](/citus/reference/api-guc/)
- [什么是 Azure Cosmos DB for PostgreSQL？](/citus/overview/what-is-citus/)
