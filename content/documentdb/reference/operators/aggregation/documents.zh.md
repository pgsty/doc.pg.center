---
title: $documents
description: $documents 阶段从一组提供的文档创建流水线。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$documents.md
weight: 90
translation_source_sha256: cd66d96c9913b99edd9c2bc531818badfcd4814c68e9edd1fbf3367de4006524
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$documents` 聚合流水线阶段用于从一组提供的文档创建流水线。当你希望处理特定文档而无需查询集合时，此阶段特别有用。

## 语法 {#syntax}

```javascript
{
  $documents: [
    <document1>,
    <document2>,
    ...
  ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<document>`** | 表示要包含在流水线中的文档的 JSON 对象。 |
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

### 示例 1：从特定文档创建流水线 {#example-1-create-a-pipeline-from-specific-documents}

此查询演示了如何使用 `$documents` 阶段来处理一组预定义的文档：

```javascript
db.aggregate([{
    $documents: [{
        _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        name: "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        location: {
            lat: 60.1441,
            lon: -141.5012
        },
        sales: {
            fullSales: 3700
        },
        tag: ["#ShopLocal", "#SeasonalSale"]
    }, {
        _id: "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        name: "Contoso, Ltd. | Office Supply Deals - South Shana",
        location: {
            lat: 40.7128,
            lon: -74.0060
        },
        sales: {
            fullSales: 5400
        },
        tag: ["#TechDeals", "#FreeShipping"]
    }]
}, {
    $project: {
        _id: 1,
        name: 1,
        "location.lat": 1,
        "location.lon": 1,
        "sales.fullSales": 1,
        tags: "$tag"
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "location": {
            "lat": 60.1441,
            "lon": -141.5012
        },
        "sales": {
            "fullSales": 3700
        },
        "tags": [
            "#ShopLocal",
            "#SeasonalSale"
        ]
    },
    {
        "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
        "location": {
            "lat": 40.7128,
            "lon": -74.006
        },
        "sales": {
            "fullSales": 5400
        },
        "tags": [
            "#TechDeals",
            "#FreeShipping"
        ]
    }
]
```

### 示例 2：将 `$documents` 与其他流水线阶段结合使用 {#example-2-combine-documents-with-other-pipeline-stages}

此查询将 $documents 流水线阶段与 $match 和 $sort 流水线阶段结合使用。

```javascript
db.aggregate([{
    $documents: [{
        _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        name: "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        location: {
            lat: 60.1441,
            lon: -141.5012
        },
        sales: {
            fullSales: 3700
        },
        tag: ["#ShopLocal", "#SeasonalSale"]
    }, {
        _id: "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        name: "Contoso, Ltd. | Office Supply Deals - South Shana",
        location: {
            lat: 40.7128,
            lon: -74.0060
        },
        sales: {
            fullSales: 5400
        },
        tag: ["#TechDeals", "#FreeShipping"]
    }]
}, {
    $match: {
        "sales.fullSales": {
            $gt: 4000
        }
    }
}, {
    $sort: {
        "sales.fullSales": -1
    }
}])
```

此查询返回以下结果：

```json
[
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "location": { "lat": 40.7128, "lon": -74.006 },
    "sales": { "fullSales": 5400 },
    "tag": [ "#TechDeals", "#FreeShipping" ]
  }
]
```

## 限制条件 {#limitations}

- $documents 阶段仅在数据库级聚合流水线中受支持。
- 它必须是流水线中的第一个阶段，才能正确运行。
