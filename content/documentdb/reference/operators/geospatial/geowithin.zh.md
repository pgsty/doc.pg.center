---
title: $geoWithin
description: $geoWithin 运算符选择 location 字段完全位于指定几何对象内部的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$geowithin.md
weight: 60
translation_source_sha256: 017e50a97e879decb015f22fbb6892edaf910a5bfdd1fdbb1584beaddc1d1787
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$geoWithin` 运算符选择 location 字段完全位于指定几何对象内部的文档。该运算符支持多种形状运算符，包括 `$box`、`$polygon`、`$center` 和 `$geometry`。

## 语法 {#syntax}

```javascript
// Using $box
{
  <location field>: {
    $geoWithin: {
      $box: [ [ <bottom left coordinates> ], [ <upper right coordinates> ] ]
    }
  }
}

// Using $center
{
  <location field>: {
    $geoWithin: {
      $center: [ [ <x>, <y> ], <radius> ]
    }
  }
}

// Using $geometry
{
  <location field>: {
    $geoWithin: {
      $geometry: {
        type: <GeoJSON type>,
        coordinates: <coordinates>
      }
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `location field` | 包含位置坐标的字段 |
| `$box` | 定义矩形框两个对角点的两组坐标 |
| `$center` | 中心点坐标和以度为单位的半径 |
| `$geometry` | 定义边界的 GeoJSON 对象 |
{.fields}

## 示例 {#examples}

下面通过 `stores` 数据集中的示例 JSON 了解其用法。

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

### 示例 1：查找 $box 所定义区域内的商店 {#example-1-find-stores-defined-by-box}

为提高性能，请确保已创建 `2dsphere` 索引。

```javascript
db.stores.createIndex({ location: "2dsphere" })
```

此查询查找位于地图上特定矩形区域内的商店，该区域由一个矩形框（边界矩形）定义。

```javascript
db.stores.find({
  location: {
    $geoWithin: {
      $box: [
        [65.0, 65.0],    // Bottom left corner
        [75.0, 75.0]     // Top right corner
      ]
    }
  }
}, {
  name: 1,
  location: 1
}).limit(2)
```

此查询返回的前两个结果如下。

```json
[
 {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "location": {
      "lat": 70.1272,
      "lon": 69.7296,
      "address": "123 Entertainment Blvd",
      "city": "East Linwoodbury"
    }
  },
  {
    "_id": "fc286536-cb94-45aa-b975-7040fde04cf7",
    "name": "First Up Consultants | Medical Supply Corner - South Elnoraview",
    "location": {
      "lat": 72.2184,
      "lon": 68.9829
    }
  }
]
```

### 示例 2：查找 $center 所定义区域内的商店 {#example-2-find-stores-defined-by-center}

此查询使用 `$geoWithin` 运算符，查找由中心点和半径定义的圆形区域内的商店。

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $center: [
        [-82.5543, -65.105],  // Center point (Wide World Importers location)
        5                     // Radius in degrees
      ]
    }
  }
}, {
  name: 1,
  location: 1
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "3e962dd0-dffb-49d6-8a96-1d29fa1553d2",
    "name": "Tailwind Traders | Book Center - Lake Marlen",
    "location": { "lat": -85.4034, "lon": -65.9189 }
  },
  {
    "_id": "7e442816-be4c-4919-8f67-d1e9162a511f",
    "name": "Proseware, Inc. | Outdoor Furniture Bargains - North Obieberg",
    "location": { "lat": -84.1013, "lon": -69.5717 }
  }
]
```

### 示例 3：查找 $geometry 所定义区域内的商店 {#example-3-find-stores-defined-by-geometry}

此查询最多查找两家位置位于指定矩形多边形内的商店。

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-85.0, -70.0],
          [-85.0, -60.0],
          [-75.0, -60.0],
          [-75.0, -70.0],
          [-85.0, -70.0]
        ]]
      }
    }
  }
}, {
  name: 1,
  location: 1
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "66fd4cdd-ffc3-44b6-81d9-6d5e9c1f7f9a",
    "name": "Trey Research | Health Food Center - North Michelle",
    "location": { "lat": -77.9951, "lon": -62.7339 }
  },
  {
    "_id": "ea3f775b-f977-4827-ada4-ca7fd8ed0cd4",
    "name": "VanArsdel, Ltd. | Outdoor Equipment Pantry - Port Aleenton",
    "location": { "lat": -76.4516, "lon": -67.2051 }
  }
]
```
