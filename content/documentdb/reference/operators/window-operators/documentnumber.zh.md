---
title: $documentNumber
description: $documentNumber 运算符根据指定排序顺序，为分区内的每个文档分配并返回位置编号
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$documentnumber.md
weight: 50
translation_source_sha256: bd408e4f66440e1b5bfd98aec391d021f470d85aa291dbae0a2183b22d9a0008
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$documentNumber` 运算符在分区内按一个或多个字段对文档排序，并为结果集中的每个文档分配文档编号。

## 语法 {#syntax}

```javascript
{
    $documentNumber: {}
}
```

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

<span id="example-1-retrieve-a-document-number-by-total-sales"></span>

### 示例 1 - 按总销售额获取文档编号 {#example-1---retrieve-a-document-number-by-total-sales}

要获取 First Up Consultants 公司旗下每家商店的文档编号（位置排名），先按公司名称执行查询筛选，再按总销售额升序排列结果，并为排序后结果集中的每个文档分配文档编号。

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
            "documentNumber": {
                "$documentNumber": {}
            }
        }
    }
}, {
    "$project": {
        "company": 1,
        "documentNumber": 1
    }
}])
```

此查询返回的前 5 个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "company": "First Up Consultants",
        "documentNumber": 1
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "company": "First Up Consultants",
        "documentNumber": 2
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "company": "First Up Consultants",
        "documentNumber": 3
    },
    {
        "_id": "bfb213fa-8db8-419f-8e5b-e7096120bad2",
        "company": "First Up Consultants",
        "documentNumber": 4
    },
    {
        "_id": "14ab145b-0819-4d22-9e02-9ae0725fcda9",
        "company": "First Up Consultants",
        "documentNumber": 5
    }
]
```
