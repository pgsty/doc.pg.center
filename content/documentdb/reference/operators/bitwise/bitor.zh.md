---
title: $bitOr
description: $bitOr 运算符对整数值执行按位或运算，并以整数形式返回结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise/$bitor.md
weight: 30
translation_source_sha256: 14da089e86badbde1eb840cccbf8ca869bd70957a3f681a16ef517344463c897
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitOr` 运算符对整数值执行按位或运算。它将第一个操作数的每一位与第二个操作数的对应位进行比较。只要任意一位为 1，结果中的对应位就设为 1；若两位均为 0，则设为 0。

## 语法 {#syntax}

```javascript
{
  $bitOr: [ <expression1>, <expression2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression1, expression2, ...`** | 求值结果为整数的表达式。`$bitOr` 运算符对所有给定表达式的结果执行按位或运算。 |
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

### 示例 1：基本的按位或运算 {#example-1-basic-bitwise-or-operation}

此查询对指定商店文档中的员工人数值执行按位或运算，以合并权限标志。3（二进制为 011）与 2（二进制为 010）按位或的结果为 3（二进制为 011）。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66"
        }
    },
    {
        $project: {
            name: 1,
            fullTimeStaff: "$staff.totalStaff.fullTime",
            partTimeStaff: "$staff.totalStaff.partTime",
            combinedStaffFlag: {
                $bitOr: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
    "fullTimeStaff": 3,
    "partTimeStaff": 2,
    "combinedStaffFlag": 3
  }
]
```

### 示例 2：对多个折扣百分比值执行按位或运算 {#example-2-multiple-value-bitwise-or-with-discount-percentages}

此查询提取指定促销活动的折扣详情，并计算一个结合折扣与员工人数值的位标志。输出展示了聚合查询的结果：为 `Super Saver Spectacular` 活动中的每项折扣计算一个组合位标志。此操作通过按位或运算合并折扣百分比与员工人数：7|3|2 = 7，11|3|2 = 11。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66"
        }
    },
    {
        $unwind: "$promotionEvents"
    },
    {
        $match: {
            "promotionEvents.eventName": "Super Saver Spectacular"
        }
    },
    {
        $project: {
            name: 1,
            eventName: "$promotionEvents.eventName",
            discountFlags: {
                $map: {
                    input: "$promotionEvents.discounts",
                    as: "discount",
                    in: {
                        categoryName: "$$discount.categoryName",
                        discountPercentage: "$$discount.discountPercentage",
                        combinedFlag: {
                            $bitOr: [
                                "$$discount.discountPercentage",
                                "$staff.totalStaff.fullTime",
                                "$staff.totalStaff.partTime"
                            ]
                        }
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
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
    "eventName": "Super Saver Spectacular",
    "discountFlags": [
      {
        "categoryName": "Car Chargers",
        "discountPercentage": 7,
        "combinedFlag": 7
      },
      {
        "categoryName": "Dash Cameras",
        "discountPercentage": 11,
        "combinedFlag": 11
      }
    ]
  }
]
```
