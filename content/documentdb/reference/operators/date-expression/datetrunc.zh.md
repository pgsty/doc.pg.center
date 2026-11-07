---
title: $dateTrunc
description: $dateTrunc 运算符将日期截断到指定单位。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datetrunc.md
weight: 80
translation_source_sha256: 4a86b63ee9135ea05a629af835b602c5bee9b6e84f13a5b4fb0c41942e0c2045
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 简介中“最近”的措辞有歧义。示例明确向下截断到一周的起点，并非舍入到距离最近的边界。

`$dateTrunc` 表达式运算符将日期截断到最近的指定时间单位边界（例如小时、天、月）。在处理时间序列数据或按特定时间间隔对数据分组时，可以使用此运算符，以简化并规范日期计算。

## 语法 {#syntax}

```javascript
  $dateTrunc: {
    date: <dateExpression>,
    unit: "<unit>",
    binSize: <number>,       // optional
    timezone: "<timezone>",  // optional
    startOfWeek: "<day>"     // optional (used when unit is "week")
  }
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`date`** | 要截断的日期。 |
| **`unit`** | 日期截断使用的单位。支持的值包括 `year`、`month`、`week`、`day`、`hour`、`minute`、`second` 和 `millisecond`。 |
| **`binSize`** | （可选）截断时每个时间区间的大小。例如，`binSize` 为 2 且 `unit` 为 `hour` 时，按每 2 小时一个区间截断日期。 |
| **`timezone`** | （可选）截断使用的时区。未指定时默认为 UTC。 |
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

### 示例 1：截断到天 {#example-1-truncate-to-the-day}

此查询使用 `$dateTrunc` 将 `lastUpdated` 时间戳截断到 UTC 当天的起点（00:00:00）。此运算符适合按日历日对数据分组或比较，而不考虑具体时刻。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      truncatedToDay: {
        $dateTrunc: {
          date: "$lastUpdated",
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
    "truncatedToDay": "2024-11-29T00:00:00.000Z"
  }
]
```

### 示例 2：截断到一周的起点 {#example-2-truncate-to-the-start-of-the-week}

此查询使用 `$dateTrunc` 将 `lastUpdated` 时间戳向下取整到所在周的起点，并指定星期一为一周的起始日，以确保日历对齐方式一致。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      truncatedToWeek: {
        $dateTrunc: {
          date: "$lastUpdated",
          unit: "week",
          startOfWeek: "Monday"
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
    "truncatedToWeek": "2024-11-25T00:00:00.000Z"
  }
]
```
