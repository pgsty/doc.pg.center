---
title: $min
description: $min 运算符用于检索指定字段的最小值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$min.md
weight: 120
translation_source_sha256: a712cc48259f38d617fd9ef813570b3929f7ce4ffe15e9f3a7b2a67cc001e3b1
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$min` 运算符可在聚合流水线阶段（如 `$group`、`$bucket`、`$bucketAuto` 或 `$setWindowFields`）中使用。min 运算符特别适用于数据汇总或查找数据集中的最小值。

作为字段更新运算符使用时，`$min` 运算符会在指定值小于字段当前值时，将字段值更新为指定值。如果字段不存在，`$min` 会创建该字段并将其设置为指定值。

## 语法 {#syntax}

```javascript
$min: <expression>
```

`<expression>` 可以是字段路径，也可以是指定用于最小值计算的值的聚合表达式。

作为字段更新运算符：

```javascript
{
  $min: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 指定用于确定最小值的字段或计算值。 |
{.fields}

作为字段更新运算符：

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要用最小值更新的字段名称。 |
| **`value`** | 与当前字段值进行比较的值。仅当该值更小时，字段才会被更新。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### 示例 1：在 `$group` 中使用 `$min` {#example-1-using-min-in-group}

此查询通过先按销售类别分组文档，再计算每个类别内的最小销售量，来计算 `sales.salesByCategory` 数组中每个类别的最小销售值。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            minSales: {
                $min: "$sales.salesByCategory.totalSales"
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
    {
        "_id": "Christmas Trees",
        "minSales": 391
    },
    {
        "_id": "Nuts",
        "minSales": 257
    },
    {
        "_id": "Camping Tables",
        "minSales": 171
    },
    {
        "_id": "Music Theory Books",
        "minSales": 323
    },
    {
        "_id": "Fortified Wine",
        "minSales": 521
    },
    {
        "_id": "Children's Mystery",
        "minSales": 1470
    },
    {
        "_id": "Short Throw Projectors",
        "minSales": 111
    },
    {
        "_id": "Pliers",
        "minSales": 1981
    },
    {
        "_id": "Bluetooth Headphones",
        "minSales": 465
    },
    {
        "_id": "Video Storage",
        "minSales": 1568
    },
    {
        "_id": "Cleansers",
        "minSales": 170
    },
    {
        "_id": "Camera Straps",
        "minSales": 127
    },
    {
        "_id": "Carry-On Bags",
        "minSales": 149
    },
    {
        "_id": "Disinfectant Wipes",
        "minSales": 647
    },
    {
        "_id": "Insignia Smart TVs",
        "minSales": 451
    },
    {
        "_id": "Toner Refill Kits",
        "minSales": 3525
    },
    {
        "_id": "iPads",
        "minSales": 325
    },
    {
        "_id": "Storage Baskets",
        "minSales": 1151
    },
    {
        "_id": "Memory Foam Mattresses",
        "minSales": 422
    },
    {
        "_id": "Body Spray",
        "minSales": 448
    }
]
```

### 示例 2：在 `$bucket` 中使用 `$min` {#example-2-using-min-in-bucket}

此查询根据销售值创建桶，并计算每个桶的最小销售值。

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales",
        boundaries: [0, 1000, 5000, 10000],
        default: "Other",
        output: {
            minSales: {
                $min: "$sales.totalSales"
            }
        }
    }
}])
```

此查询返回以下结果。

```json
[
    {
        "_id": 1000,
        "minSales": 1000
    },
    {
        "_id": "Other",
        "minSales": null
    },
    {
        "_id": 0,
        "minSales": 108
    },
    {
        "_id": 5000,
        "minSales": 5001
    }
]
```

<span id="example-3-using-min-in-set-window-fields"></span>

### 示例 3：在 `$setWindowFields` 中使用 `$min` {#example-3-using-min-in-setwindowfields}

此查询按公司检索 2023 年 "Laptops" 类别的最小折扣：

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
                minDiscount: {
                    $min: "$promotionEvents.discounts.discountPercentage",
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
            minDiscount: {
                $first: "$minDiscount"
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
    {
        "_id": "VanArsdel, Ltd.",
        "minDiscount": 6
    },
    {
        "_id": "Proseware, Inc.",
        "minDiscount": 8
    },
    {
        "_id": "Fabrikam, Inc.",
        "minDiscount": 5
    },
    {
        "_id": "Contoso, Ltd.",
        "minDiscount": 5
    },
    {
        "_id": "Fourth Coffee",
        "minDiscount": 6
    },
    {
        "_id": "Trey Research",
        "minDiscount": 7
    },
    {
        "_id": "Adatum Corporation",
        "minDiscount": 5
    },
    {
        "_id": "Relecloud",
        "minDiscount": 5
    },
    {
        "_id": "Lakeshore Retail",
        "minDiscount": 7
    },
    {
        "_id": "Northwind Traders",
        "minDiscount": 8
    },
    {
        "_id": "First Up Consultants",
        "minDiscount": 9
    },
    {
        "_id": "Wide World Importers",
        "minDiscount": 10
    },
    {
        "_id": "Tailwind Traders",
        "minDiscount": 5
    }
]
```

### 示例 4：设置最低人员要求（字段更新运算符） {#example-4-setting-minimum-staff-requirements-field-update-operator}

为设置最低人员要求，仅当当前字段值更高时才更新全职员工数量。由于当前 `fullTime` 值为 14，而 10 小于 14，因此字段将被更新为 10。

```javascript
db.stores.updateOne(
  { _id: "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.totalStaff.fullTime": 10
    }
  }
)
```

### 示例 5：多个字段更新（字段更新运算符） {#example-5-multiple-field-updates-field-update-operator}

要同时用最小值更新多个字段，请使用 $min 运算符配合多个字段及其对应的最小值。

```javascript
db.stores.updateOne(
  { _id: "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.totalStaff.partTime": 12,
      "sales.totalSales": 50000
    }
  }
)
```

在此情况下：

- `partTime` (8) 将更新为 8，因为 12 > 8（无变化）
- `totalSales` (83865) 将更新为 50000，因为 50000 < 83865

### 示例 6：创建新字段（字段更新运算符） {#example-6-creating-new-fields-field-update-operator}

如果字段不存在，`$min` 会以指定值创建该字段。

```javascript
db.stores.updateOne(
  { _id: "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.minStaffRequired": 15,
      "sales.minimumSalesTarget": 30000
    }
  }
)
```

### 示例 7：处理日期（字段更新运算符） {#example-7-working-with-dates-field-update-operator}

设置最小日期以跟踪最早事件。

```javascript
db.stores.updateOne(
  { _id: "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "lastInventoryCheck": new Date("2024-01-15"),
      "firstSaleDate": new Date("2023-06-01")
    }
  }
)
```

### 示例 8：更新数组元素（字段更新运算符） {#example-8-updating-array-elements-field-update-operator}

使用位置运算符更新数组元素中的最小值。

```javascript
db.stores.updateOne(
  {
    _id: "26afb024-53c7-4e94-988c-5eede72277d5",
    "sales.salesByCategory.categoryName": "Lavalier Microphones"
  },
  {
    $min: {
      "sales.salesByCategory.$.totalSales": 40000
    }
  }
)
```

执行这些字段更新操作后，更新后的文档如下：

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "staff": {
    "totalStaff": {
      "fullTime": 10,
      "partTime": 8
    },
    "minStaffRequired": 15
  },
  "sales": {
    "totalSales": 50000,
    "minimumSalesTarget": 30000,
    "salesByCategory": [
      {
        "categoryName": "Lavalier Microphones",
        "totalSales": 40000
      },
      {
        "categoryName": "Wireless Microphones",
        "totalSales": 39691
      }
    ]
  },
  "lastInventoryCheck": ISODate("2024-01-15T00:00:00.000Z"),
  "firstSaleDate": ISODate("2023-06-01T00:00:00.000Z")
}
```
