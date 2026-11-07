---
title: $sampleRate
description: $sampleRate 运算符根据指定概率，从集合中随机采样文档，适用于统计分析和测试。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/miscellaneous/$samplerate.md
weight: 20
translation_source_sha256: 944eb40fd01ad410fdbb9135cf23d28b5ec84d91f9567b1b630b3972a2b5c5b8
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 运算符定义指定的是采样概率。示例中的百分比并不保证每次运行都返回精确比例的文档数。

`$sampleRate` 运算符根据指定概率，从集合中随机采样文档。处理需要代表性样本的大型数据集时，该运算符可用于统计分析、使用数据子集进行测试以及性能优化。

## 语法 {#syntax}

```javascript
{
  $match: {
    $sampleRate: <number>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`number`** | 介于 0 和 1 之间的浮点数，表示文档被纳入样本的概率。例如，0.33 表示约 33% 的文档会被采样。
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

### 示例 1：基本随机采样 {#example-1-basic-random-sampling}

此查询从 stores 集合的全部文档中随机选取三分之一并返回。

```javascript
db.stores.aggregate([{
    $match: {
        $sampleRate: 0.33
    }
}])
```

### 示例 2：结合更多筛选条件采样 {#example-2-sampling-with-more-filters}

此查询先筛选销售额超过 50,000 的商店，再从匹配文档中随机采样 50%。

```javascript
db.stores.aggregate([
  { $match: { 
    "sales.totalSales": { $gt: 50000 },
    $sampleRate: 0.5 
  }}
])
```

### 示例 3：为统计分析采样 {#example-3-sampling-for-statistical-analysis}

此查询采样 25% 的商店，并对样本数据计算统计指标。

```javascript
db.stores.aggregate([
  { $match: { $sampleRate: 0.25 } },
  { $group: {
    _id: null,
    averageSales: { $avg: "$sales.totalSales" },
    totalStores: { $sum: 1 },
    maxSales: { $max: "$sales.totalSales" },
    minSales: { $min: "$sales.totalSales" }
  }}
])
```

处理大型数据集时，如果处理全部文档的计算开销过高，$sampleRate 运算符就很适合用于统计分析和数据探索。它能高效生成有代表性的样本，用于性能测试、质量保证验证和机器学习数据集生成。该运算符非常适合近似报表场景：统计准确性能够满足要求，且处理速度优先于结果的精确性。
