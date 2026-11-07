---
title: getMore
description: getMore 命令用于从现有游标中检索额外的数据批次。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/getMore.md
weight: 40
translation_source_sha256: 24c53c1cca9f9d7282761c7c3ef9a8ecce52fe6569f97f5a6394e4b009054fca
translation_review: AI-assisted bilingual review; 2026-11-07
---

`getMore` 命令用于从现有游标中检索额外的数据批次。该命令在处理无法通过单次查询获取的大型数据集时非常有用，因为存在大小限制。该命令允许客户端通过返回游标的命令（例如 [find](/documentdb/reference/commands/query-and-write/find/) 和 [aggregate](/documentdb/reference/commands/aggregation/aggregate/)）分页获取结果，以管理可处理的块大小。

返回现有游标在 `cursor.nextBatch` 中的下一个数据批次。必须使用前一个命令返回的游标标识符；其 BSON int64 类型必须保持不变。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`getMore`** | (必需) 一个 BSON int64，指定游标 ID。BSON int32 将被拒绝。 |
| **`collection`** | (有条件) 一个字符串，指定与游标关联的集合。当启用网关参数验证时，此参数为必需。 |
| **`batchSize`** | (可选) 一个数字或 null，指定请求的数据批次上限。启用参数验证时，可转换为负整数的值将被拒绝。 |
| **`maxTimeMS`** | (可选) 一个数字，指定批次的超时时间；对于可尾随游标，限制等待新数据的时间。 |
| **`comment`** | (可选) 一个字符串，携带用于网关请求追踪的上下文信息；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

Shell 和驱动程序游标会自动维护继续使用游标所需的 [会话和事务元数据](/documentdb/reference/commands/diagnostic/wire-protocol/#common-request-fields)。请求必须使用创建游标的会话和事务。未使用会话创建的游标必须保持无会话状态。

若省略 `batchSize`，则不会使用初始查询的默认值 `101`：分页由剩余结果和响应大小限制（最多 16 MB）决定。仅一个短批次并不能证明游标已耗尽。当返回的 `cursor.id` 为零时停止。

启用参数验证时，未知的非 `$` 字段将被拒绝。旧版配置在此阶段仅验证游标 ID。

## 示例：分页浏览航班 {#example-page-through-flights}

使用 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)，让 Shell 继续游标操作：

```javascript
const flightCursor = db.flights.find({}, { _id: 0, route_no: 1 })
  .sort({ route_no: 1 }).batchSize(2)
flightCursor.next()
flightCursor.next()
flightCursor.next()
flightCursor.next()
flightCursor.close()
```

连续调用 `next()` 会返回路线 `PG0101`、`PG0102`、`PG0103` 和 `PG0104` 的文档。当首次两个结果被消耗后，Shell 会请求下一个批次，自动管理游标 ID 和会话元数据。上述选项说明涵盖了底层 `getMore` 请求的内容。

## Shell 语法 {#shell-syntax}

```javascript
db.runCommand({
   getMore: NumberLong("<cursor-id>"),
   collection: <collection-name>,
   batchSize: <number-of-documents>,
   maxTimeMS: <milliseconds>
})
```

## 详细示例 {#detailed-examples}

### 示例 1：从游标检索更多文档 {#example-1-retrieve-more-documents-from-a-cursor}

假设你有一个来自 `stores` 集合的游标 ID `1234567890`。以下命令将获取最多五个额外的文档：

```javascript
db.runCommand({
   getMore: NumberLong("1234567890"),
   collection: "stores",
   batchSize: 5
})
```

### 示例 2：耗尽游标的剩余内容 {#example-2-drain-the-rest-of-the-cursor}

省略 `batchSize` 将在单个批次中返回游标当前持有的所有文档，最多不超过 16 MB：

```javascript
db.runCommand({
   getMore: NumberLong("1234567890"),
   collection: "stores"
})
```

批次可能比请求的更小，且省略 `batchSize` 并不能保证游标已被耗尽——16 MB 的批次限制可能使其提前终止。应持续调用 `getMore`，直到响应报告 `cursor.id` 为 `0`，而不是在批次小于 `batchSize` 时停止。

## 实现 {#implementation}

源码：网关 `processor/cursor.rs`、`validate_get_more_arguments` 和 `process_get_more`。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/) 以获取经审计的源版本和元数据行为。
