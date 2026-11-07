---
title: $reduce
description: $reduce 运算符对数组中的每个元素应用表达式，并将结果累积为单个值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$reduce.md
weight: 90
translation_source_sha256: becd30530f2da9ca4257487ddcac3beaa457225aa930fe438dcfa125f61975b8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$reduce` 运算符用于对数组中的每个元素应用表达式，并将结果累积为单个值。该运算符适用于需要遍历数组元素并聚合其值的操作。

## 语法 {#syntax}

```javascript
$reduce: {
   input: <array>,
   initialValue: <expression>,
   in: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 要遍历的数组。 |
| **`initialValue`** | 在数组迭代开始前设置的初始累积值。 |
| **`in`** | 一个有效的表达式，用于计算数组中每个元素的累积值。 |
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

### 示例 1：聚合数组值 {#example-1-aggregates-the-array-values}

此查询演示了如何使用 `$reduce` 来计算 `salesByCategory` 数组中不同类别总销售额的总和。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "988d2dd1-2faa-4072-b420-b91b95cbfd60"
    }
}, {
    $project: {
        totalSalesByCategory: {
            $reduce: {
                input: "$sales.salesByCategory.totalSales",
                initialValue: 0,
                in: {
                    $add: ["$$value", "$$this"]
                }
            }
        }
    }
}])
```

此查询返回以下结果。

```json
[
  {
      "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
      "totalSalesByCategory": 149849
  }
]
```
