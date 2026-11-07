---
title: $zip
description: $zip 运算符可将两个或更多数组中的对应元素合并为一个数组或多个数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$zip.md
weight: 130
translation_source_sha256: d51b571060fa87ac2b2a0b6e10a875611677d479fc5eb15ac03b43b851e6042a
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 上游摘要写的是“数组或多个数组”，而定义和示例描述的是“由数组组成的数组”。应结合正文理解摘要。

`$zip` 运算符用于将两个或更多数组中对应位置的元素逐一合并为一个由数组组成的数组。当需要将多个数组中的相关元素合并到同一个数组结构中时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $zip: {
    inputs: [ <array1>, <array2>, ... ],
    useLongestLength: <boolean>, // Optional
    defaults: <array> // Optional
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`inputs`** | 由多个数组组成的数组；这些数组将按对应位置逐一合并元素。 |
| **`useLongestLength`** | 布尔值。设为 true 时，使用输入数组中的最长长度；设为 false 或未指定时，使用最短长度。 |
| **`defaults`** | 默认值数组，当 `useLongestLength` 为 true 且某个输入数组短于最长数组时使用。 |
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

### 示例 1：基本用法 {#example-1-basic-usage}

假设要合并 `salesByCategory` 数组中的 `categoryName` 和 `totalSales` 字段。此查询在 `categoryWithSales` 字段中返回一个由数组组成的数组。将 `useLongestLength` 设为 `true` 时，会返回以下输出；设为 `false` 时，则会从输出中移除 `Napkins` 数组。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"
        }
    },
    {
        $project: {
            name: 1,
            categoryNames: "$sales.salesByCategory.categoryName",
            totalSales: "$sales.salesByCategory.totalSales",
            categoryWithSales: {
                $zip: {
                    inputs: ["$sales.salesByCategory.categoryName", "$sales.salesByCategory.totalSales"],
                    useLongestLength: false
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
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "categoryNames": ["Stockings"],
    "totalSales": [25731],
    "categoryWithSales": [["Stockings", 25731]]
  }
]
```
