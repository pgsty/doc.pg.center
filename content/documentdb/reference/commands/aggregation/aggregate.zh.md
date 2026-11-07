---
title: 聚合
description: aggregate 命令用于处理数据记录并返回计算结果。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/aggregation/aggregate.md
weight: 10
translation_source_sha256: 53e79a53d6269a4f861f999b40c5e527e8df317efd7d8312757f96830df04d53
translation_review: AI-assisted bilingual review; 2026-11-07
---

`aggregate` 命令用于处理数据记录并返回计算结果。它对数据执行操作，例如过滤、分组和排序，并可对数据进行多种转换。`aggregate` 命令功能高度灵活，常用于数据分析和报告。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`aggregate`** | (必需) 指定集合名称的字符串或数字，或使用 `1` 表示与集合无关的流水线。 |
| **`pipeline`** | (必需) 聚合流水线阶段文档数组。 |
| **`cursor`** | (必需，除非解释命令) 接受 `batchSize` 和 DocumentDB 扩展 `singleBatch` 的文档。 |
| **`hint`** | (可选) 指定输入集合的索引名称或键模式的字符串或文档。 |
| **`let`** | (可选) 指定命令作用域变量的文档，可通过 `$$name` 引用。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation`。当该功能被禁用时拒绝使用。 |
| **`collectionUUID`** | (可选) 必须与输入集合的 UUID 匹配的 BSON UUID；不匹配将导致命令失败。 |
| **`explain`** | (可选) 布尔值，请求返回解释而非正常执行。[`explain`](/documentdb/reference/commands/diagnostic/explain/) 包装器提供详细程度选择。 |
| **`cursor.batchSize`** | (可选) 限制初始批次大小的数字，转换为整数后必须为非负数；默认值为 `101`；`0` 返回空的首个批次。响应大小限制仍然适用。 |
| **`cursor.singleBatch`** | (可选) 布尔值，当 `true` 时在首个批次后关闭游标。 |
{.fields}

`cursor.batchSize` 被转换为整数，转换后必须为非负数。初始批次默认为 `101`；`0` 返回空的首个批次。`cursor.singleBatch: true` 在该批次后关闭游标。响应大小限制仍然适用。

## 示例：按机场汇总出发信息 {#example-summarize-departures-by-airport}

加载 [航空业示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)，然后运行：

```javascript
db.flights.aggregate(
  [
    { $group: {
      _id: "$departure_airport",
      departures: { $sum: 1 },
      total_seats: { $sum: "$seat_capacity" }
    } },
    { $sort: { _id: 1 } }
  ],
  { batchSize: 10, maxTimeMS: 5000 }
).toArray()
```

返回的数组为：

```json
[
  { "_id": "LED", "departures": 1, "total_seats": 100 },
  { "_id": "SVO", "departures": 3, "total_seats": 440 }
]
```

Shell 游标会自动检索后续批次。[`getMore`](/documentdb/reference/commands/query-and-write/getmore/) 参考文档描述了底层的续传请求。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.aggregate(pipeline, options)
```

## 详细示例 {#detailed-examples}

### 示例 1：按类别计算总销售额 {#example-1-calculate-total-sales-by-category}

本示例演示如何计算 `stores` 集合中每个类别的总销售额。

```javascript
db.stores.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      totalSales: { $sum: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

#### 示例输出 {#sample-output}

```json
[
  { "_id": "Christmas Trees", "totalSales": 3147281 },
  { "_id": "Nuts", "totalSales": 3002332 },
  { "_id": "Camping Tables", "totalSales": 4431667 }
]
```

### 示例 2：查找全职员工超过 10 人的门店 {#example-2-find-stores-with-full-time-staff-greater-than-10}

本示例展示如何筛选全职员工人数大于 10 的门店。

```javascript
db.stores.aggregate([
  {
    $match: {
      "staff.totalStaff.fullTime": { $gt: 10 }
    }
  }
])
```

#### 示例输出 {#sample-output-1}

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lenore's DJ Equipment Store",
    "location": { "lat": -9.9399, "lon": -0.334 },
    "staff": { "totalStaff": { "fullTime": 18, "partTime": 7 } },
    "sales": {
      "totalSales": 35911,
      "salesByCategory": [ { "categoryName": "DJ Headphones", "totalSales": 35911 } ]
    },
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "DJ Turntables", "discountPercentage": 18 },
          { "categoryName": "DJ Mixers", "discountPercentage": 15 }
        ]
      }
    ],
    "tag": [ "#SeasonalSale", "#FreeShipping", "#MembershipDeals" ]
  }
]
```

### 示例 3：列出所有折扣大于 15% 的促销活动 {#example-3-list-all-promotion-events-with-discounts-greater-than-15}

本示例列出所有至少有一项折扣大于 15% 的促销活动。

```javascript
db.stores.aggregate([
  {
    $unwind: "$promotionEvents"
  },
  {
    $unwind: "$promotionEvents.discounts"
  },
  {
    $match: {
      "promotionEvents.discounts.discountPercentage": { $gt: 15 }
    }
  },
  {
    $group: {
      _id: "$promotionEvents.eventName",
      discounts: { $push: "$promotionEvents.discounts" }
    }
  }
])
```

#### 示例输出 {#sample-output-2}

```json
[
  {
    "discounts": [
      { "categoryName": "Basketball Gear", "discountPercentage": 23 },
      { "categoryName": "Wool Carpets", "discountPercentage": 22 },
      {
        "categoryName": "Portable Bluetooth Speakers",
        "discountPercentage": 24
      }
    ]
  }
]
```

## 实现 {#implementation}

在集合或与集合无关的输入上运行流水线。后端将流水线解析为 PostgreSQL 查询；网关通过游标返回结果。

源码：`pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`、`ParseAggregationQueryAndLookupCollection` 和 `ParseCursorDocument`。源码修订版本和共享元数据在 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 中有文档说明。
