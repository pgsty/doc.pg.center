---
title: $type
description: $type 运算符检索所选字段为指定类型的文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/element-query/$type.md
weight: 20
translation_source_sha256: b7626aa5fdb499d03390e3cb1c55868b2e35bd44bf8af7a3e114152064e15573
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$type` 运算符检索所选字段为指定类型的文档。$type 运算符可用于数据验证，并确保集合中各文档的一致性。

## 语法 {#syntax}

```javascript
{
  <field>: { $type: <BSON type number> | <string alias> }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要检查类型的字段。 |
| **`BSON type number`** | BSON 类型对应的编号（例如，1 表示 double，2 表示 string）。 |
| **`string alias`** | BSON 类型的字符串别名（例如，"double"、"string"、"object"、"array"）。 |
{.fields}

## 常见 BSON 类型 {#common-bson-types}

| 类型 | 编号 | 别名 | 说明 |
| --- | --- | --- | --- |
| 双精度浮点数 | 1 | "double" | 64 位浮点数 |
| 字符串 | 2 | "string" | UTF-8 字符串 |
| 对象 | 3 | "object" | 嵌入式文档 |
| 数组 | 4 | "array" | 数组 |
| ObjectId | 7 | "objectId" | ObjectId |
| 布尔值 | 8 | "bool" | 布尔值 |
| 日期 | 9 | "date" | 日期 |
| null | 10 | "null" | null 值 |
| 32 位整数 | 16 | "int" | 32 位整数 |
| 时间戳 | 17 | "timestamp" | 时间戳 |
| 64 位整数 | 18 | "long" | 64 位整数 |
{.wide .expand}

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

### 示例 1：查找名称为字符串类型的商店 {#example-1-find-stores-with-string-type-names}

要查找任意一家 name 字段为字符串类型的商店，可对 name 字段使用 $type 运算符执行查询。然后仅投影 ID 和 name 字段，并将结果限制为结果集中的一个文档。

```javascript
db.stores.find({
    "name": {
        $type: "string"
    }
}, {
    "_id": 1,
    "name": 1
}).limit(1)
```

此查询返回以下结果：

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort"
    }
]
```

### 示例 2：通过多项类型检查验证数据 {#example-2-data-validation-using-multiple-type-checks}

此查询演示如何验证集合文档结构中的关键字段是否具有预期的数据类型。

```javascript
db.stores.find({
      "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
      "name": {
          $type: "string"
      },
      "location": {
          $type: "object"
      },
      "staff.employeeCount.fullTime": {
          $type: ["int", "long"]
      },
      "promotionEvents": {
          $type: "array"
      }
  }, {
      "_id": 1,
      "name": 1,
      "location": 1,
      "staff": 1
  }
)
```

此查询返回以下结果。

```json
[
    {
        "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
        "name": "Trey Research | Home Office Depot - Lake Freeda",
        "location": {
            "lat": -48.9752,
            "lon": -141.6816
        },
        "staff": {
            "employeeCount": {
                "fullTime": 12
            }
        }
    }
]
```
