---
title: $mod
description: $mod 运算符对字段值执行取模运算，并选择结果为指定值的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/evaluation-query/$mod.md
weight: 30
translation_source_sha256: 5f4883d5a548d59ba7d349b711640aa7211d220c5276429621ee9f724929a632
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$mod` 运算符对字段值执行取模运算，并选择结果为指定值的文档。该运算符可用于查找数值字段除以某个除数后得到特定余数的文档，常用于分页、数据采样或寻找数值序列中的规律。

## 语法 {#syntax}

```javascript
{
  <field>: { $mod: [ <divisor>, <remainder> ] }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<field>`** | 要执行取模运算的字段。该字段必须包含数值。 |
| **`<divisor>`** | 用于除字段值的除数。必须为正数。 |
| **`<remainder>`** | 取模运算后的预期余数。必须为小于除数的非负数。 |
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

### 示例 1：查找销售额可被 1000 整除的商店 {#example-1-find-stores-with-sales-divisible-by-1000}

此查询检索总销售额可被 1000 整除的商店（适用于找出销售额为整千数的商店）。

```javascript
db.stores.find({
  "sales.totalSales": { $mod: [1000, 0] }
}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "new-store-001",
    "name": "TechWorld Electronics - Downtown Branch",
    "sales": {
      "totalSales": 5000
    },
    "createdDate": "2025-06-11T11:11:32.262Z",
    "status": "new",
    "staff": {
      "totalStaff": {
        "fullTime": 0,
        "partTime": 0
      }
    },
    "version": 1
  },
  {
    "_id": "gaming-store-mall-001",
    "name": "Gaming Paradise - Mall Location",
    "location": {
      "lat": 35.6762,
      "lon": 139.6503
    },
    "createdDate": "2025-06-11T11:13:27.180Z",
    "status": "active",
    "staff": {
      "totalStaff": {
        "fullTime": 8,
        "partTime": 12
      },
      "manager": "Alex Johnson",
      "departments": [
        "gaming",
        "accessories",
        "repairs"
      ]
    },
    "sales": {
      "totalSales": 0,
      "salesByCategory": []
    },
    "operatingHours": {
      "weekdays": "10:00-22:00",
      "weekends": "09:00-23:00"
    },
    "metadata": {
      "version": 1,
      "source": "store-management-system"
    }
  }
]
```

### 示例 2：分页式查询 {#example-2-pagination-style-querying}

此查询检索兼职员工人数除以 4 后余数为 0 的商店（适用于创建数据子集）。

```javascript
db.stores.find({
  "staff.totalStaff.partTime": { $mod: [4, 0] }
})
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "new-store-001",
    "name": "TechWorld Electronics - Downtown Branch",
    "sales": {
      "totalSales": 5000
    },
    "createdDate": "2025-06-11T11:11:32.262Z",
    "status": "new",
    "staff": {
      "totalStaff": {
        "fullTime": 0,
        "partTime": 0
      }
    },
    "version": 1
  },
  {
    "_id": "gaming-store-mall-001",
    "name": "Gaming Paradise - Mall Location",
    "location": {
      "lat": 35.6762,
      "lon": 139.6503
    },
    "createdDate": "2025-06-11T11:13:27.180Z",
    "status": "active",
    "staff": {
      "totalStaff": {
        "fullTime": 8,
        "partTime": 12
      },
      "manager": "Alex Johnson",
      "departments": [
        "gaming",
        "accessories",
        "repairs"
      ]
    },
    "sales": {
      "totalSales": 0,
      "salesByCategory": []
    },
    "operatingHours": {
      "weekdays": "10:00-22:00",
      "weekends": "09:00-23:00"
    },
    "metadata": {
      "version": 1,
      "source": "store-management-system"
    }
  }
]
```
