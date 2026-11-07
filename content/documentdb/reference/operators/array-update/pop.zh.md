---
title: $pop
description: $pop 运算符用于移除数组的第一个或最后一个元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$pop.md
weight: 60
translation_source_sha256: 660b66fbfc687c763405f002bcba3087f860b45148e57e6980a3eea3c5785c5c
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$pop` 运算符用于移除数组的第一个或最后一个元素。当需要从数组的任一端移除元素来管理数组时，该运算符非常有用。`$pop` 运算符可在更新操作中使用。

## 语法 {#syntax}

```javascript
{
  $pop: {
    <field>: <value>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field>`** | 包含要移除元素的数组的字段。 |
| **`<value>`** | 使用 `1` 移除最后一个元素，使用 `-1` 移除第一个元素。 |
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

### 示例 1：移除数组中的最后一个元素 {#example-1-remove-the-last-element-from-an-array}

要从 tag 数组中移除最后一个元素，请对 tag 字段使用 $pop 运算符，并将其值设为 1。

```javascript
db.stores.update({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $pop: {
        tag: 1
    }
})
```

此查询返回以下结果。

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]

```

### 示例 2：移除数组中的第一个元素 {#example-2-removing-the-first-element-from-an-array}

要从 promotionEvents 数组中移除第一个元素，请对 promotionEvents 数组使用 $pop 运算符，并将其值设为 -1。

```javascript
db.stores.update({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $pop: {
        promotionEvents: -1
    }
})
```

此查询返回以下结果。

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```
