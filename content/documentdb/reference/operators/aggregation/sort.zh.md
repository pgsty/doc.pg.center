---
title: $sort
description: 聚合流水线中的 $sort 阶段用于按指定的一个或多个字段对流水线中的文档进行排序。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$sort.md
weight: 320
translation_source_sha256: eb63e3d3ab8298902fe03b930b71d66698dc1566c79303889d2acd06ebb486c7
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 $sort 阶段用于按指定的一个或多个字段对流水线中的文档进行排序。例如，可以按金额排列销售记录，或按日期排列事件。

## 语法 {#syntax}

```javascript
{
    $sort: {
        < field1 >: < sort order > ,
        < field2 >: < sort order >
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 用于排序的字段 |
| **`sort order`** | 排序顺序。1 表示升序，-1 表示降序。 |
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

### 示例 1：按总销售额降序排序 {#example-1-sorting-by-total-sales-in-sescending-order}

按总销售额降序排列销售类别：

```javascript
db.collection.aggregate([
  {
    $unwind: "$store.sales.salesByCategory"
  },
  {
    $sort: { "store.sales.salesByCategory.totalSales": -1 }
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
                "salesByCategory": [
                    {
                        "category": "Electronics",
                        "totalSales": 15000
                    },
                    {
                        "category": "Clothing",
                        "totalSales": 12000
                    },
                    {
                        "category": "Home Goods",
                        "totalSales": 10000
                    }
                ]
            }
        }
    },
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
        "store": {
            "name": "Uptown Store",
            "sales": {
                "salesByCategory": [
                    {
                        "category": "Electronics",
                        "totalSales": 20000
                    },
                    {
                        "category": "Clothing",
                        "totalSales": 18000
                    },
                    {
                        "category": "Home Goods",
                        "totalSales": 15000
                    }
                ]
            }
        }
    }
]
```

### 示例 2：按事件开始日期升序排序 {#example-2-sorting-by-event-start-date-in-ascending-order}

按开始日期升序排列促销活动：

```javascript
db.collection.aggregate([
  {
    $unwind: "$store.promotionEvents"
  },
  {
    $sort: { "store.promotionEvents.promotionalDates.startDate": 1 }
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
            "promotionEvents": [
                {
                    "eventName": "Summer Sale",
                    "promotionalDates": {
                        "startDate": "2024-06-01T00:00:00Z",
                        "endDate": "2024-06-30T23:59:59Z"
                    }
                },
                {
                    "eventName": "Black Friday",
                    "promotionalDates": {
                        "startDate": "2024-11-25T00:00:00Z",
                        "endDate": "2024-11-25T23:59:59Z"
                    }
                },
                {
                    "eventName": "Holiday Deals",
                    "promotionalDates": {
                        "startDate": "2024-12-01T00:00:00Z",
                        "endDate": "2024-12-31T23:59:59Z"
                    }
                }
            ]
        }
    },
    {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
        "store": {
            "name": "Uptown Store",
            "promotionEvents": [
                {
                    "eventName": "Back to School",
                    "promotionalDates": {
                        "startDate": "2024-08-01T00:00:00Z",
                        "endDate": "2024-08-31T23:59:59Z"
                    }
                },
                {
                    "eventName": "Winter Sale",
                    "promotionalDates": {
                        "startDate": "2024-12-01T00:00:00Z",
                        "endDate": "2024-12-31T23:59:59Z"
                    }
                }
            ]
        }
    }
]
```

### 示例 3：对对象数组进行排序 {#example-3-sorting-an-array-of-objects}

该示例基于 `totalSales` 字段按升序对 `salesByCategory` 数组原地排序。

```javascript
db.stores.updateOne({
            _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
        }, {
            $push: {
                "sales.salesByCategory": {
                    $each: [],
                    $sort: {
                        totalSales: 1
                    }
                }
            }
        }
)
```
