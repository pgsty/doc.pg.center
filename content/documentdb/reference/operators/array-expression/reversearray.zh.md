---
title: $reverseArray
description: $reverseArray 运算符用于反转数组中元素的顺序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$reversearray.md
weight: 100
translation_source_sha256: 7edf150a51b0edcadc2eac91655267dd320064adddd70ee5f3c3bb0c2b1fb21d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$reverseArray` 运算符用于反转数组中元素的顺序。当需要以相反顺序处理或显示数组元素时，该运算符非常有用。它是一个数组表达式运算符，可在聚合流水线中使用。

## 语法 {#syntax}

```javascript
{
  $reverseArray: <array>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<array>`** | 要反转的数组。|
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "location": {
        "lat": 60.1441,
        "lon": -141.5012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 2,
            "partTime": 0
        }
    },
    "sales": {
        "salesByCategory": [
            {
                "categoryName": "DJ Headphones",
                "totalSales": 35921
            }
        ],
        "fullSales": 3700
    },
    "promotionEvents": [
        {
            "eventName": "Bargain Blitz Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 3,
                    "Day": 11
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 2,
                    "Day": 18
                }
            },
            "discounts": [
                {
                    "categoryName": "DJ Turntables",
                    "discountPercentage": 18
                },
                {
                    "categoryName": "DJ Mixers",
                    "discountPercentage": 15
                }
            ]
        },
        {
            "eventName": "Discount Delight Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 5,
                    "Day": 11
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 5,
                    "Day": 18
                }
            }
        }
    ],
    "tag": [
        "#ShopLocal",
        "#FashionStore",
        "#SeasonalSale",
        "#FreeShipping",
        "#MembershipDeals"
    ]
}
```

### 示例 1：反转数组元素的顺序 {#example-1-reversing-the-order-of-an-array}

此查询演示了如何使用运算符对 `promotionEvents` 数组的顺序进行反转。

```javascript
db.stores.aggregate([
    //filtering to one document
    {
        $match: {
            _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
        }
    },
    {
        $project: {
            _id: 1,
            name: 1,
            promotionEventsReversed: {
                $reverseArray: "$promotionEvents"
            }
        }
    },
    // Include only _id, name, promotionalDates and eventName fields in the output 
    {
        $project: {
            _id: 1,
            name: 1,
            "promotionEventsReversed.promotionalDates": 1,
            "promotionEventsReversed.eventName": 1
        }
    }
])
```

此查询返回以下结果。

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
        "promotionEventsReversed": [
            {
                "eventName": "Discount Delight Days",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 5,
                        "Day": 11
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 5,
                        "Day": 18
                    }
                }
            },
            {
                "eventName": "Bargain Blitz Days",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 3,
                        "Day": 11
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 2,
                        "Day": 18
                    }
                }
            }
        ]
    }
]
```
