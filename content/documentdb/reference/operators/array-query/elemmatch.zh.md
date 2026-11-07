---
title: $elemMatch
description: $elemMatch 运算符返回完整的数组，其中包含至少一个满足匹配条件的数组元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-query/$elemmatch.md
weight: 20
translation_source_sha256: 425f1802c21d5c484fd831344db89ffbf82af2f620b553b3a1384d36c0780f99
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$elemMatch` 运算符用于匹配这样的文档：文档包含一个数组字段，且数组中至少有一个元素满足全部指定的查询条件。当需要查找数组中包含指定元素的文档时，可以使用此运算符。

## 语法 {#syntax}

```javascript
db.collection.find({ <field>: { $elemMatch: { <query1>, <query2>, ... } } })
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 包含待查询数组的文档字段。 |
| **`query`** | 数组中至少有一个元素必须满足的条件。 |
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

### 示例 1：在数组的元素列表中查找特定元素 {#example-1-find-in-an-array-for-specific-element-among-the-list-of-elements}

此查询检索 `stores` 集合中的前两个文档，这些文档的 `promotionEvents` 数组中至少包含一个类别名称为 "DJ Lighting" 的折扣。该查询仅返回这些文档的 `_id` 和 `promotionEvents.discounts` 字段。

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        $elemMatch: {
            categoryName: "DJ Lighting"
        }
    }
}, {
    _id: 1,
    "promotionEvents.discounts": 1
}).limit(2)
```

此查询返回以下结果：

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "promotionEvents": [
            {
                "discounts": [
                    {
                        "categoryName": "DJ Turntables",
                        "discountPercentage": 18
                    },
                    {
                        "categoryName": "DJ Mixers",
                        "discountPercentage": 15
                    }
                ]
            },
            {
                "discounts": [
                    {
                        "categoryName": "DJ Lighting",
                        "discountPercentage": 14
                    },
                    {
                        "categoryName": "DJ Cases",
                        "discountPercentage": 20
                    }
                ]
            }
        ]
    },
    {
        "_id": "91de5201-8194-44bf-848f-674e8df8bf5e",
        "promotionEvents": [
            {
                "discounts": [
                    {
                        "categoryName": "DJ Cases",
                        "discountPercentage": 6
                    },
                    {
                        "categoryName": "DJ Mixers",
                        "discountPercentage": 14
                    }
                ]
            },
            {
                "discounts": [
                    {
                        "categoryName": "DJ Headphones",
                        "discountPercentage": 19
                    },
                    {
                        "categoryName": "DJ Speakers",
                        "discountPercentage": 13
                    }
                ]
            },
            {
                "discounts": [
                    {
                        "categoryName": "DJ Lighting",
                        "discountPercentage": 12
                    },
                    {
                        "categoryName": "DJ Accessories",
                        "discountPercentage": 6
                    }
                ]
            }
        ]
    }
]
```
