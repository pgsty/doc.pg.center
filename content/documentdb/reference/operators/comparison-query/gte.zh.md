---
title: $gte
description: $gte 运算符获取字段值大于或等于指定值的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$gte.md
weight: 40
translation_source_sha256: 55ec538f374c93c1e01f5e598712d22591fe02a63e4029f7312a2cc6d29f1ae9
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 参数表遗漏了“或等于”。按定义和示例，`$gte` 包含等于阈值的情形。

`$gte` 运算符获取字段值大于或等于指定值的文档。`$gte` 运算符可获取字段值达到最低阈值的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $gte: <value>
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

<span id="example-1-find-a-store-with-sales-35-000"></span>

### 示例 1：查找销售额 >= $35,000 的商店 {#example-1-find-a-store-with-sales--35000}

要获取销售额至少为 $35,000 的一个商店，先运行查询，对 sales.totalSales 字段使用 $gte 运算符。然后仅投影商店名称及其总销售额，并将结果集限制为一个文档。

```javascript
db.stores.find({
    "sales.totalSales": {
        $gte: 35000
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

### 示例 2：查找全职员工为 12 人或更多的商店 {#example-2-find-a-store-with-12-or-more-full-time-staff}

要获取全职员工至少为 12 人的一个商店，先运行查询，对 staff.totalStaff.fullTime 字段使用 $gte 运算符。然后仅投影名称和全职员工人数，并将结果限制为结果集中的一个文档。

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        $gte: 12
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
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "staff": { "totalStaff": { "fullTime": 18 } }
    }
]
```

### 示例 3：查找 Laptops 折扣百分比大于或等于 15% 的促销活动 {#example-3-find-promotion-events-with-a-discount-percentage-greater-than-or-equal-to-15-for-laptops}

要查找两家笔记本电脑促销折扣至少为 15% 的商店，先运行查询，筛选开展笔记本电脑促销的商店。然后对 discountPercentage 字段使用 $gte 运算符。最后仅投影商店名称，并将结果限制为结果集中的两个文档。

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        $elemMatch: {
            categoryName: "Laptops",
            discountPercentage: {
                $gte: 15
            }
        }
    }
}, {
    name: 1
}, {
    limit: 2
})
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "60e43617-8d99-4817-b1d6-614b4a55c71e",
    "name": "Wide World Importers | Electronics Emporium - North Ayanashire"
  },
  {
    "_id": "3c441d5a-c9ad-47f4-9abc-ac269ded44ff",
    "name": "Contoso, Ltd. | Electronics Corner - New Kiera"
  }
]
```
