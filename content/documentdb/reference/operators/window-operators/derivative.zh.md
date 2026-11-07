---
title: $derivative
description: $derivative 运算符计算指定窗口内字段值的平均变化率。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$derivative.md
weight: 40
translation_source_sha256: 7095a072a6ede3dcf1ca914b60809959a451914374bcdc4fc6f5e9f6c88adcfa
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 参数表写的是“rate of range”，并将 unit 称为“时间窗口”，而页面定义描述的是变化率。中文将明显误写的 range 按 change 理解，译为“变化率”，同时保留原文对 unit 的说明。

`$derivative` 运算符在分区内按一个或多个字段对文档排序，并计算窗口内第一个文档到最后一个文档之间某个字段的平均变化率。

## 语法 {#syntax}

```javascript
{
    $derivative: {
        input: < expression >,
        unit: < timeWindow >
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`input`** | 要计算变化率的表达式或字段|
| **`unit`** | 计算变化率的时间窗口|
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

<span id="example-1-calculate-the-derivative-for-total-sales"></span>

### 示例 1 - 计算总销售额的导数 {#example-1---calculate-the-derivative-for-total-sales}

要计算 First Up Consultants 公司旗下每家商店总销售额的导数，先按公司执行查询筛选，按最后更新时间戳升序排列结果文档，再计算结果集中第一个文档到当前文档之间总销售额的导数（平均变化率）。

```javascript
db.stores.aggregate([{
        "$match": {
            "company": {
                "$in": [
                    "First Up Consultants"
                ]
            },
            "$and": [{
                    "lastUpdated": {
                        "$gt": ISODate("2024-12-01T03:06:24.180Z")
                    }
                },
                {
                    "lastUpdated": {
                        "$lt": ISODate("2025-12-01T03:55:17.557Z")
                    }
                }
            ]
        }
    },
    {
        "$setWindowFields": {
            "partitionBy": "$company",
            "sortBy": {
                "lastUpdated": 1
            },
            "output": {
                "storeAverageSales": {
                    "$derivative": {
                        "input": "$sales.totalSales",
                        "unit": "week"
                    },
                    "window": {
                        "range": [
                            -1,
                            0
                        ],
                        "unit": "week"
                    }
                }
            }
        }
    },
    {
        "$project": {
            "lastUpdated": 1,
            "storeAverageSales": 1
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "lastUpdated": "2025-06-11T10:48:01.291Z",
        "storeAverageSales": 21554495.708753344
    }
]
```
