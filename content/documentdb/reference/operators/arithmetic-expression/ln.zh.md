---
title: $ln
description: $ln 运算符计算输入的自然对数
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$ln.md
weight: 70
translation_source_sha256: 3f92ea12ee3777fceb52dde9d30bec0a78ec11f19ebd1f6add6ab252b186133d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$ln` 运算符计算输入数字的自然对数（以 e 为底）。

## 语法 {#syntax}

```javascript
{
  $ln: <number>
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

<span id="example-1-calculate-the-natural-logarithm-of-total-sales-by-category"></span>

### 示例 1 - 按类别计算总销售额的自然对数 {#example-1---calculate-the-natural-logarithm-of-total-sales-by-category}

要计算按类别划分的销售量的自然对数以分析增长率，请在 totalSales 字段上使用 $ln 运算符运行查询，以返回所需结果。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            salesGrowthMetrics: {
                $map: {
                    input: "$sales.salesByCategory",
                    as: "category",
                    in: {
                        categoryName: "$$category.categoryName",
                        salesValue: "$$category.totalSales",
                        naturalLog: {
                            $ln: "$$category.totalSales"
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
    "salesGrowthMetrics": [
      {
        "categoryName": "Sound Bars",
        "salesValue": 2120,
        "naturalLog": 7.659
      },
      {
        "categoryName": "Home Theater Projectors",
        "salesValue": 45004,
        "naturalLog": 10.714
      },
      {
        "categoryName": "Game Controllers",
        "salesValue": 43522,
        "naturalLog": 10.681
      },
      {
        "categoryName": "Remote Controls",
        "salesValue": 28946,
        "naturalLog": 10.273
      },
      {
        "categoryName": "VR Games",
        "salesValue": 32272,
        "naturalLog": 10.382
      }
    ]
  }
]
```
