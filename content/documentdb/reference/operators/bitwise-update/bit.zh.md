---
title: $bit
description: '`$bit` 运算符用于对整数值执行位运算。'
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-update/$bit.md
weight: 10
translation_source_sha256: 458b4bc9ee8b12001f4ae3db38c41fa6bab6060fd37b8db4357935b23044c09e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$bit` 运算符用于对整数值执行位运算。它可通过按位与、按位或和按位异或运算来更新文档中的整数字段。$bit 这类位运算符用于直接操作位（例如检查、设置或清除特定的位），而非递增数值。

## 语法 {#syntax}

```javascript
{
    $bit: {
        < field >: {
            < operator >: < number >
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field>`** | 要对其执行位运算的字段。 |
| **`<operator>`** | 要执行的位运算，可选值为 `and`、`or` 或 `xor`。 |
| **`<number>`** | 位运算中使用的数字。 |
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

<span id="example-1-perform-a-bitwise-and-operation-on-the-part-time-field-in-total-staff"></span>

### 示例 1：对 `totalStaff` 中的 `partTime` 字段执行按位与运算 {#example-1-perform-a-bitwise-and-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            and: 1
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
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

<span id="example-2-perform-a-bitwise-or-operation-on-the-part-time-field-in-total-staff"></span>

### 示例 2：对 `totalStaff` 中的 `partTime` 字段执行按位或运算 {#example-2--perform-a-bitwise-or-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            "or": 1
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
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

<span id="example-3-perform-a-bitwise-xor-operation-on-the-part-time-field-in-total-staff"></span>

### 示例 3：对 `totalStaff` 中的 `partTime` 字段执行按位异或运算 {#example-3-perform-a-bitwise-xor-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            "xor": 1
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
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```
