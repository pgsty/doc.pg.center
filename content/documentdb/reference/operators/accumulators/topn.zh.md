---
title: $topN
description: $topN 运算符返回按一个或多个字段排序后结果集中的前 N 个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$topn.md
weight: 190
translation_source_sha256: f6419f773ab1143b64827f114da6fff84371f9ff1ed6b4de3090557bba64d347
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> `listOfFields` 一行写的是“最后一个文档”，与简介中的“前 N 个文档”不一致。应结合示例中的排序和选取方式理解这一行。

`$topN` 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的前 N 个文档。该运算符扩展了 `$top` 的功能，允许你获取多个最高排名的元素，而不仅限于单一最高排名项。

## 语法 {#syntax}

```javascript
{
    $topN: {
        output: [listOfFields],
        sortBy: {
            <fieldName>: < sortOrder >
        },
        n: < numDocumentsToReturn >
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`listOfFields`** | 返回结果集中最后一个文档的字段列表 |
| **`fieldName`** | 用于对结果集进行排序的字段 |
| **`sortOrder`** | 1 或 -1。1 表示按字段值升序排序，-1 表示按字段值降序排序 |
| **`n`** | 从排序后结果集顶部返回的文档数量 |
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

<span id="example-1-get-the-two-stores-with-the-lowest-total-sales"></span>

### 示例 1 - 获取总销售额最低的两个门店 {#example-1---get-the-two-stores-with-the-lowest-total-sales}

要获取 First Up Consultants 公司内销售额最低的两个门店，请运行一个查询，筛选公司名称，按销售额升序排序结果文档，并从排序后的结果集中返回前两个文档。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $group: {
        _id: "$company",
        topSales: {
            $topN: {
                output: ["$company", "$sales"],
                sortBy: {
                    "sales.totalSales": 1
                },
                n: 2
            }
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "First Up Consultants",
        "topSales": [
            [
                "First Up Consultants",
                {
                    "salesByCategory": [
                        {
                            "categoryName": "Towel Sets",
                            "totalSales": 520
                        },
                        {
                            "categoryName": "Bath Accessories",
                            "totalSales": 41710
                        },
                        {
                            "categoryName": "Drapes",
                            "totalSales": 42893
                        },
                        {
                            "categoryName": "Towel Racks",
                            "totalSales": 30773
                        },
                        {
                            "categoryName": "Hybrid Mattresses",
                            "totalSales": 39491
                        },
                        {
                            "categoryName": "Innerspring Mattresses",
                            "totalSales": 6410
                        },
                        {
                            "categoryName": "Bed Frames",
                            "totalSales": 41917
                        },
                        {
                            "categoryName": "Mattress Protectors",
                            "totalSales": 44124
                        },
                        {
                            "categoryName": "Bath Towels",
                            "totalSales": 5671
                        },
                        {
                            "categoryName": "Turkish Towels",
                            "totalSales": 25674
                        }
                    ],
                    "revenue": 279183
                }
            ],
            [
                "First Up Consultants",
                {
                    "salesByCategory": [
                        {
                            "categoryName": "Lavalier Microphones",
                            "totalSales": 40000
                        },
                        {
                            "categoryName": "Wireless Microphones",
                            "totalSales": 39691
                        }
                    ],
                    "minimumSalesTarget": 30000,
                    "revenue": 50000
                }
            ]
        ]
    }
]
```

### 示例 2：获取每个门店最近的两次促销活动 {#example-2-get-the-two-most-recent-promotion-events}

要查找每个门店最近的两次促销活动，请按门店对集合中的文档进行分组，按促销日期升序排序，并为每个门店从排序结果集中返回前两个结果。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            top2RecentPromotions: {
                $topN: {
                    n: 2,
                    sortBy: {
                        "promotionEvents.promotionalDates.startDate.Year": -1,
                        "promotionEvents.promotionalDates.startDate.Month": -1,
                        "promotionEvents.promotionalDates.startDate.Day": -1
                    },
                    output: {
                        eventName: "$promotionEvents.eventName",
                        startDate: "$promotionEvents.promotionalDates.startDate"
                    }
                }
            }
        }
    }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "4a99546f-a1d2-4e61-ae9f-b8c7c1faf73c'",
        "storeName": "Lakeshore Retail | Stationery Nook - West Van",
        "top2RecentPromotions": [
            {
                "eventName": "Crazy Markdown Madness",
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                }
            },
            {
                "eventName": "Flash Sale Fiesta",
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                }
            }
        ]
    },
    {
        "_id": "e0c47a06-4fe0-46b7-a309-8971bbb3978f",
        "storeName": "VanArsdel, Ltd. | Baby Products Bargains - Elainamouth",
        "top2RecentPromotions": [
            {
                "eventName": "Crazy Deal Days",
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                }
            }
        ]
    }
]
```
