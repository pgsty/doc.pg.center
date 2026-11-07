---
title: $indexOfArray
description: $indexOfArray 运算符用于在数组中搜索元素，并返回该元素首次出现的下标。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$indexofarray.md
weight: 50
translation_source_sha256: 2d6e5b05c4a2a26a4103667e0bbd61f94cbe13580e532b9fae44d2fdcc3e9fc0
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$indexOfArray` 运算符用于在数组中搜索元素，并返回该元素首次出现的下标。如果未找到该元素，则返回 `-1`。此运算符适用于需要确定元素在数组中位置的查询，例如查找列表中特定值或对象的下标。

## 语法 {#syntax}

```javascript
{
    $indexOfArray: [ < array > , < searchElement > , < start > , < end > ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<array>`**| 要在其中搜索元素的数组。|
| **`<searchElement>`**| 要在数组中搜索的元素。|
| **`<start>`**| （可选）开始搜索的下标。若省略，则从数组开头开始搜索。|
| **`<end>`**| （可选）结束搜索的下标。若省略，则搜索到数组末尾。|
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
        }
    ],
    "tag": [
        "#ShopLocal",
        "#SeasonalSale",
        "#FreeShipping",
        "#MembershipDeals"
    ]
}
```

### 示例 1：查找首次出现位置的下标 {#example-1-finding-the-index-of-the-first-occurrence}

此查询在集合中各文档的 `salesByCategory` 数组内，查找特定类别名称（"DJ Headphones"）的位置（下标）。

```javascript
db.stores.aggregate([
  {
    $project: {
      index: {
        $indexOfArray: [
          "$sales.salesByCategory.categoryName",
          "DJ Headphones"
        ]
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
        "index": -1
    },
    {
        "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
        "index": -1
    },
    {
        "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
        "index": -1
    }
]
```

### 示例 2：在指定范围内查找下标 {#example-2-finding-the-index-in-a-range}

此查询在 `promotionEvents` 数组的指定下标范围（3 到 5）内查找 "Bargain Blitz Days" 促销活动的位置，筛选结果并返回前三个匹配的文档。

```javascript
db.stores.aggregate([
  // Step 1: Project the index of the "Bargain Blitz Days" event name within the specified range
  {
    $project: {
      index: {
        $indexOfArray: [
          "$promotionEvents.eventName",
          "Bargain Blitz Days",
          3,
          5
        ]
      }
    }
  },
  // Step 2: Match documents where index > 0
  {
    $match: {
      index: { $gt: 0 }
    }
  },
 // Limit the result to the first 3 documents
  { $limit: 3 }                          
])
```

此查询返回以下结果：

```json
 [
    {
        "_id": "ced8caf0-051a-48ce-88d3-2935815261c3",
        "index": 3
    },
    {
        "_id": "509be7ce-539a-41b5-8fde-b85fb3ef3faa",
        "index": 3
    },
    {
        "_id": "d06e8136-9a7f-4b08-92c8-dc8eac73bad3",
        "index": 3
    }
]
```
