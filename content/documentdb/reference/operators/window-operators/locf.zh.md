---
title: $locf
description: $locf 运算符在窗口查询的分区内，将最后观测到的非 null 值向后续文档传播。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$locf.md
weight: 90
translation_source_sha256: c6eb29bb4c815545f839e786c86bd56205e82035c39f2f689cca680531297907
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 说明写的是 `$lecf`，而标题和代码使用 `$locf`。前者是上游原文中的拼写不一致。

`$locf` 运算符在窗口查询的分区内，将最后观测到的非 null 值向后续文档传播。$locf 运算符尤其适合填充时间序列数据或其他存在缺口的数据集中的缺失数据点。

## 语法 {#syntax}

```javascript
{
  $locf: {
    input: <expression>,
    sortBy: <document>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`input`** | 求值结果指向要传播其值的字段的表达式。 |
| **`sortBy`** | 指定分区排序顺序的文档。 |
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

### 示例 1：使用 `$locf` 填充缺失的时间序列数据 {#example-1-using-locf-to-fill-missing-time-series-data}

要在 "First Up Consultants" 公司旗下各商店间传播 lastUpdated 字段最近的非 null 值，先执行查询，对该公司旗下商店分区。然后使用 $lecf 运算符，将该字段最后的非 null 值传播到分区内的所有商店。

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["First Up Consultants"]
        }
    }
}, {
    "$setWindowFields": {
        "partitionBy": "$name",
        "sortBy": {
            "sales.revenue": 1
        },
        "output": {
            "lastUpdatedDate": {
                "$locf": {
                    "lastUpdated": 1
                }
            }
        }
    }
}, {
    "$project": {
        "company": 1,
        "name": 1,
        "lastObservedDiscount": 1
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "0f4c48fe-c43b-4083-a856-afe6dd902077",
        "name": "First Up Consultants | Appliance Bargains - Feilmouth",
        "company": "First Up Consultants"
    },
    {
        "_id": "c4883253-7ccd-4054-a7e0-8aeb202307b5",
        "name": "First Up Consultants | Appliance Bargains - New Kari",
        "company": "First Up Consultants"
    },
    {
        "_id": "a159ff5c-6ec5-4ca8-9672-e8903a54dd90",
        "name": "First Up Consultants | Appliance Bargains - Schadenstad",
        "company": "First Up Consultants"
    }
]
```
