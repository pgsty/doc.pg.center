---
title: $bottom
description: $bottom 运算符返回按一个或多个字段排序后的查询结果集中的最后一个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$bottom.md
weight: 20
translation_source_sha256: 13c4f892f356734dccec4fd5d591de2f73759acad653f07abc00479a7945eb12
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bottom` 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的最后一个文档。

## 语法 {#syntax}

```javascript
{
    $bottom: {
        output: [listOfFields],
        sortBy: {
            <fieldName>: < sortOrder >
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`listOfFields`** | 从结果集中的最后一个文档返回的字段列表 |
| **`fieldName`** | 用于对结果集进行排序的字段 |
| **`sortOrder`** | 1 或 -1。1 表示按字段值升序排序，-1 表示按字段值降序排序 |
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

### 示例 1：查找总销售额最低的门店 {#example-1-find-the-store-with-lowest-total-sales}

假设要确定 First Up Consultants 公司中总销售额最低的门店，可运行查询以获取该公司内的文档，按总销售额降序排序，并返回排序后结果集中的最后一个文档。

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
            $bottom: {
                output: ["$company", "$sales"],
                sortBy: {
                    "sales.revenue": -1
                }
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
        "First Up Consultants",
        {
            "totalSales": 119,
            "salesByCategory": [
                {
                    "categoryName": "Skirts",
                    "totalSales": 109
                }
            ]
        }
    ]
}]
```

### 示例 2：查找每个门店销售额最低的类别 {#example-2-find-the-category-per-store-with-the-lowest-sales}

要查找每个门店销售额最低的类别，可运行一个查询以获取包含多个销售类别的门店，按每个门店内总销售额降序排序类别，并返回排序后结果集中的最后一个文档。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $match: {
            "sales.salesByCategory.totalSales": {
                $exists: true
            }
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            lowestCategory: {
                $bottom: {
                    sortBy: {
                        "sales.salesByCategory.totalSales": 1
                    },
                    output: {
                        categoryName: "$sales.salesByCategory.categoryName",
                        totalSales: "$sales.salesByCategory.totalSales"
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
    "_id": "b1d86d1f-8705-4157-b64c-a9eda0df4921",
    "storeName": "VanArsdel, Ltd. | Baby Products Haven - West Kingfort",
    "lowestCategory": { "categoryName": "Baby Monitors", "totalSales": 49585 }
  },
  {
    "_id": "22e6367e-8341-415f-9795-118d2b522abf",
    "storeName": "Adatum Corporation | Outdoor Furniture Mart - Port Simone",
    "lowestCategory": { "categoryName": "Outdoor Benches", "totalSales": 4976 }
  }
]
```
