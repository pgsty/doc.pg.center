---
title: 计数
description: 计数命令用于统计集合中符合指定查询条件的文档数量。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/aggregation/count.md
weight: 20
translation_source_sha256: 3ad620862a9f91022ea147a7cc55493b68cf16a848d4cff4d2dbe58e038f2721
translation_review: AI-assisted bilingual review; 2026-11-07
---

`count` 命令用于统计集合中符合指定查询条件的文档数量。该命令适用于快速获取存储在集合中的数据的统计信息，例如满足特定条件的文档数量。

计数结果放在 `n` 中返回，不返回游标。如果查询被省略或为空，且没有其他查询修饰项，可以使用集合统计信息；提供查询或索引提示时，会通过执行查询来计数。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`count`** | (必需) 指定集合名称的字符串。 |
| **`query`** | (可选) 指定匹配过滤条件的文档。省略则对集合不加过滤地进行计数。 |
| **`skip`** | (可选) 非负整数，表示在计数前跳过多少个匹配项。 |
| **`limit`** | (可选) 指定最大计数的整数；`0` 表示无限制。负值使用其绝对值。 |
| **`hint`** | (可选) 指定索引名称或键模式的字符串或文档；强制使用基于查询的计数路径。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数值，单位为毫秒。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation`。 |
{.fields}

## 示例：统计延迟航班数量 {#example-count-delayed-flights}

使用 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)：

```javascript
db.flights.count({ status: "Delayed" })
```

该辅助函数返回 `2`。与原始命令响应不同，它是一个数字，而非包含 `n` 的文档。

要跳过第一个匹配项后最多统计一个匹配航班：

```javascript
db.flights.count({ departure_airport: "SVO" }, { skip: 1, limit: 1 })
```

此操作返回 `1`。`count()` 辅助函数针对此处记录的命令；当前 mongosh 已将该辅助函数标记为已弃用。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.count(query, options)
```

## 详细示例 {#detailed-examples}

以下是一些演示 `count` 命令用法的示例：

### 示例 1. 统计集合中的所有文档数量 {#example-1-counting-all-documents-in-a-collection}

统计 `stores` 集合中的所有文档数量：

```javascript
db.stores.count({})
```

#### 示例输出 {#sample-output}

```json
60570
```

### 示例 2. 统计满足特定条件的文档数量 {#example-2-counting-documents-with-specific-criteria}

统计门店 ID（`_id`）为指定值的门店数量：

```javascript
db.stores.count({ "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
```

#### 示例输出 {#sample-output-1}

```json
1
```

### 示例 3. 统计满足嵌套条件的文档数量 {#example-3-counting-documents-with-nested-criteria}

统计具有特定促销活动的商店数量：

```javascript
db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })   
```

#### 示例输出 {#sample-output-2}

```json
2156
```

### 示例 4. 统计满足多个条件的文档数量 {#example-4-counting-documents-with-multiple-criteria}

统计位于特定经纬度的商店数量：

```javascript
db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
```

#### 示例输出 {#sample-output-3}

```json
1
```

## 实现 {#implementation}

源码：`pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`, `GenerateCountQuery`。有关源码范围和共享元数据，请参阅 [线协议与通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。
