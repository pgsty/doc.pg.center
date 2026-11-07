---
title: $trunc
description: $trunc 运算符将数字截断到指定的小数位数。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$trunc.md
weight: 150
translation_source_sha256: a89380a419b73f1f4e75b791cda3f7da3f6c4cd63f43a2eee376af78d7ae7538
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$trunc` 运算符将数字截断到指定的小数位数。

## 语法 {#syntax}

```javascript
{
  $trunc: [ <number>, <decimal place> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<number>`** | 要截断的数字。 |
| **`<decimal place>`** | 要截断到的小数位数。正值表示截断到小数点右侧，负值表示截断到小数点左侧。 |
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

<span id="example-1-fetch-truncated-location-coordinates"></span>

### 示例 1 - 获取截断后的地理位置坐标 {#example-1---fetch-truncated-location-coordinates}

要检索 "First Up Consultants" 公司内门店的截断坐标，首先运行查询以按公司名称过滤门店。然后，在纬度和经度字段上使用 $trunc 运算符，以返回所需结果。

```javascript
db.stores.aggregate([
  {
    $project: {
      truncatedLat: { $trunc: ["$location.lat", 2] }
    }
  }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
        "location": {
            "lat": 87.2239,
            "lon": -129.0506
        },
        "truncatedLatitute": 87,
        "truncatedLongitude": -129
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
        "location": {
            "lat": -29.1866,
            "lon": -112.7858
        },
        "truncatedLatitute": -29,
        "truncatedLongitude": -112
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "name": "First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort",
        "location": {
            "lat": -0.2136,
            "lon": 108.7466
        },
        "truncatedLatitute": 0,
        "truncatedLongitude": 108
    }
]
```
