---
title: $ceil
description: $ceil 运算符返回大于或等于指定数字的最小整数。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$ceil.md
weight: 30
translation_source_sha256: 63e9df6da32dbd6e09b0e2d3529220c461af61fe0c71610046090d7a50a84a55
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$ceil` 运算符计算输入数字的上取整值。该运算符返回大于或等于输入值的最小整数值。

## 语法 {#syntax}

```javascript
{
  $ceil: <number>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 需要返回其上取整值的输入数字。对于 null 或缺失字段，$ceil 返回 null。 |
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

<span id="example-1-calculate-the-ceiling-of-average-sales-volume-per-employee"></span>

### 示例 1 - 计算每位员工平均销售额的上取整值 {#example-1---calculate-the-ceiling-of-average-sales-volume-per-employee}

要计算每位员工销售额的上取整值，首先运行查询，将门店的总销售额除以员工人数。然后，使用 $ceil 运算符返回计算值的上取整结果。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            totalSales: "$sales.totalSales",
            totalStaff: {
                $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
            },
            ceiledAverageSalesPerStaff: {
                $ceil: {
                    $divide: [
                        "$sales.totalSales",
                        {
                            $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
                        }
                    ]
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
    "totalSales": 151864,
    "totalStaff": 39,
    "ceiledAverageSalesPerStaff": 3894
  }
]
```
