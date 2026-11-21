---
title: 分布式分片与放置
description: 通过 documentdb_distributed 对 DocumentDB 集合进行分片、重新分片、取消分片和移动。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/sharding.md
weight: 40
translation_source_sha256: bdb7e9b665cef93514c8e87a78d42a0c193c72574f8388f723e7b9182302ace6
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

这些操作需要 [documentdb_distributed 及其依赖项](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation)。shell 示例使用[航空数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)。

这些线协议 API 及其选项是否可用，取决于提供商网关的集成情况。

## 对集合分片 {#shard-a-collection}

按航线编号的哈希值分布存储 `bookings.flights`，请求创建四个初始块：

```javascript
sh.shardCollection("bookings.flights", { route_no: "hashed" }, { numInitialChunks: 4 })
```

扩展会对底层表进行分布存储。对已有集合分片会重新分布其数据并重新创建索引，并非只更新元数据。

| 参数 | 说明 |
| --- | --- |
| **`shardCollection`** | （必需）`database.collection` 形式的完全限定命名空间。 |
| **`key`** | （必需）受支持的哈希分片键文档。 |
| **`numInitialChunks`** | （可选）正整数，指定所请求的初始块数量，不得超过配置的分片限制。分布式钩子在分布存储底层表时使用该数量。 |
{.fields}

提供商网关必须转发 `numInitialChunks`，才能遵循所请求的数量。公共命令选项见[分片命令](/documentdb/reference/commands/sharding/sharding-commands/#shardcollection-and-reshardcollection)。

## 对集合重新分片 {#reshard-a-collection}

执行前面的示例后，按出发机场重新分布航班数据：

```javascript
sh.reshardCollection("bookings.flights", { departure_airport: "hashed" }, { numInitialChunks: 4 })
```

这会使用新键重建集合的数据分布，可能移动数据并重新创建索引，因此需要为重写现有集合的工作预留资源和时间。

| 参数 | 说明 |
| --- | --- |
| **`reshardCollection`** | （必需）完全限定命名空间。 |
| **`key`** | （必需）新的、受支持的哈希分片键文档。 |
| **`numInitialChunks`** | （可选）正整数，指定所请求的块数量，受配置的上限约束。 |
| **`forceRedistribution`** | （可选）类布尔值，即使分片键与现有键相同，也强制重新分布。未指定时，键相同可能导致操作被跳过。 |
{.fields}

## 取消集合分片 {#unshard-a-collection}

将航班集合恢复为未分片布局：

```javascript
db.adminCommand({ unshardCollection: "bookings.flights" })
```

| 参数 | 说明 |
| --- | --- |
| **`unshardCollection`** | （必需）完全限定命名空间。 |
{.fields}

取消分片会移除集合的逻辑分片键，并将其数据重新分布为未分片布局，不会卸载分布式扩展。此 API 不选择目标节点；需要改变放置位置时，应另行使用 `moveCollection`。`sh.unshardCollection()` 辅助函数要求提供 `toShard` 参数，因此示例通过 `db.adminCommand` 只发送命名空间。

## 移动未分片集合 {#move-an-unsharded-collection}

取消分片后，使用 [`moveCollection`](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/) 将集合移动到指定节点组。其参考文档说明了目标发现、`useLogicalReplication`、事务限制及对共置的影响。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

`shardCollection`、`reshardCollection` 和 `unshardCollection` 线协议 API 分别映射到 SQL UDF `documentdb_api.shard_collection`、`documentdb_api.reshard_collection` 和 `documentdb_api.unshard_collection`。接受命令文档的重载版本接收 BSON 参数文档。

SQL [分片入口](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb/sql/udfs/schema_mgmt/shard_collection--latest.sql)调用核心分片实现。`internal/pg_documentdb_distributed/src/distribution/distributed_hooks.c` 中的 `DistributePostgresTableCore` 通过 `create_distributed_table` 对底层表进行分布存储。

源码：`pg_documentdb/src/sharding/sharding.c`、`ParseShardCollectionRequest`、`ParseReshardCollectionRequest` 和 `ParseUnshardCollectionRequest`；放置：`internal/pg_documentdb_distributed/src/colocation/shard_colocation.c`、`documentdb_command_move_collection`。
