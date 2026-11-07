---
title: $arrayElemAt
description: $arrayElemAt 返回数组中指定下标处的元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$arrayelemat.md
weight: 10
translation_source_sha256: 0be808143e9f3b66e7a67eba0b77b4910e021e48ea9e4931d465a00d318b542e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$arrayElemAt` 运算符用于返回数组中指定下标处的元素。当需要从文档内的数组中提取特定元素时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $arrayElemAt: ["<array>", <idx>]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<array>`**| 要从中取出元素的数组引用。|
| **`<idx>`**| 要返回的元素的下标。下标从零开始，负数下标从数组末尾开始计数。|
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
                "categoryName": "DJ Cables",
                "totalSales": 1000
            },
            {
                "categoryName": "DJ Headphones",
                "totalSales": 35921
            }
        ],
        "fullSales": 3700
    },
    "promotionEvents": [
        {
            "eventName": "Cyber Monday Event",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 8,
                    "Day": 1
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 8,
                    "Day": 7
                }
            },
            "discounts": [
                {
                    "categoryName": "DJ Speakers",
                    "discountPercentage": 25
                }
            ]
        },
        {
            "eventName": "Black Friday Event",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 8,
                    "Day": 1
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 8,
                    "Day": 7
                }
            },
            "discounts": [
                {
                    "categoryName": "DJ Speakers",
                    "discountPercentage": 25
                }
            ]
        },
        {
            "eventName": "Mega Discount Days",
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
            },
            "discounts": [
                {
                    "categoryName": "DJ Lights",
                    "discountPercentage": 20
                }
            ]
        }
    ],
    "tag": [
        "#ShopLocal",
        "#NewArrival",
        "#FashionStore",
        "#SeasonalSale",
        "#FreeShipping",
        "#MembershipDeals"
    ]
}

```

### 示例 1：返回数组字段中的第一个元素 {#example-1-return-the-first-element-from-an-array-field}

此查询从所查找商店的 `promotionEvents` 数组中获取第一个活动的详细信息。

```javascript
db.stores.aggregate([
  { $match: { name: "Lakeshore Retail | DJ Equipment Stop - Port Cecile" } },
  {
    $project: {
      firstPromotionEvent: { $arrayElemAt: ["$promotionEvents", 0] } 
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
      "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
      "firstPromotionEvent": {
          "eventName": "Cyber Monday Event",
          "promotionalDates": {
              "startDate": {
                  "Year": 2024,
                  "Month": 8,
                  "Day": 1
              },
              "endDate": {
                  "Year": 2024,
                  "Month": 8,
                  "Day": 7
              }
          },
          "discounts": [
              {
                  "categoryName": "DJ Speakers",
                  "discountPercentage": 25
              }
          ]
      }
  }
]
```
