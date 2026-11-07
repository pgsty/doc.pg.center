---
title: $not
description: $not 运算符对指定表达式执行逻辑非运算，选择不匹配该表达式的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/logical-query/$not.md
weight: 30
translation_source_sha256: 3c7822171ac99b90829b7b50c84ab8554808cc8b8b2522f9040140238e404881
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$not` 运算符对指定表达式执行逻辑非运算，并选择不匹配该表达式的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $not: {
            < operator - expression >
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
|-----------|-------------|
| `operator-expression` | 要取反的表达式 |
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

### 示例 1：将 NOT 运算符用于逻辑查询 {#example-1-use-not-operation-as-logical-query-operator}

此查询将 `$not` 运算符与 $eq 组合使用，检索全职员工人数不等于 5 的商店。它最多返回两个匹配文档，且仅返回 `name` 和 `staff` 字段。

```javascript
 db.stores.find({
     "staff.totalStaff.fullTime": {
         $not: {
             $eq: 5
         }
     }
 }, {
     "name": 1,
     "staff": 1
 }).limit(2)
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "staff": {
            "totalStaff": {
                "fullTime": 9,
                "partTime": 18
            }
        }
    },
    {
        "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
        "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
        "staff": {
            "totalStaff": {
                "fullTime": 7,
                "partTime": 6
            }
        }
    }
]
```

<span id="example-2-use-not-operator-as-boolean-expression-to-identify-stores-that-aren-t-high-volume"></span>

### 示例 2：将 NOT 运算符用于布尔表达式，找出销售额不高的商店 {#example-2-use-not-operator-as-boolean-expression-to-identify-stores-that-arent-high-volume}

此查询检索销售额不高（不大于 50,000）的商店。

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      isNotHighVolume: {
        $not: { $gt: ["$sales.salesByCategory.totalSales", 50000] }
      },
      storeCategory: {
        $cond: [
          { $not: { $gt: ["$sales.salesByCategory.totalSales", 50000] } },
          "High Volume Store",
          "Small/Medium Store"
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
    "totalSales": [ 37978 ],
    "isNotHighVolume": false,
    "storeCategory": "Small/Medium Store"
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalSales": [ 25731 ],
    "isNotHighVolume": false,
    "storeCategory": "Small/Medium Store"
  }
]
```
