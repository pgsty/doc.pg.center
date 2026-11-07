---
title: listCollections
description: 在 DocumentDB 中列出集合和视图的元数据，支持过滤和游标选项。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/listCollections.md
weight: 40
translation_source_sha256: de39e235ea03013ff3f11de9019bcf20496f5b368dbef278fd0631170042e402
translation_review: AI-assisted bilingual review; 2026-11-07
---

通过游标返回集合和视图的元数据。

```javascript
db.getCollectionInfos({ name: "flights" }, { batchSize: 20 })
```

该辅助函数返回元数据文档数组，并处理命令游标。

| 参数 | 描述 |
| --- | --- |
| **`listCollections`** | (必需) 命令标记符，通常为 `1`。 |
| **`filter`** | (可选) 用于过滤返回的元数据文档的文档；`null` 表示无过滤。 |
| **`cursor`** | (可选) 用于支持数值型 `batchSize` 的文档，转换为非负整数，用于第一批次；也支持布尔型 `singleBatch` 以在该批次后关闭游标。 |
| **`nameOnly`** | (可选) 类布尔值，仅返回集合名称和类型而非完整元数据；默认为 `false`。 |
| **`addDistributedMetadata`** | (可选) 类布尔值，作为 DocumentDB 扩展提供分布式集合元数据。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`cursor.batchSize`** | (可选) 指定第一批次限制的数字，转换为非负整数。 |
| **`cursor.singleBatch`** | (可选) 布尔值，当 `true` 时在第一批次后关闭游标。 |
{.fields}

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 以获取共享元数据。

源码： `pg_documentdb/src/aggregation/bson_aggregation_metadata_queries.c`, `GenerateListCollectionsQuery`。
