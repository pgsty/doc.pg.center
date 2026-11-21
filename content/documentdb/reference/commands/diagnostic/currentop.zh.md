---
title: currentOp
description: 使用支持的 currentOp 字段和过滤器检查 DocumentDB 中的活动操作。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/diagnostic/currentOp.md
weight: 40
translation_source_sha256: c0b3229ad705034558a887ce42b788673a3a4d259bc97ffd10b640925d7d5419
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

返回 `inprog` 中的操作信息，包括索引构建和集合维护进度。

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
| **`Progress`** | 当前阶段报告的块工作完成百分比：`100 * blocks_done / blocks_total`。大写的 `P` 具有重要意义。当 `blocks_total` 为零时，此字段被省略。 |
| **`terms_done`, `terms_total`** | 索引构建在当前阶段报告的已完成和总元组/词项数，不一定是集合中的文档数量。 |
| **`terms_progress`** | 当前阶段报告的元组/词项工作完成百分比：`100 * terms_done / terms_total`。当 `terms_total` 为零时被省略，如上例所示。 |
| **`msg`** | 操作级别的摘要。它可以描述构建阶段、排队构建或等待重试的失败构建。 |
| **`waitingForLock`** | 操作级别的指示，表明该操作正在等待锁或相关同步事件。当计数器停止推进时，请检查此字段和 `msg`。 |
{.fields}

示例中的 `400 / 1000` 表示**该阶段**按块计算的工作完成了 **40%**，并不代表整个索引构建完成了 40%。词项总数为零，表示无法给出按词项计算的百分比。

达到 `100%` 表示当前阶段报告的工作已完成，不代表整个索引构建已完成。后续阶段仍可能需要排序、验证或等待。计数器和百分比可能在阶段转换时重置或改变含义；不要对记录间的百分比求和，也不应将其用作整体完成度的估算。

比较多次采样的 `phase`、`msg` 和计数器，跟踪构建经过的各个阶段。计数器不可用时，详细进度可能缺失或为空；排队中、失败后等待重试的条目可能只有状态消息。处于等待阶段或缺少百分比，本身不表示失败。

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
| **`Validating index.`** | 在此前的构建阶段完成后验证索引。 |
| **`Index is waiting for commands to reach snapshot threshold.`** | 并发索引验证完成后，等待其他命令持有的旧快照，以便索引可被标记为有效。 |
| **`Cleaning up.`** | 执行清理工作。 |
| **`Concurrent cleanup.`** | 执行并发清理工作。 |
| **`Finalizing.`** | 执行最终化工作。 |
| **`Aborting.`** | 中止操作；这不是成功完成的状态。 |

## 监视 compact 和统计信息维护 {#monitor-compact-and-statistics-maintenance}

使用另一个 shell 连接监视 [`compact`](/documentdb/reference/commands/diagnostic/compact/)，包括 `mode: "full"` 和 `mode: "updateStats"`：

```javascript
db.currentOp({
  $all: true,
  ns: "bookings.flights",
  "command.compact": "flights"
})
```

过滤结果同时包含底层维护操作和 compact 命令包装层。包装层可能没有进度计数器；应查看维护条目了解进度。能否获得这些信息，取决于已安装的实现和调用者对操作的可见权限。

完整重写扫描底层表时，输出片段可能如下所示：

```json
{
  "ns": "bookings.flights",
  "active": true,
  "secs_running": 180,
  "op": "workerCommand",
  "command": { "compact": "flights", "mode": "full" },
  "waitingForLock": false,
  "progress": {
    "phase": "seq scanning heap",
    "blocks_done": 400,
    "blocks_total": 1000,
    "Progress": 40
  },
  "msg": "Vacuum progress: seq scanning heap."
}
```

与索引构建不同，维护计数器直接位于 `progress` 下，不在 `progress.builds` 中。

| 字段 | 说明 |
| --- | --- |
| **`command.compact`** | 正在维护的集合。底层 vacuum 和 analyze 操作也报告为 compact 操作。 |
| **`command.mode`** | 识别为完整重写时为 `full`，analyze 时为 `updateStats`。普通 vacuum 可能省略此字段；字段缺失不代表没有维护在运行。 |
| **`ns`** | 逻辑数据库和集合的命名空间。 |
| **`opid`** | 操作标识符（若有报告）。不同的包装层或工作进程条目可能具有不同标识符。 |
| **`active`** | 操作是否活跃。活跃操作也可能处于等待中；应比较多次采样的阶段和计数器来检查进度。 |
| **`secs_running`** | 此操作已经运行的时间，单位为秒。 |
| **`progress.phase`** | 当前维护阶段，使用底层阶段文本。尚无可用进度行时，可能为 `waiting to start`。 |
| **`progress.blocks_done`** | vacuum/完整重写已扫描的堆块数，或 analyze 已扫描的采样块数。它不是已重写或已删除的文档数量。 |
| **`progress.blocks_total`** | vacuum/完整重写的堆块总数，或 analyze 的采样块总数。计数器可用前，可能为零。 |
| **`progress.Progress`** | 扫描工作完成百分比：`100 * blocks_done / blocks_total`；总数为零时省略。大写的 `P` 具有重要意义。达到 `100%` 表示扫描阶段完成，其他维护阶段可能尚未完成。 |
| **`msg`** | 摘要，例如 `Vacuum progress: seq scanning heap.` 或 `Analyze progress: acquiring sample rows.`。 |
| **`waitingForLock`** | 操作是否正在等待所报告的锁或相关同步事件。计数器停止推进时，应检查此字段。 |
| **`locking_op_prefixes`** | 等待操作可获得的阻塞方操作标识符。 |
| **`writeConflicts`** | 随锁等待信息报告的阻塞进程数量，不是写入失败的累计次数。 |
{.fields}

阶段取决于维护模式。完整重写可能从扫描依次进入写入新堆、重建索引和交换关系文件。扫描进度达到 `100%` 只表示扫描阶段完成，不代表整个 compact 操作完成；后续阶段可能仍在运行。这些计数器既不提供整体完成度估算，也不提供剩余时间估算。Analyze 报告采样块进度，而非完整集合扫描进度。分布式维护可能产生多个条目；不要将其百分比相加。

使用 compact 命令最终的成功响应确认整个操作已完成。客户端超时后，重新连接并使用同一查询，检查维护是否仍然活跃。超时不保证维护会继续：取消操作可能使其停止。条目消失可能意味着成功、失败或取消；`currentOp` 不保留已完成的 compact 结果或其 `bytesFreed` 值。参见[延长 compact 超时并调查结果](/documentdb/reference/commands/diagnostic/compact/#allow-more-time-for-a-full-rewrite)。

## 实现 {#implementation}

索引构建计数器来自 PostgreSQL 的索引创建进度报告。该实现会转换阶段消息，并将报告的计数器归类为 `progress.builds`；排队中和失败/重试中的后台构建也包含在操作输出中。

包含 `waiting for` 的阶段名会先应用通用转换规则，然后才判断各类工作进程等待情况。因此，工作进程的加入、启动、完成、中止、收尾和清理等待目前都显示为 `Index is waiting for other concurrent commands.`，不会分别显示不同的工作进程等待消息。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/current_op.c`、`BuildAggregateSpecFromCommandSpec`、`WriteIndexBuildProgressAndGetMessage`、`PhaseToUserMessage` 和 `AddIndexBuilds`。

维护报告使用同一源文件中的 `MaintenanceProgressQuery`、`WriteMaintenanceProgressAndGetMessage` 和 vacuum/analyze 命令映射。普通 vacuum 读取 `pg_stat_progress_vacuum`，完整重写读取 `pg_stat_progress_cluster`，统计信息刷新读取 `pg_stat_progress_analyze`。
