---
title: $ne
description: $ne 运算符获取字段值不等于指定值的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$ne.md
weight: 80
translation_source_sha256: 688d8b8a08d962c5ed6d8a35e8ee031d4d4a83e90d7ce01aceecc8d106a99b25
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$ne` 运算符获取字段值不等于指定值的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $ne: value
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要比较的字段。|
| **`value`** | 字段值不应等于此值。|
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

<span id="example-1-find-a-store-whose-name-isn-t-fourth-coffee"></span>

### 示例 1：查找名称不是 "Fourth Coffee" 的商店 {#example-1---find-a-store-whose-name-isnt-fourth-coffee}

要查找名称不是 "Fourth Coffee" 的商店，先运行查询，对 name 字段使用 $ne。然后仅投影结果文档的名称，并将结果限制为结果集中的一个商店。

```javascript
db.stores.find({
    name: {
        $ne: "Fourth Coffee"
    }
}, {
    _id: 1,
    name: 1
}, {
    limit: 1
})
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir"
    }
]
```

<span id="example-2-find-a-store-with-promotion-events-that-aren-t-in-2024"></span>

### 示例 2：查找促销活动不在 2024 年的商店 {#example-2---find-a-store-with-promotion-events-that-arent-in-2024}

要查找促销活动并非始于 2024 年的商店，先运行查询，对嵌套的 startDate 字段使用 $ne。然后投影商店的名称及其提供的促销活动，并将结果限制为结果集中的一个文档。

```javascript
db.stores.find({
    "promotionEvents.promotionalDates.startDate": {
        $ne: "2024"
    }
}, {
    name: 1,
    "promotionEvents.promotionalDates.startDate": 1
}, {
    limit: 1
})
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "promotionEvents": [
          {
            "promotionalDates": { "startDate": { "Year": 2024, "Month": 9, "Day": 21 } }
          }
        ]
    }
]
```
