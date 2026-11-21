---
title: listShards
description: 使用 documentdb_distributed 列出 DocumentDB 分布式节点组及其活跃成员。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/listShards.md
weight: 60
translation_source_sha256: fb80977bd9a34588ae27007d4899c5011f3683fd568f3a55ece86179e896c4fb
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

使用 [documentdb_distributed 扩展](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation)列出节点组及其活跃成员节点名称。这些是用于数据放置的节点组，不是各个集合底层的物理分片。

通过已集成分布式实现的网关，在 `admin` 数据库上运行命令：

```javascript
db.adminCommand({ listShards: 1 })
```

| 参数 | 说明 |
| --- | --- |
| **`listShards`** | （必需）命令标记，通常为 `1`。分布式实现没有此命令特有的选项。 |
{.fields}

## 响应 {#response}

例如，某个部署包含一个符合条件的节点组，且该组有一个活跃主节点成员，可能返回：

```json
{
  "ok": 1,
  "shards": [
    { "_id": "shard_1", "nodes": "shard_1/node_default_2" }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| **`ok`** | 成功时为 `1`。 |
| **`shards`** | 符合条件的节点组数组。不存在符合条件的节点组时，实现可能省略此字段，只返回 `{ ok: 1 }`。 |
| **`shards._id`** | `shard_<groupid>` 形式的节点组名称。`moveCollection.toShard` 应使用此值，而非物理分片标识符。 |
| **`shards.nodes`** | 节点组名称、`/` 和以逗号分隔的活跃成员节点名称。这些名称是元数据标识符，不是主机连接字符串。 |
{.fields}

实现从集群元数据中选择标记为 `shouldhaveshards` 的节点，并在 `nodes` 中列出活跃成员，但不包含其角色。[移动集合](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/#choose-a-destination)之前，应使用 [`getShardMap`](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#getshardmap) 确认选定节点组中有活跃主节点成员。上面的示例标识符不保证在你的部署中存在。

## 可用性 {#availability}

是否可用取决于提供商的网关实现。

相关的配置分片元数据查询和集合放置字段，见[分布式集合与放置元数据](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#distributed-collection-and-placement-metadata)。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：[分布式节点与共置代码](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/colocation/shard_colocation.c)、`command_list_shards`、`GetShardMapNodes` 和 `WriteShardList`；默认网关：`pg_documentdb_gw/documentdb_gateway_core/src/postgres/documentdb_data_client.rs`、`execute_list_shards`。
