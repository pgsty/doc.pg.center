---
title: $bottomN
description: $bottomN 运算符返回按一个或多个字段排序后结果集的最后 N 个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$bottomn.md
weight: 30
translation_source_sha256: 6c9c852df03cdee71f4bb30bad63e568fb20fd2dcef337f2c87e63fc58e6cc53
translation_review: AI-assisted bilingual review; 2026-11-07
---

$bottomN 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的最后 N 个文档。

## 语法 {#syntax}

```javascript
{
    $bottomN: {
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
| **`n`** | 从排序后结果集的底部返回的文档数量 |
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

### 示例 1：按总销售额找出销售额最低的两家门店 {#example-1-find-the-bottom-two-stores-by-total-sales}

要确定 First Up Consultants 公司中销售额最低的两家门店，运行查询以获取属于 "First Up Consultants" 公司的门店，按总销售额降序排序结果文档，并返回排序后结果集中的最后两个文档。

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
        bottomSales: {
            $bottomN: {
                output: ["$company", "$sales"],
                sortBy: {
                    "sales.revenue": -1
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
    "bottomSales": [
        [
            "First Up Consultants",
            {
                "salesByCategory": [
                    {
                        "categoryName": "Skirts",
                        "totalSales": 109
                    }
                ],
                "revenue": 109
            }
        ],
        [
            "First Up Consultants",
            {
                "salesByCategory": [
                    {
                        "categoryName": "Mirrors",
                        "totalSales": 120
                    }
                ],
                "revenue": 120
            }
        ]
    ]
}
]
```

### 示例 2：在每家门店内按总销售额找出表现最差的两个类别 {#example-2-find-the-bottom-two-categories-by-total-sales-within-each-store}

为确定每家门店中总销售额最低的两个类别，运行查询以获取至少包含两个销售类别的文档，按总销售额降序排序类别，并最终为每家门店返回销售额最低的两个类别。

```javascript
db.stores.aggregate([{
    $unwind: "$sales.salesByCategory"
}, {
    $match: {
        "sales.salesByCategory.totalSales": {
            $exists: true
        }
    }
}, {
    $group: {
        _id: "$_id",
        storeName: {
            $first: "$name"
        },
        categoryCount: {
            $sum: 1
        },
        bottomTwoCategories: {
            $bottomN: {
                n: 2,
                sortBy: {
                    "sales.salesByCategory.totalSales": -1
                },
                output: {
                    categoryName: "$sales.salesByCategory.categoryName",
                    totalSales: "$sales.sale"
                }
            }
        }
    }
}, {
    $match: {
        categoryCount: {
            $gte: 2
        }
    }
}])
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "64ec6589-068a-44a6-be5b-9d37bb0a90f1",
        "storeName": "First Up Consultants | Computer Gallery - West Cathrine",
        "categoryCount": 8,
        "bottomTwoCategories": [
            {
                "categoryName": "Gaming Controllers",
                "totalSales": null
            },
            {
                "categoryName": "Network Adapters",
                "totalSales": null
            }
        ]
    }
]
```
