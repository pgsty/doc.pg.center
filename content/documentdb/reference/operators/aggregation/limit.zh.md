---
title: $limit
description: 聚合流水线中的 $limit 阶段限制传递到下一阶段的文档数量。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$limit.md
weight: 180
translation_source_sha256: e9a4848d07f8a1cdfd5de087c2e021cc0a6efbabc3a9e5b5fb6386a1cfd97df0
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$limit` 流水线阶段限制传递到下一阶段的文档数量。它通常与 `$sort` 结合使用以返回前 N 个结果，或置于 `$match` 之后以限制后续阶段的工作量。

## 语法 {#syntax}

```javascript
{
  $limit: <positiveInteger>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`positiveInteger`** | 传递到下一阶段的最大文档数量。必须是可以表示为 64 位整数的数值，且必须大于零。 |
{.fields}

## 示例 {#examples}

本页示例使用 `stores` 集合中的以下文档。

```json
[
  {
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "sales": { "totalSales": 75670 }
  },
  {
    "_id": "2e2f4c9e-6a1c-4a3a-9b52-7f1a5d0c2f11",
    "name": "Fourth Coffee | Beverage Shop - Lake Ellenmouth",
    "sales": { "totalSales": 21200 }
  },
  {
    "_id": "9d2c1a77-8f52-4a1e-9a55-3d4e6b8c0a22",
    "name": "Contoso | Beverage Shop - Port Alina",
    "sales": { "totalSales": 112400 }
  }
]
```

### 示例 1：返回前 N 个结果 {#example-1-returning-the-top-results}

此查询按总销售额对 stores 进行排序，并仅返回最高的两个文档。

```javascript
db.stores.aggregate([
  { $sort: { "sales.totalSales": -1 } },
  { $project: { _id: 0, name: 1, "sales.totalSales": 1 } },
  { $limit: 2 }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "Contoso | Beverage Shop - Port Alina",
    "sales": { "totalSales": 112400 }
  },
  {
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "sales": { "totalSales": 75670 }
  }
]
```

需要前 N 个结果时，应将 `$limit` 放在 `$sort` 之后。如果 `$limit` 在 `$sort` 之前执行，就会先截断输入，因此排序只会处理保留下来的文档。

### 示例 2：限制为单个文档 {#example-2-limiting-to-a-single-document}

```javascript
db.stores.aggregate([
  { $match: { "sales.totalSales": { $gt: 50000 } } },
  { $limit: 1 },
  { $project: { _id: 0, name: 1 } }
])
```

此查询返回以下结果：

```json
[
  { "name": "First Up Consultants | Beverage Shop - Satterfieldmouth" }
]
```

若无前置的 `$sort`，哪个文档能够保留下来无法保证。

## 行为 {#behavior}

每个 `$limit` 均作用于其前序阶段的输出。当两个 `$limit` 阶段相邻时，其效果为两者中较小值——`[{ $limit: 10 }, { $limit: 3 }]` 最多产生三个文档。

该优化不适用于可产生多于其消耗文档数量的阶段。在以下流水线中，第一个 `$limit` 将输入限制为三个文档，`$unwind` 扩展这些文档，第二个 `$limit` 再对扩展后的行进行限制——因此结果最多可达十个文档，而非三个：

```javascript
db.stores.aggregate([
  { $limit: 3 },
  { $unwind: "$promotionEvents" },
  { $limit: 10 }
])
```

`$lookup` 后接 `$unwind` 的组合，以及 `$unionWith` 阶段，也具有相同的行为。

## 错误情况 {#error-cases}

| 规范 | 错误 |
| --- | --- |
| `{ $limit: 0 }` | `The specified limit value must always be positive` |
| `{ $limit: -1 }` | `Invalid argument passed to the $skip stage: a non-negative number was expected but received in $limit: -1` |
| `{ $limit: "2" }` | `the limit must be specified as a number` |

无法表示为 64 位整数的值同样会被拒绝。

## 相关 {#related}

- [`$skip`](/documentdb/reference/operators/aggregation/skip/) —— 跳过文档而非截断结果。
- [`$sort`](/documentdb/reference/operators/aggregation/sort/) —— 在限制前对文档进行排序。
