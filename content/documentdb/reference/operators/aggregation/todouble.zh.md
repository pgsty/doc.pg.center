---
title: $toDouble
description: $toDouble 运算符将表达式转换为 Double 值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$todouble.md
weight: 370
translation_source_sha256: d4a73d71c04c7c400c5a16726306ef0e5c5fb2e3da790e5547f8cbdda6c92026
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$toDouble` 运算符将指定的值转换为 Double 值。

## 语法 {#syntax}

```javascript
{
    $toDouble: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要转换为 Double 值的指定值 |
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

### 示例 1：将字符串值转换为 Double 值 {#example-1-convert-a-string-value-into-a-double-value}

要将数字 72 的字符串表示形式（"72"）转换为双精度浮点值，可对字符串运行使用 $toDouble 运算符的查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsDouble: {
            $toDouble: {
                $toString: "72"
            }
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
        "latitudeAsDouble": 72
    }
]
```

下表描述了 $toDouble 运算符根据输入值的数据类型所表现出的预期行为。

| **值类型**                                               | **行为/输出** |
|--------------------------------------------------------------|---------------------|
| 布尔值 true                                           | 输出 -> 1         |
| 布尔值 false                                          | 输出 -> 0         |
| Double 值。例如，72.0                                     | 输出 -> 72        |
| 数字值的字符串表示形式。例如，"72"  | 输出 -> 72        |
| null 值                                                   | 输出 -> null      |
