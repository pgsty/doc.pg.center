---
title: $geoIntersects
description: $geoIntersects 运算符选择 location 字段与指定 GeoJSON 对象相交的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$geointersects.md
weight: 40
translation_source_sha256: b2c3508a0dbc216d37f87791d629ac142066bedb70c5c1ba948c9322fb3e1974
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 最后的说明使用 `$geointersects`，而标题和代码使用 `$geoIntersects`。该处正文中的运算符大小写与示例不一致。

`$geoIntersects` 运算符选择 location 字段与指定 GeoJSON 对象相交的文档。该运算符适用于查找与特定地理区域相交的商店。

## 语法 {#syntax}

```javascript
{
  <location field>: {
    $geoIntersects: {
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
| `location field` | 包含 GeoJSON 对象的字段 |
| `type` | GeoJSON 对象类型（例如，"Polygon"、"MultiPolygon"） |
| `coordinates` | 定义 GeoJSON 对象的坐标 |
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

<span id="example-1-find-stores-that-geographically-intersect"></span>

### 示例 1 - 查找地理位置相交的商店 {#example-1---find-stores-that-geographically-intersect}

为提高性能，首先创建所需的 `2dsphere` 索引。

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

此示例查询使用 `stores` 集合查找与特定多边形区域相交的商店。该多边形包含数据集中的多个商店位置。

```javascript
db.stores.find(
  {
    location: {
      $geoIntersects: {
        $geometry: {
          type: "Polygon",
          coordinates: [[
            [-80.0, -75.0],
            [-80.0, -70.0],
            [-55.0, -70.0],
            [-55.0, -75.0],
            [-80.0, -75.0]
          ]]
        }
      }
    }
  },
  {
    name: 1,
    location: 1
  }
).limit(2)
```

此查询返回位置与坐标所定义的 Polygon 轮廓相交的商店。

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

$geointersects 运算符适用于以下场景：

- 查找特定地理边界内的商店
- 确定服务覆盖区域
- 规划配送路线
