---
title: $percentile
description: $percentile 运算符用于计算符合筛选条件的数值的百分位数
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$percentile.md
weight: 140
translation_source_sha256: 6eb7ea277b90b0565aea78bb9e7640d330dd12f291b47ef2e6ec1b8bc7a4893f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$percentile` 运算符用于计算符合筛选条件的数值的百分位数。该运算符特别适用于识别统计阈值，例如中位数或百分位数。

## 语法 {#syntax}

```javascript
$percentile: {
    input: < field or expression > ,
    p: [ < percentile values > ],
    method: < method >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 指定用于计算百分位数的数值数据。 |
| **`p`** | 要计算的百分位数值数组（取值范围为 0 到 1）。 |
| **`method`** | 指定使用的插值方法。有效值为 `"approximate"` 和 `"continuous"`。 |
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

### 示例 1：计算销售量的第 50 百分位数 {#example-1-calculate-the-50th-percentile-of-sales-volume}

此查询计算所有商店中每个销售类别内的总销售量的第 50 百分位数（中位数）。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: null,
            medianSales: {
                $percentile: {
                    input: "$sales.salesByCategory.totalSales",
                    p: [0.5],
                    method: "approximate"
                }
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": null,
        "medianSales": [
            25070.449624139295
        ]
    }
]
```

### 示例 2：计算多个百分位数 {#example-2-calculate-multiple-percentiles}

此查询计算所有商店中总销售量的第 25、第 50 和第 75 百分位数。

```javascript
db.stores.aggregate([{
    $group: {
        _id: null,
        percentiles: {
            $percentile: {
                input: "$sales.fullSales",
                p: [0.25, 0.5, 0.75],
                method: "approximate"
            }
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": null,
        "percentiles": [
            3700,
            3700,
            3700
        ]
    }
]
```
