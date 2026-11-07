---
title: $dateFromString
description: $dateFromString 运算符将日期／时间字符串转换为日期对象。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datefromstring.md
weight: 40
translation_source_sha256: a178ff18e005d7eb4fc9b4bece83a5fcd33d2110d7aae0b64c3be2fcdd3de65b
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateFromString` 运算符用于将日期／时间字符串转换为日期对象。当需要将字符串表示的日期作为日期对象进行操作或查询时，可以使用此操作。

## 语法 {#syntax}

```javascript
{
    $dateFromString: {
        dateString: < string > ,
        format: < string > ,
        timezone: < string > ,
        onError: < expression > ,
        onNull: < expression >
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateString`** | 要转换为日期对象的日期／时间字符串。 |
| **`format`** | （可选）`dateString` 的日期格式说明。 |
| **`timezone`** | （可选）用于格式化日期的时区。 |
| **`onError`** | （可选）解析 `dateString` 时出错所返回的值。 |
| **`onNull`** | （可选）`dateString` 为 `null` 或缺失时返回的值。 |
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

### 示例 1：将促销活动日期转换为 ISO 日期 {#example-1-convert-promotional-event-dates-to-iso-dates}

此查询使用 `$concat` 将独立的年、月、日字段拼成完整的 ISO 日期字符串，再使用 `$dateFromString` 将其转换为 startDate 和 endDate。当日期分量分开存储在文档中时，可以使用此查询。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $unwind: "$promotionEvents"
  },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      startDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.startDate.Year" },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.startDate.Month", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.startDate.Month" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.startDate.Month" }
                }
              },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.startDate.Day", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.startDate.Day" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.startDate.Day" }
                }
              }
            ]
          }
        }
      },
      endDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.endDate.Year" },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.endDate.Month", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.endDate.Month" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.endDate.Month" }
                }
              },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.endDate.Day", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.endDate.Day" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.endDate.Day" }
                }
              }
            ]
          }
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
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "eventName": "Massive Markdown Mania",
    "startDate": "2024-09-21T00:00:00.000Z",
    "endDate": "2024-09-29T00:00:00.000Z"
  }
]
```
