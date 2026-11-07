---
title: $covariancePop
description: $covariancePop 运算符返回两个数值表达式的协方差
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$covariancepop.md
weight: 10
translation_source_sha256: 0a0a5a81707f83d3cb23039c4c4c248f6367ca05e63afe27ac21d5443b5272f5
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 原文将 `numericalExpression1` 和 `numericalExpression2` 都描述为“第一个”表达式。它们在语法块中分别处于第一、第二个位置。

`$covariancePop` 运算符在分区内按一个或多个字段对文档排序，并计算指定文档窗口内两个数值字段的协方差。

## 语法 {#syntax}

```javascript
{
  $covariancePop: [ < numericalExpression1 > , < numericalExpression2 > ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`numericalExpression1`** | 用于计算指定文档窗口内协方差的第一个数值表达式|
| **`numericalExpression2`** | 用于计算指定文档窗口内协方差的第一个数值表达式|
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

<span id="example-1-calculate-the-covariance-in-sales-volume"></span>

### 示例 1 - 计算销售额的协方差 {#example-1---calculate-the-covariance-in-sales-volume}

要获取 First Up Consultants 公司旗下商店总销售额的协方差，先按公司名称执行查询筛选，再按最后更新时间戳升序排列结果文档，并计算排序后结果集中第一个文档到当前文档之间的协方差。

```javascript
db.stores.aggregate(
    [{
            "$match": {
                "company": {
                    "$in": [
                        "First Up Consultants"
                    ]
                }
            }
        },
        {
            "$setWindowFields": {
                "partitionBy": "$company",
                "sortBy": {
                    "lastUpdated": 1
                },
                "output": {
                    "covariancePopForSales": {
                        "$covariancePop": [{
                                "$hour": "$lastUpdated"
                            },
                            "$sales.totalSales"
                        ],
                        "window": {
                            "documents": [
                                "unbounded",
                                "current"
                            ]
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "company": 1,
                "name": 1,
                "sales.totalSales": 1,
                "lastUpdated": 1,
                "covariancePopForSales": 1
            }
        }
    ]
)
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "sales": {},
        "company": "First Up Consultants",
        "lastUpdated": "2025-06-11T10:48:01.291Z",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "covariancePopForSales": null
    },
    {
        "_id": "8e7a259b-f7d6-4ec5-a521-3bed53adc587",
        "name": "First Up Consultants | Drone Stop - Lake Joana",
        "sales": {},
        "company": "First Up Consultants",
        "lastUpdated": {
            "t": 1727827539,
            "i": 1
        },
        "covariancePopForSales": null
    }
]
```
