---
title: $bucketAuto
description: $bucketAuto 阶段根据分组表达式，自动将文档分配到指定数量的桶中。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$bucketauto.md
weight: 30
translation_source_sha256: 58ecc124a09ae9670db610d92a786c19f00027b87868f0009ff12e534a6c8d02
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bucketAuto` 流水线阶段根据 `groupBy` 表达式的值，将文档分类到指定数量的桶中，尝试基于该表达式的值均匀分布文档。与 [`$bucket`](/documentdb/reference/operators/aggregation/bucket/) 不同，你无需提供边界——DocumentDB 会为你自动计算。

自 `v0.105-0` 起支持。

## 语法 {#syntax}

```javascript
{
  $bucketAuto: {
    groupBy: <expression>,
    buckets: <number>,
    output: {
      <outputField1>: { <accumulator1> },
      ...
    },
    granularity: <granularity-string>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`groupBy`** | 用于分组文档的表达式。该表达式必须解析为可比较的值。 |
| **`buckets`** | 指定输入文档应分组到的桶数量的正 32 位整数。 |
| **`output`** | 可选。指定每个桶计算字段的文档。每个字段是一个累加器表达式，例如 `$sum`、`$avg`、`$min`、`$max`、`$push` 或 `$addToSet`。若省略，则 `$bucketAuto` 默认输出一个 `count` 字段。 |
| **`granularity`** | 可选。指定用于舍入桶边界的[首选数列](https://en.wikipedia.org/wiki/Preferred_number)的字符串。支持的值：`POWERSOF2`、`1-2-5`、`R5`、`R10`、`R20`、`R40`、`R80`、`E6`、`E12`、`E24`、`E48`、`E96`、`E192`。当使用 `granularity` 时，`groupBy` 值必须为数值且非负。 |
{.fields}

## 行为 {#behavior}

- `$bucketAuto` 输出的文档包含一个 `_id`，其形式为 `{ "min": <lower>, "max": <upper> }`，表示桶的下限和上限。除最后一个桶包含其上界外，其余桶均不包含上界。
- 若未指定 `granularity`，非最后一个桶的 `max` 为下一个桶的首个 `groupBy` 值，因此相邻桶共享边界。最后一个桶的 `max` 为其自身最大值。
- 文档按输入允许的最均匀方式分布：若有 `n` 个文档和 `b` 个桶，则每个桶平均分配 `floor(n / b)` 个文档，剩余的 `n mod b` 个文档将按顺序逐个分配给需要的桶，优先分配给较早的桶。随后，每个桶会扩展以吸收与其最大值相等的后续文档，确保相等值不会跨越边界。每个吸收的文档消耗一个剩余名额，因此当 `n` 不能被 `b` 整除时，多余的文档并不总落在最早的桶中。
- 该阶段可能生成少于请求数量的桶——当不同 `groupBy` 值的数量少于 `buckets` 时，或当 `granularity` 舍入吸收文档时（见下文）。
- 当指定 `granularity` 时，第一个桶的 `min` 会向下舍入到其严格下方最近的数列值，每个桶的 `max` 会向上舍入到其严格上方最近的数列值；每个后续桶的 `min` 仅是前一个桶的 `max`。由于向上舍入后的 `max` 可能超过后续桶分配的值，这些文档会被拉入当前桶，因此结果通常返回的桶数少于请求数量。通过这种方式生成的边界为双精度浮点数。
- 使用 `granularity` 时，每个 `groupBy` 值必须为数值且非负；非数值值将导致 `$bucketAuto only allows specifying a 'granularity' with numeric boundaries` 错误。

## 示例 {#examples}

考虑以下示例 `sales` 集合：

```json
[
  { "_id": 1, "category": "Books",       "price":   8 },
  { "_id": 2, "category": "Books",       "price":  12 },
  { "_id": 3, "category": "Electronics", "price":  45 },
  { "_id": 4, "category": "Electronics", "price": 230 },
  { "_id": 5, "category": "Toys",        "price":   3 },
  { "_id": 6, "category": "Toys",        "price":  18 },
  { "_id": 7, "category": "Clothing",    "price":  35 },
  { "_id": 8, "category": "Clothing",    "price":  60 }
]
```

### 示例 1：三个均匀价格桶 {#example-1-three-even-price-buckets}

将销售记录分为三个桶，每个桶包含大致相同数量的文档，并计算每个桶的文档计数和平均价格：

```javascript
db.sales.aggregate([
  {
    $bucketAuto: {
      groupBy: "$price",
      buckets: 3,
      output: {
        count: { $sum: 1 },
        avgPrice: { $avg: "$price" }
      }
    }
  }
])
```

示例输出：

```json
[
  { "_id": { "min": 3,  "max": 18  }, "count": 3, "avgPrice": 7.666666666666667 },
  { "_id": { "min": 18, "max": 60  }, "count": 3, "avgPrice": 32.666666666666664 },
  { "_id": { "min": 60, "max": 230 }, "count": 2, "avgPrice": 145 }
]
```

八个文档分为三个桶，大小为 3、3、2。桶分别包含价格 `3, 8, 12`、然后 `18, 35, 45`、然后 `60, 230`。每个非最后一个桶报告下一个桶的第一个价格作为其 `max`，因此第一个桶在 `18` 结束，第二个桶在 `60` 结束。

### 示例 2：通过 `granularity` 对桶边界进行舍入 {#example-2-buckets-with-rounded-boundaries-via-granularity}

请求四个桶，并将边界舍入到 2 的幂构成的数列中的值：

```javascript
db.sales.aggregate([
  {
    $bucketAuto: {
      groupBy: "$price",
      buckets: 4,
      granularity: "POWERSOF2"
    }
  }
])
```

示例输出：

```json
[
  { "_id": { "min": 2,  "max": 16  }, "count": 3 },
  { "_id": { "min": 16, "max": 64  }, "count": 4 },
  { "_id": { "min": 64, "max": 256 }, "count": 1 }
]
```

请求的是四个桶，但返回了三个。均匀划分原本会将 `3, 8` 放入第一个桶，但将其 `max` 从 `8` 向上舍入到 `16` 后，`12` 也被纳入其中。第二个桶从 `18` 开始，将其 `max` 从 `35` 向上舍入到 `64` 后，会吸收 `45` 和 `60`，第三个桶便只剩下 `230`。

## 参见 {#see-also}

- [`$bucket`](/documentdb/reference/operators/aggregation/bucket/) — 固定边界的分桶。
- [`$group`](/documentdb/reference/operators/aggregation/group/) — 通过表达式进行通用分组。
