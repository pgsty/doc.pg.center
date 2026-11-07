---
title: $isoWeekYear
description: $isoWeekYear 运算符返回 ISO 8601 格式的年份；对于年初或年末的日期，该年份可能与日历年不同。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$isoweekyear.md
weight: 150
translation_source_sha256: cccc17380014d04603bbe3e7945b083466a0f35cf38d42e12e71ec8b56cb8918
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$isoWeekYear` 运算符返回 ISO 8601 格式的年份。对于年初或年末的日期，ISO 周编号年份可能与日历年不同。ISO 周编号年份是该日期所在周的星期四所属的年份。

## 语法 {#syntax}

```javascript
{
  $isoWeekYear: <dateExpression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateExpression`** | 求值结果为 Date、Timestamp 或 ObjectId 的表达式。若表达式的结果为 null 或缺失，`$isoWeekYear` 返回 null。 |
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

### 示例 1：比较日历年与 ISO 周编号年份 {#example-1-compare-calendar-year-vs-iso-week-year}

此查询演示日历年与 ISO 周编号年份的区别，尤其是年初年末附近的日期。

```javascript
db.stores.aggregate([
  { $match: {_id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
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
      },
      endDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.endDate.Year",
          month: "$promotionEvents.promotionalDates.endDate.Month",
          day: "$promotionEvents.promotionalDates.endDate.Day"
        }
      }
    }
  },
  {
    $project: {
      eventName: 1,
      startDate: 1,
      endDate: 1,
      startCalendarYear: { $year: "$startDate" },
      startISOWeekYear: { $isoWeekYear: "$startDate" },
      endCalendarYear: { $year: "$endDate" },
      endISOWeekYear: { $isoWeekYear: "$endDate" },
      yearDifference: {
        $ne: [{ $year: "$startDate" }, { $isoWeekYear: "$startDate" }]
      }
    }
  },
  { $match: {"eventName": "Discount Delight Days" } }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "startDate": "2023-12-26T00:00:00.000Z",
    "endDate": "2024-01-05T00:00:00.000Z",
    "startCalendarYear": 2023,
    "startISOWeekYear": Long("2023"),
    "endCalendarYear": 2024,
    "endISOWeekYear": Long("2024"),
    "yearDifference": true
  }
]
```
