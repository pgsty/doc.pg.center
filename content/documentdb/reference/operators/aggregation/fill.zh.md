---
title: $fill
description: $fill 阶段允许根据指定的方法和条件填充文档中的缺失值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$fill.md
weight: 110
translation_source_sha256: 4da25555ea527599825a5c7bc594a0bce807b79bf1a0ed5f09fb1a22d66388e9
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$fill` 流水线阶段用于在聚合流水线中填充文档内的缺失或 null 值。它提供多种方法来填充缺失数据，包括使用静态值、线性插值，或使用前一个/后一个文档的值。

## 语法 {#syntax}

```javascript
{
  $fill: {
    sortBy: <sort specification>,
    partitionBy: <partition fields>,
    partitionByFields: <array of partition field names>,
    output: {
      <field1>: { value: <expression> },
      <field2>: { method: <string> }
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`sortBy`** | 指定应用依赖文档顺序的填充方法时的文档排序顺序。 |
| **`partitionBy`** | 可选。将文档分组为分区。填充操作在每个分区内部独立应用。 |
| **`partitionByFields`** | 可选。使用字段名数组形式的 partitionBy 的替代语法。 |
| **`output`** | 指定要填充的字段以及用于填充缺失数据的方法或值。 |
{.fields}

### 填充方法 {#fill-methods}

| 方法 | 描述 |
| --- | --- |
| **`value`** | 使用指定的静态值或表达式结果进行填充。 |
| **`linear`** | 仅限数值字段，使用已知值之间的线性插值。 |
| **`locf`** | 上次观测值向前传递——使用最后一个已知值。 |
| **`linear`** | 使用周围值之间的线性插值。 |

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        }
      ]
    }
  ]
}
```

### 示例 1：使用静态值 填充缺失值 {#example-1-fill-missing-values-with-static-value}

此查询将 `salesByCategory` 数组中缺失的 `totalSales` 值填充为默认值 0。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $unwind: "$sales.salesByCategory"
}, {
    $fill: {
        output: {
            "sales.salesByCategory.totalSales": {
                value: 0
            }
        }
    }
}, {
    $group: {
        _id: "$_id",
        name: {
            $first: "$name"
        },
        salesByCategory: {
            $push: "$sales.salesByCategory"
        }
    }
}])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "affdc09c-7356-4fff-a857-e8301f57159c",
        "name": "First Up Consultants | Sports Gear Pantry - Wildermanhaven",
        "salesByCategory": [
            {
                "categoryName": "Baseball Gear",
                "totalSales": 33878
            },
            {
                "categoryName": "Volleyball Gear",
                "totalSales": 34031
            }
        ]
    },
    {
        "_id": "1cf667b4-d8ce-4f1a-bad1-a1f0bbce26c2",
        "name": "First Up Consultants | Picture Frame Variety - New Abrahamborough",
        "salesByCategory": [
            {
                "categoryName": "Picture Hanging Supplies",
                "totalSales": 7229
            },
            {
                "categoryName": "Collage Frames",
                "totalSales": 40014
            }
        ]
    }
]
```

### 示例 2：使用上次观测值向前传递方法 填充缺失的员工数据 {#example-2-fill-missing-staff-data-using-last-observation-carried-forward}

此查询在每个商店分组内，使用最后一个已知值填充缺失的兼职员工数据。

```javascript
db.stores.aggregate([{
    $fill: {
        sortBy: {
            "_id": 1
        },
        output: {
            "staff.totalStaff.partTime": {
                method: "locf"
            }
        }
    }
}, {
    $project: {
        name: 1,
        "staff.totalStaff": 1
    }
}])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "00003278-4226-4ca7-871d-e80d8f414431",
        "name": "Wide World Importers | Camera Depot - Lake Luramouth",
        "staff": {
            "totalStaff": {
                "fullTime": 20,
                "partTime": 6
            }
        }
    },
    {
        "_id": "00009bd0-c44e-4cc8-ab03-347076d74a1a",
        "name": "Wide World Importers | Music Stop - Rebeccaside",
        "staff": {
            "totalStaff": {
                "fullTime": 9,
                "partTime": 0
            }
        }
    }
]
```

### 示例 3：使用平均值 填充缺失的折扣百分比 {#example-3-fill-missing-discount-percentages-with-average-value}

此查询使用所有商店的平均折扣百分比填充缺失的折扣百分比。

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $fill: {
      partitionBy: "$promotionEvents.eventName",
      sortBy: { "promotionEvents.discounts.categoryName": 1 },
      output: {
        "promotionEvents.discounts.discountPercentage": { 
          value: { $avg: "$promotionEvents.discounts.discountPercentage" } 
        }
      }
    }
  },
  {
    $group: {
      _id: { storeId: "$_id", eventName: "$promotionEvents.eventName" },
      storeName: { $first: "$name" },
      eventName: { $first: "$promotionEvents.eventName" },
      discounts: { $push: "$promotionEvents.discounts" }
    }
  }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": {
            "storeId": "70d4cc90-23b1-46e3-8f59-630648e311a4",
            "eventName": "Price Slash Spectacular"
        },
        "storeName": "Wide World Importers | Music Bazaar - West Johnpaulhaven",
        "eventName": "Price Slash Spectacular",
        "discounts": [
            {
                "categoryName": "CDs",
                "discountPercentage": 22
            },
            {
                "categoryName": "Vinyl Records",
                "discountPercentage": 21
            }
        ]
    },
    {
        "_id": {
            "storeId": "24873ac4-b2d1-4216-a425-3375a384b23d",
            "eventName": "Massive Deal Mania"
        },
        "storeName": "Northwind Traders | Furniture Pantry - Farrellchester",
        "eventName": "Massive Deal Mania",
        "discounts": [
            {
                "categoryName": "Bookcases",
                "discountPercentage": 22
            },
            {
                "categoryName": "Cabinets",
                "discountPercentage": 8
            }
        ]
    }
]
```

## 使用场景 {#use-cases}

- **数据清洗**：填充导入数据集中的缺失值
- **时间序列数据**：使用插值处理顺序数据中的空缺
- **默认值**：为可选字段分配默认值
- **数据标准化**：确保文档间数据结构的一致性
