---
title: $pull
description: 从数组中移除某个值的所有实例。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$pull.md
weight: 80
translation_source_sha256: 5cfa92536445bac936e7ac84aa5292a5ded80612bf706edb6113d62c83b85e4d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$pull` 运算符用于从数组中移除指定值的所有实例，或移除满足条件的所有值。当需要清理或修改文档内的数组数据时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $pull: { <field>: <value|condition> }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field>`** | 要从中移除一个或多个值的字段。 |
| **`<value\|condition>`** | 要从数组中移除的值，或用于确定移除哪些值的条件。 |
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

### 示例 1：从 `tag` 数组中移除指定标签 {#example-1-remove-a-specific-tag-from-the-tag-array}

要从 tag 数组字段中移除值 "#SeasonalSale"，可运行查询，对 tag 字段使用 $pull 运算符。

```javascript
db.stores.update({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $pull: {
        tag: "#SeasonalSale"
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

<span id="example-2-remove-all-events-from-the-promotion-events-array-that-end-before-a-certain-date"></span>

### 示例 2：从 `promotionEvents` 数组中移除在指定日期之前结束的所有活动 {#example-2-remove-all-events-from-the-promotionevents-array-that-end-before-a-certain-date}

要从 promotionEvents 数组中移除 endDate 的年份为 2024 且 endDate 的月份早于 3 月的所有元素，可运行查询，对 promotionEvents 字段使用 $pull 运算符，并指定相应的日期值。

```javascript
db.stores.update({
            _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
        }, {
            $pull: {
                promotionEvents: {
                    "promotionalDates.endDate.Year": 2024,
                    "promotionalDates.endDate.Month": {
                        $lt: 3
                    }
                }
            }
        }
)
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
