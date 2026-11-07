---
title: $firstN
description: $firstN 运算符根据查询指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的前 N 个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$firstn.md
weight: 60
translation_source_sha256: 8fd3dce05949d76dd91146131b1dae2afa2cdaa07d3b829dc1b9a7dadc7d4ab0
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$firstN` 运算符根据分组的排序顺序返回分组中的前 N 个值。如果未指定排序顺序，则顺序未定义。

## 语法 {#syntax}

```javascript
{
    $firstN: {
        input: [listOfFields],
        sortBy: {
            <fieldName>: <sortOrder>
        },
        n: <numDocumentsToReturn>
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`listOfFields`** | 要从结果集的前 N 个文档中返回的字段列表 |
| **`fieldName`** | 用于对结果集进行排序的字段 |
| **`sortOrder`** | 1 或 -1。1 表示按字段值升序排序，-1 表示按字段值降序排序 |
| **`n`** | 从排序后结果集顶部返回的文档数量 |
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

<span id="example-1-use-first-n-operator-as-accumulator-to-find-first-two-stores-by-total-sales"></span>

### 示例 1：将 $firstN 运算符作为累加器使用，按总销售额查找前两个商店 {#example-1-use-firstn-operator-as-accumulator-to-find-first-two-stores-by-total-sales}

要获取总销售额最高的前两个商店，运行查询以按 sales.totalSales 字段降序排序所有文档，并从排序后结果集中返回前两个文档。

```javascript
db.stores.aggregate([{
        $sort: {
            "sales.totalSales": -1
        }
    },
    {
        $group: {
            _id: null,
            topTwoStores: {
                $firstN: {
                    n: 2,
                    input: {
                        storeId: "$_id",
                        storeName: "$name",
                        totalSales: "$sales.totalSales"
                    }
                }
            }
        }
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": null,
        "topTwoStores": [
            {
                "storeId": "ffe155dd-caa2-4ac1-8ec9-0342241a84a3",
                "storeName": "Lakeshore Retail | Electronics Stop - Vicentastad",
                "totalSales": 399426
            },
            {
                "storeId": "cba62761-10f8-4379-9eea-a9006c667927",
                "storeName": "Fabrikam, Inc. | Electronics Nook - East Verlashire",
                "totalSales": 374845
            }
        ]
    }
]
```

<span id="example-2-use-first-n-operator-as-accumulator-to-find-first-two-categories-per-store"></span>

### 示例 2：将 $firstN 运算符作为累加器使用，按每个商店的总销售额查找前两个类别 {#example-2-use-firstn-operator-as-accumulator-to-find-first-two-categories-per-store}

要检索每个商店内总销售额最高的前两个类别，运行查询以在每个商店范围内按 sales.totalSales 字段降序排序所有文档，并为每个商店从排序后结果集中返回前两个类别。

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $match: {
      "sales.salesByCategory.totalSales": { $exists: true }
    }
  },
  {
    $sort: {
      "_id": 1,
      "sales.salesByCategory.totalSales": -1
    }
  },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      categoryCount: { $sum: 1 },
      firstTwoCategories: {
        $push: {
          categoryName: "$sales.salesByCategory.categoryName",
          totalSales: "$sales.salesByCategory.totalSales"
        }
      }
    }
  },
  {
    $project: {
      storeName: 1,
      categoryCount: 1,
      firstTwoCategories: { $slice: ["$firstTwoCategories", 2] }
    }
  },
  {
    $match: {
      categoryCount: { $gte: 2 }
    }
  },
  { $limit: 2 }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "2e07b49d-1730-491b-b847-44b6a34812c1",
        "storeName": "VanArsdel, Ltd. | Electronics Market – North Bransonborough",
        "categoryCount": 3,
        "firstTwoCategories": [
            {
                "categoryName": "iPads",
                "totalSales": 37113
            },
            {
                "categoryName": "Laptops",
                "totalSales": 9175
            }
        ]
    },
    {
        "_id": "1bec7539-dc75-4f7e-b4e8-afdf8ff2f234",
        "storeName": "Adatum Corporation | Health Food Market – East Karina",
        "categoryCount": 2,
        "firstTwoCategories": [
            {
                "categoryName": "Protein Bars",
                "totalSales": 49900
            },
            {
                "categoryName": "Superfoods",
                "totalSales": 39683
            }
        ]
    }
]
```

<span id="example-3-use-first-n-operator-as-array-expression-to-find-first-three-sales-categories"></span>

### 示例 3：将 `firstN` 运算符作为数组表达式使用，查找前三个销售类别 {#example-3-use-firstn-operator-as-array-expression-to-find-first-three-sales-categories}

该示例演示了运算符的用法，用于分析前三个销售类别。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      firstThreeCategories: {
        $firstN: {
          input: "$sales.salesByCategory",
          n: 3
        }
      }
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
      "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
      "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
      "totalSales": 165000,
      "firstThreeCategories": [
          {
              "categoryName": "Sound Bars",
              "totalSales": 2120
          },
          null,
          {
              "categoryName": "Game Controllers",
              "totalSales": 43522
          }
      ]
  }
]
```
