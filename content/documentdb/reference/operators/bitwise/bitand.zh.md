---
title: $bitAnd
description: $bitAnd 运算符对整数值执行按位与运算，并以整数形式返回结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise/$bitand.md
weight: 10
translation_source_sha256: 7e35ca0808a1bd0d58470421c3c2c7f1a87204659d4cd05c913db20dca7f76ce
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitAnd` 运算符对整数值执行 `bitwise AND` 运算。它将第一个操作数的每一位与第二个操作数的对应位进行比较。若两位均为 1，结果中的对应位就设为 1；否则设为 0。

## 语法 {#syntax}

```javascript
{
  $bitAnd: [ <expression1>, <expression2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression1, expression2, ...`** | 求值结果为整数的表达式。`$bitAnd` 运算符对所有给定表达式的结果执行按位与运算。 |
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

### 示例 1：基本的按位与运算 {#example-1-basic-bitwise-and-operation}

此查询获取指定商店的员工信息，并对全职与兼职员工人数执行 `bitwise AND` 运算，以创建权限标志。

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
            staffPermissionFlag: {
                $bitAnd: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
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
    "staffPermissionFlag": 16
  }
]
```

<span id="example-2-multiple-value-bit-and"></span>

### 示例 2：对多个值使用 `$bitAnd` {#example-2-multiple-value-bitand}

此查询根据单个商店的多个数值字段，检查以位表示的权限或组合标志。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            combinedFlag: {
                $bitAnd: [
                    "$staff.totalStaff.fullTime",
                    "$staff.totalStaff.partTime",
                    255
                ]
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
    "combinedFlag": 16
  }
]
```
