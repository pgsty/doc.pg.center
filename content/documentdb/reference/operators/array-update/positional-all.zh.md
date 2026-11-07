---
title: $[]
description: $[] 全位置运算符会更新数组中的每个元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$positional-all.md
weight: 20
translation_source_sha256: 4ba49f037af693c573956820808f48289d796b6fd18af641788b159a18e15d9c
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$[]` 全位置运算符会更新每个匹配文档中数组的所有元素。与 `$` 不同，它不依赖于查询匹配的是哪个元素；与 `$[<identifier>]` 不同，它不接受 `arrayFilters`。如果路径对应的值不是数组，更新就会失败。

## 语法 {#syntax}

```javascript
db.collection.update(
   <query>,
   {
     $set: {
       <arrayField>.$[]: <value>
     }
   }
)
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<query>`** | 用于选择要更新的文档的条件。 |
| **`<arrayField>`** | 包含要更新数组的字段。 |
| **`<value>`** | 要为数组中的每个元素设置的值。 |
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

### 示例 1：更新折扣百分比 {#example-1-updating-discount-percentages}

此查询更新每个促销活动内 discounts 数组中的所有元素。

```javascript
db.stores.updateOne(
  { _id: "0fcc0bf0-ed18-4ab8-b558-9848e18058f4" },
  {
    $inc: {
      "promotionEvents.$[].discounts.$[].discountPercentage": 5
    }
  }
)
```

### 示例 2：按类别更新销售额 {#example-2-updating-sales-by-category}

此查询使用 $[] 运算符将所有类别的总销售额提高 10%。

```javascript
db.stores.update(
  { _id: "0fcc0bf0-ed18-4ab8-b558-9848e18058f4" },
  {
    $mul: {
      "sales.salesByCategory.$[].totalSales": 1.10
    }
  }
)
```
