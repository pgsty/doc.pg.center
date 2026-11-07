---
title: $near
description: $near 运算符返回 location 字段所表示的位置靠近指定点的文档，并按距离排序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$near.md
weight: 90
translation_source_sha256: 78c215328e9935189679536a58b0ae407f5311c94143e792f80d63545c46489b
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例说明对同一范围先写 20–200 千米，随后又写 20–200 米。代码使用的距离限制是 20 和 200，然后将返回的距离除以 1000，作为以千米为单位的字段值。原文说明存在单位冲突。

`$near` 运算符返回 location 字段所表示的位置靠近指定点的文档，并按距离排序。它要求存在 '2dsphere' 索引，且按由近到远的顺序返回文档。

## 语法 {#syntax}

```javascript
{
  <location field>: {
    $near: {
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
| `$maxDistance` | 可选。与中心点之间的最大距离，以米为单位 |
| `$minDistance` | 可选。与中心点之间的最小距离，以米为单位 |
{.fields}

## 前提条件 {#prerequisite}

为提高性能，首先创建所需的 `2dsphere` 索引。

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

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

### 示例 1：基本邻近搜索 {#example-1-basic-proximity-search}

此查询通过地理空间搜索，检索距离特定地理点 (70.1272, 69.7296) 最近的两家商店。它搜索最接近给定点的位置，并按与该点距离的升序返回商店。

```javascript
db.stores.find({
  'location': {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [69.7296, 70.1272]  // [longitude, latitude]
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
     "_id": "3882eb86-5dd6-4701-9640-f670ccb67859",
     "name": "Fourth Coffee | DJ Equipment Stop - Schuppestad",
     "location": { "lat": 69.4923, "lon": 70.1851 }
   },
   {
     "_id": "bbec6d3e-1666-45b4-8803-8b7ef8544845",
     "name": "First Up Consultants | Baby Products Bargains - South Keenan",
     "location": { "lat": 69.2158, "lon": 70.3328 }
   }
]
```

### 示例 2：同时使用最小距离和最大距离 {#example-2-using-both-min-and-max-distance}

此查询检索距指定点 20 千米至 200 千米范围内的商店，并以千米为单位计算距离。该查询搜索一个“圆环形”区域，查找距指定点至少 20 米、但不超过 200 米的商店。

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [70.3328, 69.2158]
      },
      distanceField: "distance",
      minDistance: 20,
      maxDistance: 200,
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      location: 1,
      distanceKm: { $divide: ["$distance", 1000] },
      _id: 0
    }
  },
  { $limit: 2 }
])
```
