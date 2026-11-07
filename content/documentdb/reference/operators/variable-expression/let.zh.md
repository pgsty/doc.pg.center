---
title: $let
description: $let 运算符允许定义供指定表达式使用的变量，从而实现复杂计算并减少重复代码。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/variable-expression/$let.md
weight: 10
translation_source_sha256: 9e07c25eb63b2c41a2063d2cff41806b1ba93b99ad0a9faf873eba2e2a5cf1a8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$let` 运算符用于定义供指定表达式使用的变量。它允许创建可在表达式内引用的临时变量，使复杂计算更易读，并避免重复计算。

## 语法 {#syntax}

```javascript
{
  $let: {
    vars: { 
      <var1>: <expression1>,
      <var2>: <expression2>,
      ...
    },
    in: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`vars`** | 定义变量及其值的对象。每个变量都被赋予一个表达式的结果。 |
| **`in`** | 使用 `vars` 对象中定义的变量的表达式。变量通过 `$$<variable_name>` 引用。 |
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

### 示例 1：变量的基本用法 {#example-1-basic-variable-usage}

使用定义好的变量计算员工效率指标。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      staffMetrics: {
        $let: {
          vars: {
            fullTime: "$staff.totalStaff.fullTime",
            partTime: "$staff.totalStaff.partTime",
            totalSales: "$sales.totalSales"
          },
          in: {
            totalStaff: { $add: ["$$fullTime", "$$partTime"] },
            salesPerEmployee: { $divide: ["$$totalSales", { $add: ["$$fullTime", "$$partTime"] }] },
            fullTimeRatio: { $divide: ["$$fullTime", { $add: ["$$fullTime", "$$partTime"] }] }
          }
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    "name": 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    "staffMetrics": {
      "totalStaff": 39,
      "salesPerEmployee": 3893.948717948718,
      "fullTimeRatio": 0.5128205128205128
    }
  }
]
```

### 示例 2：嵌套 $let 表达式 {#example-2-nested-let-expressions}

通过嵌套变量定义计算基于位置的分析结果。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      locationInsights: {
        $let: {
          vars: {
            lat: "$location.lat",
            lon: "$location.lon"
          },
          in: {
            coordinates: { lat: "$$lat", lon: "$$lon" },
            hemisphere: {
              $let: {
                vars: {
                  northSouth: { $cond: [{ $gte: ["$$lat", 0] }, "North", "South"] },
                  eastWest: { $cond: [{ $gte: ["$$lon", 0] }, "East", "West"] }
                },
                in: {
                  latitudeHemisphere: "$$northSouth",
                  longitudeHemisphere: "$$eastWest",
                  quadrant: { $concat: ["$$northSouth", " ", "$$eastWest"] }
                }
              }
            },
            distanceFromEquator: { $abs: "$$lat" },
            distanceFromPrimeMeridian: { $abs: "$$lon" }
          }
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    "name": 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    "locationInsights": {
      "coordinates": { "lat": 70.1272, "lon": 69.7296 },
      "hemisphere": {
        "latitudeHemisphere": 'North',
        "longitudeHemisphere": 'East',
        "quadrant": 'North East'
      },
      "distanceFromEquator": 70.1272,
      "distanceFromPrimeMeridian": 69.7296
    }
  }
]
```
