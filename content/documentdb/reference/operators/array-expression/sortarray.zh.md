---
title: $sortArray
description: $sortArray 运算符有助于对数组中的元素进行排序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$sortarray.md
weight: 120
translation_source_sha256: f9011a094d78b390efb927cbbbbc2909278de343e81b7ff3841cb43dbe4847ee
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$sortArray` 运算符用于对数组元素进行排序。当需要根据特定字段或条件对文档中的数组进行排序时，该运算符非常有用。它可以应用于嵌入文档的数组或简单值数组。

## 语法 {#syntax}

```javascript
{
  $sortArray: {
    input: <arrayExpression>,
    sortBy: <sortSpecification>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 需要排序的数组。 |
| **`sortBy`** | 指定排序顺序。可以是单个字段，也可以是多个字段及其对应的排序顺序（1 表示升序，-1 表示降序）。 |
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

### 示例 1：对嵌入文档数组排序 {#example-1-sorting-an-array-of-embedded-documents}

此查询根据 `totalSales` 对每个文档中的 `sales.salesByCategory` 数组按降序进行排序。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45"
    }
}, {
    $project: {
        sortedSalesByCategory: {
            $sortArray: {
                input: "$sales.salesByCategory",
                sortBy: {
                    totalSales: -1
                }
            }
        }
    }
}])
```

此查询返回以下结果。

```json
[
    {
        "_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45",
        "sortedSalesByCategory": [
            {
                "categoryName": "DJ Accessories",
                "totalSales": 60000
            },
            {
                "categoryName": "Music Accessories",
                "totalSales": 40000
            },
            {
                "categoryName": "DJ Speakers",
                "totalSales": 36972
            },
            {
                "categoryName": "DJ Headphones",
                "totalSales": 12877
            }
        ]
    }
]
```
