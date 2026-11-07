---
title: $stddevpop
description: $stddevpop 运算符计算指定值的标准差
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$stddevpop.md
weight: 150
translation_source_sha256: d015a2ace90dcf212869f6ff1bb04258e1dc50a7ff4bff86b0de78616f2a52f6
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 原文简介使用 `$stddevpop`，而示例代码使用 `$stdDevPop`。此处保留原始拼写；阅读示例时，应以代码中的标识符为准。

`$stddevpop` 运算符计算指定值的标准差。该运算符只能计算数值的标准差。

## 语法 {#syntax}

```javascript
{
  $stddevpop: {fieldName}
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`fieldName`** | 用于计算标准差的字段 |
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

<span id="example-1-calculate-the-standard-deviation-of-total-sales"></span>

### 示例 1 - 计算总销售额的标准差 {#example-1---calculate-the-standard-deviation-of-total-sales}

要计算 "Fourth Coffee" 公司旗下门店所有销售类别总销售额的标准差，首先按 company 字段过滤，然后使用 stddevpop 对筛选所得门店的总销售额计算标准差，并返回聚合结果。

```javascript
db.stores.aggregate([{
    $match: {
        company: "Fourth Coffee"
    }
}, {
    $group: {
        _id: "$company",
        stdDev: {
            $stdDevPop: "$sales.totalSales"
        }
    }
}])[{
    _id: 'Fourth Coffee',
    stdDev: 0
}]
```

此查询返回以下结果：

```json
[
  {
      "_id": "Fourth Coffee",
      "stdDev": 39133.27057120701
  }
]
```

<span id="example-2-calculate-the-standard-deviation-of-a-field-with-a-single-value"></span>

### 示例 2 - 计算仅包含一个值的字段的标准差 {#example-2---calculate-the-standard-deviation-of-a-field-with-a-single-value}

当字段仅包含一个不同值时，标准差为 0。此查询对属于 "Fourth Company" 的文档进行分组。每个商店仅包含一个文档，且总销售额仅有一个不同值。

```javascript
db.stores.aggregate([{
    $match: {
        company: "Fourth Coffee"
    }
}, {
    $group: {
        _id: "$name",
        stdDev: {
            $stdDevPop: "$sales.totalSales"
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
      "_id": "Fourth Coffee | Outdoor Equipment Collection - Kochview",
      "stdDev": 0
  },
  {
      "_id": "Fourth Coffee | Grocery Hub - Brakusborough",
      "stdDev": 0
  },
  {
      "_id": "Fourth Coffee | Pet Supply Nook - Lake Armanimouth",
      "stdDev": 0
  },
  {
      "_id": "Fourth Coffee | Beauty Product Nook - Emmytown",
      "stdDev": 0
  },
  {
      "_id": "Fourth Coffee | Bed and Bath Closet - Legroston",
      "stdDev": 0
  },
  {
      "_id": "Fourth Coffee | Automotive Part Collection - Cassinport",
      "stdDev": 0
  }
]
```

<span id="example-3-calculate-the-standard-deviation-for-a-field-when-using-window-operators"></span>

### 示例 3 - 使用窗口运算符计算字段的标准差 {#example-3---calculate-the-standard-deviation-for-a-field-when-using-window-operators}

此查询计算属于 "First Up Consultants" 公司的商店从结果集中的第一个文档到当前文档之间总销售额的标准差。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        },
        $and: [{
            lastUpdated: {
                $gt: ISODate("2024-09-01T03:06:24.180Z")
            }
        }, {
            lastUpdated: {
                "$lt": ISODate("2025-09-30T03:55:17.557Z")
            }
        }]
    }
}, {
    $setWindowFields: {
        partitionBy: "$company",
        sortBy: {
            lastUpdated: 1
        },
        output: {
            stdDevPopTotalSales: {
                $stdDevPop: "$sales.totalSales",
                window: {
                    documents: ["unbounded", "current"]
                }
            }
        }
    }
}, {
    $project: {
        company: 1,
        name: 1,
        "sales.totalSales": 1,
        lastUpdated: 1,
        stdDevPopTotalSales: 1
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "sales": {},
        "company": "First Up Consultants",
        "lastUpdated": {
            "$date": "2025-06-11T10:48:01.291Z"
        },
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "stdDevPopTotalSales": null
    }
]
```
