---
title: 什么是 Citus？
description: 了解 Citus 的节点、分片模型、表类型、分片放置、共置与查询执行等核心概念。
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/what-is-citus?view=citus-14
upstream_ref: citus-14; a4ec7e731f6c
translation_status: translated
---

Citus 是用于横向扩展 PostgreSQL 的开源扩展。你可以从单节点起步，逐步扩展为分布式集群。Citus 是扩展而非数据库分支，因此保留了原生 PostgreSQL 的兼容性、功能、生态工具与扩展。

主要能力包括：

- 分布式表，支持基于行和基于模式的分片
- 用于维度数据或共享数据的参考表
- 共置连接与分布式查询规划器
- 跨工作节点的并行查询执行
- 可选的列式存储
- MX 模式下从任意节点发起查询，自 Citus 11.0 起支持

Citus 通常用于提高多租户 SaaS、实时分析仪表盘、时序数据及微服务状态管理的性能与扩展能力。

使用方式：

1. **开源版本**：[下载 Citus](https://www.citusdata.com/download/)，或从 [GitHub 仓库](https://github.com/citusdata/citus)构建。
2. **托管服务**：使用 [Azure Database for PostgreSQL Flexible server 弹性集群](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508)。

以下内容将原先的“概览”和“概念”文章合并为一份完整指南。

## 架构概念 {#architecture-concepts}

本节介绍 Citus 实现分布式数据库的基本组成：节点如何协作、数据如何划分、有哪些表抽象，以及查询如何并行执行。

### 节点与集群 {#nodes-and-cluster}

Citus 让普通服务器（*节点*）以无共享架构协作。多个节点构成一个*集群*，可以容纳比单机更多的数据，使用更多 CPU 核心。添加工作节点即可扩容。

### 协调节点与工作节点 {#coordinator-and-workers}

每个集群包含一个*协调节点*和一个或多个*工作节点*。Citus 内部元数据表记录工作节点的健康状况、节点地址与分片放置位置，并将这些元数据同步到每个节点。应用可连接协调节点；在 MX 模式下，也可连接任意工作节点（自 Citus 11.0 起支持）。接收查询的节点根据表分布元数据，将查询路由到相应节点或拆分为并行任务。接收节点模型的详情见 [Citus 查询处理](/citus/reference/reference-processing/#query-entry-points-and-mx-mode)。

对于每条查询，接收节点会采取以下一种方式：

- 所需数据都在一个工作节点上时，将查询路由到该节点。
- 数据跨越多个分片时，让多个工作节点并行执行。

### 分片模型 {#sharding-models}

> [!NOTE]
> Azure 托管环境中分片模型的完整说明，见 [Azure Cosmos DB for PostgreSQL 的分片模型](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/concepts-sharding-models)。

Citus 支持两种分片模型，各有取舍：

| 模型 | 说明 | 适用场景 | 注意事项 |
| --- | --- | --- | --- |
| 基于行的分片 | 共享模式，通过表中的分布列（分片键）区分租户 | 高密度多租户、物联网、时序数据 | 需要添加分布列和查询过滤条件；硬件利用效率最高 |
| 基于模式的分片 | 每个租户拥有独立模式，自 Citus 12.0 引入 | 微服务、租户模式各异、希望尽量少改应用 | 租户密度较低；接入更简单；需按租户设置 `search_path` |

#### 基于行的分片 {#row-based-sharding}

这是 Citus 的经典模型：一个数据库，共享同一模式。指定的 `dist_column` 标识租户或分布键，并决定数据行所属的分片。该模型能密集容纳租户，尽可能提高硬件利用率，但需要调整模式和应用查询，使其包含分布列并按该列过滤。

优点：

- 租户密度最高
- 性能特性最好

缺点：

- 需要修改模式和查询
- 所有租户使用统一模式

#### 基于模式的分片 {#schema-based-sharding}

该模型在 Citus 12.0 中引入。每个租户或微服务使用自己的模式，模式映射到分片组。查询只需极少改动，通常只要设置正确的 `search_path`。

优点：

- 允许租户采用不同模式
- 应用和查询改动很少
- 迁移路径更简单

缺点：

- 与基于行的分片相比，每个节点可容纳的租户较少

### 表类型 {#table-types}

> [!NOTE]
> Azure 托管环境中表类型的详细说明，见 [Azure Cosmos DB for PostgreSQL 的表类型](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/concepts-nodes#table-types)。

Citus 提供以下表抽象：

| 类型 | 用途 | 说明 |
| --- | --- | --- |
| 分布式表 | 跨工作节点横向分片 | 需要分布列，基于模式的分片除外 |
| 参考表 | 在每个工作节点完整复制的小表 | 适合维度或枚举数据 |
| 本地表 | 普通 PostgreSQL 表，不分片 | 未纳入管理时仅存在于协调节点 |
| 受管本地表 | 已登记在元数据中的本地表 | 可在整个集群查询；在 `citus_tables` 中显示为 `local` |
| 模式表 | 分布式模式中的表，用于基于模式的分片 | 自动共置，无须显式指定分片键 |

#### 分布式表 {#distributed-tables}

对用户而言像普通表，底层由各个分片表（如 `table_1001`）组成。DDL 变更会传播到全部分片。可使用分布式表辅助函数创建，参见 [创建与分布表](/citus/reference/reference-ddl/#creating-and-distributing-tables)。

##### 分布列 {#distribution-column}

对分布列执行确定性的哈希计算，将数据行映射到分片。合理选择分布列有助于提高性能，并实现共置。参见分布式数据建模指南。

#### 参考表 {#reference-tables}

参考表只有一个分片，并在每个工作节点上保留副本，可避免产品分类等常用查找产生的网络开销。写入通过两阶段提交保证一致性，参见 [参考表](/citus/reference/reference-ddl/#reference-tables)。

#### 本地表与受管本地表 {#local-and-local-managed-tables}

这类表是协调节点上的普通表。可通过 `citus_add_local_table_to_metadata` 将其纳入管理，也可用 `enable_local_ref_fkeys` 开启外键自动登记，之后便可从任意节点访问。

#### 模式表 {#schema-tables}

在基于模式的分片中，分布式模式中的表会自动成为共置的分布式表，无须手动选择分片键。它们在 `citus_tables` 中显示为 `schema`。

### 分片与放置位置 {#shards-and-placements}

分布式表会被拆分成多个分片，在工作节点上以普通表存储，例如 `github_events_102027`。协调节点的元数据（如 `pg_dist_shard`）将哈希范围映射到分片 ID；*分片放置（placement）*将分片 ID 映射到工作节点。为保障持久性，复制使用 PostgreSQL 流复制实现，不由 Citus 元数据管理。

### 共置 {#colocation}

将相关表的分片按相同哈希映射放到一起，可以在节点本地执行连接。例如，让 `stores`、`products` 和 `purchases` 共用 `store_id`。共置可减少跨节点数据传输，参见 [表共置](/citus/modeling/data-modeling/#table-colocation)。

### 查询并行与执行流程 {#query-parallelism-and-execution-flow}

接收节点（协调节点，或 MX 模式中的任意工作节点）将跨分片查询拆成各分片上的*任务*。任务执行需要平衡：

- 并发度，即每个工作节点的并行连接数
- 连接开销，通过慢启动逐步增加连接
- 工作节点资源占用，通过限制空闲连接控制

关键设置：

| 设置 | 用途 |
| --- | --- |
| `max_adaptive_executor_pool_size` | 限制每条查询在每个工作节点上的同时连接数 |
| `executor_slow_start_interval` | 逐步增加并行度，避免过载 |
| `max_cached_conns_per_worker` | 限制每个会话对每个工作节点缓存的空闲连接数 |
| `max_shared_pool_size` | 对工作节点连接总数设置全局安全上限 |

## 相关内容 {#related-content}

- [使用 Citus 扩展 PostgreSQL](/citus/overview/postgresql-citus-scale/)
- [多租户应用教程](/citus/tutorials/tutorial-multi-tenant/)
