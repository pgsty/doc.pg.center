---
title: $replaceWith
description: DocumentDB 中的 $replaceWith 运算符在将文档替换为指定文档后返回一个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$replacewith.md
weight: 260
translation_source_sha256: f129ccdd13fb9a35dc381a7375b22c1dd358b002b567a506c2592b998fa71c08
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$replaceWith` 聚合流水线阶段运算符用于将输入文档替换为指定的文档。`$replaceWith` 运算符可将文档从一种结构转换为另一种结构，或完全用新字段和值替换文档。

## 语法 {#syntax}

```javascript
{
  "$replaceWith": <newDocument>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`newDocument`** | 用于替换原始文档的新文档 |
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

<span id="example-1-return-a-document-that-replaces-the-contents-of-the-original-document-with-a-subset-of-items"></span>

### 示例 1 - 返回一个文档，该文档将原始文档的内容替换为指定字段的子集 {#example-1---return-a-document-that-replaces-the-contents-of-the-original-document-with-a-subset-of-items}

首先，通过 _id 字段匹配要替换的特定文档，并将文档内容替换为指定字段。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "bda56164-954d-4f47-a230-ecf64b317b43"
    }
}, {
    $replaceWith: {
        _id: "$_id",
        name: "$name",
        sales: "$sales.totalSales"
    }
}])
```

此查询返回以下结果：

```json
[
  {
      "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
      "name": "Boulder Innovations | Home Security Place - Ankundingburgh",
      "sales": 37015
  }
]
```

<span id="example-2-return-a-document-that-replaces-the-contents-of-the-original-document-after-aggregating-specified-fields"></span>

### 示例 2 - 返回一个文档，该文档在聚合指定字段后替换原始文档的内容 {#example-2---return-a-document-that-replaces-the-contents-of-the-original-document-after-aggregating-specified-fields}

```javascript
db.stores.aggregate([{
    $match: {
        _id: "bda56164-954d-4f47-a230-ecf64b317b43"
    }
}, {
    $replaceWith: {
        _id: "$_id",
        name: "$name",
        totalStaff: {
            $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
        }
    }
}])
```

此操作返回以下结果：

```json
[
  {
      "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
      "name": "Boulder Innovations | Home Security Place - Ankundingburgh",
      "totalStaff": 29
  }
]
```
