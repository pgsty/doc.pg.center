---
title: $toString
description: $toString 运算符将表达式转换为字符串
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$tostring.md
weight: 410
translation_source_sha256: a4d1b847a0ebccd7d548488ab81a97bc7a620b292ceeb1f405a85b03fb55bd84
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$toString` 运算符仅将指定表达式的值作为字符串返回。

## 语法 {#syntax}

```javascript
{
    $toString: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要转换为字符串值的指定值 |
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

### 示例 1：将 Double 值转换为字符串值 {#example-1-convert-a-double-value-into-a-string-value}

要将 latitude 字段的值从 Double 转换为字符串，需在该字段上使用 $toString 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsString: {
            $toString: "$location.lat"
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
        "latitudeAsString": "72.8377"
    }
]
```

### 示例 2：将 Int 值转换为字符串值 {#example-2-convert-an-int-value-into-a-string-value}

要将 totalSales 字段的值从 Int 转换为字符串，需在该字段上使用 $toString 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalTotalSales: "$sales.totalSales",
        totalSalesAsString: {
            $toString: "$sales.totalSales"
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalTotalSales": 9366,
        "totalSalesAsString": "9366"
    }
]
```

下表描述了 $toString 运算符根据输入值的数据类型所表现出的预期行为。

| **值类型**                                                         | **行为/输出**                  |
|------------------------------------------------------------------------|--------------------------------------|
| 布尔值 true                                                     | 输出 -> "true"                     |
| 布尔值 false                                                    | 输出 -> "false"                    |
| 任意 Double、Int、Long 或 Decimal 值。例如，72                | 输出 -> "72"                       |
| 任意 ObjectId 值。例如，ObjectId("b010763193704acdaafa8ac3")  | 输出 -> "b010763193704acdaafa8ac3" |
