---
title: $median
description: $median 运算符计算一组文档中数值字段的中位数。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/operators/accumulators/$median.md
weight: 110
translation_source_sha256: 452ab29270d01b9c3e1ebdb9901546eb60bbc770644c7b6553fffc536c086523
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$median` 累加器运算符计算一组文档中数值字段的中位数。

## 语法 {#syntax}

```javascript
{
    $group: {
        _id: < expression > ,
        medianValue: {
            $median: {
                input: < field or expression > ,
                method: < >
            }
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field or expression>`** | 用于计算中位数的字段或表达式。 |
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

### 示例 1：计算中位数销售量 {#example-1-calculate-the-median-sales-volume}

要计算每个类别内的中位数销售量，首先按不同的销售类别对文档进行分组，然后计算每组类别内的中位数销售量。

```javascript
db.stores.aggregate([{
    $unwind: "$sales.salesByCategory"
}, {
    $group: {
        _id: "$sales.salesByCategory.categoryName",
        medianSales: {
            $median: {
                "input": "$sales.salesByCategory.totalSales",
                "method": "approximate"
            }
        }
    }
}])
```

此查询返回的前五个结果如下：

```json
[
    {
        "_id": "Light Bulbs",
        "medianSales": 24845
    },
    {
        "_id": "Christmas Trees",
        "medianSales": 28210
    },
    {
        "_id": "Ukuleles",
        "medianSales": 27295
    },
    {
        "_id": "GPUs",
        "medianSales": 19813
    },
    {
        "_id": "Towels",
        "medianSales": 27771
    }
]
```
