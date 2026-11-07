---
title: $integral
description: $integral 运算符使用指定范围内相邻的文档进行计算，求得曲线下面积。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$integral.md
weight: 70
translation_source_sha256: d472a24a33e931d405f24e6b8697313e6e806ee8857f048f6dcbb32f612140ad
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$integral` 运算符以按特定字段排序的指定范围内的文档为依据，计算曲线下面积。

## 语法 {#syntax}

```javascript
{
    $integral: {
        input: < expression > ,
        unit: < time window >
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`input`** | 文档中用于计算积分的字段|
| **`unit`** | 为积分指定的时间单位|
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

<span id="example-1-calculate-the-integral-of-total-sales"></span>

### 示例 1 - 计算总销售额的积分 {#example-1---calculate-the-integral-of-total-sales}

要计算 First Up Consultants 公司旗下所有商店总销售额的积分，先按公司名称执行查询筛选。然后按开业日期升序排列结果中的商店。最后，计算排序后结果集中第一个文档到当前文档之间总销售额的积分。

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
            "salesIntegral": {
                "$integral": {
                        "input": "$sales.revenue",
			"unit": "hour"
                },
                "window": {
                    "range": [
                        "unbounded",
                        "current"
                    ],
					        "unit": "hour"
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
        "salesIntegral": 1
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
        "storeOpeningDate": "2021-10-03T00:00:00.000Z",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "salesIntegral": 0
    },
    {
        "_id": "8e7a259b-f7d6-4ec5-a521-3bed53adc587",
        "name": "First Up Consultants | Drone Stop - Lake Joana",
        "sales": {
            "revenue": 14329
        },
        "company": "First Up Consultants",
        "storeOpeningDate": "2024-09-02T00:05:39.311Z",
        "salesIntegral": 664945851.9932402
    }
]
```
