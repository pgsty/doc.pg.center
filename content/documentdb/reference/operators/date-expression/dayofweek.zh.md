---
title: $dayOfWeek
description: $dayOfWeek 运算符从日期中提取星期序号。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$dayofweek.md
weight: 100
translation_source_sha256: 3e54bc1f95925d39a00371f44a58516d31d0c8f9fa892c786c3d708a9a750f06
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例将星期日为 1、星期六为 7 误称为 ISO-8601 顺序。本页 `$dayOfWeek` 的编号方式，与 `$isoDayOfWeek` 页面描述的星期一为 1、星期日为 7 不同。

`$dayOfWeek` 运算符从日期值中提取星期序号，其中 1 表示星期日，7 表示星期六。它可用于按星期对文档分组或筛选。

## 语法 {#syntax}

```javascript
{
  $dayOfWeek: <dateExpression>
}
```

## 参数 {#parameters}

| 参数              | 描述                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **`<dateExpression>`** | 要从中提取星期序号的日期表达式。 |
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

### 示例 1：提取星期序号 {#example-1-extract-day-of-the-week}

此查询使用 `$dayOfWeek` 运算符从 `lastUpdated` 时间戳中提取星期序号。返回值范围为 1（星期日）到 7（星期六），采用 ISO-8601 排序。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dayOfWeek: { $dayOfWeek: "$lastUpdated" }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "dayOfWeek": "4"
  }
]
```
