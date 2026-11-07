---
title: $each
description: $each 运算符用于在 `$addToSet` 或 `$push` 操作中，通过一次更新向数组字段添加多个元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$each.md
weight: 50
translation_source_sha256: 5670e6b3c836f2dcc9e7d5bac918fad15ebb883349a9c645937c2d5da6092785
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$each` 运算符用于在 `$addToSet` 或 `$push` 操作中，通过一次更新向数组字段添加多个元素。当需要向数组中插入多个元素而不必执行多次更新时，可以使用此运算符。`$each` 运算符确保指定数组中的每个元素都被添加到目标数组中。

## 语法 {#syntax}

```javascript
{
  $push: {
    <field>: {
      $each: [ <value1>, <value2>],
      <modifier1>: <value1>,
      <modifier2>: <value2>
    }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field>`** | 要更新的字段。|
| **`$each`** | 要添加到数组字段中的值的数组。|
| **`<modifier>`** | 可选的修饰符，例如 `$sort`、`$slice` 和 `$position`，用于控制 `$push` 操作的行为。|
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

### 示例 1：向数组中添加多个元素 {#example-1-add-multiple-elements-to-an-array}

此查询向 `promotionEvents` 数组中添加多个新的促销活动。

```javascript
db.stores.updateOne({
    name: "Lenore's New DJ Equipment Store"
}, {
    $push: {
        promotionEvents: {
            $each: [{
                    eventName: "Grand Savings",
                    promotionalDates: {
                        startDate: "2024-08-01",
                        endDate: "2024-08-31"
                    },
                    discounts: [{
                        categoryName: "DJ Headphones",
                        discountPercentage: 5
                    }]
                },
                {
                    eventName: "Big Bargain",
                    promotionalDates: {
                        startDate: "2024-11-25",
                        endDate: "2024-11-30"
                    },
                    discounts: [{
                        categoryName: "DJ Headphones",
                        discountPercentage: 20
                    }]
                }
            ]
        }
    }
})
```

此查询返回以下结果。

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "0",
    "modifiedCount": "0",
    "upsertedCount": 0
  }
]
```
