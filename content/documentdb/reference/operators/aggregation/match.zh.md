---
title: $match
description: 聚合流水线中的 $match 流水线阶段用于筛选符合指定条件的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$match.md
weight: 200
translation_source_sha256: 4b5ad053ae99667a8180e31e9f0e5c03fd40eb150f510ec590656874129cc325
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$match` 流水线阶段用于筛选符合指定条件的文档。它类似于 `find` 操作，但用于聚合流水线中，以缩小传递到下一阶段的文档范围。该阶段对于通过减少后续阶段需要处理的文档数量来优化性能非常有用。

## 语法 {#syntax}

```javascript
{
  $match: {
    <query>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<query>`** | 一个标准的 MongoDB 查询文档，指定文档必须满足的条件。|
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

### 示例 1：使用字符串比较匹配文档 {#example-1-match-documents-using-string-comparison}

此查询检索 `_id` 为 "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" 的文档：

```javascript
db.stores.aggregate([
    {
      $match: {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
      }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
        "location": {
            "lat": 60.1441,
            "lon": -141.5012
        },
        "staff": {
            "employeeCount": {
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
        "promotionEvents": [],
        "tag": [
            "#ShopLocal",
            "#NewArrival",
            "#NewArrival",
            "#FreeShipping"
        ],
        "company": "Lakeshore Retail",
        "city": "Port Cecile",
        "lastUpdated": "2025-08-04T05:57:04.619Z",
        "storeOpeningDate": "2024-09-12T10:21:58.274Z"
    }
]
```

### 示例 2：使用数值比较匹配文档 {#example-2-match-documents-using-numeric-comparison}

此查询检索所有总销售额大于 35,000 美元的 stores：

```javascript
db.stores.aggregate([
    {
      $match: {
        "sales.totalSales": { $gt: 35000 }
      }
    },
    // Limit the result to the first 3 documents
    { $limit: 3 },
      // Include only _id and name fields in the output 
    { $project: { _id: 1, name: 1 } } 
])
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland"
  },
  {
    "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
    "name": "Wide World Importers | Bed and Bath Store - West Vitafort"
  },
  {
    "_id": "560099f8-325f-4c35-a4e5-2e0879eb95af",
    "name": "Wide World Importers | Bed and Bath Depot - North Maritzaberg"
  }
]
```

### 示例 3：在子文档中匹配文档 {#example-3-match-documents-within-sub-documents}

此查询检索所有对 DJ Mixers 类别提供 15% 折扣的商店：

```javascript
db.stores.aggregate([
    {
      $match: {
        "promotionEvents.discounts": {
          $elemMatch: {
            "categoryName": "DJ Mixers",
            "discountPercentage": 15
          }
        }
      }
    },
    // Limit the result to the first 3 documents
    { $limit: 3 },
      // Include only _id and name fields in the output 
    { $project: { _id: 1, name: 1 } } 
])
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile"
  },
  {
    "_id": "3c7eda41-23a1-4226-abf6-17ee9e851b5b",
    "name": "Boulder Innovations | DJ Equipment Bazaar - New Ceasarview"
  },
  {
    "_id": "63831a7d-13a9-4d8b-bf1d-ac004057f96d",
    "name": "Contoso, Ltd. | DJ Equipment Shop - Reillyfurt"
  }
]
```
