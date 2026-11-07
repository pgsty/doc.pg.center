---
title: $linearFill
description: $linearFill 运算符使用线性插值对文档序列中的缺失值进行插值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$linearfill.md
weight: 80
translation_source_sha256: d62364feb8cda03e643c961228b06721b6fd19ef965887901646cf61e540b860
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$linearFill` 运算符对文档序列中的缺失值进行插值。$linearFill 运算符对缺失数据执行线性插值，适用于时间序列数据等存在数值缺口的数据集。

## 语法 {#syntax}

```javascript
{
    $linearFill: {
        input: < expression > ,
        sortBy: {
            < field >: < 1 or - 1 >
        }
    }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`input`** | 要对其缺失值进行插值的字段或表达式。 |
| **`sortBy`** | 指定为插值而对数据排序的字段及排序顺序（1 表示升序，-1 表示降序）。 |
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

### 示例 1：对缺失的销售数据进行插值 {#example-1-interpolating-missing-sales-data}

要对缺失的销售数据进行插值，先执行查询，按名称对数据集中的商店分区。然后使用 $linearFill 运算符，对分区内各商店缺失的销售数据进行插值。

```javascript
db.stores.aggregate([{
        "$match": {
            "company": {
                "$in": ["First Up Consultants"]
            }
        }
    },
    {
        "$setWindowFields": {
            "partitionBy": "$name",
            "sortBy": {
                "storeOpeningDate": 1
            },
            "output": {
                "interpolatedSales": {
                    "$linearFill": "$sales.totalSales"
                }
            }
        }
    }
])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "0f4c48fe-c43b-4083-a856-afe6dd902077",
        "name": "First Up Consultants | Appliance Bargains - Feilmouth",
        "interpolatedSales": 26630
    },
    {
        "_id": "c4883253-7ccd-4054-a7e0-8aeb202307b5",
        "name": "First Up Consultants | Appliance Bargains - New Kari",
        "interpolatedSales": 31568
    },
    {
        "_id": "a159ff5c-6ec5-4ca8-9672-e8903a54dd90",
        "name": "First Up Consultants | Appliance Bargains - Schadenstad",
        "interpolatedSales": 59926
    }
]
```
