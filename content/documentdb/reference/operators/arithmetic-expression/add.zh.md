---
title: $add
description: $add 运算符返回两个数字的和，或日期与数字的和。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$add.md
weight: 20
translation_source_sha256: 4d0c122fb9f4b1deb38dd15745141d1b70cbad727c539eb748b2106471ce791b
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$add` 运算符用于将数字相加，或对数字和日期进行相加。当对数字和日期相加时，数字被视为毫秒数。

## 语法 {#syntax}

```javascript
{
  $add: [ <listOfExpressions> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<listOfExpressions>`** | 任何有效表达式，其结果为数字或日期。表达式可以是数字和日期的任意组合。 |
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

<span id="example-1-get-the-current-and-project-staff-count"></span>

### 示例 1 - 获取当前员工人数并预测未来员工人数 {#example-1---get-the-current-and-project-staff-count}

要计算总员工人数并预测未来总员工人数，可在嵌套的 totalStaff 对象上使用 $add 运算符，以返回所需结果。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
    }
}, {
    $project: {
        name: 1,
        currentTotalStaff: {
            $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
        },
        projectedNextYearStaff: {
            $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime", 2]
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "currentTotalStaff": 39,
    "projectedNextYearStaff": 41
  }
]
```
