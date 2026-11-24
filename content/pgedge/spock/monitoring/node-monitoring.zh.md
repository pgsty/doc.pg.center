---
title: "使用 Spock 状态视图监控节点"
description: "通过 spock 模式中的视图查询节点保存在共享内存里的运行状态。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/node_monitoring.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



Spock 将节点状态保存在共享内存中，通过 `spock` 模式下的一组视图提供查询。管理员可以直接查看订阅是否正在复制、哪些工作进程正在运行、各提供方的复制进度落后多少、复制槽保留了多少 WAL，以及最近发生了哪些事件。

| 视图 | 每行代表 | 用途 |
|------|-------------|---------|
| `spock.system_status` | 主机 | 主机与实例的运行状况，包括磁盘、负载、连接、长事务、事务 ID 回卷风险及归档。 |
| `spock.node_status` | 节点 | 一行汇总节点的版本、计数、WAL、延迟及最近事件。 |
| `spock.subscription_status` | 订阅 | 配置、状态、处理该订阅的工作进程、复制位置与延迟，以及最近的错误。 |
| `spock.subscription_stats` | 订阅 | 活动计数，包括工作进程启动、连接、事务、元组、冲突和错误。 |
| `spock.worker_status` | Spock 进程 | 监督进程、管理进程、应用和同步工作进程及其状态。 |
| `spock.slot_status` | 复制槽 | 提供方各 Spock 槽的 walsender 状态、位置及保留的 WAL。 |
| `spock.table_sync_status` | 订阅或表 | 以可读形式显示初始同步状态。 |
| `spock.peer_status` | 已知节点 | 本节点已知的每个节点，以及将其变更传入本地的订阅。 |
| `spock.replication_set_status` | 复制集 | 本地复制集，以及各复制集的表数、序列数和订阅数。 |
| `spock.settings` | 参数 | Spock 参数及复制所依赖的 PostgreSQL 核心参数。 |
| `spock.events` | 事件 | 最近的状态变化，如启停订阅、重启、报错和升级。 |
{.wide .expand}

`spock.node_report()` 依次查询这些视图，将整个节点整理成一份文本报告。参见[完整报告](#the-full-report)。

各视图的范围均为当前数据库。`spock.lag_tracker`、`spock.progress` 和 `spock.channel_*_stats` 视图仍可使用，也是上述视图的数据来源。

## 系统状态 {#system-status}

`spock.system_status` 用一行描述主机和 PostgreSQL 实例。排查复制前，可以先看磁盘是否已满、系统负载是否过高、连接是否耗尽、长事务或空闲事务是否阻碍 VACUUM 和复制槽推进，以及 WAL 归档是否失败。

| 列 | 说明 |
|--------|-------------|
| `hostname`, `os_name`, `os_release`, `architecture`, `cpu_count`, `memory_bytes` | 主机信息。 |
| `load_average_1min`, `load_average_5min`, `load_average_15min` | 系统平均负载。 |
| `data_directory`, `data_disk_total_bytes`, `data_disk_free_bytes` | 数据目录及其所在卷的空间。 |
| `wal_disk_total_bytes`, `wal_disk_free_bytes`, `wal_size_bytes` | `pg_wal` 所在卷的空间及 `pg_wal` 目录大小。此目录可能是符号链接，因此单独测量。 |
| `database_size_bytes` | 当前数据库大小。 |
| `postgres_version`, `postmaster_pid`, `postmaster_start_time`, `uptime`, `in_recovery` | 实例信息。 |
| `max_connections`, `connections`, `active_connections`, `idle_in_transaction` | 客户端连接数及其状态。 |
| `longest_transaction`, `longest_idle_in_transaction` | 存续时间最长的事务以及空闲时间最长的未结束事务。两者均可能阻碍 VACUUM 和复制槽的 `catalog_xmin` 推进。 |
| `waiting_on_locks` | 当前正在等待锁的会话。 |
| `prepared_transactions` | 已预备的事务。它们在最终提交或回滚前保持锁和 xmin。 |
| `physical_standbys` | 除 Spock 订阅方外的其他流复制副本。 |
| `oldest_xid_age` | 数据库中最老事务 ID 的年龄，用来判断距回卷还有多远。 |
| `xact_commit`, `xact_rollback`, `deadlocks`, `recovery_conflicts`, `temp_files`, `temp_bytes`, `checksum_failures`, `database_stats_reset` | 取自当前数据库的 `pg_stat_database`。 |
| `archive_mode`, `archived_count`, `last_archived_time`, `archive_failed_count`, `last_archive_failure` | WAL 归档状态。归档持续失败会填满 WAL 所在卷。 |
{.wide .expand}

```sql
SELECT pg_size_pretty(data_disk_free_bytes) AS data_free,
       pg_size_pretty(wal_disk_free_bytes) AS wal_free,
       load_average_1min, connections, max_connections,
       longest_transaction, idle_in_transaction, deadlocks,
       archive_failed_count, last_archive_failure
  FROM spock.system_status;
```

## 节点状态 {#node-status}

`spock.node_status` 始终恰好返回一行，即使尚未创建本地节点。

| 列 | 说明 |
|--------|-------------|
| `node_id`, `node_name`, `location`, `country` | 本地节点的信息。无本地节点时为 NULL。 |
| `database_name` | 当前数据库。 |
| `hostname`, `operating_system`, `postmaster_start_time` | 主机信息和服务器启动时间。 |
| `spock_version` | 已加载共享库的版本。 |
| `extension_version` | 系统目录中已安装扩展的版本。 |
| `extension_update_pending` | 共享库版本高于已安装扩展时为 true。管理进程会在下次启动时执行 `ALTER EXTENSION UPDATE`。 |
| `postgres_version` | 服务器版本。 |
| `spock_started_at` | Spock 共享内存初始化时间，通常为 postmaster 启动时间。 |
| `postmaster_pid`, `supervisor_pid`, `manager_pid` | postmaster、监督进程和当前数据库管理进程的 PID。 |
| `readonly_mode` | `spock.readonly` 的当前值。 |
| `apply_paused` | `spock.pause_apply_workers()` 生效期间为 true。 |
| `worker_slots`, `worker_slots_used` | Spock 可使用的后台工作进程槽数，以及已占用的槽数。 |
| `subscriptions`, `subscriptions_enabled`, `subscriptions_replicating` | 各状态的订阅数。 |
| `replication_slots`, `replication_slots_active` | 当前数据库的 Spock 槽数，以及其中已连接 walsender 的槽数。 |
| `apply_workers`, `sync_workers` | 正在运行的工作进程数。 |
| `workers_restart_pending` | 出错退出、等待管理进程重新启动的工作进程数。 |
| `pending_exceptions` | 当前正按 `spock.exception_behaviour` 设置重试的事务。 |
| `replicated_tables`, `unreplicated_tables` | 本节点已加入某个复制集的表数及尚未加入任何复制集的表数。 |
| `current_wal_lsn` | 当前 WAL 位置；在备库上为重放位置。 |
| `wal_size_bytes` | `pg_wal` 的大小，由 `spock.wal_size_bytes()` 自行对文件大小求和，因此不具备 `pg_monitor` 的角色也可读取此值。 |
| `data_disk_free_bytes`, `wal_disk_free_bytes` | 数据目录和 `pg_wal` 所在卷的可用空间。 |
| `max_retained_wal_bytes` | 进度最慢的 Spock 槽要求保留的 WAL 量。 |
| `max_replication_lag_bytes`, `max_replication_lag` | 所有订阅中的最大延迟。 |
| `exceptions_logged` | `spock.exception_log` 中的行数。 |
| `last_event_time`, `last_error_event_time` | 最近事件和最近错误事件的时间。 |
| `events_retained`, `events_recorded` | 历史中仍保留的事件数，以及启动以来记录的事件总数。 |
{.wide .expand}

```sql
SELECT node_name, extension_update_pending, subscriptions_replicating,
       replication_slots_active, workers_restart_pending,
       pg_size_pretty(max_retained_wal_bytes) AS retained_wal,
       max_replication_lag, last_error_event_time
  FROM spock.node_status;
```

## 订阅状态 {#subscription-status}

当复制看起来停滞时，先查看 `spock.subscription_status`。

| 列 | 说明 |
|--------|-------------|
| `subscription_id`, `subscription_name`, `enabled` | 订阅标识、名称和启用状态。 |
| `status` | `replicating`、`initializing`、`starting`（工作进程已启动但尚未开始传输，如循环重连时）、`down`（已启用但无工作进程）、`disabled` 或 `unknown`。 |
| `provider_node`, `provider_dsn` | 提供方信息。DSN 中的密码用星号代替。 |
| `slot_name`, `replication_sets`, `forward_origins`, `apply_delay`, `skip_lsn`, `skip_schema`, `force_text_transfer`, `created_at` | 订阅配置。 |
| `sync_status` | 整个订阅的初始同步状态。 |
| `worker_pid`, `worker_status`, `worker_started_at` | 应用工作进程信息。失败后等待重启时，`worker_status` 为 `restart pending`。 |
| `worker_terminated_at`, `worker_restart_delay` | 上一个工作进程失败的时间，以及管理进程重新启动它之前的等待时长（毫秒）。 |
| `worker_paused` | 因应用已暂停而休眠时为 true。 |
| `in_exception_handling` | 按 `spock.exception_behaviour` 重放失败事务时为 true。 |
| `pending_exception_lsn`, `pending_exception_error` | 正在重试的事务的提交 LSN 和首次错误（如有）。 |
| `origin_lsn` | 取自 `spock.replication_origin_status()`，表示本地已持久应用的最后一个提供方 LSN。 |
| `remote_commit_lsn`, `remote_commit_ts`, `remote_insert_lsn`, `received_lsn` | 来自 `spock.progress` 的复制位置。 |
| `replication_lag_bytes` | 提供方已写入、本节点尚未应用的 WAL 量。 |
| `replication_lag` | 最近已应用事务在提供方提交与在本地应用之间的时间差。 |
| `last_message_received`, `last_xact_applied` | 最近收到提供方数据的时间，以及最近在本地提交事务的时间。 |
| `time_since_last_message` | 距最近一次收到数据已有多久。上游长时间没有消息时，先看此项。 |
| `worker_blocked_by_pids`, `worker_blocking_pid`, `worker_blocking_query` | 工作进程等待锁时，显示持锁会话以及第一个持锁会话正在执行的查询。 |
| `worker_starts`, `worker_failures`, `xacts_applied`, `apply_errors` | 来自 `spock.subscription_stats` 的计数器。 |
| `last_apply_error`, `last_error_sqlstate`, `last_error_pid`, `last_error_message` | 应用工作进程最近一次错误的时间、SQLSTATE、报错进程及包含 DETAIL 和 CONTEXT 的消息。 |
{.wide .expand}

```sql
SELECT subscription_name, status, worker_status, replication_lag,
       pg_size_pretty(replication_lag_bytes) AS lag, last_error_message
  FROM spock.subscription_status;
```

## 订阅统计 {#subscription-statistics}

`spock.subscription_stats` 为每个订阅返回一行，汇总应用和同步工作进程收集的计数。工作进程重启后计数仍保留。使用 `spock.reset_subscription_stats(subid)` 可重置指定订阅，省略参数则重置全部订阅。每项计数都有对应的 `last_*` 时间戳，记录最近一次变化时间。

| 列 | 说明 |
|--------|-------------|
| `worker_starts`, `worker_failures` | 应用工作进程启动次数和出错退出次数。 |
| `sync_worker_starts`, `sync_worker_failures` | 复制表的同步工作进程的相应计数。重新同步时，每张表增加一次启动。 |
| `provider_connects`, `provider_disconnects`, `idle_timeouts` | 依次为成功连接提供方的次数、连接中断及连接尝试失败的合计（提供方离线时每次重试均计入），以及由 `spock.apply_idle_timeout` 触发的重连次数。 |
| `messages_received`, `bytes_received` | 从提供方收到的数据消息及字节数。 |
| `xacts_applied`, `xacts_skipped`, `xacts_discarded` | 在本地提交、通过 `sub_skip_lsn` 跳过、按 `transdiscard` 丢弃的事务数量。 |
| `apply_errors`, `sync_errors` | 应用和同步工作进程报告的错误数。应用错误每个失败事务计一次。 |
| `deadlocks`, `lock_timeouts`, `constraint_violations`, `resource_errors` | 按 SQLSTATE 分类的同一批错误：检测到死锁、无法获取锁、23 类（约束违例）和 53 类（资源不足）。 |
| `tables_synced` | 已完成初始同步的表数。 |
| `n_tup_ins`, `n_tup_upd`, `n_tup_del`, `n_conflict`, `n_dca` | 元组相关计数，由 `spock.channel_table_stats` 汇总。 |
| `confl_*` | 按类型统计的冲突数；PostgreSQL 18 之前为 NULL。 |
| `last_error_message`, `last_error_lsn`, `last_error_sqlstate`, `last_error_pid` | 最近一次工作进程错误，含 DETAIL、CONTEXT、当时的提供方 LSN、SQLSTATE 和报错进程。 |
| `stats_reset` | 计数最近一次重置的时间。 |
{.wide .expand}

## 工作进程 {#workers}

`spock.worker_status` 列出监督进程、当前数据库的管理进程及所有应用和同步工作进程，也包括出错退出后等待重新启动的工作进程槽。

| 列 | 说明 |
|--------|-------------|
| `worker_slot`, `worker_type`, `pid` | 共享内存中的槽位、进程类型（`supervisor`、`manager`、`apply` 或 `sync`）及 PID。 |
| `worker_status` | `starting`、`running`、`idle`、`stopping`、`stopped`、`failed` 或 `restart pending`。 |
| `subscription_id`, `subscription_name` | 适用于应用和同步工作进程。 |
| `sync_schema_name`, `sync_table_name` | 同步工作进程正在复制的表。 |
| `started_at`, `xact_start`, `backend_state`, `wait_event_type`, `wait_event` | 取自 `pg_stat_activity`。 |
| `blocked_by_pids`, `blocking_pid`, `blocking_xact_start`, `blocking_query` | 工作进程因其他会话持锁而等待时填写，信息来自 `pg_blocking_pids()`。 |
| `paused`, `in_exception_handling`, `sync_pending` | 应用工作进程的状态标志。 |
| `replay_stop_lsn`, `remote_wal_insert_lsn` | 工作进程要重放到的位置，以及最近在提供方看到的 WAL 位置。 |
| `generation`, `terminated_at`, `restart_delay` | 注册计数、最近失败时间和重启等待时长（毫秒）。 |
{.wide .expand}

## 复制槽 {#replication-slots}

`spock.slot_status` 是提供方视图。当前数据库每个 Spock 复制槽各占一行，并关联为其服务的 walsender。

| 列 | 说明 |
|--------|-------------|
| `slot_name`, `active`, `active_pid` | 复制槽及其 walsender。 |
| `client_name`, `client_addr`, `connected_at`, `state` | 已连接的订阅方信息，取自 `pg_stat_replication`。 |
| `restart_lsn`, `confirmed_flush_lsn`, `sent_lsn`, `write_lsn`, `flush_lsn`, `replay_lsn` | 各阶段的 WAL 位置。 |
| `retained_wal_bytes` | 因该复制槽而保留在磁盘上的 WAL 量。 |
| `pending_wal_bytes` | 订阅方尚未确认的 WAL 量。 |
| `write_lag`, `flush_lag`, `replay_lag`, `last_reply_time` | 反馈延迟及最近应答时间。 |
| `wal_status`, `safe_wal_size`, `catalog_xmin`, `catalog_xmin_age`, `temporary`, `two_phase` | 取自 `pg_replication_slots`。`catalog_xmin_age` 持续增长，表示该槽正在妨碍系统目录的 VACUUM 回收。 |
| `decoded_txns`, `decoded_bytes`, `spill_*`, `stream_*`, `decode_stats_reset` | 该槽完成的解码工作量，取自 `pg_stat_replication_slots`。`spill_bytes` 持续增加，表示有事务超过 `logical_decoding_work_mem` 的内存上限。 |
| `slot_group_*` | 复制槽组的共享状态，仅适用于并行槽。 |
{.wide .expand}

```sql
SELECT slot_name, active, state, pg_size_pretty(retained_wal_bytes) AS retained,
       pg_size_pretty(pending_wal_bytes) AS pending, replay_lag
  FROM spock.slot_status;
```

## 对等节点、复制集与参数 {#peers-replication-sets-and-settings}

`spock.peer_status` 列出 `spock.node` 中的所有节点及其接口（隐藏密码）、是否为本地节点，以及将该节点变更传入本地的订阅、订阅状态和延迟。一个节点若对应多个订阅，每个订阅各占一行。

`spock.replication_set_status` 列出本地节点的各个复制集及其复制标志、表数、序列数，以及包含该复制集的本地订阅数。尚未加入任何复制集的表可以在 `spock.tables` 中按 `set_name IS NULL` 查找。

`spock.settings` 显示所有 `spock.*` 参数和复制所依赖的核心配置（`wal_level`、`max_worker_processes`、`max_replication_slots`、`max_wal_senders`、`max_slot_wal_keep_size`、`track_commit_timestamp`、`shared_preload_libraries`、walsender 与 walreceiver 超时、同步提交配置以及 `logical_decoding_work_mem`），包括单位、配置来源及是否等待重启。参数中连接串的密码会隐藏。

## 事件 {#events}

`spock.events` 是共享内存中的环形事件历史，按从旧到新的顺序显示近期状态变化。`spock.event_history_size` 决定保存的条数。postmaster 重启会清空历史，`spock.reset_events()` 可清空当前数据库的事件。

| 列 | 说明 |
|--------|-------------|
| `event_id` | 每记录一个事件就递增一，已分配的编号不再使用。 |
| `event_time`, `event_type`, `severity` | 事件时间、类型和级别（`info`、`warning` 或 `error`）。 |
| `sqlstate` | `worker_error` 或 `stream_error` 事件对应的 SQLSTATE。 |
| `subscription_id`, `subscription_name`, `provider_node` | 相关订阅（如有）及其变更的来源节点。 |
| `pid` | 报告事件的进程。 |
| `lsn` | 与事件相关的提供方 LSN，例如数据流起始位置、跳过／丢弃／失败事务的提交 LSN，或禁用订阅时的位置。工作进程启动等生命周期事件为 NULL。 |
| `detail` | 简短说明。 |
{.wide .expand}

事件类型如下。

| 类型 | 记录时机 |
|------|---------------|
| `node_created`, `node_dropped` | `spock.node_create()` 或 `spock.node_drop()` 完成。 |
| `subscription_created`, `subscription_dropped` | 创建或删除订阅。 |
| `subscription_enabled`, `subscription_disabled` | 管理员或异常处理流程启用或禁用订阅。 |
| `subscription_altered` | 接口、复制集、`skip_lsn`、选项或同步请求发生变化。 |
| `worker_started`, `worker_stopped`, `worker_failed` | 管理、应用或同步进程启动、正常退出或出错退出。 |
| `worker_error` | 应用或同步进程报错。详细信息包含带 DETAIL 和 CONTEXT 的错误消息。 |
| `provider_connected`, `provider_disconnected` | 已连接指定提供方（附起始 LSN），或连接中断（附错误）。 |
| `transaction_skipped`, `transaction_discarded` | 通过 `sub_skip_lsn` 跳过某一事务，或按 `transdiscard` 丢弃事务。 |
| `sync_started`, `sync_finished`, `sync_failed` | 表的初始复制。`sync_failed` 携带使复制中止的错误。下一个负责该表的同步进程会再记录一次 `sync_failed`，说明因前次失败已放弃该表，不再尝试。 |
| `slot_created`, `stream_started`, `stream_stopped`, `stream_error` | 提供方创建 Spock 槽、walsender 开始向订阅方传输（详情含订阅方地址、Spock 版本及协议，`lsn` 为槽位置）、停止传输（walsender 退出时记录，订阅方断开或重启也会产生此事件），或解码时出错。 |
| `apply_paused`, `apply_resumed` | 调用 `spock.pause_apply_workers()` 或 `spock.resume_apply_workers()`。 |
| `repair_mode_enabled`, `repair_mode_disabled` | 调用 `spock.repair_mode()`。 |
| `extension_upgraded` | 管理进程将已安装扩展更新到共享库版本。 |
{.wide .expand}

报告代码运行时就记录事件，无论外围事务最终是否提交。

```sql
SELECT event_time, event_type, subscription_name, detail
  FROM spock.events
 WHERE severity <> 'info'
 ORDER BY event_id DESC
 LIMIT 20;
```

## 完整报告 {#the-full-report}

`spock.node_report()` 逐节返回节点的文本报告，包括系统状态、已安装扩展、设置、节点状态、对等节点、订阅及其统计、工作进程、待处理异常、复制槽、复制集、未加入任何复制集的表、表同步、各节点对的延迟、最近异常、最近冲突处理和最近事件。宽视图按每行一个区块显示，列表输出为对齐的表格。若某节查询失败，例如角色没有 `node_status` 所用函数的 `EXECUTE` 权限，该节只显示一行错误，其余部分照常生成。

```sql
SELECT * FROM spock.node_report();
SELECT * FROM spock.node_report(200);   -- list up to 200 events, exceptions and resolutions
```

在 `psql` 中可先运行 `\pset format unaligned` 和 `\o report.txt`，再调用报告函数，生成可附在工单上的纯文本文件。报告不包含密码。

`spock.report_section(title, query, expanded)` 是报告使用的格式化函数，也可以同样的形式呈现任意查询。

## 常见操作 {#common-tasks}

下列查询可以回答以往需要查阅服务器日志的问题。若结果较宽，可在 `psql` 中用 `\x` 打开扩展显示。

### 节点是否健康？ {#is-the-node-healthy}

一行就能看出概况。如果 `workers_restart_pending` 非零、`subscriptions_enabled` 与 `subscriptions_replicating` 不相等，或 `last_error_event_time` 显示近期有预期之外的错误，都值得进一步检查。

```sql
SELECT node_name, extension_update_pending,
       subscriptions_enabled, subscriptions_replicating,
       workers_restart_pending, apply_paused, readonly_mode,
       pg_size_pretty(max_retained_wal_bytes) AS retained_wal,
       max_replication_lag, last_error_event_time
  FROM spock.node_status;
```

### 为什么订阅没有在复制？ {#why-is-a-subscription-not-replicating}

先看订阅对应的行。`status` 指示是否有工作进程；`worker_status` 和 `worker_terminated_at` 显示进程是否因失败而等待重启；`last_error_message` 给出最近的错误，无须先打开日志。

```sql
SELECT subscription_name, status, enabled, worker_status,
       worker_terminated_at, worker_restart_delay,
       in_exception_handling, last_apply_error, last_error_message
  FROM spock.subscription_status
 WHERE status <> 'replicating';
```

再按从新到旧的顺序读取该订阅的事件。

```sql
SELECT event_time, event_type, severity, detail
  FROM spock.events
 WHERE subscription_name = 'sub_n2_n1'
 ORDER BY event_id DESC
 LIMIT 20;
```

如果订阅被异常处理流程禁用，会记录 `subscription_disabled` 事件，详情为 `disabled by exception handling`，`lsn` 是失败事务在来源节点上的 LSN。出错的元组可在 `spock.exception_log` 中找到。

### 工作进程是否被阻塞或发生死锁？ {#is-a-worker-blocked-or-deadlocking}

等待锁时，工作进程显示 `wait_event_type = 'Lock'`，`blocked_by_pids` 和 `blocking_query` 会显示持锁会话及查询。死锁或锁等待超时会中止事务，工作进程随之退出并重新启动，同时按类型记录错误。

```sql
SELECT worker_type, subscription_name, wait_event_type, wait_event,
       blocked_by_pids, blocking_pid, blocking_xact_start, blocking_query
  FROM spock.worker_status
 WHERE blocked_by_pids IS NOT NULL;

SELECT subscription_name, deadlocks, lock_timeouts,
       constraint_violations, resource_errors,
       last_error_sqlstate, last_apply_error, last_error_message
  FROM spock.subscription_stats;
```

### 工作进程是否在反复重启？ {#is-a-worker-restarting-in-a-loop}

应用工作进程每次尝试都崩溃时，`worker_starts` 与 `worker_failures` 会同步增长。事件历史可显示间隔及原因。同步工作进程有独立的计数器，因此重新同步大量表不会在这里被误判为反复重启。

```sql
SELECT subscription_name, worker_starts, worker_failures,
       last_worker_failure, last_error_message
  FROM spock.subscription_stats
 WHERE worker_failures > 0;

SELECT event_time, event_type, detail
  FROM spock.events
 WHERE event_type IN ('worker_started', 'worker_failed', 'worker_error')
 ORDER BY event_id DESC
 LIMIT 30;
```

### 夜间发生了什么变化？ {#what-changed-overnight}

非例行事件的严重级别高于 `info`。

```sql
SELECT event_time, event_type, severity, subscription_name, detail
  FROM spock.events
 WHERE event_time > now() - interval '12 hours'
   AND severity <> 'info'
 ORDER BY event_id;
```

启停订阅、切换接口、更改复制集、`sub_skip_lsn`、暂停与恢复、修复模式及扩展升级等都会产生 `info` 或 `warning` 事件，`pid` 中为操作者的后端 PID。

### 相对各提供方落后多少？ {#how-far-behind-is-each-provider}

```sql
SELECT subscription_name, provider_node,
       pg_size_pretty(replication_lag_bytes) AS lag_bytes,
       replication_lag, remote_commit_ts, received_lsn, origin_lsn
  FROM spock.subscription_status
 ORDER BY replication_lag_bytes DESC NULLS LAST;
```

`replication_lag_bytes` 是提供方已写入、本节点尚未应用的 WAL 量。`replication_lag` 是最近已应用事务在提供方提交与在本节点应用之间的时间差。两者均取自 `spock.progress`，也可在 `spock.lag_tracker` 中按节点对查询。

### 提供方是否有复制槽阻碍 WAL 回收？ {#is-a-slot-holding-back-wal-on-the-provider}

在提供方运行下列查询。某槽 `active = false` 或 `retained_wal_bytes` 持续增长，通常表示订阅方已离线或进度滞后。

```sql
SELECT slot_name, active, client_name, state,
       pg_size_pretty(retained_wal_bytes) AS retained,
       pg_size_pretty(pending_wal_bytes) AS pending,
       replay_lag, last_reply_time, wal_status
  FROM spock.slot_status
 ORDER BY retained_wal_bytes DESC;
```

### 初始同步完成了吗？ {#is-the-initial-synchronization-finished}

```sql
SELECT subscription_name, schema_name, table_name, sync_kind, sync_status
  FROM spock.table_sync_status
 WHERE sync_status NOT IN ('ready', 'synchronized');
```

未指定表的行代表订阅整体。正在运行的同步工作进程见 `spock.worker_status`，其中 `worker_type = 'sync'`，同时列出正在复制的表。

### 扩展是否已升级？ {#did-the-extension-get-upgraded}

`spock.node_status` 比较已加载的共享库版本与已安装扩展版本。升级二进制文件后，管理进程下次启动时会更新扩展并记录事件。

```sql
SELECT spock_version, extension_version, extension_update_pending
  FROM spock.node_status;

SELECT event_time, detail
  FROM spock.events
 WHERE event_type = 'extension_upgraded';
```

### 开始新一轮测量 {#starting-a-fresh-measurement}

计数器和事件自 postmaster 启动后积累。在基准测试前或故障修复后重置，可单独观察后续活动。

```sql
SELECT spock.reset_subscription_stats();   -- all subscriptions
SELECT spock.reset_subscription_stats(sub_id)
  FROM spock.subscription WHERE sub_name = 'sub_n2_n1';
SELECT spock.reset_events();
```

每张表的元组计数器需另用 `spock.reset_channel_stats()` 清零。

### 从外部监控 {#watching-from-outside}

这些视图均可用 SQL 查询，任何监控代理都可轮询。按 `event_id` 轮询 `spock.events` 即可只取新行。如果事件编号有空缺，说明相对于轮询间隔，`spock.event_history_size` 太小，有历史已被淘汰。`spock.get_monitor_summary()` 显示事件环形缓冲区和计数表的占用情况。只读视图及所调用函数的权限已授予 `pg_monitor`，该角色还需要对模式的 `USAGE` 权限。

```sql
GRANT pg_monitor TO monitoring_role;
GRANT USAGE ON SCHEMA spock TO monitoring_role;
```

本版本授予 `spock` 模式的 `USAGE` 也意味着可以调用 Spock 管理函数，因此只应授予可信角色，改变状态的函数应视为需要超级用户权限。`pg_monitor` 的成员不能重置计数或事件，`spock.reset_events()` 和 `spock.reset_subscription_stats()` 仍仅限超级用户。`node_report()` 中读取 `spock.tables`、`spock.lag_tracker`、`spock.exception_log` 和 `spock.resolutions` 的各节还需要各对象的 `SELECT` 权限，上述授权不包含这些权限，缺失时相应章节各显示一行错误。

## 底层函数 {#underlying-functions}

视图建立在返回共享内存原始内容的函数之上。需要未经过滤的行时，工具可以直接使用这些函数。

| 函数 | 返回值 |
|----------|---------|
| `spock.get_worker_status()` | 集群中所有工作进程槽，附 `database_id`。 |
| `spock.get_events()` | 历史中的全部事件，附 `database_id`。限超级用户或 `pg_monitor`。 |
| `spock.get_apply_stats()` | 当前数据库所有订阅的计数器。限超级用户或 `pg_monitor`。 |
| `spock.get_slot_groups()` | 已有 walsender 加入的复制槽组。 |
| `spock.get_monitor_summary()` | 共享内存数据结构的容量及使用量。 |
| `spock.get_system_info()` | 主机名、操作系统、CPU、内存、平均负载、数据卷及 WAL 卷空间、postmaster 启动时间、PostgreSQL 和 Spock 版本。限超级用户或 `pg_monitor`；读取数据目录还需要 `pg_read_all_settings`。 |
| `spock.get_pending_exceptions()` | 异常处理中正在重试的事务，附首次错误和失败变更在事务中的位置。限超级用户或 `pg_monitor`。 |
| `spock.replication_origin_status()` | 各复制来源及其远端进度，与超级用户在 `pg_replication_origin_status` 中看到的一样。限超级用户或 `pg_monitor`。 |
| `spock.reset_events()` | 清空当前数据库的事件历史。仅限超级用户。 |
| `spock.reset_subscription_stats(subid)` | 重置一个或所有订阅的活动及冲突计数器。仅限超级用户。 |
| `spock.redact_dsn(text)` | 返回已隐藏密码的连接串。 |
{.wide .expand}

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/node_monitoring.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
