---
title: $range
description: $range 运算符可生成按顺序排列的整数数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$range.md
weight: 80
translation_source_sha256: 88ca77450cd03d94eb938a5b39328c748e05e17b43a6e3c2b63e812771e629c5
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$range` 运算符用于生成按顺序排列的整数数组。此运算符可用于创建指定范围内的数字数组，适用于分页、索引或测试数据。

## 语法 {#syntax}

```javascript
{
    $range: [ <start>, <end>, <step> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`start`** | 范围的起始值（包含）。 |
| **`end`** | 范围的结束值（不包含）。 |
| **`step`** | 范围内每个数字之间的增量值（可选，默认为 1）。 |
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

### 示例 1：生成指定范围内的数字 {#example-1-generate-a-range-of-numbers}

此查询演示了使用运算符生成从 0 到 5 的整数数组，包含左边界但不包含右边界。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"
    }
}, {
    $project: {
        rangeArray: {
            $range: [0, 5]
        }
    }
}])
```

此查询返回以下结果。

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            1,
            2,
            3,
            4
        ]
    }
]
```

### 示例 2：按步长生成指定范围内的数字 {#example-2-generate-a-range-of-numbers-with-a-step-value}

此查询演示了使用运算符生成从 0 到 18 的偶数数组。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"
    }
}, {
    $project: {
        evenNumbers: {
            $range: [0, 8, 2]
        }
    }
}])
```

此查询返回以下结果。

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            2,
            4,
            6
        ]
    }
]
```
