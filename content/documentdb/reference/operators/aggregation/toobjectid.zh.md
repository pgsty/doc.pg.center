---
title: $toObjectId
description: $toObjectId 运算符将表达式转换为 ObjectId
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$toobjectid.md
weight: 400
translation_source_sha256: 281334288fd519d24ec24e228a94db50ba02c7d0259c2a84b3fa6bf61b277e71
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 简介将运算符写为 `$toObject`，而页面标题和示例使用 `$toObjectId`。前者是上游原文中的拼写不一致。

`$toObject` 运算符将指定的值转换为 ObjectId。

## 语法 {#syntax}

```javascript
{
    $toObject: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 要转换为 ObjectId 的指定字符串值 |
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

<span id="example-1-convert-the-first-24-alphanumeric-characters-in-the-id-field-into-an-object-id-value"></span>

### 示例 1：将 _id 字段中的前 24 个字母数字字符转换为 ObjectId 值 {#example-1-convert-the-first-24-alphanumeric-characters-in-the-_id-field-into-an-objectid-value}

为移除 _id 字段中所有 "-" 字符，并将前 24 个字符转换为 ObjectId，需对修改后的 _id 字段的子字符串使用 $toObjectId 运算符执行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        idAsObjectId: {
            $toObjectId: {
                $substr: [{
                    $replaceAll: {
                        input: "$_id",
                        find: "-",
                        replacement: ""
                    }
                }, 0, 24]
            }
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "idAsObjectId": "ObjectId('b010763193704acdaafa8ac3')"
    }
]
```
