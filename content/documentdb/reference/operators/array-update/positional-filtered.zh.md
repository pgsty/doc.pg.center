---
title: $[identifier]
description: $[identifier] 运算符通过特定标识符，更新数组中满足查询条件的所有元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$positional-filtered.md
weight: 30
translation_source_sha256: 6097ee941508d1ff19c6b8848dbc81c1cbf6c2610d571037cd2043df8d995b93
translation_review: AI-assisted bilingual review; 2026-11-07
---

$[identifier] 数组更新运算符用于更新数组中满足给定条件的特定元素。当需要根据一定条件更新数组中的多个元素时，可以使用此运算符。它支持在文档内部进行更精细的更新，是管理复杂数据结构的有力工具。

## 语法 {#syntax}

```javascript
{
  <update operator>: {
    <array field>.$[<identifier>]: <value>
  }
},
{
  arrayFilters: [
    { <identifier>.<field>: <condition> }
  ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<update operator>`** | 要应用的更新运算符（例如 `$set`、`$inc` 等）。 |
| **`<array field>`** | 包含待更新数组的字段。 |
| **`<identifier>`** | 在 `arrayFilters` 中使用的占位符，用于匹配数组中的特定元素。 |
| **`<value>`** | 要设置或更新的值。 |
| **`arrayFilters`** | 筛选条件数组，用于确定要更新哪些元素。 |
| **`<field>`** | 数组元素中要检查的特定字段。 |
| **`<condition>`** | 数组元素必须满足此条件才会被更新。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "location": {
        "lat": -48.9752,
        "lon": -141.6816
    },
    "staff": {
        "employeeCount": {
            "fullTime": 12,
            "partTime": 19
        }
    },
    "sales": {
        "salesByCategory": [
            {
                "categoryName": "Desk Lamps",
                "totalSales": 37978
            }
        ],
        "revenue": 37978
    },
    "promotionEvents": [
        {
            "eventName": "Crazy Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2023,
                    "Month": 9,
                    "Day": 27
                },
                "endDate": {
                    "Year": 2023,
                    "Month": 10,
                    "Day": 4
                }
            },
            "discounts": [
                {
                    "categoryName": "Desks",
                    "discountPercentage": 25
                },
                {
                    "categoryName": "Filing Cabinets",
                    "discountPercentage": 23
                }
            ]
        },
        {
            "eventName": "Incredible Markdown Mania",
            "promotionalDates": {
                "startDate": {
                    "Year": 2023,
                    "Month": 12,
                    "Day": 26
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 1,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Monitor Stands",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Desks",
                    "discountPercentage": 24
                }
            ]
        },
        {
            "eventName": "Major Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 3,
                    "Day": 25
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 4,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Office Accessories",
                    "discountPercentage": 9
                },
                {
                    "categoryName": "Desks",
                    "discountPercentage": 13
                }
            ]
        },
        {
            "eventName": "Blowout Bonanza",
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
                    "categoryName": "Office Chairs",
                    "discountPercentage": 24
                },
                {
                    "categoryName": "Desk Lamps",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Super Saver Fiesta",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 10,
                    "Day": 1
                }
            },
            "discounts": [
                {
                    "categoryName": "Desks",
                    "discountPercentage": 5
                },
                {
                    "categoryName": "Monitor Stands",
                    "discountPercentage": 10
                }
            ]
        }
    ],
    "company": "Trey Research",
    "city": "Lake Freeda",
    "storeOpeningDate": "2024-12-30T22:55:25.779Z",
    "lastUpdated": {
        "t": 1729983325,
        "i": 1
    }
}
```

### 示例 1：更新指定促销活动中所选类别的折扣百分比。 {#example-1-update-the-discount-percentage-for-the-chosen-category-in-the-specified-promotion-event}

此查询修改促销活动数组中活动名称为 'Blowout Bonanza' 的特定元素，更新 'Desk Lamps' 类别的折扣百分比。

```javascript
db.stores.updateOne(
  {
    _id: "905d1939-e03a-413e-a9c4-221f74055aac",
    "promotionEvents.eventName": "Blowout Bonanza"
  },
  {
    $set: {
      "promotionEvents.$[event].discounts.$[discount].discountPercentage": 18
    }
  },
  {
    arrayFilters: [
      { "event.eventName": "Blowout Bonanza" },
      { "discount.categoryName": "Desk Lamps" }
    ]
  }
)
```
