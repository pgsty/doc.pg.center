---
title: update
description: DocumentDB 中的 update 命令用于修改集合中匹配特定筛选条件的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/update.md
weight: 70
translation_source_sha256: f9b97da024b66c176db1643d00c551d5c3fb8d71ca4134ee61f4bc338fc2d271
translation_review: AI-assisted bilingual review; 2026-11-07
---

`update` 命令用于修改集合中的现有文档。`update` 命令可根据筛选条件更新一个或多个文档。字段的值可以更改，可以添加新字段和值，也可以移除现有字段。

应用一批更新操作。每个条目提供自己的筛选条件和修改操作，支持单文档更新、多文档更新或 upsert 操作。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`update`** | (必需) 指定集合名称的字符串。 |
| **`updates`** | (必需) 指定操作的文档数组。驱动程序可改用名为 `updates` 的 OP_MSG 序列，但不可同时使用两者。 |
| **`ordered`** | (可选) 布尔值，默认为 `true`；在首次操作出错后停止。 |
| **`let`** | (可选) 指定命令作用域表达式变量的文档，以 `$$name` 形式引用。 |
| **`bypassDocumentValidation`** | (可选) 布尔值，在服务器启用该功能时跳过模式验证；否则被忽略。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数值，单位为毫秒。 |
| **`comment`** | (可选) 携带网关请求追踪上下文的字符串；详见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

## 每个更新操作的参数 {#per-update-parameters}

| 参数 | 描述 |
| --- | --- |
| **`q`** | (必需) 指定匹配筛选条件的文档。 |
| **`u`** | (必需) 替换文档、运算符文档，或定义更新流水线的数组。 |
| **`multi`** | (可选) 布尔值，若为 `true`，则更新所有匹配项；默认为 `false`。 |
| **`upsert`** | (可选) 布尔值，若无文档匹配，则插入新文档；默认为 `false`。 |
| **`arrayFilters`** | (可选) 指定运算符更新中命名位置标识符的文档数组；与流水线更新不兼容。 |
| **`sort`** | (可选) 指定按顺序选择第一个匹配文档的文档；不可与 `multi: true` 同时使用。 |
| **`collation`** | (可选) 指定比较规则的文档；需配合 `documentdb_core.enableCollation` 使用，且集群版本为 1.1 或更高。 |
{.fields}

## 示例：记录修订后的延迟 {#example-record-a-revised-delay}

以下每个示例均独立，均从 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 开始。

```javascript
db.flights.updateOne(
  { route_no: "PG0102" },
  { $inc: { delay_minutes: 3 } },
  { upsert: false, maxTimeMS: 5000 }
)
```

航线 `PG0102` 上的航班延迟从 12 分钟更改为 15 分钟。辅助函数报告 `matchedCount: 1` 和 `modifiedCount: 1`，分别对应线协议响应中的 `n` 和 `nModified`。

## 示例：更新数组内的票价等级 {#example-change-a-fare-class-inside-an-array}

```javascript
db.flights.updateOne(
  { route_no: "PG0101" },
  { $set: { "segments.$[segment].fare_conditions": "Business" } },
  { arrayFilters: [{ "segment.ticket_no": "0005432000101" }] }
)
```

航线 `PG0101` 上的航班中，仅机票航段 `0005432000101` 从 `Economy` 变为 `Business`。其他机票航段和航班保持不变。

## 示例：更新所有延迟航班 {#example-update-every-delayed-flight}

```javascript
db.flights.updateMany(
  { status: "Delayed" },
  { $set: { dispatch_reviewed: true } }
)
```

新字段被添加至 `PG0102` 和 `PG0104`。此多文档更新中不可添加每个更新操作的 `sort`。

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

<span id="example-1-update-a-single-document-using-the-inc-operator"></span>

### 示例 1 - 使用 $inc 运算符更新单个文档 {#example-1---update-a-single-document-using-the-inc-operator}

将指定 _id 文档的 totalSales 增加 10，并减少全职员工数量。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$inc": {"sales.salesByCategory.0.totalSales": 10, "staff.totalStaff.fullTime": -6}})
```

<span id="example-2-update-a-single-document-using-the-min-operator"></span>

### 示例 2 - 使用 $min 运算符更新单个文档 {#example-2---update-a-single-document-using-the-min-operator}

若指定 _id 文档的字段当前值大于 10，则将其 totalStaff 计数更新为 10。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$min": {"staff.totalStaff.fullTime": 10}})
```

<span id="example-3-update-a-single-document-using-the-max-operator"></span>

### 示例 3 - 使用 $max 运算符更新单个文档 {#example-3---update-a-single-document-using-the-max-operator}

若指定 _id 文档的字段当前值小于 14，则将其 totalStaff 计数更新为 14。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$max": {"staff.totalStaff.fullTime": 14}})
```

<span id="example-4-update-a-single-document-using-the-mul-operator"></span>

### 示例 4 - 使用 $mul 运算符更新单个文档 {#example-4---update-a-single-document-using-the-mul-operator}

将指定 _id 文档的兼职员工数量乘以 2。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$mul": {"staff.totalStaff.partTime": 2}})
```

<span id="example-5-update-a-single-document-using-the-rename-operator"></span>

### 示例 5 - 使用 $rename 运算符更新单个文档 {#example-5---update-a-single-document-using-the-rename-operator}

将 totalSales 和 totalStaff 字段分别重命名为 fullSales 和 staffCounts。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$rename": {"sales.totalSales": "sales.fullSales", "staff.totalStaff": "staff.staffCounts"}})
```

<span id="example-6-update-a-single-document-using-the-set-operator"></span>

### 示例 6 - 使用 $set 运算符更新单个文档 {#example-6---update-a-single-document-using-the-set-operator}

将指定 _id 文档的 fullSales 字段设置为 3700。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$set": {"sales.fullSales": 3700}})
```

<span id="example-7-update-a-single-document-using-the-unset-operator"></span>

### 示例 7 - 使用 $unset 运算符更新单个文档 {#example-7---update-a-single-document-using-the-unset-operator}

从指定 _id 文档的 location 对象中移除 lon 字段。

```javascript
db.stores.updateOne({"_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"}, {"$unset": {"location.lon": ""}})
```

<span id="example-8-update-multiple-documents"></span>

### 示例 8 - 更新多个文档 {#example-8---update-multiple-documents}

将所有第一个促销活动在二月开始的文档的开始时间更新为三月。

```javascript
db.stores.updateMany({"promotionEvents.0.promotionalDates.startDate.Month": 2}, {"$inc": {"promotionEvents.0.promotionalDates.startDate.Month": 1}})
```

<span id="example-9-upsert-a-single-document"></span>

### 示例 9 - upsert 单个文档 {#example-9---upsert-a-single-document}

将 upsert 标志设置为 true，若查询筛选条件指定的文档在集合中不存在，则创建新文档。

```javascript
db.stores.updateOne({"_id": "NonExistentDocId"}, {"$set": {"name": "Lakeshore Retail", "sales.totalSales": 0}}, {"upsert": true})
```

## 相关内容 {#related-content}

- [使用 DocumentDB 插入](/documentdb/reference/commands/query-and-write/insert/)
- [使用 DocumentDB 删除](/documentdb/reference/commands/query-and-write/delete/)

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/update.c`、`BuildBatchUpdateSpec` 及每个更新操作的解析。有关会话和事务元数据，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。
