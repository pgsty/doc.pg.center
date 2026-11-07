---
title: $nor
description: $nor 运算符对表达式数组执行逻辑或非运算，并检索所有条件均不满足的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/logical-query/$nor.md
weight: 20
translation_source_sha256: c90f6f6fe3a639ca3e0528bab35928a31523231cc14049e4afd919625dd3db49
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例 2 用“或”连接各个否定条件，这与本页对 `$nor` 的定义不一致。只有 `$nor` 内的所有表达式均不成立，文档才会匹配。

`$nor` 运算符对表达式数组执行逻辑或非运算，并选择所有指定表达式均不满足的文档。

## 语法 {#syntax}

```javascript
{
    $nor: [{
        < expression1 >
    }, {
        < expression2 >
    }, ..., {
        < expressionN >
    }]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `expression` | 表达式数组；所有表达式都必须为假，文档才会被包含在内 |
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

### 示例 1：基本或非运算 {#example-1-basic-nor-operation}

要查找全职员工人数不超过 15 且兼职员工人数不超过 20 的商店，可对这两个条件使用 $nor 运算符执行查询。然后仅投影结果集中商店的 name 和 staff 字段。

```javascript
db.stores.find({
    $nor: [{
        "staff.totalStaff.fullTime": {
            $gt: 15
        }
    }, {
        "staff.totalStaff.partTime": {
            $gt: 20
        }
    }]
}, {
    "name": 1,
    "staff": 1
})
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "staff": {
            "totalStaff": {
                "fullTime": 9,
                "partTime": 18
            }
        }
    },
    {
        "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
        "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
        "staff": {
            "totalStaff": {
                "fullTime": 7,
                "partTime": 6
            }
        }
    }
]
```

### 示例 2：复杂或非运算 {#example-2-complex-nor-operation}

要查找销售额未超过 $100,000、未销售 "Digital Watches" 或在 2024 年 9 月未开展促销的商店，可对这三个条件使用 $nor 运算符执行查询。最后仅投影结果集中商店的 name、sales 和促销活动。

```javascript
db.stores.find({
    $nor: [{
        "sales.totalSales": {
            $gt: 100000
        }
    }, {
        "sales.salesByCategory.categoryName": "Digital Watches"
    }, {
        "promotionEvents": {
            $elemMatch: {
                "promotionalDates.startDate.Month": 9,
                "promotionalDates.startDate.Year": 2024
            }
        }
    }]
}, {
    "name": 1,
    "sales": 1,
    "promotionEvents": 1
})
```

此查询返回的一个结果如下：

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "DJ Headphones",
                    "totalSales": 35921
                }
            ],
            "fullSales": 3700
        },
        "promotionEvents": [
            {
                "eventName": "Bargain Blitz Days",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 3,
                        "Day": 11
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 2,
                        "Day": 18
                    }
                },
                "discounts": [
                    {
                        "categoryName": "DJ Turntables",
                        "discountPercentage": 18
                    },
                    {
                        "categoryName": "DJ Mixers",
                        "discountPercentage": 15
                    }
                ]
            }
        ]
    }
]
```
