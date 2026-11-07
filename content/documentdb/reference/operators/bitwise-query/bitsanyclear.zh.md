---
title: $bitsAnyClear
description: $bitsAnyClear 运算符匹配位掩码所指定的位中至少有一位未置位的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-query/$bitsAnyClear.md
weight: 30
translation_source_sha256: 5e473a577b943b3d5dd1dd2ba0592b86b79710bf11b8965103ee0aba11fdcffd
translation_review: AI-assisted bilingual review; 2026-11-07
---

此运算符用于匹配这样的文档：位掩码所指定的位中至少有一位未置位（即为 0）。它适用于查询包含二进制数据或以整数形式存储的标志的文档，支持根据特定的位模式高效查询。

## 语法 {#syntax}

```javascript
{
  <field>: { $bitsAnyClear: <bitmask> }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 文档中要查询的字段。|
| **`<bitmask>`** | 位掩码，用于指定要检查哪些位是否为 0（未置位）。|
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

`storeFeatures` 字段是一个位掩码整数，用于表示商店的各种服务和设施。每一位对应一项：

| 位 | 值 | 服务或设施                 |
|-----|-------|--------------------------|
| 0   | 1     | 店内自提          |
| 1   | 2     | 停车场                  |
| 2   | 4     | 轮椅通道        |
| 3   | 8     | 24 小时营业            |
| 4   | 16    | 允许携带宠物             |
| 5   | 32    | 免费 Wi-Fi               |
| 6   | 64    | 卫生间                |
| 7   | 128   | 送货上门            |

<span id="example-1-find-stores-that-don-t-have-wi-fi-or-in-store-pickup"></span>

### 示例 1：查找未提供 Wi-Fi 或未提供店内自提服务的商店 {#example-1-find-stores-that-dont-have-wi-fi-or-in-store-pickup}

此查询获取未提供 Wi-Fi 或未提供店内自提服务的商店（第 0 位和第 5 位）。

```javascript
db.stores.find({
    storeFeatures: {
        $bitsAnyClear: [0, 5]
    }
}, {
    _id: 1,
    name: 1,
    storeFeatures: 1
}).limit(5)
```

等价写法：

```javascript
db.stores.find({
        storeFeatures: {
            $bitsAnySet: 33
        }
    }, // 1 + 32
    {
        _id: 1,
        name: 1,
        storeFeatures: 1
    }).limit(5)
```

此查询返回的前五个结果如下：

```json
[
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "storeFeatures": 38
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "storeFeatures": 86
  },
  {
    "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
    "name": "Fourth Coffee | Storage Solution Gallery - Port Camilla",
    "storeFeatures": 222
  },
  {
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "name": "Relecloud | Toy Collection - North Jaylan",
    "storeFeatures": 108
  },
  {
    "_id": "9024d615-eed0-429a-a098-6640207cc2b6",
    "name": "Adatum Corporation | Paper Product Mart - Lake Coralie",
    "storeFeatures": 204
  }
]
```
