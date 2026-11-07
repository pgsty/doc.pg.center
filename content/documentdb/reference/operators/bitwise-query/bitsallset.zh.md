---
title: $bitsAllSet
description: bitsAllSet 命令用于匹配所有指定位均已置位的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-query/$bitsAllSet.md
weight: 20
translation_source_sha256: 3404452967dae0f85f11663f7f366a187175ddc4e855eb944d751702e406ec7d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitsAllSet` 运算符用于匹配所有指定位均已置位（即为 1）的文档。此运算符适用于对存储整数值的字段执行位运算，可用于根据整数字段中特定位已置位这一条件筛选文档。

## 语法 {#syntax}

```javascript
{
  <field>: { $bitsAllSet: <bitmask> }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 文档中要对其执行位运算的字段。|
| **`<bitmask>`** | 位掩码，用于指示字段值中哪些位必须已置位。|
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

### 示例 1：查找设有停车场和卫生间的商店 {#example-1-find-stores-that-have-parking-and-restrooms}

此查询获取**同时设有停车场和卫生间**的商店（第 1 位和第 6 位）。

```javascript
db.stores.find({
    storeFeatures: {
        $bitsAllSet: [1, 6]
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
        $bitsAllSet: 66
    }
}, {
    _id: 1,
    name: 1,
    storeFeatures: 1
}).limit(5)
```

此查询返回的前五个结果如下：

```json
[
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
    "_id": "728c068a-638c-40af-9172-8ccfa7dddb49",
    "name": "Contoso, Ltd. | Book Store - Lake Myron",
    "storeFeatures": 239
  },
  {
    "_id": "a2b54e5c-36cd-4a73-b547-84e21d91164e",
    "name": "Contoso, Ltd. | Baby Products Corner - Port Jerrold",
    "storeFeatures": 126
  },
  {
    "_id": "dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3",
    "name": "Contoso, Ltd. | Home Improvement Closet - Jaskolskiview",
    "storeFeatures": 107
  }
]
```
