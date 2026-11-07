---
title: $jsonSchema
description: $jsonSchema 运算符根据 JSON Schema 定义验证文档，以验证数据并强制要求文档符合指定结构。了解支持的功能及限制。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/evaluation-query/$jsonschema.md
weight: 20
translation_source_sha256: 0601f2c464913c336876c95e6dd11525018fe33c47f5e7183f6602776d44a143
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$jsonSchema` 运算符用于按照 JSON Schema 规范验证文档，确保文档符合预定义的结构、数据类型和验证规则。

## 语法 {#syntax}

`$jsonSchema` 运算符的语法如下：

```javascript
db.createCollection("collectionName", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["field1", "field2"],
      properties: {
        field1: {
          bsonType: "string",
          description: "Description of field1 requirements"
        },
        field2: {
          bsonType: "int",
          minimum: 0,
          description: "Description of field2 requirements"
        }
      }
    }
  },
  validationLevel: "strict", // Optional: "strict" or "moderate"
  validationAction: "error"   // Optional: "error" or "warn"
})
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`bsonType`** | 指定字段必须匹配的二进制 JSON（BSON）类型。接受 $type 运算符使用的字符串别名。 |
| **`properties`** | 定义特定字段验证规则的对象。 |
| **`minimum/maximum`** | 数值字段的数值约束。 |
| **`minLength/maxLength`** | 字符串长度约束。 |
| **`minItems/maxItems`** | 数组长度约束。 |
| **`pattern`** | 用于字符串验证的正则表达式模式。 |
| **`items`** | 数组元素的模式验证。 |
| **`uniqueItems`** | 布尔值，表示数组元素是否必须唯一。 |
{.fields}

## 支持的关键字 {#supported-keywords}

DocumentDB 支持以下 JSON Schema 关键字：

| 关键字 | 类型 | 说明 | 用途 |
|---------|------|-------------|--------|
| `additionalItems` | 数组 | 额外数组元素的模式 | 扩展数组验证 |
| `bsonType` | 所有类型 | MongoDB 扩展，接受 BSON 类型别名 | `"string"`、`"int"`、`"double"`、`"object"`、`"array"`、`"bool"`、`"date"` |
| `description` | 不适用 | 说明性文本；必须为字符串 | 仅用于文档说明 |
| `enum` | 所有类型 | 值必须等于所列值之一 | 将字段限制为固定取值 |
| `exclusiveMinimum` | 数值 | 布尔值；使下限不包含 `minimum` 本身（必须同时指定 `minimum`） | 高级数值验证 |
| `exclusiveMaximum` | 数值 | 布尔值；使上限不包含 `maximum` 本身（必须同时指定 `maximum`） | 高级数值验证 |
| `items` | 数组 | 数组元素的模式 | 数组元素验证 |
| `minimum` | 数值 | 最小值约束 | 数值验证 |
| `maximum` | 数值 | 最大值约束 | 数值验证 |
| `minItems` | 数组 | 数组的最小长度 | 数组大小验证 |
| `maxItems` | 数组 | 数组的最大长度 | 数组大小验证 |
| `multipleOf` | 数值 | 值必须为指定数值的倍数 | 数学约束 |
| `minLength` | 字符串 | 字符串的最小长度 | 字符串验证 |
| `maxLength` | 字符串 | 字符串的最大长度 | 字符串验证 |
| `oneOf` | 所有类型 | 值必须恰好匹配所列子模式中的一个 | 可选结构 |
| `pattern` | 字符串 | 正则表达式模式匹配 | 字符串格式验证 |
| `properties` | 对象 | 定义对象字段的验证规则 | 嵌套对象的模式定义 |
| `required` | 对象 | 必需字段名称组成的数组 | 强制要求指定字段 |
| `type` | 所有类型 | 标准 JSON Schema 类型 | `"object"`、`"array"`、`"number"`、`"boolean"`、`"string"`、`"null"` |
| `uniqueItems` | 数组 | 强制要求数组元素唯一 | 数据完整性 |
{.wide .expand}

### 不支持的关键字 {#unsupported-keywords}

以下关键字会被拒绝，并返回错误 `The '<keyword>' keyword in $jsonSchema is not supported at this time`：

| 关键字 | 类型 | 替代方法 |
|---------|------|------------|
| `$ref` | 不适用 | 将引用的模式内联 |
| `$schema` | 不适用 | 省略该关键字 |
| `default` | 不适用 | 在应用逻辑中设置默认值 |
| `definitions` | 不适用 | 将子模式内联 |
| `format` | 字符串 | 使用 `pattern` |
| `id` | 不适用 | 省略该关键字 |

系统接受 `encrypt` 和 `encryptMetadata`，以便解析客户端字段级加密模式；DocumentDB 本身不执行任何加密。

其他任何关键字，包括 `additionalProperties`、`allOf`、`anyOf`、`dependencies`、`maxProperties`、`minProperties`、`not`、`patternProperties` 和 `title`，都会被拒绝，并返回错误 `Unknown $jsonSchema keyword: <keyword>`。

## 示例 {#examples}

下面使用 `stores` 数据集介绍实际示例：

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  }
}
```

### 示例 1：基本结构验证 {#example-1-basic-structure-validation}

此查询检索名称长度为 5 至 100 个字符、且地理坐标处于有效范围内的所有商店：纬度介于 -90 与 90 之间，经度介于 -180 与 180 之间。

```javascript
db.stores.find({
  $jsonSchema: {
    bsonType: "object",
    required: ["name", "location"],
    properties: {
      _id: {
        bsonType: "string"
      },
      name: {
        bsonType: "string",
        minLength: 5,
        maxLength: 100
      },
      location: {
        bsonType: "object",
        required: ["lat", "lon"],
        properties: {
          lat: {
            bsonType: "double",
            minimum: -90,
            maximum: 90
          },
          lon: {
            bsonType: "double",
            minimum: -180,
            maximum: 180
          }
        }
      }
    }
  }
}).limit(1)

```

### 示例 2：结合数组元素验证销售数据 {#example-2-sales-validation-with-array-items}

此查询检索 sales 字段为有效对象的所有商店文档，该对象须包含非负的 totalSales 值，以及至少含有一个元素的 salesByCategory 数组。

```javascript
db.stores.find({
  $jsonSchema: {
    bsonType: "object",
    required: ["sales"],
    properties: {
      sales: {
        bsonType: "object",
        required: ["totalSales", "salesByCategory"],
        properties: {
          totalSales: {
            bsonType: "int",
            minimum: 0
          },
          salesByCategory: {
            bsonType: "array",
            minItems: 1,
            items: {
              bsonType: "object",
              properties: {
                categoryName: {
                  bsonType: "string",
                  minLength: 1
                },
                totalSales: {
                  bsonType: "int",
                  minimum: 0
                }
              }
            }
          }
        }
      }
    }
  }
}).limit(1)

```

此查询匹配示例数据中的一家商店，其 `name` 和 `sales` 字段如下：

```javascript
[
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    sales: {
      salesByCategory: [
        { categoryName: 'Phone Mounts', totalSales: 12000 },
        { categoryName: 'Dash Cameras', totalSales: 22300 }
      ],
      peakSalesRecord: 100000,
      revenue: 50000,
      totalSales: 50000
    }
  }
]
```

### 示例 3：结合查询运算符使用 {#example-3-combining-with-query-operators}

此查询检索所有满足以下条件的商店文档：staff 字段为有效对象，包含 totalStaff 子对象且其中至少有一名全职员工（fullTime ≥ 1），并且 sales.totalSales 大于 10,000。

```javascript
db.stores.find({
  $and: [
    {
      $jsonSchema: {
        required: ["staff"],
        properties: {
          staff: {
            bsonType: "object",
            required: ["totalStaff"],
            properties: {
              totalStaff: {
                bsonType: "object",
                required: ["fullTime"],
                properties: {
                  fullTime: {
                    bsonType: "int",
                    minimum: 1
                  }
                }
              }
            }
          }
        }
      }
    },
    // Additional query constraints
    {
      "sales.totalSales": { $gt: 10000 }
    }
  ]
}).limit(1)
```

此查询匹配示例数据中的一家商店，其 `name`、`staff` 和 `sales.totalSales` 字段如下：

```javascript
[
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    staff: {
      maxStaffCapacity: 25,
      employeeCount: { fullTime: 10, partTime: 2 },
      totalStaff: { fullTime: 10, partTime: 2 }
    },
    sales: { totalSales: 50000 }
  }
]
```
