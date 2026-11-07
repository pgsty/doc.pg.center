---
title: $sqrt
description: $sqrt 运算符计算并返回输入数字的平方根
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$sqrt.md
weight: 130
translation_source_sha256: 5684d6c044e2a83932ffe4ad2e9222ec5c25a48586ee23c2f088f65f4bcc7334
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$sqrt` 运算符用于计算指定数字的平方根。

## 语法 {#syntax}

```javascript
{
  $sqrt: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 任何有效表达式，其结果为数字。 |
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

### 示例 1：计算销售额的平方根 {#example-1-calculate-the-square-root-of-sales}

要计算 "First Up Consultants" 公司下每个门店的销售额的平方根，首先运行查询以按公司名称筛选门店。然后，在 totalSales 字段上使用 $sqrt 运算符，以获取所需结果。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $project: {
        name: 1,
        "sales.revenue": 1,
        categoryName: "$promotionEvents.discounts.categoryName",
        sqrtFullSales: {
            $sqrt: "$sales.revenue"
        }
    }
}])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "c52c9f65-5b1a-4ef5-a7a2-d1af0426cbe4",
        "name": "First Up Consultants | Jewelry Pantry - Nicolasberg",
        "sales": {
            "revenue": 4624
        },
        "categoryName": [
            [
                "Watches",
                "Bracelets"
            ],
            [
                "Brooches",
                "Necklaces"
            ],
            [
                "Charms",
                "Brooches"
            ],
            [
                "Brooches",
                "Anklets"
            ],
            [
                "Earrings",
                "Anklets"
            ]
        ],
        "sqrtFullSales": 68
    },
    {
        "_id": "176aa484-c21c-44ce-ab6d-5e097bbdc2b4",
        "name": "First Up Consultants | Medical Supply Shop - Daughertyville",
        "sales": {
            "revenue": 67311
        },
        "categoryName": [
            [
                "First Aid Kits",
                "OTC Medications"
            ],
            [
                "Blood Pressure Monitors",
                "OTC Medications"
            ],
            [
                "Face Masks",
                "Stethoscopes"
            ]
        ],
        "sqrtFullSales": 259.44363549719236
    }
]
```
