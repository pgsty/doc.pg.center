---
title: $log
description: $log 运算符计算一个数以指定底数为底的对数
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$log.md
weight: 80
translation_source_sha256: cf5eeac0f29d8799472bba8a8607402f511ceb6a81dffb60c3eec582d8e290e6
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$log` 运算符计算一个数以指定底数为底的对数。

## 语法 {#syntax}

```javascript
{
  $log: [ <number>, <base> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 任何有效表达式，其结果为正数。 |
| **`<base>`** | 任何有效表达式，其结果为正数，用作对数的底数。 |
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

<span id="example-1-calculate-the-log-of-total-sales"></span>

### 示例 1 - 计算总销售额的对数 {#example-1---calculate-the-log-of-total-sales}

要计算按类别划分的销售额在底数为 2 和 10 时的对数，可对 totalSales 字段分别使用 $log 运算符并指定底数 2 和 10，以返回所需结果。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            categoryAnalysis: {
                $map: {
                    input: "$sales.salesByCategory",
                    as: "category",
                    in: {
                        categoryName: "$$category.categoryName",
                        sales: "$$category.totalSales",
                        logBase2: {
                            $log: ["$$category.totalSales", 2]
                        },
                        logBase10: {
                            $log: ["$$category.totalSales", 10]
                        }
                    }
                }
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "categoryAnalysis": [
      {
        "categoryName": "Sound Bars",
        "sales": 2120,
        "logBase2": 11.051,
        "logBase10": 3.326
      },
      {
        "categoryName": "Home Theater Projectors",
        "sales": 45004,
        "logBase2": 15.458,
        "logBase10": 4.653
      },
      {
        "categoryName": "Game Controllers",
        "sales": 43522,
        "logBase2": 15.410,
        "logBase10": 4.639
      },
      {
        "categoryName": "Remote Controls",
        "sales": 28946,
        "logBase2": 14.822,
        "logBase10": 4.462
      },
      {
        "categoryName": "VR Games",
        "sales": 32272,
        "logBase2": 14.977,
        "logBase10": 4.509
      }
    ]
  }
]
```
