---
title: $lookup
description: 聚合框架中的 $lookup 流水线阶段用于与其他集合执行左外连接。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$lookup.md
weight: 190
translation_source_sha256: c094a58a30b91ed1ee610a3460675dc9448d0615077b8482450118f667bbe889
translation_review: AI-assisted bilingual review; 2026-11-07
---

Aggregation Framework 中的 `$lookup` 流水线阶段用于与其他集合执行左外连接。它允许你根据指定条件合并来自不同集合的文档。此运算符有助于在不执行多个查询的情况下，将其他集合中的相关数据丰富到文档中。

## 语法 {#syntax}

```javascript
{
  $lookup: {
    from: <collection to join>,
    localField: <field from input documents>,
    foreignField: <field from the documents of the "from" collection>,
    as: <output array field>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`from`** | 要连接的集合的名称。|
| **`localField`** | 输入文档中与 `foreignField` 匹配的字段。|
| **`foreignField`** | `from` 集合中与 `localField` 匹配的文档字段。|
| **`as`** | 要添加到输入文档的新数组字段的名称。该数组包含从 `from` 集合中匹配到的文档。|
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

假设我们还有一个包含两个文档的 `ratings` 集合。

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "rating": 5
}
{
  "_id": "fecca713-35b6-44fb-898d-85232c62db2f",
  "rating": 3
}
```

### 示例 1：将两个集合合并，列出评分为 5 的商店的促销活动 {#example-1-combine-two-collections-to-list-promotion-events-for-stores-with-a-rating-of-5}

此查询将 `ratings` 集合与 `stores` 集合连接，列出与每个评分为 5 的商店相关的促销活动。

```javascript
db.ratings.aggregate([
  // filter based on rating in ratings collection
  {
    $match: {
      "rating": 5
    }
  },
  // find related documents in stores collection
  {
    $lookup: {
      from: "stores",
      localField: "_id",
      foreignField: "_id",
      as: "storeEvents"
    }
  },
  // deconstruct array to output a document for each element of the array
  {
    $unwind: "$storeEvents"
  },
   // Include only _id and name fields in the output 
  { $project: { _id: 1, "storeEvents.name": 1 } }  

])
```

此查询返回以下结果：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "storeEvents": { "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile" }
  }
]
```

### 示例 2：使用 ratings 中的变量连接 ratings 和 stores 两个集合。 {#example-2-joining-two-collections-ratings-and-stores-using-a-variable-from-ratings}

```javascript
db.ratings.aggregate([
  {
    $match: { rating: 5 }
  },
  {
    $lookup: {
      from: "stores",
      let: { id: "$_id" },
      pipeline: [
        {
          $match: {
            $expr: { $eq: ["$_id", "$$id"] }
          }
        },
        {
          $project: { _id: 0, name: 1 }
        }
      ],
      as: "storeInfo"
    }
  },
  {
    $unwind: "$storeInfo"
  },
  {
    $project: {
      _id: 1,
      rating: 1,
      "storeInfo.name": 1
    }
  }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "rating": 5,
        "storeInfo": {
            "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile"
        }
    }
]
```
