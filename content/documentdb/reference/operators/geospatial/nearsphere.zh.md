---
title: $nearSphere
description: $nearSphere 运算符返回 location 字段所表示的位置靠近球面上指定点的文档，并按球面距离排序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$nearsphere.md
weight: 100
translation_source_sha256: 34a2bac047f96b4aad53ed91452bef461a90295bbb73b01405b6fcb454a68f03
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$nearSphere` 运算符返回 location 字段所表示的位置靠近球面上指定点的文档，使用球面几何计算距离。在基于地球的计算中，该运算符比 `$near` 更准确。

## 语法 {#syntax}

```javascript
{
  <location field>: {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [<longitude>, <latitude>]
      },
      $maxDistance: <distance in meters>,
      $minDistance: <distance in meters>
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `location field` | 包含 GeoJSON Point 的字段 |
| `$geometry` | 指定中心点的 GeoJSON Point 对象 |
| `$maxDistance` | 可选。球面上的最大距离，以米为单位 |
| `$minDistance` | 可选。球面上的最小距离，以米为单位 |
{.fields}

## 示例 {#examples}

下面通过 `stores` 数据集中的示例 JSON 了解其用法。

```json
{
  "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
  "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
  "location": { "lat": -74.0427, "lon": 160.8154 },
  "staff": { "employeeCount": { "fullTime": 9, "partTime": 18 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Stockings", "totalSales": 25731 } ],
    "revenue": 25731
  },
  "promotionEvents": [
    {
      "eventName": "Mega Savings Extravaganza",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 6, "Day": 29 },
        "endDate": { "Year": 2023, "Month": 7, "Day": 7 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 16 },
        { "categoryName": "Tree Ornaments", "discountPercentage": 8 }
      ]
    },
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 11 },
        { "categoryName": "Holiday Cards", "discountPercentage": 9 }
      ]
    },
    {
      "eventName": "Massive Deal Mania",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 2 }
      },
      "discounts": [
        { "categoryName": "Gift Bags", "discountPercentage": 21 },
        { "categoryName": "Bows", "discountPercentage": 19 }
      ]
    },
    {
      "eventName": "Super Saver Soiree",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
        "endDate": { "Year": 2024, "Month": 4, "Day": 1 }
      },
      "discounts": [
        { "categoryName": "Tree Ornaments", "discountPercentage": 15 },
        { "categoryName": "Stockings", "discountPercentage": 14 }
      ]
    },
    {
      "eventName": "Fantastic Savings Fiesta",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 30 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 24 },
        { "categoryName": "Gift Wrap", "discountPercentage": 16 }
      ]
    },
    {
      "eventName": "Price Plunge Party",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 9, "Day": 21 },
        "endDate": { "Year": 2024, "Month": 9, "Day": 28 }
      },
      "discounts": [
        { "categoryName": "Holiday Tableware", "discountPercentage": 13 },
        { "categoryName": "Holiday Cards", "discountPercentage": 11 }
      ]
    }
  ],
  "company": "Lakeshore Retail",
  "city": "Marvinfort",
  "storeOpeningDate": { "$date": "2024-10-01T18:24:02.586Z" },
  "lastUpdated": { "$timestamp": { "t": 1730485442, "i": 1 } },
  "storeFeatures": 38
}
```

为提高性能，首先创建所需的 `2dsphere` 索引。

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### 示例 1：基本球面搜索 {#example-1-basic-spherical-search}

此查询检索在球面（类似地球表面）上距离指定点 (-141.9922, 16.8331) 最近的商店。

```javascript
db.stores.find({
  'location': {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [-141.9922, 16.8331]
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
    "_id": "643b2756-c22d-4063-9777-0945b9926346",
    "name": "Contoso, Ltd. | Outdoor Furniture Corner - Pagacfort",
    "location": {
      "type": "Point",
      "coordinates": [152.1353, -89.8688]
    }
  },
  {
    "_id": "daa71e60-75d4-4e03-8b45-9df59af0811f",
    "name": "First Up Consultants | Handbag Corner - South Salvatore",
    "location": {
      "type": "Point",
      "coordinates": [150.2305, -89.8431]
    }
  }
]
```

### 示例 2：复杂距离分析 {#example-2-complex-distance-analysis}

此查询检索距点 (65.3765, -44.8674) 20 米至 200 米范围内的商店。该查询搜索一个“圆环形”区域，查找距指定点至少 20 米、但不超过 200 米的商店。

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [65.3765, -44.8674]
      },
      distanceField: "sphericalDistance",
      minDistance: 20,
      maxDistance: 200,
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      location: 1,
      distanceKm: { $divide: ["$sphericalDistance", 1000] },
      _id: 0
    }
  },
  {
    $limit: 2
  }
])
```

`$nearSphere` 与 `$near` 运算符的主要区别如下。

* 前者使用球面几何计算距离。
* 前者在基于地球的距离计算中更准确。
* 前者更适合需要精确计算全球距离的应用。
