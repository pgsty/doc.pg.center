---
title: Spock 发布说明
description: Spock 各版本的新功能、缺陷修复、兼容性变更与升级说明。
weight: 140
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_release_notes.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: 发布说明
type: docs
---

## Spock 6.0.0-beta.2 {#spock-600-beta2}

本节列出自 6.0.0-beta.1 以来的变更，供测试 beta 版本的用户参考。大部分条目在下方 6.0.0 说明中有完整介绍。本节将在正式发布时移除。

### 从 beta 1 升级 {#upgrading-from-beta-1}

* Beta 1 和 beta 2 安装的扩展版本均为 `6.0.0`，但两者的系统目录不同，因此在 beta 1 节点上直接执行 `ALTER EXTENSION spock UPDATE` 不会产生任何效果。请改用以下方式更新：

  1. 暂停集群上的 DDL。
  2. 安装 beta 2 二进制文件并重启节点。
  3. 在每个安装了 Spock 的数据库中执行：

     ```sql
     ALTER EXTENSION spock UPDATE TO '6.0.0-beta1-to-beta2';
     ALTER EXTENSION spock UPDATE TO '6.0.0';
     ```

  4. 对每个节点重复，然后恢复 DDL。
  5. 在每个主库上检查所有 Spock 槽是否具有 `failover` 标志：

     ```sql
     SELECT slot_name, failover
     FROM pg_replication_slots
     WHERE plugin = 'spock_output';
     ```

     对仍显示 `false` 的槽，暂停占用它的订阅者，并在主库上执行 `SELECT spock.slot_enable_failover();`。

  第一条命令添加 beta 2 所需对象（`spock.reserved_object` 系统目录及其函数、节点元数据函数和 `spock.node` 上的触发器，以及监控视图、函数及其 `pg_monitor` 授权），移除 `spock.wait_for_apply_worker()`，基于 `spock.get_worker_status()` 重新实现 `spock.get_apply_worker_status()`，在从 5.x 升级的节点上将 `spock.md5_agg` 标记为并行安全，并为现有槽设置 `failover` 标志。第二条命令仅将版本名称改回 `6.0.0`。

  `failover` 标志在 PostgreSQL 17 和 18 上很重要，因为原生槽同步只会将带标志的槽复制到备库。Beta 1 从 5.x 升级时未为已有槽设置标志，因此从 5.x 升级而来的 beta 1 节点，可能存在备库上缺失、故障切换后不可用的槽。由 6.0.0 创建的槽已具有该标志。第一条命令为其余槽设置标志，但会跳过当时正在使用的槽，并输出含其名称的 NOTICE。PostgreSQL 16 及更早版本，或 PostgreSQL 17 使用 Spock 自身槽同步工作进程时，不使用此标志，可以跳过步骤 5。

  数据库更新之前，AutoDDL、将表添加到复制集及结构同步都会报错 `catalog "spock.reserved_object"
  does not exist`；对端修改 location、country 或 info 时，其应用工作进程也会因缺少 `spock.node_info_apply()` 而失败。在已经具备 beta 2 系统目录的节点上执行这些命令，不会产生变更。这两个更新步骤将在正式发布时移除。
* 从 5.0.x 升级的路径现在从 5.0.14 开始。5.0.11、5.0.12 或 5.0.13 节点仍可通过一次 `ALTER EXTENSION spock UPDATE`，经 5.0.14 完成升级。
* 如果服务器包含 PostgreSQL 对 CVE-2026-6471 的修复，`output_plugin_libraries` 必须列出 `spock_output`。参见下方*升级*。
* 在 PostgreSQL 18 上，beta 1 的 `spock.pg_standby_slot_names` 不起作用，无论显式设置还是由提升的备库继承，都没有效果。Beta 2 开始遵循该设置：`spock.standby_slots_min_confirmed` 采用默认值 `-1` 时，逻辑 walsender 会等待每个指定槽，直到 `wal_sender_timeout` 超时后重新开始，因此只要指定槽缺失，复制就会停滞。安装 beta 2 之前，检查每个 PostgreSQL 18 节点上的该值，创建其指定的槽，或清空设置。

### 节点监控 {#node-monitoring}

这是自 beta 1 以来最大的变更。各视图展示的内容见 6.0.0 说明中的*节点监控视图*。视图的 SELECT 权限及其所读函数的 EXECUTE 权限已授予 `pg_monitor`，但 `spock` 模式的 USAGE 权限未授予，因此监控角色还需获得该权限。

**GUC**

* `spock.event_history_size`（整数，默认 `1024`，范围 16 至 1048576，`POSTMASTER`）：`spock.events` 视图在共享内存中保留的近期事件数量。

**视图**

* `spock.node_status`：一行展示整个节点，包括版本、待升级状态、工作进程及订阅数量、复制槽保留的 WAL、复制延迟和最近事件。
* `spock.peer_status`：已知节点。
* `spock.subscription_status`：每个订阅的配置、状态、负责处理的工作进程、复制位置和延迟，以及最后错误。
* `spock.subscription_stats`：每个订阅的工作进程启动与失败、提供者连接、消息、事务、元组和冲突计数器。
* `spock.worker_status`：监督进程、管理进程、应用工作进程和同步工作进程，包括等待重启的工作进程。
* `spock.slot_status`：提供者侧的 spock 槽及其 walsender、位置、保留的 WAL 和反馈延迟。
* `spock.table_sync_status`：表同步状态。
* `spock.replication_set_status`：复制集。
* `spock.system_status`：磁盘空间、负载、连接、长事务和空闲事务、回卷年龄、归档。
* `spock.settings`：复制所依赖的参数。
* `spock.events`：近期事件历史。

**函数**

* `spock.node_report(recent integer DEFAULT 50) RETURNS SETOF text`：将整个节点汇总为一份文本报告，供支持请求使用，包含主机和版本、已安装扩展、设置、所有监控视图，以及最近的异常、冲突解决记录和事件。
* `spock.replication_origin_status()`：复制源及其进度，允许 `pg_monitor` 读取，而 `pg_replication_origin_status` 仅限超级用户。
* 视图和 `node_report()` 背后的内部函数：`spock.get_worker_status()`、`spock.get_events()`、`spock.reset_events()`、`spock.get_apply_stats()`、`spock.get_slot_groups()`、`spock.get_monitor_summary()`、`spock.get_system_info()`、`spock.get_pending_exceptions()`、`spock.redact_dsn()`、`spock.wal_size_bytes()` 和 `spock.report_section()`。`get_system_info()`、`get_events()`、`get_apply_stats()` 和 `get_pending_exceptions()` 仅允许 `pg_monitor` 执行，`reset_events()` 仅允许超级用户执行。

**变更**

* `spock.get_apply_worker_status()` 现在是基于 `spock.get_worker_status()` 的 SQL 函数，列和行与之前相同。`spock.get_worker_status()` 及 `spock.worker_status` 视图涵盖所有工作进程类型，并提供更多详情。
* `spock.reset_subscription_stats()` 在所有支持的 PostgreSQL 版本上也会重置新增的活动计数器，其 EXECUTE 权限已从 PUBLIC 撤销。

### 其他 GUC 变更 {#other-guc-changes}

**新增**

* `spock.sync_timeout`（秒，默认 `0`，`USERSET`）：节点管理例程中单次等待的时限。`0` 保持各例程内置的限制。
* `spock.non_conflicting_inserts`（布尔值，默认 `off`，`POSTMASTER`）：断言复制的 `INSERT` 绝不会与本地行冲突，使应用工作进程跳过冲突查找和推测插入。
* `spock.failover_slots_naptime`（毫秒，默认 `1000`，`SIGHUP`）和 `spock.failover_slots_feedback_naptime`（毫秒，默认 `10000`，`SIGHUP`）：Spock 故障切换槽工作进程同步槽的频率。此前固定等待 60 秒。
* `spock.failover_slots_recreate_invalidated`（布尔值，默认 `on`，`SIGHUP`）：故障切换槽工作进程是否删除并重建在备库上已失效的同步槽副本。关闭时保持副本原状，并报告一次。
* `spock.failover_slots_database`（字符串，默认为空，`POSTMASTER`）：在 PostgreSQL 16 和 17 上，故障切换槽工作进程连接的数据库，以便在备库解码每个槽副本。不设置时，副本没有自身快照，提升后可能跳过故障切换前不久提交的事务。在 PostgreSQL 16 上，必须是槽所属的数据库。

**变更**

* `spock.pause_timeout`：移除 300 秒上限。
* `spock.restart_delay_default`、`spock.restart_delay_on_exception` 和 `spock.output_delay` 现在声明为毫秒单位，因此接受 `'5s'` 等带单位的值。
* `spock.restart_delay_default` 现在适用于每次应用工作进程重启，包括连接丢失或临时错误之后的重启。

### 其他 SQL 函数和系统目录变更 {#other-sql-function-and-catalog-changes}

监控视图和函数已在上方*节点监控*中列出。

**新增**

* 表 `spock.reserved_object`，列出 Spock 排除在结构同步转储、复制集或 DDL 复制之外的模式与扩展。
* `spock.reserved_object_add(p_name name, p_kind text, p_exclude_from_dump
  boolean DEFAULT true, p_block_in_repset boolean DEFAULT true,
  p_replicate_ddl boolean DEFAULT true)`。
* `spock.reserved_object_remove(p_name name, p_kind text)`。
* `spock.node_alter(p_location text, p_country text, p_info_patch jsonb)`，修改本地节点元数据，并验证 `tiebreaker` 值。
* `spock.node_refresh_info(p_node_name name DEFAULT NULL)`，重新获取某个或所有对端的元数据。
* `spock.slot_enable_failover() RETURNS integer`，由 5.x 升级调用。
* 内部函数 `spock.node_info_emit()`、`spock.node_info_apply()`、`spock.node_info_broadcast()` 和 `spock.node_refresh_info_one()`，以及 `spock.node` 上的 `node_info_broadcast_trigger` 触发器。前两个函数和 `node_refresh_info_one()` 的 EXECUTE 权限已从 PUBLIC 撤销。

**移除**

* `spock.wait_for_apply_worker(p_subbid bigint, timeout int)`。

**变更**

* `spock.repset_add_all_tables()` 现在会跳过无法添加的表并发出警告，而不使整个调用失败。

### 其他变更 {#other-changes}

* 故障切换槽工作进程等待主库上的新槽追平时，不再停止所有槽的同步。新副本在追平之前保持临时槽状态；如果备库先被提升，则删除而非保留该副本。
* PostgreSQL 18 及之后的版本重新安装基于 `spock.pg_standby_slot_names` 和 `spock.standby_slots_min_confirmed` 的 walsender 等待机制。此前它随故障切换槽工作进程一同移除，但原生槽同步只替代工作进程：PostgreSQL 的 `synchronized_standby_slots` 等待其列出的每个槽，因此有两个备库时，只要一个停机，就会停止向所有订阅者复制。
* 故障切换槽工作进程会重建备库上已失效的槽副本，不再继续推进永远无法使用的副本、直到提升后才导致订阅中断。见上面的 `spock.failover_slots_recreate_invalidated`。
* 在 PostgreSQL 16 和 17 上，设置了 `spock.failover_slots_database` 且备库 `wal_level = logical` 时，故障切换槽工作进程会在备库解码每个槽副本，为其建立一致快照。不这样做，提升后可能遗漏故障切换前不久提交的事务。无法解码的副本会通过 WARNING 报告一次。
* 在 PostgreSQL 17 上，故障切换槽工作进程接管原生槽同步后，如果主库删除了原生同步创建的某个副本对应的槽，不再导致工作进程失败并每分钟重启。
* `spock.sub_resync_table()` 清空表时，已经在应用的变更会被跳过，不再因应用失败而在 `spock.exception_behaviour = sub_disable` 时禁用订阅。分区表重新同步时，其分区也采用相同行为。在远端事务中途请求的表同步，现在会启动同步工作进程。
* 使用 `last_update_wins` 时，传入的 `UPDATE` 过去总会胜过被 `VACUUM` 冻结的本地行，即使本地变更发生得更晚，也会如此，可能使各节点最终值不同。现在能够找到冻结行的提交时间戳。
* 通过扩展查询协议、带绑定参数调用执行 `COMMIT` 或 `ROLLBACK` 的过程，可能导致服务器崩溃。`spock.wait_for_sync_event()` 就会这样执行，因此 psycopg 或 JDBC 等客户端等待同步事件时，可能使节点崩溃。
* 开启 `spock.apply_change_logging` 后，如果同一表的列在提供者和订阅者上的布局不同，日志会把值记到错误的列下，并可能使应用工作进程每次重启都崩溃。
* 两个表同步同时完成时，可能同时写入 `resource.dat`，导致应用工作进程结束，并在重启后使其订阅保持禁用。
* PostgreSQL 19 上，AutoDDL 在本地执行 `REPACK (ANALYZE)` 和 `REPACK (CONCURRENTLY)`，不复制它们，因为两者均不能在应用工作进程的事务内运行。
* 当订阅没有同步状态行时，`spock.sub_wait_for_sync()` 和 `spock.table_wait_for_sync()` 会报错，而非永久等待；应用工作进程也会拒绝短到无法容纳类型字段的 Spock 消息。
* 启用 DDL 复制时，拒绝直接针对 `spock` 和 `snowflake` 模式执行 DDL。
* lolor 存储的大对象可以复制，Zodan `add_node` 会将它们复制到新节点。
* Zodan `add_node` 可以将 6.0.0 节点加入由 5.0.9 或更新节点组成的集群，并将源节点的复制集复制到新节点。
* 节点上另一个订阅已启用时，当前订阅不能启用 `forward_origins`。
* 遇到死锁或锁超时等临时错误后，应用工作进程会重启并重试，而非将其视为数据异常。
* PostgreSQL 17 及之后版本上，对 Spock 节点执行 `pg_upgrade` 不再报错 `resource manager with ID 144 not registered`。
* 节点的 location、country 和 info（包括 `tiebreaker`）发生变化时，会发送给其直接订阅者。提供者记录与本地副本不同时，`spock.sub_resync_table()` 会发出警告。
* 复制的 `INSERT` 与同一时刻在本地提交的行冲突时，会进入冲突解决，而非以重复键错误失败。现在，每次向带唯一索引的表执行 `INSERT` 都采用推测插入；见上面的 `spock.non_conflicting_inserts`。
* 有三个或更多节点时，两个提交时间戳相同的变更发生冲突，会根据现有行的真实来源裁决，因此只要各节点对所有节点的 `tiebreaker` 认识一致，就会选择同一胜者。行来源未知时，仍与之前一样使用正在应用变更的节点。初始表同步复制的行记录本地复制源 ID，仍可能被误认成其他节点。`CONFLICT: ... wins over ... by
  tiebreaker` 日志消息现在指出现有行及传入变更的来源，而非当前节点和远端节点。
* pg_duckdb 等扩展在 `SET` 时执行查询，不再导致表同步报错 `SET TRANSACTION SNAPSHOT must be called
  before any query`。
* 增加在 Patroni 下运行逻辑槽故障切换的文档，以及示例 `samples/set_synchronized_standby_slots.sh`。
* 纳入 5.0.11 至 5.0.14 的错误修复。来自 5.0.13 的修复：订阅者的物理备库提升后，不再请求提供者重发订阅者已经应用的事务，避免冲突或无主键表中的重复行；等待期间删除订阅，不再使 `spock.sub_wait_for_sync()` 和 `spock.table_wait_for_sync()` 导致服务器崩溃；结构同步期间 pg_dump 或 pg_restore 失败时，报告子进程的退出情况，而非 `Invalid argument` 等无关错误；表同步不再因源端早于 5.0.7、缺少 `spock.pause_apply_workers()` 而失败。来自 5.0.14 的修复，除上述故障切换槽、冻结行和 `CALL` 修复外，还包括：即使其他槽已满足 `spock.standby_slots_min_confirmed`，也会报告 `spock.pg_standby_slot_names` 中不存在的槽；重复指定的槽只计数一次；AutoDDL 不再复制未指定表的 `CLUSTER` 或针对分区表的 `CLUSTER`；应用工作进程不再在异常日志仍有空闲条目时报告已满，也不再在真正满时遗留未释放的 Spock 锁。
* 提供者启动消息中的错误或格式错误的 `BEGIN`，不再使应用工作进程写出共享内存中分配给它的异常日志条目边界。工作进程会等待 `spock.restart_delay_default` 后重启。
* AutoDDL 过去会使 `CREATE SCHEMA ... CREATE TABLE ...` 报错 `relation "..."
  does not exist`，中止语句。问题发生于 PostgreSQL 19 RC2，以及更早版本中从函数或通过扩展查询协议执行该语句时。
* 可针对 PostgreSQL 19 beta 3、beta 4、RC1、RC2，以及 PostgreSQL 15.20、16.16、17.11、17.12 和 18.7 构建。`attoptions` 服务器补丁已适配这些版本的变更；只有上下文行发生改变。

## Spock 6.0.0 {#spock-600}

本版本同时修改了磁盘上的系统目录格式和 GUC 接口；执行 `ALTER EXTENSION spock UPDATE` 之前，请阅读下方*升级*。


### 主要变化 {#highlights}

* **灾难性节点故障恢复**：基于 ACE 的新工作流通过保留来源的修复，防止节点丢失后发生静默数据分歧。
* **进度跟踪移至 WAL 和共享内存**：消除应用热路径中的高开销系统目录写入；`spock.progress` 现在是基于 `spock.apply_group_progress()` 的视图。
* **更细致的冲突分类**：冲突类型从四种增加到七种，可根据来源抑制冲突，DELETE 冲突也改为通过时间戳裁决。
* **自动传播节点元数据**：通过新函数 `spock.node_alter()` 或普通 `UPDATE` 修改节点的 `location`、`country` 和 `info`（包括用于冲突裁决的 `tiebreaker`）后，会自动传播到所有直接订阅者，不再因遗漏 `spock.node_refresh_info()` 而使裁决值悄然不一致。
* **按订阅统计冲突**：PostgreSQL 18+ 通过自定义 pgstat 类型实现。
* **节点监控视图**：`spock.node_status`、`spock.subscription_status`、`spock.subscription_stats`、`spock.worker_status`、`spock.slot_status` 和 `spock.events` 提供节点的完整情况，无需读取服务器日志。
* **存活检测与反馈重构**：TCP keepalive 取代脆弱的 `wal_sender_timeout` 变通方案；新增 GUC `spock.apply_idle_timeout`。
* **逻辑槽故障切换**：在 PG17+ / PG18+ 上使用 PostgreSQL 原生 slotsync。
* **滚动升级支持**：协议协商（5.0.x 使用 v4，6.0+ 使用 v5）支持零停机滚动升级。
* **异常处理重构**：TRANSDISCARD / SUB_DISABLE 下行为稳定；`spock.exception_log` 保留原始错误消息。
* **重放队列溢写到磁盘**：不再从发布者重新获取。
* **可配置保留模式与扩展**：新系统目录 `spock.reserved_object` 控制哪些模式和扩展排除在结构同步、复制集及 DDL 复制之外。
* **混合版本添加节点**：Zodan `add_node` 可将 6.0.0 节点加入由 5.0.9 或更新节点组成的集群。
* **大对象复制**：lolor 扩展的表可加入复制集，Zodan `add_node` 会将大对象复制到新节点。
* **PostgreSQL 19 支持**：适配内核补丁及特定版本的 API 变更，包括复制源会话状态并入 `replorigin_xact_state`、`CLUSTER` 并入 `REPACK`、`pgstat` 和恢复冲突信号变更，以及 `RepOriginId` 重命名。Spock 可针对 PostgreSQL 19 beta 3、beta 4 和 RC1 构建。这仍是初步支持：本文所述阶段 PostgreSQL 19 尚未发布，不支持在生产环境中使用 PostgreSQL 19 上的 Spock。

### 灾难性节点故障恢复 {#catastrophic-node-failure-recovery}

针对一个节点永久失效、一个或多个存活节点仍有延迟的场景，Spock 6.0 提供并说明了一套结构化恢复流程。使用[主动一致性引擎（ACE）](https://github.com/pgEdge/ace)，运维人员可以：

1. 通过 `table-diff --preserve-origin` 找出落后的存活节点上缺失的行。
2. 通过 `table-repair --recovery-mode --source-of-truth --preserve-origin`，从完全同步的存活节点修复落后节点。

`--preserve-origin` 标志很重要：它确保修复的行保留原始复制源 ID 和提交时间戳，使复制元数据保持正确、集群保持无冲突。不使用此标志，修复的行会被视为本地变更，可能触发虚假冲突。

单节点和多节点故障场景均有说明。完整指南见[灾难性节点故障恢复](/pgedge/spock/recovery/catastrophic-node-failure/)。

### 复制进度跟踪 {#replication-progress-tracking}

复制进度不再通过 `spock.progress` 系统目录表跟踪。Spock 现在在共享内存中实时跟踪，并将快照持久化到 `$PGDATA/spock/resource.dat`。应用工作进程启动时，会将快照与已持久化的复制源 LSN 核对：如果 `resource.dat` 过期，就根据复制源推进 `remote_commit_lsn`，并清空过期的时间戳字段，待后续应用变更时刷新。

每次转储 `resource.dat` 时，自定义资源管理器（ID 144）会为每个 `SpockGroupHash` 条目生成一条 WAL 记录。它们可通过 `pg_waldump` 查看以供调试，不用于状态恢复。

系统目录接口也相应重构：

* `spock.progress` 现在是基于新引入的返回集合的函数 `spock.apply_group_progress()` 的**视图**，按当前数据库过滤。读取原同名*表*的代码仍可工作，但不能再写入。需要实时数据时，直接使用 `apply_group_progress()` 或该视图；导入槽快照时，使用新函数 `spock.read_peer_progress(slot, provider_node_id, subscriber_node_id)`。
* 重新定义 `spock.lag_tracker` 视图。原 `last_received_lsn` 列改名为 `commit_lsn`，准确体现其含义；新增 `received_lsn` 列，报告发布者最后发送的 LSN，与 `pgoutput` 协议约定一致。
* `remote_insert_lsn` 现在在每条传入 WAL 记录上更新，而不只在 COMMIT 时更新，因此延迟读数响应更及时。

### 异常处理改进 {#exception-handling-improvements}

* 修复重试模式提交阶段的 TRANSDISCARD / SUB_DISABLE 处理，避免应用工作进程陷入反复失败的循环。
* 消除错误上下文中的 "(unknown action)" 和 `exception_log` 中的 NULL 错误消息。最初失败的行现在携带真实错误消息；同一事务中受牵连的其他行引用包含根因消息的条目。
* 新增 `initial_operation` 字段，跟踪导致事务丢弃的 DML 操作。
* 卡在无法恢复的同步阶段的订阅，现在会被禁用，而不是无限重启。

### 异常重放：溢写到磁盘 {#exception-replay-spill-to-disk}

`spock.exception_replay_queue_size` 的语义发生变化。

* **以前**：单一字节阈值（默认 4 MiB ≈ 4194304）。内存队列超过阈值时，Spock 无法重放事务，只能从发布者重新获取。
* **现在**：软上限（默认 `4` MB，单位 `MB`）。队列超过上限后，后续条目溢写到磁盘临时文件。设为 `0` 可禁用溢写，并允许无上限地使用内存；这可提高超大事务的吞吐量，分配失败则按 `spock.exception_behaviour` 处理。

`spock.exception_behaviour` 继续控制无法恢复的错误发生时采取的操作：

| 值 | 操作 |
|----------------|----------------------------------------------------------|
| `discard` | 跳过失败事务，继续复制。 |
| `transdiscard` | 回滚失败事务并继续。 |
| `sub_disable` | 禁用订阅并正常退出。 |
{.wide .expand}

### 逻辑槽故障切换 {#logical-slot-failover}

* **PostgreSQL 17+**：Spock 创建所有逻辑复制槽时都设置 `FAILOVER` 标志，使 PostgreSQL 内置 slotsync 工作进程（`sync_replication_slots = on`）能够自动将它们同步到物理备库。
* **PostgreSQL 18+**：不再注册 Spock 自己的 `spock_failover_slots` 后台工作进程，由 PostgreSQL 原生 slotsync 工作进程完全取代。所需的 `postgresql.conf` 设置见配置指南的[逻辑槽故障切换](/pgedge/spock/configuration/#logical-slot-failover-ha-standby)一节。
* **PostgreSQL 17**：Spock 工作进程仍然活动，但设置 `sync_replication_slots = on` 时自动让原生 slotsync 工作进程接管，避免冲突。
* 在 Spock 自己的工作进程运行的版本上（PostgreSQL 15 至 17）：
  * 按 `spock.failover_slots_naptime` 同步槽（默认每秒一次），取代原先每 60 秒一次。
  * 重建在备库上已失效的槽副本，而不是继续推进无法使用的副本。`spock.failover_slots_recreate_invalidated = off` 会保留该副本供检查，并报告一次。
  * 主库槽追上新副本之前，不再停止所有槽的同步。新副本在此期间保持临时槽状态；如果备库先被提升，则删除而非保留副本。
  * 在 PostgreSQL 16 和 17 上，如果设置了 `spock.failover_slots_database`，且备库 `wal_level = logical`，会在备库解码每个副本，为其建立一致快照，行为与 PostgreSQL 17 自身的槽同步相同。否则，提升后可能遗漏故障切换前不久提交的事务。不能解码的副本会通过 WARNING 报告一次。工作进程会持续连接该数据库，因此针对该数据库的 `DROP DATABASE` 等命令会失败。

### 更细致的冲突分类 {#more-granular-conflict-classification}

v5.0 将冲突分为四种。v6.0 扩展为七种，并采用 PostgreSQL 原生冲突类型的命名：

| v5.0 类型 | v6.0 类型 | 变化 |
|-----------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `insert_exists` | `insert_exists` | 不变。 |
| `update_update` | `update_exists` / `update_origin_differs` | 区分本地来源与传入来源一致的更新（静默抑制冲突）和来源不同的更新（通过冲突解决评估）。`update_exists` 用于更新中的约束违例。 |
| `update_delete` | `update_missing` | 重命名，使含义更清楚。 |
| `delete_delete` | `delete_missing` / `delete_origin_differs` | 现在记录缺失行最后是否由不同来源修改。 |
| *（新增）* | `delete_exists` | 远端 DELETE 到达，但本地行的更新时间晚于删除的时间戳，保留较新的本地版本。 |
{.wide .expand}

现有 `spock.resolutions` 数据在 `ALTER EXTENSION spock UPDATE` 时自动迁移，见下方*系统目录变更*。

### DELETE 操作现在使用冲突解决 {#delete-operations-now-use-conflict-resolution}

v5.0 中，DELETE 找到匹配的本地行后会立即应用，不经过冲突解决。v6.0 中，DELETE 与更新一样，通过时间戳裁决。这使新增的 `delete_exists` 分类成为可能：Spock 可以判断应执行删除，还是保留较新的本地版本。

### 自动传播节点元数据 {#automatic-node-metadata-propagation}

节点的 `location`、`country` 和 `info`（包括用于裁决同时间戳冲突的 `tiebreaker` 键，见 [conflict_types.md](/pgedge/spock/conflicts/) 中的*Tiebreaker*）过去每次修改后，都需要在其他每个节点上手动执行 `spock.node_refresh_info()` 重新获取。遗漏刷新的节点会悄然保留不同于其余集群的该对端裁决值。

v6.0 通过 `spock.node` 上新增的 `AFTER UPDATE` 触发器和自定义逻辑复制消息，将此类变更自动传播到每个*直接*订阅它的节点。设计上仅限直接订阅者，不通过级联拓扑转发，以免给现有复制流引入消息顺序依赖。推荐使用新函数 `spock.node_alter()` 修改：它验证 `tiebreaker` 值（必须是可容纳于 32 位整数的 JSON 整数），并合并 `info` 补丁，而非整体替换。直接对节点自身记录执行 `UPDATE spock.node` 仍有效，并以相同方式传播。如果携带变更的事务被跳过或丢弃，某节点缓存记录可能遗漏变更，可通过 `spock.node_refresh_info()` 刷新；提供者记录与缓存不同时，`spock.sub_resync_table()` 会发出警告。详见[自动传播节点元数据](/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)和 [spock.node_alter](/pgedge/spock/reference/functions/spock-node-alter/)。

### 级联复制源跟踪 {#cascade-replication-origin-tracking}

v6.0 支持在级联拓扑（节点 A → 节点 B → 节点 C）中跟踪和转发复制源。协议版本为 5 或更高时，ORIGIN 消息现在包含复制源名称。这样，即使变更经过中间节点 B，节点 C 在评估冲突时仍能获得准确的来源信息。

如果节点 C 还有一个直接订阅节点 A、但处于禁用状态的订阅，节点 A 的变更经节点 B 转发到达时，Spock 现在也会推进该直接订阅的复制源。之后启用直接订阅时，会从已转发变更结束的位置开始，避免再次发送已经通过节点 B 收到的行。

同一节点上已有其他启用的订阅时，不能启用某订阅的 `forward_origins`；其他订阅正在转发时，也不能启用订阅。请先清除 `forward_origins`（通过 `spock.sub_alter_options`），或禁用另一个订阅。详见[复制源转发](/pgedge/spock/reference/sub-mgmt/#origin-forwarding)。

### 按订阅统计冲突 {#per-subscription-conflict-statistics}

在 PostgreSQL 18+ 上，Spock 注册自定义 pgstat 类型（`SPOCK_PGSTAT_KIND_LRCONFLICTS`），按订阅统计复制冲突。新 SQL 函数 `spock.get_subscription_stats(subid)` 和 `spock.reset_subscription_stats(subid)` 用于读取和重置。在 PostgreSQL 18 之前，`get_subscription_stats()` 报告功能不受支持的错误；`reset_subscription_stats()` 则可在所有版本工作，因为它也重置 `spock.subscription_stats` 背后的活动计数器。

### 节点监控视图 {#node-monitoring-views}

Spock 现在在共享内存中保存近期事件历史和各订阅的活动计数器，并通过 `spock` 模式中的一组视图，与工作进程、复制槽和复制状态一起提供：

* `spock.node_status`：一行展示整个节点，包括库与扩展版本、待升级状态、工作进程及订阅数量、复制槽保留的 WAL、复制延迟和最近事件。
* `spock.subscription_status`：每个订阅的配置、状态、负责处理的工作进程、复制位置和延迟，以及最后错误。
* `spock.subscription_stats`：应用和同步工作进程的启动与失败、提供者连接、消息、事务、元组和冲突计数器。
* `spock.worker_status`：监督进程、管理进程、应用和同步工作进程，包括等待重启的工作进程。
* `spock.slot_status`：提供者侧的 spock 槽及其 walsender、位置、保留的 WAL 和反馈延迟。
* `spock.events`：订阅启用与禁用，工作进程启动、停止和失败，提供者连接与断开，跳过及丢弃的事务，表同步，扩展升级。
* `spock.peer_status`、`spock.replication_set_status` 和 `spock.settings`：分别提供已知节点、复制集和复制所依赖的参数。
* `spock.system_status`：主机和实例健康状况，包括数据与 WAL 卷的磁盘空间、负载、连接、长事务和空闲事务、回卷年龄、归档。
* `spock.node_report()`：将整个节点汇总为一份文本报告，依次列出主机和版本、已安装扩展、设置及每个视图。
* 错误记录包含 SQLSTATE、DETAIL、CONTEXT、时间和 pid，并分为死锁、锁超时、约束违例和资源错误；运行输出插件的 walsender 错误记录为 `stream_error` 事件。等待锁的工作进程会显示阻塞它的会话。

事件历史大小由新 GUC `spock.event_history_size` 设置。`spock.reset_subscription_stats()` 现在同时重置活动和冲突计数器。保留 `spock.get_apply_worker_status()`，将其改为基于新函数 `spock.get_worker_status()` 的 SQL 函数；后者与 `spock.worker_status` 视图涵盖所有工作进程类型。GUC、视图和函数见下方*节点监控 GUC、视图和函数*。

### 存活检测与反馈重构 {#liveness-and-feedback-refactoring}

基于 `wal_sender_timeout` 的存活检测机制改为更清晰的两层模型：

* **TCP keepalive** 作为主要存活检测机制，约 25 秒内发现网络或主机失效。
* 复制连接设置 **`wal_sender_timeout=0`**，使 walsender 不会因缺少反馈而断开。
* **`spock.apply_idle_timeout`**（默认 300 秒）作为订阅者侧的保护机制，应对仍保持连接但已卡住的 walsender。

这取代了 `maybe_send_feedback()` 变通方案；原方案将订阅者行为耦合到它无法控制的服务器 GUC。


### 只读模式重构 {#read-only-mode-refactoring}

只读模式改为使用 PostgreSQL 原生 `DefaultXactReadOnly` 机制，取代手动按命令类型过滤：

* `READONLY_USER` 重命名为 `READONLY_LOCAL`，旧名称保留为向后兼容的别名，以明确它限制的是本地非复制连接。
* `READONLY_ALL` 模式下，应用工作进程发送保活反馈，但跳过新事务的应用。
* 在应用下一个事务之前检测只读模式变化，`CHECK_FOR_INTERRUPTS` 已移到重放循环顶部。

### 通过协议协商滚动升级 {#rolling-upgrade-via-protocol-negotiation}

Spock 现在在发布者和订阅者之间协商输出插件协议版本：v5.0.x 使用协议 4，v6.0+ 使用协议 5。这支持零停机滚动升级：v6.0 订阅者可应用 v5 发布者的变更，反之亦然；只有两端都支持时，才启用级联复制源转发等协议 5 专属功能。

现在会及早拒绝不兼容的上游：请求 `synchronize_structure` 时，`create_subscription()` 在执行 DDL 时检查版本；如果上游大版本更高，拒绝结构同步，因为 pg_dump 无法读取更新的服务器。不再等槽和快照创建后才以难以理解的错误失败。

### Zodan：修复写入负载下添加节点的数据丢失 {#zodan-data-loss-fix-when-adding-a-node-under-write-load}

在现有节点处理写入时添加节点，新节点可能永久遗漏行，或积累过期更新。根因是创建槽时没有暂停应用工作进程（该操作耗时不到一秒），使捕获的恢复 LSN 可能落在 COPY 边界之前。修复后在创建槽期间暂停应用工作进程，并以确定的方式捕获恢复 LSN。

6.0 中还包含以下 Zodan 修复：

* 通过新辅助函数 `spock.gen_sub_name()`，将槽和订阅统一命名为 `sub_{provider}_{subscriber}`。
* `remove_node` 根据 `spock.subscription` 系统目录删除订阅，不再猜测名称。
* 对齐阶段 3 的追平等待，并将 `spock.sync_event()` 参数化，避免阶段 9 的握手死锁。
* **混合版本**：`add_node` 可将 6.0.0 节点加入运行 5.0.9 或更新版本的集群，无需先升级全部节点。现有节点也可以已经混合运行不同版本。新节点的版本必须不低于任何现有节点。
* **复制集配置一并复制**：新节点获得源节点的复制集，包括用户创建的集合、列列表、行过滤器，以及从集合中移除表的情况。此前订阅只指定三个内置集合，因此用户自建集合中的表既不发送也不接收。
* **大对象**：只要表为空，新节点可以预装 lolor；如果源节点复制 lolor 表，新节点就必须安装它。初始数据同步会复制大对象。
* **更长等待**：新 GUC `spock.sync_timeout` 可提高节点管理例程中每次等待的时限。此前固定约三分钟，对大型数据库过短。`spock.pause_timeout` 也不再有 300 秒上限。
* 移除旧 Python 版本 `zodan.py` 和 `zodremove.py`，请使用 SQL 过程。

### AutoDDL 改进 {#autoddl-improvements}

AutoDDL 已重构并加固：

* **集中到 `spock_autoddl.c`**：所有 AutoDDL 基础代码移入单一模块，便于维护。
* **简化控制流**：移除递归标签匹配启发式，改用更清晰的提前退出过滤。
* **扩展脚本保护**：不再复制 `CREATE EXTENSION` / `ALTER EXTENSION UPDATE` 期间的内部子命令。
* **事务保护**：工具命令（例如不带表名的 `CLUSTER`）在事务上下文之外执行时，AutoDDL 钩子不再失败。
* **过滤非事务性 DDL**：对不能在订阅者事务块内执行的命令（例如针对分区表的 `CLUSTER`、`VACUUM`），在发布者入队前就过滤。
* **不复制临时关系的 DDL**：跳过 `CREATE TABLE … (LIKE temp)` 和 `CREATE TABLE … AS SELECT … FROM temp`，因为订阅者上没有该临时关系。
* **`ALTER TABLE` 保留复制集归属**：启用 `spock.include_ddl_repset` 时，除非添加或删除主键／复制标识，否则 `ALTER TABLE` 不再将表移出用户自定义复制集。内联 `ADD COLUMN … PRIMARY KEY` 和 `REPLICA IDENTITY FULL` 表现在能正确分类。
* **安全插入 `search_path`**：即使会话路径为空，复制的 DDL 也会携带有效的 `SET search_path`。
* **拒绝直接针对 `spock` 和 `snowflake` 的 DDL**（行为变更）：启用 `spock.enable_ddl_replication` 时，如果语句目标模式是内置扩展拥有的模式之一，现在会直接失败：

  ```
  ERROR:  cannot run DDL against schema snowflake while DDL replication is enabled
  DETAIL:  The schema is managed by an extension and its objects are not replicated.
  HINT:  For a deliberate node-local change, run the statement with spock.enable_ddl_replication = off.
  ```

  这些模式由扩展脚本填充，而扩展脚本中的 AutoDDL 已被抑制，因此运行时直接针对它们执行语句几乎总是误操作。此前这类语句只部分生效：命令文本复制到对端，但关系却悄然被排除在所有复制集之外。影响范围见*升级*。
* **`DROP EXTENSION` 期间扩展自身的 DDL 保留在本地**：开启 `spock.allow_ddl_from_functions` 后，扩展被删除时执行的 DDL 过去会进入复制队列，即使每个对端应用 `DROP EXTENSION` 时都会执行相同清理。对于 lolor，这会使对端无法删除扩展，并导致应用停滞。`DROP EXTENSION` 本身仍会复制，下述本地扩展除外。
* **不再复制 `CREATE`、`ALTER` 和 `DROP EXTENSION lolor`。** lolor 拒绝由应用工作进程创建或删除，因此过去每个对端都会将复制来的语句写入 `spock.exception_log` 并丢弃，而发出语句的节点却报告已复制。`spock.reserved_object` 中 `lolor` 扩展记录的 `replicate_ddl = false`，AutoDDL 仅在发出语句的节点执行，并发出 WARNING 说明。请在每个节点分别运行。`COMMENT ON EXTENSION lolor` 和 `SECURITY
  LABEL ON EXTENSION lolor` 同样保留在本地。启用 DDL 复制时，同时指定 lolor 和其他扩展的 `DROP EXTENSION` 会被拒绝；对依赖 lolor 的扩展执行 `CREATE EXTENSION ... CASCADE` 也会被拒绝。`spock.replicate_ddl()` 拒绝针对 lolor 执行这些语句。

### 保留模式与扩展 {#reserved-schemas-and-extensions}

Spock 会将部分模式和扩展排除在结构同步转储及复制集之外。这份列表过去固定在代码中，现在改为 `spock.reserved_object` 系统目录，每行包含三个设置：

* `exclude_from_dump`：排除在结构同步转储之外。
* `block_in_repset`：其表不得加入复制集。
* `replicate_ddl`：为 `false` 时，针对该扩展的 `CREATE`、`ALTER` 和 `DROP EXTENSION` 只在发出语句的节点执行。对模式而言，AutoDDL 能追溯到该模式的 DDL 也如此；其他语句，如 `GRANT`，仍会复制。语句列表见[复制集管理](/pgedge/spock/reference/repset-mgmt/)。默认值为 `true`。

内置记录不能修改或删除：

| 对象 | exclude_from_dump | block_in_repset | replicate_ddl |
|--------------|-------------------|-----------------|---------------|
| `spock` | 是 | 是 | 是 |
| `snowflake` | 是 | 是 | 是 |
| `lolor` | 是 | 否 | 模式为是，扩展为否 |
| `coldfront` | 是 | 否 | 是 |
| `pgedge_ace` | 是 | 是 | 否 |
{.wide .expand}

通过 `spock.reserved_object_add()` 添加自己的记录，通过 `spock.reserved_object_remove()` 删除。自建记录会在转储和恢复后保留。详见[保留模式与扩展](/pgedge/spock/reference/repset-mgmt/#reserved-schemas-and-extensions)。

现在，无论订阅者上是否存在该对象，都会应用转储排除规则。此前，只存在于提供者上的对象从不会被排除。

### `repset_add_all_tables()` 跳过无法添加的表 {#repset_add_all_tables-skips-tables-it-cannot-add}

过去，只要有一张表没有复制标识索引，`spock.repset_add_all_tables()` 就会失败，且不添加任何表。现在会添加能够添加的表，并以警告逐个指出被跳过的表。保留模式中的表或保留扩展拥有的表也同样跳过。调用时指定保留模式仍会报错；`spock.repset_add_table()` 遇到无法添加的表也仍会失败。

错误消息现在使用 "replica identity index"，而不再归咎于缺少主键，因为具有主键但设置了 `REPLICA IDENTITY FULL` 或 `NOTHING` 的表也会被拒绝。

### 内存与稳定性 {#memory-and-stability}

* **重放队列溢写到磁盘**（见上方*异常重放*），不再触发工作进程重启，消除大型事务带来的不可预测重启和复制延迟突增。
* **修复资源泄漏**：
  * 过滤大量行时，行过滤处理不再泄漏资源所有者条目。
  * 冲突报告路径使用完 `remotetuple` 后会将其释放。
* **共享内存初始化**集中到 `spock_shmem.c`，正确处理启动进程、检查点进程和后台工作进程。

### 6.0 专属错误修复 {#bug-fixes-specific-to-60}

* **应用工作进程失败后的 WAL 恢复崩溃**：应用工作进程崩溃触发服务器重启时，共享内存结构初始化不当可能使 WAL 恢复失败。共享内存初始化已重构，正确处理启动进程、检查点进程和后台工作进程。
* **崩溃恢复后丢失 `remote_insert_lsn`**：该值过去未写入 WAL 记录，崩溃恢复后默认为 0，破坏 `spock.lag_tracker` 的延迟跟踪。
* **生成列**：包含 `GENERATED ALWAYS AS … STORED` 列的表会发生复制错误，因为 COPY、协议消息、默认值填充和冲突解决将生成列视为普通列。现在已正确排除。
* **`REPLICA IDENTITY FULL` 下的复制索引查找**：调用 `RelationGetReplicaIndex()` 前未使缓存索引信息失效，导致切换复制标识模式时使用错误索引。
* **哈希表遍历安全**：修复遍历时删除造成的损坏、`HASH_FIXED_SIZE` 表缺少 NULL 检查，以及无自旋锁保护时 64 位计数器的撕裂读取。
* **跳过 LSN 机制**：`SUB_DISABLE` 模式下成功跳过事务后，由于跳过点（BEGIN LSN）与清除点（COMMIT LSN）不匹配，会错误地再次禁用订阅。现在成功跳过后会清除异常处理状态。
* **检测表同步失败**：表同步期间的 COPY 失败过去被悄然吞掉，同步工作进程无限重试。现在在 `PQputCopyEnd()` 后调用 `PQgetResult()` 检测失败，并用新状态 `SYNC_STATUS_FAILED` 停止重试循环，呈现明确错误消息。
* **无法应用的 TRUNCATE 导致循环崩溃**：`discard` 模式下，订阅者上失败的 TRUNCATE（例如关系不存在）会使应用工作进程陷入崩溃循环。现在与其他 DML 一样，将其置于子事务中，记录后丢弃。
* **PostgreSQL 17 及之后版本的 `pg_upgrade` 失败**：`pg_upgrade` 解码每个逻辑槽剩余的 WAL，以确认槽已排空，但 `pg_upgrade` 启动的服务器未注册 Spock 资源管理器，检查因此报错 `resource manager with ID 144 not registered`。
* **应用空闲超时被当作数据异常**：事务中途触发 `spock.apply_idle_timeout` 时，错误过去进入数据异常路径，可能禁用订阅或丢弃正常事务。现在按连接丢失处理。
* **进度跟踪中的时钟偏差**：源端提交时间戳领先于订阅者时钟，或转发事务的时间戳未随提供者 WAL 位置递增时，会在启用断言的构建中触发断言。现在 `remote_commit_lsn` 独立于时间戳字段推进。
* **从溢写文件恢复的重放条目未添加终止标记**：从磁盘读取的截断或格式错误记录，过去可能被扫描到缓冲区末尾之外，而非被拒绝。
* **对端会话使用固定时间格式**：Spock 以文本形式读取其他节点的提交时间戳，含义过去依赖两端的 `DateStyle` 和 `TimeZone`。两端设置不同时，相同文本可能表示不同时间；在 `add_node` 依据时间戳选择推进槽的 LSN 时尤其重要。对端连接现在请求 `datestyle=ISO`，并拒绝未显式包含 UTC 偏移的对端时间戳。
* **已删除列的表使用行过滤器进行初始同步**：删除列之后的行值曾按错误偏移读取，造成行损坏或崩溃。
* **同步工作进程丢失原始错误**：表同步创建槽时失败，曾被报告为 `errstart was not called`，而非真实错误。
* **复制的 `INSERT` 与本地插入竞争**：应用工作进程查找冲突行，未找到便插入；期间在本地提交的行被遗漏，导致插入以重复键错误失败，而未进入冲突解决。现在采用推测插入，以每个即时唯一索引作为裁决索引，并查找及解决报告的重复项。这使每次向带唯一索引的表执行 `INSERT` 都增加推测插入；确定不会碰撞时，可通过 `spock.non_conflicting_inserts` 关闭。如果冲突发生在用于查找行的索引之外的其他唯一索引上，除非开启 `spock.check_all_uc_indexes`，否则仍会报重复键错误。
* **三节点或更多节点网状集群中的同时间戳裁决**：过去裁决比较正在应用变更的节点与传入变更的来源。节点处理来自另外两个节点的写入冲突时，可能选择不同于那两个节点的胜者。现在在现有行记录的来源与传入变更来源之间裁决；行来源未知时，才回退到应用节点。
* **使用 pg_duckdb 时的表同步**：会话 `SET` 曾在 COPY 事务内发送，因此在 `SET` 时执行查询的扩展会使快照导入报错 `SET TRANSACTION SNAPSHOT must be called before
  any query`。现在在事务开始前发送这些设置。
* **重新同步期间正在应用的变更**：`spock.sub_resync_table()` 将表标记为正在同步并清空，但应用工作进程只在远端事务之间重新读取正在同步的表列表。已经在应用的变更遇到空表时，找不到行的 `UPDATE` 会在 `sub_disable` 下禁用订阅。现在跳过这些变更，包括分区表正在重新同步时对其分区的变更；同步工作进程复制的数据包含它们。远端事务中途请求的表同步过去也无法启动同步工作进程。
* **`last_update_wins` 与冻结行**：本地行的提交时间戳过去通过 xmin 查找；`VACUUM` 冻结行后，xmin 读作冻结值，使该行被视为早于任何变更。较旧的传入 `UPDATE` 因而覆盖较新的本地值，可能使节点数据分歧。所有支持的 PostgreSQL 版本均受影响：`VACUUM (FREEZE)` 和激进清理会冻结近期写入的行，PostgreSQL 16 起普通 `VACUUM` 也可能这样做。现在改用原始 xid。
* **过程结束事务后崩溃**：通过扩展查询协议、带绑定参数执行的 `CALL` 运行 `COMMIT` 或 `ROLLBACK` 后，AutoDDL 从已释放内存中读取语句，导致服务器崩溃。`spock.wait_for_sync_event()` 会执行 `ROLLBACK`，因此 psycopg 或 JDBC 客户端等待同步事件时可能使节点崩溃。
* **列布局不同时的 `spock.apply_change_logging`**：过去按提供者的列位置读取值，因此两端列顺序或删除情况不同时，值被记到错误的列下；将一种类型按另一种类型打印，可能使应用工作进程每次重启都崩溃。
* **并发写入 `resource.dat`**：两个表同步同时完成时会写同一临时文件，第二次重命名失败，导致应用工作进程结束，并在重启后使订阅保持禁用。
* **PostgreSQL 19 上的 `REPACK`**：AutoDDL 曾将 `REPACK (ANALYZE)` 和 `REPACK (CONCURRENTLY)` 入队，但它们不能在应用工作进程的事务内运行。现在只在本地执行，与无表名和针对分区表的 `CLUSTER` 相同。
* **故障切换槽工作进程**：PostgreSQL 15 至 17 上，它曾推进备库上已失效的副本，使副本看似最新，订阅却在提升后中断；它无限期等待落后的主库槽，期间不再同步其他槽，等待期间提升还会保留遗漏提交的副本；PostgreSQL 16 和 17 上，副本没有自身快照，可能遗漏故障切换前不久提交的事务；PostgreSQL 17 上，原生槽同步创建的副本对应主库槽被删除，会使工作进程每分钟重启。见上方*逻辑槽故障切换*。
* **`spock.sub_wait_for_sync()` 和 `spock.table_wait_for_sync()` 永久等待**：订阅没有同步状态行时会如此。现在改为报错。

### 安全 {#security}

* **DSN 密码隐藏**：DSN 连接字符串中的密码不再出现在错误消息或日志输出中。消息过滤钩子会在写入前清除错误消息中的密码字符。


### 其他值得关注的变更 {#other-notable-changes}

* **协议清理**：从 Spock 协议中移除未使用的 SPI API 支持，修复多项协议参数验证问题。
* **阻止将被忽略的模式中的表添加到复制集。**
* **移除 Snowflake**：删除 snowflake 相关函数和文档，因为它已迁入独立仓库。
* **移除 SpockCtrl**：删除 SpockCtrl 工具代码。
* **移除 Windows 支持**：删除 Win32 专用代码路径，Spock 仅面向 POSIX 环境。
* **`--exclude-extension`**：扩大对该 pg_dump 选项的使用（PostgreSQL 17+）。
* **PostgreSQL 18 支持**：适配内核补丁、initdb、行过滤器和编译器警告。
* **重组源码树**：使用 `src/` 和 `include/` 目录。
* **打包**：仓库现在自行构建 `spock60` 的 RPM 和 DEB 软件包。不再为已结束生命周期的 Debian bullseye 构建。
* **文档**：新增按节点数和数据库数规划 Spock 所需 PostgreSQL 资源的指南（见[资源规划](/pgedge/spock/sizing/)）、说明漏洞报告方法的 `SECURITY.md`，并在 README、配置、安装和故障排查指南中补充 `output_plugin_libraries` 要求。从 5.0.12 纳入在 Patroni 下运行逻辑槽故障切换的指南及示例 `samples/set_synchronized_standby_slots.sh`，见[逻辑槽故障切换](/pgedge/spock/logical-slot-failover/)。

### GUC 变更 {#guc-changes}

**新增**

* `spock.apply_idle_timeout`（整数，秒，默认 `300`，`SIGHUP`）：用于检测仍保持 TCP 连接、却已停止发送数据的卡住的 walsender。收到任何消息都会重置计时器。设为 `0` 可禁用，仅依赖 TCP keepalive 检测存活状态。
* `spock.output_delay`（整数，毫秒，默认 `0`，范围 0–60000，`SIGHUP`）：在发布者侧输出插件中人为引入延迟，用于测试中重现冲突和延迟场景。
* `spock.resolutions_retention_days`（整数，天，默认 `100`，`SIGHUP`）：`spock.resolutions` 中记录的存活时间。超过此期限的记录由应用工作进程定期删除。设为 `0` 禁用自动清理。与 `spock.cleanup_resolutions(days)` 及新增的 `resolutions(log_time)` 索引配合使用。
* `spock.enable_quiet_mode`（布尔值，默认 `off`，`SIGHUP`）：启用后，将 DDL 复制的 INFO/WARNING 消息降为 LOG，并抑制 `DROP CASCADE` 操作的依赖对象报告。用于回归测试及希望减少输出的生产环境。
* `spock.log_verbosity`（枚举 `normal`/`debug1`/`debug2`，默认 `normal`，`SUSET`）：将 Spock 自身的 `DEBUG1`/`DEBUG2` 消息提升为 `LOG`，使其在常规 `log_min_messages` 下也能保留。
* `spock.apply_change_logging`（枚举 `none`/`key_only`/`verbose`，默认 `none`，`SUSET`）：应用工作进程按每项变更输出 JSON，包含操作、表、键、来源和提交时间戳；`verbose` 还包含行数据。
* `spock.read_retry_count`：配置未找到预期行时的重试次数。默认值与此前硬编码的 5 相同，每次重试之间休眠 1 毫秒。设为 0 禁用重试，适合节点延迟很大、不希望拖慢处理的情况。
* `spock.sync_timeout`（整数，秒，默认 `0`，`USERSET`）：节点管理例程中单次等待的时限，用于等待同步事件到达、对端追平或订阅开始复制。大型数据库追平耗时超过内置时限时，可增大此值。`0` 保持各例程内置限制。可针对单次操作设置，例如 `SET spock.sync_timeout = '2h'`。
* `spock.failover_slots_naptime`（整数，毫秒，默认 `1000`，范围 1–3600000，`SIGHUP`）：Spock 故障切换槽工作进程在两轮槽同步之间休眠多久。此前固定为 60 秒，可能使备库槽落后多达一分钟。
* `spock.failover_slots_feedback_naptime`（整数，毫秒，默认 `10000`，范围 1–3600000，`SIGHUP`）：故障切换槽工作进程等待备库接收槽所需 WAL 时采用的较短重试间隔。这两个故障切换槽设置只在 Spock 自身工作进程运行时有效，即 PostgreSQL 15、16，以及关闭 `sync_replication_slots` 的 17。
* `spock.non_conflicting_inserts`（布尔值，默认 `off`，`POSTMASTER`）：断言复制的 `INSERT` 绝不会与本地行冲突，例如各节点从独立范围生成键。应用工作进程因此跳过冲突查找和推测插入，直接插入行。系统不验证该断言：发生碰撞会抛出重复键错误，由 `spock.exception_behaviour` 而非冲突解决处理。
* `spock.failover_slots_recreate_invalidated`（布尔值，默认 `on`，`SIGHUP`）：Spock 故障切换槽工作进程是否删除并重建备库上已失效的槽副本。`off` 保持副本原状供排查原因，并报告一次；重新开启后，在第一轮同步时重建副本。
* `spock.failover_slots_database`（字符串，默认为空，`POSTMASTER`）：PostgreSQL 16 和 17 上，Spock 故障切换槽工作进程连接的数据库，以便在备库解码每个槽副本并为其建立一致快照。PostgreSQL 16 上必须是槽所属数据库。为空时保留旧行为，提升后可能遗漏故障切换前不久提交的事务。

**移除**

* `spock.use_spi`：不再使用，旧 SPI 应用路径已移除。
* `spock.feedback_frequency`：由内部节奏控制取代。
* `spock.batch_inserts`：未使用。

**变更**

* `spock.exception_replay_queue_size`：默认值从 `4194304` 改为 `4`，单位从字节改为 MB，语义从硬阈值（超出后向发布者重新获取）改为软上限（超出后溢写磁盘）。见上文。
* `spock.pause_timeout`：移除 300 秒上限，以支持超大或长时间运行的事务。默认值仍为 10 秒。
* `spock.restart_delay_default`、`spock.restart_delay_on_exception` 和 `spock.output_delay` 现在声明为毫秒，因此接受带单位的值（`'5s'`），`SHOW` 也会显示单位。其数值不变。
* `spock.restart_delay_default` 现在适用于每次应用工作进程重启，包括连接丢失或临时错误之后的重启，防止未消除的问题导致频繁重启。

### 系统目录变更 {#catalog-changes}

* 新增 `spock.sub_id_generator` 序列，取代订阅记录中内联的计数器生成 OID 方式。
* 新增 `spock.reserved_object` 表，列出保留模式和扩展（见上方*保留模式与扩展*）。内置记录由触发器保护，只转储用户添加的记录。
* 新增索引 `spock.resolutions(log_time)`，支持 `spock.cleanup_resolutions()`。
* 升级时重命名 `spock.resolutions.conflict_type` 值：`update_update` → `update_exists`，`update_delete` → `update_missing`，`delete_delete` → `delete_missing`；`insert_exists` 不变。
* `spock.subscription.sub_skip_schema` 现在正确声明为 `text[]`。该列在 5.0.2 中被添加为 `text`，但 C 代码一直按 `text[]` 处理其字节；5.0.7 升级步骤重新标注系统目录，因此无需重写或停机。
* 新监控视图见下方*节点监控 GUC、视图和函数*。

### 新增函数 {#new-functions}

* `spock.apply_group_progress()`：返回健康状态集合的函数，为 `spock.progress` 提供数据。
* `spock.read_peer_progress(slot, provider_node_id, subscriber_node_id)`：由 zodan 在导入槽快照时使用。
* `spock.get_subscription_stats(subid)` / `spock.reset_subscription_stats(subid)`：按订阅统计冲突，读取要求 PostgreSQL 18 或更新版本。
* `spock.cleanup_resolutions(days int DEFAULT NULL)`：按存活时间清理冲突解决日志。默认权限从 PUBLIC 撤销 EXECUTE。
* `spock.sub_alter_options(subscription_name name, options text[])`：批量修改订阅选项，验证输入，并在无实际变更时跳过重启。
* `spock.reserved_object_add(p_name name, p_kind text,
  p_exclude_from_dump boolean DEFAULT true, p_block_in_repset boolean
  DEFAULT true, p_replicate_ddl boolean DEFAULT true)`：保留模式或扩展，或修改现有记录。
* `spock.reserved_object_remove(p_name name, p_kind text)`：移除自己添加的保留模式或扩展。
* `spock.slot_enable_failover() RETURNS integer`：在 PostgreSQL 17 及之后版本为 Spock 逻辑槽设置 `failover` 标志，并返回修改的槽数。从 5.x 升级时会调用它。EXECUTE 权限已从 PUBLIC 撤销。
* `spock.node_alter(p_location text, p_country text, p_info_patch jsonb)`：以经过验证的方式修改本地节点自身的 location/country/info，合并 info 并验证 `tiebreaker` 补丁；见上方*自动传播节点元数据*。
* `spock.node_refresh_info(p_node_name name DEFAULT NULL) RETURNS boolean`：针对遗漏变更的缓存记录，重新从对端获取其 location、country 和 info；不指定名称时获取所有对端。指定名称调用时，若无法刷新该节点就报错；不指定名称时，对每个无法刷新的对端发出警告，只要有一个失败就返回 `false`。
* `spock.node_info_emit()` / `spock.node_info_apply()` / `spock.node_info_broadcast()`（触发器函数，支撑 `spock.node` 上新增的 `node_info_broadcast_trigger`）/ `spock.node_refresh_info_one()`：节点元数据传播和刷新背后的内部函数，不供直接调用；除触发器函数外，`EXECUTE` 已从 `PUBLIC` 撤销。
* 监控函数见下方*节点监控 GUC、视图和函数*。

### 移除函数 {#removed-functions}

* `spock.convert_column_to_int8(regclass, smallint)`：已被替代。
* `spock.convert_sequence_to_snowflake(regclass)`：已被替代。
* `spock.wait_for_apply_worker(p_subbid bigint, timeout int)`：SpockCtrl 移除后已无调用者。

### 节点监控 GUC、视图和函数 {#node-monitoring-gucs-views-and-functions}

这里集中列出 6.0 新增的监控功能。上方*节点监控视图*介绍展示内容。视图的 SELECT 权限及其所读函数的 EXECUTE 权限已授予 `pg_monitor`；`spock` 模式的 USAGE 权限未授予，因此监控角色还需获得该权限。

**GUC**

* `spock.event_history_size`（整数，默认 `1024`，范围 16 至 1048576，`POSTMASTER`）：`spock.events` 视图在共享内存中保留的近期事件数量。历史已满时，每个新事件都会挤掉最旧事件；重启后历史丢失。

**视图**

* `spock.node_status`：一行展示整个节点，包括版本、待升级状态、工作进程和订阅数量、复制槽保留的 WAL、复制延迟、最近事件。
* `spock.peer_status`：已知节点。
* `spock.subscription_status`：每个订阅的配置、状态、负责处理的工作进程、复制位置和延迟，以及最后错误。
* `spock.subscription_stats`：各订阅的工作进程启动与失败、提供者连接、消息、事务、元组和冲突计数器。
* `spock.worker_status`：监督进程、管理进程、应用和同步工作进程，包括等待重启的工作进程。
* `spock.slot_status`：提供者侧的 spock 槽及其 walsender、位置、保留的 WAL 和反馈延迟。
* `spock.table_sync_status`：表同步状态。
* `spock.replication_set_status`：复制集。
* `spock.system_status`：磁盘空间、负载、连接、长事务和空闲事务、回卷年龄、归档。
* `spock.settings`：复制所依赖的参数。
* `spock.events`：近期事件历史。

**函数**

* `spock.node_report(recent integer DEFAULT 50) RETURNS SETOF text`：将整个节点汇总为一份文本报告，供支持请求使用，包含主机和版本、已安装扩展、设置、所有监控视图，以及最近的异常、冲突解决记录和事件。
* `spock.replication_origin_status()`：复制源及其进度，允许 `pg_monitor` 读取；`pg_replication_origin_status` 仅限超级用户。
* 视图和 `node_report()` 背后的内部函数：`spock.get_worker_status()`、`spock.get_events()`、`spock.reset_events()`、`spock.get_apply_stats()`、`spock.get_slot_groups()`、`spock.get_monitor_summary()`、`spock.get_system_info()`、`spock.get_pending_exceptions()`、`spock.redact_dsn()`、`spock.wal_size_bytes()` 和 `spock.report_section()`。`get_system_info()`、`get_events()`、`get_apply_stats()` 和 `get_pending_exceptions()` 仅允许 `pg_monitor` 执行，`reset_events()` 仅允许超级用户执行。
* `spock.reset_subscription_stats(subid)` 在所有支持的 PostgreSQL 版本上也重置 `spock.subscription_stats` 背后的活动计数器，且仅允许超级用户运行。
* `spock.get_apply_worker_status()` 现在是基于 `spock.get_worker_status()` 的 SQL 函数，列和行与以前相同。

### 从 5.0.x 系列纳入的错误修复 {#bug-fixes-carried-forward-from-the-50x-line}

以下修复已在 5.0.6–5.0.14 发布，并纳入 6.0.0。5.0.14 的修复见上方 6.0.0-beta.2 说明的*其他变更*。

* 订阅者的物理备库提升后，可能重放订阅者已经应用的事务。应用工作进程提交时记录的是源节点的进度，而非订阅进度，因此崩溃恢复和物理备库上的订阅复制源仍停留在最后检查点或基础备份的位置；提升后便要求提供者重发该位置之后的全部内容。应用和同步工作进程现在在每次提交后将订阅进度写入 WAL。（5.0.13）
* 等待期间删除订阅，过去会使 `spock.sub_wait_for_sync()` 和 `spock.table_wait_for_sync()` 导致服务器崩溃。现在报告订阅不存在。（5.0.13）
* 结构同步期间 pg_dump 和 pg_restore 失败，过去会用过期的 `errno` 报告 `Invalid argument` 等消息。现在错误会提供子进程退出码或信号。（5.0.13）
* 对早于 5.0.7 的源端执行表同步，过去会因缺少 `spock.pause_apply_workers()` 和 `spock.resume_apply_workers()` 报错 `function does not exist`。现在在这种情况下跳过暂停和恢复。（5.0.13）
* 正确处理上游连接丢失，避免复制源被错误推进。此前，过期的 libpq 套接字 fd 引发一连串 `epoll_ctl(EINVAL)` 错误，恢复路径可能悄然将复制源推进到正在处理的远端事务之后，导致重连时遗漏事务。使用 `spock.exception_behaviour = transdiscard` 时，其行会进入 `spock.exception_log`，并带有 `error_message = unknown`。应用工作进程现在对连接类错误执行 `PG_RE_THROW`，由管理进程从最后持久提交的远端 LSN 重新启动它。
* 在 `transdiscard` / `sub_disable` 下应用变更时，`spock.exception_log` 保留原始错误消息。最初失败的行携带真实错误，同一事务中受牵连的其他行记为 `unavailable`，而非 `unknown`。
* zodan：通过新辅助函数 `spock.gen_sub_name()`，将槽和订阅统一命名为 `sub_{provider}_{subscriber}`；`remove_node` 从 `spock.subscription` 系统目录读取订阅，而非猜测名称；创建槽期间暂停应用工作进程，防止添加节点时丢失数据；对齐阶段 3 的追平等待，并参数化 `spock.sync_event()`，避免阶段 9 的握手死锁。
* 防止订阅者只读时 `resync_table` 丢失数据（SPOC-440）。
* 修复关系缺失时 INSERT 异常路径中的过期 `local_tuple` 指针；`SUB_DISABLE` 现在正常退出，不再解引用已释放内存。
* 备库用于报表而非故障切换时，抑制反复出现的 `hot_standby_feedback off` ERROR。
* 修复 `spock_connect_base()` 中栈变量超出作用域后继续使用的问题（ASan 发现）。
* 修复资源所有者错误。
* 将 `apply_replay_bytes` 从 `int` 改为 `uint64`，修复溢出（`b4ba9bdf`）。
* `SUB_DISABLE` 下提供者连接丢失可能禁用订阅：重发事务被误认成曾应用失败的事务。
* 应用工作进程遇到临时错误会重试，包括死锁、`lock_timeout`、资源耗尽（SQLSTATE 类 53），或提供者正在重启、恢复（57P02、57P03）。不再将其当作会禁用订阅或丢弃事务的数据异常。工作进程退出时不推进复制源，由提供者重发事务。
* 事务中途重启应用工作进程，过去可能在 `SUB_DISABLE` 下禁用订阅。工作进程因 `SIGTERM` 退出时，现在会清除失败标记。
* 事务之间的错误过去会使应用工作进程在下一个从未失败过的事务中仍处于重放模式，导致 `TRANSDISCARD` 或 `SUB_DISABLE` 下丢弃事务或禁用订阅。
* 名称具有共同前缀的两个订阅（如 `sub` 和 `sub_parallel`）过去共用一个异常日志槽位。查找现在比较完整名称，也不再读出数组边界。
* `spock.get_lsn_from_commit_ts()` 可能在空闲节点上挂起。其 WAL 扫描现在以扫描开始时的 WAL 末尾为终点。
* 未设置 `spock.primary_dsn` 时，walreceiver 每次重连主库都可能使故障切换槽工作进程退出。现在等待下一轮。
* 两条从 LOG 降为 DEBUG1 的重试消息，过去因级别判断反向，在默认设置下仍进入服务器日志。
* 提供者有而订阅者没有的列，过去会使应用工作进程陷入重启循环。现在按表缺失的方式处理，并在错误中列出每个缺失列。
* 使用提供者元组数据之前，会对照本地列定义检查；不匹配的元组被拒绝，而非继续应用。也检查 RELATION 消息中的名称和属性数量；未启用 lz4 构建的订阅者会拒绝 lz4 压缩的值。


### 升级 {#upgrading}

替换二进制文件后，从 5.0.14 升级到 6.0.0 只需一次 `ALTER EXTENSION spock UPDATE`。更早的 5.0.x 版本也可通过同一命令，经 5.0.14 升级。升级过程会：

* 删除旧 `spock.progress` 表，并重建为视图；
* 替换 `spock.lag_tracker` 视图定义；
* 迁移 `spock.resolutions.conflict_type` 值；
* 添加新函数、`sub_id_generator` 序列和 `spock.reserved_object` 系统目录；
* 删除 `spock.wait_for_apply_worker()`；
* 将 C 函数 `spock.get_apply_worker_status()` 替换为基于 `spock.get_worker_status()` 的 SQL 函数；
* 在 `spock.node` 上添加 `node_info_broadcast_trigger` 触发器；
* 添加监控视图和函数，并向 `pg_monitor` 授予读取权限；
* 刷新 `spock.md5_agg_sfunc`、`spock.md5_agg` 和 `spock.spock_gen_slot_name` 的并行安全属性；
* 调用 `spock.slot_enable_failover()`，为现有逻辑槽开启 `failover` 标志，使 PostgreSQL 17 和 18 的槽同步能发现它们。PostgreSQL 16 及更早版本以及备库上不执行此操作，正在使用的槽会被跳过。如何处理跳过的槽，见[逻辑槽故障切换](/pgedge/spock/logical-slot-failover/)。

升级前，检查操作手册和自动化是否直接针对 `spock` 或 `snowflake` 模式执行 DDL。`DROP TABLE snowflake.x` 或在 `spock` 表上执行 `CREATE INDEX` 等语句，在 5.0.x 上可以成功，现在会报错，见上方*AutoDDL 改进*。必须继续这样操作的流程，需要先为会话设置 `spock.enable_ddl_replication = off`，错误提示也会这样说明。限制仅覆盖内置扩展拥有的模式；通过 `spock.reserved_object_add()` 自行保留的模式不受影响，`pgedge_ace` 仍接受 DDL 并将其保留在本地。

PostgreSQL 2026 年针对 CVE-2026-6471 的安全修复新增 `output_plugin_libraries` 参数，其默认值不含 `spock_output`，因此带此修复的服务器上逻辑解码会失败。请在所有支持该参数的节点上（包括物理备库）设置 `output_plugin_libraries = 'pgoutput, test_decoding, spock_output'`；不支持该参数的服务器不要设置。见[配置 Spock](/pgedge/spock/configuration/)。

应用工作进程现在遇到死锁或锁超时等临时错误后会重启并重试。如果问题始终不消失，工作进程会每隔 `spock.restart_delay_default`（默认 5 秒）重启，而不是禁用订阅或丢弃事务。

## Spock 5.0.14 {#spock-5014}

### 升级说明 {#upgrade-notes}

* 5.0.14 没有模式变更。

* 在 PostgreSQL 16 及之后版本，建议在每个备库将新增的 `spock.failover_slots_database` 设为 Spock 数据库。这能确保备库在故障切换中提升后，订阅者不遗漏事务。不设置时，主库在故障切换前不久提交的少量事务可能永远不会发送给订阅者。此时槽副本按 5.0.13 的方式同步，并为每个副本发出一次 WARNING。必须指定数据库，因为故障切换槽工作进程每台服务器只运行一个，不属于某个数据库。该设置需要重启。设置后，工作进程会持续连接该数据库，因此 `DROP DATABASE` 和 `ALTER DATABASE ... RENAME` 会失败，除非使用 `WITH (FORCE)` 或清空设置。见[配置 Spock](/pgedge/spock/configuration/)。

* AutoDDL 不再复制未指定表的 CLUSTER、针对分区表的 CLUSTER，以及 PostgreSQL 19 上带 ANALYZE 或 CONCURRENTLY 的 REPACK。这些操作会在执行中途自行提交，破坏应用工作进程。现在仅在发出语句的节点运行，请自行在每个节点执行。滚动升级时，仍运行 5.0.13 的节点仍可能发送这些语句，因此在所有节点升级到 5.0.14 之前，应避免使用或关闭 AutoDDL。

### 错误修复 {#bug-fixes}

* 物理备库上的故障切换槽工作进程过去继续推进已失效的副本，使其看似最新，但提升后无法为订阅者提供服务。现在会报告该副本，删除并从主库重建。新设置 `spock.failover_slots_recreate_invalidated` 可关闭此行为。

* 在备库创建槽副本，过去会阻塞其他所有槽的同步，直到主库槽追上；提升时仍在等待的副本会被保留，却带有无法提供服务的位置。新副本现在保持临时槽状态，直到主库追上；如果备库先提升，则删除它。

* 槽副本携带主库的位置，却没有其快照，提升后，在解码达到一致状态之前提交的事务永远不会被发送。使用新设置 `spock.failover_slots_database` 后，工作进程会在备库解码每个副本，为其建立一致快照。

* PostgreSQL 17 及之后版本上，原生槽同步创建的副本对应的主库槽后来被删除，会使工作进程失败并每分钟重启。现在保留副本并报告一次。

* 如果 `spock.pg_standby_slot_names` 指定的物理槽不存在，但其余槽已满足 `spock.standby_slots_min_confirmed`，过去不会报告缺失槽，walsender 可能静默等待它。现在即使达到所需确认数量，也会在警告中指出缺失槽；重新加载设置、改为指定另一个缺失槽时，会再次警告。

* `spock.pg_standby_slot_names` 中重复列出的槽过去会计数两次。因此，默认 `spock.standby_slots_min_confirmed` 为 -1 时，`'sb1,sb1'` 要求同一个槽提供两次确认，每次尝试都会阻塞复制直到 `wal_sender_timeout`。现在忽略重复名称。

* 即使大多数异常日志条目仍空闲，应用工作进程也可能报错 `unable to find an empty exception log
  slot`，例如不同数据库中的同名订阅同时启动时。该错误还会遗留未释放的 Spock 共享内存锁，使管理工作进程、`spock.sub_create()` 和 `spock.sub_show_status()` 挂起，直到服务器重启。现在仅当日志真正已满时才报错，且先释放锁，工作进程在 `spock.restart_delay_default` 后重启。

* `last_update_wins` 下，传入 UPDATE 过去总会胜过 VACUUM 已冻结的本地行，即使本地变更发生得更晚，也可能使节点最终值不同。PostgreSQL 16 起，VACUUM 可以冻结近期写入的行。Spock 现在通过原始事务 ID 查找冻结行的提交时间戳。

* 通过扩展查询协议（psycopg、JDBC）、带绑定参数调用执行 COMMIT 或 ROLLBACK 的过程，可能使后端崩溃并重启节点。`spock.wait_for_sync_event()` 会执行 ROLLBACK，因此仅从此类客户端等待同步事件就足以触发。Spock 过去在过程释放语句后才读取它；现在在执行前判断语句是否为 DDL。

* 复制未指定表的 CLUSTER 会使订阅者应用工作进程崩溃，导致 postmaster 重启，且每次重启都再次重放该语句。针对分区表的 CLUSTER，以及 PostgreSQL 19 上带 ANALYZE 或 CONCURRENTLY 的 REPACK，也有同类问题或导致工作进程挂起。这些形式不再复制，见升级说明。

* PostgreSQL 19 RC1 改变了 `RelationFindReplTupleByIndex()` 的签名，导致 Spock 无法针对该版本构建。

* 不同 PostgreSQL 大版本的 Debian 调试符号包过去不能同时安装，因为各自都包含相同的 `spockctrl` build-id 文件。`-dbgsym` 包现在不再包含 `spockctrl`。

## Spock 5.0.13 {#spock-5013}

### 升级说明 {#upgrade-notes-1}

* 5.0.13 没有模式变更。

### 错误修复 {#bug-fixes-1}

* 订阅者备库提升后可能重放订阅者已经应用的事务。订阅的复制源未写入 WAL，使备库从最后检查点位置恢复。应用和同步工作进程现在在每次提交后记录复制源进度。

* 等待期间删除订阅，过去会使 `spock.sub_wait_for_sync()` 和 `spock.table_wait_for_sync()` 导致后端崩溃。现在报告订阅不存在。

* 结构同步期间 pg_dump 和 pg_restore 失败，过去会用过期的 `errno` 报告 `Invalid argument` 等消息。现在错误会提供子进程退出码或信号。

* 对早于 5.0.7 的源端执行同步，过去会因缺少 `spock.pause_apply_workers()` 和 `spock.resume_apply_workers()` 报错 `function does not exist`。现在在这种情况下跳过暂停和恢复。

## Spock 5.0.12 {#spock-5012}

### 升级说明 {#upgrade-notes-2}

* 5.0.12 没有模式变更。

* PostgreSQL 2026 年针对 CVE-2026-6471 的安全修复（已回补至所有受支持的大版本）新增 `output_plugin_libraries` 参数。未列在其中的库不能再用作输出插件。默认值不含 `spock_output`，因此带此修复的服务器会在逻辑解码时报错 `library "spock_output" may not be used as an output
  plugin`。每次开始解码都会检查，而不只在创建槽时检查，因此小版本升级后，既有集群也会停止复制，并非只影响新订阅。请在所有支持该参数的节点上（包括物理备库）设置 `output_plugin_libraries = 'pgoutput, test_decoding, spock_output'`；旧版本不识别该参数，设置后会阻止服务器启动。见[配置 Spock](/pgedge/spock/configuration/)。回归与 TAP 测试套件以及 Docker 测试镜像现在会自行检查并设置该参数。

* 应用工作进程因与数据无关的原因失败，例如死锁、锁超时或提供者重启，现在会重启并重试，而非当作异常处理。见错误修复。如果问题持续存在，工作进程会每隔 `spock.restart_delay_default`（默认 5 秒）重启，而非禁用订阅或丢弃事务。

### 错误修复 {#bug-fixes-2}

* 应用工作进程现在会在临时错误后重试。有些错误与复制数据无关：PostgreSQL 选择应用工作进程作为死锁牺牲者、触发 `lock_timeout`、服务器短暂资源耗尽（SQLSTATE 类 53），或提供者正在重启或恢复（57P02、57P03）。这些操作重试即可成功。此前它们与永久数据错误走同一路径，依 `spock.exception_behaviour` 禁用订阅，或将事务写入 `spock.exception_log` 后丢弃，即使提供者完全可以重发。现在工作进程退出时不推进复制源，管理进程重新启动它，由提供者重发事务。所有重启路径，包括已有的连接丢失路径，都先等待 `spock.restart_delay_default`，防止持续问题导致频繁重启。

* 含有 `GENERATED ALWAYS AS ... STORED` 列的表过去会发生复制错误。初始表复制、复制协议、缺失列默认值填充及冲突解决都将生成列当作普通列。现在在各处排除，由订阅者按列定义计算。

* 在事务块之外运行的工具命令（如不带表名的 `CLUSTER`）之后，AutoDDL 过去会失败。这些命令每处理一张表就提交，因此 AutoDDL 钩子运行时已无打开的事务或快照，系统目录查找和队列插入随之失败。现在需要时，AutoDDL 自行开启事务并取得快照。

* `spock.get_lsn_from_commit_ts()` 可能在空闲节点挂起。该函数扫描节点 WAL，查找不晚于给定时间戳的最后一次本地提交，但扫描过去没有终点，追上后便等待无人写入的 WAL。曾观察到 `add_node` 在此调用上卡住超过十一分钟。现在扫描以开始时的 WAL 末尾为终点，从 WAL 记录而非 `pg_commit_ts` 读取提交时间戳和来源，计入其他应用写入的本地两阶段提交，并拒绝在恢复中的服务器运行。没有匹配提交的时间戳仍返回槽的 `restart_lsn`，现在以 DEBUG1 记录。

* 事务之间的失败可能使应用工作进程错误处理下一个事务。事务应用失败后，工作进程重启，提供者重发，再以代码所称的重放模式运行：每行在子事务中尝试，以便将失败行写入 `spock.exception_log`，并由 `spock.exception_behaviour` 决定如何处理。重放模式本应仅用于该事务。但事务之间的错误会在没有对应失败事务时开启重放模式，标志一直保留到提供者发来的下一个事务。该事务从未失败，却按重放执行，在 `TRANSDISCARD` 或 `SUB_DISABLE` 下被丢弃或用于禁用订阅。现在仅对实际失败的事务启用重放模式，其他事务会清除记录的失败状态。

* 没有应用任何内容的重放事务过去仍会提交。`TRANSDISCARD` 和 `SUB_DISABLE` 下，重放中的每行都在始终回滚的子事务中执行，因此不会应用任何行。“已经重放但未遇到错误”的检查却在复制源前进、事务提交后才运行，导致复制源越过从未应用的事务。事务丢失，日志却声称是有意丢弃。现在先检查，并回滚事务，使提供者重发。通过 `spock.sub_alter_skiplsn` 跳过的事务不受此限制。

* 名称具有共同前缀的两个订阅（如 `sub` 和 `sub_parallel`）过去共用一个异常日志槽位，因为查找只比较前几个字符。共用槽位意味着共用标记事务已失败的提交 LSN，因此一个订阅记录的失败可能使另一个订阅对从未失败的事务进入重放模式。现在比较完整名称。同一段代码过去还会读取、并可能写入数组末尾之外的一个条目。

* walreceiver 每次重连主库时，故障切换槽工作进程都可能退出。未设置 `spock.primary_dsn` 时，它从 walreceiver 取得主库连接字符串；walreceiver 在每次连接尝试的整个过程中都会清空该字符串，而不只在备库启动时。连接因此失败，工作进程退出，故障切换槽停止同步，直到重启。现在工作进程等待下一轮。

* 两条串行化失败重试消息从 LOG 降为 DEBUG1，但决定是否按新级别输出的判断写反了。默认设置下，无论 `log_min_messages` 如何，它们都会写入服务器日志。同时，为应用工作进程中有意的 switch 分支贯穿添加标记，避免 clang 在针对 PostgreSQL 19 之前版本的每次构建中都发出警告。

* 事务中途重启应用工作进程可能禁用订阅。工作进程记录每个开始的事务的提交 LSN，而不只记录失败事务；正常关闭曾留下该标记，使提供者重发的中断事务看起来像已经失败。在 `SUB_DISABLE` 下，即使没有实际错误也会禁用订阅。工作进程因 `SIGTERM` 退出时，现在清除此标记。

* 提供者有而订阅者没有的列，过去会使应用工作进程陷入重启循环。错误在打开表时抛出，早于异常处理所需的逐行子事务，因此 `spock.exception_behaviour` 无法介入，每次重试都无限重复。缺失列现在按缺失表处理：首次尝试报错，重试时丢弃变更并通过正常异常路径记录。消息还会列出本地表缺少的全部列，修复模式差异不再需要每次应用只发现一列。

* 使用从网络接收的元组数据之前，现在会对照本地列定义检查。每个属性从消息复制到独立缓冲区，并检查长度；不匹配本地列的元组被拒绝，而非应用。关闭 DDL 复制后仅在提供者执行 `ALTER COLUMN TYPE`，就会如此：应用工作进程退出并重试，直到两端模式一致。也验证 RELATION 消息中的名称和属性数量；未启用 lz4 构建的订阅者现在拒绝 lz4 压缩值，而非将其存储。


### 其他变更 {#other-changes-1}
* 更新 `attoptions` 服务端补丁，以适配 PostgreSQL 17.11、18.5 和 19 beta 3 中的 `heap_update()` 变更。此前一个补丁块的上下文行不再匹配，导致补丁无法应用。本次仅修改了上下文行。

* Spock 可在 PostgreSQL 19 beta 3 和 beta 4 上构建，新增的 `compat/19` 层用于适配该测试版的 API 变更（`CLUSTER` 并入 `REPACK`、恢复冲突信号机制变更、元组描述符定型，以及 `ReorderBufferTXN` 提交时间字段的扁平化）。`CREATE EXTENSION` 接受主版本 19，CI 和发布包也已覆盖该版本。这仍是初步支持：在本文所述阶段，PostgreSQL 19 尚处于测试期，兼容层会在正式发布前继续调整，不支持将 Spock 与 PostgreSQL 19 的这一测试版本组合用于生产环境。

* 发布工作流不再为 Debian bullseye 构建软件包，因为该版本已结束生命周期。

* 移除旧的 Z0DAN Python 文件及其 TAP 测试。`add_node` 和 `remove_node` 由 SQL 实现提供。

* 新增在 PostgreSQL 17 及更高版本上配合 Patroni 使用逻辑复制槽故障切换的文档，涵盖所需参数、应写入引导 DCS 的设置，以及主备切换时如何处理 `synchronized_standby_slots`。Patroni `on_role_change` 回调示例 `samples/set_synchronized_standby_slots.sh` 会在提升后重置 `synchronized_standby_slots`。参见[逻辑复制槽故障切换](/pgedge/spock/logical-slot-failover/)。

* 补充 `spock.wait_for_sync_event()` 的 `wait_if_disabled` 参数说明。

* TAP 测试套件：各测试共用一组日志与等待辅助函数，不再各自保留副本；启动集群时等待服务器就绪，不再固定休眠 17 秒；可使用 `prove` 单独运行一个测试。新增测试覆盖临时错误后的重试、实际死锁、跨事务保留重放模式、`spock.get_lsn_from_commit_ts()`、事务执行中途重启工作进程，以及订阅者缺少列等情况。

## Spock 5.0.11 {#spock-5011}

### 新功能 {#new-features}
* 新增 `spock.use_native_failover_slots`（默认为关闭，PGC_POSTMASTER）。启用后，Spock 在 PG17+ 上为逻辑复制槽设置 FAILOVER 标志；在 PG17 上，当 `sync_replication_slots=on` 时让 PostgreSQL 原生 slotsync 工作进程接管同步；在 PG18+ 上不再注册 Spock 自带的故障切换复制槽工作进程。关闭时保留现有的工作进程实现。该设置在创建逻辑复制槽的订阅者节点上读取，修改后需要重启服务器。配置步骤及提升后必须执行的 `synchronized_standby_slots` 操作流程，参见[逻辑复制槽故障切换](/pgedge/spock/logical-slot-failover/)。

* 默认每 1 秒向备库同步一次故障切换复制槽，取代此前固定的 60 秒，缩短提升时遇到过期复制槽的时间窗口。现在可通过 `spock.failover_slots_naptime` 调整间隔，通过 `spock.failover_slots_feedback_naptime` 调整等待反馈的重试间隔；两者均以毫秒为单位，可通过 SIGHUP 重新加载。

* 通过 `add_node` 加入节点时，不再复制 `pgedge_ace` 模式。ACE 状态仅属于本地节点，因此模式复制与数据同步均排除其中的对象，即使 ACE 表属于复制集也不例外。

### 缺陷修复 {#bug-fixes-3}

* 修复提供者连接短暂中断时，SUB_DISABLE 异常处理可能错误禁用订阅的问题。重连后重新传输的事务不再被误判为应用失败，因此复制会正常恢复，不会停止。


## Spock 5.0.10 {#spock-5010}

### 缺陷修复 {#bug-fixes-4}
* 改善在经常为 NULL 的列上建有唯一索引的表的应用性能。此类键中含 NULL 的行现在会被识别为无冲突，无须进行多余的索引扫描，避免性能随表大小增加而下降。
* 正确处理 `NULLS NOT DISTINCT` 唯一索引上的冲突。在这类索引（PostgreSQL 15+）中，两个 NULL 值被视为相等，因此匹配到 NULL 键的行现在会通过正常的冲突解决机制（最后更新者获胜）处理，不再因重复键错误而失败。
* 修复复制过程中删除索引时，应用工作进程出现 `could not open relation` 错误的问题。现在工作进程在使用表的索引缓存前会先刷新缓存。
* 修复事务向 `spock.exception_log` 写入日志时内存逐渐增长的问题。记录异常所用的内存现在逐行释放，不再累积到事务提交。
* 在 `spock.exception_log` 中记录事务被丢弃的真正原因，取代含义不明的占位值 `unavailable`。现在会保存失败命令的错误消息（在有助于说明问题时，以 SQLSTATE 为前缀），并在同一事务的其他行中注明它们是受牵连而被丢弃，以便查明异常根因。
* 修复 ZODAN（`add_node`）的版本检查。此前按文本比较 Spock 版本，导致 `5.0.10` 排在 `5.0.4` 之前，有效节点被错误拒绝。现在按数值比较版本；只要主版本号和次版本号相同，节点就可以使用不同的补丁版本，从而支持滚动升级。
* 修复单写入者拓扑中时间戳相同的冲突（以及节点 ID 哈希碰撞）错误产生的 "tiebreaker values are equal" 警告。现在决胜比较会比较应用节点与远端发送者，并在创建节点时检测节点 ID 冲突。

## Spock 5.0.9 {#spock-509}

### 新功能 {#new-features-1}
* 初步支持 PostgreSQL 19。新增在 PostgreSQL 19 上构建和运行 Spock 所需的服务端补丁。

### 缺陷修复 {#bug-fixes-5}
* 修复同步备库故障切换后写入被静默丢弃的问题。此前 Spock 可能向发布者报告错误的复制位置，导致提升后的备库从错误位置恢复，丢失其间的变更。现在向发布者报告的位置始终取自发布者自身的 WAL 流。
* 修复 `spock_failover_slots` 在 PG17+ 备库上停滞的问题。复制槽同步可能长时间独占复制槽锁和进程数组锁，阻塞备库上所有尝试启动的后端，使工作进程和新连接都无法继续。现在同步路径使用与 PostgreSQL 自身复制槽代码一致的短时共享锁。
* 修复 Spock 启动数据库工作进程时，若同时删除数据库或禁用其连接（`datconnlimit = -2`），管理工作进程会反复重启的问题。现在会在注册工作进程前立即重新验证数据库 OID，避免竞态。
* 减少应用路径中逐行执行的工作和内存增长。复制变更不再为每一行重新打开表的索引；临时内存逐行释放，不再在事务中不断累积。

### 性能 {#performance}
* 跳过构建不会写入日志的冲突消息。当日志级别屏蔽了相关消息时，Spock 不再为最终会被丢弃的 `ereport()` 格式化冲突行，从而加快高冲突负载下的应用速度。在 `spock.resolutions` 中记录冲突的行为不受影响。

## Spock 5.0.8 {#spock-508}

### 缺陷修复 {#bug-fixes-6}
* 修复事务超过 2 GB 时订阅者崩溃的问题。此前 `apply_replay_bytes` 声明为 `int`，单个复制事务的 WAL 数据超过 2 GB 时会发生有符号整数溢出并导致崩溃。现已改为 `uint64`。
* 上游连接失效（防火墙重载、WAL 发送进程收到 SIGKILL/RST、WAL 发送进程探测超时）时，应用工作进程现在会正常退出，管理进程从最后一个已持久提交的远端 LSN 重新启动它。此前，过期的 libpq 套接字文件描述符会引发一连串 `epoll_ctl()` 错误，每次断连后还会出现 `error during exception handling`；恢复路径中的一种边界情况可能静默地将复制源进度推进到正在处理的远端事务之后，导致重连时跳过该事务。
* 移除原生 PG17+/PG18 复制槽同步集成。Spock 不再使用 (FAILOVER) 创建复制槽，不再将同步交给 PostgreSQL 的 slotsync 工作进程，并在 PG18 上继续启用 spock_failover_slots；在该 5.x 版本中，Spock 工作进程再次成为故障切换复制槽同步的唯一路径。
* spock_failover_slots：处理主库断连和提升后的边界情况。同步期间发生临时故障时会重新连接主库；修复 PG15/16 上的一种 PANIC：刚提升的备库可能因同步复制槽的 restart_lsn 低于备库保留的最早 WAL 位置而陷入崩溃循环；容许此前会触发断言的无效或零值 LSN 和 catalog_xmin。

## Spock 5.0.7 {#spock-507}

### 新功能 {#new-features-2}

逻辑复制槽故障切换改进

* 在 **PostgreSQL 17+** 上，Spock 现在为所有逻辑复制槽设置 `FAILOVER` 标志，使 PostgreSQL 内置 slotsync 工作进程（`sync_replication_slots = on`）能够自动将它们同步到物理备库。
* 在 **PostgreSQL 18+** 上，不再注册 Spock 自带的 `spock_failover_slots` 后台工作进程，完全由 PostgreSQL 原生 slotsync 工作进程替代。所需的 `postgresql.conf` 设置，参见配置指南的[逻辑复制槽故障切换](/pgedge/spock/configuration/#logical-slot-failover-ha-standby)一节。
* 在 **PostgreSQL 17** 上，Spock 工作进程保持启用，但设置了 `sync_replication_slots = on` 时会自动让原生 slotsync 工作进程接管，以避免冲突。

### 缺陷修复 {#bug-fixes-7}
* 在 `TRANSDISCARD` 或 `SUB_DISABLE` 模式下应用变更时，在 `spock.exception_log` 中保留原始错误消息。此前原始错误只写入服务器日志，并在重试前丢失；被丢弃事务的每一行都记录为 `error_message = NULL`（存储为 "unknown"）。现在最初失败的行会携带真实错误消息，同一事务中受牵连的其他行则记录为 "unavailable"，不再使用容易误导的 "unknown" 默认值。
* 修复添加节点时缺少数据的问题。若应用工作进程在 `ensure_replication_slot_snapshot` 与 `adjust_progress_info` 之间提交事务，可能将 `spock.progress` 推进到 COPY 快照边界之后，导致新节点永久跳过这些变更。现在创建复制槽期间，会通过 `SpockContext` 中的原子标志和条件变量暂停应用工作进程，在 `adjust_progress_info` 完成后再恢复。
* 修复提供者连接失效后，应用工作进程因 `epoll_ctl() failed: Invalid argument` 而崩溃的问题。此前在 `stream_replay:` 之前取得的套接字文件描述符一直未更新，再次进入时将过期描述符传给了 `WaitLatchOrSocket`。现在会在 `stream_replay:` 处刷新描述符，工作进程正常退出，由 postmaster 重新启动并连接。
* 修复 PG15/16 提升时故障切换复制槽丢失的问题：重连时进行重试，并防止使用零值的 WAL 刷盘 LSN。
* ZODAN：`create_sub_on_new_node_to_src_node`（`add_node` 的第 9 阶段）此前按 `sub_{subscriber}_{provider}` 生成订阅名，而非预期的 `sub_{provider}_{subscriber}` 约定，导致 `remove_node` 按名称查找订阅时失败。现在用新的辅助函数 `spock.gen_sub_name(provider_node, subscriber_node)` 取代内联名称拼接。
* ZODAN：`remove_node` 清理循环此前靠推测名称和节点来删除订阅；只要 `cross_wire` 和 `add_node` 使用不同的命名约定，就会失败。现在会直接读取 `spock.subscription` 目录，并在各节点上对其中的每个订阅执行 `DROP`。
* 修复自 5.0.2 起 spock.subscription.sub_skip_schema 类型错误的问题；其正确类型应为 text[]。spock-5.0.6--5.0.7.sql 迁移脚本也包含相应修复。
* 修复使用增量应用列时，在高并发下偶尔出现 ResourceOwner 异常的问题。
* 改善 spock.exception_log 中的消息，使其更有助于理解问题。

### 运维改进 {#operational-improvements}
* 文档：补全 `snowflake.md`；修订 `upgrading_spock.md`；修复事件触发器语法（用 `EXECUTE FUNCTION` 替代已弃用的 `EXECUTE PROCEDURE`）；规范函数参考文件名，使其与函数名完全一致；移除过时的 `batch_inserts.md`。
* 测试基础设施与 `main` 对齐：`run_tests.sh` 和 `SpockTest.pm` 现在使用绝对 `TESTLOGDIR` 路径，为每个测试派生日志文件名，并让 `psql` 不受开发者的 `psqlrc` 和历史记录影响。新增回归测试覆盖故障切换复制槽（018）、异常处理/TRANSDISCARD 错误信息质量（013），以及连接失效后使用过期文件描述符的场景（019）。
* 避免在 sync_event() 之后进行不必要的等待。

## Spock 5.0.6 {#spock-506}

### 新功能 {#new-features-3}
* 新增 `spock.feedback_frequency` GUC，控制向 WAL 发送进程发送反馈的频率。每处理 *n* 条消息发送一次反馈，其中 *n* 为配置值。注意，每隔 `wal_sender_timeout / 2` 秒也会发送一次反馈。
* 新增 `spock.log_origin_change` GUC，控制是否在 PostgreSQL 日志中记录行的复制源变更。复制引起的复制源变更仅用于提供信息，不是真正的冲突，因此不再写入 `spock.resolutions` 表。可选模式有三种：
    * `none` — 不记录复制源变更（默认）。
    * `remote_only_differs` — 仅在来自一个远端发布者的行被另一个远端发布者更新时记录。
    * `since_sub_creation` — 记录订阅创建后修改的元组的复制源变更（减少 pg_restore 恢复的数据产生的干扰信息）。
* 在 `spock.subscription` 上新增 `sub_created_at` 列，帮助区分原有数据（例如通过 pg_restore 恢复的数据）与订阅创建后的数据。
* COPY TO 被视为只读操作，现在可以在节点处于只读模式时执行。

### 性能改进 {#performance-improvements}
* 延迟写入 `spock.progress` 目录。此前每次事务提交和每次保活都会更新进度表，造成严重的表膨胀和 I/O 开销。现在会在主应用循环中批量写入进度目录，每秒最多刷写一次。为保证正确性，内部共享内存仍会立即更新。

### 缺陷修复 {#bug-fixes-8}
* 修复 PG15/16/17 的 attoptions 补丁导致 initdb 断言失败的问题。
* 修复表重新同步流程中的两个缺陷：截断和重新同步期间关闭 WAL 发送，防止数据丢失；使用最后提交的 LSN 取代最后接收的 LSN，解决不再提交 DML 时无限等待的问题。
* 无法确定复制源（例如 pg_dump、冻结事务、提交时间戳被截断）时，在 `spock.resolutions` 中将未知的 `local_origin` 记为 NULL，不再使用无效的复制源 ID。同时修复 `spock_conflict_row_to_json()` 中覆盖 `local_origin` NULL 标志的偏一错误。
* 修复 Zodan 初始化问题：`present_final_cluster_state` 现在执行 COMMIT，使新创建的订阅能够更新状态；最终集群状态检查也会检查整个集群的全部订阅。
* 当只读副本用于报表而非故障切换时，不再在日志中输出 hot_standby_feedback 关闭的错误消息（故障切换仍要求启用该设置）。
* 修复向已删除的表应用变更时出现的问题。

### 运维改进 {#operational-improvements-1}
* `add_node` 现在只能在新节点（尚未初始化的节点）上运行，以防误用。

## Spock 5.0.5（2026 年 2 月 12 日） {#spock-505-on-feb-12-2026}

* 修复使用 18.2 等新 PostgreSQL 次版本时发生的段错误。
* 零停机添加节点（Zodan）的小型缺陷修复与改进。
* 更新文档。

## Spock 5.0.4（2025 年 10 月 8 日） {#spock-504-on-oct-8-2025}

* 减少含大量插入操作的事务的内存用量。
* 当订阅者的应用工作进程更新来自同一复制源的行时，Spock 不再在 `spock.resolutions` 表中记录该操作，恢复到 5.0.0 之前的行为。
  - 改善添加扩展时阻止 DDL 复制的处理。
  - 改进文档。
  - 零停机添加节点改进：
    - 在添加节点之前及过程中执行新的健康检查与验证（例如版本兼容性检查）。
    - 新增移除节点的 SQL 过程（samples/Zodan/zodremove.sql 中的 `spock.remove_node()`）和 Python 脚本（samples/Zodan/zodremove.py）。当用户决定撤销操作时，它们也能移除只完成部分添加流程的节点。
    - 处理含引号的 DSN 字符串。

- 缺陷修复：
    - 含凭据的日志消息现在会遮蔽密码信息。
    - 修复订阅者收到针对不存在的表的 DML 时出现的问题。这种情况将按配置的 `spock.exception_behaviour` 设置（`SUB_DISABLE`、`DISCARD`、`TRANSDISCARD`）处理。
    - 修复事务在修复模式下执行时，Spock 错误输出 DDL 已被复制的消息的问题。


## v5.0.3（2025 年 9 月 26 日） {#v503-on-sep-26-2025}

* Spock 5.0.3 新增对 PostgreSQL 18 的支持。
* 在 PostgreSQL 18 上使用行过滤器时（例如在 spock.repset_add_table() 或 spock.repset_add_partition() 中），对允许使用的过滤条件有了更严格的限制。表达式不得使用用户定义函数，也不得引用其他表，与 PostgreSQL 原生逻辑复制的要求类似。

## v5.0.2（2025 年 9 月 22 日） {#v502-on-sept-22-2025}

* 改善存储过程与 Python 示例中 Zodan 各阶段的日志记录。
* 添加节点时，可使用新的 Zodan skip_schema 参数排除模式，防止复制本地扩展元数据。
    * 为 sub_create 新增 skip_schema 选项。当 synchronize_structure = true 时，不同步 skip_schema 中列出的模式。
    * 基于 dblink 的添加节点存储过程使用 skip_schema 跳过新节点上已有的模式，避免因模式已存在而失败。
    * Python add_node 现在与存储过程具有相同的语义，包括 skip_schema 处理、结构同步和日志记录。它可直接替代该过程，且不再需要 dblink 扩展。
* Spock 已改用 PostgreSQL 许可证。



## v5.0.1（2025 年 8 月 27 日） {#v501-on-aug-27-2025}

* 修复更新同一事务中插入的行时使用错误提交时间戳的问题。该问题可能导致更新冲突被错误解决。
* 在 replicate_ddl() 函数中使用默认 search_path。
* 防止使用部分唯一索引时误报冲突。
* 新增零停机添加节点的示例文件。
    * Python 示例。
    * 增强 samples/zodan.sql 中存储过程的添加节点功能。
        * 只有一个节点时添加第二个节点。
        * 扩展对第三个、第四个及后续节点的支持。
        * 以前一个新加入的节点为来源，链式添加后续节点（例如，先从 N1 添加 N2，再从 N2 添加 N3）。

## v5.0（2025 年 7 月 15 日） {#v50-on-july-15-2025}

* Spock 函数和存储过程现在支持添加节点和 PostgreSQL 主版本升级。这意味着：
    * 在向新节点填充数据并将其加入集群期间，现有节点仍可正常读写。
    * 可以添加使用新 PostgreSQL 主版本的节点，再移除使用旧版本的节点，从而滚动完成 PostgreSQL 主版本升级。
* 现在通过 spock.exception_replay_queue_size GUC 控制异常处理的性能优化。
* 此前在源节点估算复制延迟，因此即使没有事务需要复制，报告的延迟仍可能持续增长。现在改为在目标节点计算，精度有所提高。
* Spock 5.0 通过 `spock.sync()` 和 `spock.wait_for_sync_event()` 实现 LSN 检查点机制。利用该功能，可以在源节点 WAL 文件中确定一个检查点，并在副本节点上等待该检查点的 LSN。这样就能保证在发布更新前，DDL 变更已从源节点复制到所有其他节点。
* `spockctrl` 命令行工具与示例工作流简化了 PostgreSQL Spock 多主复制环境的管理。`spockctrl` 为以下操作提供便捷接口：
    * 节点管理。
    * 复制集管理。
    * 订阅管理。
    * 临时 SQL 执行。
    * 工作流自动化。
* 此前，复制的 `DELETE` 语句若尝试删除*不存在*的行，会被记为异常。由于 `DELETE` 的目的是移除一行，现在不再将这种情况记为异常，而是记录到 `Resolutions` 表中。
* 因主键或复制标识重复而产生的 `INSERT` 冲突，现在会转换为 `UPDATE`，依据最后写入者获胜（LWW）规则更新现有行的所有列。随后在节点的 `Resolutions` 表中将该事务记录为以下两种结果之一：
    * `keep local`：本地节点的 `INSERT` 时间戳晚于收到的 `INSERT`。
    * `apply remote`：来自远端节点的 `INSERT` 时间戳更晚。
* 在包含分布式节点与物理副本节点的集群中，Spock 5.0 会跟踪已在本地应用、仍在等待物理副本确认的事务的日志序列号（LSN），从而改善性能。只有物理副本确认这些 LSN 后，才会给出最终的 `COMMIT` 确认。这构成了两阶段确认：
   * 目标节点接收并应用事务时确认一次。
   * 物理副本确认提交时再确认一次。
* `spock.check_all_uc_indexes` GUC 是实验性功能（默认 `disabled`），使用者需自行承担风险。将该 GUC 设为 `enabled` 后，Spock 在检查主键/复制标识索引之后，会继续检查唯一约束索引。只会依据最后写入者获胜规则解决一个冲突；如果出现第二个冲突，就在 `spock.exception_log` 表中记录异常。


## 版本 4.1 {#version-41}
* 强化并行复制槽，使其适用于 OLTP 生产环境。
  - 提交顺序。
  - 跳过 LSN。
  - 可选择在出错时停止复制。
* 增强自动 DDL 复制。

## 版本 4.0 {#version-40}

* 全面重构并行复制槽实现，以支持混合 OLTP 负载。
* 改善 delta_apply 列对多种数据类型的支持。
* 扩大回归测试覆盖范围。
* 支持[大对象逻辑复制](https://github.com/pgedge/lolor)。
* 支持 pg17。

上游在此处保留的 v3.3 生产版本说明列出了相对于 v3.2 的以下增强：

* 自动复制 DDL 语句。

## 版本 3.2 {#version-32}

* 支持 pg14。
* 支持 [Snowflake 序列](https://github.com/pgedge/snowflake)。
* 支持将数据库设为只读。
* 纳入 pgLogical 的几项小型缺陷修复。
* 通过集成 pg_failover_slots 扩展，原生支持故障切换复制槽。
* 为仅插入的负载提供并行复制槽支持。

## 版本 3.1 {#version-31}

* 同时支持 pg15 *和* pg16。
* 初步测试 pg15 与 pg16 之间的在线升级。
* 改善回归测试。
* 改善对同一区域内不同可用区的影子节点的支持。
* 改善对分区表复制与维护的支持，并补充文档。

**版本 3.0（Beta）** 在 BDR/pg_logical 基础上包含以下重要增强：

* 支持 pg15（不再支持 pg10 至 pg14）。
* 支持带冲突解决的异步多主复制。
* 无冲突的增量应用列。
* 复制分区表（以支持地理分片）。
* 使数据库集群具备位置感知能力（以支持地理分片）。
* 改善冲突解决过程中的错误处理。
* 改善管理、监控统计信息及集成。
* 提供 'pii' 表，便于将个人身份信息保留在本国境内。
* 改善对主备切换和故障切换的支持，尽可能缩短系统中断。

---

[上游来源](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_release_notes.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/pgedge/about/license/)。
