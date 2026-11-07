---
title: delete
description: DocumentDB 中的 delete 命令用于删除符合指定条件的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/delete.md
weight: 10
translation_source_sha256: 5fd391a9a3023f97d76d7f346530315456f7f815834920aaa4801e68b06f2523
translation_review: AI-assisted bilingual review; 2026-11-07
---

`delete` 命令用于从集合中删除文档。可根据指定的查询过滤器删除单个文档或多个文档。

根据删除批次中每个条目的选择移除文档。每个条目的 `limit`（而非命令级选项）决定是移除一个匹配项还是所有匹配项。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`delete`** | (必需) 指定集合名称的字符串。 |
| **`deletes`** | (必需) 指定操作的文档数组。驱动程序可改而发送名为 `deletes` 的 OP_MSG 序列，但不可同时使用两者。 |
| **`ordered`** | (可选) 布尔值，默认为 `true`；在首次操作错误后停止。 |
| **`let`** | (可选) 指定命令作用域内引用为 `$$name` 的表达式变量的文档。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒。 |
| **`comment`** | (可选) 携带网关请求追踪的跟踪上下文字符串；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

## 每次删除的参数 {#per-deletion-parameters}

| 参数 | 描述 |
| --- | --- |
| **`q`** | (必需) 指定匹配过滤器的文档。 |
| **`limit`** | (必需) 一个数字，具有如下行为：`1` 移除最多一个匹配项，`0` 移除所有匹配项。小数和其他整数将被拒绝。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation`。 |
{.fields}

## 示例：删除一个航班 {#example-remove-one-flight-service}

以下每个示例均独立，均从 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 开始。

```javascript
db.flights.deleteOne({ route_no: "PG0103" })
```

该辅助函数报告 `deletedCount: 1`，对应线协议响应中的 `n: 1`。它发送 `limit: 1`。按已知航班进行过滤可以确定要删除的文档；非唯一过滤条件不能指定选中哪个匹配项。

## 示例：删除所有延误航班 {#example-remove-all-delayed-services}

```javascript
db.flights.deleteMany({ status: "Delayed" }, { maxTimeMS: 5000 })
```

此操作发送 `limit: 0`，移除 `PG0102` 和 `PG0104`，并报告 `deletedCount: 2`。

空的 `q` 配合 `limit: 0` 会移除集合中的所有文档；它不会删除集合或其索引。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.deleteOne(
   <filter>,
   <options>
)

db.collection.deleteMany(
   <filter>,
   <options>
)
```

## 详细示例 {#detailed-examples}

考虑以下来自 StoreData 数据库中 stores 集合的示例文档。

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

上述示例商店运行两个促销活动，其三个折扣为 19%，因此过滤器 `"promotionEvents.discounts.discountPercentage": 19` 会匹配它。以下每个示例均独立，假设集合已完全填充；它们按顺序排列，使破坏性操作位于最后。

<span id="example-1-delete-a-document-that-matches-a-specified-query-filter"></span>

### 示例 1 - 删除匹配指定查询过滤器的文档 {#example-1---delete-a-document-that-matches-a-specified-query-filter}

```javascript
db.stores.deleteOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"})
```

<span id="example-2-delete-all-documents-that-match-a-specified-query-filter"></span>

### 示例 2 - 删除所有匹配指定查询过滤器的文档 {#example-2---delete-all-documents-that-match-a-specified-query-filter}

```javascript
db.stores.deleteMany({"promotionEvents.discounts.discountPercentage": 19})
```

<span id="example-3-delete-only-one-of-many-documents-that-match-a-specified-query-filter"></span>

### 示例 3 - 仅删除多个匹配指定查询过滤器的文档中的一个 {#example-3---delete-only-one-of-many-documents-that-match-a-specified-query-filter}

应使用 `deleteOne` 而非 `deleteMany`。Shell 中没有选项可将 `deleteMany` 限制为单个文档——`limit` 是线协议 `deletes` 数组元素中的字段（见下文），而非 `deleteMany` 选项，将其在此处传递无效。

```javascript
db.stores.deleteOne({"promotionEvents.discounts.discountPercentage": 19})
```

<span id="example-4-delete-all-documents-in-a-collection"></span>

### 示例 4 - 删除集合中的所有文档 {#example-4---delete-all-documents-in-a-collection}

空过滤器匹配所有内容，因此此操作将清空集合：

```javascript
db.stores.deleteMany({})
```

## 线协议形式 {#wire-protocol-form}

上述 Shell 辅助函数是 `delete` 命令的封装。`deletes` 数组中的每个元素都携带其自身的 `limit`，该值必须为 `0`（删除所有匹配项）或 `1`（最多删除一个匹配项）；任何其他值将被拒绝并返回 `The limit field in delete objects must be 0 or 1`。

```javascript
db.runCommand({
   delete: "stores",
   deletes: [
      { q: {"promotionEvents.discounts.discountPercentage": 19}, limit: 1 }
   ]
})
```

`deleteOne` 发送 `limit: 1`；`deleteMany` 发送 `limit: 0`。

## 相关内容 {#related-content}

- [使用 DocumentDB 的 insert](/documentdb/reference/commands/query-and-write/insert/)
- [使用 DocumentDB 的 update](/documentdb/reference/commands/query-and-write/update/)

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/delete.c`、`BuildBatchDeletionSpec` 和每次删除的解析。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 以获取共享元数据。
