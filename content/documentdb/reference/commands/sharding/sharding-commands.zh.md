---
title: 分片命令
description: DocumentDB 中支持的 shardCollection、reshardCollection、unshardCollection 和 getShardMap 线协议字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/sharding/sharding-commands.md
weight: 10
translation_source_sha256: aad8282d16437a97805556f494a6beb04a4288a08fdc7dbf108aee7fb5f8105f
translation_review: AI-assisted bilingual review; 2026-11-07
---

分片行为和选项支持取决于已安装的实现。

<span id="shard-collection-and-reshard-collection"></span>

## shardCollection 和 reshardCollection {#shardcollection-and-reshardcollection}

```javascript
sh.shardCollection("bookings.flights", { route_no: "hashed" })
sh.reshardCollection("bookings.flights", { departure_airport: "hashed" })
```

| 参数 | 描述 |
| --- | --- |
| **`shardCollection`** | (必需) 指定完全限定命名空间的字符串，`database.collection`。 |
| **`reshardCollection`** | (必需) 指定完全限定命名空间的字符串，`database.collection`。 |
| **`key`** | (必需) 指定分片键规范的文档；后端会验证支持的哈希分片键形式。 |
| **`numInitialChunks`** | (可选，依赖于实现) 请求初始数据块数量的正整数。支持情况及最大允许数量取决于部署的分片实现。 |
{.fields}

在支持 `numInitialChunks` 的实现上，任一 shell 辅助函数均可传递该选项：

```javascript
sh.shardCollection("bookings.flights", { route_no: "hashed" }, { numInitialChunks: 4 })
sh.reshardCollection("bookings.flights", { departure_airport: "hashed" }, { numInitialChunks: 4 })
```

`numInitialChunks` 的支持取决于已安装的分片实现，与提交请求的客户端辅助函数无关。

<span id="unshard-collection"></span>

## unshardCollection {#unshardcollection}

```javascript
db.adminCommand({ unshardCollection: "bookings.flights" })
```

使用原始请求仅发送命名空间。shell 的 `sh.unshardCollection()` 辅助函数需要额外的 `toShard` 参数。

| 参数 | 描述 |
| --- | --- |
| **`unshardCollection`** | (必需) 指定完全限定命名空间的字符串。 |
{.fields}

<span id="get-shard-map"></span>

## getShardMap {#getshardmap}

```javascript
db.adminCommand({ getShardMap: 1 })
```

返回由部署提供的分片元数据。默认线协议适配器不会向其后端查询传递任何命令特定选项。

## 其他分片命令 {#other-sharding-commands}

`enableSharding` 是一个无操作，返回成功；它不会改变数据库状态。

`balancerStart`、`balancerStatus`、`balancerStop`、`listShards` 和 `moveCollection` 可由某些提供方实现。

请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 以获取完整的分发支持清单。

## 实现 {#implementation}

后端命令文档入口点会解析 `numInitialChunks` 以同时处理 `shardCollection` 和 `reshardCollection`，并在创建分布式集合时应用。该数值必须为正数，且不超过配置的分片限制。

默认开源网关适配器使用遗留后端调用，仅传递命名空间、`key` 和请求是否为重新分片的标志。它不会转发 `numInitialChunks`；部署必须使用能够转发完整命令文档的实现，以确保此选项生效。该适配器也不转发 `unique`、`presplitHashedZones`、`collation`、`forceRedistribution` 或 `shardDistribution`。

源码：网关 `processor/data_description.rs`、`postgres/documentdb_data_client.rs`，以及后端 `pg_documentdb/src/sharding/sharding.c`，包括 `ParseShardCollectionRequest`、`ParseReshardCollectionRequest` 和 `ParseUnshardCollectionRequest`。
