---
title: $size
description: $size 运算符用于查询数组字段包含指定元素数量的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-query/$size.md
weight: 30
translation_source_sha256: 99209fb84a90f6353fecc04545333d0fff4a6114148b7a6bfb587f2bc3689ead
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$size` 运算符用于查询数组字段包含指定数量元素的文档。当需要根据数组字段的大小查找文档时，可以使用此运算符，例如查找列表中包含一定数量条目的文档。

## 语法 {#syntax}

```javascript
db.collection.find({ <field>: { $size: <number> } })
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 包含数组的字段。 |
| **`number`** | 数组应包含的元素数量。 |
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

### 示例 1：查找数组中包含特定数量元素的文档 {#example-1-finding-documents-with-a-specific-number-of-elements-in-an-array}

此查询从 `stores` 集合中检索 `sales.salesByCategory` 数组恰好包含七个元素的文档。

```javascript
db.stores.find({
    "sales.salesByCategory": {
        $size: 7
    }
}, {
    _id: 1,
    name: 1,
    "sales.salesByCategory": 1
}).limit(2)
```

此查询返回以下结果：

```json
[
    {
        "_id": "7ed4b356-1290-433e-bd96-bf95f817eaaa",
        "name": "Wide World Importers",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Ultrabooks",
                    "totalSales": 31304
                },
                {
                    "categoryName": "Laptop Accessories",
                    "totalSales": 10044
                },
                {
                    "categoryName": "Laptops",
                    "totalSales": 48851
                },
                {
                    "categoryName": "Refill Kits",
                    "totalSales": 9604
                },
                {
                    "categoryName": "Prepaid Phones",
                    "totalSales": 28600
                },
                {
                    "categoryName": "Android Phones",
                    "totalSales": 4580
                },
                {
                    "categoryName": "Photo Printers",
                    "totalSales": 35234
                }
            ]
        }
    },
    {
        "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
        "name": "Lakeshore Retail",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Towel Racks",
                    "totalSales": 13237
                },
                {
                    "categoryName": "Washcloths",
                    "totalSales": 44315
                },
                {
                    "categoryName": "Face Towels",
                    "totalSales": 42095
                },
                {
                    "categoryName": "Toothbrush Holders",
                    "totalSales": 47912
                },
                {
                    "categoryName": "Hybrid Mattresses",
                    "totalSales": 48660
                },
                {
                    "categoryName": "Napkins",
                    "totalSales": 31439
                },
                {
                    "categoryName": "Pillow Cases",
                    "totalSales": 38833
                }
            ]
        }
    }
]
```
