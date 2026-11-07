---
title: $addFields
description: 聚合流水线中的 $addFields 流水线阶段用于向文档添加新字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$addfields.md
weight: 10
translation_source_sha256: f1afd801ef8fad3ea20fe9687943927056a2c8519994772bd7ea6d3c2e12ad4b
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 $addFields 流水线阶段用于向文档添加新字段。它也可用于重置现有字段的值。当需要基于现有数据创建新字段或修改文档中的现有字段时，此阶段特别有用。

## 语法 {#syntax}

```javascript
{
  $addFields: {
    <newField1>: <expression1>,
    <newField2>: <expression2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`newField1`** | 要添加的新字段名称，或要修改的现有字段名称。 |
| **`expression1`** | 计算 newField1 值的表达式。 |
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

### 示例 1：添加新字段 {#example-1-adding-a-new-field}

此查询添加一个名为 totalDiscountEvents 的新字段，用于统计促销活动的数量。

```javascript
db.stores.aggregate([
  {
    $addFields: {
      totalDiscountEvents: { $size: "$store.promotionEvents" }
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    },
    "totalDiscountEvents": 3
  }
]
```

### 示例 2：修改现有字段 {#example-2-modifying-an-existing-field}

此查询添加一个名为 totalStaffCount 的字段，用于计算全职和兼职员工数量的总和。

```javascript
db.stores.aggregate([
  {
    $addFields: {
      totalStaffCount: {
        $add: ["$store.staff.totalStaff.fullTime", "$store.staff.totalStaff.partTime"]
      }
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "staff": {
        "totalStaff": {
          "fullTime": 12,
          "partTime": 8
        }
      }
    },
    "totalStaffCount": 20
  }
]
```

### 示例 3：添加嵌套字段 {#example-3-adding-nested-fields}

此查询添加一个嵌套字段 location.coordinates，将纬度和经度合并为一个数组。

```javascript
db.stores.aggregate([
  {
    $addFields: {
      "store.location.coordinates": ["$store.location.lat", "$store.location.lon"]
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "location": {
        "lat": 47.6097,
        "lon": -122.3331,
        "coordinates": [47.6097, -122.3331]
      }
    }
  }
]
```
