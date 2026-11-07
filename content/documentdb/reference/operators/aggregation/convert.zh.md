---
title: $convert
description: $convert 运算符将表达式转换为指定类型
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$convert.md
weight: 60
translation_source_sha256: a87aa2320171baf02dae1def74d06cc0c67ffd91b83085bb0c37fe6a08e9a18e
translation_review: AI-assisted bilingual review; 2026-11-07
---

$convert 运算符将表达式转换为指定类型的值。

## 语法 {#syntax}

```javascript
{
    $convert: {
        input: < expression > ,
        to: < type > ,
        format: < binData format > ,
        onError: < value to return on error > ,
        onNull: < value to return on null >
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`input`** | 要转换为指定类型的输入值 |
| **`to`** | 输入值要转换成的目标类型 |
| **`format`** | （可选）将值转换为 binData 或从 binData 转换时，输入或输出所用的 binData 格式 |
| **`onError`** | （可选）将输入值转换为指定类型失败时要返回的值 |
| **`onNull`** | （可选）要转换为指定类型的输入值为 null 或缺失时要返回的值 |
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

### 示例 1：将整数转换为字符串 {#example-1-convert-an-int-value-into-a-string}

要将 fullTime 字段从整数转换为字符串，请使用 $convert 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsString: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "string"
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
        "fulltimeStaff": 3,
        "fulltimeStaffAsString": "3"
    }
]
```

### 示例 2：将整数转换为布尔值 {#example-2-convert-an-int-value-into-a-boolean-value}

要将 fullTime 字段从整数转换为布尔值，请使用 $convert 运算符运行查询以完成转换。fullTime 字段的任何正值都将被转换为 true。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsBool: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "bool"
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
        "fulltimeStaff": 3,
        "fulltimeStaffAsBool": true
    }
]
```

### 示例 3：将整数转换为十进制值 {#example-3-convert-an-int-value-into-a-decimal-value}

要将 fullTime staff 字段从整数转换为十进制值，请使用 $convert 运算符运行查询以完成转换。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsDecimal: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "decimal"
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
        "fulltimeStaff": 3,
        "fulltimeStaffAsDecimal": "Decimal128('3')"
    }
]
```
