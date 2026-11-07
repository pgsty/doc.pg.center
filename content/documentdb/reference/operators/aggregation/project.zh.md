---
title: $project
description: 聚合流水线中的 $project 阶段通过包含、排除或计算字段来调整文档结构。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$project.md
weight: 230
translation_source_sha256: 7d58428733249fa1ab328b9ac9489b7d31ab2b9e145f68d7a1cd778a31666253
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$project` 阶段会调整经过它的每个文档的结构。可以用它仅保留所需字段、移除不需要的字段、重命名字段，或根据现有值计算并添加字段。

## 语法 {#syntax}

```javascript
{
  $project: {
    <field1>: <1 | true | 0 | false | expression>,
    <field2>: <1 | true | 0 | false | expression>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要包含、排除或计算的字段名称。可以使用 `sales.totalSales` 这样的点号路径指定嵌套字段。 |
| **`1` 或 `true`** | 在输出文档中包含该字段。 |
| **`0` 或 `false`** | 从输出文档中排除该字段。 |
| **`expression`** | 聚合表达式，其结果作为该字段的值。添加计算字段属于包含操作。 |
{.fields}

## 示例 {#examples}

本页示例使用 `stores` 集合中的以下文档。

```json
{
  "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
  "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
  "location": { "lat": -89.2384, "lon": -46.4012 },
  "staff": { "totalStaff": { "fullTime": 8, "partTime": 20 } },
  "sales": {
    "totalSales": 75670,
    "salesByCategory": [
      { "categoryName": "Wine Accessories", "totalSales": 34440 },
      { "categoryName": "Bitters", "totalSales": 39496 },
      { "categoryName": "Rum", "totalSales": 1734 }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Unbeatable Bargain Bash",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 7, "Day": 2 }
      },
      "discounts": [
        { "categoryName": "Whiskey", "discountPercentage": 7 },
        { "categoryName": "Bitters", "discountPercentage": 15 }
      ]
    }
  ]
}
```

此处省略了 `promotionEvents` 数组的部分内容；完整文档包含多个活动，每个活动都有自己的折扣列表。

### 示例 1：包含指定字段 {#example-1-including-specific-fields}

此查询仅保留商店名称及其总销售额，并移除 `_id`。

```javascript
db.stores.aggregate([
  { $project: { _id: 0, name: 1, "sales.totalSales": 1 } }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "sales": { "totalSales": 75670 }
  }
]
```

对点号路径进行投影会保留外围结构：返回的 `sales.totalSales` 仍然嵌套在 `sales` 中，不会被展平。

### 示例 2：添加计算字段 {#example-2-adding-a-computed-field}

此查询返回商店名称，以及从两个员工字段计算得出的员工人数。

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      name: 1,
      totalStaff: {
        $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      }
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "totalStaff": 28
  }
]
```

### 示例 3：排除字段 {#example-3-excluding-fields}

当投影定义中的所有字段均设置为 `0` 时，该阶段执行排除式投影：除列出的字段外，其余所有字段都会保留。

```javascript
db.stores.aggregate([
  { $project: { sales: 0, staff: 0, location: 0, promotionEvents: 0 } }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth"
  }
]
```

## 行为 {#behavior}

**默认包含 `_id`。** 它是唯一可以在包含式投影中使用 `0` 或 `false` 移除的字段。单独使用 `{ $project: { _id: 0 } }` 则属于纯粹的排除操作，会保留其他所有字段。

这一例外**仅适用于顶层 `_id`**。嵌套的 `_id` 与其他字段的行为相同，因此以下操作会失败：

```javascript
db.stores.aggregate([{ $project: { name: 1, sales: { _id: 0 } } }])
```

```
exclusion cannot be applied to field _id within the inclusion projection.
```

**`$$REMOVE` 可以从包含式投影中移除任何字段。** 将 `$$REMOVE` 赋给字段属于表达式，而非排除操作，因此不会违反包含与排除不能混用的规则，且输出中不会出现该字段：

```javascript
db.stores.aggregate([{ $project: { name: 1, location: "$$REMOVE" } }])
```

这使得按条件移除字段成为可能：`{ $cond: [<test>, "$field", "$$REMOVE"] }` 仅在条件满足时保留字段。

**包含与排除不能混用。** 除顶层 `_id` 外，单个 `$project` 要么执行包含式投影，要么执行排除式投影。混用二者会失败：

```javascript
db.stores.aggregate([{ $project: { name: 1, location: 0 } }])
```

```
exclusion cannot be applied to field location within the inclusion projection.
```

**字段名称不能以 `$` 开头。** 字面名称以 `$` 开头的字段会被拒绝；请使用 `$getField` 或 `$setField` 处理这类字段：

```
FieldPath field names cannot begin with the operators symbol '$'; you might want to use $getField or $setField instead.
```

DBRef 字段名称 `$id`、`$ref` 和 `$db` 不受这一限制，因此 `{ $project: { "$id": 1 } }` 可以被接受，并直接对符合 DBRef 结构的文档进行投影。

**允许使用空的投影定义。** `{ $project: {} }` 会原样传递文档，而不会报错。

## 相关 {#related}

- [`$addFields`](/documentdb/reference/operators/aggregation/addfields/) — 添加字段，同时保留所有现有字段。
- [`$set`](/documentdb/reference/operators/aggregation/set/) — `$addFields` 的别名。
- [`$unset`](/documentdb/reference/operators/aggregation/unset/) — 移除字段，而不将整个阶段切换为排除语义。
- [`$meta`](/documentdb/reference/operators/projection/meta/) — 将搜索元数据作为投影字段输出，例如 `$vectorSearch` 的相似度分数。
