---
title: killCursors
description: 通过其 BSON 64 位标识符关闭 DocumentDB 游标。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/killCursors.md
weight: 60
translation_source_sha256: ce422cfec1e85f7d0abd54667d3b7af7b53824ddb4fd7d2c4abda8b84b14e4ae
translation_review: AI-assisted bilingual review; 2026-11-07
---

关闭指定的游标并释放其资源。

```javascript
const flightCursor = db.flights.find().batchSize(1)
flightCursor.next()
flightCursor.close()
```

[航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)包含多架航班。`next()` 执行查询并消耗一个结果；`close()` 关闭剩余的服务器游标。Shell 管理游标 ID 和会话元数据。

| 参数 | 描述 |
| --- | --- |
| **`killCursors`** | (必需) 指定集合名称的字符串。 |
| **`cursors`** | (必需) 指定要关闭的游标 ID 的 BSON int64 值数组。请使用服务器返回的 ID，而非 JavaScript 数字。 |
{.fields}

响应将 `cursorsKilled`、`cursorsNotFound`、`cursorsAlive` 和 `cursorsUnknown` 中的 ID 进行分类。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：网关 `processor/cursor.rs`，`process_kill_cursors`。
