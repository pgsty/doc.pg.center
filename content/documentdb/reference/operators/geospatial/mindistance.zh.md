---
title: $minDistance
description: $minDistance 运算符指定地理空间查询中两点之间必须保持的最小距离。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$mindistance.md
weight: 80
translation_source_sha256: 1a11c820ccff265b0be115bfff74b24c833df548a0035c3ba5e82982d12072d7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$minDistance` 运算符用于在地理空间查询中指定两点之间必须保持的最小距离（以米为单位）。它适用于查找一定半径范围之外的位置。

## 语法 {#syntax}

```javascript
{
  <location field>: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [<longitude>, <latitude>]
      },
      $minDistance: <distance in meters>
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `location field` | 包含地理空间数据的字段 |
| `coordinates` | 指定中心点的 [经度, 纬度] 数组 |
| `$minDistance` | 与中心点之间的最小距离，以米为单位 |
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

### 示例 1：按距参考点的最小距离查找商店 {#example-1-finding-stores-by-minimum-distance-from-a-reference-point}

此示例查询查找距离坐标为 [69.7296, 70.1272] 的点至少 500 千米的商店。

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [69.7296, 70.1272]  // Proseware Home Entertainment Hub location
      },
      $minDistance: 500000  // 500 kilometers in meters
    }
  }
},
{
  name: 1,
  location: 1
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
 {
   "_id": "9d9d768b-4daf-4126-af15-a963bd3b88aa",
   "name": "First Up Consultants | Perfume Gallery - New Verniceshire",
   "location": { "lat": 36.0762, "lon": 98.7799 }
 },
 {
   "_id": "76b03913-37e3-4779-b3b8-0f654c1ae3e7",
   "name": "Fabrikam, Inc. | Turntable Depot - Schinnershire",
   "location": { "lat": 37.5534, "lon": 81.6805 }
 }
]
```
