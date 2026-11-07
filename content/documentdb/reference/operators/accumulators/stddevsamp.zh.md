---
title: $stddevsamp
description: $stddevsamp 运算符计算的是指定样本值的标准差，而非整个总体的标准差
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$stddevsamp.md
weight: 160
translation_source_sha256: e4d91c28d745a35756f110d9220449d786ad2dfb99d933f242ace26cc4682f30
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 简介将随机采样归于标准差运算符。示例实际先通过单独的 `$sample` 阶段选取 10 个文档，再由 `$stdDevSamp` 计算这些文档的标准差。原文在简介和语法块中还使用了不一致的拼写 `$stddevsamp`。

`$stddevsamp` 运算符通过获取指定字段值的一个样本计算标准差。标准差是通过随机选取指定大小的样本计算得出的。如果需要精确的标准差，则必须改用 $stdDevPop。

## 语法 {#syntax}

```javascript
{
  $stddevsamp: {fieldName}
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`fieldName`** | 用于计算指定样本大小标准差的字段 |
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

此查询通过随机选取符合筛选条件的 10 个文档样本，计算 "Fourth Coffee" 公司各门店总销售额的标准差。

```javascript
db.stores.aggregate([{
    $match: {
        "company": "Fourth Coffee"
    }
}, {
    $sample: {
        size: 10
    }
}, {
    $group: {
        _id: "$company",
        stdDev: {
            $stdDevSamp: "$sales.totalSales"
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
      "_id": "Fourth Coffee",
      "stdDev": 22040.044055209048
  }
]
```
