---
title: $replaceRoot
description: $replaceRoot 流水线阶段会将输入文档替换为指定的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$replaceroot.md
weight: 250
translation_source_sha256: 45207d5000f4e688b77abeffd41b2a26f5043a4d033ba7793b4ed6b5c61d78fa
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$replaceRoot` 流水线阶段会将输入文档替换为指定的文档。该操作会替换输入文档中的所有现有字段，包括 `_id` 字段。此操作适用于将嵌入式文档提升至顶层。

## 语法 {#syntax}

```javascript
{
  $replaceRoot: {
    newRoot: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`newRoot`** | 必需。一个解析为文档的表达式。该表达式可以是任何有效且能解析为文档的表达式，例如指向嵌入式文档的字段路径、`$mergeObjects` 表达式，或字面量文档。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
  "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
  "location": {
    "lat": -89.2384,
    "lon": -46.4012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 8,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 75670,
    "salesByCategory": [
      { "categoryName": "Wine Accessories", "totalSales": 34440 }
    ]
  }
}
```

### 示例 1：提升嵌入式文档 {#example-1-promote-an-embedded-document}

将 `staff.totalStaff` 子文档提升至顶层：

```javascript
db.stores.aggregate([
  { $replaceRoot: { newRoot: "$staff.totalStaff" } },
  { $limit: 1 }
])
```

此查询返回：

```json
[
  { "fullTime": 8, "partTime": 20 }
]
```

<span id="example-2-use-merge-objects-to-combine-fields"></span>

### 示例 2：使用 $mergeObjects 合并字段 {#example-2-use-mergeobjects-to-combine-fields}

将 staff 子文档与额外的顶层字段合并：

```javascript
db.stores.aggregate([
  {
    $replaceRoot: {
      newRoot: {
        $mergeObjects: [
          "$staff.totalStaff",
          { storeName: "$name", totalSales: "$sales.totalSales" }
        ]
      }
    }
  },
  { $limit: 1 }
])
```

此查询返回：

```json
[
  {
    "fullTime": 8,
    "partTime": 20,
    "storeName": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "totalSales": 75670
  }
]
```

### 示例 3：在 $unwind 之后替换根文档 {#example-3-replace-root-after-unwind}

将各个销售类别提取为顶层文档：

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $replaceRoot: {
      newRoot: {
        $mergeObjects: [
          "$sales.salesByCategory",
          { storeName: "$name" }
        ]
      }
    }
  },
  { $limit: 3 }
])
```

## 限制条件 {#limitations}

- 如果 `newRoot` 求值为缺失值或非文档类型，该操作将报错

## 关键要点 {#key-takeaways}

- **替换整个文档** — 输出文档即为求值后的 `newRoot` 表达式
- **`$replaceWith` 是别名** — `{ $replaceWith: <expression> }` 是 `{ $replaceRoot: { newRoot: <expression> } }` 的简写形式
- **可与 `$mergeObjects` 结合使用** — 使用 `$mergeObjects` 可在提升嵌入式文档的同时保留原始文档的字段
