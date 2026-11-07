---
title: $dateAdd
description: $dateAdd 运算符为日期加上指定数量的时间单位（如天、小时、月等）。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$dateadd.md
weight: 10
translation_source_sha256: dd58bd0bd81cc067b535c8b00f3cafd8786083b16e90199ad7e2b70222d2944c
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateAdd` 运算符为日期加上指定数量的时间单位。当需要根据给定日期和时间间隔计算未来日期时，可以使用此运算符。

## 语法 {#syntax}

```javascript
$dateAdd: {
   startDate: <expression>,
   unit: <string>,
   amount: <number>,
   timezone: <string>  // Optional
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`startDate`** | 加法运算的起始日期。 |
| **`unit`** | 要添加的时间单位。有效单位包括：`year`、`quarter`、`month`、`week`、`day`、`hour`、`minute`、`second`、`millisecond`。 |
| **`amount`** | 要添加的单位数量。 |
| **`timezone`** | 可选。此操作使用的时区。 |
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

### 示例 1：为日期加上若干天 {#example-1-adding-days-to-a-date}

此查询投影 `eventName`，并根据嵌套的年、月、日字段构造日期，再加上 7 天，计算出 `newEndDate`。结果是一个简化文档，显示活动名称及延长后的结束日期。

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.promotionalDates" },
  {
    $project: {
      eventName: 1,
      newEndDate: {
        $dateAdd: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.endDate.Year",
              month: "$promotionEvents.promotionalDates.endDate.Month",
              day: "$promotionEvents.promotionalDates.endDate.Day"
            }
          },
          unit: "day",
          amount: 7
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
     "newEndDate": "2024-10-06T00:00:00.000Z"
   }
]
```

### 示例 2：为日期加上若干月 {#example-2-adding-months-to-a-date}

此聚合查询投影 `eventName`，并根据嵌套的促销字段重新构造开始日期，再加上 1 个月，计算出 newStartDate。这样可根据原定日程确定调整后的活动开始日期。此查询返回每个文档的 eventName 和 newStartDate，后者比嵌套促销活动数据中的原始 startDate 晚 1 个月。

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.promotionalDates" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      newStartDate: {
        $dateAdd: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.startDate.Year",
              month: "$promotionEvents.promotionalDates.startDate.Month",
              day: "$promotionEvents.promotionalDates.startDate.Day"
            }
          },
          unit: "month",
          amount: 1
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
     "newStartDate": "2024-10-21T00:00:00.000Z"
   }
]
```
