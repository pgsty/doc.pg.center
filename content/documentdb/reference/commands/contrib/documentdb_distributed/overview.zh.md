---
title: documentdb_distributed
description: 为 DocumentDB 增加分布式存储、共置和再平衡功能。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/overview.md
weight: 50
translation_source_sha256: f4b1541e3ba40842d2c324e10326f041dbf5dc32cbf29f6fc502fdb946e0b19e
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

`documentdb_distributed` 是可选的 PostgreSQL 扩展，为 DocumentDB 增加分布式行为。它实现了现有 DocumentDB 命令所用的分布式钩子，并增加用于集群管理、集合放置和再平衡的 SQL API。

这些功能要求**安装并加载 `documentdb_distributed`**。**[Citus](https://github.com/citusdata/citus) 是必需依赖，它是将表分布到多个节点的 PostgreSQL 扩展**；此外还需要 `documentdb_core` 和 `documentdb`。仅有 DocumentDB 核心扩展无法提供这些分布式接口。

## 前提条件与安装 {#prerequisites-and-installation}

安装依赖项前，请审阅所选软件包和版本的许可条款，以及适用的使用、分发或部署限制。

在协调节点和工作节点上安装兼容的 Citus 和 DocumentDB 扩展包。在初始化 DocumentDB 的分布式元数据之前，先配置包含协调节点和工作节点的 Citus 集群。

**推荐使用 Citus 14。** 使用与 PostgreSQL 主版本及平台兼容的构建。不能假定任意较新的 Citus 软件包都兼容，也不能假定同一个 Citus 构建适用于不同 PostgreSQL 主版本。

为同一 PostgreSQL 主版本和平台，构建或获取同一 DocumentDB 发行版的 `documentdb_core`、`documentdb` 和 `documentdb_distributed`，并在协调节点和工作节点上使用一致的软件包组合。对于提供商管理的软件包，应使用该提供商支持的依赖组合，不要自行替换其中的版本。下方的已安装版本查询只报告实际安装的版本，并不能证明兼容性。

协调节点和工作节点都必须通过 `shared_preload_libraries` 加载 `pg_documentdb_distributed` 库，顺序位于 `citus` 和 `pg_documentdb` 之后。保留部署所需的其他库，并在修改该设置后重启 PostgreSQL。

在目标 PostgreSQL 数据库中创建 `citus`、`documentdb_core` 和 `documentdb` 后，管理员即可创建扩展：

```sql
CREATE EXTENSION IF NOT EXISTS documentdb_distributed;
```

在已配置的协调节点上初始化分布式元数据：

```sql
SELECT documentdb_api_distributed.initialize_cluster();
```

创建扩展本身不会注册 Citus 工作节点。工作节点注册和连通性配置属于 Citus 集群的设置步骤。

检查目标数据库中已安装的依赖项：

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('citus', 'documentdb_core', 'documentdb', 'documentdb_distributed')
ORDER BY extname;
```

## 命令扩展 {#command-extensions}

| API | 分布式行为 |
| --- | --- |
| `shard_collection` / `shardCollection` | 使用哈希分片键和分布式底层表[分布存储集合](/documentdb/reference/commands/contrib/documentdb_distributed/sharding/#shard-a-collection)。 |
| `reshard_collection` / `reshardCollection` | 使用不同的分片键或指定的分布方式[重新分布现有数据](/documentdb/reference/commands/contrib/documentdb_distributed/sharding/#reshard-a-collection)。 |
| `unshard_collection` / `unshardCollection` | [将集合恢复为未分片布局](/documentdb/reference/commands/contrib/documentdb_distributed/sharding/#unshard-a-collection)，同时保留分布式底层存储。 |
| `coll_mod` / `collMod` | 通过 `colocation` 扩展选项[共置集合](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/)；将受支持的索引修改传播到分布式分片索引。 |
| `move_collection` / `moveCollection` | 通过阻塞式传输或逻辑复制[将未分片集合移动](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/)到指定节点组。 |
| `balancerStart`, `balancerStatus`, `balancerStop` | [启动、检查和停止分片再平衡](/documentdb/reference/commands/contrib/documentdb_distributed/rebalancer/)，前提是提供商网关已集成相关功能，且已单独启用再平衡器。 |
| `getShardMap` | 网关集成分布式实现后，可[发现节点组和各节点的元数据](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#getshardmap)。 |
| `listShards` | 网关集成分布式实现后，可[列出节点组及其活跃成员](/documentdb/reference/commands/contrib/documentdb_distributed/listshards/)。 |
| `listCollections` | 请求 `addDistributedMetadata` 时，[增加分片数量和共置元数据](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#listcollections)。 |

上面的蛇形命名是 PostgreSQL SQL API。驼峰命名表示对应的线协议命令（若提供）。现有 shell 辅助函数仍在[分片参考](/documentdb/reference/commands/sharding/sharding-commands/)中说明。

安装 PostgreSQL 扩展不会改变网关转发的命令或字段。例如，默认网关的旧版分片适配器不转发 `numInitialChunks`；SQL 命令文档 API 可直接传入此选项。再平衡器的线协议命令依赖提供商网关将其接入分布式实现。

<span id="cluster-lifecycle-ap-is"></span>

## 集群生命周期 API {#cluster-lifecycle-apis}

扩展还导出用于部署管理的 SQL 生命周期 API：

| API | 用途 |
| --- | --- |
| `documentdb_api_distributed.initialize_cluster()` | 如上所示，为已配置的集群初始化分布式元数据。已经初始化的集群保持不变。 |
| `documentdb_api_distributed.complete_upgrade()` | 执行已安装扩展版本所需的分布式设置操作。返回布尔值，表示是否执行了升级工作。它是部署的扩展升级流程的一部分，不能替代扩展包的安装或升级。 |

工作节点索引更新、版本缓存和系统目录修复辅助函数服务于实现内部及其维护流程，并非额外的应用线协议命令。

## 实现 {#implementation}

[分布式扩展源码树](https://github.com/documentdb/documentdb/tree/main/internal/pg_documentdb_distributed)链接到当前 `main`。其中的 `documentdb_distributed.control` 文件声明了 Citus 和 DocumentDB 依赖项，`src/documentdb_distributed.c` 在 PostgreSQL 启动期间注册分布式钩子。本节核查命令行为所用的源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：`internal/pg_documentdb_distributed/src/distribution/distributed_hooks.c`、`InitializeDocumentDBDistributedHooks`；`src/colocation/shard_colocation.c`、`UpdateColocationHooks`；生命周期 API：`src/distribution/cluster_operations.c`、`command_initialize_cluster` 和 `command_complete_upgrade`。
