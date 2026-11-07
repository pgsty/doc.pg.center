---
title: $indexStats
description: $indexStats 流水线阶段返回集合中每个索引的使用统计信息。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$indexstats.md
weight: 150
translation_source_sha256: bb2604c46ae53768329ba596506e3d745712e2ab5d251c5a2e9e7350d0ea1832
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$indexStats` 聚合流水线阶段返回集合中每个索引的使用统计信息。该阶段有助于分析索引性能、识别未使用的索引，并优化查询性能。

## 语法 {#syntax}

```javascript
{
  $indexStats: {}
}
```

## 参数 {#parameters}

`$indexStats` 流水线阶段不接受任何参数。

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
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

<span id="example-1-fetch-index-statistics"></span>

### 示例 1 - 获取索引统计信息 {#example-1---fetch-index-statistics}

此查询检索 stores 集合上所有索引的使用统计信息。

```javascript
db.stores.aggregate([
  { $indexStats: {} }
])
```

该查询返回每个索引的统计信息，包括访问模式和使用频率。

```json
[
  {
    "name": "_id_",
    "key": { "_id": 1 },
    "accesses": { "ops": 41675, "since": "2025-06-07T13:51:41.231Z" },
    "spec": { "v": 2, "key": { "_id": 1 }, "name": "_id_" }
  },
  {
    "name": "location_2dsphere",
    "key": { "location": "2dsphere" },
    "accesses": { "ops": 0, "since": "2025-06-07T13:51:41.231Z" },
    "spec": {
      "v": 2,
      "key": { "location": "2dsphere" },
      "name": "location_2dsphere",
      "2dsphereIndexVersion": 3
    }
  },
  {
    "name": "name_text_sales.salesByCategory.categoryName_text_promotionEvents.eventName_text_promotionEvents.discounts.categoryName_text",
    "key": {
      "name": "text",
      "sales.salesByCategory.categoryName": "text",
      "promotionEvents.eventName": "text",
      "promotionEvents.discounts.categoryName": "text"
    },
    "accesses": { "ops": 8, "since": "2025-06-07T13:51:41.231Z" },
    "spec": {
      "v": 2,
      "key": {
        "name": "text",
        "sales.salesByCategory.categoryName": "text",
        "promotionEvents.eventName": "text",
        "promotionEvents.discounts.categoryName": "text"
      },
      "name": "name_text_sales.salesByCategory.categoryName_text_promotionEvents.eventName_text_promotionEvents.discounts.categoryName_text"
    }
  }
]
```
