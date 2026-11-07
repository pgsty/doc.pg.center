---
title: $anyElementTrue
description: $anyElementTrue 运算符在数组中任意元素的求值结果为 true 时返回 true。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$anyelementtrue.md
weight: 20
translation_source_sha256: a2e43d3aec5ad3c4b3fb710d667c767bd0de2e2453b739292c937ead53253187
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$anyElementTrue` 运算符将数组视为集合进行求值。如果数组中任意元素为 `true`（或等同于 `true` 的值），则返回 `true`。如果所有元素的求值结果均为 `false`、`null`、`0` 或 `undefined`，该运算符返回 `false`。

## 语法 {#syntax}

```javascript
{
  $anyElementTrue: [ <array> ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `array` | 要求值的表达式数组。如果数组为空，`$anyElementTrue` 返回 `false`。 |
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

### 示例 1：判断是否有销售类别超过目标值 {#example-1-determine-if-any-sales-category-exceeds-a-target}

此查询判断是否有销售类别超过指定目标值。本例中的目标销售额为 40,000。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      salesByCategory: "$sales.salesByCategory",
      hasHighPerformingCategory: {
        $anyElementTrue: [
          {
            $map: {
              input: "$sales.salesByCategory",
              as: "category",
              in: { $gt: ["$$category.totalSales", 40000] }
            }
          }
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
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120,
        "lastUpdated": "2025-06-11T11:10:34.414Z"
      },
      null,
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ],
    "hasHighPerformingCategory": true
  }
]
```

### 示例 2：判断是否有促销活动提供高折扣 {#example-2-determine-if-any-promotion-event-has-high-discounts}

此查询判断是否有促销活动提供超过 20% 的折扣。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      hasHighDiscount: {
        $anyElementTrue: [
          {
            $map: {
              input: "$promotionEvents.discounts",
              as: "discount",
              in: { $gte: ["$$discount.discountPercentage", 20] }
            }
          }
        ]
      }
    }
  }
])
```

此查询返回的前五个结果如下：

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Massive Markdown Mania",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Fantastic Deal Days",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Super Sale Spectacular",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Grand Deal Days",
    "hasHighDiscount": true
  }
]
```
