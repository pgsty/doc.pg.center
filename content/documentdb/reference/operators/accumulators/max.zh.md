---
title: $max
description: $max 运算符从一组输入值中返回最大值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$max.md
weight: 90
translation_source_sha256: 96969f13b89f76625a3b60ef97f0ae02d4190e1c79dbbc6ecce6419a5228c2c9
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$max` 运算符返回一组输入值中的最大值。

作为字段更新运算符使用时，`$max` 运算符会在指定值大于字段当前值时，将字段值更新为指定值。如果字段不存在，`$max` 会创建该字段并将其设置为指定值。

## 语法 {#syntax}

```javascript
$max: <expression>
```

作为字段更新运算符使用时：

```javascript
{
  $max: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 任何有效表达式，可解析为一个值。`$max` 运算符会评估此表达式以确定最大值。 |
{.fields}

作为字段更新运算符使用时：

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要用最大值更新的字段名称。 |
| **`value`** | 要与当前字段值进行比较的值。仅当该值更大时，字段才会被更新。 |
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

### 示例 1：按类别计算最高销售额 {#example-1-calculate-the-highest-sales-by-category}

要计算每个类别的最高销售额，首先运行一个查询，按销售额类别对所有文档进行分组。然后运行 $max 查询，以获取每个类别在所有商店中的最高销售额。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            maxSales: {
                $max: "$sales.salesByCategory.totalSales"
            }
        }
    }
])
```

此查询返回的前五个结果如下：

```json
[
    {
        "_id": "Christmas Trees",
        "maxSales": 49697
    },
    {
        "_id": "Nuts",
        "maxSales": 48020
    },
    {
        "_id": "Camping Tables",
        "maxSales": 48568
    },
    {
        "_id": "Music Theory Books",
        "maxSales": 46133
    },
    {
        "_id": "Fortified Wine",
        "maxSales": 49912
    }
]
```

### 示例 2：在 `$bucket` 中使用 `$max` {#example-2-using-max-in-bucket}

要检索销售额区间内的最高销售额：

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales",
        boundaries: [0, 1000, 5000, 10000],
        default: "Other",
        output: {
            maxSales: {
                $max: "$sales.totalSales"
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
        "maxSales": 4996
    },
    {
        "_id": "Other",
        "maxSales": 404106
    },
    {
        "_id": 0,
        "maxSales": 995
    },
    {
        "_id": 5000,
        "maxSales": 9999
    }
]
```

<span id="example-3-using-max-in-set-window-fields"></span>

### 示例 3：在 `$setWindowFields` 中使用 `$max` {#example-3-using-max-in-setwindowfields}

要获取 2023 年笔记本电脑的最高折扣，首先运行一个查询，展开促销事件并筛选出选定类别。然后按公司对结果文档进行分区，并计算每个分区内的最高折扣百分比。

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
                maxDiscount: {
                    $max: "$promotionEvents.discounts.discountPercentage",
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
            maxDiscount: {
                $first: "$maxDiscount"
            }
        }
    }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "Proseware, Inc.",
        "maxDiscount": 24
    },
    {
        "_id": "Fabrikam, Inc.",
        "maxDiscount": 23
    },
    {
        "_id": "Contoso, Ltd.",
        "maxDiscount": 24
    }
]
```

### 示例 4：设置最大员工容量（字段更新运算符） {#example-4-setting-maximum-staff-capacity-field-update-operator}

要仅在当前全职员工数量较低时将全职员工数量更新为 10，可在该字段上使用 $max 运算符执行更新。由于当前 `fullTime` 值为 3，而 10 大于 3，因此字段将被更新为 10。

```javascript
db.stores.updateOne(
  { _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.totalStaff.fullTime": 10
    }
  }
)
```

### 示例 5：多个字段更新（字段更新运算符） {#example-5-multiple-field-updates-field-update-operator}

要使用最大值更新多个字段，可将 $max 运算符与多个字段及其对应的最大值一起使用以设置值。

```javascript
db.stores.updateOne(
  { _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.totalStaff.partTime": 1,
      "sales.totalSales": 50000
    }
  }
)
```

在此情况下：

- `partTime`（2）将保持为 2，因为 1 < 2（不变）
- `totalSales`（31211）将更新为 50000，因为 50000 > 31211

### 示例 6：创建新字段（字段更新运算符） {#example-6-creating-new-fields-field-update-operator}

如果字段不存在，`$max` 会使用指定值创建该字段。

```javascript
db.stores.updateOne(
  { _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.maxStaffCapacity": 25,
      "sales.peakSalesRecord": 100000
    }
  }
)
```

### 示例 7：更新数组元素（字段更新运算符） {#example-7-updating-array-elements-field-update-operator}

使用位置运算符更新数组元素中的最大值。

```javascript
db.stores.updateOne(
  {
    _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "sales.salesByCategory.categoryName": "Phone Mounts"
  },
  {
    $max: {
      "sales.salesByCategory.$.totalSales": 12000
    }
  }
)
```

### 示例 8：跟踪峰值性能（字段更新运算符） {#example-8-tracking-peak-performance-field-update-operator}

设置仅在超过时才更新的峰值性能指标。

```javascript
db.stores.updateOne(
  { _id: "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "performance.peakDailySales": 5000,
      "performance.maxCustomersPerDay": 150,
      "performance.highestSalesMonth": 45000
    }
  }
)
```

执行这些字段更新操作后，更新后的文档如下：

```json
{
  "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
  "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
  "staff": {
    "totalStaff": {
      "fullTime": 10,
      "partTime": 2
    },
    "maxStaffCapacity": 25
  },
  "sales": {
    "totalSales": 50000,
    "peakSalesRecord": 100000,
    "salesByCategory": [
      {
        "categoryName": "Phone Mounts",
        "totalSales": 12000
      },
      {
        "categoryName": "Dash Cameras",
        "totalSales": 22300
      }
    ]
  },
  "performance": {
    "peakDailySales": 5000,
    "maxCustomersPerDay": 150,
    "highestSalesMonth": 45000
  },
  "lastPromotionDate": ISODate("2024-12-31T00:00:00.000Z"),
  "inventoryDeadline": ISODate("2024-06-30T00:00:00.000Z")
}
```
