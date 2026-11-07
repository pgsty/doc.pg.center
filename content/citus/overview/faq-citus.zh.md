---
title: Citus for PostgreSQL 常见问题
description: 解答 Citus 主键、节点管理、分片分布、故障切换与 PostgreSQL 功能支持等常见问题。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/faq-citus?view=citus-14
upstream_ref: citus-14; be6cf64ecd13
translation_status: translated
---

本文解答 Citus for PostgreSQL 的常见问题，涵盖主键、节点管理、分片分布、故障切换与 PostgreSQL 功能支持。初次接触 Citus，可先阅读[什么是 Citus？](/citus/overview/what-is-citus/)。

## 基本问题 {#general}

### 可以在分布式表上创建主键吗？ {#can-i-create-primary-keys-on-distributed-tables-}

目前，只有主键包含分布列时，Citus 才能实施主键约束。这样只需检查一个分片，就能保证唯一性。

### 哪些 PostgreSQL 功能不受 Citus 支持？ {#are-there-any-postgresql-features-not-supported-by-citus-}

Citus 通过扩展 PostgreSQL 提供分布式能力，因此使用标准 PostgreSQL SQL 语法。大多数查询都受支持，包括通过网络组合多个数据库节点的数据，以及跨节点事务语义。当前 SQL 支持范围见[变通方案](/citus/reference/reference-workarounds/#workarounds)。

此外，对于仅访问集群中单个节点的查询，Citus 提供 100% 的 SQL 支持。这类查询很常见，例如多租户应用中，不同节点存储不同租户的数据。详情见[什么是 Citus？](/citus/overview/what-is-citus/)。

即使 SQL 支持范围很广，数据建模仍可能显著影响查询性能。Citus 的查询执行方式见[查询处理](/citus/reference/reference-processing/)。

### 可以在 Microsoft Azure 上运行 Citus 吗？ {#can-i-run-citus-on-microsoft-azure-}

可以。Citus 通过 [Azure Database for PostgreSQL Flexible server 弹性集群](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508)提供托管服务。

## 集群管理 {#cluster-management}

### 如何为现有 Citus 集群添加节点？ {#how-do-i-add-nodes-to-an-existing-citus-cluster-}

使用 Azure Database for PostgreSQL 弹性集群上的 Citus 托管服务时，可通过 Azure 门户或 Azure CLI 添加节点。使用开源 Citus 时，可调用 `citus_add_node` 用户定义函数（UDF），传入新节点的主机名或 IP 地址以及端口号，手动添加节点。

无论使用哪种方式，新节点刚加入现有集群时都没有数据（分片）。Citus 会开始将新创建的分片分配给该节点。若要将旧节点上的已有分片重新均衡到新节点，可使用开源分片再平衡器。详情见[并行再平衡](/citus/operations/cluster-management/#parallel-rebalancing)。

### Citus 如何处理工作节点故障？ {#how-does-citus-handle-failure-of-a-worker-node-}

Citus 使用 PostgreSQL 流复制，原样复制整个工作节点：将工作节点的 WAL 记录持续发送到备用节点。在自建环境中，可参照 [PostgreSQL 复制文档](https://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION)自行配置流复制。

### Citus 如何处理协调节点的故障切换？ {#how-does-citus-handle-failover-of-the-coordinator-node-}

Citus 协调节点类似于标准 PostgreSQL 服务器，因此可以使用常规的 PostgreSQL 同步复制与故障切换，提高其可用性。许多 Citus 客户通过同步复制增强协调节点故障时的韧性。详情见[处理节点故障](/citus/operations/cluster-management/#dealing-with-node-failures)。

### 工作节点的地址变了怎么办？ {#what-if-a-worker-node-s-address-changes-}

工作节点的主机名或 IP 地址发生变化时，需要使用 `citus_update_node` 通知协调节点：

```sql
-- update worker node metadata on the coordinator
-- (remember to replace 'old-address' and 'new-address'
--  with the actual values for your situation)

select citus_update_node(nodeid, 'new-address', nodeport)
  from pg_dist_node
 where nodename = 'old-address';
```

执行更新之前，协调节点无法与该工作节点通信并执行查询。

## 分片与数据分布 {#sharding-and-distribution}

### 按哈希划分数据时，如何选择分片数量？ {#how-do-i-choose-the-shard-count-when-i-hash-partition-my-data-}

首次将表转换为分布式表时，需要选择分片数量。不同共置组可设置不同值，最佳值取决于使用场景。集群创建后也能修改分片数量，但操作较为复杂。可按以下原则选择。

对于[多租户应用](/citus/tutorials/tutorial-multi-tenant/)，选择 32～128 个分片。较小的负载（不足 100 GB）可从 32 个分片开始；较大的负载选择 64 或 128 个分片。工作节点规模可扩展到 32～128 台。

对于[实时分析](/citus/tutorials/tutorial-analytics/)，应将分片数量与工作节点的 CPU 核心总数关联。为获得最大并行度，每个节点上的分片应足够多，至少每个 CPU 核心对应一个分片。初始分片数可设为当前 CPU 核心数的两倍或四倍，为日后增加工作节点和 CPU 核心留出扩容空间。

要为待分布的表设置分片数量，可修改 `citus.shard_count`。该参数影响之后的 `create_distributed_table` 调用。例如：

```sql
SET citus.shard_count = 64;
-- any tables distributed at this point will have
-- sixty-four shards
```

详情见[选择集群规模](/citus/operations/cluster-management/#choosing-cluster-size)。

### 如何修改哈希分布表的分片数量？ {#how-do-i-change-the-shard-count-for-a-hash-partitioned-table-}

Citus 提供 `alter_distributed_table` 函数，可修改分布式表的分片数量。

### 某个租户的数据位于哪个分片？ {#which-shard-contains-data-for-a-particular-tenant-}

Citus 提供 UDF 和元数据表，用于确定分布列值对应的分片，以及该分片在工作节点上的放置位置。详情见[查找特定租户数据所在的分片](/citus/operations/diagnostic-queries/#finding-which-shard-contains-data-for-a-specific-tenant)。

### 忘记表的分布列了，如何查找？ {#i-forgot-the-distribution-column-of-a-table--how-do-i-find-it-}

Citus 协调节点的元数据表中保存了这些信息。详情见[查找表的分布列](/citus/operations/diagnostic-queries/#finding-the-distribution-column-for-a-table)。

### 可以按多个键分布一张表吗？ {#can-i-distribute-a-table-by-multiple-keys-}

不可以，每张表必须选择单个列作为分布列。时序数据是常见的希望按两列分布的场景；此时应按一个非时间列进行哈希分布，再结合 PostgreSQL 按时间列分区。详情见[时序数据](/citus/modeling/data-modeling/#time-series-data)。

### 多租户应用可以在 Citus 中按模式分片吗？ {#can-i-shard-by-schema-on-citus-for-multitenant-applications-}

可以。Citus 自 12.0 起支持[基于模式的分片](/citus/overview/what-is-citus/#schema-based-sharding)。

## 查询与性能 {#queries-and-performance}

### Citus 如何支持 count(distinct) 查询？ {#how-does-citus-support-count-distinct--queries-}

Citus 既能在单个工作节点内，也能跨工作节点计算 `count(distinct)` 聚合。按表的分布列聚合时，可将计数下推到工作节点，再汇总结果；其他情况下，可将去重后的行拉取到协调节点计算。如果传输到协调节点的代价过高，也可使用快速近似计数。详情见 [Count(distinct) 聚合](/citus/reference/reference-sql/#countdistinct-aggregates)。

### 为什么会出现 max_intermediate_result_size 错误？ {#why-am-i-seeing-an-error-about-max-intermediate-result-size-}

某些包含子查询或 CTE 的查询，需要由 Citus 分多个步骤执行。在[推拉式执行](/citus/reference/reference-processing/#subquery-and-cte-push-pull-execution)中，Citus 将子查询结果推送到所有工作节点，供主查询使用。如果结果过大，可能产生难以接受的网络开销，甚至耗尽协调节点用于收集和分发结果的存储空间。

Citus 用 `citus.max_intermediate_result_size` 设置子查询结果大小的阈值；超过该阈值就取消查询。错误信息如下：

```text
ERROR: the intermediate result size exceeds citus.max_intermediate_result_size (currently 1 GB)
DETAIL: Citus restricts the size of intermediate results of complex subqueries and CTEs to avoid accidentally pulling large result sets into once place.
HINT: To run the current query, set citus.max_intermediate_result_size to a higher value or -1 to disable.
```

按错误提示，可谨慎调高该参数：

```sql
SET citus.max_intermediate_result_size = '3GB';
```

## 表与约束 {#tables-and-constraints}

### 分布式表在什么情况下支持唯一约束？ {#in-which-situations-are-uniqueness-constraints-supported-on-distributed-tables-}

只有受约束的列包含分布列时，Citus 才能实施主键或唯一约束。如果主键只有一列，该列必须是分布列。

这一限制使唯一性检查能够在单个分片内完成，由工作节点上的 PostgreSQL 高效执行。

### 为什么 pg_relation_size 显示分布式表大小为零字节？ {#why-does-pg-relation-size-report-zero-bytes-for-a-distributed-table-}

分布式表的数据位于工作节点的分片中，而非协调节点。真实大小需要将各分片大小相加。Citus 提供了查询这些信息的辅助函数，详情见[表管理](/citus/operations/table-management/)。

## 数据库对象 {#database-objects}

### 如何在 Citus 集群中创建角色、函数、扩展等数据库对象？ {#how-do-i-create-database-roles--functions--extensions--and-other-objects-in-a-citus-cluster-}

在协调节点上执行的某些命令不会传播到工作节点：

- `CREATE ROLE/USER`
- `CREATE DATABASE`
- `ALTER ... SET SCHEMA`
- `ALTER TABLE ALL IN TABLESPACE`
- `CREATE TABLE`，参见[表类型](/citus/overview/what-is-citus/#table-types)

这类对象需要在所有节点上显式创建。Citus 提供了在所有工作节点上执行查询的函数：

```sql
SELECT run_command_on_workers($cmd$
  /* the command to run */
  CREATE ROLE ...
$cmd$);
```

详情见[手动传播命令](/citus/reference/reference-propagation/)。手动传播 `CREATE DATABASE` 后，仍需在新数据库中安装 Citus，参见[创建新数据库](/citus/operations/cluster-management/#creating-a-new-database)。

自 Citus 13.1 起，更多数据库与角色 DDL 会自动传播，具体见[数据库与角色管理 DDL](/citus/reference/reference-ddl/#database-and-role-management-ddl)。

今后 Citus 会自动传播更多类型的对象。自动传播的优势在于：新增工作节点时，Citus 会自动创建这些对象的副本。详情见[分布式对象表](/citus/reference/api-metadata/#distributed-object-table)。

## 扩展与存储 {#extensions-and-storage}

### cstore_fdw 如何与 Citus 配合使用？ {#how-does-cstore-fdw-work-with-citus-}

在 PostgreSQL 12 及更高版本上，无须安装 cstore_fdw，因为 Citus 已直接实现 `columnar` 列式存储。与 cstore_fdw 不同，Citus 列存表支持事务语义、复制和 `pg_upgrade`。对于大型数据集的归档与报表，可以同时利用 Citus 的查询并行、透明分片与高可用能力，以及列存的高压缩率和高 I/O 利用率。

## 迁移与历史项目 {#migration-and-legacy}

### pg_shard 后来怎样了？ {#what-happened-to-pg-shard-}

pg_shard 扩展已弃用，不再受支持。

从 Citus v5.x 的开源版本开始，Citus 团队将 pg_shard 代码合入 Citus，提供统一方案。该方案带来了此前仅面向 CitusDB 客户的高级分布式查询规划能力，同时保留 pg_shard 为 PostgreSQL 生态带来的简单透明分片和实时读写。旗舰产品 Citus 的功能涵盖并超出了 pg_shard。Citus 团队提供迁移步骤，帮助现有用户直接替换 pg_shard。更多信息可[联系项目团队](https://www.citusdata.com/about/contact_us)。

## 相关内容 {#related-content}

- [什么是 Citus？](/citus/overview/what-is-citus/)
- [教程：设计多租户数据库](/citus/tutorials/tutorial-multi-tenant/)
- [教程：设计实时分析仪表盘](/citus/tutorials/tutorial-analytics/)
