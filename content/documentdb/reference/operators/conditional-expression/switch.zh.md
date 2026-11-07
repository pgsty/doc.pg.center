---
title: $switch
description: $switch 运算符用于依次对一系列条件求值，并根据第一个求值结果为 true 的条件返回值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/conditional-expression/$switch.md
weight: 30
translation_source_sha256: 64fb39120372a6f855e56f924bea02ff3dc5597d9929849ec7d3bb01abab91d5
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 原文对 branches 的说明没有写完。语法块明确展示了结构：每个分支包含一个 case 表达式和一个 then 表达式。

`$switch` 运算符用于依次对一系列条件求值，并根据第一个求值结果为 true 的条件返回值。当需要在聚合流水线中实现复杂的条件逻辑时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $switch: {
    branches: [
      { case: <expression>, then: <expression> },
      { case: <expression>, then: <expression> }
    ],
    default: <expression>
  }
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **branches**| 文档数组，其中每个文档包含：|
| **case**| 求值结果为 `true` 或 `false` 的表达式。|
| **then**| 关联的 `case` 表达式求值结果为 `true` 时返回的表达式。|
| **default**| 所有 `case` 表达式的求值结果均不为 `true` 时返回的表达式。此字段可选。|
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

### 示例 1：根据全职和兼职员工人数确定员工类型 {#example-1-to-determine-staff-type-based-on-full-time-and-part-time-counts}

此查询根据员工人数确定员工类型。

```javascript
db.stores.aggregate([{
        $project: {
            name: 1,
            staffType: {
                $switch: {
                    branches: [{
                            case: {
                                $eq: ["$staff.totalStaff.partTime", 0]
                            },
                            then: "Only Full time"
                        },
                        {
                            case: {
                                $eq: ["$staff.totalStaff.fullTime", 0]
                            },
                            then: "Only Part time"
                        }
                    ],
                    default: "Both"
                }
            }
        }
    },
    // Limit the result to the first 3 documents
    {
        $limit: 3
    }
])
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "staffType": "Only Full time"
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "staffType": "Both"
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "staffType": "Both"
  }
]
```
