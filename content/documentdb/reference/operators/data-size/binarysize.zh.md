---
title: $binarySize
description: $binarySize 运算符用于返回二进制数据字段的大小。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/data-size/$binarysize.md
weight: 10
translation_source_sha256: 1f488b12083056a0fbd65bb9b668e6ae5c5c6aa7c2da9c1b900e7ab097a4c115
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$binarySize` 运算符用于返回二进制数据字段的大小。在处理存储的图像、文件或其他二进制内容时，可以使用此运算符。`$binarySize` 的参数应为字符串或二进制值。

## 语法 {#syntax}

```javascript
{
  $binarySize: "<field>"
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field>`**| 要获取其二进制大小的字段。|
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

<span id="example-1-calculate-the-size-of-a-string-or-binary-data-in-bytes-using-binary-size"></span>

### 示例 1：使用 $binarySize 计算字符串或二进制数据的字节数 {#example-1-calculate-the-size-of-a-string-or-binary-data-in-bytes-using-binarysize}

此查询计算 stores 集合中每个文档的 name 字段的二进制大小。

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,          
      dataSize: {
        $binarySize: "$name" // Calculate the binary size of the string data
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
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "dataSize": 49
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "dataSize": 48
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "dataSize": 50
  }
]
```
