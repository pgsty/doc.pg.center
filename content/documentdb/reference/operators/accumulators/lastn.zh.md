---
title: $lastN
description: $lastN 累加器运算符返回文档组中的最后 N 个值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$lastn.md
weight: 80
translation_source_sha256: b3b3e004e62cf34303cfae13ece3b4a4bd86226f2da764b8b584c4ff8d51b6b5
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$lastN` 累加器运算符返回指定表达式在文档组中的最后 N 个值。当需要从已排序的集合中检索多个最终值，而不仅仅是单个最后值时，该运算符非常有用。

## 语法 {#syntax}

```javascript
{
    $group: {
        _id: < expression > ,
        < field >: {
            $lastN: {
                 n: < number >,
                 input: < expression >               
            }
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`n`** | 要返回的值的数量。必须为正整数。 |
| **`input`** | 指定要返回最后 N 个出现值的字段或值的表达式。 |
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

<span id="example-1-use-last-n-as-accumulator-to-find-last-two-promotion-events-by-store"></span>

### 示例 1：将 $lastN 用作累加器，查找每家商店的最后两次促销活动 {#example-1-use-lastn-as-accumulator-to-find-last-two-promotion-events-by-store}

要检索每个商店的最后两次促销活动，请运行查询，按促销活动开始日期升序排序，按商店分组，并返回每个商店内的最后两次活动。

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $sort: {
            "promotionEvents.promotionalDates.startDate.Year": 1,
            "promotionEvents.promotionalDates.startDate.Month": 1,
            "promotionEvents.promotionalDates.startDate.Day": 1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $last: "$name"
            },
            lastTwoPromotions: {
                $lastN: {
                    input: "$promotionEvents.eventName",
                    n: 2
                }
            },
            lastTwoPromotionDates: {
                $lastN: {
                    input: "$promotionEvents.promotionalDates.startDate",
                    n: 2
                }
            }
        }
    }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "e28fff9b-a8fb-4ac9-bb37-dea60d2a7d32",
        "storeName": "Lakeshore Retail | Outdoor Furniture Collection - Erdmanside",
        "lastTwoPromotions": [
            "Big Bargain Bash",
            "Spectacular Savings Showcase"
        ],
        "lastTwoPromotionDates": [
            {
                "Year": 2024,
                "Month": 9,
                "Day": 21
            },
            {
                "Year": 2024,
                "Month": 6,
                "Day": 23
            }
        ]
    },
    {
        "_id": "1bec7539-dc75-4f7e-b4e8-afdf8ff2f234",
        "storeName": "Adatum Corporation | Health Food Market - East Karina",
        "lastTwoPromotions": [
            "Price Slash Spectacular",
            "Spectacular Savings Showcase"
        ],
        "lastTwoPromotionDates": [
            {
                "Year": 2024,
                "Month": 9,
                "Day": 21
            },
            {
                "Year": 2024,
                "Month": 6,
                "Day": 23
            }
        ]
    }
]
```

<span id="example-2-use-last-n-as-accumulator-to-find-the-three-highest-selling-categories-of-sales"></span>

### 示例 2：将 $lastN 用作累加器，查找销量最高的三个销售类别 {#example-2-use-lastn-as-accumulator-to-find-the-three-highest-selling-categories-of-sales}

要检索每个商店销售量最高的三个销售类别，请运行查询，按销售量升序排序销售类别，按商店分组，并返回每个商店的最后三个类别。

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $sort: {
            "sales.salesByCategory.totalSales": 1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $last: "$name"
            },
            top3Categories: {
                $lastN: {
                    input: "$sales.salesByCategory.categoryName",
                    n: 3
                }
            },
            top3SalesAmounts: {
                $lastN: {
                    input: "$sales.salesByCategory.totalSales",
                    n: 3
                }
            }
        }
    }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "22e6367e-8341-415f-9795-118d2b522abf",
        "storeName": "Adatum Corporation | Outdoor Furniture Mart - Port Simone",
        "top3Categories": [
            "Outdoor Benches"
        ],
        "top3SalesAmounts": [
            4976
        ]
    },
    {
        "_id": "a00a3ccd-49a2-4e43-b0d9-e56b96113ed0",
        "storeName": "Wide World Importers | Smart Home Deals - Marcuschester",
        "top3Categories": [
            "Smart Thermostats",
            "Smart Plugs"
        ],
        "top3SalesAmounts": [
            38696,
            633
        ]
    }
]
```

<span id="example-3-use-last-n-operator-as-array-expression-to-get-last-two-promotion-events"></span>

### 示例 3：将 $lastN 运算符用作数组表达式，获取最后两次促销活动 {#example-3-use-lastn-operator-as-array-expression-to-get-last-two-promotion-events}

该示例演示了如何使用该运算符查找来自商店的最后或最近两次促销活动。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lastTwoPromotions: {
        $lastN: {
          input: "$promotionEvents",
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
      "lastTwoPromotions": [
          {
              "eventName": "Grand Deal Days",
              "promotionalDates": {
                  "startDate": {
                      "Year": 2024,
                      "Month": 6,
                      "Day": 23
                  },
                  "endDate": {
                      "Year": 2024,
                      "Month": 6,
                      "Day": 30
                  }
              },
              "discounts": [
                  {
                      "categoryName": "Remote Controls",
                      "discountPercentage": 7
                  },
                  {
                      "categoryName": "Televisions",
                      "discountPercentage": 11
                  },
                  {
                      "categoryName": "Business Projectors",
                      "discountPercentage": 13
                  },
                  {
                      "categoryName": "Laser Projectors",
                      "discountPercentage": 6
                  },
                  {
                      "categoryName": "Projectors",
                      "discountPercentage": 6
                  },
                  {
                      "categoryName": "Projector Screens",
                      "discountPercentage": 24
                  }
              ]
          },
          {
              "eventName": "Major Bargain Bash",
              "promotionalDates": {
                  "startDate": {
                      "Year": 2024,
                      "Month": 9,
                      "Day": 21
                  },
                  "endDate": {
                      "Year": 2024,
                      "Month": 9,
                      "Day": 30
                  }
              },
              "discounts": [
                  {
                      "categoryName": "Sound Bars",
                      "discountPercentage": 9
                  },
                  {
                      "categoryName": "VR Games",
                      "discountPercentage": 7
                  },
                  {
                      "categoryName": "Xbox Games",
                      "discountPercentage": 25
                  },
                  {
                      "categoryName": "Projector Accessories",
                      "discountPercentage": 18
                  },
                  {
                      "categoryName": "Mobile Games",
                      "discountPercentage": 8
                  },
                  {
                      "categoryName": "Projector Cases",
                      "discountPercentage": 22
                  }
              ]
          }
      ]
  }
]
```
