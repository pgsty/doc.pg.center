---
title: $allElementsTrue
description: $allElementsTrue 运算符在数组中所有元素的求值结果均为 true 时返回 true。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$allelementstrue.md
weight: 10
translation_source_sha256: 2eb8cedb24212ef6a806c261b903baeb4756241211bb6ee5e77fa05fdadc6caa
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$allElementsTrue` 运算符将数组视为集合进行求值。如果数组中没有任何元素的值为 `false` 或等同于 `false` 的值（例如 `null`、`0` 或 `undefined`），则返回 `true`。如果任意元素的求值结果为 `false` 或等价值，该运算符返回 `false`。

## 语法 {#syntax}

```javascript
{
  $allElementsTrue: [ <array> ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `array` | 要求值的表达式数组。如果数组为空，`$allElementsTrue` 返回 `true`。 |
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

### 示例 1：判断所有折扣百分比是否大于零 {#example-1-determine-if-all-the-discount-percentages-are-higher-than-zero}

此查询判断每个促销活动中的所有折扣百分比是否都大于零。

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      allDiscountsValid: {
        $allElementsTrue: [
          {
            $map: {
              input: "$promotionEvents.discounts.discountPercentage",
              as: "discount",
              in: { $gt: ["$$discount", 0] }
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
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "allDiscountsValid": true
  }
]
```
