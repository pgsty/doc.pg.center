---
title: $and
description: $and 运算符连接多个查询子句，返回满足所有指定条件的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/logical-query/$and.md
weight: 10
translation_source_sha256: 440de92a9559fc4753333c1301527147014f1e9b06dbd7f2da58ffa8e241abf6
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$and` 运算符对表达式数组执行逻辑与运算，并检索满足所有表达式的文档。

## 语法 {#syntax}

```javascript
{
    $and: [{
        < expression1 >
    }, {
        < expression2 >
    }, ..., {
        < expressionN >
    }]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `expression` | 表达式数组；所有表达式都必须为真，文档才会包含在结果中 |
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

### 示例 1：将 AND 运算符用于逻辑查询 {#example-1-use-and-operator-as-logical-query}

此查询使用 `$and` 运算符，筛选全职员工人数大于 10 且兼职员工人数小于 15 的商店。它仅投影 `name` 和 `staff` 字段，并将结果限制为三条记录。

```javascript
db.stores.find({
    $and: [{
        "staff.employeeCount.fullTime": {
            $gt: 10
        }
    }, {
        "staff.employeeCount.partTime": {
            $lt: 15
        }
    }]
}, {
    "name": 1,
    "staff": 1
}).limit(3)
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "e60c807b-d31c-4903-befb-5d608f260ba3",
        "name": "Wide World Importers | Appliance Emporium - Craigfort",
        "staff": {
            "totalStaff": {
                "fullTime": 11,
                "partTime": 8
            }
        }
    },
    {
        "_id": "70032165-fded-47b4-84a3-8d9c18a4d1e7",
        "name": "Northwind Traders | Picture Frame Bazaar - Lake Joesph",
        "staff": {
            "totalStaff": {
                "fullTime": 14,
                "partTime": 0
            }
        }
    },
    {
        "_id": "dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3",
        "name": "Contoso, Ltd. | Home Improvement Closet - Jaskolskiview",
        "staff": {
            "totalStaff": {
                "fullTime": 16,
                "partTime": 8
            }
        }
    }
]
```

### 示例 2：将 AND 运算符用于布尔表达式，查找销售额高且员工充足的商店 {#example-2-use-and-operator-as-boolean-expression-to-find-stores-with-high-sales-and-sufficient-staff}

此查询查找总销售额大于 100,000 且员工总人数超过 30 的商店。

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: {
        $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"]
      },
      meetsHighPerformanceCriteria: {
        $and: [
          { $gt: ["$sales.totalSales", 100000] },
          { $gt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 30] }
        ]
      }
    }
  },
  { $limit: 2 }
])
```

此查询返回的前两个结果如下：

```json
[
 {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalStaff": 31,
    "meetsHighPerformanceCriteria": false
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalStaff": 27,
    "meetsHighPerformanceCriteria": false
  }
]
```
