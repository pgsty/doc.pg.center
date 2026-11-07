---
title: $bitsAllClear
description: $bitsAllClear 运算符用于匹配位掩码所指定的所有位均未置位的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-query/$bitsAllClear.md
weight: 10
translation_source_sha256: 096b93dbe336c5a2f6462115eb387850fb9222841082785ee84e3d09aca8a650
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bitsAllClear` 运算符用于匹配这样的文档：位掩码所指定的所有位均未置位（即为 0）。当需要根据字段的二进制表示中特定位未置位这一条件筛选文档时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  <field>: { $bitsAllClear: <bitmask> }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 文档中要对其执行位运算的字段。|
| **`<bitmask>`** | 位掩码，用于指定字段值中的哪些对应位必须为 0（未置位）。|
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

### 示例 1：查找非 24 小时营业且不允许携带宠物的商店 {#example-1-find-stores-that-are-not-open-24-hours-and-do-not-allow-pets}

此查询获取非 24 小时营业且不允许携带宠物的商店（第 3 位和第 4 位）。

```javascript
db.stores.find({
    storeFeatures: {
        $bitsAllClear: [3, 4]
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
            $bitsAnySet: 24
        }
    }, // 8 + 16
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
    "_id": "94792a4c-4b03-466b-91f6-821c4a8b2aa4",
    "name": "Fourth Coffee | Eyewear Shop - Lessiemouth",
    "storeFeatures": 225
  },
  {
    "_id": "1a2c387b-bb43-4b14-a6cd-cc05a5dbfbd5",
    "name": "Contoso, Ltd. | Smart Home Device Vault - Port Katarina",
    "storeFeatures": 36
  },
  {
    "_id": "e88f0096-4299-4944-9788-695c40786d97",
    "name": "Adatum Corporation | Handbag Shoppe - Lucienneberg",
    "storeFeatures": 135
  },
  {
    "_id": "bfb213fa-8db8-419f-8e5b-e7096120bad2",
    "name": "First Up Consultants | Beauty Product Shop - Hansenton",
    "storeFeatures": 135
  }
]
```
