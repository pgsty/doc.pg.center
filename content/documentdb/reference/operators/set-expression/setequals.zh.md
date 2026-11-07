---
title: $setEquals
description: $setEquals 运算符在两个集合去重后的元素相同时返回 true。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$setequals.md
weight: 40
translation_source_sha256: 352c2d1fd3d935687f37485a8c1831da7819e1b78b6dbe0382821b309b4df7cd
translation_review: AI-assisted bilingual review; 2026-11-07
---

如果两个集合去重后的元素相同，`$setEquals` 运算符返回 `true`，不受顺序或重复项影响。它将数组视为集合，忽略重复值和元素顺序。

## 语法 {#syntax}

```javascript
{
  $setEquals: [ <array1>, <array2>, ... ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `array1, array2, ...` | 要比较是否相等的数组。可以指定两个或更多数组。 |
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

### 示例 1：比较不同活动的折扣类别 {#example-1-compare-discount-categories-between-events}

此查询判断两个促销活动是否对相同类别提供折扣。

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      event1Categories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      event2Categories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
      sameDiscountCategories: {
        $setEquals: [
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] }
        ]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "event1Categories": [
      "Condenser Microphones",
      "Dynamic Microphones"
    ],
    "event2Categories": [
      "Streaming Microphones",
      "Microphone Stands"
    ],
    "sameDiscountCategories": false
  }
]
```

### 示例 2：比较员工需求 {#example-2-compare-staff-requirements}

此查询判断两家商店的员工结构要求是否相同。

```javascript
db.stores.aggregate([
  { $match: {"_id": { $in: ["26afb024-53c7-4e94-988c-5eede72277d5", "f2a8c190-28e4-4e14-9d8b-0256e53dca66"] }} },
  {
    $group: {
      _id: null,
      stores: { $push: { _id: "$_id", name: "$name" }}
    }
  },
  {
    $project: {
      store1: { $arrayElemAt: ["$stores", 0] },
      store2: { $arrayElemAt: ["$stores", 1] },
      staffTypes1: ["fullTime", "partTime"],
      staffTypes2: ["fullTime", "partTime"],
      sameStaffStructure: {
        $setEquals: [
          ["fullTime", "partTime"],
          ["fullTime", "partTime"]
        ]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": null,
    "store1": {
      "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
      "name": "First Up Consultants | Microphone Bazaar - South Lexusland"
    },
    "store2": {
      "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
      "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele"
    },
    "staffTypes1": ["fullTime", "partTime"],
    "staffTypes2": ["fullTime", "partTime"],
    "sameStaffStructure": true
  }
]
```

### 示例 3：比较包含重复项的集合 {#example-3-compare-sets-with-duplicates}

此查询使用 `$setEquals` 运算符，忽略重复项和顺序。

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      array1: ["Microphones", "Stands", "Microphones", "Accessories"],
      array2: ["Stands", "Accessories", "Microphones"],
      arraysEqual: {
        $setEquals: [
          ["Microphones", "Stands", "Microphones", "Accessories"],
          ["Stands", "Accessories", "Microphones"]
        ]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "array1": ["Microphones", "Stands", "Microphones", "Accessories"],
    "array2": ["Stands", "Accessories", "Microphones"],
    "arraysEqual": true
  }
]
```
