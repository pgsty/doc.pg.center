---
title: $floor
description: $floor 运算符返回小于或等于指定数字的最大整数
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$floor.md
weight: 60
translation_source_sha256: 0dd16aebb5b988bce1071909abd64d8d3a1b1387f500fee2153dc6ed87de3fb6
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$floor` 运算符返回小于或等于指定数字的最大整数。

## 语法 {#syntax}

```javascript
{
  $floor: <number>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 任何有效表达式，其结果为数字。 |
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

<span id="example-1-calculate-the-floor-of-total-sales-and-discounts"></span>

### 示例 1 - 计算总销售额和折扣的下取整值 {#example-1---calculate-the-floor-of-total-sales-and-discounts}

要计算指定商店的平均销售量的下取整值以及各类别的销售量下取整值，请运行使用 $floor 运算符的查询，以返回所需结果。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            averageSalesFloor: {
                $floor: {
                    $divide: [
                        "$sales.totalSales",
                        {
                            $size: "$sales.salesByCategory"
                        }
                    ]
                }
            },
            categoriesWithFloorSales: {
                $map: {
                    input: "$sales.salesByCategory",
                    as: "category",
                    in: {
                        categoryName: "$$category.categoryName",
                        floorSales: {
                            $floor: "$$category.totalSales"
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
    "averageSalesFloor": 30372,
    "categoriesWithFloorSales": [
      {
        "categoryName": "Sound Bars",
        "floorSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "floorSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "floorSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "floorSales": 28946
      },
      {
        "categoryName": "VR Games",
        "floorSales": 32272
      }
    ]
  }
]
```
