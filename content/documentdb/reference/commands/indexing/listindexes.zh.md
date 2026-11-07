---
title: listIndexes
description: 使用 DocumentDB 命令游标列出索引规范。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/indexing/listIndexes.md
weight: 30
translation_source_sha256: c3b625b2099a0c5b368ca1f4ed047022a9287cd9d59bcd34b45132cc3953b8c6
translation_review: AI-assisted bilingual review; 2026-11-07
---

在游标中返回集合的索引规范。

```javascript
db.flights.getIndexes()
```

该辅助函数返回索引规范数组，并处理命令游标。

| 参数 | 描述 |
| --- | --- |
| **`listIndexes`** | (必需) 指定集合名称的字符串。 |
| **`cursor`** | (可选) 支持数值型 `batchSize` 的文档，转换为非负整数，用于指定第一个批次；也支持布尔型 `singleBatch`，用于在该批次后关闭游标。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`cursor.batchSize`** | (可选) 指定首批次限制的数字，转换为非负整数。 |
| **`cursor.singleBatch`** | (可选) 布尔值，当 `true` 为真时，在首批次后关闭游标。 |
{.fields}

默认线协议命令不提供 `includeBuildUUIDs` 或 `includeIndexBuildInfo`。有关共享元数据，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

后端解析器也接受 `listindexes` 的拼写形式，但网关名称解析器不会将其作为线协议命令别名暴露。

源码：`pg_documentdb/src/aggregation/bson_aggregation_metadata_queries.c`、`GenerateListIndexesQuery`。
