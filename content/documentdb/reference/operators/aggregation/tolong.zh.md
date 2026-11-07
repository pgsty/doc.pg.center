---
title: $toLong
description: $toLong 运算符将表达式转换为 Long 值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$tolong.md
weight: 390
translation_source_sha256: bf44ab37e061bb3b9c73d617a4ea03db2e45d7122a06fb22ac4e1225f0f60f23
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 原文行为表对 true 和 false 都列出了 Long("1") 这一输出。此处为便于追溯而保留这一可疑条目，不应将其视为已验证的转换结果。

`$toLong` 运算符将指定的值转换为 Long 值。

## 语法 {#syntax}

```javascript
{
    $toLong: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要转换为长整型值的指定值 |
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

### 示例 1：将 Double 值转换为 Long 值 {#example-1-convert-a-double-value-into-a-long-value}

要将 latitude 字段的值从 Double 转换为 Long 值，请在该字段上使用 $toLong 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsLong: {
            $toLong: "$location.lat"
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
        "latitudeAsLong": "Long('72')"
    }
]
```

### 示例 2：将 String 值转换为 Long 值 {#example-2-convert-a-string-value-into-a-long-value}

要将字符串形式的 72（"72"）转换为 Long 值，请在字符串上使用 $toLong 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsLong: {
            $toLong: {
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
        "latitudeAsLong": Long('72')
    }
]
```

下表描述了 $toLong 运算符根据输入值的数据类型所表现出的预期行为。

| **值类型**                                               | **行为/输出** |
|--------------------------------------------------------------|---------------------|
| 布尔值 true                                           | 输出 -> Long("1") |
| 布尔值 false                                          | 输出 -> Long("1") |
| Double 值。例如，72.0                                     | 输出 -> Long("72")|
| Long 值的字符串表示形式。例如，"72"     | 输出 -> Long("72")|
| Double 值的字符串表示形式。例如，"72.0" | 输出 -> 错误     |
| null 值                                                   | 输出 -> null      |
