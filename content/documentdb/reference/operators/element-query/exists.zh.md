---
title: $exists
description: $exists 运算符检索文档结构中包含指定字段的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/element-query/$exists.md
weight: 10
translation_source_sha256: 5896abe26b868e5784bc547651c7cf853105eb013d08f851839bbfc25967af3a
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 简介中的“fall”与参数表中的 false 不一致。这是来源中的笔误，并非另一种布尔值。

$exists 运算符检索包含指定字段的文档。对于包含指定字段的文档，$exists 运算符返回 true，即使该字段的值为 null 也是如此。对于文档结构中不包含指定字段的文档，$exists 运算符返回 fall。

## 语法 {#syntax}

```javascript
{
  <field>: { $exists: <true or false> }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要检查是否存在的字段。 |
| **`true or false`** | `true` 对应包含该字段的文档（包括字段值为 null 的文档），`false` 对应不包含该字段的文档。 |
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

### 示例 1：查找有促销活动的商店 {#example-1-find-stores-with-promotion-events}

要查找任意两家有促销活动的商店，可对 promotionEvents 数组使用 $exists 运算符执行查询。然后仅投影 ID 和 promotionEvents 字段，并将结果限制为结果集中的两个文档。

```javascript
db.stores.find({
    "promotionEvents": {
        $exists: true
    }
}, {
    "_id": 1,
    "promotionEvents": {
        $slice: 1
    }
}).limit(2)
```

此查询返回以下结果：

```json
  [
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "location": {
            "lat": -74.0427,
            "lon": 160.8154
        },
        "staff": {
            "employeeCount": {
                "fullTime": 9,
                "partTime": 18
            }
        },
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Stockings",
                    "totalSales": 25731
                }
            ],
            "revenue": 25731
        },
        "promotionEvents": [
            {
                "eventName": "Mega Savings Extravaganza",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2023,
                        "Month": 6,
                        "Day": 29
                    },
                    "endDate": {
                        "Year": 2023,
                        "Month": 7,
                        "Day": 7
                    }
                },
                "discounts": [
                    {
                        "categoryName": "Stockings",
                        "discountPercentage": 16
                    },
                    {
                        "categoryName": "Tree Ornaments",
                        "discountPercentage": 8
                    }
                ]
            }
        ],
        "company": "Lakeshore Retail",
        "city": "Marvinfort",
        "storeOpeningDate": "2024-10-01T18:24:02.586Z",
        "lastUpdated": "2024-10-02T18:24:02.000Z"
    },
    {
        "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
        "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
        "location": {
            "lat": 61.3945,
            "lon": -3.6196
        },
        "staff": {
            "employeeCount": {
                "fullTime": 7,
                "partTime": 6
            }
        },
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Lamps",
                    "totalSales": 19880
                },
                {
                    "categoryName": "Rugs",
                    "totalSales": 20055
                }
            ],
            "revenue": 39935
        },
        "promotionEvents": [
            {
                "eventName": "Unbeatable Markdown Mania",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 3,
                        "Day": 25
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 4,
                        "Day": 1
                    }
                },
                "discounts": [
                    {
                        "categoryName": "Vases",
                        "discountPercentage": 8
                    },
                    {
                        "categoryName": "Lamps",
                        "discountPercentage": 5
                    }
                ]
            }
        ],
        "company": "Lakeshore Retail",
        "city": "Franciscoton",
        "lastUpdated": "2024-12-02T12:01:46.000Z",
        "storeOpeningDate": "2024-09-03T07:21:46.045Z"
    }
]
```

### 示例 2：确认嵌套字段是否存在 {#example-2-confirm-the-presence-of-a-nested-field}

要检索任意两家有全职员工的商店，可对嵌套字段 staff.employeeCount.fullTime 使用 $exists 运算符执行查询。然后仅投影 name 和 ID 字段，并将结果限制为结果集中的两个文档。

```javascript
db.stores.find({
    "staff.employeeCount.fullTime": {
        $exists: true
    }
}, {
    "_id": 1,
    "staff.employeeCount": 1
}).limit(2)
```

此查询返回以下结果：

```json
[
  {
      "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
      "staff": {
          "employeeCount": {
              "fullTime": 9,
              "partTime": 18
          }
      }
  },
  {
      "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
      "staff": {
          "employeeCount": {
              "fullTime": 7,
              "partTime": 6
          }
      }
  }
]
```
