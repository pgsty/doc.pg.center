---
title: $isoDayOfWeek
description: $isoDayOfWeek 运算符返回 ISO 8601 格式的星期序号，范围为 1（星期一）到 7（星期日）。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$isodayofweek.md
weight: 130
translation_source_sha256: a2d08bbf92f553bdc4072226b998214fc8abb9166e209c99a76c94c128dad5f7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$isoDayOfWeek` 运算符返回 ISO 8601 格式的星期序号，范围为 1（星期一）到 7（星期日）。此运算符接受求值结果为 Date、Timestamp 或 ObjectId 的日期表达式。

## 语法 {#syntax}

```javascript
{
  $isoDayOfWeek: <dateExpression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateExpression`** | 求值结果为 Date、Timestamp 或 ObjectId 的表达式。若表达式的结果为 null 或缺失，`$isoDayOfWeek` 返回 null。 |
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

### 示例 1：按星期分析促销活动 {#example-1-analyze-promotion-events-by-day-of-week}

此查询检查促销活动，以了解这些活动是在星期几开始的。

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
    $group: {
      _id: { $isoDayOfWeek: "$startDate" },
      eventCount: { $sum: 1 },
      events: { $push: "$eventName" }
    }
  },
  {
    $project: {
      _id: 1,
      dayName: {
        $switch: {
          branches: [
            { case: { $eq: ["$_id", 1] }, then: "Monday" },
            { case: { $eq: ["$_id", 2] }, then: "Tuesday" },
            { case: { $eq: ["$_id", 3] }, then: "Wednesday" },
            { case: { $eq: ["$_id", 4] }, then: "Thursday" },
            { case: { $eq: ["$_id", 5] }, then: "Friday" },
            { case: { $eq: ["$_id", 6] }, then: "Saturday" },
            { case: { $eq: ["$_id", 7] }, then: "Sunday" }
          ]
        }
      },
      eventCount: 1,
      events: 1
    }
  },
  { $sort: { "_id": 1 } }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": 1,
    "eventCount": 1,
    "events": ["Super Sale Spectacular"],
    "dayName": "Monday"
  },
  {
    "_id": 2,
    "eventCount": 1,
    "events": ["Discount Delight Days"],
    "dayName": "Tuesday"
  },
  {
    "_id": 3,
    "eventCount": 1,
    "events": ["Fantastic Deal Days"],
    "dayName": "Wednesday"
  },
  {
    "_id": 4,
    "eventCount": 1,
    "events": ["Massive Markdown Mania"],
    "dayName": "Thursday"
  },
  {
    "_id": 6,
    "eventCount": 1,
    "events": ["Major Bargain Bash"],
    "dayName": "Saturday"
  },
  {
    "_id": 7,
    "eventCount": 1,
    "events": ["Grand Deal Days"],
    "dayName": "Sunday"
  }
]
```
