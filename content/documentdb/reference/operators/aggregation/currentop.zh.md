---
title: $currentOp
description: $currentOp 阶段返回数据库当前活动和排队操作的信息。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$currentop.md
weight: 70
translation_source_sha256: 290c4092f7de5af7dd8757dc81d3b338e68dac51188d3abc7d61b1d99ad2198d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$currentOp` 流水线阶段返回包含数据库实例上当前活动和排队操作信息的文档流。此阶段必须是聚合流水线中的第一个阶段，并在 `admin` 数据库上运行。

## 语法 {#syntax}

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    {
      $currentOp: {
        allUsers: <boolean>,
        idleConnections: <boolean>,
        idleCursors: <boolean>,
        idleSessions: <boolean>,
        localOps: <boolean>
      }
    }
  ],
  cursor: {}
})
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`allUsers`** | 可选。布尔值。若为 `true`，则报告所有用户的操作。默认值：`false`。 |
| **`idleConnections`** | 可选。布尔值。若为 `true`，则报告空闲连接。默认值：`false`。 |
| **`idleCursors`** | 可选。布尔值。若为 `true`，则报告空闲游标。默认值：`false`。 |
| **`idleSessions`** | 可选。布尔值。若为 `true`，则报告空闲会话。默认值：`false`。 |
| **`localOps`** | 可选。布尔值。若为 `true`，则报告在当前实例上本地运行的操作。默认值：`false`。 |
{.fields}

## 示例 {#examples}

### 示例 1：列出活动操作 {#example-1-list-active-operations}

返回所有当前活动的操作：

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    { $currentOp: { allUsers: true } }
  ],
  cursor: {}
})
```

### 示例 2：过滤活动操作 {#example-2-filter-active-operations}

返回特定数据库的活动操作，结合使用 `$match`：

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    { $currentOp: { allUsers: true } },
    { $match: { "ns": /^mydb\./ } }
  ],
  cursor: {}
})
```

## 关键要点 {#key-takeaways}

- **必须为首个阶段** — `$currentOp` 必须是聚合流水线中的第一个阶段
- **仅限管理员数据库** — 此阶段必须在 `admin` 数据库上使用 `db.adminCommand()` 执行
- **与集合无关** — 不针对特定集合操作
