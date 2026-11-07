---
title: $first
description: $first 运算符根据分组的排序顺序返回该组中的第一个值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$first.md
weight: 50
translation_source_sha256: a6b09026c2495e374b57a36a238f69bd62918231e1337ec611dbc089da1b092d
translation_review: AI-assisted bilingual review; 2026-11-07
---

$first 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的第一个文档。如果未指定排序顺序，则顺序是未定义的。

## 语法 {#syntax}

```javascript
{
    $first: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要计算并从结果集中返回第一个文档的表达式 |
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

### 示例 1：获取上次更新时间最早的文档 {#example-1-get-the-least-recently-updated-document}

要检索 First Up Consultants 公司下上次更新时间最早的商店文档，运行查询以获取属于 "First Up Consultants" 公司的所有文档，按 lastUpdated 字段升序对结果文档排序，并返回结果集中的第一个文档。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $sort: {
        lastUpdated: 1
    }
}, {
    $group: {
        _id: "$company",
        firstUpdated: {
            $first: "$lastUpdated"
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
      "_id": "First Up Consultants",
      "firstUpdated": "ISODate('2025-06-11T10:48:01.291Z')"
  }
]
```

### 示例 2：按销售额获取每个商店的第一个类别 {#example-2-get-first-category-by-sales-amount-per-store}

要检索每个商店内按字母顺序排列的第一个类别，运行查询以对每个商店内的销售类别列表进行排序，并返回每个商店排序结果集中的第一个类别。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $sort: {
            "_id": 1,
            "sales.salesByCategory.categoryName": 1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            totalSales: {
                $first: "$sales.totalSales"
            },
            firstCategory: {
                $first: {
                    categoryName: "$sales.salesByCategory.categoryName",
                    categoryTotalSales: "$sales.salesByCategory.totalSales"
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
        "_id": "64ec6589-068a-44a6-be5b-9d37bb0a90f1",
        "storeName": "First Up Consultants | Computer Gallery - West Cathrine",
        "totalSales": 186829,
        "firstCategory": {
            "categoryName": "Cases",
            "categoryTotalSales": 36386
        }
    },
    {
        "_id": "14343900-2a5c-44bf-a52b-9efe63579866",
        "storeName": "Northwind Traders | Home Improvement Closet - West Evanside",
        "totalSales": 35371,
        "firstCategory": {
            "categoryName": "Doors",
            "categoryTotalSales": 21108
        }
    }
]
```

### 示例 3：按开始日期获取每个商店的第一个促销活动 {#example-3-get-first-promotion-event-per-store}

要检索每个商店的第一个促销活动，请运行查询以按 startDate 对每个商店内的促销活动列表进行排序，并返回每个商店排序结果集中的第一个活动。

根据开始日期，获取每个商店的第一个促销活动。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $sort: {
            "_id": 1,
            "promotionEvents.promotionalDates.startDate.Year": 1,
            "promotionEvents.promotionalDates.startDate.Month": 1,
            "promotionEvents.promotionalDates.startDate.Day": 1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            firstPromotionEvent: {
                $first: {
                    eventName: "$promotionEvents.eventName",
                    startYear: "$promotionEvents.promotionalDates.startDate.Year",
                    startMonth: "$promotionEvents.promotionalDates.startDate.Month"
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
        "_id": "64ec6589-068a-44a6-be5b-9d37bb0a90f1",
        "storeName": "First Up Consultants | Computer Gallery - West Cathrine",
        "firstPromotionEvent": {
            "eventName": "Crazy Markdown Madness",
            "startYear": 2024,
            "startMonth": 6
        }
    },
    {
        "_id": "a58d0356-493b-44e6-afab-260aa3296930",
        "storeName": "Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie",
        "firstPromotionEvent": {
            "eventName": "Price Drop Palooza",
            "startYear": 2023,
            "startMonth": 9
        }
    }
]
```
