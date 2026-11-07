---
title: $literal
description: $literal 运算符返回指定值，不将其解析为表达式，从而允许在聚合流水线中使用字面值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/literal-expression/$literal.md
weight: 10
translation_source_sha256: 5fd1984ce053ea497e3a5db43a29f15742b7832a6fb0b6f7e04b11e74b8864c3
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$literal` 运算符返回指定值，不将其解析为表达式。如果需要在聚合流水线中加入可能被解释为字段名称、运算符或表达式的字面值，可使用此运算符。它确保将该值视为常量，而不对其求值。

## 语法 {#syntax}

```javascript
{
  $literal: <value>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<value>`** | 应当不作解释、直接原样返回的任意值。可以是字符串、数值、布尔值、数组、对象或 null。 |
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

### 示例 1：添加字面值状态字段 {#example-1-adding-literal-status-fields}

此查询演示如何向商店文档添加字面值状态信息，包括原本可能被解释为字段名称或运算符的字符串字面值。

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      status: { $literal: "Active" },
      reviewStatus: { $literal: "$pending" },
      priority: { $literal: 1 },
      metadata: {
        $literal: {
          lastUpdated: "2024-06-13",
          source: "automated-system"
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
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "totalSales": 37701,
    "status": "Active",
    "reviewStatus": "$pending",
    "priority": 1,
    "metadata": {
      "lastUpdated": "2024-06-13",
      "source": "automated-system"
    }
  }
]
```

### 示例 2：创建数组字面量和条件值 {#example-2-creating-literal-arrays-and-conditional-values}

此查询展示如何在处理数组和编写条件表达式时使用 `$literal`，确保不会将值解释为运算符。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      performanceCategory: {
        $cond: {
          if: { $gte: ["$sales.totalSales", 100000] },
          then: { $literal: "High Performer" },
          else: { $literal: "Standard" }
        }
      },
      tags: { $literal: ["$featured", "$promoted", "$new"] },
      searchKeywords: {
        $literal: {
          "$or": ["electronics", "entertainment"],
          "$and": ["home", "theater"]
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
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "totalSales": 160000,
    "performanceCategory": "High Performer",
    "tags": ["$featured", "$promoted", "$new"],
    "searchKeywords": {
      "$or": ["electronics", "entertainment"],
      "$and": ["home", "theater"]
    }
  }
]
```

### 示例 3：null 和布尔字面值 {#example-3-literal-null-and-boolean-values}

此查询演示如何对 null 和布尔值使用 `$literal`，尤其适用于需要显式设置这些值而非通过计算得出它们的情况。

```javascript
db.stores.aggregate([
  { $match: {"_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      specialOffer: { $literal: null },
      isOnline: { $literal: false },
      hasInventory: { $literal: true },
      calculationFormula: { $literal: "$multiply: [price, quantity]" },
      ratingSystem: {
        $literal: {
          min: 0,
          max: 5,
          default: null
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
    "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
    "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
    "totalSales": 17676,
    "specialOffer": null,
    "isOnline": false,
    "hasInventory": true,
    "calculationFormula": "$multiply: [price, quantity]",
    "ratingSystem": {
      "min": 0,
      "max": 5,
      "default": null
    }
  }
]
```
