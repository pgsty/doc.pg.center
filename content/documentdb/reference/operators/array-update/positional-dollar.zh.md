---
title: $
description: $ 位置运算符用于标识数组中要更新的元素，无需显式指定该元素在数组中的位置。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$.md
weight: 10
translation_source_sha256: 02dee7c5630b079677f15745f552304bc7b5444b44a47216927651dc8bbc564a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$` 位置运算符用于标识数组中要更新的元素，无需显式指定该元素在数组中的位置。`$` 运算符充当第一个满足查询条件的元素的占位符，且数组字段必须出现在查询文档中。

## 语法 {#syntax}

```javascript
db.collection.updateOne(
  { <array>: <value> },
  { <update operator>: { "<array>.$": <value> } }
)
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`array`** | 包含要更新元素的数组字段。必须是查询条件的一部分。 |
| **`value`** | 用于在查询条件中匹配数组元素的值。 |
| **`update operator`** | 要应用的更新运算符（例如 `$set`、`$inc`、`$unset`）。 |
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

### 示例 1：投影数组中第一个满足条件的元素 {#example-1-project-the-first-element-of-an-array-matching-the-condition}

此查询返回 `salesByCategory` 数组中第一个与 `DJ` 设备对应且 `totalSales` 大于 35000 的元素。

```javascript
db.stores.find({
    "sales.salesByCategory": {
        $elemMatch: {
            categoryName: {
                $regex: "^DJ"
            }
        }
    },
    "sales.salesByCategory.totalSales": {
        $gt: 35000
    }
}, {
    "sales.salesByCategory.$": 1
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "DJ Speakers",
          "totalSales": 36972
        }
      ]
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "DJ Headphones",
          "totalSales": 35911
        }
      ]
    }
  }
]
```

### 示例 2：更新特定类别的折扣百分比 {#example-2-update-discount-percentage-for-a-specific-category}

此查询更新第一个匹配的促销活动中 "Desks" 类别的折扣百分比。

```javascript
db.stores.updateOne(
  { 
    _id: "905d1939-e03a-413e-a9c4-221f74055aac",
    "promotionEvents.discounts.categoryName": "Desks"
  },
  {
    $set: { "promotionEvents.$.discounts.$[elem].discountPercentage": 25 }
  },
  {
    arrayFilters: [{ "elem.categoryName": "Desks" }]
  }
)
```

### 示例 3：更新销售类别总额 {#example-3-update-sales-category-total}

此查询使用 `$ (positional operator)` 更新特定类别的总销售额。

```javascript
db.stores.updateOne(
  { 
    _id: "905d1939-e03a-413e-a9c4-221f74055aac",
    "sales.salesByCategory.categoryName": "Desk Lamps"
  },
  {
    $inc: { "sales.salesByCategory.$.totalSales": 1000 }
  }
)
```
