---
title: $divide
description: $divide 运算符将两个数字相除并返回商。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$divide.md
weight: 40
translation_source_sha256: 62282032892367080a4bfe7e6fefb64ff16e5d1fcc3bb3c54fdd581e357137d8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$divide` 运算符将两个数字相除并返回商。如果除数为零，$divide 运算符将返回错误。

## 语法 {#syntax}

```javascript
{
  $divide: [ <dividend>, <divisor> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<dividend>`** | 任何有效表达式，其结果为待除的数字。 |
| **`<divisor>`** | 任何有效表达式，其结果为非零数字，用作除数。 |
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

<span id="example-1-calculate-the-average-sales-volume-per-employee"></span>

### 示例 1 - 计算每位员工的平均销售额 {#example-1---calculate-the-average-sales-volume-per-employee}

要计算每位员工的平均销售额，首先使用 $divide 运算符运行查询，将总销售额除以员工人数。要计算全职员工所占百分比，使用 $divide 运算符将全职员工人数除以总员工人数，并将结果投影为百分比形式。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            averageSalesPerStaff: {
                $divide: [
                    "$sales.totalSales",
                    {
                        $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
                    }
                ]
            },
            fullTimeStaffPercentage: {
                $multiply: [{
                    $divide: [
                        "$staff.totalStaff.fullTime",
                        {
                            $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
                        }
                    ]
                }, 100]
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
    "averageSalesPerStaff": 3893.95,
    "fullTimeStaffPercentage": 48.72
  }
]
```
