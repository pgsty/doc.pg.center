---
title: moveCollection
description: 使用 documentdb_distributed 将未分片的 DocumentDB 集合移动到另一个节点组。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/moveCollection.md
weight: 70
translation_source_sha256: 85a291be56fcc15c9df716596bccaf91b666ff64d7d849225e61307175c0e158
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

将已有的未分片集合移动到指定节点组。需要 [documentdb_distributed 及其依赖项](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation)，以及部署提供的集合移动功能。

`moveCollection` 线协议 API 是否可用，取决于提供商网关。

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`moveCollection`** | （必需）字符串，指定已有未分片集合的完全限定命名空间。 |
| **`toShard`** | （必需）`shard_<groupid>` 形式的字符串。集群元数据中，该组必须有活跃主节点。这是节点组标识符，不是集合的物理分片 ID。 |
| **`useLogicalReplication`** | （可选）类布尔值；为 `true` 时，强制通过分片间逻辑复制进行传输，复制数据期间不阻塞写入。默认为 `false`，传输期间会阻塞写入。需要为部署配置逻辑分片传输。 |
{.fields}

## 选择目标 {#choose-a-destination}

通过已集成分布式实现的网关调用 [`listShards`](/documentdb/reference/commands/contrib/documentdb_distributed/listshards/)：

```javascript
db.adminCommand({ listShards: 1 })
```

使用条目的 `_id` 作为 `toShard`；例如，`_id: "shard_1"` 对应 `toShard: "shard_1"`。通过 [`getShardMap`](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#getshardmap) 确认该组有活跃主节点成员，并选择一个不同于 [`config.chunks`](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#configchunks) 中集合当前放置位置的目标。不要假定示例节点组在所有部署中都存在。

## 使用默认传输模式移动 {#move-with-the-default-transfer-mode}

使用[航空数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)，假定 `bookings.flights` 未分片，且组 1 是符合条件的目标：

```javascript
db.adminCommand({
  moveCollection: "bookings.flights",
  toShard: "shard_1"
})
```

默认情况下，底层分片移动期间会阻塞写入。请在显式事务之外运行命令。放置位置移动完成后，命令返回 `{ ok: 1 }`；它不会将后台再平衡任务加入队列。

## 使用逻辑复制 {#use-logical-replication}

在已配置逻辑分片传输的部署中，以下是前述移动操作的另一种方式，从相同的源放置位置开始：

```javascript
db.adminCommand({
  moveCollection: "bookings.flights",
  toShard: "shard_1",
  useLogicalReplication: true
})
```

这会选择 `force_logical` 而非 `block_writes`。它不会改变目标，也不会让已分片集合符合移动条件，且不保证操作永不阻塞。

## 共置与分布 {#colocation-and-distribution}

移动操作在传输底层分片之前，会将集合从原共置组中分离。不能假定此前与它共置的另一个集合也会随之移动。

`moveCollection` 不改变文档结构或逻辑分片键。源集合必须已经处于未分片状态。使用[取消分片](/documentdb/reference/commands/contrib/documentdb_distributed/sharding/#unshard-a-collection)移除分片键，使用[重新分片](/documentdb/reference/commands/contrib/documentdb_distributed/sharding/#reshard-a-collection)更改分片键，使用[再平衡器](/documentdb/reference/commands/contrib/documentdb_distributed/rebalancer/)平衡集群各处的分片放置。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

`moveCollection` 线协议 API 映射到 SQL UDF `documentdb_api_distributed.move_collection`。其 [SQL 入口](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/sql/udfs/operations/move_collection--latest.sql)调用 `internal/pg_documentdb_distributed/src/colocation/shard_colocation.c` 中的 `documentdb_command_move_collection`。实现会验证命名空间和目标、解除共置、移动底层分片的放置位置，并使缓存的放置信息失效。
