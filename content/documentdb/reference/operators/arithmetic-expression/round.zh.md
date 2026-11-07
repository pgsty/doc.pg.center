---
title: $round
description: $round 运算符将数字舍入到指定的小数位数。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$round.md
weight: 120
translation_source_sha256: 784cde708a49a326df21571c6fdc91d5fbf2ead18c7ab537b4d41bb6d1558e9e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$round` 运算符用于将数字舍入到指定的小数位数。它在需要数值精度的聚合操作中非常有用，例如财务计算或统计分析。

## 语法 {#syntax}

```javascript
{
  $round: [ <number>, <place> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 需要舍入的数字。 |
| **`<place>`** | 数字应舍入到的小数位数。 |
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

<span id="example-1-round-the-location-coordinates-of-stores"></span>

### 示例 1 - 舍入门店的地理位置坐标 {#example-1---round-the-location-coordinates-of-stores}

要舍入 "First Up Consultants" 公司所有门店的纬度和经度，首先运行查询以按公司名称过滤。然后在 lat 和 lon 字段上使用 $round 运算符，以返回所需结果。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $project: {
        company: 1,
        "location.lat": 1,
        "location.lon": 1,
        roundedLat: {
            $round: ["$location.lat", 1]
        },
        roundedLon: {
            $round: ["$location.lon", 1]
        }
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "location": {
            "lat": 87.2239,
            "lon": -129.0506
        },
        "company": "First Up Consultants",
        "roundedLat": 87.2,
        "roundedLon": -129.1
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "location": {
            "lat": -29.1866,
            "lon": -112.7858
        },
        "company": "First Up Consultants",
        "roundedLat": -29.2,
        "roundedLon": -112.8
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "location": {
            "lat": -0.2136,
            "lon": 108.7466
        },
        "company": "First Up Consultants",
        "roundedLat": -0.2,
        "roundedLon": 108.7
    }
]
```

<span id="example-2-round-to-the-nearest-thousand"></span>

### 示例 2 - 舍入到最接近的千位 {#example-2---round-to-the-nearest-thousand}

要舍入 "First Up Consultants" 公司内各门店的总销售额，首先运行查询以按公司名称过滤门店。然后在 totalSales 字段上使用 $round 运算符，将数值舍入到最接近的千位。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $project: {
        company: 1,
        "sales.totalSales": 1,
        roundedSales: {
            $round: ["$sales.totalSales", -3]
        }
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "sales": {},
        "company": "First Up Consultants",
        "roundedSales": 279000
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "sales": {},
        "company": "First Up Consultants",
        "roundedSales": 50000
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "sales": {},
        "company": "First Up Consultants",
        "roundedSales": 69000
    }
]
```
