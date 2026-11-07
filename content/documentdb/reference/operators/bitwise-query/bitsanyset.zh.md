---
title: $bitsAnySet
description: $bitsAnySet 运算符返回指定位中至少有一位为 1 的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-query/$bitsAnySet.md
weight: 40
translation_source_sha256: 30a01073667b61172f19e5c95a9b0b882f54c5189c0eb6b0a302b8a542b05e79
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例标题写的是店内自提和免下车服务，而说明及代码中的第 5、7 位，按功能表对应免费 Wi-Fi 和送货上门。

此运算符用于选择指定位中至少有一位为 `1` 的文档，适用于查询字段中存储位掩码值的文档。在处理用单个整数表示多个布尔标志的字段时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  <field>: { $bitsAnySet: [ <bit positions> ] }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要查询的字段。|
| **`<bit positions>`** | 位位置数组，用于检查这些位置中是否至少有一位为 `1`。|
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

### 示例 1：查找提供店内自提或免下车服务的商店 {#example-1-find-stores-that-have-in-store-pickup-or-drive-thru}

此查询获取提供送货上门或免费 Wi-Fi 服务的商店（第 5 位和第 7 位）。

```javascript
db.stores.find({
    storeFeatures: {
        $bitsAnySet: [5, 7]
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
            $bitsAnySet: 160
        }
    }, // 32 + 128
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
    "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
    "name": "Fourth Coffee | Storage Solution Gallery - Port Camilla",
    "storeFeatures": 222
  },
  {
    "_id": "94792a4c-4b03-466b-91f6-821c4a8b2aa4",
    "name": "Fourth Coffee | Eyewear Shop - Lessiemouth",
    "storeFeatures": 225
  },
  {
    "_id": "728c068a-638c-40af-9172-8ccfa7dddb49",
    "name": "Contoso, Ltd. | Book Store - Lake Myron",
    "storeFeatures": 239
  },
  {
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "name": "Relecloud | Toy Collection - North Jaylan",
    "storeFeatures": 108
  }
]
```
