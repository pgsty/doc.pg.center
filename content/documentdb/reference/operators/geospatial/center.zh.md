---
title: $center
description: $center 运算符使用传统坐标对指定圆形区域，供 $geoWithin 查询使用。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$center.md
weight: 20
translation_source_sha256: d21c7ed5f8da89d9ee0144ada13c26851783b9dfcb61c23758fdaa926172d9a1
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$center` 运算符使用传统坐标对指定圆形区域，供 `$geoWithin` 查询使用。它在平坦的欧几里得平面上定义地理空间查询所用的圆。

## 语法 {#syntax}

```javascript
{
  $geoWithin: {
    $center: [ [ <x>, <y> ], <radius> ]
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `<x>` | 圆心的 x 坐标 |
| `<y>` | 圆心的 y 坐标 |
| `<radius>` | 圆的半径，单位与坐标相同 |
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

<span id="example-1-find-stores-within-a-circular-area"></span>

### 示例 1 - 查找圆形区域内的商店 {#example-1---find-stores-within-a-circular-area}

下面使用 `stores` 数据集查找以 'First Up Consultants Microphone Bazaar' 为中心、半径为 50 度的范围内的所有商店。此查询检索以 First Up Consultants Microphone Bazaar 所在位置为中心、半径为 50 度的范围内的商店。

```javascript
db.stores.find(
  {
    location: {
      $geoWithin: {
        $center: [[-112.7858, -29.1866], 50]
      }
    }
  },
  {
    name: 1,
    city: 1,
    location: 1,
    _id: 0
  }
).limit(2)
```

此查询返回半径为 50 度的范围内的商店，可用于分析市场覆盖范围或规划配送路线。

```json
[
  {
    "name": "Contoso, Ltd. | Baby Products Corner - Port Jerrold",
    "location": { "lat": -72.7709, "lon": -24.3031 },
    "city": "Port Jerrold"
  },
  {
    "name": "VanArsdel, Ltd. | Smart Home Closet - Trystanport",
    "location": { "lat": -64.5509, "lon": -28.7144 },
    "city": "Trystanport"
  }
]
```

> [!IMPORTANT]
> `$center` 运算符在平坦的欧几里得平面上工作。
> 
> 要更准确地按地球这样的球面进行计算，应改用 `$centerSphere`。
> 
> 半径的单位与所用坐标系的单位相同。
