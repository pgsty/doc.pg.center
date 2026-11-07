---
title: $geoNear
description: $geoNear 运算符根据文档与地理空间点的接近程度查找并排序文档，为每个文档返回距离信息。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$geonear.md
weight: 120
translation_source_sha256: 84b878f161210d969f0cac8feb06d813daddb574b768b78c05b2fe7716b25dcb
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$geoNear` 流水线阶段计算指定点与每个文档中位置字段之间的距离，按距离对文档进行排序，并可选择按距离限制结果。

## 语法 {#syntax}

```javascript
{
  $geoNear: {
    near: {
      type: "Point",
      coordinates: [<longitude>, <latitude>]
    },
    distanceField: <field to store distance>,
    maxDistance: <optional maximum distance in meters>,
    minDistance: <optional minimum distance in meters>,
    query: <optional query conditions>,
    includeLocs: <optional boolean to include locations>,
    distanceMultiplier: <optional distance multiplier>,
    spherical: <boolean, must be true>,
    key: <optional field path>
  }
}
```

## 参数 {#parameters}

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `near` | 对象 | 用于计算距离的点 |
| `distanceField` | 字符串 | 包含计算出的距离的字段 |
| `maxDistance` | 数字 | 可选。距离点的最大距离（单位：米） |
| `minDistance` | 数字 | 可选。距离点的最小距离（单位：米） |
| `query` | 文档 | 可选。查询条件 |
| `includeLocs` | 布尔值 | 可选。在结果中包含位置数据 |
| `distanceMultiplier` | 数字 | 可选。将距离乘以该值 |
| `spherical` | 布尔值 | 使用 2dsphere 索引时必须为 true |
| `key` | 字符串 | 可选。用于计算距离的字段路径 |
{.fields}

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

### 示例 1：基本距离计算 {#example-1-basic-distance-calculation}

此查询检索 "VanArsdel Picture Frame Store" 所在位置附近的所有商店，并按距离排序：

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [-141.9922, 16.8331]  // VanArsdel Picture Frame Store location
      },
      distanceField: "distance",
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      distance: 1
    }
  }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "643b2756-c22d-4063-9777-0945b9926346",
        "name": "Contoso, Ltd. | Outdoor Furniture Corner - Pagacfort",
        "distance": 5458613.2813355485
    },
    {
        "_id": "daa71e60-75d4-4e03-8b45-9df59af0811f",
        "name": "First Up Consultants | Handbag Corner - South Salvatore",
        "distance": 5469362.958855379
    },
    {
        "_id": "02a78a15-b1fc-4bbd-ae1d-641b7428dc78",
        "name": "VanArsdel, Ltd. | Kitchen Appliance Corner - Llewellynberg",
        "distance": 5472684.4628977
    }
]
```

### 示例 2：带距离限制和可选查询条件的 {#example-2-with-distance-limits-and-optional-query}

此查询检索距离 "Proseware Home Entertainment Hub" 30 公里以内且全职员工数量超过 10 人的所有商店：

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [69.7296, 70.1272]  // "Proseware Home Entertainment Hub" location
      },
      distanceField: "distance",
      maxDistance: 30000,  // 30 kilometers in meters
      query: { "staff.totalStaff.fullTime": { $gt: 10 } },
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      distance: 1,
      "staff.totalStaff.fullTime": 1
    }
  }
])
```

此查询返回的第一个结果是：

```javascript
[
    {
        "_id": "bbec6d3e-1666-45b4-8803-8b7ef8544845",
        "name": "First Up Consultants | Baby Products Bargains - South Keenan",
        "staff": {
            "totalStaff": {
                "fullTime": 19
            }
        },
        "distance": 29934.71888123174
    }
]
```

### 示例 3：包含位置数据和距离倍数的 {#example-3-including-location-data-and-distance-multiplier}

此查询检索商店信息，距离以公里为单位，并包含位置数据：

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [-38.4071, -47.2548]  // "Fabrikam Car Accessory Outlet" location
      },
      distanceField: "distanceInKm",
      includeLocs: "storeLocation",
      distanceMultiplier: 0.001,  // Convert meters to kilometers
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      distanceInKm: 1,
      storeLocation: 1
    }
  }
])
```

此查询返回的前三个结果如下：

```javascript
[
    {
        "_id": "b677846e-bb73-46ec-9cba-7d94afee382c",
        "name": "Northwind Traders | Health Food Shoppe - Brooklynmouth",
        "storeLocation": {
            "lat": -38.3032,
            "lon": -132.7866
        },
        "distanceInKm": 9.095634270192285
    },
    {
        "_id": "27c64b44-2382-4477-b3ce-c08e74882156",
        "name": "Relecloud | VR Headset Gallery - West Jonasbury",
        "storeLocation": {
            "lat": -37.9628,
            "lon": -132.6637
        },
        "distanceInKm": 34.7104536140246
    },
    {
        "_id": "505e83eb-09bc-46a4-ba85-16135611b9de",
        "name": "Fabrikam, Inc. | Pharmacy Hub - Elijahville",
        "storeLocation": {
            "lat": -38.0349,
            "lon": -47.9571
        },
        "distanceInKm": 82.92766541748313
    }
]
```

## 限制条件 {#limitations}

* 不能与分片集合一起使用
* 聚合流水线中每个管道只能有一个 $geoNear 阶段
* 必须是流水线中的第一个阶段
