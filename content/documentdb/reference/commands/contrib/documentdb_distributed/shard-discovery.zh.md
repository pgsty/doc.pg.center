---
title: 分布式分片发现
description: 介绍 documentdb_distributed 实现的 getShardMap 和 listShards 响应。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/shard-discovery.md
weight: 30
translation_source_sha256: 54827ab3392927c8476da36e7d410fb2655b7e1578797ef8019b4aef0a775ab8
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

[documentdb_distributed 扩展](/documentdb/reference/commands/contrib/documentdb_distributed/overview/)基于集群节点元数据实现 `getShardMap` 和 `listShards` 响应。这些响应描述节点组及其成员，不描述每个文档或集合的数据分布。

这些线协议 API 是否可用，取决于提供商网关的集成情况。

<span id="get-shard-map"></span>

## getShardMap {#getshardmap}

```javascript
db.adminCommand({ getShardMap: 1 })
```

命令实现不解析此命令特有的参数。它返回 `ok`；存在符合条件的节点组时，还返回以下字段：

| 字段 | 说明 |
| --- | --- |
| **`map`** | 一个文档，将 `shard_<groupid>` 名称映射为包含节点组名称及其活跃成员节点名称的字符串。 |
| **`hosts`** | 一个文档，将每个活跃成员节点名称映射到其分片组名称。 |
| **`nodes`** | 以成员节点名称为键的文档，包含各节点的 `role`、`active` 和 `cluster` 值。非活跃成员可能出现在此处，尽管它们不在活跃主机映射中。 |
{.fields}

例如，某个部署包含一个符合条件的节点组，且该组有一个活跃主节点成员，可能返回：

```json
{
  "ok": 1,
  "map": { "shard_1": "shard_1/node_default_2" },
  "hosts": { "node_default_2": "shard_1" },
  "nodes": {
    "node_default_2": { "role": "primary", "active": true, "cluster": "default" }
  }
}
```

这些标识符仅供示例，并不要求节点采用这些名称。`shard_1` 这样的节点组名称可指定 [`moveCollection`](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/) 的目标，但使用前需确认该组中有活跃主节点。

<span id="list-shards"></span>

## listShards {#listshards}

命令语法、响应字段、结果示例和网关可用性见专门的 [`listShards` 命令参考](/documentdb/reference/commands/contrib/documentdb_distributed/listshards/)。其节点组标识符可用于选择 `moveCollection` 的目标。

两种实现都会从集群元数据中选择标记为 `shouldhaveshards` 的节点。如果没有符合条件的节点，实现可能只返回 `{ ok: 1 }`，不包含映射字段或数组。

## 其他分布式元数据 {#other-distributed-metadata}

扩展的查询钩子还会增加分布式集合元数据。带有 `addDistributedMetadata` 的 `listCollections` 响应包含 `shardCount` 和 `colocationId`。配置分片和配置块的查询钩子暴露分布式布局中的节点组和放置信息。

这些钩子不会为每个元数据字段新增线协议命令。字段、命名空间可用性及 `config.collections` 的行为，见[分布式集合与放置元数据](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#distributed-collection-and-placement-metadata)；现有命令选项见[集合元数据参考](/documentdb/reference/commands/administration/listcollections/)。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

扩展提供 `command_get_shard_map` 和 `command_list_shards`。其 SQL 安装脚本不会创建独立的 `get_shard_map` 或 `list_shards` 函数；提供商网关必须集成这些分布式实现。

源码：[分布式节点与共置代码](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/colocation/shard_colocation.c)、`command_get_shard_map`、`command_list_shards`、`GetShardMapNodes`、`WriteShardMap`、`WriteShardList` 和 `UpdateColocationHooks`。
