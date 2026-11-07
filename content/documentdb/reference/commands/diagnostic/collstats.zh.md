---
title: collStats
description: 在 DocumentDB 中返回集合统计信息，并支持配置大小缩放。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/collStats.md
weight: 10
translation_source_sha256: 650d9eb2955d884ac2d842323ff022804abbfb29b7a88f12dc16c90ab09cf678
translation_review: AI-assisted bilingual review; 2026-11-07
---

返回集合的统计信息，包括文档数量、文档大小、存储大小以及索引大小。

```javascript
db.flights.stats({ scale: 1024 })
```

shell 的 `stats()` 辅助函数通过聚合获取集合统计信息。以下字段描述了直接的 `collStats` 线协议请求。

| 参数 | 描述 |
| --- | --- |
| **`collStats`** | (必需) 指定集合名称的字符串。 |
| **`scale`** | (可选) 指定适用的字节大小字段的缩放除数；默认值为 `1`。接受数值型 BSON 类型，后端会将该值截断为整数。 |
{.fields}

`null` 或 undefined `scale` 使用 `1`；无效类型或无效缩放值会导致失败。聚合 [`$collStats`](/documentdb/reference/operators/aggregation/collstats/) 阶段的选项，例如 `latencyStats` 或 `queryExecStats`，不会通过此线协议适配器转发。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：网关 `processor/data_management.rs`、`process_coll_stats` 和后端 `pg_documentdb/src/commands/coll_stats.c`。
