---
title: $dateSubtract
description: $dateSubtract 运算符从日期中减去指定时长。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datesubtract.md
weight: 50
translation_source_sha256: f1041f47721b3b9db9e10f01b135bb2a660066677dba4622109170aa0e3e0100
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例说明同时提到 `lastUpdated` 和 `storeOpeningDate`，代码则从 `storeOpeningDate` 减去时间间隔。来源正文中的字段名不一致。

`$dateSubtract` 运算符从日期中减去指定的时间单位，适用于在聚合流水线中计算过去的日期或时间间隔。

## 语法 {#syntax}

```javascript
{
  $dateSubtract: {
    startDate: <dateExpression>,
    unit: "<unit>",
    amount: <number>,
    timezone: "<timezone>" // optional
  }
}
```

## 参数 {#parameters}

| 参数       | 描述                                      |
| --------------- | ------------------------------------------------ |
| **`startDate`** | 要从中减去时间的日期表达式。            |
| **`unit`**      | 要减去的时间单位（例如 "day"、"hour"）。 |
| **`amount`**    | 要减去的时间单位数量。         |
| **`timezone`**  | *（可选）* 日期计算使用的时区。      |
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

### 示例 1：减去七天 {#example-1-subtract-seven-days}

此查询计算比 `lastUpdated` 字段早一周的日期。此查询使用 `$dateSubtract` 计算恰好比 `storeOpeningDate` 时间戳早七天的日期。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dateOneWeekAgo: {
        $dateSubtract: {
          startDate: "$storeOpeningDate",
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
    "dateOneWeekAgo": "2024-08-29T11:50:06.549Z"
  }
]
```
