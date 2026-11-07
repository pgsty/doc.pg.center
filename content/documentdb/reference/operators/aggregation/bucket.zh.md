---
title: $bucket
description: $bucket 运算符根据指定的边界将输入文档分组到桶中。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$bucket.md
weight: 20
translation_source_sha256: 03d67552377050594881759c04936561814d6648de257528aeaac9c1b2e9a0fc
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$bucket` 流水线阶段根据指定的边界将输入文档分组到桶中。这特别适用于创建直方图或按范围对数据进行分类。该阶段允许你定义自定义的桶边界，并提供了一种汇总这些范围内的数据的方法。

## 语法 {#syntax}

```javascript
{
  $bucket: {
    groupBy: <expression>,
    boundaries: [ <lowerBoundary>, <upperBoundary>, ... ],
    default: <defaultBucket>,
    output: {
      <outputField1>: { <accumulator1> },
      ...
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`groupBy`** | 用于分组文档的表达式。 |
| **`boundaries`** | 定义桶的边界值数组。该数组必须按升序排列，且至少包含两个值。 |
| **`default`** | 用于存放未落入指定边界范围内的文档的桶名称。 |
| **`output`** | 可选字段，用于指定每个桶的计算字段。 |
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

<span id="example-1-categorizing-full-sales-into-ranges"></span>

### 示例 1：将 `fullSales` 按范围 进行分类 {#example-1-categorizing-fullsales-into-ranges}

此查询将 `fullSales` 字段分为三个桶：`[0, 1000)`、`[1000, 5000)` 和 `[5000, 10000)`。未落入这些范围内的文档将被归入默认桶。

```javascript
db.stores.aggregate([
  {
    $bucket: {
      groupBy: "$sales.fullSales",
      boundaries: [0, 1000, 5000, 10000],
      default: "Other",
      output: {
        count: { $sum: 1 },
        totalSales: { $sum: "$sales.fullSales" }
      }
    }
  }
])
```

此查询返回以下结果：

```json
[
  { "_id": 1000, "count": 1, "totalSales": 3700 },
  { "_id": "Other", "count": 41504, "totalSales": 0 }
]
```
