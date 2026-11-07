---
title: $isoWeek
description: $isoWeek 运算符返回 ISO 8601 格式的年内周编号，范围为 1 到 53。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$isoweek.md
weight: 140
translation_source_sha256: 0295aa58e779ce7c03806d33c1cfa9816b914ad777d053989a57d1aa176134d7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$isoWeek` 运算符返回 ISO 8601 格式的年内周编号，范围为 1 到 53。此运算符接受求值结果为 Date、Timestamp 或 ObjectId 的日期表达式。ISO 8601 规定每周从星期一开始，一年中的第一周是包含该年第一个星期四的那一周。

## 语法 {#syntax}

```javascript
{
  $isoWeek: <dateExpression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateExpression`** | 求值结果为 Date、Timestamp 或 ObjectId 的表达式。若表达式的结果为 null 或缺失，`$isoWeek` 返回 null。 |
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

### 示例 1：获取促销活动的 ISO 周编号 {#example-1-get-iso-week-number-for-promotion-events}

此查询提取促销活动开始日期对应的 ISO 周编号。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      startDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.startDate.Year",
          month: "$promotionEvents.promotionalDates.startDate.Month",
          day: "$promotionEvents.promotionalDates.startDate.Day"
        }
      }
    }
  },
  {
    $project: {
      eventName: 1,
      startDate: 1,
      isoWeekNumber: { $isoWeek: "$startDate" },
      year: { $year: "$startDate" }
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Massive Markdown Mania",
    "startDate": "2023-06-29T00:00:00.000Z",
    "isoWeekNumber": 26,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Fantastic Deal Days",
    "startDate": "2023-09-27T00:00:00.000Z",
    "isoWeekNumber": 39,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "startDate": "2023-12-26T00:00:00.000Z",
    "isoWeekNumber": 52,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Super Sale Spectacular",
    "startDate": "2024-03-25T00:00:00.000Z",
    "isoWeekNumber": 13,
    "year": 2024
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Grand Deal Days",
    "startDate": "2024-06-23T00:00:00.000Z",
    "isoWeekNumber": 25,
    "year": 2024
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Major Bargain Bash",
    "startDate": "2024-09-21T00:00:00.000Z",
    "isoWeekNumber": 38,
    "year": 2024
  }
]
```
