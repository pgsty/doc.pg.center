---
title: $count
description: '`$count` 运算符用于计算符合查询过滤条件的文档数量。'
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$count.md
weight: 40
translation_source_sha256: 2e476d333255f05812c348790ef661e46c60380d6228d8d1ac9248545278bdb8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$count` 运算符用于计算符合指定查询过滤条件的文档数量。计数运算符适用于数据汇总或为特定分组生成计数。

## 语法 {#syntax}

```javascript
{
    $count: "<fieldName>"
}
```

## 参数 {#parameters}

| 参数      | 描述                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **`<fieldName>`** | 输出文档中存储计数结果的字段名称。|
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

### 示例 1：检索所有文档的计数 {#example-1-retrieve-the-count-of-all-documents}

要检索集合中所有文档的数量，只需运行不带查询过滤条件的计数查询。

```javascript
db.stores.aggregate([{
    $count: "totalDocuments"
}])
```

此查询返回以下结果：

```json
[
    {
        "totalDocuments": 41501
    }
]
```

### 示例 2：按特定字段分组统计文档数量 {#example-2-count-documents-grouped-by-a-specific-field}

要获取每个销售类别的文档数量，首先运行按销售类别分组的查询。然后在每个类别内运行计数查询。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            totalCount: {
                $count: {}
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "Christmas Trees",
        "totalCount": 93
    },
    {
        "_id": "Nuts",
        "totalCount": 83
    },
    {
        "_id": "Camping Tables",
        "totalCount": 130
    },
    {
        "_id": "Music Theory Books",
        "totalCount": 52
    },
    {
        "_id": "Fortified Wine",
        "totalCount": 55
    },
    {
        "_id": "Children's Mystery",
        "totalCount": 45
    },
    {
        "_id": "Short Throw Projectors",
        "totalCount": 72
    },
    {
        "_id": "Pliers",
        "totalCount": 56
    },
    {
        "_id": "Bluetooth Headphones",
        "totalCount": 104
    },
    {
        "_id": "Video Storage",
        "totalCount": 80
    },
    {
        "_id": "Cleansers",
        "totalCount": 68
    },
    {
        "_id": "Camera Straps",
        "totalCount": 64
    },
    {
        "_id": "Carry-On Bags",
        "totalCount": 57
    },
    {
        "_id": "Disinfectant Wipes",
        "totalCount": 85
    },
    {
        "_id": "Insignia Smart TVs",
        "totalCount": 81
    },
    {
        "_id": "Toner Refill Kits",
        "totalCount": 38
    },
    {
        "_id": "iPads",
        "totalCount": 51
    },
    {
        "_id": "Memory Foam Mattresses",
        "totalCount": 58
    },
    {
        "_id": "Storage Baskets",
        "totalCount": 68
    },
    {
        "_id": "Body Spray",
        "totalCount": 96
    }
]
```

### 示例 3：统计促销活动数量 {#example-3-count-the-number-of-promotion-events}

要统计所有商店中促销活动的总数，首先运行展开促销活动的查询，然后统计不同促销活动的数量。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $count: "totalPromotionEvents"
    }
])
```

此查询返回以下结果：

```json
[
    {
        "totalPromotionEvents": 145673
    }
]
```

<span id="example-4-using-count-in-set-window-fields"></span>

### 示例 4：在 `$setWindowFields` 中使用 `$count` {#example-4-using-count-in-setwindowfields}

要获取每家商店的 Laptops 促销销售情况，首先运行查询，筛选 2023 年的笔记本电脑促销活动。然后按公司对结果中的商店进行分区。最后，对分区后的商店执行计数查询并返回结果。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    // Filter only for Laptop discounts in 2023
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023,
            "promotionEvents.discounts.categoryName": "Laptops"
        }
    },
    // Add sales count by city using window function
    {
        $setWindowFields: {
            partitionBy: "$company",
            output: {
                salesCount: {
                    $count: {},
                    window: {
                        documents: ["unbounded", "unbounded"]
                    }
                }
            }
        }
    },
    // Group to return a single result per city
    {
        $group: {
            _id: "$company",
            salesCount: {
                $first: "$salesCount"
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "VanArsdel, Ltd.",
        "salesCount": 13
    },
    {
        "_id": "Proseware, Inc.",
        "salesCount": 12
    },
    {
        "_id": "Fabrikam, Inc.",
        "salesCount": 11
    },
    {
        "_id": "Contoso, Ltd.",
        "salesCount": 13
    },
    {
        "_id": "Fourth Coffee",
        "salesCount": 8
    },
    {
        "_id": "Trey Research",
        "salesCount": 14
    },
    {
        "_id": "Adatum Corporation",
        "salesCount": 12
    },
    {
        "_id": "Relecloud",
        "salesCount": 16
    },
    {
        "_id": "Lakeshore Retail",
        "salesCount": 13
    },
    {
        "_id": "Northwind Traders",
        "salesCount": 5
    },
    {
        "_id": "First Up Consultants",
        "salesCount": 4
    },
    {
        "_id": "Wide World Importers",
        "salesCount": 7
    },
    {
        "_id": "Tailwind Traders",
        "salesCount": 12
    }
]
```
