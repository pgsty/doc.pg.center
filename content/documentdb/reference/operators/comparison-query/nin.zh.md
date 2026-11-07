---
title: $nin
description: $nin 运算符获取字段值与给定列表中的所有值都不匹配的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$nin.md
weight: 90
translation_source_sha256: 2919dd62e44eb6986ed3be63bdc7ab00c37c3a089cc28680b16af7dff4d88d1a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$nin` 运算符获取指定字段的值与给定列表中的所有值都不匹配的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $nin: [ < listOfValues > ]
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要比较的字段。|
| **`[<listOfValues>]`** | 值数组，其中的任何值都不应与所比较字段的值匹配。|
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

<span id="example-1-find-a-store-with-a-discount-that-isn-t-10-15-or-20"></span>

### 示例 1：查找折扣既不是 10%、15% 也不是 20% 的商店 {#example-1---find-a-store-with-a-discount-that-isnt-10-15-or-20}

要查找促销折扣既不是 10%、15% 也不是 20% 的商店，先运行查询，对嵌套的 discountPercentage 字段使用 $nin。然后仅投影结果商店的名称及其提供的折扣，并将结果限制为结果集中的一个文档。

```javascript
db.stores.find({
    "promotionEvents.discounts.discountPercentage": {
        $nin: [10, 15, 20]
    }
}, {
    name: 1,
    "promotionEvents.discounts.discountPercentage": 1
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
            "discounts": [
              { "discountPercentage": 18 },
              { "discountPercentage": 17 },
              { "discountPercentage": 9 },
              { "discountPercentage": 5 },
              { "discountPercentage": 5 },
              { "discountPercentage": 6 },
              { "discountPercentage": 9 },
              { "discountPercentage": 5 },
              { "discountPercentage": 19 },
              { "discountPercentage": 21 }
            ]
          }
        ]
    }
]
```

<span id="example-2-find-a-store-with-no-discounts-on-specific-categories-of-promotions"></span>

### 示例 2：查找未对特定促销类别提供折扣的商店 {#example-2---find-a-store-with-no-discounts-on-specific-categories-of-promotions}

要查找对 Smoked Salmon 和 Anklets 均未开展促销的商店，先运行查询，对嵌套的 categoryName 字段使用 $nin。然后投影商店的名称及其提供的促销活动，并将结果限制为结果集中的一个文档。

```javascript
db.stores.find({
    "promotionEvents.discounts.categoryName": {
        $nin: ["Smoked Salmon", "Anklets"]
    }
}, {
    name: 1,
    "promotionEvents.discounts.categoryName": 1
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
            "discounts": [
              { "categoryName": "Bath Accessories" },
              { "categoryName": "Pillow Top Mattresses" },
              { "categoryName": "Bathroom Scales" },
              { "categoryName": "Towels" },
              { "categoryName": "Bathrobes" },
              { "categoryName": "Mattress Toppers" },
              { "categoryName": "Hand Towels" },
              { "categoryName": "Shower Heads" },
              { "categoryName": "Bedspreads" },
              { "categoryName": "Bath Mats" }
            ]
          }
        ]
    }
]
```
