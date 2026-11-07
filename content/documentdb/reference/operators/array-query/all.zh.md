---
title: $all
description: $all 运算符可查找数组中包含全部指定元素的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-query/$all.md
weight: 10
translation_source_sha256: 8f269265427d2d4568379f8a7863f93629966a5eda6cd83e2cdb9041274ade6f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$all` 运算符用于选择字段值为数组且包含所有指定元素的文档。当需要确保数组字段包含多个指定元素（无论这些元素在数组中的顺序如何）时，该运算符非常有用。

## 语法 {#syntax}

```javascript
db.collection.find({
    field : {
        $all: [ < value1 > , < value2 > ]
    }
})
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要查询的字段。 |
| **`<value1> , <value2>`** | 必须全部存在于数组字段中的值。 |
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

### 示例 1：查找数组中包含全部指定元素的文档 {#example-1-find-documents-containing-all-the-specified-elements-in-an-array}

此查询检索在 `salesByCategory.categoryName` 数组中同时包含 `Laptops` 和 `Smartphones` 元素的文档。

```javascript
db.stores.find({
    "sales.salesByCategory.categoryName": {
        $all: ["Laptops", "Smartphones"]
    }
}, {
    _id: 1,
    "sales.salesByCategory.categoryName": 1
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "a57511bb-1ea3-4b26-bf0d-8bf928f2bfa8",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Smartphones"
                },
                {
                    "categoryName": "Laptops"
                }
            ]
        }
    },
    {
        "_id": "ca56d696-5208-40c3-aa04-d4e245df44dd",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Laptops"
                },
                {
                    "categoryName": "Smartphones"
                }
            ]
        }
    }
]
```
