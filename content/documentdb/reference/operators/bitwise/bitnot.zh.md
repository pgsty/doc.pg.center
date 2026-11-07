---
title: $bitNot
description: $bitNot 运算符对整数值执行按位非运算，并以整数形式返回结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise/$bitnot.md
weight: 20
translation_source_sha256: 558fd72a384b8598d12e2694144006d3e9c2150e81f2e12c200cf8ee46a349b5
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitNot` 运算符对整数值执行按位非运算。它将操作数的所有位取反，把 1 变为 0，把 0 变为 1。结果是输入值按位取反后得到的值。

## 语法 {#syntax}

```javascript
{
  $bitNot: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 求值结果为整数的表达式。`$bitNot` 运算符对该值执行按位非运算。 |
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

### 示例 1：基本的按位非运算 {#example-1-basic-bitwise-not-operation}

此查询对指定商店文档中的员工人数字段按位取反。取反后的值可用于特殊权限标志、功能开关或位掩码操作。14 按位取反的结果为 -15，8 按位取反的结果为 -9。这一结果源于二进制补码表示法，即 ~n = -(n+1)。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "26afb024-53c7-4e94-988c-5eede72277d5"
        }
    },
    {
        $project: {
            name: 1,
            fullTimeStaff: "$staff.totalStaff.fullTime",
            partTimeStaff: "$staff.totalStaff.partTime",
            invertedFullTime: {
                $bitNot: "$staff.totalStaff.fullTime"
            },
            invertedPartTime: {
                $bitNot: "$staff.totalStaff.partTime"
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "fullTimeStaff": 14,
    "partTimeStaff": 8,
    "invertedFullTime": -15,
    "invertedPartTime": -9
  }
]
```

<span id="example-2-using-bit-not-with-discount-percentages"></span>

### 示例 2：对折扣百分比使用 $bitNot {#example-2-using-bitnot-with-discount-percentages}

此查询提取并处理指定商店的折扣信息，对每个折扣百分比执行按位非运算。按位非运算会将所有位取反：20 变为 -21，17 变为 -18。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "26afb024-53c7-4e94-988c-5eede72277d5"
        }
    },
    {
        $unwind: "$promotionEvents"
    },
    {
        $match: {
            "promotionEvents.eventName": "Incredible Savings Showcase"
        }
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $project: {
            name: 1,
            eventName: "$promotionEvents.eventName",
            categoryName: "$promotionEvents.discounts.categoryName",
            discountPercentage: "$promotionEvents.discounts.discountPercentage",
            invertedDiscount: {
                $bitNot: "$promotionEvents.discounts.discountPercentage"
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "eventName": "Incredible Savings Showcase",
    "categoryName": "Microphone Stands",
    "discountPercentage": 17,
    "invertedDiscount": -18
  },
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "eventName": "Incredible Savings Showcase",
    "categoryName": "Condenser Microphones",
    "discountPercentage": 20,
    "invertedDiscount": -21
  }
]
```
