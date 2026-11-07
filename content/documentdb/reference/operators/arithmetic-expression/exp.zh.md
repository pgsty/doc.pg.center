---
title: $exp
description: $exp 运算符计算 e 的指定次幂并返回结果
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$exp.md
weight: 50
translation_source_sha256: 119321270277e959ef512ee82014935eef273c9afe16b3de6795b735a53f29e6
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$exp` 运算符返回 e 的指定次幂。数学常数 e 约等于 2.71828。

## 语法 {#syntax}

```javascript
{
  $exp: <exponent>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<exponent>`** | 任何有效表达式，其结果为数值。 |
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

<span id="example-1-calculate-exponential-growth-rate"></span>

### 示例 1 - 计算商店销售额的指数增长速率 {#example-1---calculate-exponential-growth-rate}

要分别计算某商店总销售额增长 10% 和 20% 的指数增长速率，可使用 $exp 运算符，将 totalSales 字段的值乘以 e^0.1 和 e^0.2。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            currentSales: "$sales.totalSales",
            projectedGrowth: {
                oneYear: {
                    $multiply: [
                        "$sales.totalSales",
                        {
                            $exp: 0.1
                        } // 10% growth rate
                    ]
                },
                twoYears: {
                    $multiply: [
                        "$sales.totalSales",
                        {
                            $exp: 0.2
                        } // 20% growth rate
                    ]
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
    "currentSales": 151864,
    "projectedGrowth": {
      "oneYear": 167809.93,
      "twoYears": 185304.95
    }
  }
]
```
