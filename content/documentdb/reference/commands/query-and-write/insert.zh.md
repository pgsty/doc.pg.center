---
title: insert
description: DocumentDB 中的 insert 命令在集合中创建新文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/insert.md
weight: 50
translation_source_sha256: db22efd593df8ec1338f4b5b8a37e73fa9686c4a7f1329a025882c5d7c20924f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`insert` 命令用于将新文档插入集合。一次操作可插入单个文档或多个文档。

将一批文档插入集合。未提供 `_id` 的文档将获得自动生成的标识符；显式指定的 `_id` 必须在集合内唯一。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`insert`** | (必需) 指定集合名称的字符串。 |
| **`documents`** | (必需) 指定批量文档的数组；驱动程序可改用名为 `documents` 的 OP_MSG 文档序列发送；不可同时提供两种表示形式。 |
| **`ordered`** | (可选) 布尔值，默认为 `true`：遇到首个写入错误后停止。`false` 尝试处理剩余文档。 |
| **`bypassDocumentValidation`** | (可选) 布尔值，当服务器启用绕过模式验证的能力时跳过模式验证；否则被忽略。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`comment`** | (可选) 携带网关请求追踪上下文的字符串；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

`collation` 默认被拒绝。

## 示例：加载航空数据集 {#example-load-the-airline-dataset}

航空示例数据集的[设置](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)使用 `insert` 加载四条航班记录。通过提供显式标识符，确保后续读取示例结果可复现。

## 示例：添加一个机场 {#example-add-an-airport}

在 `bookings` 数据库中运行此命令，且当前无使用 `_id: "SVO"` 的机场文档。机场代码作为文档标识符：

```javascript
db.airports.insertOne({
    _id: "SVO",
    airport_name: "Sheremetyevo",
    city: "Moscow",
    country: "Russia",
    timezone: "Europe/Moscow"
}, { maxTimeMS: 5000 })
```

成功时，辅助函数报告 `acknowledged: true` 和 `insertedId: "SVO"`。底层线协议响应在 `n` 中统计插入数量。

## 示例：在重复标识符后继续插入 {#example-continue-after-a-duplicate-identifier}

在前述机场插入操作后运行，且当前无使用 `_id: "LED"` 的机场：

```javascript
db.airports.insertMany(
  [
    { _id: "SVO", airport_name: "Sheremetyevo", city: "Moscow", country: "Russia", timezone: "Europe/Moscow" },
    { _id: "LED", airport_name: "Pulkovo", city: "Saint Petersburg", country: "Russia", timezone: "Europe/Moscow" }
  ],
  { ordered: false }
)
```

第一条记录产生重复键错误，第二条仍可插入。Mongosh 抛出批量写入错误，通过 `index: 0` 标识失败的输入条目。底层命令响应使用 `writeErrors` 表示失败，`n` 表示成功插入。若使用 `ordered: true`，处理将在重复项处停止。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.insert(
   <single document or array of documents>,
   {
     writeConcern: <document>,
     ordered: <boolean>
   }
)
```

## 详细示例 {#detailed-examples}

### 插入单个文档 {#inserting-a-single-document}

以下命令将单个文档插入 StoreData 数据库中的 stores 集合。

```javascript
db.stores.insertOne({
  "storeId": "12345",
  "name": "Boulder Innovations",
  "location": {
    "lat": 37.7749,
    "lon": -122.4194
  },
  "staff": {
    "totalStaff": {
      "fullTime": 15,
      "partTime": 10
    }
  },
  "sales": {
    "totalSales": 500000.00,
    "salesByCategory": [
      {
        "categoryName": "Laptops",
        "totalSales": 300000.00
      },
      {
        "categoryName": "Smartphones",
        "totalSales": 200000.00
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Summer Sale",
      "promotionalDates": {
        "startDate": "2024-06-01",
        "endDate": "2024-06-30"
      },
      "discounts": [
        {
          "categoryName": "Laptops",
          "discountPercentage": 15
        },
        {
          "categoryName": "Smartphones",
          "discountPercentage": 10
        }
      ]
    },
    {
      "eventName": "Holiday Specials",
      "promotionalDates": {
        "startDate": "2024-12-01",
        "endDate": "2024-12-31"
      },
      "discounts": [
        {
          "categoryName": "Laptops",
          "discountPercentage": 20
        },
        {
          "categoryName": "Smartphones",
          "discountPercentage": 25
        }
      ]
    }
  ]
})
```

### 插入多个文档 {#inserting-multiple-documents}

以下命令将文档数组插入 stores 集合。

```javascript
db.stores.insertMany([
  {
    "storeId": "12346",
    "name": "Graphic Design Institute",
    "location": {
      "lat": 34.0522,
      "lon": -118.2437
    },
    "staff": {
      "totalStaff": {
        "fullTime": 20,
        "partTime": 5
      }
    },
    "sales": {
      "totalSales": 750000.00,
      "salesByCategory": [
        {
          "categoryName": "Laptops",
          "totalSales": 400000.00
        },
        {
          "categoryName": "Smartphones",
          "totalSales": 350000.00
        }
      ]
    },
    "promotionEvents": [
      {
        "eventName": "Black Friday",
        "promotionalDates": {
          "startDate": "2024-11-25",
          "endDate": "2024-11-30"
        },
        "discounts": [
          {
            "categoryName": "Laptops",
            "discountPercentage": 25
          },
          {
            "categoryName": "Smartphones",
            "discountPercentage": 30
          }
        ]
      }
    ]
  },
  {
    "storeId": "12347",
    "name": "Relecloud",
    "location": {
      "lat": 40.7128,
      "lon": -74.0060
    },
    "staff": {
      "totalStaff": {
        "fullTime": 10,
        "partTime": 20
      }
    },
    "sales": {
      "totalSales": 600000.00,
      "salesByCategory": [
        {
          "categoryName": "Laptops",
          "totalSales": 350000.00
        },
        {
          "categoryName": "Smartphones",
          "totalSales": 250000.00
        }
      ]
    },
    "promotionEvents": [
      {
        "eventName": "New Year Sale",
        "promotionalDates": {
          "startDate": "2024-01-01",
          "endDate": "2024-01-07"
        },
        "discounts": [
          {
            "categoryName": "Laptops",
            "discountPercentage": 10
          },
          {
            "categoryName": "Smartphones",
            "discountPercentage": 15
          }
        ]
      }
    ]
  }
])
```

<span id="specifying-a-value-for-the-id-field"></span>

### 为 _id 字段指定值 {#specifying-a-value-for-the-_id-field}

若未指定 _id 字段，服务器将为文档自动生成唯一的 ObjectId() 值。若文档指定了 _id 字段，则必须在集合内所有文档中全局唯一。

若指定重复的 _id 字段值，服务器将抛出重复键违规错误。

```json
{
    "WriteErrors": [
        {
            "WriteError": {
                "err": {
                    "index": 0,
                    "code": 11000,
                    "errmsg": "Duplicate key violation on the requested collection: Index '_id_'",
                    "errInfo": "undefined",
                    "op": {
                        "testField": "testValue",
                        "_id": "1"
                    }
                }
            }
        }
    ]
}
```

### 按顺序插入多个文档 {#inserting-multiple-documents-in-order}

批量插入的文档按提供的顺序插入，且在首个失败处停止。这是默认行为，因此下方的 `ordered: true` 为显式而非必需。若希望服务器无视错误仍尝试处理每个文档，请改用 `ordered: false`。

```javascript
db.stores.insertMany([
  {
    "_id": "123456",
    "storeId": "123456",
    "name": "Graphic Design Institute",
    "location": {
      "lat": 34.0522,
      "lon": -118.2437
    },
    "staff": {
      "totalStaff": {
        "fullTime": 20,
        "partTime": 5
      }
    },
    "sales": {
      "totalSales": 750000.00,
      "salesByCategory": [
        {
          "categoryName": "Laptops",
          "totalSales": 400000.00
        },
        {
          "categoryName": "Smartphones",
          "totalSales": 350000.00
        }
      ]
    },
    "promotionEvents": [
      {
        "eventName": "Black Friday",
        "promotionalDates": {
          "startDate": "2024-11-25",
          "endDate": "2024-11-30"
        },
        "discounts": [
          {
            "categoryName": "Laptops",
            "discountPercentage": 25
          },
          {
            "categoryName": "Smartphones",
            "discountPercentage": 30
          }
        ]
      }
    ]
  },
  {
    "_id": "234567",
    "storeId": "234567",
    "name": "Relecloud",
    "location": {
      "lat": 40.7128,
      "lon": -74.0060
    },
    "staff": {
      "totalStaff": {
        "fullTime": 10,
        "partTime": 20
      }
    },
    "sales": {
      "totalSales": 600000.00,
      "salesByCategory": [
        {
          "categoryName": "Laptops",
          "totalSales": 350000.00
        },
        {
          "categoryName": "Smartphones",
          "totalSales": 250000.00
        }
      ]
    },
    "promotionEvents": [
      {
        "eventName": "New Year Sale",
        "promotionalDates": {
          "startDate": "2024-01-01",
          "endDate": "2024-01-07"
        },
        "discounts": [
          {
            "categoryName": "Laptops",
            "discountPercentage": 10
          },
          {
            "categoryName": "Smartphones",
            "discountPercentage": 15
          }
        ]
      }
    ]
  }
], { ordered: true })
```

成功插入后，返回结果以输入数组中的位置为键，列出插入文档的 ID。注意，`insertedIds` 报告的是输入位置，而非执行顺序，因此在 `ordered: false` 下其结构保持不变——这并非确认文档实际应用顺序的方式：

```json
{
    "acknowledged": true,
    "insertedIds": {
        "0": "123456",
        "1": "234567"
    }
}
```

## 相关内容 {#related-content}

- [使用 DocumentDB 更新](/documentdb/reference/commands/query-and-write/update/)
- [使用 DocumentDB 查询](/documentdb/reference/commands/query-and-write/find/)

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/insert.c`、`BuildBatchInsertionSpec`。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 了解事务与可重试写入元数据。
