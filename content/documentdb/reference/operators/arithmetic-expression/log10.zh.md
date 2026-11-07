---
title: $log10
description: $log10 运算符计算指定数字以 10 为底的对数
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$log10.md
weight: 90
translation_source_sha256: fa8b578f482e13c8770245df0f3a1107746e48099899184a311178dc074b5bab
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$log10` 运算符计算指定数字以 10 为底的对数，并返回结果。

## 语法 {#syntax}

```javascript
{
  $log10: <number>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 任何解析为正数的有效表达式。 |
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

<span id="example-1-analyze-sales-distribution"></span>

### 示例 1 - 分析销售分布 {#example-1---analyze-sales-distribution}

要对商店内各品类的销售分布进行分桶，可在 totalSales 字段上使用 $log10 运算符执行查询。然后根据结果将品类划入 "Low"、"Medium" 和 "High" 三个桶。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            salesAnalysis: {
                $map: {
                    input: "$sales.salesByCategory",
                    as: "category",
                    in: {
                        categoryName: "$$category.categoryName",
                        originalSales: "$$category.totalSales",
                        logScale: {
                            $log10: "$$category.totalSales"
                        },
                        magnitudeClass: {
                            $switch: {
                                branches: [{
                                        case: {
                                            $lt: [{
                                                $log10: "$$category.totalSales"
                                            }, 3]
                                        },
                                        then: "Low"
                                    },
                                    {
                                        case: {
                                            $lt: [{
                                                $log10: "$$category.totalSales"
                                            }, 4]
                                        },
                                        then: "Medium"
                                    },
                                    {
                                        case: {
                                            $lt: [{
                                                $log10: "$$category.totalSales"
                                            }, 5]
                                        },
                                        then: "High"
                                    }
                                ],
                                default: "Very High"
                            }
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
    "salesAnalysis": [
      {
        "categoryName": "Sound Bars",
        "originalSales": 2120,
        "logScale": 3.326,
        "magnitudeClass": "Medium"
      },
      {
        "categoryName": "Home Theater Projectors",
        "originalSales": 45004,
        "logScale": 4.653,
        "magnitudeClass": "High"
      },
      {
        "categoryName": "Game Controllers",
        "originalSales": 43522,
        "logScale": 4.639,
        "magnitudeClass": "High"
      },
      {
        "categoryName": "Remote Controls",
        "originalSales": 28946,
        "logScale": 4.462,
        "magnitudeClass": "High"
      },
      {
        "categoryName": "VR Games",
        "originalSales": 32272,
        "logScale": 4.509,
        "magnitudeClass": "High"
      }
    ]
  }
]
```
