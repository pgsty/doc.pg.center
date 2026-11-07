---
title: $rank
description: $rank 运算符根据指定排序顺序，为分区内的文档排名。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$rank.md
weight: 100
translation_source_sha256: 347fb4b73060d80ddd62954da96df4f4989b2f9aba084cf8f3c8ca6a6158430a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$rank` 运算符为数据集分区内的每个文档分配排名，排名由指定排序顺序决定。

## 语法 {#syntax}

```javascript
{
    $setWindowFields: {
        partitionBy: < expression > ,
        sortBy: {
            < field >: < order >
        },
        output: {
            < outputField >: {
                $rank: {}
            }
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`partitionBy`** | 指定用于将文档划分为分区的表达式。如果省略，则将所有文档视为同一个分区。 |
| **`sortBy`** | 定义排名所用的排序顺序。使用 `$rank` 时必须指定。 |
| **`output`** | 包含用于存储排名值的字段。 |
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

### 示例 1：按销售额为商店排名 {#example-1-ranking-stores-by-sales-volume}

要按销售额为 "First Up Consultants" 公司旗下所有商店排名，先执行查询，对该公司旗下商店分区。然后按销售额升序排列结果中的商店，再使用 $rank 运算符，为结果集中已排序的文档排名。

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["First Up Consultants"]
        }
    }
}, {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "sales.totalSales": -1
        },
        "output": {
            "rankBySales": {
                "$rank": {}
            }
        }
    }
}, {
    "$project": {
        "company": 1,
        "name": 1,
        "rankBySales": 1
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "a0386810-b6f8-4b05-9d60-e536fb2b0026",
        "name": "First Up Consultants | Electronics Stop - South Thelma",
        "company": "First Up Consultants",
        "rankBySales": 1
    },
    {
        "_id": "ad8af64a-d5bb-4162-9bb6-e5104126566d",
        "name": "First Up Consultants | Electronics Emporium - South Carmenview",
        "company": "First Up Consultants",
        "rankBySales": 2
    },
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
        "company": "First Up Consultants",
        "rankBySales": 3
    }
]
```
