---
title: $ifNull
description: $ifNull 运算符用于对表达式求值，并在结果为 null 时返回指定值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/conditional-expression/$ifnull.md
weight: 20
translation_source_sha256: 766933ba59c73dc1d2430a4103c2fdc44486af6e56b3ed34c3bf7cfb325590f9
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例标题引用 `store.manager`，但说明和代码操作的是 `$staff.totalStaff.intern`。代码演示的是后一个字段。

`$ifNull` 运算符用于对表达式求值，并在结果为 `null` 时返回指定值。当需要为可能不存在或值可能为 `null` 的字段提供默认值时，可以使用此运算符。

## 语法 {#syntax}

```javascript
{
  $ifNull: [ <expression>, <replacement-value> ]
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`**| 要求值的表达式。|
| **`<replacement-value>`**| 表达式求值结果为 `null` 时返回的值。|
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

<span id="example-1-default-value-for-missing-store-manager-field"></span>

### 示例 1：为缺失的 `store.manager` 字段提供默认值 {#example-1-default-value-for-missing-storemanager-field}

为确保 `$staff.totalStaff.intern` 字段始终为数值，可以使用 `$ifNull` 将 `null` 值替换为 `0`。

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      interns: { $ifNull: ["$staff.totalStaff.intern", 0] }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "interns": 0
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "interns": 0
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "interns": 0
  }
]

```
