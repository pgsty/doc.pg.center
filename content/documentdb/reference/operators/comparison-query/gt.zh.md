---
title: $gt
description: $gt 查询运算符获取字段值大于指定值的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$gt.md
weight: 30
translation_source_sha256: 18edd3b27f23a8d2b79c9469f30639985d1d8f289a5b1741bc6884cf4ede497a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$gt` 运算符获取字段值大于指定值的文档。`$gt` 运算符可查询数值和日期值，筛选超过指定阈值的记录。

## 语法 {#syntax}

```javascript
{
    field: {
        $gt: value
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 文档中要比较的字段。|
| **`value`** | 字段值应大于此值。|
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

<span id="example-1-retrieve-stores-with-sales-exceeding-35-000"></span>

### 示例 1：获取销售额超过 $35,000 的商店 {#example-1-retrieve-stores-with-sales-exceeding-35000}

要获取销售额超过 $35,000 的一个商店，先运行查询，对 sales.totalSales 字段使用 $gt 运算符，再将查询结果限制为一个商店。

```javascript
db.stores.find({
    "sales.totalSales": {
        $gt: 35000
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
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "sales": { "totalSales": 37701 }
    }
]
```

### 示例 2：查找全职员工超过 12 人的商店 {#example-2-find-a-store-with-more-than-12-full-time-staff}

要查找全职员工超过 12 人的商店，先运行查询，对 staff.totalStaff.fullTime 字段使用 $gt 运算符。然后仅投影 name 和 totalStaff 字段，并将结果集限制为匹配结果中的一个商店。

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        $gt: 12
    }
}, {
    name: 1,
    "staff.totalStaff": 1
}, {
    limit: 1
})
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "staff": { "totalStaff": { "fullTime": 18, "partTime": 17 } }
    }
]
```
