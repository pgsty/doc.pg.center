---
title: $tsSecond
description: $tsSecond 运算符提取时间戳值中的秒数部分。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/timestamp-expression/$tssecond.md
weight: 20
translation_source_sha256: b127729eb0fe957e028261acefe344685e37cc581881841f8e3b79ceb5fd0599
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$tsSecond` 运算符返回时间戳中的秒数值。时间戳由两部分组成：时间值（自纪元起经过的秒数）和增量值。该运算符提取秒数部分，表示自 Unix 纪元（1970 年 1 月 1 日 00:00:00 UTC）起经过的时间。

## 语法 {#syntax}

```javascript
{
  $tsSecond: <expression>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`expression`** | 求值结果为时间戳的表达式。如果表达式的求值结果不是时间戳，`$tsSecond` 会返回错误。 |
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

### 示例 1：从审计时间戳中提取秒数 {#example-1-extract-seconds-from-audit-timestamp}

此查询从审计日志的最后更新时间戳中提取秒数值。

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      lastUpdatedSeconds: {
        $tsSecond: "$lastUpdated"
      },
      lastUpdatedDate: {
        $toDate: {
          $multiply: [
            { $tsSecond: "$lastUpdated" },
            1000
          ]
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
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "lastUpdatedSeconds": Long("1640995200"),
    "lastUpdatedDate": ISODate("2022-01-01T00:00:00.000Z")
  }
]
```
