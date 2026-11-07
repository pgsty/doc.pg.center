---
title: $bsonSize
description: $bsonSize 运算符返回文档编码为 BSON 后的大小，单位为字节。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/data-size/$bsonsize.md
weight: 20
translation_source_sha256: 26839fd81b95c0f72ff66c1d0a086f7ae36465f53260bd0f8c175668a2ddb01e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bsonSize` 运算符用于返回文档编码为 BSON 后的大小，单位为字节。它可用于了解集合中文档的存储需求。此运算符可在聚合流水线中计算文档大小，有助于优化存储并了解对性能的影响。

## 语法 {#syntax}

```javascript
{
  $bsonSize: <expression>
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`**| 任意有效表达式，其求值结果为要计算 BSON 大小的文档。|
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

<span id="example-1-calculate-the-total-bson-encoded-size-of-a-document-in-bytes-using-bson-size"></span>

### 示例 1：使用 $bsonSize 计算文档经 BSON 编码后的总字节数 {#example-1-calculate-the-total-bson-encoded-size-of-a-document-in-bytes-using-bsonsize}

此查询计算文档的 BSON 大小。

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 1,              
      name: 1,         
      documentSize: { 
        $bsonSize: "$$ROOT"    //pass the whole document
      }
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
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "documentSize": 2226
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "documentSize": 1365
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "documentSize": 1882
  }
]
```
