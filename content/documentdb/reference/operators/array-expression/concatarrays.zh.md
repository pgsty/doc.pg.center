---
title: $concatArrays
description: $concatArrays 用于将多个数组合并为一个数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$concatarrays.md
weight: 30
translation_source_sha256: 74f2d6717573e92b623ced7894df445908f1063f950d646ff0eaf135587ec00b
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$concatArrays` 运算符用于将多个数组合并为一个数组。当需要合并来自不同文档或文档中不同字段的数组时，该运算符非常有用。

## 语法 {#syntax}

```javascript
{
  $concatArrays: ["<array1>", "<array2>"]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<array1>, <array2>`**| 需要进行连接的数组字段。|
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

### 示例 1：合并文档中的数组 {#example-1-concatenating-arrays-in-a-document}

此查询将 `promotionEvents.discounts` 数组中的 `categoryName` 字段与 `tag` 数组合并为一个 combinedTags 数组。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
    }
}, {
    $project: {
        combinedTags: {
            $concatArrays: ["$promotionEvents.discounts.categoryName", "$tag"]
        }
    }
}])
```

此查询返回以下结果。

```json
[
  {
      "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
      "combinedTags": [ '#ShopLocal', '#NewArrival', '#NewArrival', '#FreeShipping' ]
  }
]
```
