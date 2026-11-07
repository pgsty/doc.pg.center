---
title: $collStats
description: 聚合流水线中的 $collStats 流水线阶段用于返回集合的统计信息。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$collstats.md
weight: 50
translation_source_sha256: 630c0808ba7663dfcd488ea2feabec02c779daf6b78ef18c3ebf28eaaee497e2
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 $collStats 流水线阶段用于返回集合的统计信息。该阶段特别有助于了解集合的性能特征，例如文档数量、集合大小以及存储统计信息。它提供详细信息，有助于数据库优化和监控。

## 语法 {#syntax}

```javascript
{
  $collStats: {
    storageStats: { scale: <number> },
    count: {}
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`storageStats`** | 可选。指定是否包含存储统计信息。`scale` 字段是一个数字，表示存储统计信息的缩放因子。 |
| **`count`** | 可选。包含集合中文档的数量。 |
{.fields}

`latencyStats` 和 `queryExecStats` 不受支持；任一参数均会因 `collStats with <option> not supported yet`（`CommandNotSupported`）而失败。

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

### 示例：基本集合统计信息 {#example-basic-collection-statistics}

此查询统计 stores 集合中的所有文档数量。

```javascript
db.stores.aggregate([
  {
    $collStats: {
      count: {}
    }
  }
])
```

此查询返回以下结果：

```json
[
  { "ns": "StoreData.stores", "count": 41505 }
]
```
