---
title: $polygon
description: $polygon 运算符为地理空间查询定义多边形，用于查找不规则形状内的位置。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$polygon.md
weight: 110
translation_source_sha256: 902fbc69eb94891eb008428d6fe1c84c01c7f41ba8b8df5ebb5881a30eba0fe8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$polygon` 运算符为地理空间查询定义多边形，用于查找不规则形状内的位置。该运算符适用于查询复杂地理边界内的位置。

## 语法 {#syntax}

```javascript
{
  <location field>: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [
          [[<longitude1>, <latitude1>], ..., [<longitudeN>, <latitudeN>], [<longitude1>, <latitude1>]]
        ]
      }
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `location field` | 包含地理空间数据的字段 |
| `coordinates` | 构成多边形的坐标对数组。首尾两个点必须相同，以闭合多边形 |
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

<span id="example-1-search-within-a-polygon"></span>

### 示例 1 - 在多边形内搜索 {#example-1---search-within-a-polygon}

此查询根据提供的坐标，检索位于自定义多边形区域内的商店。

```javascript
db.stores.find({
  location: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-141.9922, 16.8331],  // VanArsdel Picture Frame Store
          [-112.7858, -29.1866], // First Up Consultants Microphone Bazaar
          [-38.4071, -47.2548],  // Fabrikam Car Accessory Outlet
          [-141.9922, 16.8331]   // Close the polygon by repeating first point
        ]]
      }
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
      "_id": "4a417727-a002-4c80-a01f-bc9526b300a5",
      "name": "Northwind Traders | Bed and Bath Deals - East Duane",
      "location": {
        "type": "Point",
        "coordinates": [-46.1444, -60.9697]
      }
    },
    {
      "_id": "1e27040c-7242-4970-8893-e5738e1bc1ca",
      "name": "Northwind Traders | Seasonal Decoration Bazaar - Cassidyberg",
      "location": {
        "type": "Point",
        "coordinates": [-44.3617, -81.2186]
      }
    }
]
```
