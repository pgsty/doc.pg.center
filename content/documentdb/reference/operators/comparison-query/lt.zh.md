---
title: $lt
description: $lt 运算符获取字段值小于指定值的文档
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/operators/comparison-query/$lt.md
weight: 60
translation_source_sha256: c47f75d74820ef34796de2e21a8a568bb94f0c04eada1438f1fb089f8d910482
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$lt` 运算符获取字段值严格小于指定值的文档。`$lt` 运算符可根据数值、日期或字符串值筛选文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $lt: value
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 文档中要判断的字段。|
| **`value`** | 要与字段值进行比较的值。此运算符匹配字段值小于该指定值的文档。|
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

<span id="example-1-find-a-store-with-sales-below-36-000"></span>

### 示例 1：查找销售额低于 $36,000 的商店 {#example-1-find-a-store-with-sales-below-36000}

要查找销售额低于 $36,000 的商店，先运行查询，对 sales.totalSales 字段使用 $lt。然后仅投影结果中商店的名称和总销售额，并将结果数量限制为一个文档。

```javascript
db.stores.find({
    "sales.totalSales": {
        $lt: 36000
    }
}, {
    name: 1,
    "sales.totalSales": 1
}, {
    limit: 1
})
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
        "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
        "sales": { "totalSales": 17676 }
    }
]
```
