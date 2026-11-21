---
title: $arrayToObject
description: $arrayToObject 运算符允许将数组转换为单个文档。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/operators/array-expression/$arraytoobject.md
weight: 20
translation_source_sha256: 1e2c74d7ef7799e923ef26925e23d9fd1dc5fa7601c795a04608dfbcc8a7c0d7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$arrayToObject` 运算符用于将数组转换为单个文档。当需要将键值对数组转换为更结构化的文档格式时，该运算符非常有用。

## 语法 {#syntax}

```javascript
{
  $arrayToObject: "<array>"
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<array>`**| 要转换为文档的数组。数组中的每个元素必须满足以下条件之一：a) 一个包含两个元素的数组，第一个元素为字段名，第二个元素为字段值。b) 一个恰好包含两个字段 "k" 和 "v" 的文档，其中 "k" 为字段名，"v" 为字段值。|
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
            },
            {
                "categoryName": "DJ Cables",
                "totalSales": 1000
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

### 示例 1：将数组转换为键值对文档 {#example-1-convert-the-array-to-a-key-value-document}

此查询将 `salesByCategory` 数组转换为一个对象，其中每个 `categoryName` 作为键，`totalSales` 作为对应的值。经过此转换，可以直接通过对象结构按类别访问销售数据，操作更为简便。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
        }
    },
    {
        $project: {
            "sales.salesByCategory": {
                $arrayToObject: {
                    $map: {
                        input: "$sales.salesByCategory",
                        as: "item",
                        in: {
                            k: "$$item.categoryName",
                            v: "$$item.totalSales"
                        }
                    }
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
      "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
      "sales": {
          "salesByCategory": {
              "DJ Headphones": 35921,
              "DJ Cables": 1000
          }
      }
  }
]
```
