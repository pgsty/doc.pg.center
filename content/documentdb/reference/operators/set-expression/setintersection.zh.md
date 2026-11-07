---
title: $setIntersection
description: $setIntersection 运算符返回所有输入数组中都存在的共同元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$setintersection.md
weight: 50
translation_source_sha256: 05bb05f192961d16018adccbed650a592e0686898d81e5f8e8d6eec6283646ee
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$setIntersection` 运算符返回一个数组，其中包含所有输入数组中都存在的元素。它将数组视为集合，即去除重复项并忽略元素顺序。

## 语法 {#syntax}

```javascript
{
  $setIntersection: [ <array1>, <array2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `<array1>, <array2>, ...` | 要求交集的两个或更多数组。每个数组都被视为集合。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        },
        "endDate": {
          "Year": 2023,
          "Month": 7,
          "Day": 9
        }
      },
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Projector Lamps",
          "discountPercentage": 6
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Blu-ray Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Home Theater Systems",
          "discountPercentage": 5
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 22
        }
      ]
    },
    {
      "eventName": "Discount Delight Days",
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
          "categoryName": "Game Controllers",
          "discountPercentage": 22
        },
        {
          "categoryName": "Home Theater Projectors",
          "discountPercentage": 23
        },
        {
          "categoryName": "Sound Bars",
          "discountPercentage": 10
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 10
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 9
        },
        {
          "categoryName": "Projector Lamps",
          "discountPercentage": 24
        }
      ]
    }
  ]
}
```

### 示例 1：查找销售与促销中的共同类别 {#example-1-find-common-categories-between-sales-and-promotions}

此查询判断哪些产品类别同时出现在商店的销售数据和促销折扣中。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      salesCategories: "$sales.salesByCategory.categoryName",
      firstPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      secondPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
      commonSalesAndFirstPromotion: {
        $setIntersection: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] }
        ]
      },
      commonSalesAndSecondPromotion: {
        $setIntersection: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] }
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
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "salesCategories": [
      "Sound Bars",
      "Game Controllers",
      "Remote Controls",
      "VR Games"
    ],
    "firstPromotionCategories": [
      "DVD Players",
      "Projector Lamps",
      "Media Players",
      "Blu-ray Players",
      "Home Theater Systems",
      "Televisions"
    ],
    "secondPromotionCategories": [
      "TV Mounts",
      "Game Accessories",
      "Portable Projectors",
      "Projector Screens",
      "Blu-ray Players",
      "DVD Players"
    ],
    "commonSalesAndFirstPromotion": [],
    "commonSalesAndSecondPromotion": []
  }
]
```

### 示例 2：查找多个促销活动中的共同类别 {#example-2-find-common-categories-across-multiple-promotion-events}

此查询获取出现在多个促销活动中的类别。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      commonAcrossPromotions: {
        $setIntersection: [
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
      "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
      "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
      "commonAcrossPromotions": []
   }
]
```
