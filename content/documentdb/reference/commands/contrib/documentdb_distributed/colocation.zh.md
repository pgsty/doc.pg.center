---
title: 通过分布式 collMod 共置集合
description: 使用 documentdb_distributed 提供的 collMod 扩展共置 DocumentDB 集合。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/colocation.md
weight: 10
translation_source_sha256: a6013aa0f52eb42d0aee233ffb1e82be802bd445ea76146a2ffa3372a70562fe
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

[安装并加载 documentdb_distributed 及其依赖项](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation)后，`collMod.colocation` 可更改未分片集合的共置方式。共置的集合属于同一个共置组，因此可以统一管理其放置位置。

这是现有 [`collMod`](/documentdb/reference/commands/administration/collmod/) 命令的扩展，不替代其索引、验证或统计信息选项。

## 共置两个集合 {#colocate-two-collections}

示例使用[航空数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)。`tickets` 和 `flights` 都必须存在于 `bookings` 中，且均未分片；请独立于分片示例运行：

```javascript
db.runCommand({
  collMod: "tickets",
  colocation: { collection: "flights" }
})
```

源集合是 `tickets`，目标名称在同一逻辑数据库中解析。目标必须是另一个未分片集合，底层仅有一个分片，且共置布局兼容。

| 参数 | 说明 |
| --- | --- |
| **`collMod`** | （必需）源集合名称。 |
| **`colocation`** | （此操作必需）指定共置变更的文档。 |
| **`colocation.collection`** | （必需）同一数据库中非空的目标集合名称，或 `null`，表示将源集合从当前共置组中分离。 |
{.fields}

共置可能涉及底层表的重新分布，不会合并集合或改变其文档结构。

## 分离集合 {#detach-a-collection}

要使 tickets 不再与目标集合共置：

```javascript
db.runCommand({
  collMod: "tickets",
  colocation: { collection: null }
})
```

`null` 形式也可将已分片集合从当前组中分离。已分片集合不能通过指定目标集合名称的形式加入另一个集合的共置组。

没有分布式钩子时，默认单节点实现不会应用共置变更。

## 分布式集合与放置元数据 {#distributed-collection-and-placement-metadata}

扩展除了提供共置操作，还提供元数据查询钩子。使用 `listCollections` 检查集合的共置组和分片数量，使用 `config.chunks` 查看底层分片的放置位置，使用分片元数据查询查看节点组。这些是元数据投影，不是可直接更新的应用集合。

<span id="list-collections"></span>

### listCollections {#listcollections}

设置 `addDistributedMetadata: true`，在每个返回的集合文档中包含分布式元数据。以下请求使用此扩展专用选项，将[航空数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)过滤为上面用到的两个集合：

```javascript
db.runCommand({
  listCollections: 1,
  filter: { name: { $in: ["flights", "tickets"] } },
  addDistributedMetadata: true,
  cursor: { batchSize: 20 }
})
```

命令返回通常的 `listCollections` 游标。以下新增字段位于每个集合文档的顶层，不在 `info` 内：

| 字段 | 说明 |
| --- | --- |
| **`colocationId`** | 集合底层表所属共置组的数字标识符。同组集合的值相同。它不是节点组名称，也不是物理分片标识符。 |
| **`shardCount`** | 为该共置组记录的底层分片数量。未分片集合也可能有一个底层分片；这不是工作节点数量或文档数量。 |
{.fields}

将 `tickets` 与 `flights` 共置后，相关字段可能如下所示。组标识符仅供示例：

```json
[
  { "name": "flights", "type": "collection", "colocationId": 42, "shardCount": 1 },
  { "name": "tickets", "type": "collection", "colocationId": 42, "shardCount": 1 }
]
```

此选项默认为 `false`。启用后，分布式查询将集合与底层表及共置元数据连接，因此不包含没有底层表的视图。`nameOnly: true` 可与此选项组合使用：分布式字段仍与 `name` 和 `type` 一起保留。没有分布式钩子时，不会添加分布式元数据。其他选项见 [`listCollections`](/documentdb/reference/commands/administration/listcollections/)。

<span id="config-chunks"></span>

### config.chunks {#configchunks}

分布式钩子将基础块元数据替换为底层分片及其放置信息：

```javascript
db.getSiblingDB("config").chunks.find({ ns: "bookings.flights" }).toArray()
```

| 字段 | 说明 |
| --- | --- |
| **`_id`** | 数字形式的物理分片标识符。 |
| **`ns`** | 逻辑集合命名空间，例如 `bookings.flights`。 |
| **`shard`** | 放置位置所在节点组的名称，格式为 `shard_<groupid>`。它标识一个组，不是 `_id` 中的物理分片。 |
| **`chunkSize`** | 底层存储报告的分片字节大小，不是文档数量。 |
| **`min`**, **`max`** | 分布式查询投影出的分片边界元数据，不是原始 BSON 分片键值的范围。 |
{.fields}

查询将集合底层表与分片、大小和放置元数据连接，排除视图。使用分布式底层存储的未分片集合也可能出现。每个匹配的放置位置对应一行，因此分片有多个放置位置时，不能将行数理解为不同分片的数量。

使用 `ns` 将这些行关联到集合，使用 `shard` 将放置位置关联到下文描述的节点组。共置集合仍保留不同的底层分片和 `_id` 值；共用一个 `colocationId` 不会合并其块记录。

<span id="config-shards"></span>

### config.shards {#configshards}

扩展的配置分片钩子暴露与 [`listShards`](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#listshards) 相同的节点组条目，替代基础单节点占位信息。在核查的源码修订中，后端通过 **`config._shards`** 而非 `config.shards` 提供这些元数据；不要假定安装扩展会创建 `config.shards` 别名。

```javascript
db.getSiblingDB("config").getCollection("_shards").find({}).toArray()
```

| 字段 | 说明 |
| --- | --- |
| **`_id`** | 节点组名称，格式为 `shard_<groupid>`，与 `config.chunks.shard` 对应。 |
| **`nodes`** | 包含节点组名称、`/` 和逗号分隔的活跃成员节点名称的字符串，例如 `shard_1/node_default_2`。它不是放在 `host` 字段中的连接字符串。 |
{.fields}

节点组列表由集群元数据中标记为 `shouldhaveshards` 的节点构建，活跃成员列于 `nodes` 中。各节点的角色、活跃状态和集群信息，见 [`getShardMap`](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#getshardmap)。

<span id="config-collections"></span>

### config.collections {#configcollections}

`config.collections` 描述配置了分片键的逻辑集合：

```javascript
db.getSiblingDB("config").collections.find({ _id: "bookings.flights" }).toArray()
```

| 字段 | 说明 |
| --- | --- |
| **`_id`** | 逻辑集合命名空间，例如 `bookings.flights`，与 `config.chunks.ns` 对应。 |
| **`key`** | 集合配置的 BSON 分片键文档。 |
| **`noBalance`** | 此元数据投影始终输出 `true`。它不是分布式再平衡器的当前状态。 |
{.fields}

在核查的源码修订中，扩展未在此处增加单独的 `config.collections` 重写或分布式专用字段。尤其是，此查询不包含 `colocationId` 或 `shardCount`；应通过 `listCollections.addDistributedMetadata` 请求这些字段。共置示例中的两个未分片集合，不会仅因为扩展管理其存储就出现在 `config.collections` 中。请使用[再平衡器 API](/documentdb/reference/commands/contrib/documentdb_distributed/rebalancer/) 检查实际的再平衡活动。

## 分布式索引修改 {#distributed-index-modifications}

扩展还提供受支持的 `collMod` 索引操作所用的分片索引更新钩子。例如，[索引可见性变更](/documentdb/reference/commands/administration/collmod/#hide-and-unhide-an-index)会更新底层分片索引，而不只是协调节点上的索引元数据。`collMod` 主参考文档中的限制仍然适用。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：[分布式共置](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/colocation/shard_colocation.c)、`HandleDistributedColocation`；分片索引：`internal/pg_documentdb_distributed/src/distribution/distributed_index_operations.c`、`UpdateDistributedPostgresIndex`。

元数据：分布式共置源码中的 `UpdateColocationHooks`、`RewriteListCollectionsQueryForDistribution`、`RewriteConfigChunksQueryForDistribution` 和 `RewriteConfigShardsQueryForDistribution`；基础配置查询：`pg_documentdb/src/aggregation/bson_aggregation_config_queries.c`、`GenerateConfigDatabaseQuery`、`GenerateCollectionsQuery`；列表投影：`pg_documentdb/src/aggregation/bson_aggregation_metadata_queries.c`、`BuildListCollectionsProjection`。
