---
title: $pullAll
description: $pullAll 运算符用于从数组中移除指定值的所有实例。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$pullall.md
weight: 90
translation_source_sha256: 139b99a9d57d115c9deecff6682a04a5c627aadb583023bb9c3de8061dd07c4a
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 说明将运算符拼为 `$pulAll`，并把被移除的标签值称作折扣。代码实际使用 `$pullAll` 从标签数组中移除值。

`$pullAll` 运算符用于从数组中移除指定值的所有实例。当需要在一次操作中移除多个指定元素以清理数组时，可以使用此运算符。

`$pull` 和 `$pullAll` 都用于从数组中移除元素，但确定待移除元素的方式不同。`$pull` 会移除数组中满足指定条件的所有元素，该条件可以是一个简单的值，也可以是较复杂的查询（例如匹配子文档字段）。`$pullAll` 则移除以数组形式提供、要求精确匹配的指定值，不支持条件或查询。总体而言，`$pull` 更灵活，可以根据各种条件移除元素；`$pullAll` 则更简单，只针对一组固定的值。

## 语法 {#syntax}

```javascript
{
  $pullAll: { <field1>: [ <value1>, <value2>] }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field1>`**| 要从中移除指定值的字段。|
| **`[ <value1>, <value2>, ... ]`**| 要从指定字段中移除的值所组成的数组。|
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

### 示例 1：从数组中移除多个元素 {#example-1-remove-multiple-elements-from-an-array}

要从 'tag' 数组中移除 "#MembershipDeals" 和 "#SeasonalSale" 对应的折扣，可运行查询，对 tag 字段使用 $pulAll 运算符，并指定要移除的值。

```javascript
db.stores.updateMany(
    //filter
    { _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"},
    {
      $pullAll: {
        tag: ["#MembershipDeals","#SeasonalSale" ]
      }
    }
)
```

此查询返回以下结果。

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": 1,
    "modifiedCount": 1,
    "upsertedCount": 0
  }
]
```
