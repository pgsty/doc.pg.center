---
title: $minN
description: $minN 运算符根据指定的筛选条件检索最低 N 个值
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$minn.md
weight: 130
translation_source_sha256: b0ecac2c30b86181067c01b0643f9a065a541fa99f140972fbad2256318f5efe
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$minN` 运算符用于根据指定的筛选条件检索字段的最低 N 个值。

## 语法 {#syntax}

```javascript
$minN: {
    input: < field or expression > ,
    n: < number of values to retrieve >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 指定要评估最小值的字段或表达式。 |
| **`n`** | 指定要检索的最小值数量。必须为正整数。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### 示例 1：检索最低两个销售类别 {#example-1-retrieve-bottom-two-sales-categories}

此查询检索每个门店中销售量最低的两个销售类别。对嵌套的 salesCategory 字段使用 $minN 运算符执行查询。

```javascript
db.stores.aggregate([{
        $project: {
            bottomSalesCategories: {
                $minN: {
                    input: "$sales.salesByCategory",
                    n: 2
                }
            }
        }
    },
    {
        $limit: 4
    }
])
```

此查询返回以下结果：

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "bottomSalesCategories": [
            {
                "categoryName": "Stockings",
                "totalSales": 25731
            }
        ]
    },
    {
        "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
        "bottomSalesCategories": [
            {
                "categoryName": "Lamps",
                "totalSales": 19880
            },
            {
                "categoryName": "Rugs",
                "totalSales": 20055
            }
        ]
    },
    {
        "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        "bottomSalesCategories": [
            {
                "categoryName": "Markers",
                "totalSales": 3927
            }
        ]
    },
    {
        "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
        "bottomSalesCategories": [
            {
                "categoryName": "Storage Boxes",
                "totalSales": 2236
            }
        ]
    }
]
```

<span id="example-2-using-min-n-with-set-window-fields"></span>

### 示例 2 - 将 $minN 与 $setWindowFields 配合使用 {#example-2---using-minn-with-setwindowfields}

要获取 "First Up Consultants" 公司所有门店中销售量最低的两个销售类别列表，首先按公司对门店进行分区。然后，使用 $minN 运算符在每个分区中确定销售量最低的两个类别。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $setWindowFields: {
        partitionBy: "$company",
        sortBy: {
            "sales.totalSales": -1
        },
        output: {
            minTwoBySales: {
                $minN: {
                    input: "$sales.totalSales",
                    n: 2
                }
            }
        }
    }
}, {
    $project: {
        company: 1,
        name: 1,
        minCategoriesBySales: 1
    }
}])
```

此查询返回的第一个结果是：

```json
[
    {
        "_id": "a0386810-b6f8-4b05-9d60-e536fb2b0026",
        "name": "First Up Consultants | Electronics Stop - South Thelma",
        "company": "First Up Consultants",
        "minCategoriesBySales": [
            [
                {
                    "categoryName": "3D Printers",
                    "totalSales": 20882
                },
                {
                    "categoryName": "Phone Mounts",
                    "totalSales": 13624
                },
                {
                    "categoryName": "Prepaid Phones",
                    "totalSales": 7182
                },
                {
                    "categoryName": "MacBooks",
                    "totalSales": 10541
                },
                {
                    "categoryName": "Chargers",
                    "totalSales": 37542
                },
                {
                    "categoryName": "Student Laptops",
                    "totalSales": 43977
                },
                {
                    "categoryName": "Screen Protectors",
                    "totalSales": 14648
                },
                {
                    "categoryName": "Photo Printers",
                    "totalSales": 40064
                },
                {
                    "categoryName": "Printer Ink",
                    "totalSales": 30784
                },
                {
                    "categoryName": "Smartphone Cases",
                    "totalSales": 30468
                },
                {
                    "categoryName": "Printer Drums",
                    "totalSales": 34980
                },
                {
                    "categoryName": "Desktops",
                    "totalSales": 3890
                }
            ],
            [
                {
                    "categoryName": "4K Camcorders",
                    "totalSales": 10466
                },
                {
                    "categoryName": "Tripods",
                    "totalSales": 30942
                },
                {
                    "categoryName": "Camcorder Accessories",
                    "totalSales": 25601
                }
            ]
        ]
    }
]
```

<span id="example-3-using-min-n-operator-as-array-expression-to-get-lowest-two-sales-values"></span>

### 示例 3 - 将 $minN 运算符作为数组表达式以获取最低两个销售值 {#example-3---using-minn-operator-as-array-expression-to-get-lowest-two-sales-values}

此查询提取特定门店文档中最低的两个销售值。

```javascript
db.stores.aggregate([
  { $match: {_id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lowestTwoSales: {
        $minN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
    {
      "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
      "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
      "lowestTwoSales": [28946, 3000]
    }
]
```
