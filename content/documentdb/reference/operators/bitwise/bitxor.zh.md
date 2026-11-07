---
title: $bitXor
description: $bitXor 运算符对整数值执行按位异或运算。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise/$bitxor.md
weight: 40
translation_source_sha256: 92d87dc8c5a5f7afd5d42df96e0bcc53dae9e15cc5ae3a12cc8eca611028be3d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitXor` 运算符对整数值执行按位异或（XOR）运算。对于每个位，若操作数的对应位不同，异或运算返回 1；若相同，则返回 0。

## 语法 {#syntax}

```javascript
{
  $bitXor: [ <expression1>, <expression2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression1, expression2, ...`** | 求值结果为整数的表达式。此运算符依次对这些值执行异或运算。 |
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

### 示例 1：基本的异或运算 {#example-1-basic-xor-operation}

此查询使用聚合流水线，对指定商店的全职与兼职员工人数进行计算。结果文档包含商店详情和一个计算得出的字段。19（二进制为 10011）与 20（二进制为 10100）异或的结果为 7（二进制为 00111）。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            fullTimeStaff: "$staff.totalStaff.fullTime",
            partTimeStaff: "$staff.totalStaff.partTime",
            staffXor: {
                $bitXor: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "fullTimeStaff": 19,
    "partTimeStaff": 20,
    "staffXor": 7
  }
]
```

### 示例 2：对多个值执行异或运算 {#example-2-xor-with-multiple-values}

此查询计算指定商店的 `Discount Delight Days` 活动中所有折扣百分比的按位异或结果。结果文档表示 `Discount Delight Days` 活动中所有折扣百分比的按位异或计算结果。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $unwind: "$promotionEvents"
    },
    {
        $match: {
            "promotionEvents.eventName": "Discount Delight Days"
        }
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $group: {
            _id: "$_id",
            name: {
                $first: "$name"
            },
            eventName: {
                $first: "$promotionEvents.eventName"
            },
            discountPercentages: {
                $push: "$promotionEvents.discounts.discountPercentage"
            }
        }
    },
    {
        $project: {
            name: 1,
            eventName: 1,
            discountPercentages: 1,
            xorResult: {
                $reduce: {
                    input: {
                        $map: {
                            input: "$discountPercentages",
                            as: "val",
                            in: {
                                $toLong: "$$val"
                            }
                        }
                    },
                    initialValue: {
                        $toLong: 0
                    },
                    in: {
                        $bitXor: ["$$value", "$$this"]
                    }
                }
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "eventName": "Discount Delight Days",
    "discountPercentages": [22, 23, 10, 10, 9, 24],
    "xorResult": { "$numberLong": "16" }
  }
]
```
