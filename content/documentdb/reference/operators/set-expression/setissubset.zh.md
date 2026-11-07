---
title: $setIsSubset
description: $setIsSubset 运算符判断一个数组是否为第二个数组的子集。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$setissubset.md
weight: 60
translation_source_sha256: 6d36c865cb5b4a867ae1406176bf0141490e225a68dfba86c517c1d606bd5f3e
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例说明既写“反向也检查”，又写“不进行反向检查”。代码包含两个参数顺序相反的子集表达式，因此该示例分别检查了两个方向。

`$setIsSubset` 运算符返回布尔值，表示一个数组是否为第二个数组的子集。它将数组视为集合，即忽略重复项和元素顺序。如果第一个数组中的所有元素都存在于第二个数组中，则返回 `true`；否则返回 `false`。

## 语法 {#syntax}

```javascript
{
  $setIsSubset: [ <array1>, <array2> ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `<array1>` | 要检查是否为 `<array2>` 子集的数组。 |
| `<array2>` | 用于比较的数组。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        },
        {
          "categoryName": "Bathroom Scales",
          "discountPercentage": 9
        },
        {
          "categoryName": "Towels",
          "discountPercentage": 5
        },
        {
          "categoryName": "Bathrobes",
          "discountPercentage": 5
        },
        {
          "categoryName": "Mattress Toppers",
          "discountPercentage": 6
        },
        {
          "categoryName": "Hand Towels",
          "discountPercentage": 9
        },
        {
          "categoryName": "Shower Heads",
          "discountPercentage": 5
        },
        {
          "categoryName": "Bedspreads",
          "discountPercentage": 19
        },
        {
          "categoryName": "Bath Mats",
          "discountPercentage": 21
        }
      ]
    }
  ]
}
```

### 示例 1：判断销售类别是否为促销类别的子集 {#example-1-determine-if-sales-categories-are-a-subset-of-promotion-categories}

此查询判断商店的所有类别是否都包含在促销折扣中，反向也同样检查。此查询返回同时属于销售和促销范围的类别。它确认 `sales` 值是否为特定促销类别的子集（但不进行反向检查）。

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      salesCategories: "$sales.salesByCategory.categoryName",
      promotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      salesAreSubsetOfPromotions: {
        $setIsSubset: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] }
        ]
      },
      promotionsAreSubsetOfSales: {
        $setIsSubset: [
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          "$sales.salesByCategory.categoryName"
        ]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "salesCategories": [
      "Mattress Toppers"
    ],
    "promotionCategories": [
      "Bath Accessories",
      "Pillow Top Mattresses",
      "Bathroom Scales",
      "Towels",
      "Bathrobes",
      "Mattress Toppers",
      "Hand Towels",
      "Shower Heads",
      "Bedspreads",
      "Bath Mats"
    ],
    "salesAreSubsetOfPromotions": true,
    "promotionsAreSubsetOfSales": false
  }
]
```
