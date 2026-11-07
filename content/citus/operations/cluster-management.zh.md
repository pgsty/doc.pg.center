---
title: 管理 Citus 集群
description: 了解如何管理 Citus 集群、添加或删除节点、缩放和重新平衡集群以及处理节点故障。
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/cluster-management?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

本文介绍如何在 Citus 集群中添加或删除节点，以及如何处理节点故障。

> [!NOTE]
> 为便于跨节点移动分片，或重新复制故障节点上的分片，Citus 社区版从 11.0 起支持完全在线的分片重平衡。以下各节会在相关处简要介绍分片重平衡器提供的函数。有关函数、参数和用法的详细信息，请参阅 `cluster_management_functions` 参考章节。

## 选择集群大小 {#choosing-cluster-size}

本部分探讨在生产环境中运行集群的配置设置。

### 分片数量 {#shard-count}

为每张分布式表选择分片数量时，需要在更多分片带来的灵活性与跨分片查询规划、执行的开销之间权衡。如果表已分布后需要更改分片数量，可使用 `alter_distributed_table` 函数。

#### 多租户 SaaS 用例 {#multitenant-saas-use-case}

最佳选择取决于数据访问模式。例如，在 [多租户应用](/citus/tutorials/tutorial-multi-tenant/) 用例中，可选择 **32–128 个分片**。较小的工作负载（小于 100 GB）从 32 个分片开始；较大的工作负载选择 64 或 128 个分片。这样就为扩展至 32–128 台工作节点机器留出了余地。

#### 实时分析用例 {#real-time-analytics-use-case}

在 [实时分析](/citus/tutorials/tutorial-analytics/) 用例中，分片数量应与工作节点的 CPU 核心总数相关。为获得最大并行度，每个节点上的分片应足够多，使每个 CPU 核心至少对应一个分片。通常，初始分片数应设得较高，例如**当前 CPU 核心数的 2 倍或 4 倍**，以便日后添加工作节点和 CPU 核心时继续扩展。

但要注意，对于每个查询，Citus 会为每个分片打开一个数据库连接，而连接数是有限的。分片数应足够小，避免分布式查询频繁等待可用连接。换言之，所需连接数 `(max concurrent queries * shard count)` 不应超过系统可提供的总连接数 `(number of workers * max_connections per worker)`。

## 初始硬件规模 {#initial-hardware-size}

集群规模可以通过调整节点数量和硬件容量轻松改变（在我们的 `cloud_topic` 上扩缩容尤其方便）。不过，新建集群仍需要选择初始规模。以下建议可帮助选择合理的起始配置。

### 多租户 SaaS 用例 {#multitenant-saas-use-case-1}

如果从现有的单节点数据库实例迁移到 Citus，应使集群中所有工作节点的 CPU 核心总数和内存总量与原实例相当。这类场景中，性能可能达到原来的两到三倍，因为分片能够提高资源利用率，并使索引更小。

协调节点所需的内存比工作节点少，因此可以使用计算优化型机器运行协调节点。所需核心数取决于现有工作负载，例如读写吞吐量。

### 实时分析用例 {#real-time-analytics-use-case-1}

**核心总数：** 当工作数据能够放入内存时，Citus 的性能预期会随工作节点核心数线性提升。要确定所需核心数，可比较当前单节点数据库的查询延迟与 Citus 的目标延迟，用当前延迟除以目标延迟，再将结果取整。

**工作节点内存：** 理想情况下，应提供足够的内存，容纳工作集的大部分数据。应用程序的查询类型会影响内存需求。可以对查询执行 `EXPLAIN ANALYZE`，确定其内存需求。

## 扩展集群 {#scaling-the-cluster}

Citus 的基于逻辑分片的体系结构允许横向扩展集群，而无需停机。 本部分介绍如何将更多节点添加到 Citus 集群，以提高查询性能和可伸缩性。

### 添加工作节点 {#add-a-worker}

Citus 将分布式表的全部数据保存在工作节点上。若要增加计算能力以横向扩展集群，可以添加工作节点。

要将新节点加入集群，先将节点的 DNS 名称或 IP 地址及其 PostgreSQL 端口加入 `pg_dist_node` 系统目录表。使用 `citus_add_node` UDF 添加节点，例如：

```sql
SELECT * from citus_add_node('node-name', 5432);
```

新建分布式表的分片可以使用这个新节点。已有分片仍留在原处，除非重新分布它们。因此，仅添加工作节点而不采取后续操作，可能无法提升性能。

> [!NOTE]
> 如果集群中有大型参考表，添加节点可能会变慢。此时可以考虑使用 `replicate_reference_tables_on_activate` GUC。
> 
> 新节点创建时还会同步 Citus 元数据。默认情况下，为保证一致性，同步在单个事务中完成。但在元数据量很大的大型集群中，该事务可能耗尽内存并失败。遇到这种情况时，可以通过 `metadata_sync_mode` GUC 选择非事务式元数据同步模式。

#### 基于快照的节点添加 （Citus 13.2） {#snapshot-based-node-addition-citus-132}

Citus 13.2 引入了基于快照添加节点的方式，使横向扩展更快。它将现有工作节点的流复制副本（克隆）提升为工作节点，再将分片分配到源节点和克隆节点，而不必通过网络将全部数据复制到一个全新的工作节点。

**工作流程概述：**

1. 创建工作节点的物理副本（例如使用 `pg_basebackup`），并将其配置为源工作节点的流复制副本。
2. 注册克隆节点，并可选择预览计划。
3. 将克隆节点提升为工作节点，并在源节点和克隆节点之间重平衡分片。

**优点：**

- 在横向扩展期间避免完整数据复制
- 重平衡范围仅限于源工作节点及其克隆节点
- 减少写入阻塞，加快大型数据集的节点添加过程

有关 UDF 的详细信息和示例，请参阅实用工具参考中的基于快照的节点添加函数： [citus_add_clone_node](/citus/reference/api-udf/#citus_add_clone_node)、 [citus_add_clone_node_with_nodeid](/citus/reference/api-udf/#citus_add_clone_node_with_nodeid)、 [get_snapshot_based_node_split_plan](/citus/reference/api-udf/#get_snapshot_based_node_split_plan) 和 [citus_promote_clone_and_rebalance](/citus/reference/api-udf/#citus_promote_clone_and_rebalance)。

### 无停机分片重平衡 {#rebalance-shards-without-downtime}

> [!NOTE]
> 从 11.0 版起，Citus 社区版支持在重平衡期间不阻塞读取*和*写入。

要将已有分片移到新添加的工作节点，可使用 `citus_rebalance_start` 函数，将分片均匀分布到各工作节点。

> [!NOTE]
> Citus 13.2 通过支持共置组内并行迁移和参考表并行复制来提高重平衡吞吐量；同时移除全局复制锁，改用分片级咨询锁，并放宽共置锁的限制。调用 `citus_rebalance_start` 时，启用 `parallel_transfer_colocated_shards` 和 `parallel_transfer_reference_tables` 参数（默认值均为 *false*），并调整 `max_worker_processes`、`citus.max_background_task_executor` 和 `citus.max_background_task_executors_per_node`，即可利用这些并行能力。

可以配置该函数，按不同策略重平衡分片，以匹配数据库工作负载。有关策略选择，请参阅函数参考。以下示例使用默认策略：

```sql
SELECT citus_rebalance_start();
```

多租户 SaaS 应用等许多产品无法容忍停机。在我们的托管服务上，PostgreSQL 10 及更高版本的重平衡满足这一要求：移动数据时，应用程序的读写可以继续进行，仅有极短的中断。

#### 并行重平衡 {#parallel-rebalancing}

默认情况下，重平衡会依次迁移多个分片。在某些场景中，可以接受消耗更多网络带宽等资源，以更快地完成重平衡。此时可将重平衡配置为并行迁移多个分片。

`citus.max_background_task_executors_per_node` GUC 允许分片重平衡等任务并行执行。可按需调高其默认值（1），增加并行度。若需更高的并发度，还应调高 `max_worker_processes` 和 `citus.max_background_task_executor`（全局执行器池）。要并行迁移共置组内的分片或复制参考表，可向 `citus_rebalance_start` 传入 `parallel_transfer_colocated_shards := true` 和/或 `parallel_transfer_reference_tables := true`。

```sql
ALTER SYSTEM SET citus.max_background_task_executors_per_node = 2;
ALTER SYSTEM SET citus.max_background_task_executor = 8;
ALTER SYSTEM SET max_worker_processes = 32;
SELECT pg_reload_conf();

SELECT citus_rebalance_start(parallel_transfer_colocated_shards := true,
                             parallel_transfer_reference_tables := true);
```

**典型的用例是什么？**

- 在将新节点添加到集群时，实现更快速的横向扩展。
- 更快地重平衡集群，使各节点的利用率均衡

**边界情况与注意事项**

`citus.max_background_task_executors_per_node` 限制的是并行任务执行器的总数量。默认情况下，同一共置组的分片按顺序迁移；启用 `parallel_transfer_colocated_shards` 后，可在共置组内并行迁移。启用 `parallel_transfer_reference_tables` 后，参考表也可以并行复制。

#### 工作原理 {#how-it-works}

Citus 的分片重平衡利用 PostgreSQL 逻辑复制，将数据从旧分片（复制术语中的“发布者”）迁移到新分片（“订阅者”）。复制分片数据期间，应用程序可以持续读写而不中断。只有在更新元数据、将订阅者分片提升为活动分片时，Citus 才会对分片短暂加写锁。

如 PostgreSQL 文档[所述](https://www.postgresql.org/docs/current/static/logical-replication-publication.html)，源端需要配置*复制标识*：

发布表必须配置“复制标识”，才能复制 UPDATE 和 DELETE 操作，以便在订阅端定位要更新或删除的行。如果表有主键，默认就使用主键作为复制标识；也可以使用另一个满足附加要求的唯一索引。

如果分布式表已经定义主键，就无需额外操作，可以直接进行分片重平衡。如果既没有主键，也没有显式定义复制标识，则尝试重平衡时会报错。可按以下方法处理。

**首先，表是否具有唯一索引？**

如果待复制的表已经有包含分布列的唯一索引，可以将该索引选作复制标识：

```sql
-- supposing my_table has unique index my_table_idx
-- which includes distribution column

ALTER TABLE my_table REPLICA IDENTITY
  USING INDEX my_table_idx;
```

> [!NOTE]
> 可以使用 `REPLICA IDENTITY USING INDEX`，但**不建议**为表设置 `REPLICA IDENTITY FULL`。后者会使每次更新或删除都在订阅端进行全表扫描，以查找相应元组。我们的测试发现，这种设置的性能甚至比下一节的第四种解决方案还差。

**否则，是否可以添加主键？**

为表添加主键。如果希望使用的键就是分布列，只需添加主键约束。如果主键包含非分布列，则必须使用复合主键，并将分布列也包含在内。

### 添加协调节点 {#adding-a-coordinator}

Citus 协调节点只保存表分片的元数据，不保存实际数据。这种架构将计算下推到工作节点，协调节点只对工作节点返回的结果进行最终聚合。因此，协调节点通常不会成为读取性能的瓶颈。也可以将其迁移到性能更强的机器上，提高处理能力。

不过，在某些写入密集型场景中，协调节点可能成为性能瓶颈。这时可按以下方式添加另一个节点，并对客户端连接进行负载均衡。

```sql
SELECT * FROM citus_add_node(second_coordinator_hostname, second_coordinator_port);
SELECT * FROM citus_set_node_property(second_coordinator_hostname, second_coordinator_port, 'shouldhaveshards', false);
```

> [!NOTE]
> DDL 查询只能通过第一个协调节点执行。参见[数据库与角色 DDL 传播](/citus/reference/reference-ddl/)。

## 处理节点故障 {#dealing-with-node-failures}

本节介绍如何处理节点故障，避免 Citus 集群停机。

### 工作节点故障 {#worker-node-failures}

Citus 使用 PostgreSQL 流复制来容忍工作节点故障。流复制持续将 WAL 记录发送到备用节点，从而复制整个工作节点。可以参考 [PostgreSQL 复制文档](https://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION)，自行在本地部署中配置流复制；也可以使用已预先配置复制和高可用性的 `cloud_topic`。

### 协调节点故障 {#coordinator-node-failures}

Citus 协调节点维护元数据表，记录所有集群节点以及各节点上数据库分片的位置。元数据表通常只有几 MB，且变更不频繁。因此，可以复制这些表，并在节点故障时快速恢复。处理协调节点故障有以下几种选择。

1. **使用 PostgreSQL 流复制：** 利用 PostgreSQL 流复制为协调节点建立热备。主协调节点故障时，可自动将备用节点提升为主节点，继续为集群处理查询。有关配置方法，请参阅 [PostgreSQL wiki](https://wiki.postgresql.org/wiki/Streaming_Replication)。
2. **使用备份工具：** 元数据表很小，可以通过 EBS 卷或 [PostgreSQL 备份工具](https://www.postgresql.org/docs/current/static/backup.html)进行备份。之后将元数据复制到新节点，即可恢复运行。

## 租户隔离 {#tenant-isolation}

### 基于行的分片 {#row-based-sharding}

> [!NOTE]
> 从 11.0 版起，Citus 社区版包含租户隔离功能！

Citus 根据每行分布列的哈希值，将行放入工作节点上的分片。多个分布列值通常落在同一分片中。因此，在多租户场景中，租户通常会共享分片。

当租户的数据规模差异很大时，共享分片可能导致资源争用。这在租户众多的系统中很常见。随着租户数量增加，租户数据量往往遵循 Zipf 分布，即少数租户很大，而大量租户较小。为改善资源分配、保障租户的服务质量（QoS），可以将大租户迁移到专用节点。

Citus 提供了将租户隔离到特定节点的工具，过程分为两步：先将租户数据隔离到一个新的专用分片，再将该分片移到目标节点。理解这一过程，需要先了解数据行如何分配到分片。

每个分片都在 Citus 元数据中标记了它包含的哈希值范围（更多信息请参阅 [pg_dist_shard](/citus/reference/api-metadata/#shard-table) 的参考）。 Citus UDF `isolate_tenant_to_new_shard(table_name, tenant_id)` 通过三个步骤将租户移到专用分片中：

1. 为 `table_name` 创建一个新分片，其中 (a) 包括分布列值为 `tenant_id` 的行，并且 (b) 排除所有其他行。
2. 将相关行从其当前分片移动到新分片。
3. 将旧分片拆成两个分片，其哈希范围分别紧邻被分离范围的下界和上界。

此外，该 UDF 接受 `CASCADE` 选项，不仅隔离 `table_name` 中的租户行，还会隔离与该表共置的所有表中该租户的行。例如：

```sql
-- This query creates an isolated shard for the given tenant_id and
-- returns the new shard id.

-- General form:

SELECT isolate_tenant_to_new_shard('table_name', tenant_id);

-- Specific example:

SELECT isolate_tenant_to_new_shard('lineitem', 135);

-- If the given table has co-located tables, the query above errors out and
-- advises to use the CASCADE option

SELECT isolate_tenant_to_new_shard('lineitem', 135, 'CASCADE');
```

输出：

```text
┌─────────────────────────────┐
│ isolate_tenant_to_new_shard │
├─────────────────────────────┤
│                      102240 │
└─────────────────────────────┘
```

新分片创建在原分片所在的节点上。要实现真正的硬件隔离，可以将它们移到 Citus 集群的另一个节点。如前所述，`isolate_tenant_to_new_shard` 会返回新分片的 ID，可以使用该 ID 迁移分片：

有了分片标识符后，可以使用 `move_shard`。

### 基于模式的分片 {#schema-based-sharding}

使用基于模式的分片时，无需先隔离租户，因为每个租户已经位于独立的模式中。执行迁移前，需要获取该模式中一个分片的标识符。

首先，找出待迁移模式的共置 ID。

```sql
select * from citus_schemas;
```

```text
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 0 bytes     | user_service
time_service |             2 | 0 bytes     | time_service
ping_service |             3 | 0 bytes     | ping_service
a            |             4 | 128 kB      | citus
b            |             5 | 32 kB       | citus
with_data    |            11 | 6408 kB     | citus
(6 rows)
```

接下来，查询 `citus_shards`。 使用前面输出中的共置标识符 11：

```sql
select * from citus_shards where colocation_id = 11;
```

```text
table_name    | shardid |       shard_name       | citus_table_type | colocation_id | nodename  | nodeport | shard_size
-----------------+---------+------------------------+------------------+---------------+-----------+----------+------------
with_data.test  |  102180 | with_data.test_102180  | schema           |            11 | localhost |     9702 |     647168
with_data.test2 |  102183 | with_data.test2_102183 | schema           |            11 | localhost |     9702 |    5914624
(2 rows)
```

可以选择输出中的任意一个分片。迁移操作会同时作用于所有共置表。因此，在基于模式的分片中，会迁移该模式中的所有表。

有了分片标识符后，可以使用 `move_shard`。

### 执行迁移 {#make-the-move}

确定代表该租户的分片标识符后，即可执行迁移：

```sql
-- find the node currently holding the new shard
SELECT nodename, nodeport
  FROM citus_shards
 WHERE shardid = 102240;

-- list the available worker nodes that could hold the shard
SELECT * FROM master_get_active_worker_nodes();

-- move the shard to your choice of worker
-- (it will also move any shards created with the CASCADE option)
SELECT citus_move_shard_placement(
  102240,
  'source_host', source_port,
  'dest_host', dest_port);
```

`citus_move_shard_placement` 还会移动与指定分片共置的任何分片，以保持其共置状态。

## 查看查询统计信息 {#viewing-query-statistics}

> [!NOTE]
> 从 11.0 版起，Citus 社区版包含 `citus_stat_statements` 视图。

管理 Citus 集群时，了解用户运行哪些查询、涉及哪些节点以及 Citus 对每个查询使用哪个执行方法很有用。 Citus 在一个名为 `citus_stat_statements` 的元数据视图中记录查询统计信息，其命名方式类似于 PostgreSQL 的 [pg_stat_statements](https://www.postgresql.org/docs/current/static/pgstatstatements.html)。 而 `pg_stat_statements` 存储有关查询持续时间和 I/O 的信息，`citus_stat_statements` 存储有关 Citus 执行方法和分片分区键的信息（如果适用）。

Citus 需要安装 `pg_stat_statements` 扩展，才能跟踪查询统计信息。在我们的 `cloud_topic` 上，该扩展已预先启用；自托管的 PostgreSQL 实例则需要通过 `postgresql.conf` 的 `shared_preload_libraries` 加载扩展，再执行 SQL 创建扩展：

```sql
CREATE EXTENSION pg_stat_statements;
```

下面来看具体过程。假设有一张名为 `foo` 的表，按其 `id` 列进行哈希分布。

```sql
-- create and populate distributed table
create table foo ( id int );
select create_distributed_table('foo', 'id');

insert into foo select generate_series(1,100);
```

你又运行了两个查询，`citus_stat_statements` 显示 Citus 如何选择执行它们。

```sql
-- counting all rows executes on all nodes, and sums
-- the results on the coordinator
SELECT count(*) FROM foo;

-- specifying a row by the distribution column routes
-- execution to an individual node
SELECT * FROM foo WHERE id = 42;
```

要了解这些查询如何执行，可以查询统计信息表：

```sql
SELECT * FROM citus_stat_statements;
```

结果：

```text
-[ RECORD 1 ]-+----------------------------------------------
queryid       | -6844578505338488014
userid        | 10
dbid          | 13340
query         | SELECT count(*) FROM foo;
executor      | adaptive
partition_key |
    calls         | 1
    -[ RECORD 2 ]-+----------------------------------------------
    queryid       | 185453597994293667
    userid        | 10
    dbid          | 13340
    query         | insert into foo select generate_series($1,$2)
    executor      | insert-select
    partition_key |
    calls         | 1
    -[ RECORD 3 ]-+----------------------------------------------
    queryid       | 1301170733886649828
    userid        | 10
    dbid          | 13340
    query         | SELECT * FROM foo WHERE id = $1
    executor      | adaptive
    partition_key | 42
    calls         | 1
```

可以看到，Citus 最常使用自适应执行器执行查询。该执行器将查询拆成子查询，发送到相关节点执行，再在协调节点合并结果。对于第二个查询（按分布列 `id = $1` 过滤），Citus 判定只需访问一个节点的数据。最后，`insert into foo select...` 语句使用 insert-select 执行器，灵活处理这类查询。

### citus_stats 视图（Citus 13.2） {#citus_stats-view-citus-132}

有关集群范围的列统计信息，请参阅视图参考：[citus_stats](/citus/reference/api-metadata/#citus_stats-view)。

### 租户级统计信息 {#tenant-level-statistics}

到目前为止，这个视图提供的信息，都可以通过对单条查询执行 `EXPLAIN` 获得。但除了查看单个查询，`citus_stat_statements` 还可以回答“集群中有多少比例的查询仅涉及单个租户”等问题。

```sql
SELECT sum(calls),
       partition_key IS NOT NULL AS single_tenant
FROM citus_stat_statements
GROUP BY 2;
```

```text
    .
     sum | single_tenant
    -----+---------------
       2 | f
       1 | t
```

例如，在多租户数据库中，预期大多数查询都只涉及单个租户。如果出现过多跨租户查询，可能说明查询缺少恰当的租户过滤条件，因而消耗了不必要的资源。

若要调查哪些租户最活跃，请使用 `citus_stat_tenants` 视图。

### 统计信息过期时间 {#statistics-expiration}

`pg_stat_statements` 视图会限制所跟踪的语句数量和记录保留时长。由于 `citus_stat_statements` 跟踪的查询是 `pg_stat_statements` 的严格子集，两者采用相同上限时，保留的数据可能不一致。这种记录不匹配可能使两个视图之间的连接产生不可预测的结果。

三种方法有助于同步视图，你可以结合使用这三种方法。

1. 让维护守护进程定期同步 Citus 和 PostgreSQL 的统计信息。`citus.stat_statements_purge_interval` GUC 设置同步间隔，单位为秒；设为 0 则禁用定期同步。
2. 调整 `citus_stat_statements` 的条目数上限。新增条目使总数超过 `citus.stat_statements_max` GUC 所设阈值时，会移除旧条目。默认值为 50K，最大允许值为 10M。每个条目约占 140 字节共享内存，因此应合理设置。
3. 调高 `pg_stat_statements.max`。默认值为 5,000，调高至 10K、20K，甚至 50K，通常也不会带来很大开销。当本地（即协调节点上的）查询工作负载较多时，这种方法尤其有用。

> [!NOTE]
> 修改 `pg_stat_statements.max` 或 `citus.stat_statements_max` 后，需要重启 PostgreSQL 服务。修改 `citus.stat_statements_purge_interval` 后，调用 [pg_reload_conf()](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL) 即可生效。

## 节约资源 {#resource-conservation}

### 限制长时间运行的查询 {#limiting-long-running-queries}

长时间运行的查询可能持有锁、导致 WAL 积压，或消耗大量系统资源。生产环境中应避免查询运行过久。要取消超时查询，可在协调节点和工作节点上设置 [statement_timeout](https://www.postgresql.org/docs/current/static/runtime-config-client.html#GUC-STATEMENT-TIMEOUT) 参数。

```sql
-- limit queries to five minutes
ALTER DATABASE citus
  SET statement_timeout TO 300000;
SELECT run_command_on_workers($cmd$
  ALTER DATABASE citus
    SET statement_timeout TO 300000;
$cmd$);
```

指定超时（以毫秒为单位）。

若要自定义每个查询的超时，请在事务中使用 `SET LOCAL`。

````postgres
```sql

BEGIN;
-- this limit applies to just the current transaction
SET LOCAL statement_timeout TO 300000;

-- ...
COMMIT;
````

## 安全性 {#security}

### 连接管理 {#connection-management}

> [!NOTE]
> 从 Citus 8.1.0（2018-12-17 发布）开始，新安装的集群会加密节点之间的通信。这种加密使用 TLS 和自签名证书，**不能防范中间人攻击**，只能防止网络上的被动窃听。
> 
> 最初使用 Citus 8.1.0 之前版本创建的集群，节点间不会启用网络加密，之后升级也不会自动启用。要为此类部署设置自签名 TLS，请按 [PostgreSQL 官方文档](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CERTIFICATE-CREATION)操作，并应用此处介绍的 Citus 专用设置，例如将 `citus.node_conninfo` 改为 `sslmode=require`。协调节点和工作节点都需要进行此配置。

Citus 节点相互通信时，会查询保存连接凭据的表。数据库管理员可以据此灵活调整参数，兼顾安全性和效率。

若要为所有节点连接设置非敏感的 libpq 连接参数，请更新 `citus.node_conninfo` GUC：

```sql

-- key=value pairs separated by spaces.
-- For example, ssl options:

ALTER SYSTEM SET citus.node_conninfo =
  'sslrootcert=/path/to/citus-ca.crt sslcrl=/path/to/citus-ca.crl sslmode=verify-full';
```

该 GUC 只接受允许列表中的参数，详见 [node_conninfo](/citus/reference/api-guc/#citusnode_conninfo-text) 参考。从 Citus 8.1 开始，`node_conninfo` 默认为 `sslmode=require`，禁止节点间未加密的通信。如果集群最初创建于 Citus 8.1 之前，该值为 `sslmode=prefer`。在所有节点上配置自签名证书后，应将其改为 `sslmode=require`。

更改此设置后，重新加载 PostgreSQL 配置。虽然新设置可能在所有会话中都可见，但 Citus 只在建立新连接时读取它。收到重新加载信号后，Citus 会将所有现有连接标记为待关闭；当前运行的事务完成后，连接将关闭并重新建立。

```sql

SELECT pg_reload_conf();
```

> [!WARNING]
> 9.2.4 之前的 Citus 版本需要重启才能关闭现有连接。
> 
> 对于这些旧版本，重新加载配置不会触发连接关闭及重新连接。需要重启服务器，才能强制所有连接使用新设置。

```sql

-- only superusers can access this table

-- add a password for user jdoe
INSERT INTO pg_dist_authinfo
  (nodeid, rolename, authinfo)
VALUES
  (123, 'jdoe', 'password=abc123');
```

在此 `INSERT` 之后，任何需要以用户 jdoe 身份连接到节点 123 的查询都会使用提供的密码。 关于[pg_dist_authinfo](/citus/reference/api-metadata/#connection-credentials-table)的文档中包含更多信息。

```sql

-- update user jdoe to use certificate authentication
UPDATE pg_dist_authinfo
SET authinfo = 'sslcert=/path/to/user.crt sslkey=/path/to/user.key'
WHERE nodeid = 123 AND rolename = 'jdoe';
```

此变更使用户连接节点 123 时，从密码认证切换为使用证书和密钥文件。应确保用户证书由目标工作节点信任的证书签署，且工作节点的认证设置允许证书认证。客户端证书的完整使用说明见 [PostgreSQL libpq 文档](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT)。

更改 `pg_dist_authinfo` 不会强制任何现有连接重新连接。

### 设置由证书颁发机构签署的证书 {#setup-certificate-authority-signed-certificates}

本节假定有一个受信任的证书颁发机构（CA），能够为集群中的所有节点签发服务器证书。请与所在组织的安全部门合作，避免错误处理密钥材料。本指南仅介绍需要应用的 Citus 专用配置，不涵盖 PKI 管理的最佳实践。

集群中的所有节点都需要由*同一证书颁发机构*签署的有效证书。每台机器上应有以下**该机器专用**的文件：

- `/path/to/server.key`：服务器私钥
- `/path/to/server.crt`：与服务器密钥对应的服务器证书或证书链，由受信任的证书颁发机构签署。

除上述机器专用文件外，还需要以下集群或 CA 范围内共用的文件：

- `/path/to/ca.crt`：证书颁发机构的证书
- `/path/to/ca.crl`：证书颁发机构的证书吊销列表

> [!NOTE]
> 证书吊销列表可能随时间变化。请与安全部门合作，建立机制，及时更新集群所有节点上的吊销列表。更新后，需要重新加载每个节点的配置。

在节点上设置所有文件后，请在 PostgreSQL 配置文件中配置以下设置：

```ini

# the following settings allow the PostgreSQL server to enable ssl, and

# configure the server to present the certificate to clients when

# connecting over tls/ssl

ssl = on
ssl_key_file = '/path/to/server.key'
ssl_cert_file = '/path/to/server.crt'

# this will tell citus to verify the certificate of the server it is connecting to

citus.node_conninfo = 'sslmode=verify-full sslrootcert=/path/to/ca.crt sslcrl=/path/to/ca.crl'
```

更改这些设置后，请重启数据库或重新加载配置以应用这些更改。 如果使用低于 9.2.4 的 Citus 版本，则需要重启。 此外，可能需要调整 `local_hostname` 以确保 `sslmode=verify-full` 的正常运行。

根据所用 CA 的策略，可能需要或希望将 `citus.node_conninfo` 中的 `sslmode=verify-full` 改为 `sslmode=verify-ca`。两种设置的区别见 [PostgreSQL 官方文档](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS)。

最后，要禁止用户通过未加密连接访问数据库，需要修改 `pg_hba.conf`。许多 PostgreSQL 安装包含 `host` 条目，同时允许 SSL/TLS 和普通 TCP 连接。将所有 `host` 条目替换为 `hostssl` 后，只有加密连接才能通过 PostgreSQL 认证。完整说明见 PostgreSQL 官方文档中的 [pg_hba.conf 文件](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)。

> [!NOTE]
> 如果没有可用的受信任 CA，可以使用自签名根证书建立自己的 CA。这个过程较为复杂，应向安全团队寻求指导。

要验证协调节点到工作节点的连接是否已加密，可以执行以下查询，查看这些连接使用的 SSL/TLS 版本：

```sql

SELECT run_command_on_workers($$
  SELECT version FROM pg_stat_ssl WHERE pid = pg_backend_pid()
$$);
```

```text

    ┌────────────────────────────┐
    │   run_command_on_workers   │
    ├────────────────────────────┤
    │ (localhost,9701,t,TLSv1.2) │
    │ (localhost,9702,t,TLSv1.2) │
    └────────────────────────────┘
    (2 rows)
```

### 提高工作节点安全性 {#increasing-worker-security}

为方便起见，多节点安装说明将工作节点 `pg_hba.conf` 中本地网络连接的[认证方法](https://www.postgresql.org/docs/current/static/auth-methods.html)设为 “trust”。但实际部署可能需要更高的安全性。

若要要求所有连接都提供哈希密码，请使用如下所示的内容更新每个工作节点上的 PostgreSQL `pg_hba.conf` ：

```bash

# Require password access and a ssl/tls connection to nodes in the local

# network. The following ranges correspond to 24, 20, and 16-bit blocks

# in Private IPv4 address spaces.

hostssl    all             all             10.0.0.0/8              md5

# Require passwords and ssl/tls connections when the host connects to

# itself as well.

hostssl    all             all             127.0.0.1/32            md5
hostssl    all             all             ::1/128                 md5
```

协调节点需要知道各角色的密码才能与工作节点通信。我们的 `cloud_topic` 会代为维护这类信息，但使用 Citus 社区版时，需要在 [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html) 文件中维护认证信息。编辑 postgres 用户主目录中的 .pgpass 文件，为每个工作节点地址与角色的组合添加一行：

*hostname:port:database:username:password*

工作节点有时需要相互连接，例如执行[重分区连接](/citus/reference/reference-sql/#repartition-joins)时。因此，每个工作节点也需要一份 .pgpass 文件。

### 行级安全性 {#row-level-security}

> [!NOTE]
> 从 11.0 版起，Citus 社区版支持分布式表的行级安全。

PostgreSQL 的[行级安全](https://www.postgresql.org/docs/current/static/ddl-rowsecurity.html)策略按用户限制普通查询可返回哪些行，以及数据修改命令可插入、更新或删除哪些行。这在多租户 Citus 集群中尤其有用：可以赋予租户完整的 SQL 数据库访问能力，同时使其无法看到其他租户的信息。

可以将数据库角色的命名约定与表的行级安全策略结合，实现租户数据隔离。为每个租户按编号分配数据库角色：`tenant_1`、`tenant_2`，依此类推。租户使用不同角色连接 Citus。行级安全策略将角色名与 `tenant_id` 分布列的值比较，以决定是否允许访问。

以下示例在一张按 `tenant_id` 分布的简化事件表上演示此方法。先创建 `tenant_1` 和 `tenant_2` 角色，再以管理员身份执行以下命令：

````sql

``` sql
CREATE TABLE events(
  tenant_id int,
  id int,
  type text
);

SELECT create_distributed_table('events','tenant_id');

INSERT INTO events VALUES (1,1,'foo'), (2,2,'bar');

-- assumes that roles tenant_1 and tenant_2 exist
GRANT select, update, insert, delete
  ON events TO tenant_1, tenant_2;
````

当前，任何具有该表 SELECT 权限的用户都能看到这两行。任一租户的用户都能查看并更新另一个租户的行。可以用表的行级安全策略解决这一问题。

每个策略包含 `USING` 和 `WITH CHECK` 两个子句。用户尝试读取或写入行时，数据库逐行按这些子句检查。现有行按 `USING` 表达式检查；由 `INSERT` 或 `UPDATE` 产生的新行按 `WITH CHECK` 表达式检查。

```sql
-- first a policy for the system admin "citus" user
CREATE POLICY admin_all ON events
  TO citus           -- apply to this role
  USING (true)       -- read any existing row
  WITH CHECK (true); -- insert or update any row

-- next a policy which allows role "tenant_<n>" to
-- access rows where tenant_id = <n>
CREATE POLICY user_mod ON events
  USING (current_user = 'tenant_' || tenant_id::text);
  -- lack of CHECK means same condition as USING

-- enforce the policies
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
```

现在角色 `tenant_1` 和 `tenant_2` 针对其各自的查询获得不同的结果：

**以 tenant_1 身份连接：**

```sql
SELECT * FROM events;
```

```text
┌───────────┬────┬──────┐
│ tenant_id │ id │ type │
├───────────┼────┼──────┤
│         1 │ 1  │ foo  │
└───────────┴────┴──────┘
```

**以 tenant_2 身份连接：**

```sql
SELECT * FROM events;
```

```text
┌───────────┬────┬──────┐
│ tenant_id │ id │ type │
├───────────┼────┼──────┤
│         2 │ 2  │ bar  │
└───────────┴────┴──────┘
```

```sql
-- connected as tenant_1INSERT INTO events VALUES (3,3,'surprise');
/*
ERROR: new row violates row-level security policy for table "events_102055"
*/
```

## PostgreSQL 扩展 {#postgresql-extensions}

Citus 提供分布式功能，通过挂钩和扩展 API 扩展 PostgreSQL。 此方法使你能够受益于丰富的 PostgreSQL 生态系统中的功能。 这些功能包括但不限于对各种 [数据类型](http://www.postgresql.org/docs/current/static/datatype.html) （包括 jsonb 和 hstore 等半结构化数据类型）、 [运算符和函数](http://www.postgresql.org/docs/current/static/functions.html)、全文搜索和其他扩展（如 [PostGIS](http://postgis.net/) 和 [HyperLogLog](https://github.com/aggregateknowledge/postgresql-hll)）的支持。 正确使用扩展 API 可实现与标准 PostgreSQL 工具（如 [pgAdmin](http://www.pgadmin.org/) 和 [pg_upgrade](http://www.postgresql.org/docs/current/static/pgupgrade.html)）的兼容性。

Citus 可以安装在任何 PostgreSQL 实例上，因此可直接与 hstore、hll、PostGIS 等其他扩展配合使用。但若在 `shared_preload_libraries` 中同时加载其他扩展，Citus 必须排在第一位。

> [!NOTE]
> 有些扩展功能无法直接用于 Citus。例如，扩展中的某些聚合可能需要调整，才能跨多个节点并行执行。如果某个扩展的功能与 Citus 配合使用时不符合预期，请[联系我们](https://www.citusdata.com/about/contact_us)。

除了核心 Citus 扩展之外，我们还维护了其他几个扩展：

- [cstore_fdw](https://github.com/citusdata/cstore_fdw) — 用于分析的列式存储。只从磁盘读取相关数据来提高性能，还可能将数据压缩至原来的六分之一到十分之一，从而减少数据归档的空间需求。
- [pg_cron](https://github.com/citusdata/pg_cron) - 直接从数据库运行定期作业。
- [postgresql-topn](https://github.com/citusdata/postgresql-topn) — 按特定条件返回数据库中排名靠前的值。它使用近似算法，以较少的计算和内存资源快速返回结果。
- [postgresql-hll](https://github.com/citusdata/postgresql-hll) — 将 HyperLogLog 数据结构实现为原生数据类型。这种固定大小、类似集合的结构用于统计不同值的数量，精度可调。

## 创建新数据库 {#creating-a-new-database}

每个 PostgreSQL 服务器可以包含[多个数据库](https://www.postgresql.org/docs/current/static/manage-ag-overview.html)。新数据库不会继承其他数据库的扩展，必须逐一添加所需扩展。要在新数据库中使用 Citus，需在协调节点和工作节点上创建数据库，在其中创建 Citus 扩展，然后在协调节点的数据库中注册工作节点。

连接到每个工作节点并运行：

```psql
-- on every worker node

CREATE DATABASE newbie;
\c newbie
CREATE EXTENSION citus;
```

然后在协调节点上运行：

```psql
CREATE DATABASE newbie;
\c newbie
CREATE EXTENSION citus;

SELECT * from citus_add_node('node-name', 5432);
SELECT * from citus_add_node('node-name2', 5432);
-- ... for all of them
```

现在，新数据库作为另一个 Citus 集群运行。

## 相关内容 {#related-content}

- [Citus 表管理](/citus/operations/table-management/)
- [升级 Citus](/citus/operations/upgrade-citus/)
- [Citus 的诊断查询](/citus/operations/diagnostic-queries/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
