---
title: Spock 节点监控：spock_monitor 子系统设计
description: 本文档的 Word 版本以 spock-monitor-design.docx 为名保存在上游同一目录中。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/specs/spock-monitor-design.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---

**日期：** 2026-09-23
**状态：** 已实现，通过回归测试
**组件：** `src/spock_monitor.c`、`include/spock_monitor.h`
**PostgreSQL：** 15 至 19

本文档的 Word 版本以 `spock-monitor-design.docx` 为名保存在上游同一目录中。

## 1. 概述 {#1-summary}

Spock 集群的运维人员过去必须查看 PostgreSQL 服务器日志，才能回答一些日常问题：所有订阅是否都在复制、工作进程夜间是否重启、订阅为什么被禁用、复制槽积压了多少 WAL、扩展是否升级。系统目录和现有统计视图描述配置及累计计数，却不记录状态变化或故障。

监控子系统将状态变化记录为事件，在共享内存中维护各订阅的活动计数器，并通过 `spock` 模式下的十一个视图，将这些信息与工作进程、复制槽及复制进度一起提供出来。查询 `spock.node_status` 或 `spock.subscription_status` 即可了解节点的完整情况；`spock.events` 则提供近期历史。该模块还统一容纳所有监控相关的 C 代码，包括通道计数器、应用组进度函数和复制槽确认等待功能。

## 2. 目标与非目标 {#2-goals-and-non-goals}

### 目标 {#goals}

* 日常运维无需再翻查日志：所有值得关注的状态变化都能查询。
* 每个节点、订阅、工作进程和复制槽各占一行，列名无需另附说明。
* 应用热路径的开销低：每条消息只需要一个自旋锁和几次整数加法，不写系统目录，也不产生 WAL。
* 错误路径安全：记录错误绝不能分配内存、阻塞或抛出错误。
* 所有支持的 PostgreSQL 版本使用同一份源码；PG18 冲突计数器等特定版本的数据，在不支持的版本上返回 NULL。
* 所有监控代码集中在一个模块中，遵循 PostgreSQL 的命名和布局惯例。

### 非目标 {#non-goals}

* 在 postmaster 重启后保持持久性。事件和计数器仅存于共享内存；系统目录和 pgstat 仍承担持久化存储职责。
* 事务语义。事件在报告代码执行时记录，与所在事务是否提交无关。
* 集群范围的汇总。每个节点只报告自身情况；所有节点的整体视图由外部工具读取各节点视图后汇总。

## 3. 架构 {#3-architecture}

子系统分为三层：由 spock 进程写入的共享内存结构、读取这些结构并返回行的 C 函数，以及将这些行与系统目录、`pg_stat_replication` 和 `pg_stat_activity` 等内核视图联接的 SQL 视图。

| 层 | 元素 | 负责模块 |
|-------|----------|-------|
| 共享内存 | 事件环形缓冲区（`SpockMonitorShmem`）、各订阅计数器（`SpockMonitorStatsHash`） | `spock_monitor.c`，由 `spock_shmem.c` 分配 |
| 事件生产者 | 工作进程挂接与分离、应用循环、同步工作进程、输出插件、节点和订阅管理函数、异常处理器、扩展管理器、`emit_log_hook` | 每处调用一次 |
| SQL 函数 | `get_worker_status`、`get_events`、`get_apply_stats`、`get_slot_groups`、`get_monitor_summary`、`reset_events`、`reset_subscription_stats`、`get_channel_stats`、`reset_channel_stats`、`apply_group_progress`、`wait_slot_confirm_lsn` | `spock_monitor.c` |
| 视图 | `system_status`、`node_status`、`subscription_status`、`subscription_stats`、`worker_status`、`slot_status`、`peer_status`、`replication_set_status`、`settings`、`table_sync_status`、`events` | `sql/spock--6.0.0.sql` 和 5.x 升级脚本 |
{.wide .expand}

生产者从不拼装 SQL，也不访问系统目录。它们调用 `spock_monitor.h` 中声明的少数几个函数之一，在持锁期间将固定大小的数据复制到共享内存。读取者取得每个条目的一致副本，然后在不持有任何自旋锁的情况下构造元组。

## 4. 共享内存 {#4-shared-memory}

### 4.1 事件环形缓冲区 {#41-event-ring}

事件存放在固定大小的环形缓冲区中，该缓冲区位于名为 `spock monitor` 的单次 `ShmemInitStruct` 分配内。容量由 GUC 参数 `spock.event_history_size` 指定（默认 1024，`PGC_POSTMASTER`）。

```c
typedef struct SpockMonitorEvent
{
    uint64      event_id;      /* increases by one, never reused */
    TimestampTz event_time;
    SpockMonitorEventType event_type;
    Oid         dboid;         /* database of the reporting process */
    Oid         subid;         /* subscription, or InvalidOid */
    int         pid;
    int         sqlerrcode;    /* SQLSTATE of an error event, else 0 */
    XLogRecPtr  lsn;           /* origin LSN, if any */
    char        detail[512];
} SpockMonitorEvent;
```

头部保存 LWLock、共享内存初始化时间（报告为 `spock_started_at`）、下一个事件 ID，以及头位置和计数索引。缓冲区已满时，追加事件会推进头位置，丢弃最旧的事件。重置后事件 ID 仍持续递增，使轮询者既能发现新事件，也能发现缺失区间。该缓冲区在集群范围内共享；视图按当前数据库过滤，同时保留不属于任何数据库的事件，例如监督进程的事件。

每种事件类型的固定名称和严重级别都存放在以枚举值为索引的表中，因此添加一种类型只需添加一个枚举成员和一行表项。严重级别为 `info`、`warning` 和 `error`。`warning` 包括即使由用户主动请求、运维人员也需要知晓的状态变化，例如禁用订阅、开启修复模式或跳过事务。

### 4.2 各订阅计数器 {#42-per-subscription-counters}

计数器存放在以 `(dboid, subid)` 为键的固定大小共享哈希表中，容量为 `max(64, 4 * max_worker_processes)` 个条目。这个倍数为禁用的订阅留出了空间，使其停止期间仍能保留历史。

```c
typedef struct SpockMonitorStatsEntry
{
    SpockMonitorStatsKey key;
    int64       counter[SPOCK_MONITOR_NUM_COUNTERS];
    TimestampTz counter_time[SPOCK_MONITOR_NUM_COUNTERS];
    XLogRecPtr  last_error_lsn;
    int         last_error_sqlerrcode;
    int         last_error_pid;
    char        last_error_message[512];
    TimestampTz stats_reset;
    slock_t     mutex;
} SpockMonitorStatsEntry;
```

每个计数器都携带最后一次递增的时间。仅凭这条规则，视图就能提供 `last_worker_start`、`last_provider_connect`、`last_xact_applied` 和 `last_apply_error` 列，无需单独设置字段；读取逻辑也可保持通用：`spock_get_apply_stats()` 中的两张小表将计数器分别映射到计数列和时间戳列，并在编译时对照列枚举检查。

| 计数器 | 递增时机 |
|---------|------------------|
| `worker_starts` | 应用工作进程挂接到其共享内存槽位。 |
| `worker_failures` | 应用工作进程因错误退出后分离。 |
| `sync_worker_starts`、`sync_worker_failures` | 同步工作进程发生上述对应事件，从而区分重新同步与应用工作进程重启。 |
| `provider_connects` | 应用工作进程中的 `START_REPLICATION` 成功。 |
| `provider_disconnects` | `apply_work()` 将错误归类为连接丢失。同步工作进程的连接失败会记录为事件和最后错误，但不计入此处，以使这两个计数器相互对应。 |
| `idle_timeouts` | `spock.apply_idle_timeout` 强制重连。 |
| `messages_received`、`bytes_received` | 从流中读取了一条数据消息。 |
| `xacts_applied` | 远端事务在本地提交。 |
| `xacts_skipped` | 通过 `sub_skip_lsn` 跳过事务。 |
| `xacts_discarded` | 在 `transdiscard` 下丢弃事务。 |
| `apply_errors`、`sync_errors` | 应用或同步工作进程中抛出 ERROR（第 6 节）。 |
| `deadlocks`、`lock_timeouts`、`constraint_violations`、`resource_errors` | 上述错误按 SQLSTATE 分类。 |
| `tables_synced` | 同步工作进程完成一张表的同步，且未发生故障。 |
{.wide .expand}

工作进程挂接时，将指向自身条目的指针缓存在 `MySpockMonitorStats` 中。`HASH_FIXED_SIZE` 共享哈希表中的条目从不移动，因此该指针在进程存活期间始终有效。这样，每次计数只需要一个自旋锁、一次加法和一个时间戳。仅记录事件的后端进程不访问该哈希表。

订阅 ID 来自循环序列，因此可能被复用。每个条目记录挂接到它的工作进程数。删除订阅时，如果没有工作进程挂接，就立即删除条目；否则只标记为已删除，等最后一个工作进程分离时再删除，避免工作进程通过指针写入已释放的元素。如果 ID 被复用，新的工作进程挂接到已标记删除的条目时会将其重置。

### 4.3 锁 {#43-locking}

* `spock_monitor` 锁组中的一个 LWLock 保护环形缓冲区和哈希表结构。各条目另有自旋锁保护其计数器。
* 监控锁处于锁获取顺序的末端：持有它时不再获取其他锁。可以在持有 `SpockCtx->lock` 时获取监控锁，反向顺序则不允许。
* 错误报告路径使用 `LWLockConditionalAcquire`；如果锁忙就跳过该事件，因此错误报告绝不会阻塞。
* 读取者仅在将环形缓冲区或条目复制到本地内存时持有监控锁，避免格式化结果时妨碍只尝试获取锁的错误报告路径。

## 5. 监测点 {#5-instrumentation-points}

每个生产者在原本已记录状态变化日志的位置添加一次调用，确保事件始终与日志行一致。

| 事件类型 | 调用位置 |
|------------|-----------|
| `node_created`、`node_dropped` | `spock_create_node()`、`spock_drop_node()` 中系统目录变更之后 |
| `subscription_created`、`subscription_dropped` | `spock_create_subscription()`、`spock_drop_subscription()` |
| `subscription_enabled`、`subscription_disabled` | `spock_alter_subscription_enable()`、`spock_alter_subscription_disable()`，以及异常处理器中的 `spock_disable_subscription()` |
| `subscription_altered` | 接口变更、添加和移除复制集、`skip_lsn`、选项、同步和重新同步表 |
| `worker_started`、`worker_stopped`、`worker_failed` | `spock_worker_attach()` 和 `spock_worker_detach()`；故障详情携带最后记录的错误消息 |
| `worker_error` | `emit_log_hook`，针对 spock 工作进程中的任何 ERROR 或 FATAL |
| `provider_connected`、`provider_disconnected` | `spock_start_replication()`；`apply_work()` 的连接丢失分支 |
| `transaction_skipped`、`transaction_discarded` | `stop_skipping_changes()`；`handle_commit()` 的 `transdiscard` 分支 |
| `sync_started`、`sync_finished`、`sync_failed` | `spock_sync_main()` 和 `spock_sync_worker_finish()` |
| `slot_created`、`stream_started`、`stream_stopped` | 设置或未设置 `is_init` 时的 `pg_decode_startup()`；`pg_decode_shutdown()` |
| `apply_paused`、`apply_resumed` | `spock_pause_apply_workers()`、`spock_resume_apply_workers()` |
| `repair_mode_enabled`、`repair_mode_disabled` | `spock_repair_mode()` |
| `extension_upgraded` | `spock_manage_extension()` 中 `ALTER EXTENSION UPDATE` 之后 |
{.wide .expand}

工作进程的启动和停止在通用挂接与分离代码中记录，因此两个调用位置即可覆盖管理进程、所有应用工作进程和所有同步工作进程。分离钩子在获取 `SpockCtx->lock` 之前运行，使锁顺序保持简单。

## 6. 错误捕获 {#6-error-capture}

模块通过 `spock.c` 已安装的 `emit_log_hook` 挂钩捕获错误，无需在每个错误位置设置监测点。每次报告都会调用 `spock_monitor_report_error()`，并应用以下规则：

1. 除非进程是 spock 工作进程（已设置 `MySpockWorker`），或是运行 spock 输出插件的 walsender，并且已经挂接共享内存，否则忽略。
2. 忽略低于 ERROR 的级别，以及 PANIC 和更高级别；PANIC 路径不得获取锁。
3. 将连接类错误（连接失败、管理员关闭、当前无法连接及相关错误码）视为对端丢失，绝不作为应用错误。在工作进程中，钩子将它们记录为 `provider_disconnected`，并把消息保留为最后错误，涵盖没有处理器捕获的连接或 START_REPLICATION 阶段的失败。`apply_work()` 的连接丢失分支使用同一判断条件，在重新抛出错误前通过同一函数报告；它会标记重新抛出，以免钩子再次计数。在 walsender 中，此类错误表示订阅者离开，不作任何记录。
4. 在 walsender 中记录 `stream_error` 事件，携带复制槽名称、SQLSTATE 和消息。输出插件在启动时标记进程，关闭时清除标记。只有 walsender 会被标记：通过 SQL 函数解码复制槽的普通后端进程，在解码失败时不会收到关闭调用，而其后续错误不得被报告为流错误。
5. 对应用和同步工作进程，递增 `apply_errors` 或 `sync_errors` 以及对应类别的计数器（死锁、锁超时、约束违例、资源错误），并将消息、SQLSTATE、pid 和当前复制源 LSN 保存为最后错误。
6. 采用条件式获取锁，记录包含消息和 SQLSTATE 的 `worker_error` 事件。

保存的消息由错误消息及其后的 DETAIL 和 CONTEXT 行组成，因此约束违例会包含出错行和应用上下文。函数有重入保护，并且不分配内存：文本使用 `snprintf` 格式化到固定缓冲区中。

被 `PG_CATCH` 捕获的 ERROR 从不会输出：PostgreSQL 在 `EmitErrorReport()` 之前执行 longjmp，应用工作进程的处理器会复制并清除错误。因此，钩子只能看到导致工作进程终止的错误。`apply_work()` 中有两条路径会吞掉错误：触发重放的首次异常，以及 `sub_disable` 路径；它们自行对复制的 `ErrorData` 调用 `spock_monitor_report_error()`。重新抛出错误的路径则交由钩子处理，确保每个错误只计数一次。在 `sub_disable` 下，重放以一个请求禁用的合成错误结束；工作进程记得该事务的首次错误已报告，因而不会报告这个合成错误。`discard` 重放期间的行级错误不再重复计数，因此 `apply_errors` 统计失败的事务数，而非失败的行数。

## 7. SQL 接口 {#7-sql-surface}

### 7.1 函数 {#71-functions}

函数返回原始共享内存行，供工具调用。返回集合的函数使用 `InitMaterializedSRF` 和 OUT 参数；C 代码通过断言检查列数是否与枚举一致。

| 函数 | 返回内容 |
|----------|---------|
| `spock.get_worker_status()` | 集群中的所有工作进程槽位和监督进程，带有 `database_id` |
| `spock.get_events()` | 环形缓冲区中的所有事件，最旧的在前，带有 `database_id` |
| `spock.get_apply_stats()` | 当前数据库中所有订阅的计数器，包含 PG18 冲突计数器 |
| `spock.get_slot_groups()` | 挂接了 walsender 的复制槽组 |
| `spock.get_monitor_summary()` | 一行：启动时间、监督进程 pid、槽位和容量使用情况 |
| `spock.get_system_info()` | 一行：主机名、操作系统、CPU、内存、平均负载、数据目录和 `pg_wal` 的 `statvfs()` 结果、postmaster 启动时间、PostgreSQL 和 spock 版本 |
| `spock.get_pending_exceptions()` | 已记录错误的异常日志槽位，即正在重试的事务，附带 `failed_action_number`，表示出错变更在事务中的位置 |
| `spock.report_section(title, query, expanded)` | 以文本形式返回查询的行，值采用 PostgreSQL 文本格式 |
| `spock.node_report(recent)` | 整个节点的文本报告，每个视图占一节 |
| `spock.reset_events()` | 清空环形缓冲区；ID 继续递增 |
| `spock.reset_subscription_stats(subid)` | 重置一个或所有订阅的活动计数器，以及 PG18 上的冲突计数器 |
| `spock.redact_dsn(text)` | 隐藏密码后的连接字符串，支持关键字和 URI 形式 |
{.wide .expand}

### 7.2 视图 {#72-views}

视图按展示内容命名：`*_status` 表示状态，`*_stats` 表示计数器。列名使用完整单词，不用缩写，同一概念在所有位置都使用相同词语（`subscription_name`、`provider_node`、`worker_pid`、`replication_lag_bytes`）。

| 视图 | 行数 | 数据来源 |
|------|------|------------|
| `spock.system_status` | 恰好一行 | `get_system_info()`、`pg_stat_activity`、`pg_prepared_xacts`、`pg_stat_replication`、`pg_database`、`pg_stat_database`、`pg_stat_archiver`、`spock.wal_size_bytes()` |
| `spock.node_status` | 恰好一行 | `get_monitor_summary()`、`local_node`、`pg_extension`、对其他视图的聚合、`spock.wal_size_bytes()` |
| `spock.subscription_status` | 每个订阅一行 | `subscription`、`node`、`node_interface`、`local_sync_status`、`get_worker_status()`（横向联接，优先选择运行中的工作进程）、`pg_stat_activity`、`progress`、`replication_origin_status()`、`subscription_stats` |
| `spock.subscription_stats` | 每个订阅一行 | `get_apply_stats()` 和 `channel_summary_stats`，计数器空值按零处理 |
| `spock.worker_status` | 每个工作进程一行 | `get_worker_status()`、`pg_stat_activity`，以及用于找出持有该工作进程正在等待的锁的会话的 `pg_blocking_pids()` |
| `spock.slot_status` | 每个 spock 复制槽一行 | `pg_replication_slots`、`pg_stat_replication`、`get_slot_groups()`、当前 WAL 位置或重放位置 |
| `spock.table_sync_status` | 每条同步记录一行 | `local_sync_status`，类型和状态以可读形式显示 |
| `spock.peer_status` | 每个节点与订阅组合一行 | `node`、`node_interface`、`subscription_status` |
| `spock.replication_set_status` | 每个复制集一行 | `replication_set`，以及其中表、序列和订阅的数量 |
| `spock.settings` | 每个参数一行 | `pg_settings`、spock 参数及内核复制参数，DSN 已脱敏 |
| `spock.events` | 每个事件一行 | `get_events()`、`subscription`，以及用于取得提供者名称的 `node` |
{.wide .expand}

订阅的状态文本在 SQL 中按与 `spock.sub_show_status()` 相同的规则计算：工作进程运行时为 `replicating`、`initializing` 或 `unknown`，否则为 `disabled` 或 `down`。在视图中计算状态，可以使 `node_status` 在尚未创建本地节点时仍可用；此时调用该函数则会报错。

复制槽视图只使用 PostgreSQL 15 起就存在于 `pg_replication_slots` 中的列，因为所有版本共用一份 SQL 脚本。在备库上，它回退到 `pg_last_wal_replay_lsn()`，因此在恢复期间也不会报错。

### 7.3 报告 {#73-the-report}

`spock.node_report()` 是一个 plpgsql 函数，对每个视图调用一次 `spock.report_section()`。格式化器执行查询两次：先通过 `row_to_json` 按查询顺序取得列名，再将所有列转换为文本，使值按 PostgreSQL 的打印格式呈现，而非 JSON 格式。每一节的查询都在独立的异常块中运行，因此某个视图失败时只产生一行错误，不会中止整份报告。密码绝不会出现：视图已对连接字符串脱敏，`spock.settings` 也会对 DSN 参数脱敏。

异常处理器为每个订阅保留一个共享槽位，保存正在处理的事务的提交 LSN 及其首次错误。`spock.get_pending_exceptions()` 仅报告存在错误的槽位，因为每个事务都会设置 LSN，单有 LSN 并不能说明发生了错误。

## 8. 兼容性与升级 {#8-compatibility-and-upgrade}

* 同一段 SQL 同时附加到 `spock--6.0.0.sql` 和 `spock--5.0.14--6.0.0.sql`。视图引用的所有系统目录列自 5.0.6 起就已存在，因此升级后的节点与全新安装具有相同对象。
* 为兼容现有调用者，保留 `spock.get_apply_worker_status()`，将其实现为基于 `spock.get_worker_status()` 的 SQL 函数，返回 5.x 的列和行。其 C 符号保留为报错的桩函数，因为从 5.x 执行 pg_upgrade 时，会先重建旧 C 绑定，然后扩展更新才将其替换。
* 移除 `spock_monitoring.c`。`spock.wait_slot_confirm_lsn()`、`spock.get_channel_stats()`、`spock.reset_channel_stats()` 和 `spock.apply_group_progress()` 保留原 SQL 定义及 C 符号，现在位于 `spock_monitor.c`。
* `spock.reset_subscription_stats()` 保留 SQL 定义和 C 符号，现有升级脚本无需修改；但现在会重置两组计数器，并且在 PostgreSQL 18 之前的版本上不再报错。
* 当 `PG_VERSION_NUM >= 180000` 时，通过 pgstat 条目读取冲突计数器，否则为 NULL。
* 共享内存增加量为环形缓冲区加哈希表的大小。`SpockMonitorStatsEntry` 为 800 字节，主要由 512 字节的 `last_error_message` 和两个按计数器组织的数组占用。因此，每个受跟踪订阅的哈希开销约为该大小加上 dynahash 开销，条目数上限为 `max(64, 4 * max_worker_processes)`。
  `SpockMonitorEvent` 为 560 字节，主要由 512 字节的 `detail` 占用，因此环形缓冲区需要 `spock.event_history_size * 560` 字节：默认 1024 条时为 560 kB，提高设置后可达到一兆字节或更多。请据此估算共享内存，而不要只看事件数量。

## 9. 测试 {#9-testing}

回归测试 `tests/regress/sql/monitor.sql` 在 `basic` 之后运行。在提供者上，它检查 `node_status`、`worker_status`、`slot_status` 及提供者侧事件；在订阅者上，它检查 `subscription_status`、`worker_status`、`table_sync_status`、实际流量产生后的 `subscription_stats`、订阅创建和工作进程启动事件、两个重置函数，并验证禁用和启用订阅会产生预期事件以及可从计数器中观察到的工作进程重启。不同运行之间会变化的值只作比较，不打印输出。全部 41 项测试在 PostgreSQL 18 上通过。

## 10. 限制与后续工作 {#10-limitations-and-future-work}

* 这些视图及其调用的函数（`get_system_info()`、`get_events()`、`get_apply_stats()`、`get_pending_exceptions()`、`replication_origin_status()`，后者替代仅限超级用户访问的 `pg_replication_origin_status`）均向 `pg_monitor` 授权；超级用户或该角色的成员可以读取。
  `wal_size_bytes()` 仍允许任何角色调用，因为 WAL 总大小并非敏感信息。重置函数仅限超级用户。
* 订阅统计哈希表最多容纳 `max(64, 4 * max_worker_processes)` 个条目。超过该上限后，`spock_monitor_attach_stats()` 返回 NULL 并记录日志；工作进程继续运行，订阅也正常工作，但不再记录其计数器：`spock.subscription_stats` 仍保留该订阅的行，所有计数器读作 0，所有时间戳为 NULL，因此超出容量的订阅看起来像是空闲，而非未被记录。
  `spock.node_status.channel_stats_full` 报告通道计数器哈希表的同类情况。
* 环形缓冲区在集群范围内共享，因此活动频繁的数据库可能挤掉安静数据库的事件。为每个数据库设置独立缓冲区可以消除这一问题，但会增加共享内存开销。
* postmaster 重启后，事件和计数器都会丢失。如果需要跨重启保留历史，可以由后台工作进程定期将事件追加到 spock 系统目录表中。
* 不显示 PostgreSQL 17 新增的 `pg_replication_slots` 列（`failover`、`invalidation_reason`、`inactive_since`）；这需要按版本条件定义视图。
* 提供者上的复制集变更（添加或移除表）不记录为事件；这些变更可从系统目录中看到，增加两个调用位置即可记录它们。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/specs/spock-monitor-design.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
