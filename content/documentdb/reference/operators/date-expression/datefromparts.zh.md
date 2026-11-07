---
title: $dateFromParts
description: $dateFromParts 运算符根据各个分量构造日期。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datefromparts.md
weight: 30
translation_source_sha256: fff32a9221c60a8e27ce5feb46f2202e5868c095d31aaa1a9f663fca830ac4f9
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateFromParts` 运算符根据年、月、日、时、分、秒和毫秒等各个分量构造日期。在处理将日期分量分开存储的数据时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
    $dateFromParts: {
        year: < year > ,
        month: < month > ,
        day: < day > ,
        hour: < hour > ,
        minute: < minute > ,
        second: < second > ,
        millisecond: < millisecond > ,
        timezone: < timezone >
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`year`** | 日期中的年份分量。 |
| **`month`** | 日期中的月份分量。 |
| **`day`** | 日期中的日分量。 |
| **`hour`** | 日期中的小时分量。 |
| **`minute`** | 日期中的分钟分量。 |
| **`second`** | 日期中的秒分量。 |
| **`millisecond`** | 日期中的毫秒分量。 |
| **`timezone`** | 可选。指定时区。 |
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

### 示例 1：构造开始日期 {#example-1-constructing-a-start-date}

此查询使用 `$dateFromParts` 根据嵌套字段构造精确的 startDate 和 endDate 值，然后计算活动持续的天数。它有助于对分散存储的日期分量所表示的活动时间进行标准化和分析。

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
      _id: 1,
      startDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.startDate.Year",
          month: "$promotionEvents.promotionalDates.startDate.Month",
          day: "$promotionEvents.promotionalDates.startDate.Day"
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
    "startDate": "2024-09-21T00:00:00.000Z"
  }
]
```
