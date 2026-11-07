---
title: $unwind
description: 聚合框架中的 $unwind 流水线阶段用于从输入文档中拆解数组字段，为数组中的每个元素输出一个文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$unwind.md
weight: 440
translation_source_sha256: 66e387fa912fcb40eedf314f22220df6a10156d9bddfa1f3d9cc07119b06abd3
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合框架中的 $unwind 流水线阶段用于从输入文档中拆解数组字段，为数组中的每个元素输出一个文档。每个输出文档都是原始文档的副本，但数组字段的值被替换为单个元素。此操作特别适用于规范化存储在数组中的数据，以及对数组中的每个元素分别执行操作。

## 语法 {#syntax}

```javascript
{
  $unwind: {
    path: <field path>,
    includeArrayIndex: <string>, // Optional
    preserveNullAndEmptyArrays: <boolean> // Optional
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`path`** | 数组字段的字段路径。此参数为必填项。 |
| **`includeArrayIndex`** | 可选。用于存储拆解后元素在数组中索引的新字段名称。 |
| **`preserveNullAndEmptyArrays`** | 可选。如果为 true，当路径为 null、缺失或空数组时，`$unwind` 会原样输出文档。 |
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

### 示例 1：按类别拆解销售数据 {#example-1-unwind-sales-by-category}

拆解 store 文档中的 salesByCategory 数组：

```javascript
db.stores.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "totalSales": 15000,
        "salesByCategory": {
          "category": "Electronics",
          "totalSales": 5000
        }
      }
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "totalSales": 15000,
        "salesByCategory": {
          "category": "Clothing",
          "totalSales": 10000
        }
      }
    }
  }
]
```

### 示例 2：拆解促销活动并包含数组索引 {#example-2-unwind-promotion-events-with-array-index}

拆解 promotionEvents 数组，并在输出中包含数组索引：

```javascript
db.stores.aggregate([
  {
    $unwind: {
      path: "$promotionEvents",
      includeArrayIndex: "eventIndex"
    }
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Summer Sale",
        "eventDate": ISODate("2024-08-01T00:00:00Z")
      },
      "eventIndex": 0
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Black Friday",
        "eventDate": ISODate("2024-11-25T00:00:00Z")
      },
      "eventIndex": 1
    }
  }
]
```

### 示例 3：在促销活动中拆解折扣数据 {#example-3-unwind-discounts-within-pomotion-events}

拆解每个促销活动中 discounts 数组内的元素，并保留没有折扣的文档：

```javascript
db.stores.aggregate([
  {
    $unwind: {
      path: "$promotionEvents.discounts",
      preserveNullAndEmptyArrays: true
    }
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Summer Sale",
        "discounts": {
          "discountType": "Percentage",
          "discountAmount": 20
        }
      }
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Black Friday"
      }
    }
  }
]
```
