---
title: $month
description: $month 运算符从日期值中提取月份分量。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$month.md
weight: 180
translation_source_sha256: 32196982b361d747f4afdfc5d9417cee4a7f28bc4042a87111caad33a4ce5700
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$month` 运算符从日期值中提取月份分量，返回 1 到 12 之间的数字，其中 1 表示一月，12 表示十二月。此运算符对于季节性分析和月度报表十分重要。

## 语法 {#syntax}

```javascript
{
  $month: <dateExpression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateExpression`** | 求值结果为 Date、Timestamp 或 ObjectId 的表达式。若表达式的结果为 `null` 或缺失，`$month` 返回 `null`。 |
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

### 示例 1：从商店开业日期中提取月份分量 {#example-1-extract-month-from-store-opening-date}

此查询从商店开业日期中提取月份分量，以分析开业日期的季节性规律。

```javascript
db.stores.aggregate([
  { $match: {_id: "905d1939-e03a-413e-a9c4-221f74055aac"} },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingMonth: {
        $month: "$storeOpeningDate"
      },
      openingMonthName: {
        $switch: {
          branches: [
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 1] }, then: "January" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 2] }, then: "February" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 3] }, then: "March" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 4] }, then: "April" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 5] }, then: "May" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 6] }, then: "June" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 7] }, then: "July" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 8] }, then: "August" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 9] }, then: "September" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 10] }, then: "October" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 11] }, then: "November" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 12] }, then: "December" }
          ]
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
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "storeOpeningDate": "2024-12-30T22:55:25.779Z",
    "openingMonth": 12,
    "openingMonthName": "December"
  }
]
```
