---
title: $top
description: $top 运算符返回按一个或多个字段排序后的结果集中的第一个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$top.md
weight: 180
translation_source_sha256: 1fa76fb8ddd3ef9c51ea85a78003b8e6e5023288df82dc947251ebb82632240b
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> `listOfFields` 一行写的是“最后一个文档”，与简介中的“第一个文档”不一致。示例按降序排序，并选取排序后的首项。

`$top` 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的第一个文档。该运算符将排序和选择合并为单一操作，从而高效地查找最高或最低值，而无需单独的排序阶段。

## 语法 {#syntax}

```javascript
{
    $top: {
      output: [listOfFields],
      sortBy: {
          < fieldName >: < sortOrder >
      }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`listOfFields`** | 返回结果集中最后一个文档的字段列表 |
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

### 示例 1：获取每个商店的最高销售额类别 {#example-1-get-the-top-selling-category-per-store}

要查找 First Up Consultants 公司内销售额最高的类别，请运行查询以检索该公司内的商店，按每个类别的总销售额降序排序文档，并返回排序后结果集中的第一个文档。

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
            $top: {
                output: ["$company", "$sales"],
                sortBy: {
                    "sales.totalSales": -1
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
        "topSales": [
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
        ]
    }
]
```

### 示例 2：获取每个促销类别的最高折扣 {#example-2-get-the-highest-discount-by-promotion-category}

要获取每个销售类别的最高折扣，请先运行查询按商店分组所有文档，然后按每个促销活动内的折扣百分比降序排序文档，并为每个商店返回排序后结果集中的第一个文档。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            highestDiscount: {
                $top: {
                    sortBy: {
                        "promotionEvents.discounts.discountPercentage": -1
                    },
                    output: {
                        categoryName: "$promotionEvents.discounts.categoryName",
                        discountPercentage: "$promotionEvents.discounts.discountPercentage",
                        eventName: "$promotionEvents.eventName"
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
        "_id": "64ec6589-068a-44a6-be5b-9d37bb0a90f1",
        "storeName": "First Up Consultants | Computer Gallery - West Cathrine",
        "highestDiscount": {
            "categoryName": "Gaming Accessories",
            "discountPercentage": 24,
            "eventName": "Crazy Markdown Madness"
        }
    },
    {
        "_id": "a58d0356-493b-44e6-afab-260aa3296930",
        "storeName": "Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie",
        "highestDiscount": {
            "categoryName": "Fire Pits",
            "discountPercentage": 22,
            "eventName": "Savings Showdown"
        }
    }
]
```
