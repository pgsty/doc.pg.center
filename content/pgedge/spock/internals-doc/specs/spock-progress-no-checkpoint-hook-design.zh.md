---
title: "移除维护 spock.progress 的检查点钩子和逐提交 WAL 刷盘"
description: "Spock 进度视图的持久化改造：以复制来源、提交时间戳和主动保活替代原先相互关联的机制。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/specs/spock-progress-no-checkpoint-hook-design.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



**日期**：2026-04-21；2026-05-01 按实际实现修订。**状态**：已实现。

> **相比最初提案，有两处扩大范围的设计调整。**
>
> 1. **崩溃后通过扫描 `pg_commit_ts` 恢复 `remote_commit_ts`。** 最初设计允许该值为 NULL，接受监控数据暂时不够新。实际实现向后扫描 `pg_commit_ts`，找出对应来源的提交并回填该字段。这项工作从后续改进提升为设计目标，让 `spock.progress` 在崩溃后也能显示准确的时间戳。恢复的 `prev_remote_ts` 还计划用于今后的并行应用改造。
> 2. **保留编号为 144 的 WAL 资源管理器（RMGR）**，改为按事件记录进度。原计划会将其完全删除。实际实现保留了注册，在每个 `resource.dat` 转储位置（正常关闭、`add_node`、表同步）为每个受影响的 `SpockGroupHash` 条目写一条 WAL，保存该条目的完整 `SpockApplyProgress` 快照。恢复状态无须这些记录，但可以通过 `pg_waldump` 查看每个事件 LSN 对应的落盘状态，以便还原事故经过。每批末尾只执行一次 `XLogFlush`，使 WAL 获得与 `resource.dat` 使用 `durable_rename()` 相对应的持久性保证。
>
> 以下各节反映已交付的实现。

## 问题 {#problem}

原方案依靠三套相互关联的机制维护 `spock.progress` 视图。

1. 自定义 WAL 资源管理器（`src/spock_rmgr.c`）在应用每个远端来源的提交时生成 `SPOCK_RMGR_APPLY_PROGRESS` 记录，并同步调用 `XLogFlush`。核心的 `CommitTransactionCommand` 已执行过一次 `XLogFlush`。
2. `Checkpoint_hook` 在 `src/spock.c:1248` 注册，每次 PostgreSQL 检查点都将内存中的 `SpockGroupHash` 转储到 `PGDATA/spock/resource.dat`。为此需要修改 PostgreSQL 核心的 `src/backend/access/transam/xlog.c` 和 `src/include/access/xlog.h`，加入钩子调用。
3. 加载和重做路径在 `shmem_startup_hook` 中以 `resource.dat` 初始化共享内存，恢复时再重做 WAL 中的 `APPLY_PROGRESS` 记录以覆盖初始值。

这种设计有两项成本。

- 每个支持的 PostgreSQL 版本都要维护一份**核心补丁**，共涉及两个文件、四行代码。
- **每应用一笔远端事务都要额外同步调用一次 `XLogFlush`**，仅用于持久化监控数据，使应用关键路径上的 fsync 压力加倍。

调查发现，Spock 的应用工作进程重连时已通过原生复制来源（`replorigin_session_get_progress`）确定从哪个 LSN 继续。恢复位置的正确性由标准逻辑复制机制保障。检查点钩子和 WAL RMGR 主要用来在崩溃后保留额外监控字段（`remote_commit_ts`、`remote_insert_lsn`、`received_lsn`、`last_updated_ts`）。引入检查点钩子（提交 `a4b93e8`）是为了处理应用进程跨检查点空闲的情况：保活消息推进的 `remote_insert_lsn` 不会记入 WAL，原实现只能由该钩子保存它。

## 目标 {#goal}

移除 PostgreSQL 核心补丁（`Checkpoint_hook`）以及每次提交额外的 `XLogFlush`，同时保留正常重启和崩溃重启后用户看到的 `spock.progress` 行为。崩溃后向后扫描 `pg_commit_ts`，按来源恢复 `remote_commit_ts`，使视图中的时间戳准确。恢复的 `prev_remote_ts` 也计划用于后续并行应用改造。

## 范围之外 {#non-goals}

- 更改 `spock.progress` 的列定义或 SQL 层 API。
- 改变应用工作进程继续重放的语义。它已由 PostgreSQL 复制来源机制处理。
- 删除或改变共享内存中 `SpockGroupHash` 的布局，或修改 `SpockApplyProgress` 的结构。
- 精确恢复 `last_updated_ts`（本地应用时间）。崩溃后将其设为恢复得到的 `remote_commit_ts`（发布方提交时间），作为本地应用时间的下界。这可能低估延迟；下一笔提交应用后将刷新。

## 设计概述 {#design-overview}

实际实现继续用 `resource.dat` 保存快照，在正常关闭（监督进程的 `before_shmem_exit`）、`add_node` 和表同步三个位置写入。原先依赖 WAL 持久化监控状态的做法由以下三部分替代。

1. **以复制来源记录的 LSN 作为 `remote_commit_lsn` 的依据。** 应用工作进程启动时读取来源 LSN，与共享内存核对。如果 `resource.dat` 中某条记录的 LSN 落后（file_lsn < origin_lsn），先将该条记录的时间戳置为 NULL，在第三步恢复。
2. **应用进程每次连接或重连都主动请求保活消息。** `spock_start_replication` 返回后，订阅方立即发送带 `replyRequested=true` 的状态更新。PostgreSQL 的 walsender 回复一条携带当前 `sentPtr` 的 'k' 保活消息，已有处理程序便可在重连后的几毫秒内填充共享内存的 `remote_insert_lsn` 和 `received_lsn`，无须等待 `wal_sender_timeout / 2`（默认为 30 秒）。
3. **向后扫描 `pg_commit_ts`，按来源恢复 `remote_commit_ts`。** 若核对发现状态过期或缺失，`recover_progress_timestamps_from_commit_ts()` 从最新 xid 开始向后扫描 `pg_commit_ts`，按发布方的来源 ID 过滤，将最大时间戳写回共享内存。找到该来源的 1000 次提交或共扫描 100 万个 xid 即停止，以先到者为准。`last_updated_ts` 取恢复出的 `remote_commit_ts`，满足 `progress_update_struct` 的异或不变量。发布方提交时间是本地应用时间的下界，可能低估延迟，但不会将延迟直接隐藏为零。

借助这三项机制，以下共享内存字段都不必逐笔写入 WAL 或在检查点持久化。

| 字段 | 数据来源 | 何时可信 |
|---|---|---|
| `remote_commit_lsn` | 复制来源（`replorigin_session_get_progress`） | 应用工作进程启动时，始终准确 |
| `remote_commit_ts` | 若通过来源 LSN 校验，使用 `resource.dat`；否则扫描 `pg_commit_ts` | 正常重启时保留，崩溃后恢复。首次启动且还没有提交时为 NULL |
| `remote_insert_lsn` | 主动请求的 'k' 保活消息 | 应用工作进程连接后的几毫秒内 |
| `received_lsn` | 同上 | 同上 |
| `last_updated_ts` | 每次更新时取 `GetCurrentTimestamp()`；崩溃后设为恢复出的 `remote_commit_ts` | 应用期间持续推进。崩溃后采用发布方提交时间，作为本地应用时间的下界，可能低估延迟；下一笔提交应用后刷新 |
| `prev_remote_ts` | 与 `remote_commit_ts` 一起设置，取值相同 | 与 `remote_commit_ts` 同时恢复 |
{.wide .expand}

## 架构 {#architecture}

### 启动流程 {#startup-flow}

**阶段 1：`shmem_startup_hook`（恢复之前）。**

通过 `spock_group_shmem_startup()` 执行。与旧实现的主要区别是 Spock RMGR 不再携带恢复应用进度所需的记录，WAL 恢复也无须重做任何承载 Spock 状态的记录。

1. 创建空的 `SpockGroupHash` 哈希表。
2. 调用 `spock_group_resource_load()`。如果 `PGDATA/spock/resource.dat` 存在且有效（版本及 `system_identifier` 均匹配），则加载文件。通过 `spock_group_progress_update()` 将每条记录插入或更新到哈希表中。
3. **Spock 的 WAL 重做不再恢复共享内存状态。** 保留 RMGR（编号 144），唯一的记录类型标记转储事件。重做处理程序只输出一条 `LOG` 日志，不修改共享内存。

阶段 1 结束时，共享内存中的哈希表要么为空，要么包含上次正常关闭时 `resource.dat` 的内容。若此后发生过崩溃，这些值可能已经过期。

**阶段 2：各应用工作进程分别核对进度。**

在 `spock_apply_main()` 中，`replorigin_session_setup()` 已设置好会话的复制来源、且尚未调用 `spock_start_replication()` 时，各工作进程核对自己的共享内存条目。`reconcile_progress_with_origin()` 返回 `ReconcileResult` 枚举，调用方据此决定是否需要阶段 3 的恢复扫描。

1. 计算共享内存键：`(MyDatabaseId, MySubscription->target->id, MySubscription->origin->id)`。
2. 读取 `origin_lsn = replorigin_session_get_progress(false)`。
3. 以排他模式获取 `SpockCtx->apply_group_master_lock`，通过 HASH_ENTER 查找或创建条目。
   - **条目不存在。** 以 `remote_commit_lsn = origin_lsn` 初始化，其余字段为零或 NULL，返回 `RECONCILE_FILE_ABSENT`。
   - **条目存在且 `file_lsn == origin_lsn`。** 文件与复制来源同步，保留载入的 `remote_commit_ts` 和 `last_updated_ts`，返回 `RECONCILE_FILE_IN_SYNC`。
   - **条目存在且 `file_lsn < origin_lsn`。** 文件中的条目已落后。将 `remote_commit_lsn` 设为 `origin_lsn`，把 `remote_commit_ts` 和 `last_updated_ts` 清零，并将 `remote_insert_lsn` 和 `received_lsn` 至少提升到 `origin_lsn`，保持 `insert_lsn >= commit_lsn` 的不变量。稍后的主动保活会刷新这两个位置。返回 `RECONCILE_FILE_STALE`。
   - **条目存在且 `file_lsn > origin_lsn`。** 这在正常流程中不应出现。记录警告并以 `origin_lsn` 为准，处理同 STALE 分支。返回 `RECONCILE_FILE_ANOMALY`。
4. 释放锁并返回结果。

阶段 2 放在应用工作进程中执行，因为运行 shmem_startup_hook 时还无法读取系统目录和订阅。

**阶段 3：扫描 `pg_commit_ts`，恢复 `remote_commit_ts`。**

若核对结果不等于 `RECONCILE_FILE_IN_SYNC`，则运行 `recover_progress_timestamps_from_commit_ts(entry, target_origin)`。其中 `target_origin = MySubscription->origin->id` 是发布方的 Spock 节点 ID，也是订阅方在 `pg_commit_ts` 中为已应用事务记录的来源：`handle_origin()` 会按消息将 `replorigin_session_origin` 覆写为该值。

从 `ReadNextTransactionId() - 1` 开始以 `SPOCK_TS_RECOVERY_BATCH_SIZE`（1000）为一批向后扫描，对每个 xid 调用 `TransactionIdGetCommitTsData(xid, &ts, &origin)`，按 `origin == target_origin` 过滤。每个来源分别维护 `running_max_ts` 和 `seen_count`，满足以下任一条件即停止。

- `seen_count >= SPOCK_TS_RECOVERY_MIN_SEEN_PER_ORIGIN`（1000）。
- `total_scanned >= SPOCK_TS_RECOVERY_SCAN_LIMIT`（100 万）。
- 向后到达 `FirstNormalTransactionId`。

每个来源观察到 1000 次提交即可停止，是基于对并发宽度的假设：发布方的 `max_connections` 和连接池限制使在途事务远少于 1000。即使并行应用时订阅方的 xid 顺序与提交时间顺序不同，在这一假设下，更早提交的事务也不会有更大的提交时间戳。

若 `running_max_ts > 0`，持有主锁将该值写入 `remote_commit_ts`、`prev_remote_ts` 和 `last_updated_ts`。`progress_update_struct` 的异或不变量要求 `remote_commit_ts` 和 `last_updated_ts` 同为零或同为非零。以发布方的提交时间作为 `last_updated_ts`，可给出本地应用时间的下界，可能低估延迟。下一笔提交应用后，`last_updated_ts` 会更新为订阅方真实的 `GetCurrentTimestamp()`。若 `running_max_ts == 0`，记录 `WARNING` 并保留 NULL。

这些常量以 `#define` 定义在 `src/spock_progress_recovery.c` 中（`SPOCK_TS_RECOVERY_MIN_SEEN_PER_ORIGIN`、`SPOCK_TS_RECOVERY_SCAN_LIMIT`、`SPOCK_TS_RECOVERY_BATCH_SIZE`）。只有性能分析表明确需调优时才考虑改为 GUC。

无论跳过还是执行，结束时都记录 `LOG`：「ts recovery: file in sync with origin, skipping scan」或「ts recovery: scanned N xids, found K commits, recovered remote_commit_ts」。选用 `LOG` 是因为后台工作进程的 `INFO` 仅发给客户端，不进入服务器日志。

必须开启 `track_commit_timestamp = on`。Spock 在 postmaster 启动时已通过 `spock.conflict_resolution` 的 `check_hook` 检查这一条件，因为唯一允许的值 `last_update_wins` 要求开启它。执行恢复扫描时该项必定已启用，无须重复检查。

**阶段 4：主动请求保活。**

`spock_start_replication()` 返回之后、进入接收循环之前，应用工作进程立即调用一个新的辅助函数。

```c
static void
request_initial_status_update(PGconn *conn, XLogRecPtr startpos);
```

它发送带 `replyRequested=true` 的 'r' 状态更新消息，保留 `send_feedback()` 的内部静态状态。walsender 的 `ProcessStandbyReplyMessage` 识别该标志，调用 `WalSndKeepalive(false, InvalidXLogRecPtr)`，发出携带发布方当前 `sentPtr` 的 'k' 消息。订阅方的保活处理程序通过 `UpdateWorkerStats` 将 `remote_insert_lsn` 和 `received_lsn` 填入共享内存。

### 运行流程 {#runtime-flow}

**提交路径（`src/spock_apply.c:992-1023` 中的 `handle_commit`）。**

删除 `spock_apply_progress_add_to_wal(&sap)` 调用。其外围构造 `SpockApplyProgress` 的代码保留，仍由 `spock_group_progress_update_ptr()` 更新共享内存。每应用一笔远端来源的提交，就少一次 `XLogFlush`。

**保活路径。**

沿用原来的处理逻辑。每次有消息到达，`UpdateWorkerStats()` 都会在共享内存中更新 `remote_insert_lsn` 和 `received_lsn`。

**`spock_group_progress_force_set_list()`（add_node 路径）。**

`add_node` 利用 `read_peer_progress()` 的输出来初始化新节点所见的各对等节点进度。这些记录也是全互联集群中转发事务的*去重状态*，因此必须在首次正常关闭之前就能经受崩溃。

改动如下。
1. 删除逐条执行的 `spock_apply_progress_add_to_wal(sap)`。
2. 对每一条目，先持有主锁，再修改共享内存，然后释放锁。持锁期间不做 I/O。
3. 循环结束后只调用一次 `spock_group_resource_dump()`，通过 `durable_rename` 原子地持久化全部条目。

`resource.dat` 保存完整快照。若每个条目都转储一次，N 个条目就要重写整个文件 N 次。循环末尾只转储一次只需 O(1) 次文件写入。由于管理员视角下的 `add_node` 是整体操作，两者的持久性等效。

**`spock_group_progress_update_list()`（表同步路径）。**

与 `force_set_list` 相同，删除逐条写 WAL 的调用，在循环结束后调用一次 `spock_group_resource_dump()`。

### 关闭流程 {#shutdown-flow}

正常关闭时由监督进程的 `before_shmem_exit` 回调（`src/spock.c` 中的 `spock_supervisor_on_exit`）执行转储。监督进程先轮询，等同级应用／同步进程释放 `PGPROC` 槽，最多约 5 秒。随后执行 `spock_group_resource_dump()` 和 `spock_rmgr_log_resource_dump(SPOCK_DUMP_SHUTDOWN, NULL)`。生成 WAL 必须在监督进程中进行，因为 postmaster 没有可供 `XLogInsert` 使用的后端槽。等待其他进程退出，确保文件和 SHUTDOWN 事件记录都反映各工作进程对 `SpockGroupHash` 的最终更新。这是正常退出时唯一写入 `resource.dat` 的运行路径。

## 代码变更 {#code-changes}

### 删除项 {#delete}

- `src/spock_group.c` 中的 `spock_checkpoint_hook()` 函数，已无注册或引用。
- `include/spock_group.h` 中的 `extern void spock_checkpoint_hook(...)` 声明。
- `src/spock_rmgr.c` 中恢复应用进度的部分，即将 `SPOCK_RMGR_APPLY_PROGRESS` 重做到共享内存的处理程序。文件本身保留，详见下文「精简的代码」。
- 生成 WAL 的辅助函数 `spock_apply_progress_add_to_wal()`。

### 移除的单行代码 {#remove-one-liners}

- `src/spock.c` 中的 `Checkpoint_hook = spock_checkpoint_hook;`。
- `src/spock_apply.c:handle_commit` 中的 `spock_apply_progress_add_to_wal(&sap);`。
- `src/spock_group.c:spock_group_progress_update_list` 中的 `spock_apply_progress_add_to_wal(sap);`。
- `src/spock_group.c:spock_group_progress_force_set_list` 中的 `spock_apply_progress_add_to_wal(sap);`。
- `include/spock_group.h` 中的 `#include "spock_rmgr.h"`。它造成循环包含，且没有使用方。

### 精简的代码 {#trim-do-not-delete}

- **`src/spock_rmgr.c`**：以唯一记录类型 `SPOCK_RMGR_RESOURCE_DUMP` 替换原有应用进度恢复内容。三个 `resource.dat` 转储点都调用新辅助函数 `spock_rmgr_log_resource_dump(event, changed_entries)`。每个进度条目写一条 WAL，内含完整的 `SpockApplyProgress` 快照。由此可用 `pg_waldump` 查看各事件 LSN 对应的实际磁盘状态，还原事故经过。每批记录结束时只需调用一次 `XLogFlush`。
  - 对于 `SHUTDOWN` 和 `ADD_NODE`，调用方为 `changed_entries` 传入 `NULL`。辅助函数遍历 `SpockGroupHash`，为每个条目生成一条记录。这两类事件反映所有订阅的变化。
  - 对于 `TABLE_SYNC`，调用方传入刚才更新共享内存时用过的 `SpockApplyProgress *` 列表。表同步按订阅进行，所以只为受影响订阅的条目生成记录。
  - 重做处理程序逐条输出 `LOG`，包括事件类型、该条在批内的序号、键、LSN 和 `commit_ts`。恢复状态不依赖这些记录。
- **`include/spock_rmgr.h`**：更新声明以匹配精简后的实现，包括 `SPOCK_RMGR_ID = 144`、`SPOCK_RMGR_RESOURCE_DUMP = 0x10`、`SpockResourceDumpRec`（包含 `event_type`、`entry_seq`/`entry_total` 和内嵌 `SpockApplyProgress`）、`SpockResourceDumpEvent` 及生成记录的辅助函数。
- **`src/spock.c`**：`_PG_init` 中保留对 `spock_rmgr_init()` 的调用，并保留相应头文件。

### 修改 {#modify}

- **`src/spock_progress_recovery.c` 和 `include/spock_progress_recovery.h`** 是新模块，只公开 `spock_init_progress_state(XLogRecPtr origin_lsn)`。文件内部包含 `ReconcileResult` 枚举、`reconcile_progress_with_origin()`、`recover_progress_timestamps_from_commit_ts()` 和以 `#define` 定义的 `SPOCK_TS_RECOVERY_*` 常量。
- **`src/spock_apply.c`**：新增 `request_initial_status_update(PGconn *conn, XLogRecPtr startpos)`，发送带 `replyRequested=true` 的 'r' 消息，保留 `send_feedback` 的静态状态。
- **`src/spock_apply.c:spock_apply_main`**：在 `replorigin_session_setup` 与 `spock_start_replication` 之间调用一次 `spock_init_progress_state(origin_lsn)`。它核对进度，发现状态过期时扫描 `pg_commit_ts`。`spock_start_replication` 返回后调用 `request_initial_status_update`。
- **`src/spock_group.c:spock_group_progress_force_set_list`**：移除 WAL 调用，在循环结束后执行一次 `spock_group_resource_dump()`，再调用 `spock_rmgr_log_resource_dump(SPOCK_DUMP_ADD_NODE, ...)`。
- **`src/spock_group.c:spock_group_progress_update_list`**：处理相同，事件类型改用 `SPOCK_DUMP_TABLE_SYNC`。
- **`src/spock.c:spock_supervisor_main`**：通过 `before_shmem_exit` 注册 `spock_supervisor_on_exit`。回调使用新的 `spock_any_apply_worker_running()`（位于 `src/spock_worker.c`）轮询等待应用／同步进程脱离，然后依次调用 `spock_group_resource_dump()` 和 `spock_rmgr_log_resource_dump(SPOCK_DUMP_SHUTDOWN, NULL)`。移除原先 `src/spock_shmem.c` 中在 postmaster 上下文执行的 `spock_on_shmem_exit`。现在文件和 WAL 的转储均由允许调用 `XLogInsert` 的监督进程负责。

### 沿用原实现的部分 {#keep-unchanged}

- `spock_supervisor_on_exit` 继续遵循正常关闭的条件，只在 `code == 0` 时转储。
- `spock_group_resource_load()`、`spock_group_resource_dump()` 的文件加载和转储格式。
- `SpockApplyProgress` 和 `SpockGroupEntry` 的结构布局。
- `spock.progress` SQL 视图和 `get_apply_group_progress()` 函数。

### 移除 PostgreSQL 核心补丁 {#postgres-core-patch-removal}

删除 Spock 侧依赖后，可整体撤回核心补丁。共涉及两个文件的四行代码。

- `postgresql/src/backend/access/transam/xlog.c:173` 中的 `Checkpoint_hook_type Checkpoint_hook = NULL;`。
- `postgresql/src/backend/access/transam/xlog.c:7648-7649` 中 `CreateCheckPoint` 内的两行 `if (Checkpoint_hook) Checkpoint_hook(...)` 调用。
- `postgresql/src/include/access/xlog.h:218-219` 中的 typedef 和 `extern PGDLLIMPORT` 声明。

其余 Spock 代码和 PostgreSQL 补丁均不依赖 `Checkpoint_hook`。

## 边界情况 {#edge-cases}

**发布方没有回复主动保活请求。** 工作进程不阻塞，继续正常接收。`remote_insert_lsn` 和 `received_lsn` 保留初始值（或 NULL），直到 PostgreSQL 按自身的 `wal_sender_timeout / 2` 节奏发来 'k' 或 'w' 消息。最坏情况与原行为相同。

**启动时已有来源，但缺少 `resource.dat`。** 阶段 2 以 `remote_commit_lsn = origin_lsn` 和空时间戳初始化共享内存条目，与首次启动相同。

**启动时 `resource.dat` 中仍有已删除订阅的条目。** 旧条目留在共享内存，无对应工作进程核对。行为与原实现一致。今后可考虑在系统目录可读后清除无主条目。

**启动时来源 LSN 是 `InvalidXLogRecPtr`。** 订阅存在但尚未应用事务。仍先执行核对：若载入的 `resource.dat` 满足 `file_lsn > 0`，则视为 ANOMALY，`commit_lsn` 置零，清空时间戳，插入和接收位置按零下界处理。若 `file_lsn == 0`，则走 IN_SYNC 分支并保留文件值。之后 `spock_init_progress_state` 中的 `XLogRecPtrIsInvalid(origin_lsn)` 会短路跳过 `pg_commit_ts` 扫描。新来源没有可恢复的进度，旧订阅在 `pg_commit_ts` 中的记录只会回填过期的历史时间。

**重试 `add_node`。** 若循环中途失败，共享内存可能只更新一部分，文件则因尚未转储而保持原值。重试会经 `init_progress_fields`、`progress_update_struct` 无条件覆盖这部分状态，最后再转储。

**`add_node` 在转储后中断。** 所有条目均已持久化，重跑操作具有幂等性。

**多个应用工作进程。** 各进程在主锁保护下核对自己的键，互不干扰。主动保活请求按连接发送。

**崩溃后发布方离线。** 阶段 3 从订阅方的 `pg_commit_ts` 恢复 `remote_commit_ts`，这些信息能经受崩溃，无须连接发布方。只有最近 100 万个 xid 内 `pg_commit_ts` 没有该来源的条目时，才会得到 NULL，典型情形是尚未应用任何提交的新订阅。

**扫描未找到任何提交。** 若最近 100 万个 xid 内的 `pg_commit_ts` 条目都不满足 `roident == target_origin`，`running_max_ts` 会保持为 0。记录 `WARNING`，令 `remote_commit_ts` 为 NULL 并继续。

**扫描找到了无关提交。** `roident == MySubscription->origin->id` 过滤的是发布方的 Spock 节点 ID，同一发布方的多个订阅可以共享它。与当前订阅同源的其他订阅，以及已删除重建且旧提交仍在扫描窗口内的订阅，都可能影响 `running_max_ts`。若发布方时钟单调递增，最大时间通常来自当前订阅的最近提交。主要例外是重建期间时钟回拨，或历史提交时间晚于当前提交。影响限于事后分析，应用组排序目前已禁用，尚不消费 `prev_remote_ts`。并行应用改造时可重新评估。

**并发度与扫描停止条件。** 每个来源找到 1000 次提交就停止，假设发布方同时在途的事务少于 1000。PostgreSQL 的 `max_connections` 默认为 100，连接池通常会进一步限制并发。若部署超出假设，只需调高一个 `#define` 常量。

**发布方时钟回拨（NTP 校时）。** `running_max_ts` 取时间戳最大值。如果回拨导致时间戳顺序与实际提交顺序不同，恢复出的 `prev_remote_ts` 可能与发布方下一笔事务的 `required_commit_ts` 不匹配。目前使用 `prev_remote_ts` 的应用组排序机制已禁用，这仍属理论风险。并行应用改造时将重新评估。

**执行 `force_set_list` 时共享内存哈希表已满。** 延续已有行为，给出警告后继续。循环后的转储只持久化成功插入的条目。

**核对期间并发关闭。** 工作进程持锁完成更新，释放后在下一次 `CHECK_FOR_INTERRUPTS` 退出。关闭钩子将已核对的值写入 resource.dat。先核对再转储不会让共享内存落后于文件。

## 测试 {#testing}

### 修改的既有测试 {#modified-existing-tests}

- `tests/tap/t/008_rmgr.pl`：重写阶段 4 的断言以覆盖新的核对语义，包括多来源的两种情况：A 为文件中有过期条目，B 为文件中缺少某来源。测试在 SIGKILL 前执行 `CHECKPOINT`，确保第二批应用记录的 WAL 已持久化，否则 walwriter 的刷新时机可能使恢复位置仍停在第一批，误走 IN_SYNC 而非 STALE。
- `tests/tap/t/022_rmgr_progress_post_checkpoint_crash.pl`：改为验证崩溃后核对能发现 `file_lsn < origin_lsn`、从复制来源推进 `remote_commit_lsn`，且通过扫描将 `remote_commit_ts` 恢复为非 NULL。同时断言 CHECKPOINT 不会更新 `resource.dat`，防止重新引入检查点钩子。

### 新增测试 {#new-tests}

1. **`023_forced_keepalive_timing.pl`**：设置 `wal_sender_timeout=10min` 以排除定时触发的影响，断言 `remote_insert_lsn` 在 1 秒内填入，从而确认刷新来自主动保活。
2. **`026_no_double_wal_flush.pl`**：在应用 30 笔提交期间统计 `pg_stat_wal.wal_sync` 的增量，要求增量小于 N，证明应用关键路径没有逐提交强制 fsync。
3. **`027_remote_commit_ts_recovery.pl`**：依次执行提交、正常重启、更多提交、CHECKPOINT、SIGKILL 和重启。断言崩溃后的 `remote_commit_ts` 非 NULL，证明 `pg_commit_ts` 扫描恢复了该值。
4. **`029_remote_commit_ts_recovery_clean_shutdown.pl`**：只执行正常重启，断言出现跳过扫描的 `LOG`（"file in sync with origin, skipping scan"），未出现实际扫描日志，且 `remote_commit_ts` 得以保留。

### 推迟或尚未实现的测试 {#deferred--not-implemented}

- **关闭 `track_commit_timestamp = off` 的测试。** 实际无法走到此路径。如果关闭该选项，现有的 `spock.conflict_resolution` GUC 校验会在启动时中止 postmaster，恢复扫描不会执行。
- **空闲集群测试（最近 100 万个 xid 内没有该来源的提交）。** 需制造超过 100 万个无关 xid，或临时修改常量。对第一版而言，两种方式开销都过高。
- **`add_node` 循环中断测试。** 超出本设计范围，由已有 `add_node` 集成测试覆盖。

### 回归兼容性 {#regression-safety-checks}

- `spock.progress` 的列集合保持一致。
- `read_peer_progress()` SQL 函数的输出保持一致。
- 使用 `spock.progress` 的下游工具（如 spockctrl 和监控脚本）可以沿用原有模式和列类型。

## 后续工作 {#follow-ups-out-of-scope}

- 若有部署确实需要调优，可将 `SPOCK_TS_RECOVERY_*` 系列 `#define` 常量改为 GUC。
- 把用于事后分析的 RMGR 记录扩充为小型审计事件集，记录更多低频操作，如 `add_node`、`drop_node` 的生命周期、订阅状态转换和同步起止。另见 `2026-05-01-spock-audit-rmgr-design.md` 中的设计草案。
- 重新审视并行应用的排序依据。当前基于 `commit_ts` 的方式受发布方时钟偏差影响，并行应用改造时将考虑其他方案。
- 多个来源共用一次反向扫描，同时填充各来源的共享内存记录，并用 `SpockGroupEntry` 中逐来源的「恢复完成」标志控制。只有性能分析表明逐工作进程扫描的成本确实重要时才值得实现。
- 清除 `resource.dat` 中引用已删除订阅的条目。
- 从 `SpockApplyProgress` 的布局中移除已废弃的 `updated_by_decode`。`prev_remote_ts` 仍是并行应用机制等待和唤醒时使用的坐标，应保留到相关改造落地。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/specs/spock-progress-no-checkpoint-hook-design.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
