---
title: $cmp
description: $cmp 运算符比较两个值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$cmp.md
weight: 10
translation_source_sha256: a1c131f3ec35212500adc92fb9b8261490eb86b3110072d14c529d286984e2ca
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$cmp` 运算符比较两个指定的值。若第一个值小于第二个值，$cmp 运算符返回 -1；若两值相等，返回 0；若第一个值大于第二个值，返回 1。

## 语法 {#syntax}

```javascript
{
  $cmp: [<firstValueToCompare>, <secondValueToCompare>]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<firstValueToCompare>`** | 第一个值，$cmp 运算符将其与第二个值进行比较。|
| **`<secondValueToCompare>`** | 第二个值，$cmp 运算符将第一个值与之进行比较。|
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

<span id="example-1-compare-the-total-sales-of-stores-to-25-000"></span>

### 示例 1：将商店总销售额与 $25,000 比较 {#example-1---compare-the-total-sales-of-stores-to-25000}

要将 Boulder Innovations 公司的商店总销售额与 $25,000 比较，先运行查询，按商店的公司名称筛选。然后使用 $cmp 将 sales.totalSales 字段与 25000 比较。最后，仅投影结果中各商店的名称和总销售额。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["Boulder Innovations"]
        }
    }
}, {
    $project: {
        name: 1,
        "sales.salesByCategory.totalSales": 1,
        greaterThan25000: {
            $cmp: ["$sales.revenue", 25000]
        }
    }
}])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "a5040801-d127-4950-a320-e55f6aed4b36",
        "name": "Boulder Innovations | DJ Equipment Pantry - West Christopher",
        "sales": {
            "salesByCategory": [
                {
                    "totalSales": 21522
                }
            ]
        },
        "greaterThan25000": -1
    },
    {
        "_id": "bb6e097a-e204-4b64-9f13-5ae8426fcc76",
        "name": "Boulder Innovations | Kitchen Appliance Outlet - Lake Chazville",
        "sales": {
            "salesByCategory": [
                {
                    "totalSales": 24062
                },
                {
                    "totalSales": 24815
                }
            ]
        },
        "greaterThan25000": 1
    }
]
```
