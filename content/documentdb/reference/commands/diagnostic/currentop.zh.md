---
title: currentOp
description: 使用支持的 currentOp 字段和过滤器检查 DocumentDB 中的活动操作。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/currentOp.md
weight: 40
translation_source_sha256: ce69c77b1a5eaa3468960767312c5da2f4f7152d3f81c4b81f3fb646fd5f4718
translation_review: AI-assisted bilingual review; 2026-11-07
---

返回 `inprog` 中的操作信息，包括索引构建进度。

```javascript
db.currentOp({ $all: true, active: true, ns: "bookings.flights" })
```

Mongosh 通过聚合实现 `currentOp()`，并在 `inprog` 中返回结果。下文选项描述的是直接线协议命令；它处理 `$all` 的方式与 shell 辅助函数将选项转换为聚合选项的方式不同。

| 参数 | 描述 |
| --- | --- |
| **`currentOp`** | (必需) 一个命令标记，通常为 `1`。 |
| **`$all`** | (可选) 类布尔值，用于设置底层 `allUsers` 的选择；默认为 `false`。 |
| **其他非通用字段** | (可选) 一个查询谓词，用于过滤操作文档，例如 `active: true` 或 `ns: "bookings.flights"`。 |
{.fields}

该命令构建一个包含空闲连接和会话的当前操作查询，然后再进行过滤。[`$currentOp`](/documentdb/reference/operators/aggregation/currentop/) 聚合流水线阶段具有独立的选项文档。

## 监控索引构建 {#monitor-index-builds}

在索引构建期间，从另一个 shell 连接运行以下命令：

```javascript
db.currentOp({
  $all: true,
  ns: "bookings.flights",
  "command.createIndexes": { $exists: true }
})
```

这包括 [airline 示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 的索引创建操作。在调查排队或重试中的构建时，不要添加 `active: true`：这些条目可能报告 `active: false`。当存在时，使用 `command.indexes` 识别索引名称和键模式。

`inprog` 中一个条目的示例摘录如下：

```json
{
  "ns": "bookings.flights",
  "active": true,
  "command": {
    "createIndexes": "flights",
    "indexes": [{ "key": { "route_no": 1 }, "name": "route_no_1" }],
    "$db": "bookings"
  },
  "progress": {
    "builds": [
      {
        "phase": "Scanning Table (building index).",
        "concurrent": true,
        "blocks_done": 400,
        "blocks_total": 1000,
        "Progress": 40,
        "terms_done": 0,
        "terms_total": 0
      }
    ]
  }
}
```

### 读取进度字段 {#read-the-progress-fields}

| 字段 | 描述 |
| --- | --- |
| **`progress.builds`** | 报告的构建进度记录数组。检查每个记录；多个记录或操作可能参与分布式构建。 |
| **`phase`** | 当前阶段，使用以下[转换后的阶段消息](#index-build-phase-messages)。可用阶段取决于索引和构建路径。 |
| **`concurrent`** | 报告的构建是否使用并发索引创建。这并非完成指示。 |
| **`blocks_done`, `blocks_total`** | 当前阶段已完成和总块数。这些并非文档计数。 |
| **`Progress`** | 基于块的百分比：`100 * blocks_done / blocks_total`。大写的 `P` 具有重要意义。当 `blocks_total` 为零时，此字段被省略。 |
| **`terms_done`, `terms_total`** | 索引构建在当前阶段报告的已完成和总元组/词项数，不一定是集合中的文档数量。 |
| **`terms_progress`** | 基于元组/词项的百分比：`100 * terms_done / terms_total`。当 `terms_total` 为零时被省略，如上例所示。 |
| **`msg`** | 操作级别的摘要。它可以描述构建阶段、排队构建或等待重试的失败构建。 |
| **`waitingForLock`** | 操作级别的指示，表明该操作正在等待锁或相关同步事件。当计数器停止推进时，请检查此字段和 `msg`。 |
{.fields}

示例中的 `400 / 1000` 表示**该阶段**按块计算的工作完成了 **40%**，并不代表整个索引构建完成了 40%。词项总数为零，表示无法给出按词项计算的百分比。

计数器和百分比可能在构建阶段转换时重置或改变含义。一个阶段达到 `100%` 后，仍可能继续排序、验证或等待。不要对记录间的百分比求和，也不应将其用作整体完成度的估算。

计数器不可用时，详细进度可能缺失或为空；排队中、失败后等待重试的条目可能只有状态消息。处于等待阶段或缺少百分比，本身不表示失败。请结合 `phase`、`msg` 和多次采样结果判断。

`currentOp` 中条目消失并不证明成功。对于[索引创建调用](/documentdb/reference/commands/indexing/createindexes/)中等待完成的情况，请使用调用的最终结果确认构建是否成功。

### 索引构建阶段消息 {#index-build-phase-messages}

`progress.builds[].phase` 存放的是转换后的消息，不是底层阶段名称。这些消息也可能出现在操作级别的 `msg` 中。下表按大致的时间顺序排列，并非必须依次经过的流程：具体阶段取决于索引与构建路径，有些阶段会跳过。等待并发命令可能在多个阶段之间反复出现；中止属于另一条执行路径，不是成功构建的最后一步。

| 报告阶段 | 描述 |
| --- | --- |
| **`Initializing index.`**, **`Initializing index`** | 准备索引构建。两种标点变体由实现返回，用于不同的初始化阶段。 |
| **`Index is waiting for other concurrent commands.`** | 在构建前或后续阶段之间等待并发活动，包括工作进程协调。等待期间计数器可能保持不变。 |
| **`Building index.`** | 正在构建索引；不再报告更具体的构建阶段。 |
| **`Scanning Table (building index).`** | 作为构建的一部分，扫描集合的底层表。 |
| **`Concurrently Sorting tuples (building index).`** | 工作进程正在并发排序元组。 |
| **`Concurrently merging tuples on workers (building index).`** | 工作进程正在并发合并元组。 |
| **`Sorting tuples (building index).`** | 为索引构建排序元组。 |
| **`Merging tuples into index (building index).`** | 将元组合并到索引中。 |
| **`Writing WAL files (building index).`** | 为索引构建写入预写日志（WAL）文件。 |
| **`Finalizing index build.`** | 完成索引构建工作，准备验证（如适用）；尚未确认索引创建请求成功。 |
| **`Validating index.`** | 验证索引。这可能在早期构建工作达到 `100%` 后出现。 |
| **`Index is waiting for commands to reach snapshot threshold.`** | 并发索引验证完成后，等待其他命令持有的旧快照，以便索引可被标记为有效。 |
| **`Cleaning up.`** | 执行清理工作。 |
| **`Concurrent cleanup.`** | 执行并发清理工作。 |
| **`Finalizing.`** | 执行最终化工作。 |
| **`Aborting.`** | 中止操作；这不是成功完成的状态。 |

## 实现 {#implementation}

索引构建计数器来自 PostgreSQL 的索引创建进度报告。该实现会转换阶段消息，并将报告的计数器归类为 `progress.builds`；排队中和失败/重试中的后台构建也包含在操作输出中。

包含 `waiting for` 的阶段名会先应用通用转换规则，然后才判断各类工作进程等待情况。因此，工作进程的加入、启动、完成、中止、收尾和清理等待目前都显示为 `Index is waiting for other concurrent commands.`，不会分别显示不同的工作进程等待消息。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/current_op.c`、`BuildAggregateSpecFromCommandSpec`、`WriteIndexBuildProgressAndGetMessage`、`PhaseToUserMessage` 和 `AddIndexBuilds`。
