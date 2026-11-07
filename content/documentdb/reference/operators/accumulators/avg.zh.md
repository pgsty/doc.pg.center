---
title: $avg
description: $avg 运算符计算分组、分桶或窗口中文档的数值平均值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$avg.md
weight: 10
translation_source_sha256: f6beeb2f7697698bd44ee2b31bfe23b40376b8099d72604559e2b0cd5d8f81a2
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$avg` 运算符计算分组文档或在定义窗口内数值的平均值。

## 语法 {#syntax}

```javascript
$avg: <field or expression>
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field or expression>`** | 指定要计算平均值的字段或表达式。非数值类型值将被忽略。 |
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

### 示例 1：按类别计算平均销售额 {#example-1-calculate-the-average-sales-by-category}

要计算每个类别中所有商店的平均销售额，首先运行一个查询，将文档按销售类别分组。然后，计算每个组内所有文档的平均销售额。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            avgSales: {
                $avg: "$sales.salesByCategory.totalSales"
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
        "avgSales": 25987.956989247312
    },
    {
        "_id": "Nuts",
        "avgSales": 25115.98795180723
    },
    {
        "_id": "Camping Tables",
        "avgSales": 25012.546153846153
    },
    {
        "_id": "Music Theory Books",
        "avgSales": 26138.80769230769
    },
    {
        "_id": "Fortified Wine",
        "avgSales": 24748.672727272726
    },
    {
        "_id": "Children's Mystery",
        "avgSales": 23764.044444444444
    },
    {
        "_id": "Short Throw Projectors",
        "avgSales": 27157.472222222223
    },
    {
        "_id": "Pliers",
        "avgSales": 26712.875
    },
    {
        "_id": "Bluetooth Headphones",
        "avgSales": 26311.58653846154
    },
    {
        "_id": "Video Storage",
        "avgSales": 26121.475
    },
    {
        "_id": "Cleansers",
        "avgSales": 25836.397058823528
    },
    {
        "_id": "Camera Straps",
        "avgSales": 22487.609375
    },
    {
        "_id": "Carry-On Bags",
        "avgSales": 24294.263157894737
    },
    {
        "_id": "Disinfectant Wipes",
        "avgSales": 27066.929411764704
    },
    {
        "_id": "Insignia Smart TVs",
        "avgSales": 27096.83950617284
    },
    {
        "_id": "Toner Refill Kits",
        "avgSales": 24963.71052631579
    },
    {
        "_id": "iPads",
        "avgSales": 22583.882352941175
    },
    {
        "_id": "Memory Foam Mattresses",
        "avgSales": 28073.05172413793
    },
    {
        "_id": "Storage Baskets",
        "avgSales": 24092.514705882353
    },
    {
        "_id": "Body Spray",
        "avgSales": 26080.84375
    }
]
```

### 示例 2：在 `$bucket` 中使用 `$avg` {#example-2-using-avg-in-bucket}

要获取特定销售额范围内的平均销售额，此查询根据销售额值创建分桶，并计算每个分桶内的平均销售额。

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales",
        boundaries: [0, 1000, 5000, 10000],
        default: "Other",
        output: {
            avgSales: {
                $avg: "$sales.totalSales"
            }
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": 1000,
        "avgSales": 3029.053674121406
    },
    {
        "_id": "Other",
        "avgSales": 52169.85442987472
    },
    {
        "_id": 0,
        "avgSales": 576.3164179104477
    },
    {
        "_id": 5000,
        "avgSales": 7538.786819770345
    }
]
```

<span id="example-3-using-avg-in-set-window-fields"></span>

### 示例 3：在 `$setWindowFields` 中使用 `$avg` {#example-3-using-avg-in-setwindowfields}

要获取 2023 年每家商店中 "Laptops" 类别的平均折扣，首先运行查询，按公司对商店进行分区，并筛选 "Laptops" 类别的折扣促销活动。然后计算每个分区结果集内的平均折扣百分比。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },

    // Filter only Laptops category and events in 2023
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023,
            "promotionEvents.discounts.categoryName": "Laptops"
        }
    },

    // Use $setWindowFields to calculate average discount by city
    {
        $setWindowFields: {
            partitionBy: "$company",
            output: {
                avgDiscount: {
                    $avg: "$promotionEvents.discounts.discountPercentage",
                    window: {
                        documents: ["unbounded", "unbounded"]
                    }
                }
            }
        }
    },

    // Group by city to return one result per city
    {
        $group: {
            _id: "$company",
            avgDiscount: {
                $first: "$avgDiscount"
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
        "avgDiscount": 14.461538461538462
    },
    {
        "_id": "Proseware, Inc.",
        "avgDiscount": 16.25
    },
    {
        "_id": "Fabrikam, Inc.",
        "avgDiscount": 14.454545454545455
    },
    {
        "_id": "Contoso, Ltd.",
        "avgDiscount": 14.384615384615385
    },
    {
        "_id": "Fourth Coffee",
        "avgDiscount": 13.625
    },
    {
        "_id": "Trey Research",
        "avgDiscount": 17.785714285714285
    },
    {
        "_id": "Adatum Corporation",
        "avgDiscount": 11.666666666666666
    },
    {
        "_id": "Relecloud",
        "avgDiscount": 14.375
    },
    {
        "_id": "Lakeshore Retail",
        "avgDiscount": 15.846153846153847
    },
    {
        "_id": "Northwind Traders",
        "avgDiscount": 14.2
    },
    {
        "_id": "First Up Consultants",
        "avgDiscount": 11.25
    },
    {
        "_id": "Wide World Importers",
        "avgDiscount": 15.571428571428571
    },
    {
        "_id": "Tailwind Traders",
        "avgDiscount": 16.166666666666668
    }
]
```
