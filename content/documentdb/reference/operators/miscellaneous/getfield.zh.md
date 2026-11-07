---
title: $getField
description: $getField 运算符可从文档中获取指定字段的值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/miscellaneous/$getfield.md
weight: 10
translation_source_sha256: 0a21048c6f33579c12e075ced773707ab64e0446e93fc317576ff6343c61c8d3
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$getField` 运算符用于从文档中获取指定字段的值。它适用于处理动态字段名称，或需要在聚合流水线中以编程方式访问字段的情况。

## 语法 {#syntax}

```javascript
{
  $getField: {
    field: <string>,
    input: <document>
  }
}
```

也可以使用以下简写语法：

```javascript
{
  $getField: <string>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 表示要获取的字段名称的字符串。 |
| **`input`** | 从中获取字段的文档。如果未指定，则默认为当前文档（`$$ROOT`）。 |
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

### 示例 1：基本字段获取 {#example-1-basic-field-retrieval}

使用 `$getField` 获取总销售额：

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      totalSalesValue: {
        $getField: {
          field: "totalSales",
          input: "$sales"
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "totalSalesValue": 37701
  }
]
```

### 示例 2：简写语法 {#example-2-shorthand-syntax}

使用简写语法获取商店名称：

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      storeName: { $getField: "name" },
      storeLocation: { $getField: "location" }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "storeName": "First Up Consultants | Bed and Bath Center - South Amir",
    "storeLocation": {
      "lat": 60.7954,
      "lon": -142.0012
    }
  }
]
```
