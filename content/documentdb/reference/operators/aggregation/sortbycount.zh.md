---
title: $sortByCount
description: 聚合流水线中的 $sortByCount 流水线阶段用于按指定表达式对文档进行分组，然后按每组文档数量降序排序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$sortbycount.md
weight: 330
translation_source_sha256: 3ea9d3620737739bf6600c6dd2a6fc2c9cde52c725a2339bfbef1aef37cf1497
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 $sortByCount 流水线阶段用于按指定表达式对文档进行分组，然后按每组文档数量降序排序。`$sortByCount` 流水线阶段有助于快速识别数据集中最常见的值。

## 语法 {#syntax}

```javascript
{
  $sortByCount: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 用于分组和统计文档的字段或计算表达式。 |
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

### 示例 1：按名称分组促销事件并按出现次数降序计数 {#example-1-group-promotion-events-by-name-and-count-occurrences-in-descending-order}

按 eventName 字段分组，并统计每个事件名称的出现次数，结果按计数降序排列

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $sortByCount: "$promotionEvents.eventName" }
])
```

此查询返回以下结果：

```json
[
  { "_id": "Crazy Deal Days", "count": 4239 },
  { "_id": "Markdown Madness", "count": 2967 },
  { "_id": "Bargain Bonanza", "count": 2925 },
  { "_id": "Crazy Discount Days", "count": 2922 },
  { "_id": "Price Smash Spectacular", "count": 2915 },
  { "_id": "Super Saver Spectacular", "count": 2900 },
  { "_id": "Crazy Markdown Madness", "count": 2899 },
  { "_id": "Price Cut Carnival", "count": 2868 },
  { "_id": "Grand Bargain Bash", "count": 2849 },
  { "_id": "Bargain Blitz Bash", "count": 2843 },
  { "_id": "Grand Savings Gala", "count": 2826 },
  { "_id": "Super Saver Fiesta", "count": 1551 },
  { "_id": "Major Deal Days", "count": 1548 },
  { "_id": "Price Slash Carnival", "count": 1535 },
  { "_id": "Super Discount Days", "count": 1533 },
  { "_id": "Big Deal Bonanza", "count": 1533 },
  { "_id": "Incredible Savings Showcase", "count": 1531 },
  { "_id": "Unbeatable Savings Spectacular", "count": 1518 },
  { "_id": "Fantastic Deal Days", "count": 1511 },
  { "_id": "Flash Bargain Frenzy", "count": 1504 }
]
```

此聚合流水线将执行以下操作：

1. 使用 $unwind 从输入文档中展开 promotionEvents 数组字段。
2. 使用 $sortByCount 按 eventName 字段分组，并统计每个事件名称的出现次数，结果按计数降序排列。
