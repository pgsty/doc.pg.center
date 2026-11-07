---
title: $sum
description: $sum 运算符根据筛选条件计算字段值的总和
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$sum.md
weight: 170
translation_source_sha256: f5e7a71db14a06d70ddb79a1f7dc80ad266c5f4611c4a4e7ecb9ce6f49f4e792
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$sum` 运算符计算满足筛选条件的字段或表达式的数值总和。

## 语法 {#syntax}

```javascript
{
  $sum: <field or expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field or expression>`** | 要计算总和的字段或表达式。可以是字段、数值或表达式。 |
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

### 示例 1：在 `$group` 中使用 `$sum` {#example-1-using-sum-in-group}

计算 2023 年所有促销活动按类别汇总的总折扣百分比：

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023
        }
    },
    {
        $group: {
            _id: "$promotionEvents.discounts.categoryName",
            totalDiscountIn2023: {
                $sum: "$promotionEvents.discounts.discountPercentage"
            }
        }
    },
    {
        $project: {
            _id: 0,
            categoryName: "$_id",
            totalDiscountIn2023: 1
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "categoryName": "Glass Frames",
        "totalDiscountIn2023": 25
    },
    {
        "categoryName": "Picture Hanging Supplies",
        "totalDiscountIn2023": 14
    }
]
```

<span id="example-2-using-sum-in-bucket"></span>

### 示例 2：在 `$bucket` 中使用 `$sum` {#example-2--using-sum-in-bucket}

获取在指定销售范围内的总销售额：

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales", // Field to group by
        boundaries: [0, 10000, 20000, 50000, 100000], // Sales ranges
        default: "Other", // Default bucket for values outside the defined ranges
        output: {
            totalSalesSum: {
                $sum: "$sales.totalSales"
            }, // Sum the sales for each bucket
            count: {
                $sum: 1
            } // Count the number of documents in each bucket
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "Other",
        "totalSalesSum": 454981695,
        "count": 3001
    },
    {
        "_id": 0,
        "totalSalesSum": 20033725,
        "count": 3903
    },
    {
        "_id": 10000,
        "totalSalesSum": 71303703,
        "count": 4712
    },
    {
        "_id": 50000,
        "totalSalesSum": 756168541,
        "count": 11025
    },
    {
        "_id": 20000,
        "totalSalesSum": 678976078,
        "count": 18861
    }
]
```

<span id="example-3-using-sum-in-set-window-fields"></span>

### 示例 3：在 `$setWindowFields` 中使用 `$sum` {#example-3-using-sum-in-setwindowfields}

计算 2023 年促销活动中各销售类别对应的总折扣：

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023
        }
    },
    {
        $setWindowFields: {
            partitionBy: "$promotionEvents.discounts.categoryName", // Group by categoryName
            output: {
                totalDiscountIn2023: {
                    $sum: "$promotionEvents.discounts.discountPercentage", // Sum discount percentage
                    window: {
                        documents: ["unbounded", "unbounded"] // Aggregate over all documents in the partition
                    }
                }
            }
        }
    },
    {
        $project: {
            _id: 0,
            categoryName: "$promotionEvents.discounts.categoryName",
            discountPercentage: "$promotionEvents.discounts.discountPercentage",
            totalDiscountIn2023: 1
        }
    },
    {
        $limit: 5
    }
])
```

此查询返回以下结果：

```json
[
    {
        "totalDiscountIn2023": 1106,
        "categoryName": "2-in-1 Laptops",
        "discountPercentage": 25
    },
    {
        "totalDiscountIn2023": 1106,
        "categoryName": "2-in-1 Laptops",
        "discountPercentage": 22
    },
    {
        "totalDiscountIn2023": 1106,
        "categoryName": "2-in-1 Laptops",
        "discountPercentage": 19
    },
    {
        "totalDiscountIn2023": 1106,
        "categoryName": "2-in-1 Laptops",
        "discountPercentage": 17
    },
    {
        "totalDiscountIn2023": 1106,
        "categoryName": "2-in-1 Laptops",
        "discountPercentage": 10
    }
]
```
