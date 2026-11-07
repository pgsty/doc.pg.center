---
title: $dateToParts
description: $dateToParts 运算符将日期拆分为年、月、日等各个分量。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datetoparts.md
weight: 60
translation_source_sha256: 2a181328f59b29aa0c290aa694cfa7f47a8632b28adf8b34f9dc9191de4367ee
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateToParts` 运算符用于从日期对象中提取各个分量（年、月、日、时、分、秒、毫秒等）。当需要操作或分析特定日期分量时，可以使用此运算符，例如根据单个日期分量对数据排序、筛选或聚合。

## 语法 {#syntax}

```javascript
$dateToParts: {
  date: <dateExpression>,
  timezone: <string>, // optional
  iso8601: <boolean> // optional
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`date`** | 要从中提取各分量的日期表达式。 |
| **`timezone`** | 可选。指定日期的时区。未提供时默认为 UTC。 |
| **`iso8601`** | 可选。为 true 时，此运算符使用 ISO 8601 周日期历法。默认为 false。 |
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

### 示例 1：从字段中提取日期分量 {#example-1-extracting-date-parts-from-a-field}

此查询使用 `$dateToParts` 将 `lastUpdated` 日期拆分为年、月、日及时间等分量，便于分析或转换日期的各个分量，以供后续处理。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dateParts: {
        $dateToParts: { 
          date: "$lastUpdated" 
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
    "dateParts": {
      "year": 2024,
      "month": 12,
      "day": 4,
      "hour": 11,
      "minute": 50,
      "second": 6,
      "millisecond": 0
    }
  }
]
```

### 示例 2：使用时区 {#example-2-using-timezone}

此查询提取指定文档的 `lastUpdated` 时间戳，并使用 $dateToParts 将其拆分为年、月、日、小时等日期分量。指定 "America/New_York" 时区后，拆分结果反映的是当地时间，而非 UTC。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      datePartsWithTimezone: {
        $dateToParts: { 
          date: "$lastUpdated", 
          timezone: "America/New_York" 
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
    "datePartsWithTimezone": {
      "year": 2024,
      "month": 12,
      "day": 4,
      "hour": 6,
      "minute": 50,
      "second": 6,
      "millisecond": 0
    }
  }
]
```
