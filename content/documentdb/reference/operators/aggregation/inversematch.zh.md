---
title: $inverseMatch
description: $inverseMatch 流水线阶段在聚合流水线中保留那些其存储查询与所提供文档匹配的文档，从而反转了通常的匹配方向。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$inversematch.md
weight: 160
translation_source_sha256: 3ebbf3b4561179bd53b8e1a45c039b89885d9f1f28fd206baa4772198877a623
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$inverseMatch` 流水线阶段反转了通常的匹配方向。当 `$match` 持有一个查询并将其与多个文档进行匹配时，`$inverseMatch` 则从每个文档中读取一个查询，并将其与一个提供的输入进行测试。当文档所携带的查询与该输入匹配时，该文档将通过此阶段。

这使得该阶段适用于存储查询的集合——保存的搜索、告警规则、订阅过滤器、路由策略等场景，其核心问题不再是“哪些文档匹配此查询”，而是“哪些存储的查询匹配此文档”。

`$inverseMatch` 专用于 DocumentDB，没有 MongoDB 对应的等价操作。

## 语法 {#syntax}

该阶段以两种形式之一提供要测试的输入。可以将输入内联在 `input` 中：

```javascript
{
  $inverseMatch: {
    path: <string>,
    input: <expression>,
    defaultResult: <boolean>
  }
}
```

或者通过 `from` 和 `pipeline` 从另一个集合中读取输入：

```javascript
{
  $inverseMatch: {
    path: <string>,
    from: <string>,
    pipeline: [ <stage>, ... ],
    defaultResult: <boolean>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`path`** | 必需。每个文档存储其查询的点号路径。省略该参数将导致 `Path parameter is missing for the operator $inverseMatch` 错误。 |
| **`input`** | 要用存储查询测试的文档。必须是常量值或字符串路径表达式，例如 `"$payload"` — 任何其他形式将导致 `$inverseMatch expects 'input' to be a constant value or a string path expression.` 错误。该值必须解析为一个文档或文档数组。与 `from` 互斥。 |
| **`from`** | 要从中读取输入文档的集合，以字符串形式表示。需要 `pipeline`。与 `input` 互斥。 |
| **`pipeline`** | 当 `from` 设置时为必需。在 `from` 上运行的流水线，用于生成输入文档。仅允许 `$match`、`$project` 和 `$limit` 出现在其中。 |
| **`defaultResult`** | 可选布尔值，默认为 `false`。当文档在 `path` 处无值时所使用的结果 — `false` 会将其丢弃，`true` 会将其保留。 |
{.fields}

`input` 或 `from` 中必须且仅能存在一个。任何其他键都将被拒绝，并返回 `Unrecognized parameter supplied to $inverseMatch: '<name>'` 错误。

## 示例 {#examples}

示例使用一个 `alerts` 集合，其中每个文档存储定义告警的查询：

```json
[
  { "_id": 1, "name": "High value orders", "criteria": { "total": { "$gt": 500 } } },
  { "_id": 2, "name": "Electronics", "criteria": { "category": "electronics" } },
  { "_id": 3, "name": "Bulk orders", "criteria": { "quantity": { "$gte": 10 } } },
  { "_id": 4, "name": "Unfiltered" }
]
```

### 示例 1：哪些存储的查询匹配此文档 {#example-1-which-stored-queries-match-this-document}

查找单个订单会触发的告警：

```javascript
db.alerts.aggregate([
  {
    $inverseMatch: {
      path: "criteria",
      input: { total: 750, category: "electronics", quantity: 2 }
    }
  },
  { $project: { name: 1 } }
])
```

```json
[
  { "_id": 1, "name": "High value orders" },
  { "_id": 2, "name": "Electronics" }
]
```

告警 3 被丢弃，因为该订单的 `quantity` 低于其阈值；告警 4 被丢弃，因为它根本没有 `criteria` 字段 — `defaultResult` 默认为 `false`。

### 示例 2：保留未存储查询的文档 {#example-2-keeping-documents-that-store-no-query}

将 `defaultResult` 设置为 `true`，可将缺失的查询视为匹配，从而实现全匹配规则的建模：

```javascript
db.alerts.aggregate([
  {
    $inverseMatch: {
      path: "criteria",
      input: { total: 750, category: "electronics", quantity: 2 },
      defaultResult: true
    }
  },
  { $project: { name: 1 } }
])
```

```json
[
  { "_id": 1, "name": "High value orders" },
  { "_id": 2, "name": "Electronics" },
  { "_id": 4, "name": "Unfiltered" }
]
```

### 示例 3：从另一个集合获取输入 {#example-3-taking-the-input-from-another-collection}

使用 `from` 和 `pipeline` 将存储的查询与另一个位置保存的文档进行测试，而非直接写入流水线的文档：

```javascript
db.alerts.aggregate([
  {
    $inverseMatch: {
      path: "criteria",
      from: "orders",
      pipeline: [
        { $match: { _id: 4001 } },
        { $project: { total: 1, category: 1, quantity: 1, _id: 0 } },
        { $limit: 1 }
      ]
    }
  },
  { $project: { name: 1 } }
])
```

该流水线仅限于 `$match`、`$project` 和 `$limit`。任何其他阶段将导致：

```
<stage> is not allowed to be used within an $inverseMatch stage, only $match, $project or $limit are allowed
```

## 行为 {#behavior}

- **存储的值必须是一个查询文档。** 如果 `path` 处的值存在但不是文档，则该阶段会报错，而非跳过该文档。
- **缺失的路径不是错误。** 当文档在 `path` 处无值时，该阶段使用 `defaultResult` — `false`，除非你另行设置，因此这些文档默认会静默丢弃。
- **`input` 是一个表达式，而不仅仅是字面量。** 字符串被视为路径表达式，因此 `input: "$payload"` 会将每个存储的查询与该文档自身的 `payload` 字段进行测试。若要传递一个字面量文档，需如上例所示直接内联书写。
- **`input` 可以是数组。** 数组形式的文档也允许，而不仅限于单个文档。

## 相关内容 {#related-content}

- [`$match`](/documentdb/reference/operators/aggregation/match/) — 通常的匹配方向：一个查询，多个文档。
- [`$project`](/documentdb/reference/operators/aggregation/project/) — 调整通过筛选的文档的结构。
- [`$limit`](/documentdb/reference/operators/aggregation/limit/) — `pipeline` 内允许的三个阶段之一。
