---
title: $expMovingAvg
description: $expMovingAvg 运算符根据指定的最高权重文档数量，计算字段的移动平均值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$expmovingavg.md
weight: 60
translation_source_sha256: 05f3402ff80dd68732d5594a47fa3680d2f82b31868e4206da783daaa5f04dc1
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$expMovingAvg` 运算符计算指定字段值的指数移动平均值。

## 语法 {#syntax}

```javascript
{
    $expMovingAvg: {
        input: < field to use for calculation >,
        N: < number of recent documents with the highest weight
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`input`** | 用于计算指数移动平均值的字段|
| **`N`** | 计算指数移动平均值时具有最高权重的先前文档数量|
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

<span id="example-1-calculate-the-exponential-moving-average-of-total-sales"></span>

### 示例 1 - 计算总销售额的指数移动平均值 {#example-1---calculate-the-exponential-moving-average-of-total-sales}

要获取 First Up Consultants 公司旗下所有商店总销售额的指数移动平均值，先按公司执行查询筛选。然后按开业日期升序排列结果文档。最后赋予最近两个文档最高权重，以计算总销售额的指数移动平均值。

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
            "storeOpeningDate": 1
        },
        "output": {
            "expMovingAvgForSales": {
                "$expMovingAvg": {
                    "input": "$sales.totalSales",
						        "N": 2
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
        "storeOpeningDate": 1,
        "expMovingAvgForSales": 1
    }
  }])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "sales": {
            "revenue": 37701
        },
        "company": "First Up Consultants",
        "storeOpeningDate": {
            "$date": 1633219200000
        },
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "expMovingAvgForSales": 37701
    },
    {
        "_id": "8e7a259b-f7d6-4ec5-a521-3bed53adc587",
        "name": "First Up Consultants | Drone Stop - Lake Joana",
        "sales": {
            "revenue": 14329
        },
        "company": "First Up Consultants",
        "storeOpeningDate": {
            "$date": 1706958339311
        },
        "expMovingAvgForSales": 22119.666666666668
    }
]
```

<span id="example-2-calculate-the-exponential-moving-average-of-the-total-sales-using-the-alpha-parameter"></span>

### 示例 2 - 使用 alpha 参数计算总销售额的指数移动平均值 {#example-2---calculate-the-exponential-moving-average-of-the-total-sales-using-the-alpha-parameter}

要获取 First Up Consultants 公司旗下所有商店总销售额的指数移动平均值，先按公司执行查询筛选。然后按开业日期升序排列结果文档。最后指定衰减率（alpha），以计算总销售额的指数移动平均值。alpha 值越大，先前文档在计算中的权重越低。

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
                "storeOpeningDate": 1
            },
            "output": {
                "expMovingAvgForSales": {
                    "$expMovingAvg": {
                        "input": "$sales.totalSales",
                        "alpha": 0.75
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
            "storeOpeningDate": 1,
            "expMovingAvgForSales": 1
        }
    }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "sales": {
            "revenue": 37701
        },
        "company": "First Up Consultants",
        "storeOpeningDate": "2021-10-03T00:00:00.000Z",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "expMovingAvgForSales": 37701
    },
    {
        "_id": "8e7a259b-f7d6-4ec5-a521-3bed53adc587",
        "name": "First Up Consultants | Drone Stop - Lake Joana",
        "sales": {
            "revenue": 14329
        },
        "company": "First Up Consultants",
        "storeOpeningDate": "2024-09-02T00:05:39.311Z",
        "expMovingAvgForSales": 20172
    }
]
```
