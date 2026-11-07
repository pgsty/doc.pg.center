---
title: $subtract
description: $subtract 运算符对两个数字进行相减并返回结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$subtract.md
weight: 140
translation_source_sha256: 6d294219567b3e3251b56da833bbd078fcb3a1ce639906764e64b1343f61a35e
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例说明写的是 `$diff`，而代码将 `$subtract` 与 `$abs` 配合使用。正文保留了来源中的拼写。

`$subtract` 运算符用于对两个数字进行相减并返回结果。

## 语法 {#syntax}

```javascript
{
  $subtract: [ <expression 1>, <expression 2> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression 1>`** | 被减数（即从其中减去另一个数的数）。 |
| **`<expression 2>`** | 减数（即要被减去的数）。 |
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

### 示例 1：计算全职与兼职员工人数的差值 {#example-1-calculating-the-difference-between-full-time-and-part-time-staff}

要计算 "First Up Consultants" 公司旗下各门店全职与兼职员工人数的绝对差值，首先运行查询以按公司名称筛选门店。然后，使用 $diff 运算符结合 $abs 运算符，计算每家门店全职与兼职员工人数的绝对差值。

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
        staff: 1,
        staffCountDiff: {
            $abs: {
                $subtract: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"]
            }
        }
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "name": "First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort",
        "staff": {
            "employeeCount": {
                "fullTime": 20,
                "partTime": 18
            }
        },
        "staffCountDiff": 2
    },
    {
        "_id": "bfb213fa-8db8-419f-8e5b-e7096120bad2",
        "name": "First Up Consultants | Beauty Product Shop - Hansenton",
        "staff": {
            "employeeCount": {
                "fullTime": 18,
                "partTime": 10
            }
        },
        "staffCountDiff": 8
    },
    {
        "_id": "14ab145b-0819-4d22-9e02-9ae0725fcda9",
        "name": "First Up Consultants | Flooring Haven - Otisville",
        "staff": {
            "employeeCount": {
                "fullTime": 19,
                "partTime": 10
            }
        },
        "staffCountDiff": 9
    }
]
```
