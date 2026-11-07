---
title: $toDate
description: $toDate 运算符将支持的类型转换为正确的 Date 对象。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$todate.md
weight: 350
translation_source_sha256: 54506211c56839d24d5fc1b3680d4d926d0d51f7f911c30f0868005fc106ac88
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$toDate` 运算符将指定的值转换为日期类型。

## 语法 {#syntax}

```javascript
{
  $toDate: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 可以转换为日期的表达式。支持的格式包括：ISO 日期字符串、自 Unix 纪元以来的毫秒数（数字）、ObjectId 和 Timestamp。如果表达式无法转换为日期，该操作将返回错误。 |
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

### 示例 1：将时间戳转换为日期 {#example-1-convert-timestamp-to-date}

要将 lastUpdated 字段的值从 Unix 时间戳转换为日期格式，请使用 $toDate 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "905d1939-e03a-413e-a9c4-221f74055aac"
        }
    },
    {
        $project: {
            name: 1,
            lastUpdated: 1,
            lastUpdatedAsDate: {
                $toDate: "$lastUpdated"
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "lastUpdated": { "t": 1729983325, "i": 1 },
    "lastUpdatedAsDate": ISODate("2024-10-26T22:55:25.000Z")
  }
]
```
