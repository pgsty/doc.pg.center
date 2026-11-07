---
title: $geometry
description: $geometry 运算符为地理空间查询指定 GeoJSON 几何对象。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$geometry.md
weight: 50
translation_source_sha256: b3ba2214cc52e1e52cafb16c1bbb22113b93e975af68699f644629c49bebf947
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例 2、3 的标题写的是“最近”，但示例描述的分别是相交查询和包含查询。这些标题不表示结果一定按距离排序。

`$geometry` 运算符为地理空间查询指定 GeoJSON 几何对象。它在其他地理空间运算符内部使用，用来定义空间计算所需的形状和点。

## 语法 {#syntax}

```javascript
{
  $geometry: {
    type: <GeoJSON type>,
    coordinates: <coordinates>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `type` | GeoJSON 对象类型（Point、Polygon、MultiPolygon 等） |
| `coordinates` | 以数组形式定义 GeoJSON 对象的坐标 |
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

### 示例 1：查找距离点几何对象最近的商店 {#example-1-find-nearest-stores-to-point-geometry}

为提高性能，首先创建所需的 `2dsphere` 索引。

```javascript
db.stores.createIndex({ location: "2dsphere" })
```

此查询最多检索两家距离坐标 [46.2917, -62.6354] 处的点最近的商店，并按距离由近到远排列。它使用 $near 运算符，根据与特定点的距离对结果排序，从而查找地理位置上最接近给定地点的商店。

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [46.2917, -62.6354]
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
    "_id": "59c355e9-586c-44f8-bbaf-a87989142119",
    "name": "Relecloud | Outdoor Furniture Shop - Chetside",
    "location": { "lat": 46.188, "lon": -62.2789 }
  },
  {
    "_id": "d3a9cc23-e6ae-4806-93ac-1ade2f624742",
    "name": "VanArsdel, Ltd. | Furniture Place - North Dustinside",
    "location": { "lat": 47.3426, "lon": -62.4031 }
  }
]
```

### 示例 2：查找距离多边形几何对象最近的商店 {#example-2-find-nearest-stores-to-polygon-geometry}

此查询最多查找两家位置与指定矩形多边形相交的商店，该多边形由 [-80.0, -75.0] 到 [-55.0, -70.0] 的坐标限定。

`$geoIntersects` 运算符查找与多边形边界重叠或接触的商店，非常适合确定哪些位置与特定地理区域有交集，无论它们完全位于区域内部，还是仅跨越其边缘。

```javascript
db.stores.find({
  location: {
    $geoIntersects: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-80.0, -75.0],   // Bottom-left
          [-80.0, -70.0],   // Top-left
          [-55.0, -70.0],   // Top-right
          [-55.0, -75.0],   // Bottom-right
          [-80.0, -75.0]    // Close polygon
        ]]
      }
    }
  }
}, {
  name: 1,
  location: 1,
  city: 1
}).limit(2)
```

此查询返回的前两个结果如下。

```json
[
  {
    "_id": "6bba7117-d180-4584-b50c-a2f843e9c9ab",
    "name": "Wide World Importers | Craft Supply Mart - Heaneybury",
    "location": { "lat": -64.4843, "lon": -107.7003 },
    "city": "Heaneybury"
  },
  {
    "_id": "2fd37663-e0ff-41d0-9c5a-3aec86285daa",
    "name": "Relecloud | Cleaning Supply Closet - Patiencehaven",
    "location": { "lat": -70.6077, "lon": -105.9901 },
    "city": "Patiencehaven"
  }
]
```

### 示例 3：查找距离多重多边形几何对象最近的商店 {#example-3-find-nearest-stores-to-multi-polygon-geometry}

此示例最多检索两家商店，其位置位于两个指定矩形区域（MultiPolygon）中的任意一个内：一个区域在坐标 [120.0, -13.0] 到 [125.0, -10.0] 附近，另一个在 [44.0, -64.0] 到 [48.0, -61.0] 附近。

它结合 $geoWithin 运算符和 MultiPolygon 几何对象，搜索位于任意指定多边形内的商店，适合同时查询多个互不相邻的地理区域。

```javascript
db.stores.find({
  location: {
    $geoWithin: {
      $geometry: {
        type: "MultiPolygon",
        coordinates: [
          [[
            [120.0, -13.0],
            [120.0, -10.0],
            [125.0, -10.0],
            [125.0, -13.0],
            [120.0, -13.0]
          ]],
          [[
            [44.0, -64.0],
            [44.0, -61.0],
            [48.0, -61.0],
            [48.0, -64.0],
            [44.0, -64.0]
          ]]
        ]
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
    "_id": "6d70de9c-7b83-426d-81aa-f2173f97b64d",
    "name": "Fabrikam, Inc. | Footwear Haven - Port Erling",
    "location": { "lat": 45.641, "lon": -118.4963 }
  },
  {
    "_id": "96d48224-ce10-4a61-999a-8536d442f81a",
    "name": "Wide World Importers | Eyewear Bazaar - West Oletachester",
    "location": { "lat": 47.3461, "lon": -61.6605 }
  }
]
```
