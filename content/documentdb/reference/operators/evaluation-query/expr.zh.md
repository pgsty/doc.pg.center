---
title: $expr
description: $expr 运算符允许在查询语言中使用聚合表达式，实现复杂的字段比较和计算。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/evaluation-query/$expr.md
weight: 10
translation_source_sha256: 8867324acf53cd432aba85995b15fbf83bfd36d84b741fd41a534f667749ef0d
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例前后的两处说明给出了相反的比较方向。代码实际检查的是兼职人数是否大于全职人数。

`$expr` 运算符允许在查询语言中使用聚合表达式，从而比较同一文档中的字段、执行计算，以及在 find 操作中使用聚合运算符。`$expr` 运算符适用于传统查询运算符无法实现的复杂字段比较。

## 语法 {#syntax}

```javascript
{
  $expr: { <aggregation expression> }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<aggregation expression>`** | 任意求值结果为布尔值的有效聚合表达式。表达式可以包含字段比较、算术运算、条件表达式以及其他聚合运算符。 |
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

### 示例 1：比较全职与兼职员工人数 {#example-1-compare-full-time-and-part-time-staff}

此示例检索兼职员工人数多于全职员工人数的商店。

```javascript
db.stores.find({_id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  $expr: {
    $gt: ["$staff.employeeCount.partTime", "$staff.employeeCount.fullTime"]
  }
})
```

此查询比较指定文档（`_id`）中的两个字段，仅在满足条件（全职员工人数多于兼职员工人数）时返回该文档。

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
      "contractorCount": 5,
      "employeeCount": { "fullTime": 19, "partTime": 20 }
    },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    },
    "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
    "lastUpdated": ISODate("2025-06-11T11:06:57.922Z"),
    "status": "active",
    "category": "high-volume",
    "priority": 1,
    "reviewDate": ISODate("2025-06-11T11:10:50.276Z")
  }
]
```

### 示例 2：结合商店位置使用条件逻辑 {#example-2-conditional-logic-with-store-location}

此示例演示如何使用 `$expr` 实现条件逻辑，检索位于南半球且员工效率比（人均销售额）超过 2000 的商店。

```javascript
db.stores.find({_id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  $expr: {
    $and: [
      { $gte: ["$location.lat", 70.1272] },
      {
        $gt: [
          {
            $divide: [
              "$sales.totalSales",
              { $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }
            ]
          },
          2000
        ]
      }
    ]
  }
}).limit(1)
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "location": {
      "lat": 70.1272,
      "lon": 69.7296
    },
    "staff": {
      "totalStaff": {
        "fullTime": 19,
        "partTime": 20
      }
    },
    "sales": {
      "totalSales": 151864,
      "salesByCategory": [
        {
          "categoryName": "Sound Bars",
          "totalSales": 2120
        },
        {
          "categoryName": "Home Theater Projectors",
          "totalSales": 45004
        }
      ]
    },
    "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
    "lastUpdated": ISODate("2025-06-11T11:06:57.922Z"),
    "status": "active",
    "category": "high-volume",
    "priority": 1,
    "reviewDate": ISODate("2025-06-11T11:10:50.276Z")
  }
]
```
