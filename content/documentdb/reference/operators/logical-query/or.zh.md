---
title: $or
description: $or 运算符通过逻辑或运算连接查询子句，返回至少满足一个指定条件的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/logical-query/$or.md
weight: 40
translation_source_sha256: 9358d8a1155fecd113269cb1a714331bfdc917d7b31bbea72120877aa5d090e3
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$or` 运算符对表达式数组执行逻辑或运算，并检索至少满足一个指定条件的文档。

## 语法 {#syntax}

```javascript
{
    $or: [{
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
| `expression` | 表达式数组；至少一个表达式必须为真，文档才会被包含在内 |
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

### 示例 1：将 OR 运算用于逻辑查询 {#example-1-use-or-operation-as-logical-query}

此查询检索全职员工人数超过 15 或兼职员工人数超过 20 的商店，对这两个条件使用 $or 运算符执行查询。然后仅投影结果集中商店的 name 和 staff 字段。

```javascript
db.stores.find(
  {
    $or: [
      { "staff.employeeCount.fullTime": { $gt: 15 } },
      { "staff.employeeCount.partTime": { $gt: 20 } }
    ]
  },
  {
    "name": 1,
    "staff": 1
  }
).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3",
    "name": "Contoso, Ltd. | Home Improvement Closet - Jaskolskiview",
    "staff": {
      "employeeCount": {
        "fullTime": 16,
        "partTime": 8
      }
    }
  },
  {
    "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
    "name": "Fourth Coffee | Storage Solution Gallery - Port Camilla",
    "staff": {
      "employeeCount": {
        "fullTime": 17,
        "partTime": 15
      }
    }
  }
]
```

### 示例 2：将 OR 运算符用于布尔表达式，找出销售额高或员工人数多的商店 {#example-2-use-or-operator-as-boolean-expression-to-identify-stores-with-either-high-sales-or-large-staff}

此查询检索总销售额大于 50,000 或员工总人数超过 25 的商店。

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: { 
        $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] 
      },
      qualifiesForProgram: {
        $or: [
          { $gt: ["$sales.totalSales", 50000] },
          { $gt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 25] }
        ]
      }
    }
  },
  { $limit: 4 }
])
```

此查询返回的前四个结果如下：

```json
[
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalStaff": 31,
    "qualifiesForProgram": true
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalStaff": 27,
    "qualifiesForProgram": true
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "totalStaff": 13,
    "qualifiesForProgram": false
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "totalStaff": 2,
    "qualifiesForProgram": false
  }
]
```

## 性能注意事项 {#performance-considerations}

- 参考以下建议以提高性能。
  - `$or` 数组中的每个条件独立求值
  - 尽可能使用索引以提高性能
  - 考虑条件的排列顺序，以获得最佳执行效果
  - 对同一字段进行多项相等性检查时，使用 `$in` 代替 `$or`
  - 将 `$or` 条件的数量控制在合理范围内
