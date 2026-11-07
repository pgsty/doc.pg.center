---
title: $covarianceSamp
description: $covarianceSamp 运算符返回两个数值表达式的样本协方差
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$covariancesamp.md
weight: 20
translation_source_sha256: bea18f0611ee9ef79c16cd701bf949dcdc5b21790240b4b6279e5536369365b2
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 原文将 `numericalExpression1` 和 `numericalExpression2` 都描述为“第一个”表达式。它们在语法块中分别处于第一、第二个位置。

`$covarianceSamp` 运算符在分区内按一个或多个字段对文档排序，并计算指定文档窗口内两个数值字段的样本协方差。

## 语法 {#syntax}

```javascript
{
    $covarianceSamp: [ < numericalExpression1 > , < numericalExpression2 > ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`numericalExpression1`** | 用于计算指定文档窗口内样本协方差的第一个数值表达式|
| **`numericalExpression2`** | 用于计算指定文档窗口内样本协方差的第一个数值表达式|
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

<span id="example-1-calculate-the-covariance-sample-between-an-unbounded-starting-document-and-the-current-document"></span>

### 示例 1 - 计算从无界起点文档到当前文档之间的样本协方差 {#example-1---calculate-the-covariance-sample-between-an-unbounded-starting-document-and-the-current-document}

要计算 First Up Consultants 公司旗下商店的样本协方差，先按公司执行查询筛选，再按开业日期升序排列结果中的商店，并计算排序后结果集的销售额协方差。

```javascript
db.stores.aggregate(
[{
      "$match": {
          "company": {
              "$in": [
                  "First Up Consultants"
              ]
          },
        "$and": [
            {
                "storeOpeningDate": {
                    "$gt": ISODate("2024-09-01T03:06:24.180Z")
                }
            },
            {
                "storeOpeningDate": {
                    "$lt": ISODate("2025-09-30T03:55:17.557Z")
                }
            }
        ]
      }
  },
  {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "storeOpeningDate": 1
        },
        "output": {
            "covarianceSampForSales": {
                "$covarianceSamp": [
                    {
                        "$hour": "$storeOpeningDate"
                    },
                    "$sales.revenue"
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
        "sales.revenue": 1,
        "storeOpeningDate": 1,
        "covarianceSampForSales": 1
    }
  }]
)
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "2d315043-db26-4d18-8bb7-71ba922f00a0",
        "name": "First Up Consultants | Furniture Shoppe - Wymantown",
        "sales": {
            "revenue": 38042
        },
        "company": "First Up Consultants",
        "storeOpeningDate": "2024-09-02T02:00:52.592Z",
        "covarianceSampForSales": 935.0972222222222
    },
    {
        "_id": "416adb8c-7d65-40e5-af88-8659c71194ce",
        "name": "First Up Consultants | Picture Frame Bazaar - South Lysanneborough",
        "sales": {
            "revenue": 37157
        },
        "company": "First Up Consultants",
        "storeOpeningDate": "2024-09-02T02:39:50.269Z",
        "covarianceSampForSales": 1901.1777777777777
    }
]
```
