---
title: dropIndexes
description: 通过名称、键模式或名称列表删除 DocumentDB 索引。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/indexing/dropIndexes.md
weight: 20
translation_source_sha256: cbd973b1d806102678bbe73cfa580b5a2cf02d635777ade2fdee6819786ed34a
translation_review: AI-assisted bilingual review; 2026-11-07
---

从集合中删除索引。

```javascript
db.flights.dropIndex("route_no_1")
```

首先使用 [`createIndexes`](/documentdb/reference/commands/indexing/createindexes/) 中的 airline 示例创建 `route_no_1`。

| 参数 | 描述 |
| --- | --- |
| **`dropIndexes`** | (必需) 指定集合名称的字符串。 |
| **`index`** | (必需) 指定索引名称、键模式或名称列表的字符串、文档或字符串数组。`"*"` 会删除符合条件的非 `_id` 索引。 |
| **`comment`** | (可选) 携带网关请求追踪的跟踪上下文字符串；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

无法删除 `_id` 索引。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

## 实现 {#implementation}

Shell 的 `dropIndex()` 辅助函数会发送 `dropIndexes`。

源码：`pg_documentdb/src/commands/drop_indexes.c`、`ParseDropIndexesArg` 和网关 `processor/process.rs`。
