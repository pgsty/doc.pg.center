---
title: $year
description: $year 运算符返回日期对应的年份，格式为四位数字。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$year.md
weight: 210
translation_source_sha256: 99055673184f8ea03fc78bbaf56def7f3c7f7d3e1cebc0673189449e6c2dc44f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$year` 运算符返回日期对应的年份，格式为四位数字（例如 2024）。如果日期为 null 或缺失，`$year` 返回 null。

## 语法 {#syntax}

`$year` 运算符的语法如下：

```javascript
{
  $year: <dateExpression>
}
```

也可以指定时区：

```javascript
{
  $year: {
    date: <dateExpression>,
    timezone: <timezoneExpression>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`dateExpression`** | 求值结果为 Date、Timestamp 或 ObjectId 的任意表达式。 |
| **`timezone`** | 可选。计算使用的时区，可以是 Olson 时区标识符（例如 "America/New_York"），也可以是 UTC 偏移量（例如 "+0530"）。 |
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

### 示例 1：从商店开业日期中提取年份 {#example-1-extract-year-from-store-opening-date}

此查询提取商店开业的年份。

```javascript
db.stores.aggregate([
  { $match: { _id: "905d1939-e03a-413e-a9c4-221f74055aac" } },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingYear: { $year: { $toDate: "$storeOpeningDate" } }
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
    "openingYear": 2024
  }
]
```

### 示例 2：查找在指定年份开业的商店 {#example-2-find-stores-opened-in-specific-year}

此查询获取 2021 年开业的所有商店。

```javascript
db.stores.aggregate([
  {
    $match: {
      $expr: {
        $eq: [{ $year: { $toDate: "$storeOpeningDate" } }, 2021]
      }
    }
  },
  {
    $project: {
      name: 1,
      city: 1,
      openingYear: { $year: { $toDate: "$storeOpeningDate" } },
      storeOpeningDate: 1
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "city": "South Amir",
    "storeOpeningDate": "2021-10-03T00:00:00.000Z",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "openingYear": 2021
  }
]
```
