---
title: $map
description: $map 运算符允许对数组中的每个元素应用表达式。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$map.md
weight: 70
translation_source_sha256: 1f240db16dc7c3b2ce6a94020133a8c5f4020b5ac42ea117ae6cd3d1ca2b9f98
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例标题说的是提取类别名称，但代码实际给每个销售额加 500，并将结果放在 `categoryNames` 字段中。标题和输出字段名均沿用上游。

`$map` 运算符用于对数组中的每个元素应用表达式，并返回应用结果组成的数组。该运算符适用于文档中数组的转换，例如修改每个元素或提取特定字段。

## 语法 {#syntax}

```javascript
{
  $map: {
    input: <array>,
    as: <variable>,
    in: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 由表达式处理的数组。 |
| **`as`** | 数组中每个元素的变量名。 |
| **`in`** | 对每个元素应用的表达式。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "location": {
        "lat": -51.3041,
        "lon": -166.0838
    },
    "staff": {
        "totalStaff": {
            "fullTime": 5,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 266491,
        "salesByCategory": [
            {
                "categoryName": "Towel Racks",
                "totalSales": 13237
            },
            {
                "categoryName": "Washcloths",
                "totalSales": 44315
            },
            {
                "categoryName": "Face Towels",
                "totalSales": 42095
            },
            {
                "categoryName": "Toothbrush Holders",
                "totalSales": 47912
            },
            {
                "categoryName": "Hybrid Mattresses",
                "totalSales": 48660
            },
            {
                "categoryName": "Napkins",
                "totalSales": 31439
            },
            {
                "categoryName": "Pillow Cases",
                "totalSales": 38833
            }
        ]
    },
    "tag": [
        "#ShopLocal",
        "#FashionStore",
        "#SeasonalSale",
        "#FreeShipping",
        "#MembershipDeals"
    ]
}
```

### 示例 1：提取类别名称 {#example-1-extracting-category-names}

此查询按 `_id` 筛选 `stores` 集合中的文档，然后投影出新字段 `categoryNames`，其中使用 $map 运算符将 salesByCategory 数组中每个元素的 totalSales 增加 500。

```javascript
db.stores.aggregate([{
        $match: {
            _id: "988d2dd1-2faa-4072-b420-b91b95cbfd60"
        }
    },
    {
        $project: {
            categoryNames: {
                $map: {
                    input: "$sales.salesByCategory.totalSales",
                    as: "category",
                    in: {
                        $add: ["$$category", 500]
                    }
                }
            }
        }
    }
])
```

此查询返回以下结果。

```json
[
  {
      "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
      "categoryNames": [
          13737,
          44815,
          42595,
          48412,
          49160,
          31939,
          39333
      ]
  }
]
```
