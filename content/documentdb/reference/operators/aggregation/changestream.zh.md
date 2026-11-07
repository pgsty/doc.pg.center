---
title: $changeStream
description: $changeStream 阶段在 MongoDB 中打开变更流游标。DocumentDB 不支持该操作。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$changestream.md
weight: 40
translation_source_sha256: df8e1c95af5a7ec1d247829bb8e7196bcb483e554c4a8f6dc3e00c2e74f1a606
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!IMPORTANT]
> DocumentDB 不支持 `$changeStream`。任何使用该操作符的聚合流水线，包括 `db.collection.watch()`，都会因 `Stage $changeStream is not supported yet in native pipeline`（`CommandNotSupported`，错误码 115）而失败。

在 MongoDB 中，`$changeStream` 聚合流水线阶段会打开一个游标，实时报告插入、更新、删除及其他变更。以下语法仅作参考。

## 语法 {#syntax}

```javascript
{
  $changeStream: {
    allChangesForCluster: <boolean>,
    fullDocument: <string>,
    fullDocumentBeforeChange: <string>,
    resumeAfter: <ResumeToken>,
    startAfter: <ResumeToken>,
    startAtOperationTime: <Timestamp>,
    showExpandedEvents: <boolean>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`allChangesForCluster`** | 可选。布尔值。若为 true，则返回整个集群的变更。默认值为 false。 |
| **`fullDocument`** | 可选。字符串。确定更新操作的返回内容。选项：'default'、'updateLookup'、'whenAvailable'、'required'。 |
| **`fullDocumentBeforeChange`** | 可选。字符串。返回文档的前像。选项："off"、"whenAvailable"、"required"。 |
| **`resumeAfter`** | 可选。用于在特定事件后恢复变更流的恢复令牌。 |
| **`startAfter`** | 可选。用于在特定事件后启动变更流的恢复令牌。 |
| **`startAtOperationTime`** | 可选。指定变更流开始的时间戳。 |
| **`showExpandedEvents`** | 可选。布尔值。是否包含其他变更流事件。默认值为 false。 |
{.fields}

## 示例 {#example}

此流水线将被拒绝：

```javascript
db.stores.aggregate([
  {
    $changeStream: {
      fullDocument: "updateLookup"
    }
  }
])
```

```
Stage $changeStream is not supported yet in native pipeline
```
