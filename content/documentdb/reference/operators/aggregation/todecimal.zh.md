---
title: $toDecimal
description: $toDecimal 运算符将表达式转换为 Decimal 类型
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$todecimal.md
weight: 360
translation_source_sha256: 1bd29ef1f4bfc07dfd52003b311c1a3581de62f2129868b9d4670080156778ea
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$toDecimal` 运算符将输入表达式转换为 Decimal 值。Long、Double 或 Int 值将直接转换为 Decimal 数据类型，而 Decimal 值则原样返回。布尔值 true 被转换为 1，布尔值 false 被转换为 0。最后，ISODate 值将被转换为对应于该 ISODate 值自 1970 年 1 月 1 日以来的毫秒数的 Decimal 值。

## 语法 {#syntax}

```javascript
{
    $toDecimal: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要转换为 Decimal 值的指定值 |
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

### 示例 1：将 Double 值转换为 Decimal 值 {#example-1-convert-a-double-value-into-a-decimal-value}

要将 latitude 字段的值从 Double 转换为 Decimal 值，请使用 $toDecimal 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsDecimal: {
            $toDecimal: "$location.lat"
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalLatitude": 72.8377,
        "latitudeAsDecimal": "Decimal128('72.8377000000000')"
    }
]
```

<span id="example-2-convert-an-iso-date-value-into-a-decimal-value"></span>

### 示例 2：将 ISODate 值转换为 Decimal 值 {#example-2-convert-an-isodate-value-into-a-decimal-value}

要将 ISODate 转换为 Decimal 值，请对目标值使用 $toDecimal 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        dateAsDecimal: {
            $toDecimal: ISODate("2025-01-06T00:00:00.000Z")
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "dateAsDecimal": "Decimal128('1736121600000')"
    }
]
```
