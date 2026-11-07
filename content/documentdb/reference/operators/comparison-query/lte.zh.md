---
title: $lte
description: $lte 运算符获取字段值小于或等于指定值的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$lte.md
weight: 70
translation_source_sha256: d7df62bf054d17385a25518f88546f2d1dd39bdb718f1b3e6c25097f3d8cfc7b
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$lte` 运算符获取字段值小于或等于指定值的文档。`$lte` 运算符可根据数值、日期或其他可比较的字段筛选文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $lte: <value>
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要比较的字段。|
| **`value`** | 要与字段进行比较的值。|
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

<span id="example-1-find-a-store-with-sales-35-000"></span>

### 示例 1：查找销售额 <= $35,000 的商店 {#example-1-find-a-store-with-sales--35000}

要查找销售额 <= $35,000 的商店，可运行查询，对 sales.totalSales 字段使用 $lte，并将结果文档限制为一个商店。

```javascript
db.stores.find({
    "sales.totalSales": {
        $lte: 35000
    }
}, {
    _id: 1
}, {
    limit: 1
})
```

此查询返回的第一个结果是：

```json
[
  {
    "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6"
  }
]
```

### 示例 2：查找全职员工不超过 12 人的商店 {#example-2-find-a-store-with-12-or-fewer-full-time-staff}

要查找全职员工人数 <= 12 的商店，可运行查询，对嵌套的 fullTime 字段使用 $lte。然后仅投影名称和全职员工人数，并将结果限制为结果集中的一个商店。

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        $lte: 12
    }
}, {
    name: 1,
    "staff.totalStaff.fullTime": 1
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
      "staff": { "totalStaff": { "fullTime": 6 } }
  }
]
```
