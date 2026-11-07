---
title: findAndModify
description: findAndModify 命令用于原子性地修改并返回单个文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/findandmodify.md
weight: 30
translation_source_sha256: bf6678b4acb772d2779c4fb61f95a51b07a256644746c30e6800a7e06281da3d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`findAndModify` 命令用于原子性地修改并返回单个文档。该命令适用于需要在单一步骤中读取并更新文档的操作，确保数据一致性。常见用例包括实现计数器、队列以及其他原子操作。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`findAndModify`** | (必需) 指定集合名称的字符串。 |
| **`query`** | (可选) 指定选择过滤器的文档。 |
| **`sort`** | (可选) 指定从匹配结果中选取一个文档时所用排序方式的文档。 |
| **`update`** | (更新时必需) 替换文档或运算符文档，或定义更新流水线的数组。 |
| **`remove`** | (可选) 布尔值，当 `true` 时选择删除路径而非更新路径。 |
| **`new`** | (可选) 布尔值，当 `true` 时返回更新后的文档；否则返回原始文档。 |
| **`fields`** | (可选) 指定应用于返回文档的投影的文档。 |
| **`upsert`** | (可选) 布尔值，当更新过滤器不匹配任何文档时执行插入操作。 |
| **`arrayFilters`** | (可选) 文档数组，指定运算符更新中命名位置标识符的过滤条件；与流水线更新不兼容。对删除操作不生效。 |
| **`let`** | (可选) 指定命令作用域变量的文档，可在 `$$name` 中引用。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数值，单位为毫秒。 |
| **`bypassDocumentValidation`** | (可选) 布尔值，仅在启用模式验证和验证绕过时生效；否则被忽略。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation` 且集群版本为 1.1 或更高。 |
| **`comment`** | (可选) 携带网关请求追踪上下文的字符串；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

必须指定更新或 `remove: true`，二者不可同时指定。删除操作不能请求 `new: true` 或 `upsert: true`。

## 示例：修改并返回一个出发航班 {#example-revise-and-return-a-departure}

以下每个示例均独立，均从 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 开始。

```javascript
db.flights.findOneAndUpdate(
  { route_no: "PG0102" },
  { $set: { delay_minutes: 15 } },
  {
    returnDocument: "after",
    projection: { _id: 0, route_no: 1, delay_minutes: 1 }
  }
)
```

该辅助函数直接返回所选文档：

```json
{ "route_no": "PG0102", "delay_minutes": 15 }
```

`returnDocument: "after"` 映射到线协议字段 `new: true`，`projection` 映射到 `fields`。若未请求更新后的文档，返回值将包含原始的延迟 `12`。

## 示例：删除最早的延误航班 {#example-remove-the-earliest-delayed-service}

```javascript
db.flights.findOneAndDelete(
  { status: "Delayed" },
  {
    sort: { scheduled_departure: 1, _id: 1 },
    projection: { _id: 0, route_no: 1 }
  }
)
```

此操作发送 `findAndModify` 的删除形式，删除 `PG0102`，并直接返回 `{ route_no: "PG0102" }`。与 `delete` 条目不同，此路径可使用 `sort` 选择特定匹配项。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.findAndModify({
   query: <document>,
   sort: <document>,
   remove: <boolean>,
   update: <document>,
   new: <boolean>,
   fields: <document>,
   upsert: <boolean>
})
```

## 详细示例 {#detailed-examples}

### 示例 1：更新总销售额 {#example-1-update-total-sales}

假设我们希望将 `_id` 为 "e5767a9f-cd95-439c-9ec4-7ddc13d22926" 的商店的总销售额更新为 `550000.00`，并返回更新后的文档。

```javascript
db.stores.findAndModify({
   query: { "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $set: { "sales.totalSales": 550000.00 } },
   new: true
})
```

#### 示例输出 {#sample-output}

```json
{
  "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926",
  "name": "Marina's Eyewear Bargains",
  "location": { "lat": -87.4376, "lon": 42.2928 },
  "staff": { "totalStaff": { "fullTime": 20, "partTime": 6 } },
  "sales": {
    "totalSales": 550000,
    "salesByCategory": [
      { "categoryName": "Round Sunglasses", "totalSales": 39621 },
      { "categoryName": "Reading Glasses", "totalSales": 1146 },
      { "categoryName": "Aviators", "totalSales": 9385 }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 2, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 2, "Day": 18 }
      },
      "discounts": [
        { "categoryName": "Square Sunglasses", "discountPercentage": 16 },
        { "categoryName": "Safety Glasses", "discountPercentage": 17 },
        { "categoryName": "Wayfarers", "discountPercentage": 7 },
        { "categoryName": "Eyewear Accessories", "discountPercentage": 12 }
      ]
    }
],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### 示例 2：添加新的促销活动 {#example-2-add-a-new-promotional-event}

让我们向 `_id_` 为 "e5767a9f-cd95-439c-9ec4-7ddc13d22926" 的商店添加名为 "Electronics Super Saver" 的新促销活动，并返回更新后的文档。

```javascript
db.stores.findAndModify({
   query: { "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $push: { "promotionEvents": {
       "eventName": "Electronics Super Saver",
       "promotionalDates": {
         "startDate": "2025-09-31",
         "endDate": "2025-09-31"
       },
       "discounts": [
         {
           "categoryName": "Laptops",
           "discountPercentage": 45
         },
         {
           "categoryName": "Smartphones",
           "discountPercentage": 25
         }
       ]
   }}},
   new: true
})
```

#### 示例输出 {#sample-output-1}

```json
{
  "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926",
  "name": "Marina's Eyewear Bargains",
  "location": { "lat": -87.4376, "lon": 42.2928 },
  "staff": { "totalStaff": { "fullTime": 20, "partTime": 6 } },
  "sales": {
    "totalSales": 550000,
    "salesByCategory": [
      { "categoryName": "Round Sunglasses", "totalSales": 39621 },
      { "categoryName": "Reading Glasses", "totalSales": 1146 },
      { "categoryName": "Aviators", "totalSales": 9385 }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 2, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 2, "Day": 18 }
      },
      "discounts": [
        { "categoryName": "Square Sunglasses", "discountPercentage": 16 },
        { "categoryName": "Safety Glasses", "discountPercentage": 17 },
        { "categoryName": "Wayfarers", "discountPercentage": 7 },
        { "categoryName": "Eyewear Accessories", "discountPercentage": 12 }
      ]
    },
    {
      "eventName": "Electronics Super Saver",
      "promotionalDates": { "startDate": "2025-09-31", "endDate": "2025-09-31" },
      "discounts": [
        { "categoryName": "Laptops", "discountPercentage": 45 },
        { "categoryName": "Smartphones", "discountPercentage": 25 }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### 示例 3：删除一个促销活动 {#example-3-remove-a-promotional-event}

假设我们希望从 `_id` 为 "e5767a9f-cd95-439c-9ec4-7ddc13d22926" 的商店中删除名为 "Electronics Super Saver" 的促销活动，并返回更新后的文档。

```javascript
db.stores.findAndModify({
   query: { "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $pull: { "promotionEvents": { "eventName": "Electronics Super Saver" } } },
   new: true
})
```

#### 示例输出 {#sample-output-2}

```json
{
  "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926",
  "name": "Marina's Eyewear Bargains",
  "location": { "lat": -87.4376, "lon": 42.2928 },
  "staff": { "totalStaff": { "fullTime": 20, "partTime": 6 } },
  "sales": {
    "totalSales": 550000,
    "salesByCategory": [
      { "categoryName": "Round Sunglasses", "totalSales": 39621 },
      { "categoryName": "Reading Glasses", "totalSales": 1146 },
      { "categoryName": "Aviators", "totalSales": 9385 }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 2, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 2, "Day": 18 }
      },
      "discounts": [
        { "categoryName": "Square Sunglasses", "discountPercentage": 16 },
        { "categoryName": "Safety Glasses", "discountPercentage": 17 },
        { "categoryName": "Wayfarers", "discountPercentage": 7 },
        { "categoryName": "Eyewear Accessories", "discountPercentage": 12 }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

## 实现 {#implementation}

别名 `findandmodify` 会到达相同的线协议处理程序。

源码：`pg_documentdb/src/commands/find_and_modify.c`，`ParseFindAndModifyMessage`。参见 [线协议与通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 以获取共享元数据。
