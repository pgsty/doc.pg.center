---
title: $facet
description: $facet 允许在单个流水线阶段内执行多个并行聚合。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$facet.md
weight: 100
translation_source_sha256: d8c3dd7fffde06dd14b50adba03e2d98419bb49f2a483d6eb1feed12dcafeaa2
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$facet` 流水线阶段允许在单个流水线阶段内执行多个并行聚合。这在单个查询中对同一数据集执行多种分析时非常有用。

## 语法 {#syntax}

```javascript
{
  "$facet": {
    "outputField1": [ { "stage1": {} }, { "stage2": {} } ],
    "outputField2": [ { "stage1": {} }, { "stage2": {} } ]
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`outputFieldN`** | 输出字段的名称。 |
| **`stageN`** | 要执行的聚合阶段。 |
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

### 示例 1：对销售和促销活动进行分面搜索 {#example-1-faceted-search-on-sales-and-promotions}

为了对指定产品类别中的销售和促销活动进行同时分析。`salesAnalysis` 流水线展开 `salesByCategory`，筛选特定类别，并按类别分组以计算 `totalSales` 的总和。促销分析流水线展开促销事件及其折扣，筛选如 `Laptops`、`Smartphones` 等特定类别，并按类别分组以计算平均折扣百分比。来自 `stores` 集合的输入文档仅在操作开始时从数据库中获取一次。

```javascript
db.stores.aggregate([
  {
    $facet: {
      salesAnalysis: [
        { $unwind: "$sales.salesByCategory" },
        { $match: { "sales.salesByCategory.categoryName": { $in: ["Laptops", "Smartphones", "Cameras", "Watches"] } } },
        { $group: { _id: "$sales.salesByCategory.categoryName", totalSales: { $sum: "$sales.salesByCategory.totalSales" } } }
      ],
      promotionAnalysis: [
        { $unwind: "$promotionEvents" },
        { $unwind: "$promotionEvents.discounts" },
        { $match: { "promotionEvents.discounts.categoryName": { $in: ["Laptops", "Smartphones", "Cameras", "Watches"] } } },
        { $group: { _id: "$promotionEvents.discounts.categoryName", avgDiscount: { $avg: "$promotionEvents.discounts.discountPercentage" } } }
      ]
    }
  }
]).pretty()
```

此查询返回以下结果：

```json
[
  {
    "salesAnalysis": [
      { "_id": "Smartphones", "totalSales": 440815 },
      { "_id": "Laptops", "totalSales": 679453 },
      { "_id": "Cameras", "totalSales": 481171 },
      { "_id": "Watches", "totalSales": 492299 }
    ],
    "promotionAnalysis": [
      { "_id": "Smartphones", "avgDiscount": 14.32 },
      { "_id": "Laptops", "avgDiscount": 14.780645161290323 },
      { "_id": "Cameras", "avgDiscount": 15.512195121951219 },
      { "_id": "Watches", "avgDiscount": 15.174418604651162 }
    ]
  }
]
```
