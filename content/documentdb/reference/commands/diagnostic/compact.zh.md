---
title: compact
description: 运行集合维护、更新统计信息，或估算 DocumentDB 中可回收的存储空间。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/diagnostic/compact.md
weight: 20
translation_source_sha256: b4bc50821bf0ff187b87566fbfa69e4df425d9661ba5ad0c6b473eb373256ccb
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

运行集合维护或估算可回收空间。

```javascript
db.runCommand({ compact: "flights", dryRun: true })
db.runCommand({ compact: "flights", mode: "updateStats" })
```

| 参数 | 描述 |
| --- | --- |
| **`compact`** | (必需) 指定集合名称的字符串。 |
| **`dryRun`** | (可选) 布尔值，返回 `estimatedBytesFreed` 而不执行压实；默认值为 `false`。不可与 `mode: "updateStats"` 同时使用。 |
| **`freeSpaceTargetMB`** | (可选) 数字；估算的可回收空间低于此正数阈值（单位：MB）时，跳过 `standard` 或 `full` 压实。不限制实际回收量；对 `updateStats` 无效。 |
| **`mode`** | (可选) 作为 DocumentDB 扩展提供的字符串：`standard`（默认）执行普通清理，`full` 请求阻塞式表重写，`updateStats` 刷新规划器统计信息。 |
| **`maxTimeMS`** | （可选）数字，指定命令执行超时，单位为毫秒。长时间维护应显式设置时间预算；默认值和强制上限取决于部署。 |
{.fields}

完全压实要求服务器启用完整清理功能。关闭时，`mode: "full"` 会返回成功及 `bytesFreed: 0`，但不会重写集合。试运行和标准维护不要求启用该功能。操作必须通过集合维护权限检查。

## 示例 {#examples}

示例使用[航空数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)中的 `bookings.flights` 集合。此命令没有专用的 shell 辅助函数。

<span id="refresh-planner-statistics-with-update-stats"></span>

### 使用 updateStats 刷新规划器统计信息 {#refresh-planner-statistics-with-updatestats}

批量加载或大幅修改集合后，刷新查询规划所用的统计信息：

```javascript
db.runCommand({ compact: "flights", mode: "updateStats" })
```

此模式在集合的底层表上运行 PostgreSQL `ANALYZE`，更新用于估算查询选择性和选择执行计划的统计信息，不重写集合或回收存储。成功响应为：

```json
{ "ok": 1, "bytesFreed": 0 }
```

这里 `bytesFreed: 0` 是预期结果，并不意味着统计信息没有变化。刷新统计信息不保证使用某个特定索引或执行计划。

`updateStats` 不会启用按集合维护的规划器统计信息。要在刷新前为集合启用此功能，参见 [`collMod.enableStats`](/documentdb/reference/commands/administration/collmod/#enable-planner-statistics)。它不要求启用完整清理功能，但仍要求具有维护权限，并可能与其他维护操作冲突。

不要将 `updateStats` 与 `dryRun: true` 组合使用，该组合无效。此模式不压实存储，因此 `freeSpaceTargetMB` 不适用。

### 使用 full 回收存储 {#reclaim-storage-with-full}

完全压实通过 PostgreSQL `VACUUM FULL` 重写集合底层表。默认的 `standard` 模式主要使表内已删除或过时记录占用的空间可被复用，而完整重写可以减少集合的存储占用。

先估算可回收空间，不实际执行重写：

```javascript
db.runCommand({ compact: "flights", mode: "full", dryRun: true })
```

响应包含 `estimatedBytesFreed`。它是估算值，不保证后续重写一定回收这么多存储。即使完整清理功能被禁用，试运行仍然可用。

启用该功能后，请求重写：

```javascript
db.runCommand({ compact: "flights", mode: "full" })
```

完全压实会持有排他锁，重写期间阻塞集合上的读写。请安排在维护窗口执行。如果已有冲突操作正在运行，命令可能失败，而不会开始重写。

响应包含 `bytesFreed`。如果完整清理功能被禁用，命令会返回 `{ ok: 1, bytesFreed: 0 }`，不重写任何内容。因此，值为零本身不能证明完整重写已执行。

也可以仅在估算至少有 64 MB 空间可回收时请求重写：

```javascript
db.runCommand({
  compact: "flights",
  mode: "full",
  freeSpaceTargetMB: 64
})
```

压实之前会检查此阈值。若无法获得估算值，或估算值低于阈值，命令跳过重写并返回 `bytesFreed: 0`。此值不限制实际回收的空间量。

### 为完整重写预留更多时间 {#allow-more-time-for-a-full-rewrite}

大集合的完整重写可能超过两分钟。以下是前述完全压实示例的另一种用法，允许最多运行 30 分钟，而不依赖部署的默认超时：

```javascript
db.runCommand({
  compact: "flights",
  mode: "full",
  maxTimeMS: 1800000
})
```

根据集合大小和维护窗口选择时间预算。30 分钟只是示例，不是完成保证或新的默认值。延长超时不会缩短排他锁的持有时间。客户端套接字超时和提供商网关限制也必须允许所请求的时长。

### 监视维护并调查超时 {#monitor-maintenance-and-investigate-a-timeout}

从**另一个 shell 连接**检查同一集合的维护状态：

```javascript
db.currentOp({
  $all: true,
  ns: "bookings.flights",
  "command.compact": "flights"
})
```

在 compact 运行期间重复查询，或在原请求超时后重新连接并查询。结果的 `inprog` 条目可能包含命令包装层和底层维护操作。`progress.phase`、块计数器、`msg` 和锁等待信息见 [compact 进度字段](/documentdb/reference/commands/diagnostic/currentop/#monitor-compact-and-statistics-maintenance)。

Compact 是同步操作，不是异步排队作业。服务器端超时可能取消命令及其维护连接；仅凭客户端超时或连接丢失，无法确定服务器端是否已停止。如果仍有匹配的维护条目，应继续监视，不要立即提交另一个 compact 请求。如果已无条目，`currentOp` 无法判断操作是成功完成还是被取消，也无法恢复原来的 `bytesFreed` 响应。请结合原命令响应（若可获得）和提供商诊断信息确定结果。

## 实现 {#implementation}

`updateStats` 运行 `ANALYZE`，`standard` 运行 `VACUUM`，`full` 运行 `VACUUM FULL`。集群版本为 1.0 或更高时，存储回收报告比较清理前后的关系文件大小；较旧集群版本使用估算值报告。

参见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/compact.c`、`ParseCompactCommandSpec`、`command_compact`、`PerformCompactOperation` 和 `RunVacuumAndMeasureFreedSpace`。

超时处理：网关的 `postgres/documentdb_data_client.rs`、`execute_compact` 和 `postgres/conn_mgmt/query_dispatch.rs`；维护连接取消：`pg_documentdb/src/infrastructure/connection_management.c`。进度报告：`pg_documentdb/src/commands/current_op.c`、`WriteMaintenanceProgressAndGetMessage`。
