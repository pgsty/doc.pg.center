---
title: $slice
description: $slice 运算符从数组中的任意元素开始返回数组的子集。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-expression/$slice.md
weight: 110
translation_source_sha256: 619f15b31291ce90f6a1613aa3af3edc637cf5dea4c5c03ea71bd0e72e154882
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 仅保留前 N 项或后 N 项，并不能确定哪些条目最新。原文关于保留最新条目的说法，还取决于数组顺序及切片方向。

`$slice` 运算符用于返回数组的子集。它可将数组中的元素数量限制为指定数量，也可从数组中的指定位置开始返回元素。在处理大型数组时，如果只需使用或显示部分数据，可以使用此运算符。

## 语法 {#syntax}

`$slice` 运算符的语法如下所示。

- 从数组的起始位置或末尾位置返回元素

```javascript
{
  $slice: [ <array>, <n> ]
}
```

- 从数组中指定位置返回元素

```javascript
{
  $slice: [ <array>, <position>, <n> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`array`** | 任意有效的数组表达式。 |
| **`position`** | 任意有效的整数表达式。 |
| **`n`** | 任意有效的整数表达式。 |
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

### 示例 1：返回数组中的一组元素 {#example-1-return-the-set-of-elements-from-the-array}

此查询从 `stores` 集合中 `_id: 988d2dd1-2faa-4072-b420-b91b95cbfd60` 的 `sales.salesByCategory` 数组中检索前三个元素。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "988d2dd1-2faa-4072-b420-b91b95cbfd60"
    }
}, {
    $project: {
        salesByCategory: {
            $slice: ["$sales.salesByCategory", 3]
        }
    }
}])
```

此查询返回以下结果。

```json
[
    {
        "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
        "salesByCategory": [
            {
                "categoryName": "Towel Racks",
                "totalSales": 13237
            },
            {
                "categoryName": "Washcloths",
                "totalSales": 44315
            },
            {
                "categoryName": "Face Towels",
                "totalSales": 42095
            }
        ]
    }
]
```

### 示例 2：结合 $push 使用切片 {#example-2-slice-with-push}

此查询使用 `$push` 配合 `$each` 向 `promotionEvents` 数组中添加新元素，并使用 `$slice` 仅保留前 N 个元素（正数切片）或最后 N 个元素（负数切片）。这确保了更新后数组仍保留最新的条目。

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $push: {
        promotionEvents: {
            $each: [{
                    eventName: "Black Friday Event",
                    promotionalDates: {
                        startDate: {
                            Year: 2024,
                            Month: 8,
                            Day: 1
                        },
                        endDate: {
                            Year: 2024,
                            Month: 8,
                            Day: 7
                        }
                    },
                    discounts: [{
                        categoryName: 'DJ Speakers',
                        discountPercentage: 25
                    }]
                },
                {
                    eventName: "Mega Discount Days",
                    promotionalDates: {
                        startDate: {
                            Year: 2024,
                            Month: 5,
                            Day: 11
                        },
                        endDate: {
                            Year: 2024,
                            Month: 5,
                            Day: 18
                        }
                    },
                    discounts: [{
                        categoryName: "DJ Lights",
                        discountPercentage: 20
                    }]
                }
            ],
            $slice: -3
        }
    }
})
```

此查询返回以下结果。

```json
[
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
                },
                {
                    "categoryName": "DJ Cables",
                    "totalSales": 1000
                }
            ],
            "fullSales": 3700
        },
        "promotionEvents": [
            {
                "eventName": "Cyber Monday Event",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 8,
                        "Day": 1
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 8,
                        "Day": 7
                    }
                },
                "discounts": [
                    {
                        "categoryName": "DJ Speakers",
                        "discountPercentage": 25
                    }
                ]
            },
            {
                "eventName": "Black Friday Event",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 8,
                        "Day": 1
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 8,
                        "Day": 7
                    }
                },
                "discounts": [
                    {
                        "categoryName": "DJ Speakers",
                        "discountPercentage": 25
                    }
                ]
            },
            {
                "eventName": "Mega Discount Days",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 5,
                        "Day": 11
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 5,
                        "Day": 18
                    }
                },
                "discounts": [
                    {
                        "categoryName": "DJ Lights",
                        "discountPercentage": 20
                    }
                ]
            }
        ],
        "tag": [
            "#ShopLocal",
            "#NewArrival",
            "#FashionStore",
            "#SeasonalSale",
            "#FreeShipping",
            "#MembershipDeals"
        ]
    }
]
```

### 示例 3：获取数组中第一个匹配的元素 {#example-3-fetch-the-first-matching-element-from-an-array}

此查询从 "sales.salesByCategory" 数组中检索第一个文档。

```javascript
db.stores.find({
        name: "Lakeshore Retail"
    }, {
        _id: 1,
        name: 1,
        "sales.salesByCategory": {
            $slice: 1
        }
    } // restricts the fields to be returned
)
```

此查询返回以下结果。

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Towel Racks",
          "totalSales": 13237
        }
      ]
    }
  }
]
```

### 示例 4：获取数组中的最后一个元素 {#example-4-fetch-the-last-element-from-an-array}

此查询从 "sales.salesByCategory" 数组中检索最后一个文档。

```javascript
db.stores.find({
    name: "Lakeshore Retail"
}, {
    _id: 1,
    name: 1,
    "sales.salesByCategory": {
        $slice: -1
    }
})
```

此查询返回以下结果。

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Pillow Cases",
          "totalSales": 38833
        }
      ]
    }
  }
]
```

### 示例 5：获取数组中指定范围内的元素 {#example-5-retrieve-a-range-of-elements-from-an-array}

此查询从 "sales.salesByCategory" 数组中检索一个子范围。

```javascript
db.stores.find({
    name: "Lakeshore Retail"
}, {
    _id: 1,
    name: 1,
    "sales.salesByCategory": {
        $slice: [3, 2]
    }
})
```

此查询返回以下结果。

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Toothbrush Holders",
          "totalSales": 47912
        },
        {
          "categoryName": "Hybrid Mattresses",
          "totalSales": 48660
        }
      ]
    }
  }
]
```
