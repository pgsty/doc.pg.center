---
title: $maxN
description: $maxN 运算符根据指定的筛选条件检索前 N 个最大值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$maxn.md
weight: 100
translation_source_sha256: d6aa42685dcc5fa614e8d3cb8c3ed86d101b12f7602faefbed43ffb2bf79dce7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$maxN` 运算符用于根据指定的筛选条件检索字段的前 N 个最大值。

## 语法 {#syntax}

```javascript
$maxN: {
    input: < field or expression > ,
    n: < number of values to retrieve >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 指定要评估最大值的字段或表达式。 |
| **`n`** | 指定要检索的最大值数量。必须为正整数。 |
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
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

<span id="example-1-use-max-n-as-accumulator-to-retrieve-top-two-sales-categories"></span>

### 示例 1：将 `$maxN` 用作 `accumulator`，以检索前两个销售类别 {#example-1-use-maxn-as-accumulator-to-retrieve-top-two-sales-categories}

此查询检索销售表现最佳的前两个类别，或跨各商店的聚合顶级类别。

```javascript
db.stores.aggregate([{
        $project: {
            topSalesCategories: {
                $maxN: {
                    input: "$sales.salesByCategory",
                    n: 2
                }
            }
        }
    },
    {
        $limit: 4
    }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "topSalesCategories": [
      {
        "categoryName": "Stockings",
        "totalSales": 25731
      }
    ]
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "topSalesCategories": [
      {
        "categoryName": "Markers",
        "totalSales": 3927
      }
    ]
  },
  {
    "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
    "topSalesCategories": [
      {
        "categoryName": "Storage Boxes",
        "totalSales": 2236
      }
    ]
  },
  {
    "_id": "94792a4c-4b03-466b-91f6-821c4a8b2aa4",
    "topSalesCategories": [
      {
        "categoryName": "Travel Backpacks",
        "totalSales": 13189
      },
      {
        "categoryName": "Suitcases",
        "totalSales": 37858
      }
    ]
  }
]
```

<span id="example-2-using-max-n-in-set-window-fields"></span>

### 示例 2：在 `$setWindowFields` 中使用 `$maxN` {#example-2-using-maxn-in-setwindowfields}

此查询按城市检索 2023 年 "Laptops" 类别的前 N 个折扣。该查询首先筛选 2023 年的 "Laptops" 折扣条目，然后按城市对结果文档进行分组。

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $match: {
      "promotionEvents.discounts.categoryName": "Laptops",
      "promotionEvents.promotionalDates.startDate.Year": 2023
    }
  },
  {
    $group: {
      _id: "$city",
      allDiscounts: {
        $push: "$promotionEvents.discounts.discountPercentage"
      }
    }
  },
  {
    $project: {
      topDiscounts: {
        $slice: [
          { $sortArray: { input: "$allDiscounts", sortBy: -1 } },
          3 // Top N discounts
        ]
      }
    }
  }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "Lake Margareteland",
        "topDiscounts": [
            18
        ]
    },
    {
        "_id": "Horacetown",
        "topDiscounts": [
            13
        ]
    },
    {
        "_id": "D'Amoreside",
        "topDiscounts": [
            9
        ]
    }
]
```

<span id="example-3-using-max-n-operator-as-array-expression-to-find-top-three-sales-categories"></span>

### 示例 3：将 `$maxN` 运算符用作数组表达式，以查找前三个销售类别 {#example-3-using-maxn-operator-as-array-expression-to-find-top-three-sales-categories}

此查询从所有销售类别中检索前三个销售值。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      topThreeSales: {
        $maxN: {
          input: "$sales.salesByCategory.totalSales",
          n: 3
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
      "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
      "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
      "topThreeSales": [43522, 32272, 28946]
    }
]
```
