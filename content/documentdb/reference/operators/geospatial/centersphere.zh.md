---
title: $centerSphere
description: $centerSphere 运算符使用球面几何指定圆形区域，供 $geoWithin 查询使用。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/geospatial/$centersphere.md
weight: 30
translation_source_sha256: 7b53b34cbe3bf7de8c5d341ed955faddf64920ada331af152ea215507501d909
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 参数表将角半径称为“球体”半径，而定义描述的是球面上的圆形搜索区域。上游关于 UTM 分带与日期变更线的警告作为来源限制保留，此处未独立验证。

`$centerSphere` 运算符使用球面几何指定圆形区域，供 `$geoWithin` 查询使用。该运算符适用于需要考虑地球球面形状的地理计算。

## 语法 {#syntax}

```javascript
{
  $geoWithin: {
    $centerSphere: [ [ <x>, <y> ], <radius in radians> ]
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `<x>` | 圆心的经度 |
| `<y>` | 圆心的纬度 |
| `<radius in radians>` | 以弧度表示的球体半径（将以千米为单位的距离除以 6371，即可换算为弧度） |
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

<span id="example-1-find-stores-within-a-circular-area-calculation-over-earth-s-spherical-shape"></span>

### 示例 1：查找圆形区域内的商店（按地球球面形状计算） {#example-1-find-stores-within-a-circular-area-calculation-over-earths-spherical-shape}

此示例查询查找距 Wide World Importers Headphone Corner 商店所在位置约 1,000 千米范围内的两家商店（半径 ≈ 0.157 弧度）。该查询有助于找出附近商店，以开展区域营销活动或优化供应链。

```javascript
// Convert 1000km to radians: 1000/6371 ≈ 0.157
db.stores.find(
  {
    location: {
      $geoWithin: {
        $centerSphere: [[-82.5543, -65.105], 0.157]
      }
    }
  },
  {
    _id: 0,
    name: 1,
    location: 1,
    city: 1
  }
).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "name": "Fourth Coffee | Electronics Bazaar - O'Keefeburgh",
    "location": { "lat": -64.5856, "lon": -115.5241 },
    "city": "O'Keefeburgh"
  },
  {
    "name": "Boulder Innovations | Footwear Outlet - West Sybleberg",
    "location": { "lat": -72.73, "lon": -60.2306 },
    "city": "West Sybleberg"
  }
]
```

> [!IMPORTANT]
> `$centerSphere` 运算符使用球面几何计算距离，因此在基于地球的计算中比 `$center` 更准确。
> 
> 半径必须以弧度指定。
> 
> 坐标应按以下顺序指定：[经度, 纬度]。
> 
> 如果地理缓冲区超出某个 UTM 分带，或跨越国际日期变更线，结果可能不准确或不可预测。
