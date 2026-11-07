---
title: $last
description: $last 运算符返回按一个或多个字段排序后的结果集中的最后一个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/accumulators/$last.md
weight: 70
translation_source_sha256: cc410ac554e3d44e4cfb103eae610c6bd0b334818f8b2ffdce2790d4324c4d6b
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$last` 运算符根据查询中指定的一个或多个字段对文档进行排序，并返回匹配筛选条件的最后一个文档。

## 语法 {#syntax}

```javascript
{
  "$last": <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要计算并从结果集中返回最后一个文档的表达式 |
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

### 示例 1：获取公司内最后更新的门店 {#example-1-get-the-last-updated-store-within-a-company}

要检索 First Up Consultants 公司内最近更新的门店，运行查询以获取 First Up Consultants 公司内的所有门店，按 lastUpdated 字段升序对文档排序，并返回排序结果中的最后一个文档。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $sort: {
        lastUpdated: 1
    }
}, {
    $group: {
        _id: "$company",
        lastUpdated: {
            $last: "$lastUpdated"
        }
    }
}])
```

此查询返回以下结果：

```json
[
  {
      "_id": "First Up Consultants",
      "lastUpdated": "ISODate('2024-12-31T13:01:19.097Z')"
  }
]
```

<span id="example-2-using-the-window-operator"></span>

### 示例 2 - 使用窗口运算符 {#example-2---using-the-window-operator}

要检索每个公司内最近更新的门店，请运行查询以按 company 字段对结果进行分区，并在每个分区中按 lastUpdated 字段升序对文档排序，然后返回每个分区的排序结果。

```javascript
db.stores.aggregate([{
    $setWindowFields: {
        partitionBy: "$company",
        sortBy: {
            lastUpdated: 1
        },
        output: {
            lastUpdatedDateForStore: {
                $last: "$lastUpdated",
                window: {
                    documents: ["current", "unbounded"]
                }
            }
        }
    }
}])
```

此查询返回的第一个结果是：

```json
[
  {
      "_id": "First Up Consultants",
      "lastUpdated": "ISODate('2024-12-31T13:01:19.097Z')"
  }
]
```
