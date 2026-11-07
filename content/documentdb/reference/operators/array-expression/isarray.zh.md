---
title: $isArray
description: $isArray 运算符用于判断指定值是否为数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$isarray.md
weight: 60
translation_source_sha256: fa04957f059be36fb031b2954ddcd6ee75f48a13924e9dac18ce1174d893aa3c
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$isArray` 运算符用于判断指定值是否为数组。如果该值是数组，则返回 `true`；否则返回 `false`。此运算符常用于聚合流水线中，根据字段是否包含数组来筛选或转换文档。

## 语法 {#syntax}

```javascript
{
  $isArray: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 任何有效表达式，其结果为需要检查的值。|
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

### 示例 1：检查字段是否为数组 {#example-1-checking-if-a-field-is-an-array}

此查询检查每个商店文档中的 `sales.salesByCategory` 字段是否为数组，并返回前三个文档的检查结果。

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 1,
      isSalesByCategoryArray: { $isArray: "$sales.salesByCategory" }
    }
  },
 // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
        "isSalesByCategoryArray": true
    },
    {
        "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
        "isSalesByCategoryArray": true
    },
    {
        "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
        "isSalesByCategoryArray": true
    }
]
```

### 示例 2：根据数组字段筛选文档 {#example-2-filtering-documents-based-on-array-fields}

此查询演示如何使用 `$isArray` 筛选 `promotionEvents` 字段为数组的文档。

```javascript
db.stores.aggregate([
  {
    $match: {
      $expr: { $isArray: "$promotionEvents" }
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
        "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
        "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie"
    },
    {
        "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
        "name": "Northwind Traders | Bed and Bath Place - West Oraland"
    },
    {
        "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
        "name": "Wide World Importers | Bed and Bath Store - West Vitafort"
    }
]
```
