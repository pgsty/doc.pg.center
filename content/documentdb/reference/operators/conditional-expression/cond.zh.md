---
title: $cond
description: $cond 运算符用于对条件求值，并根据结果返回两个表达式中的一个。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/conditional-expression/$cond.md
weight: 10
translation_source_sha256: 8c92f55df22243ea41d3bae60ba44fae7677ba8358e15b7217bd718e218518ed
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 说明使用小写的“high”和“low”，而代码返回“High”和“Low”。实际结果字符串的大小写以代码为准。

`$cond` 运算符用于对条件求值，并根据结果返回两个表达式中的一个。它类似于许多编程语言中的三元运算符。`$cond` 运算符可用于聚合流水线，为查询添加条件逻辑。

## 语法 {#syntax}

```javascript
{
   $cond: {
      if: <boolean-expression>,
      then: <true-case>,
      else: <false-case>
   }
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **if**| 要求值的布尔表达式。|
| **then**| `if` 条件的求值结果为 true 时返回的表达式。|
| **else**| `if` 条件的求值结果为 false 时返回的表达式。|
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

### 示例 1：确定销售额高的类别 {#example-1-determine-high-sales-categories}

此查询以 $250,000 为阈值，判断每个类别的销售额应归为 "high" 还是 "low"。

```javascript
db.stores.aggregate([{
        $project: {
            _id: 0,
            storeId: "$storeId",
            category: "$sales.salesByCategory.categoryName",
            sales: "$sales.salesByCategory.totalSales",
            salesCategory: {
                $cond: {
                    if: {
                        $gte: ["$sales.salesByCategory.totalSales", 250000]
                    },
                    then: "High",
                    else: "Low"
                }
            }
        }
    },
    // Limit the result to the first 3 documents
    {
        $limit: 3
    }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "sales": [
            35921,
            1000
        ],
        "category": [
            "DJ Headphones",
            "DJ Cables"
        ],
        "salesCategory": "High"
    },
    {
        "sales": [
            4760
        ],
        "category": [
            "Guitars"
        ],
        "salesCategory": "High"
    },
    {
        "sales": [
            14697,
            44111,
            37854,
            46211,
            7269,
            25451,
            21083
        ],
        "category": [
            "Washcloths",
            "Innerspring Mattresses",
            "Microfiber Towels",
            "Shower Curtains",
            "Bathrobes",
            "Tablecloths",
            "Bath Accessories"
        ],
        "salesCategory": "High"
    }
]
```

### 示例 2：判断全职还是兼职员工占多数 {#example-2-determine-full-time-or-part-time-dominance}

此查询判断商店雇用的全职员工和兼职员工哪一种更多。

```javascript
db.stores.aggregate([{
        $project: {
            name: 1,
            staffType: {
                $cond: {
                    if: {
                        $gte: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
                    },
                    then: "More Full-Time",
                    else: "More Part-Time"
                }
            }
        }
    },
    // Limit the result to the first 3 documents
    {
        $limit: 3
    }
])
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "staffType": "More Full-Time"
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "staffType": "More Full-Time"
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "staffType": "More Part-Time"
  }
]
```
