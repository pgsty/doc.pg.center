---
title: $in
description: $in 运算符将字段值与指定值组成的数组进行匹配
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$in.md
weight: 50
translation_source_sha256: 367c59f209fa84bd07969af8b613ec85c37b9ff52424417e31d6446b67ee9e27
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$in` 运算符将字段值与包含可能取值的数组进行匹配。`$in` 运算符筛选字段值等于任一指定值的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $in: [ listOfValues ]
    }
}
```

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

<span id="example-1-use-in-operator-as-comparison-query-to-find-a-store-with-specific-categories-of-promotions"></span>

### 示例 1：将 $in 运算符用于比较查询，查找对特定类别开展促销的商店 {#example-1---use-in-operator-as-comparison-query-to-find-a-store-with-specific-categories-of-promotions}

此查询查找通过促销活动为 "Smoked Salmon" 或 "Anklets" 类别提供折扣的商店。

```javascript
db.stores.find({
    "promotionEvents.discounts.categoryName": {
        $in: ["Smoked Salmon", "Anklets"]
    }
}, {
    name: 1,
    "promotionEvents.discounts.categoryName": 1
}).limit(1)
```

此查询返回的第一个结果是：

```json
[
    {
      "_id": "48fcdab8-b961-480e-87a9-19ad880e9a0a",
      "name": "Lakeshore Retail | Jewelry Collection - South Nicholas",
      "promotionEvents": [
        {
          "discounts": [
            {"categoryName": "Anklets"},
            {"categoryName": "Cufflinks"}
          ]
        },
        {
          "discounts": [
            {"categoryName": "Anklets"},
            {"categoryName": "Brooches"}
          ]
        },
        {
          "discounts": [
            {"categoryName": "Rings"},
            {"categoryName": "Bracelets"}
          ]
        },
        {
          "discounts": [
            {"categoryName": "Charms"},
            {"categoryName": "Bracelets"}
          ]
        },
        {
          "discounts": [
            {"categoryName": "Watches"},
            {"categoryName": "Pendants"}
          ]
        }
      ]
    }
]
```

<span id="example-2-use-in-operator-as-array-expression-in-an-array-for-a-specified-value-or-set-of-values"></span>

### 示例 2：将 $in 运算符用作数组表达式，在数组中查找指定的值或一组值 {#example-2---use-in-operator-as-array-expression-in-an-array-for-a-specified-value-or-set-of-values}

此查询查找指定商店，并筛选出任意 `promotionEvents.discounts` 中至少有一个 `discountPercentage` 为 15 或 20 的文档。它使用点号表示法指定路径，并通过 $in 运算符跨越数组层级匹配嵌套的折扣值。

```javascript
db.stores.find({
    _id: "48fcdab8-b961-480e-87a9-19ad880e9a0a",
    "promotionEvents.discounts.discountPercentage": {
        $in: [15, 20]
    }
}, {
    _id: 1,
    name: 1,
    "promotionEvents.discounts": 1
})
```

此查询返回以下结果：

```json
[
    {
      "_id": "48fcdab8-b961-480e-87a9-19ad880e9a0a",
      "name": "Lakeshore Retail | Jewelry Collection - South Nicholas",
      "promotionEvents": [
        {
          "discounts": [
            { "categoryName": "Anklets", "discountPercentage": 12 },
            { "categoryName": "Cufflinks", "discountPercentage": 9 }
          ]
        },
        {
          "discounts": [
            { "categoryName": "Anklets", "discountPercentage": 23 },
            { "categoryName": "Brooches", "discountPercentage": 12 }
          ]
        },
        {
          "discounts": [
            { "categoryName": "Rings", "discountPercentage": 10 },
            { "categoryName": "Bracelets", "discountPercentage": 21 }
          ]
        },
        {
          "discounts": [
            { "categoryName": "Charms", "discountPercentage": 9 },
            { "categoryName": "Bracelets", "discountPercentage": 13 }
          ]
        },
        {
          "discounts": [
            { "categoryName": "Watches", "discountPercentage": 20 },
            { "categoryName": "Pendants", "discountPercentage": 7 }
          ]
        }
      ]
    }
]
```
