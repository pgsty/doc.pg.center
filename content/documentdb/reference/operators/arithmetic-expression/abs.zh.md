---
title: $abs
description: $abs 运算符返回一个数字的绝对值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$abs.md
weight: 10
translation_source_sha256: 7abfade4f99946814a4a1e220605f1dd52039134416c02f5e927b0dc324dd87a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$abs` 运算符返回一个数字的绝对值。它会移除数字的负号，使其变为正数。

## 语法 {#syntax}

```javascript
{
  $abs: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 任何可解析为数字的表达式。如果表达式为 null 或引用了缺失字段，则 $abs 返回 null。 |
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

<span id="example-1-use-the-absolute-value-of-total-sales"></span>

### 示例 1 - 使用总销售额的绝对值 {#example-1---use-the-absolute-value-of-total-sales}

要计算每个品类的销售额与所有品类平均销售额之间的绝对差值，首先运行查询以筛选特定门店。然后，计算每个品类与所有品类平均销售额之间的差值。最后，使用 $abs 运算符投影绝对差值。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
    }
}, {
    $project: {
        name: 1,
        salesByCategory: {
            $map: {
                input: "$sales.salesByCategory",
                as: "category",
                in: {
                    categoryName: "$$category.categoryName",
                    totalSales: "$$category.totalSales",
                    differenceFromAverage: {
                        $abs: {
                            $subtract: ["$$category.totalSales", {
                                $avg: "$sales.salesByCategory.totalSales"
                            }]
                        }
                    }
                }
            }
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120,
        "differenceFromAverage": 28252.8
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004,
        "differenceFromAverage": 14631.2
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522,
        "differenceFromAverage": 13149.2
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946,
        "differenceFromAverage": 1426.8
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272,
        "differenceFromAverage": 1899.2
      }
    ]
  }
]
```
