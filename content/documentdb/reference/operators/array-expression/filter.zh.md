---
title: $filter
description: $filter 运算符根据指定条件筛选数组中的元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$filter.md
weight: 40
translation_source_sha256: 7c97eab027056fa1ec2ade6eb862723c67b2edc9dc6a719ba15ee3522a6d5d7e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$filter` 运算符用于根据指定条件筛选数组中的元素。当需要操作或获取文档内的特定数组元素时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $filter: {
    input: "<array>",
    as: "<string>",
    cond: "<expression>"
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`**| 求值结果为数组的表达式。|
| **`as`**| 指定输入数组中各元素所用变量名的字符串。|
| **`cond`**| 决定是否将元素包含在输出数组中的表达式。|
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

### 示例 1：获取按条件筛选的元素 {#example-1-retrieve-an-element-filtered-on-condition}

此查询演示如何根据 `totalSales` 筛选销售类别。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
        }
    },
    {
        $project: {
            filteredSalesByCategory: {
                $filter: {
                    input: "$sales.salesByCategory",
                    as: "item",
                    cond: {
                        $gt: ["$$item.totalSales", 10000]
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
      "filteredSalesByCategory": [
          {
              "categoryName": "DJ Headphones",
              "totalSales": 35921
          }
      ]
  }
]
```
