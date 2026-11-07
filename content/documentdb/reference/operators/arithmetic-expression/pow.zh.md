---
title: $pow
description: '`$pow` 运算符计算数值按指定指数幂运算后的结果。'
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$pow.md
weight: 110
translation_source_sha256: 881cc96556de60ed8db0377b1ec08f52df37f4ba39b7bfd05c9c3e49c59d0725
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例说明写的是 `$power`，而本页及可执行示例使用 `$pow`。正文保留了来源中的拼写。

`$pow` 运算符计算一个数的指定次幂。

## 语法 {#syntax}

```javascript
{
  $pow: [ <number>, <exponent> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 要进行幂运算的底数。 |
| **`<exponent>`** | 用于幂运算的指数。 |
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

### 示例 1：计算总销售额的平方 {#example-1-calculate-the-square-of-total-sales-volume}

要计算 "First Up Consultants" 公司下所有门店的销售额的平方，首先运行查询以筛选公司名称。然后，在嵌套的 fullSales 字段上使用 $power 运算符，以计算所需结果。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $project: {
        company: 1,
        "sales.revenue": 1,
        fullSalesSquare: {
            $pow: ["$sales.revenue", 2]
        }
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "sales": {
            "revenue": 279183
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 558366
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "sales": {
            "revenue": 50000
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 100000
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "sales": {
            "revenue": 68508
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 137016
    }
]
```
