---
title: $toBool
description: $toBool 运算符将表达式转换为布尔类型
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$tobool.md
weight: 340
translation_source_sha256: 08606ac0d4ad76b6b959c6cd4519834a2e36adcccc363c6a9df32583eab1718e
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 行为表称任意数值都会转换为 true，但简介明确说明数值零会转换为 false。该表遗漏了零这一例外。

`$toBool` 运算符将表达式转换为布尔值。布尔值会原样返回，无需转换。非零数值被转换为 true，而值为 0 的 Decimal、Long、Double 或 Int 值被转换为 false。所有其他数据类型均被转换为 true。

## 语法 {#syntax}

```javascript
{
    $toBool: < expression >
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`expression`** | 指定要转换为布尔值的值 |
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

### 示例 1：将 Double 值转换为布尔值 {#example-1-convert-a-double-value-into-a-boolean-value}

要将 latitude 字段的值从 double 转换为布尔值，请对字段使用 $toBool 运算符运行查询以完成转换。正数被转换为 true。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsBool: {
            $toBool: "$location.lat"
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalLatitude": 72.8377,
        "latitudeAsBool": true
    }
]
```

### 示例 2：将字符串值转换为布尔值 {#example-2-convert-a-string-value-into-a-boolean-value}

要将 _id 字段的值从字符串转换为布尔值，请使用 $toBool 值运行查询以完成转换。字符串值被转换为 true。

```javascript
 db.stores.aggregate([{
     $match: {
         _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
     }
 }, {
     $project: {
         originalId: "$_id",
         idAsBool: {
             $toBool: "$_id"
         }
     }
 }])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalId": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "idAsBool": true
    }
]
```

### 示例 3：将 Int 值转换为布尔值 {#example-3-convert-an-int-value-into-a-boolean-value}

要将 sales.totalSales 字段的值从整数转换为布尔值，请使用 $toBool 运算符运行查询以完成转换。正数被转换为 true。

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalTotalSales: "$sales.totalSales",
        totalSalesAsBool: {
            $toBool: "$sales.totalSales"
        }
    }
}])
```

此查询返回以下结果：

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalTotalSales": 9366,
        "totalSalesAsBool": true
    }
]
```

下表描述了 $toBool 运算符根据输入表达式的数据类型所预期的行为。

| **值类型**                                               | **行为/输出** |
|--------------------------------------------------------------|---------------------|
| 布尔值 true                                           | 输出 -> true      |
| 布尔值 false                                          | 输出 -> false     |
| 任意 Double、Int、Long 或 Decimal 值                       | 输出 -> true      |
| 任意 ISODate 值                                            | 输出 -> true      |
| null 值                                                   | 输出 -> null      |
