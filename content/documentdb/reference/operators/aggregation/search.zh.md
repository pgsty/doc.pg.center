---
title: $search
description: $search 阶段在聚合流水线中通过 cosmosSearch 或 knnBeta 运算符运行向量相似性搜索。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$search.md
weight: 280
translation_source_sha256: 8867cbd722d3d1b2e496b378012b7f441f0a9ae379de74111255633b2ce2cb11
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$search` 阶段在向量索引上运行向量相似性搜索。该阶段仅携带一个搜索运算符——`cosmosSearch`，或已弃用的 `knnBeta`——并返回其存储嵌入与查询向量最接近的文档。

`$search` 必须是流水线中的第一个阶段，且 `path` 所命名的字段必须被向量索引覆盖。

> 在 DocumentDB 中，`$search` 是一个向量搜索阶段。它不接受文本搜索运算符：包含 `{ $search: { text: { ... } } }` 的规范将被拒绝并返回 `Unrecognized $search option: text`。对于全文查询，请使用针对文本索引的 `$text` 查询运算符。对于新项目，建议使用 [`$vectorSearch`](/documentdb/reference/operators/aggregation/vectorsearch/)，这是当前的向量搜索阶段，其规范更清晰；`$search` 仍保留以兼容现有的 `cosmosSearch` 和 `knnBeta` 查询。

## 语法 {#syntax}

```javascript
{
  $search: {
    index: <string>,
    cosmosSearch: {
      path: <string>,
      vector: [<number>, ...],
      k: <positiveInteger>,
      filter: <document>,
      exact: <boolean>,
      oversampling: <number>
    }
  }
}
```

## 参数 {#parameters}

该阶段必须恰好包含一个搜索运算符，外加少量可选参数。

| 参数 | 描述 |
| --- | --- |
| **`cosmosSearch`** | 搜索运算符，包含下文描述的查询规范。必须恰好存在一个运算符——同时提供 `cosmosSearch` 和 `knnBeta` 会因 `The $search spec can only contain one search operator.` 失败，未提供任何运算符则因 `Invalid search spec provided, must include one of the supported operators.` 失败 |
| **`knnBeta`** | 已弃用的别名，为向后兼容而保留。其规范与 `cosmosSearch` 相同，但会直接拒绝 `filter` 和 `score`。请改用 `cosmosSearch`。 |
| **`index`** | 可选。要搜索的索引名称，以字符串形式指定。 |
| **`returnStoredSource`** | 可选。为兼容性而接受，但被忽略。 |
| **`count`** | 可选。已解析并验证，但生成的计数元数据**尚未在结果中发出**，因此该选项当前无可观测效果。 |
{.fields}

任何与运算符并列的其他键都会因 `Unrecognized $search option: <name>` 被拒绝。

### 运算符规范 {#operator-spec}

| 字段 | 描述 |
| --- | --- |
| **`path`** | 必需。存储嵌入的文档字段。必须被向量索引覆盖。省略时会因 `$path is required field for using a vector index.` 失败 |
| **`vector`** | 必需。查询嵌入，作为非空数字数组。省略时会因 `$vector is required field for using a vector index.` 失败 |
| **`k`** | 必需。要返回的文档数量，为正整数。 |
| **`filter`** | 可选。与向量搜索相交的查询文档。需要在服务器上启用向量预过滤；若未启用，则查询会因 `$filter is not supported for vector search yet.` 失败。在 `knnBeta` 中完全不支持。 |
| **`exact`** | 可选。布尔值。执行精确搜索而非近似搜索。 |
| **`oversampling`** | 可选。在近似搜索期间扩大候选集，提高召回率，但增加延迟。 |
| **`score`** | 可选。与 `knnBeta` 不兼容，后者会因 `$score is not supported for knnBeta queries.` 拒绝它 |
{.fields}

## 示例 {#examples}

本页示例使用 `products` 集合中的以下文档，并在 `embedding` 上建立了向量索引。

```json
[
  { "_id": 1, "name": "Espresso Machine", "category": "appliance", "embedding": [0.9, 0.1, 0.05] },
  { "_id": 2, "name": "Coffee Grinder", "category": "appliance", "embedding": [0.85, 0.15, 0.1] },
  { "_id": 3, "name": "Merlot Bottle", "category": "wine", "embedding": [0.05, 0.9, 0.2] },
  { "_id": 4, "name": "Chardonnay Bottle", "category": "wine", "embedding": [0.1, 0.85, 0.25] }
]
```

### 示例 1：查询向量的最近邻 {#example-1-nearest-neighbors-for-a-query-vector}

返回与查询嵌入最接近的三个文档：

```javascript
db.products.aggregate([
  {
    $search: {
      cosmosSearch: {
        path: "embedding",
        vector: [0.88, 0.12, 0.07],
        k: 3
      }
    }
  },
  { $project: { name: 1, category: 1 } }
])
```

```json
[
  { "_id": 1, "name": "Espresso Machine", "category": "appliance" },
  { "_id": 2, "name": "Coffee Grinder", "category": "appliance" },
  { "_id": 4, "name": "Chardonnay Bottle", "category": "wine" }
]
```

### 示例 2：精确搜索 {#example-2-exact-search}

将 `exact` 设置为 `true`，以与每个索引向量进行比较，而非近似候选集。这速度较慢，但在需要参考结果以衡量召回率时有用：

```javascript
db.products.aggregate([
  {
    $search: {
      cosmosSearch: {
        path: "embedding",
        vector: [0.88, 0.12, 0.07],
        k: 3,
        exact: true
      }
    }
  },
  { $project: { name: 1 } }
])
```

## 行为 {#behavior}

- **`$search` 必须位于首位。** 将其置于流水线中其他位置会因 `$search must appear as the initial stage in the pipeline sequence.` 失败。即使流水线已经在它之前包含 limit 阶段，也同样如此。
- **每个规范仅允许一个运算符。** 该阶段会拒绝包含多个搜索运算符的规范，也拒绝不包含任何运算符的规范。
- **`path` 必须被索引。** `path` 所命名的字段必须被向量索引覆盖；请参阅 [`$vectorSearch`](/documentdb/reference/operators/aggregation/vectorsearch/) 了解如何创建索引。

## 相关内容 {#related-content}

- [`$vectorSearch`](/documentdb/reference/operators/aggregation/vectorsearch/) — 当前的向量搜索阶段，建议用于新查询。
- [`$project`](/documentdb/reference/operators/aggregation/project/) — 用于调整搜索返回的文档。
- [`$limit`](/documentdb/reference/operators/aggregation/limit/) — 进一步缩小结果集；`k` 已经进行了限制。
