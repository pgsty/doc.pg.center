---
title: $isNumber
description: $isNumber 运算符用于检查指定表达式是否为数值类型
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$isnumber.md
weight: 170
translation_source_sha256: 67f61ad1e19eb26058f952fda818b60253e825e1b4330292f12fa2db74e1ce3f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$isNumber` 运算符在输入表达式为数值类型时返回 true。`$isNumber` 运算符对任何其他类型的表达式均返回 false。

## 语法 {#syntax}

```javascript
{
    $isNumber: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要检查是否为数字的指定值 |
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

### 示例 1：检查 Double 值是否为数字 {#example-1-check-if-a-double-value-is-a-number}

为验证 latitude 字段的值是否为数值，可运行一个使用 $isNumber 运算符的查询，以确认该字段的 double 值为数字。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeIsNumber: {
            $isNumber: "$location.lat"
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
        "latitudeIsNumber": true
    }
]
```

### 示例 2：检查 Int 值是否为数字 {#example-2-check-if-an-int-value-is-a-number}

为验证 totalSales 字段的值是否为数值，可运行一个使用 $isNumber 运算符的查询，以确认该字段的 double 值为数字。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalTotalSales: "$sales.totalSales",
        totalSalesIsNumber: {
            $isNumber: "$sales.totalSales"
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
        "totalSalesIsNumber": true
    }
]
```

### 示例 3：检查字符串是否为数字 {#example-3-check-if-a-string-is-a-number}

为验证 _id 字段的值是否为数值，可运行一个使用 $isNumber 运算符的查询，以确认该字段的字符串值不是数字。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        idIsNumber: {
            $isNumber: "$_id"
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "idIsNumber": false
    }
]
```
