---
title: $setUnion
description: $setUnion 运算符返回包含所有输入数组中全部不重复元素的数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$setunion.md
weight: 70
translation_source_sha256: f63b8afceb98eaac2f0ed54886b31dfb021408ea1e5f12b57e3c0efdb457d273
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$setUnion` 运算符返回包含所有输入数组中全部不重复元素的数组。它将数组视为集合，去除重复项并忽略元素顺序。无论某个元素在各输入数组中出现多少次，它在结果中都只出现一次。

## 语法 {#syntax}

```javascript
{
  $setUnion: [ <array1>, <array2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `<array1>, <array2>, ...` | 要合并的两个或更多数组。每个数组都被视为集合，最终结果中的重复项会被去除。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "location": {
    "lat": -29.1866,
    "lon": -112.7858
  },
  "staff": {
    "totalStaff": {
      "fullTime": 14,
      "partTime": 8
    }
  },
  "sales": {
    "totalSales": 83865,
    "salesByCategory": [
      {
        "categoryName": "Lavalier Microphones",
        "totalSales": 44174
      },
      {
        "categoryName": "Wireless Microphones",
        "totalSales": 39691
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Cut Spectacular",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 12,
          "Day": 26
        },
        "endDate": {
          "Year": 2024,
          "Month": 1,
          "Day": 5
        }
      },
      "discounts": [
        {
          "categoryName": "Condenser Microphones",
          "discountPercentage": 5
        },
        {
          "categoryName": "Dynamic Microphones",
          "discountPercentage": 14
        }
      ]
    },
    {
      "eventName": "Bargain Bonanza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 25
        },
        "endDate": {
          "Year": 2024,
          "Month": 4,
          "Day": 3
        }
      },
      "discounts": [
        {
          "categoryName": "Streaming Microphones",
          "discountPercentage": 14
        },
        {
          "categoryName": "Microphone Stands",
          "discountPercentage": 14
        }
      ]
    },
    {
      "eventName": "Super Savings Extravaganza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 6,
          "Day": 23
        },
        "endDate": {
          "Year": 2024,
          "Month": 6,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Condenser Microphones",
          "discountPercentage": 7
        },
        {
          "categoryName": "Microphone Stands",
          "discountPercentage": 5
        }
      ]
    }
  ]
}
```

### 示例 1：合并所有产品类别 {#example-1-combine-all-product-categories}

此查询检索商店所有不重复产品类别的列表，其中包括销售类别和促销类别。

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      salesCategories: "$sales.salesByCategory.categoryName",
      firstPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      secondPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
      thirdPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 2] },
      allUniqueCategories: {
        $setUnion: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 2] }
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
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "salesCategories": [
      "Lavalier Microphones",
      "Wireless Microphones"
    ],
    "firstPromotionCategories": [
      "Condenser Microphones",
      "Dynamic Microphones"
    ],
    "secondPromotionCategories": [
      "Streaming Microphones",
      "Microphone Stands"
    ],
    "thirdPromotionCategories": [
      "Condenser Microphones",
      "Microphone Stands"
    ],
    "allUniqueCategories": [
      "Lavalier Microphones",
      "Wireless Microphones",
      "Condenser Microphones",
      "Dynamic Microphones",
      "Streaming Microphones",
      "Microphone Stands"
    ]
  }
]
```
