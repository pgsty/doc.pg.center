---
title: $unset
description: 聚合流水线中的 $unset 阶段用于从文档中移除指定字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$unset.md
weight: 430
translation_source_sha256: 8fe8eab746d8c9dfa49c4efda7c626c87f0f5ce9862eec9370b0333f78837fc7
translation_review: AI-assisted bilingual review; 2026-11-07
---

$unset 流水线阶段用于从文档中移除指定字段。当需要出于隐私保护、减少负载大小或仅清理输出结果等原因，排除聚合查询结果中的某些字段时，此操作尤为有用。

## 语法 {#syntax}

```javascript
{
    $unset: "<field1>" | ["<field1>", "<field2>", ...]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field1, field2, ...`** | 要从文档中移除的字段名称。 |
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

### 示例 1：移除单个字段 {#example-1-remove-a-single-field}

从文档中移除 location 字段。

```javascript
db.stores.aggregate([
  {
    $unset: "store.location"
  }
])
```

此查询返回的第一个结果是：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "totalSales": 15000,
        "salesByCategory": [
          {
            "category": "Electronics",
            "totalSales": 5000
          },
          {
            "category": "Clothing",
            "totalSales": 10000
          }
        ]
      }
    }
  }
]
```

### 示例 2：移除多个字段 {#example-2-remove-multiple-fields}

从文档中移除 location 和 sales.totalSales 字段。

```javascript
db.stores.aggregate([
  {
    $unset: ["store.location", "store.sales.totalSales"]
  }
])
```

此查询返回的第一个结果是：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "salesByCategory": [
          {
            "category": "Electronics",
            "totalSales": 5000
          },
          {
            "category": "Clothing",
            "totalSales": 10000
          }
        ]
      }
    }
  }
]
```

### 示例 3：移除嵌套字段 {#example-3-remove-nested-fields}

从文档中移除 staff.totalStaff.fullTime 和 promotionEvents.discounts 字段。

```javascript
db.stores.aggregate([
  {
    $unset: ["store.staff.totalStaff.fullTime", "store.promotionEvents.discounts"]
  }
])
```

此查询返回的第一个结果是：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "staff": {
        "totalStaff": {
          "partTime": 8
        }
      },
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    }
  }
]
```
