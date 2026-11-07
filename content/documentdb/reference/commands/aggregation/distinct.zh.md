---
title: 唯一值
description: distinct 命令用于在单个集合中查找指定字段的唯一值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/aggregation/distinct.md
weight: 30
translation_source_sha256: a529ac42c03b145022e577b5b26236b28156922301602af6a8ef751e23233f9f
translation_review: AI-assisted bilingual review; 2026-11-07
---

`distinct` 命令用于在单个集合中查找指定字段的唯一值。当需要识别字段的唯一值集合，而无需检索所有文档，或需要基于唯一值执行过滤或分组操作时，该命令非常有用。

返回指定字段路径上的不重复值，结果放在 `values` 中。此命令不创建游标，因此无法通过 `getMore` 继续获取结果。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`distinct`** | (必需) 指定集合名称的字符串。 |
| **`key`** | (必需) 指定字段路径的字符串。 |
| **`query`** | (可选) 指定匹配过滤条件的文档；省略或为 `null` 表示无过滤条件。 |
| **`hint`** | (可选) 指定索引名称或键模式的字符串或文档。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation`，且集群版本为 1.1 或更高版本。否则将被拒绝。 |
{.fields}

## 示例：从一个出发机场列出到达机场 {#example-list-arrival-airports-from-one-departure-airport}

使用 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)：

```javascript
db.flights.distinct("arrival_airport", { departure_airport: "SVO" }, { maxTimeMS: 5000 })
```

返回的数组包含 `"LED"` 和 `"KZN"`。该辅助函数提取命令响应中的 `values` 数组。不应依赖唯一值的顺序。

要改为从嵌入的机票航段中获取舱位等级：

```javascript
db.flights.distinct("segments.fare_conditions")
```

值为 `"Economy"` 和 `"Business"`，不包含重复项。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.distinct(field, query, options)
```

## 详细示例 {#detailed-examples}

以下是使用所提供示例 JSON 结构的示例。

### 示例 1：在销售 中查找不同的类别 {#example-1-find-distinct-categories-in-sales}

在 `salesByCategory` 数组中查找不同的 `categoryName`：

```javascript
db.stores.distinct("sales.salesByCategory.categoryName")
```

#### 示例输出 {#sample-output}

```json
[
  "Music Theory Books",
  "Superfoods",
  "Harmonicas",
  "Garden Tools"
]
```

### 示例 2：在促销事件 中查找不同的事件名称 {#example-2-find-distinct-event-names-in-promotion-events}

在 `promotionEvents` 数组中查找不同的 `eventName`：

```javascript
db.stores.distinct("promotionEvents.eventName")
```

#### 示例输出 {#sample-output-1}

```json
[
  "Super Saver Celebration",
  "Incredible Discount Days"
]
```

### 示例 3：查找特定事件的不同的折扣百分比 {#example-3-find-distinct-discount-percentages-for-a-specific-event}

在 "Summer Sale" 事件的 `discounts` 数组中查找不同的 `discountPercentage`：

```javascript
db.stores.distinct("promotionEvents.discounts.discountPercentage", { "promotionEvents.eventName": "Incredible Discount Days" })
```

#### 示例输出 {#sample-output-2}

```json
[
  6, 17, 22, 25, 9, 15, 14,
  7, 12, 19, 24, 5, 20, 10,
  23, 16, 18, 21, 13, 11, 8
]
```

## 实现 {#implementation}

源码：`pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`, `GenerateDistinctQuery`。有关源码范围和共享元数据，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。
