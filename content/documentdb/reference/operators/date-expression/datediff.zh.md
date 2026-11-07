---
title: $dateDiff
description: $dateDiff 运算符以年、月、天等不同单位计算两个日期之间的差值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datediff.md
weight: 20
translation_source_sha256: 9ba4901e101fb3a6e262f0a1bf882151327cdaa31447cb30a7cf3127c71a652c
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateDiff` 运算符以年、月、天等不同单位计算两个日期之间的差值，可用于确定数据集中两个时间戳之间的时长。

## 语法 {#syntax}

```javascript
$dateDiff: {
   startDate: <expression>,
   endDate: <expression>,
   unit: <string>,
   timezone: <string>, // Optional
   startOfWeek: <string> // Optional
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`startDate`**| 计算的起始日期。|
| **`endDate`**| 计算的结束日期。|
| **`unit`**| 用于度量差值的时间单位。有效值包括：`year`、`quarter`、`month`、`week`、`day`、`hour`、`minute`、`second`、`millisecond`。|
| **`timezone`**| 可选。计算使用的时区。|
| **`startOfWeek`**| 可选。一周的起始日。有效值为：`Sunday`、`Monday`、`Tuesday`、`Wednesday`、`Thursday`、`Friday`、`Saturday`。|
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

## 示例 1：计算两个日期之间的天数 {#example-1-calculate-duration-in-days-between-two-dates}

此查询使用 `$dateDiff` 计算两个日期字段之间相差的单位数量（例如天数、月数），可用于度量活动持续时间或自给定日期起经过的时长。此查询返回指定 `stores` 文档的 durationInDays 及其他字段。

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
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
      },
      durationInDays: {
        $dateDiff: {
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
          },
          unit: "day"
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
     "endDate": "2024-09-29T00:00:00.000Z",
     "durationInDays": 8
   }
]
```
