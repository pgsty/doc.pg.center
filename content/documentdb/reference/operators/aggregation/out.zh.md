---
title: $out
description: 聚合流水线中的 `$out` 流水线阶段将输出文档写入指定的集合。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$out.md
weight: 220
translation_source_sha256: d5935c34d3de2d12800d1214d33450e35ac1e090940eb4d40cfa4f3466cd3a00
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$out` 流水线阶段允许将流水线的输出文档写入指定的集合。该阶段通常用于保存复杂聚合操作的输出结果，以便后续使用或分析。使用时，指定的集合将被创建，或用新文档替换原有内容。

## 语法 {#syntax}

```javascript
{
  $out: "<outputCollection>"
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<outputCollection>`** | 聚合结果将被存储的集合名称。 |
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

<span id="example-1-writing-aggregation-results-to-a-new-collection"></span>

### 示例 1：将聚合结果写入新集合 {#example-1writing-aggregation-results-to-a-new-collection}

此查询将总销售额大于 30,000 的 stores 文档写入名为 `highSales` 的新集合中。

```javascript
db.stores.aggregate([
  {
    $match: {
      "sales.salesByCategory.totalSales": { $gt: 30000 }
    }
  },
  {
    $out: "highSales"
  }
])
```

### 示例 2：将处理后的数据写入另一个集合 {#example-2-writing-processed-data-to-another-collection}

此查询提取促销事件，并将它们写入名为 `promotionEventsSummary` 的集合中。

```javascript
db.stores.aggregate([
  {
    $project: {
      eventName: 1,
      promotionalDates: 1,
      "discounts.categoryName": 1,
      "discounts.discountPercentage": 1
    }
  },
  {
    $out: "promotionEventsSummary"
  }
])
```
