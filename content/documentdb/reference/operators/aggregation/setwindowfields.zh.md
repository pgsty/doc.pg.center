---
title: $setWindowFields
description: $setWindowFields 流水线阶段在指定文档范围（窗口）上执行操作，并根据所选窗口运算符返回结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$setwindowfields.md
weight: 300
translation_source_sha256: 018eec0afa019a106407a0b601774b7ce672f46189261b9459ea47ceea1d1f30
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$setWindowFields` 流水线阶段将文档分组为分区，在每个分区内的指定文档范围上应用窗口函数，并为每个文档输出一个包含结果的新字段。这在无需将文档折叠为组的情况下执行计算（如移动平均、排名和累积和）时非常有用。

## 语法 {#syntax}

```javascript
{
  $setWindowFields: {
    partitionBy: <expression>,
    sortBy: {
      <field1>: <1 or -1>,
      ...
    },
    output: {
      <outputField1>: {
        <windowOperator>: <specification>,
        window: {
          // a document window:
          documents: [<lower>, <upper>]

          // -- or a range window, mutually exclusive with the above:
          // range: [<lower>, <upper>],
          // unit: <time unit>
        }
      },
      ...
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`partitionBy`** | 可选。用于将文档分组为分区的表达式。类似于 `$group` 的 `_id`。若省略，则所有文档属于单个分区。 |
| **`sortBy`** | 指定每个分区内排序顺序的文档，每个字段值为 `1`（升序）或 `-1`（降序）。仅在特定情况下可选：`range` 窗口要求恰好一个升序排序字段，有界 `documents` 窗口要求一个排序字段，且多个运算符自身也要求一个排序字段。参见 [sortBy 要求](#sortby-requirements)。 |
| **`output`** | 必需。包含一个或多个字段的文档。每个字段指定一个窗口运算符，并可选择性地指定一个窗口框架。 |
{.fields}

### 窗口框架选项 {#window-frame-options}

| 选项 | 描述 |
| --- | --- |
| **`documents`** | 基于行的窗口边界。`[lower, upper]` 数组，其中值可以是 `"unbounded"`、`"current"` 或整数偏移量。 |
| **`range`** | 基于范围的窗口边界。使用排序键值的 `[lower, upper]` 数组。 |
| **`unit`** | 基于范围窗口的时间单位。取值：`"year"`、`"quarter"`、`"month"`、`"week"`、`"day"`、`"hour"`、`"minute"`、`"second"`、`"millisecond"`。 |
{.fields}

`window` 必须包含 **仅** `documents`，或 **仅** `range` 加上可选的 `unit` — 二者不可混合。混合使用会导致解析失败：

```
Window bounds may only define either 'documents' or 'unit', but never both.
```

既不包含 documents 也不包含 range 的 `window` 同样会被拒绝：

```
'window' field can only contain 'documents' as the only argument or 'range' with an optional 'unit' field
```

<span id="sort-by-requirements"></span>

### sortBy 要求 {#sortby-requirements}

`sortBy` 被解析为可选，但窗口和运算符各自施加其自身要求，因此大多数实际流水线都需要它：

| 情况 | 要求 | 未满足时的错误 |
| --- | --- | --- |
| `range` 窗口 | 必须恰好有一个排序字段，且必须为升序。降序或复合 `sortBy` 会被拒绝，因此 `range` 窗口不能与 `-1` 配合使用。 | `Expected a single sort by field for range-based window` / `Expected ascending sortBy field definition` |
| `documents` 窗口带边界 | 必须有排序字段。仅当窗口在两端均无界时可省略。 | `Missing sortBy field for document-based window` |
| 排名类和位置类运算符 | 要求有排序字段，且多个运算符要求非复合排序字段。`$shift` 无条件要求排序字段。 | `<operator> requires a sortBy` / `<operator> needs a non-compound sortBy parameter` / `'sortBy' parameters must be specified for $shift` |

### 支持的窗口运算符 {#supported-window-operators}

`$addToSet`, `$avg`, `$bottom`, `$bottomN`, `$count`, `$covariancePop`, `$covarianceSamp`, `$denseRank`, `$derivative`, `$documentNumber`, `$expMovingAvg`, `$first`, `$firstN`, `$integral`, `$last`, `$lastN`, `$linearFill`, `$locf`, `$max`, `$maxN`, `$min`, `$minN`, `$push`, `$rank`, `$shift`, `$stdDevPop`, `$stdDevSamp`, `$sum`, `$top`, `$topN`

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "city": "South Amir",
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701
  }
}
```

### 示例 1：按销售额对商店进行排名 {#example-1-rank-stores-by-sales}

按总销售额对所有商店进行排名：

```javascript
db.stores.aggregate([
  {
    $setWindowFields: {
      sortBy: { "sales.totalSales": -1 },
      output: {
        salesRank: { $rank: {} }
      }
    }
  },
  { $project: { name: 1, "sales.totalSales": 1, salesRank: 1 } },
  { $limit: 3 }
])
```

### 示例 2：按城市分区的移动平均值 {#example-2-running-average-partitioned-by-city}

计算每个城市内销售数据的移动平均值，使用 3 个文档的窗口：

```javascript
db.stores.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$city",
      sortBy: { "sales.totalSales": 1 },
      output: {
        movingAvgSales: {
          $avg: "$sales.totalSales",
          window: { documents: [-1, 1] }
        }
      }
    }
  },
  { $project: { name: 1, city: 1, "sales.totalSales": 1, movingAvgSales: 1 } },
  { $limit: 3 }
])
```

### 示例 3：累积和 {#example-3-cumulative-sum}

按总销售额顺序计算销售金额的累积和：

```javascript
db.stores.aggregate([
  {
    $setWindowFields: {
      sortBy: { "sales.totalSales": 1 },
      output: {
        cumulativeSales: {
          $sum: "$sales.totalSales",
          window: { documents: ["unbounded", "current"] }
        }
      }
    }
  },
  { $project: { name: 1, "sales.totalSales": 1, cumulativeSales: 1 } },
  { $limit: 3 }
])
```

### 示例 4：文档编号 {#example-4-document-number}

为每个文档分配一个连续编号：

```javascript
db.stores.aggregate([
  {
    $setWindowFields: {
      sortBy: { name: 1 },
      output: {
        docNumber: { $documentNumber: {} }
      }
    }
  },
  { $project: { name: 1, docNumber: 1 } },
  { $limit: 3 }
])
```

## 限制条件 {#limitations}

- `$setWindowFields` 不支持排序规则
- `$median` 和 `$percentile` 窗口运算符尚未支持
- 不能在同一窗口规范中同时使用 `documents` 和 `range`

## 关键要点 {#key-takeaways}

- **非破坏性** — 与 `$group` 不同，`$setWindowFields` 在每个文档上添加计算字段，而不折叠行
- **分区** — 使用 `partitionBy` 可在各组内独立计算窗口函数
- **灵活窗口** — 使用 `documents` 实现基于行的窗口，或使用 `range` 实现基于值的窗口
- **排名** — `$rank`、`$denseRank` 和 `$documentNumber` 常用于排序和分页
