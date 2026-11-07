---
title: $position
description: $position 用于指定新元素应插入到数组中的位置。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$positional.md
weight: 70
translation_source_sha256: 22b8cc3ac765b37f256bf890cdb4f21058481f3edb6e72e3efbff5af471e4369
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$position` 运算符用于指定新元素应插入到数组中的位置。当需要在数组的特定下标处插入元素，而非追加到末尾时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $push: {
    <arrayField>: {
      $each: [<value1>, <value2>],
      $position: <index>
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<arrayField>`**| 文档中包含待更新数组的字段。|
| **`<value1>, <value2>, ...`**| 要插入数组的值。|
| **`<index>`**| 应插入这些值的位置。|
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

### 示例 1：在数组字段中指定下标处插入元素 {#example-1-insert-an-element-at-specific-index-location-in-an-array-field}

此查询将标签 `#NewArrival` 插入到指定文档的 `tag` 数组的第二个位置（下标为 1）。

```javascript
db.stores.update({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $push: {
        tag: {
            $each: ["#NewArrival"],
            $position: 1
        }
    }
})
```

更新后，文档的 tag 数组包含以下值。

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "tag": [
    "#ShopLocal",
    "#NewArrival",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```
