---
title: "gp_toolkit 管理模式"
linkTitle: "gp_toolkit"
description: "Apache Cloudberry 提供名为 `gp_toolkit` 的管理模式，可用于查询系统目录、日志文件和运行环境，获取系统状态信息。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/gp_toolkit.md"
---

`gp_toolkit` 模式包含多个可通过 SQL 命令访问的视图。所有数据库用户都可以访问 `gp_toolkit` 模式，但其中一些对象可能需要超级用户权限。为方便使用，可以将 `gp_toolkit` 模式加入模式搜索路径。例如：

```sql
=> ALTER ROLE myrole SET search_path TO myschema,gp_toolkit;
```

本文介绍 `gp_toolkit` 中最有用的视图和用户定义函数（UDF）。你可能会注意到，`gp_toolkit` 模式中还有本文未介绍的其他对象（视图、函数和外部表）；这些对象用于支持本节介绍的视图。

> [!WARNING]
> 不要修改 gp_toolkit 模式中的数据库对象，也不要在此模式中创建数据库对象。修改此模式中的对象可能会影响这些对象返回的管理信息的准确性。使用 `gpbackup` 和 `gprestore` 工具备份并恢复数据库后，对 gp_toolkit 模式所做的任何更改都会丢失。

`gp_toolkit` 模式中的视图分为以下类别。

- [检查需要例行维护的表](#check-for-tables-that-need-routine-maintenance)
- [检查锁](#check-for-locks)
- [检查 AO 表](#check-append-optimized-tables)
- [查看服务器日志文件](#view-server-log-files)
- [检查服务器配置文件](#check-server-configuration-files)
- [检查故障 Segment](#check-for-failed-segments)
- [检查资源组活动和状态](#check-resource-group-activity-and-status)
- [检查资源队列活动和状态](#check-resource-queue-activity-and-status)
- [检查查询的磁盘溢出空间使用情况](#check-query-disk-spill-space-usage)
- [查看用户和组（角色）](#view-users-and-groups-roles)
- [检查数据库对象大小和磁盘空间](#check-database-object-sizes-and-disk-space)
- [检查缺失和孤立的数据文件](#check-for-missing-and-orphaned-data-files)
- [移动孤立的数据文件](#move-orphaned-data-files)
- [检查数据分布是否均匀](#check-for-uneven-data-distribution)
- [维护分区](#maintain-partitions)

## 关于扩展 {#about-the-extension}

在 Apache Cloudberry v2.0.0 中，`gp_toolkit` 以扩展形式实现。由于此扩展已在 `template1` 数据库中注册，因此你创建的每个 Apache Cloudberry 数据库都会注册此扩展，并可立即使用。

## 升级扩展 {#upgrade-the-extension}

安装或升级 Apache Cloudberry 时会安装 `gp_toolkit` 扩展。升级 Apache Cloudberry 后，已有数据库中的旧版扩展仍可继续使用。要升级到最新版本，必须执行：

```sql
ALTER EXTENSION gp_toolkit UPDATE TO '1.4';
```

需在使用此扩展的**每一个**数据库中执行。

## 检查需要例行维护的表 {#check-for-tables-that-need-routine-maintenance}

以下视图有助于识别需要例行维护（`VACUUM` 和／或 `ANALYZE`）的表。

- [`gp_bloat_diag`](#gp_bloat_diag)
- [`gp_stats_missing`](#gp_stats_missing)

`VACUUM` 或 `VACUUM FULL` 命令回收已删除行或过时行占用的磁盘空间。由于 Apache Cloudberry 使用 MVCC 事务并发模型，已删除或更新的数据行即使对任何新事务都不可见，仍会占用磁盘上的物理空间。过时行会增大表的磁盘占用，最终拖慢表扫描。

`ANALYZE` 命令收集查询优化器所需的列级统计信息。Apache Cloudberry 使用基于代价的查询优化器，依赖数据库统计信息。准确的统计信息使查询优化器能够更好地估计选择率和查询操作检索的行数，从而选择最高效的查询计划。

### gp_bloat_diag {#gp_bloat_diag}

此视图显示存在膨胀的普通堆存储表（磁盘上的实际页数超过根据表统计信息估算的预期页数）。膨胀的表需要执行 `VACUUM` 或 `VACUUM FULL`，以回收已删除行或过时行占用的磁盘空间。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的表。

注意

有关返回 AO 表信息的诊断函数，参见[检查 AO 表](#check-append-optimized-tables)。

此视图的列说明如下：

- `bdirelid`：表的对象 ID。
- `bdinspname`：模式名称。
- `bdirelname`：表名称。
- `bdirelpages`：磁盘上的实际页数。
- `bdiexppages`：根据表数据估算的预期页数。
- `bdidiag`：膨胀诊断消息。

### gp_stats_missing {#gp_stats_missing}

此视图显示没有统计信息的表，因此这些表可能需要运行 `ANALYZE`。

此视图的列说明如下：

- `smischema`：模式名称。
- `smitable`：表名称。
- `smisize`：此表是否有统计信息。如果系统目录中未记录此表的行数和行大小统计信息，则为 false，这可能表示需要分析此表。如果表中没有任何行，此值也为 false。例如，分区表的父表始终为空，因此始终返回 false。
- `smicols`：表中的列数。
- `smirecs`：表中已记录统计信息的列的总数。

## 检查锁 {#check-for-locks}

事务访问关系（例如表）时会获取锁。根据所获取锁的类型，后续事务可能需要等待，才能访问同一关系。有关锁类型的更多信息，参见[事务](/cloudberry/operate-with-data/transactional-concurrency-control/#lock-modes)。Apache Cloudberry 的资源队列（用于资源管理）也使用锁来控制查询进入系统。

`gp_locks_*` 系列视图有助于诊断因锁而等待访问对象的查询和会话。

- [`gp_locks_on_relation`](#gp_locks_on_relation)
- [`gp_locks_on_resqueue`](#gp_locks_on_resqueue)

### gp_locks_on_relation {#gp_locks_on_relation}

此视图显示关系上当前持有的所有锁，以及与锁相关的查询的会话信息。有关锁类型的更多信息，参见[事务](/cloudberry/operate-with-data/transactional-concurrency-control/#lock-modes)。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的关系上的锁。

此视图的列说明如下：

- `lorlocktype`：可锁定对象的类型：`relation`、`extend`、`page`、`tuple`、`transactionid`、`object`、`userlock`、`resource queue` 或 `advisory`。
- `lordatabase`：对象所在数据库的对象 ID；如果是共享对象，则为零。
- `lorrelname`：关系的名称。
- `lorrelation`：关系的对象 ID。
- `lortransaction`：受此锁影响的事务 ID。
- `lorpid`：持有或等待此锁的服务器进程的进程 ID。如果锁由已准备事务持有，则为 `NULL`。
- `lormode`：此进程持有或希望获取的锁模式名称。
- `lorgranted`：显示锁是否已授予：已授予为 `true`，未授予为 `false`。
- `lorcurrentquery`：会话中的当前查询。

### gp_locks_on_resqueue {#gp_locks_on_resqueue}

> [!NOTE]
> 只有启用基于资源队列的资源管理时，`gp_locks_on_resqueue` 视图才有效。

此视图显示资源队列上当前持有的所有锁，以及与锁相关的查询的会话信息。所有用户均可访问此视图，但非超级用户只能看到与自己会话相关的锁。

此视图的列说明如下：

- `lorusename`：运行会话的用户名称。
- `lorrsqname`：资源队列名称。
- `lorlocktype`：可锁定对象的类型：`resource queue`。
- `lorobjid`：被锁定事务的 ID。
- `lortransaction`：受此锁影响的事务 ID。
- `lorpid`：受此锁影响的事务的进程 ID。
- `lormode`：此进程持有或希望获取的锁模式名称。
- `lorgranted`：显示锁是否已授予：已授予为 `true`，未授予为 `false`。
- `lorwaiteventtype`：等待事件的类型（例如 I/O、锁、网络）。
- `lorwaitevent`：等待事件的名称或描述（例如文件的 I/O 操作或锁对象）。

## 检查 AO 表 {#check-append-optimized-tables}

`gp_toolkit` 模式包含一组诊断函数，可用于检查 AO 表的状态。

创建 AO 表（或列存 AO 表）时，会隐式创建另一个表，其中包含原表当前状态的元数据。元数据包括表的各个段中的记录数等信息。

AO 表中可能存在不可见行，即已经更新或删除、但在使用 `VACUUM` 压实表之前仍保留在存储中的行。这些隐藏行通过一个辅助的可见性映射表（visimap）来跟踪。

以下函数可用于访问 AO 表和列存表的元数据，以及查看不可见行。

大多数函数的输入参数为 `regclass`，可以是表的 `name` 或表的 `oid`。

### __gp_aovisimap_compaction_info(oid) {#__gp_aovisimap_compaction_infooid}

此函数显示 AO 表的压实信息。这些信息针对数据库 Segment 上存储表数据的磁盘数据文件。可以据此确定对 AO 表执行 `VACUUM` 时会压实哪些数据文件。

> [!NOTE]
> 在 `VACUUM` 操作从数据文件中删除行之前，已删除或更新的数据行即使对新事务不可见，仍会占用磁盘上的物理空间。配置参数 `gp_appendonly_compaction` 控制 `VACUUM` 命令的这一功能。

下表描述 `__gp_aovisimap_compaction_info` 函数的输出表。此表的列说明如下：

- `content`：数据库 Segment ID。
- `datafile`：Segment 上的数据文件 ID。
- `compaction_possible`：值为 `t` 或 `f`。`t` 表示执行 VACUUM 操作时会压实此数据文件中的数据。服务器配置参数 `gp_appendonly_compaction_threshold` 会影响此值。
- `hidden_tupcount`：数据文件中隐藏行（已删除或更新的行）的数量。
- `total_tupcount`：数据文件中的总行数。
- `percent_hidden`：数据文件中隐藏行（已删除或更新的行）占总行数的比例，以百分比表示。

### __gp_aoseg(regclass) {#__gp_aosegregclass}

此函数返回 AO 表的磁盘段文件中包含的元数据信息。

输入参数为 AO 表的名称或 OID。输出列的说明如下：

- `segment_id`：集群中数据 Segment 的 ID。
- `segno`：文件段编号。
- `eof`：此文件段的有效文件末尾位置。
- `tupcount`：段中的元组总数，包括不可见元组。
- `varblockcount`：文件段中 varblock 的总数。
- `eof_uncompressed`：文件段在未压缩情况下的文件末尾位置。
- `modcount`：数据修改操作的次数。
- `formatversion`：AO 文件存储格式的版本，表示文件采用的格式版本。
- `state`：文件段的状态，表示该段处于活动状态，还是已在压实后准备好删除。

### __gp_aoseg_history(regclass) {#__gp_aoseg_historyregclass}

此函数返回 AO 表的磁盘段文件中包含的元数据信息。它显示 aoseg 元信息的所有不同版本（堆元组）。这些数据较为复杂，但深入了解系统的用户可能会发现它们有助于调试。

输入参数为 AO 表的名称或 OID。输出列的说明如下：

- `segment_id`：集群中数据 Segment 的 ID。
- `segno`：段文件中的段编号。
- `tupcount`：元组数量，包括隐藏元组。
- `eof`：该段的有效文件末尾位置。
- `eof_uncompressed`：数据在未压缩情况下该段的文件末尾位置。
- `modcount`：数据修改次数。
- `formatversion`：AO 文件存储格式的版本，表示文件采用的格式版本。
- `state`：段的状态。

### __gp_aocsseg(regclass) {#__gp_aocssegregclass}

此函数返回列存 AO 表的磁盘段文件中包含的元数据信息，不包括不可见行。每一行描述表中某一列的一个段。

输入参数为列存 AO 表的名称或 OID。输出列的说明如下：

- `segment_id`：集群中数据 Segment 的 ID。
- `segno`：段编号。
- `column_num`：列编号。
- `physical_segno`：段文件中的段编号。
- `tupcount`：段中的行数，不包括隐藏元组。
- `eof`：该段的有效文件末尾位置。
- `eof_uncompressed`：数据在未压缩情况下该段的文件末尾位置。
- `modcount`：该段的数据修改操作次数。
- `formatversion`：AO 文件存储格式的版本，表示文件采用的格式版本。
- `state`：段的状态。

### __gp_aocsseg_history(regclass) {#__gp_aocsseg_historyregclass}

此函数返回列存 AO 表的磁盘段文件中包含的元数据信息。每一行描述表中某一列的一个段。这些数据较为复杂，但深入了解系统的用户可能会发现它们有助于调试。

输入参数为列存 AO 表的名称或 OID。输出列的说明如下：

- `segment_id`：集群中数据 Segment 的 ID。
- `segno`：段文件中的段编号。
- `column_num`：列编号。
- `physical_segno`：包含该列数据的段。
- `tupcount`：段中的元组总数。
- `eof`：该段的有效文件末尾位置。
- `eof_uncompressed`：数据在未压缩情况下该段的文件末尾位置。
- `modcount`：数据修改操作的次数。
- `formatversion`：AO 文件存储格式的版本，表示文件采用的格式版本。
- `state`：段的状态。

### __gp_aovisimap(regclass) {#__gp_aovisimapregclass}

此函数根据可见性映射返回每个不可见元组的元组 ID、段文件和行号。

输入参数为 AO 表的名称或 OID。输出列的说明如下：

- `tid`：元组 ID。
- `segno`：段文件编号。
- `row_num`：已删除或更新的行的行号。

### __gp_aovisimap_hidden_info(regclass) {#__gp_aovisimap_hidden_inforegclass}

此函数返回 AO 表各段文件中隐藏元组和可见元组的数量。

输入参数为 AO 表的名称或 OID。输出列的说明如下：

- `segno`：段文件编号。
- `hidden_tupcount`：段文件中的隐藏元组数量。
- `total_tupcount`：段文件中的元组总数。

### __gp_aovisimap_entry(regclass) {#__gp_aovisimap_entryregclass}

此函数返回表的每个可见性映射条目的信息。

输入参数为 AO 表的名称或 OID。输出列的说明如下：

- `segno`：可见性映射条目的段编号。
- `first_row_num`：此条目的第一个行号。
- `hidden_tupcount`：此条目中的隐藏元组数量。
- `bitmap`：可见性位图的文本表示。

### __gp_aoblkdir(regclass) {#__gp_aoblkdirregclass}

对于曾经或当前具有索引的指定 AO/AOCO 表，此函数为块目录关系中记录的每个块目录条目返回一行；它展开块目录关系的 `minipage` 列，为每个 `minipage` 条目返回一行。

输入参数为 AO 表的名称或 OID。

必须在 utility 模式下对每个 Segment 执行此函数，或按如下方式使用 `gp_dist_random()`：

```sql
SELECT (gp_toolkit.__gp_aoblkdir('<table_name>')).*
    FROM gp_dist_random('gp_id');
```

输出列的说明如下：

- `tupleid`：包含此块目录条目的块目录行的元组 ID。
- `segno`：物理段文件编号。
- `columngroup_no`：此 `minipage` 条目所描述列的 `attnum`（对于行存表始终为 `0`）。
- `entry_no`：此块目录条目在其所在 `minipage` 内的条目序号。
- `first_row_no`：此块目录条目所涵盖行中的第一个行号。
- `file_offset`：此块目录条目所涵盖行的起始文件偏移量。
- `row_count`：此块目录条目涵盖的行数。

### get_column_size(oid) {#get_column_sizeoid}

对于指定的 AOCO 表，此函数返回表中所有列的列大小和压缩比。

输入参数为列存 AO 表的对象标识符。输出列的说明如下：

- `segment`：Segment ID。
- `attnum`：列的属性编号。
- `size`：列的大小，以字节为单位。
- `size_uncompressed`：列在未压缩情况下的大小，以字节为单位。
- `compression_ratio`：压缩比。

### gp_column_size {#gp_column_size}

此视图收集所有 Segment 上列存 AO 表的列大小和压缩比。视图的列说明如下：

- `gp_segment_id`：Segment ID。
- `relid`：表的对象标识符（OID）。
- `schema`：表所属的模式。
- `relname`：表名称。
- `attnum`：列的属性编号。
- `attname`：列名称。
- `size`：列的大小，以字节为单位。
- `size_uncompressed`：列在未压缩情况下的大小，以字节为单位。
- `compression_ratio`：压缩比。

### gp_column_size_summary {#gp_column_size_summary}

此视图显示 `gp_column_size` 视图的汇总信息，将所有 Segment 上每个列存 AO 表中各列的大小和压缩比汇总起来。视图的列说明如下：

- `relid`：表的对象标识符（OID）。
- `schema`：表所属的模式。
- `relname`：表名称。
- `attnum`：列的属性编号。
- `attname`：列名称。
- `size`：列的大小，以字节为单位。
- `size_uncompressed`：列在未压缩情况下的大小，以字节为单位。
- `compression_ratio`：压缩比。

## 查看服务器日志文件 {#view-server-log-files}

Apache Cloudberry 系统中的每个组件（Coordinator、Standby Coordinator、主 Segment 和镜像 Segment）都保存自己的服务器日志文件。`gp_log_*` 系列视图允许对服务器日志文件执行 SQL 查询，查找感兴趣的特定条目。使用这些视图需要超级用户权限。

- [`gp_log_command_timings`](#gp_log_command_timings)
- [`gp_log_database`](#gp_log_database)
- [`gp_log_coordinator_concise`](#gp_log_coordinator_concise)
- [`gp_log_system`](#gp_log_system)

### gp_log_command_timings {#gp_log_command_timings}

此视图使用外部表读取 Coordinator 上的日志文件，报告数据库会话中 SQL 命令的运行时间。使用此视图需要超级用户权限。视图的列说明如下：

- `logsession`：会话标识符（以 "con" 为前缀）。
- `logcmdcount`：会话中的命令编号（以 "cmd" 为前缀）。
- `logdatabase`：数据库名称。
- `loguser`：数据库用户名称。
- `logpid`：进程 ID（以 "p" 为前缀）。
- `logtimemin`：此命令第一条日志消息的时间。
- `logtimemax`：此命令最后一条日志消息的时间。
- `logduration`：语句从开始到结束的持续时间。

### gp_log_database {#gp_log_database}

此视图使用外部表读取整个 Apache Cloudberry 系统（Coordinator、Segment 和镜像）的服务器日志文件，列出与当前数据库关联的日志条目。可以通过会话 ID（logsession）和命令 ID（logcmdcount）识别相关的日志条目。使用此视图需要超级用户权限。视图的列说明如下：

- `logtime`：日志消息的时间戳。
- `loguser`：数据库用户名称。
- `logdatabase`：数据库名称。
- `logpid`：关联的进程 ID（以 "p" 为前缀）。
- `logthread`：关联的线程计数（以 "th" 为前缀）。
- `loghost`：Segment 或 Coordinator 的主机名。
- `logport`：Segment 或 Coordinator 的端口。
- `logsessiontime`：会话连接建立的时间。
- `logtransaction`：全局事务 ID。
- `logsession`：会话标识符（以 "con" 为前缀）。
- `logcmdcount`：会话中的命令编号（以 "cmd" 为前缀）。
- `logsegment`：Segment 的内容标识符（主实例以 "seg" 为前缀，镜像以 "mir" 为前缀。Coordinator 的内容 ID 始终为 -1）。
- `logslice`：切片 ID（正在运行的查询计划的一部分）。
- `logdistxact`：分布式事务 ID。
- `loglocalxact`：本地事务 ID。
- `logsubxact`：子事务 ID。
- `logseverity`：LOG、ERROR、FATAL、PANIC、DEBUG1 或 DEBUG2。
- `logstate`：与日志消息关联的 SQL 状态码。
- `logmessage`：日志或错误消息文本。
- `logdetail`：与错误消息关联的详细消息文本。
- `loghint`：与错误消息关联的提示文本。
- `logquery`：内部生成的查询文本。
- `logquerypos`：光标在内部生成的查询文本中的位置。
- `logcontext`：生成此消息时的上下文。
- `logdebug`：包含完整细节、用于调试的查询字符串。
- `logcursorpos`：光标在查询字符串中的位置。
- `logfunction`：生成此消息的函数。
- `logfile`：生成此消息的日志文件。
- `logline`：生成此消息的日志文件行号。
- `logstack`：与此消息关联的堆栈跟踪全文。

### gp_log_coordinator_concise {#gp_log_coordinator_concise}

此视图使用外部表读取 Coordinator 日志文件中的部分日志字段。使用此视图需要超级用户权限。视图的列说明如下：

- `logtime`：日志消息的时间戳。
- `logdatabase`：数据库名称。
- `logsession`：会话标识符（以 "con" 为前缀）。
- `logcmdcount`：会话中的命令编号（以 "cmd" 为前缀）。
- `logseverity`：日志严重级别。
- `logmessage`：日志或错误消息文本。

### gp_log_system {#gp_log_system}

此视图使用外部表读取整个 Apache Cloudberry 系统（Coordinator、Segment 和镜像）的服务器日志文件，列出所有日志条目。可以通过会话 ID（logsession）和命令 ID（logcmdcount）识别相关的日志条目。使用此视图需要超级用户权限。视图的列说明如下：

- `logtime`：日志消息的时间戳。
- `loguser`：数据库用户名称。
- `logdatabase`：数据库名称。
- `logpid`：关联的进程 ID（以 "p" 为前缀）。
- `logthread`：关联的线程计数（以 "th" 为前缀）。
- `loghost`：Segment 或 Coordinator 的主机名。
- `logport`：Segment 或 Coordinator 的端口。
- `logsessiontime`：会话连接建立的时间。
- `logtransaction`：全局事务 ID。
- `logsession`：会话标识符（以 "con" 为前缀）。
- `logcmdcount`：会话中的命令编号（以 "cmd" 为前缀）。
- `logsegment`：Segment 的内容标识符（主实例以 "seg" 为前缀，镜像以 "mir" 为前缀。Coordinator 的内容 ID 始终为 -1）。
- `logslice`：切片 ID（正在运行的查询计划的一部分）。
- `logdistxact`：分布式事务 ID。
- `loglocalxact`：本地事务 ID。
- `logsubxact`：子事务 ID。
- `logseverity`：LOG、ERROR、FATAL、PANIC、DEBUG1 或 DEBUG2。
- `logstate`：与日志消息关联的 SQL 状态码。
- `logmessage`：日志或错误消息文本。
- `logdetail`：与错误消息关联的详细消息文本。
- `loghint`：与错误消息关联的提示文本。
- `logquery`：内部生成的查询文本。
- `logquerypos`：光标在内部生成的查询文本中的位置。
- `logcontext`：生成此消息时的上下文。
- `logdebug`：包含完整细节、用于调试的查询字符串。
- `logcursorpos`：光标在查询字符串中的位置。
- `logfunction`：生成此消息的函数。
- `logfile`：生成此消息的日志文件。
- `logline`：生成此消息的日志文件行号。
- `logstack`：与此消息关联的堆栈跟踪全文。

## 检查服务器配置文件 {#check-server-configuration-files}

Apache Cloudberry 系统中的每个组件（Coordinator、Standby Coordinator、主 Segment 和镜像 Segment）都有自己的服务器配置文件（`postgresql.conf`）。以下 `gp_toolkit` 对象可用于检查系统中所有主实例的 `postgresql.conf` 文件中的参数设置：

- [`gp_param_setting('parameter_name')`](#gp_param_settingparameter_name)
- [`gp_param_settings_seg_value_diffs`](#gp_param_settings_seg_value_diffs)

### gp_param_setting('parameter_name') {#gp_param_settingparameter_name}

此函数接受服务器配置参数的名称，返回 Coordinator 和各活动 Segment 的 `postgresql.conf` 中的值。所有用户均可访问此函数。视图的列说明如下：

- `paramsegment`：Segment 内容 ID（仅显示活动 Segment）。Coordinator 的内容 ID 始终为 -1。
- `paramname`：参数名称。
- `paramvalue`：参数值。

示例：

```sql
SELECT * FROM gp_toolkit.gp_param_setting('max_connections');
```

### gp_param_settings_seg_value_diffs {#gp_param_settings_seg_value_diffs}

归类为*本地*参数的服务器配置参数（即每个 Segment 从自己的 `postgresql.conf` 文件中获取参数值）应在所有 Segment 上设置为相同值。此视图显示不一致的本地参数设置。原本就应该具有不同值的参数（例如 `port`）不包含在内。所有用户均可访问此视图。

视图的列说明如下：

- `psdname`：参数名称。
- `psdvalue`：参数值。
- `psdcount`：使用此值的 Segment 数量。

## 检查故障 Segment {#check-for-failed-segments}

[`gp_pgdatabase_invalid`](#gp_pgdatabase_invalid) 视图可用于检查已停止运行的 Segment。

### gp_pgdatabase_invalid {#gp_pgdatabase_invalid}

此视图显示系统目录中标记为停止运行的 Segment 的信息。所有用户均可访问此视图。视图的列说明如下：

- `pgdbidbid`：Segment 的 dbid。每个 Segment 都有唯一的 dbid。
- `pgdbiisprimary`：此 Segment 当前是否充当主（活动）Segment（t 或 f）。
- `pgdbicontent`：此 Segment 的内容 ID。主实例及其镜像具有相同的内容 ID。
- `pgdbivalid`：此 Segment 是否正在运行且有效（t 或 f）。
- `pgdbidefinedprimary`：系统初始化时，此 Segment 是否被分配为主实例（t 或 f）。

## 检查资源组活动和状态 {#check-resource-group-activity-and-status}

注意

本节介绍的资源组活动和状态视图仅在启用基于资源组的资源管理时有效。

资源组通过管理事务来避免耗尽系统的 CPU 和内存资源。每个数据库用户都会分配一个资源组。对于用户提交的每个事务，Apache Cloudberry 都会先根据该用户资源组配置的限制进行评估，然后才运行事务。

可以使用 `gp_resgroup_config` 视图检查各资源组的配置。可以使用 `gp_resgroup_status*` 视图显示各资源组当前的事务状态和资源使用情况。

- [`gp_resgroup_config`](#gp_resgroup_config)
- [`gp_resgroup_role`](#gp_resgroup_role)
- [`gp_resgroup_status`](#gp_resgroup_status)
- [`gp_resgroup_status_per_host`](#gp_resgroup_status_per_host)
- [`gp_resgroup_status_per_segment`](#gp_resgroup_status_per_segment)

### gp_resgroup_config {#gp_resgroup_config}

`gp_resgroup_config` 视图允许管理员查看资源组当前的 CPU、内存和并发限制。

所有用户均可访问此视图。视图的列说明如下：

- `groupid`：资源组的 ID。
- `groupname`：资源组的名称。
- `concurrency`：为资源组指定的并发值（`CONCURRENCY`）。
- `cpu_max_percent`：为资源组指定的 CPU 限制值（`CPU_MAX_PERCENT`），或 `-1`。
- `cpu_weight`：资源组的调度优先级（`CPU_WEIGHT`）。
- `cpuset`：为资源组保留的 CPU 核心（CPUSET），或 -1。
- `memory_quota`：为资源组指定的内存限制值。
- `min_cost`：查询计划被纳入资源组管理所需的最低代价（`MIN_COST`）。
- `io_limit`：分配给特定表空间（以表空间 OID 显示）和资源组的查询所能使用的最大顺序磁盘读写 I/O 吞吐量，以及每秒最大读写 I/O 操作数（`IO_LIMIT`）。

### gp_resgroup_role {#gp_resgroup_role}

`gp_resgroup_role` 视图允许管理员查看每个角色分配到的资源组。

所有用户均可访问此视图。视图的列说明如下：

- `rrrolname`：角色名称。
- `rrrsgname`：资源组名称。

### gp_resgroup_status {#gp_resgroup_status}

`gp_resgroup_status` 视图允许管理员查看资源组的状态和活动。它显示各资源组中有多少查询正在等待运行，以及有多少查询当前在系统中处于活动状态。此视图还显示资源组当前的内存和 CPU 使用情况。

> [!NOTE]
> 资源组使用主机系统上配置的 Linux 控制组（cgroups）。cgroups 用于管理主机系统资源。如果资源组使用的 cgroup 位于嵌套的 cgroup 集合中，资源组限制就是相对于父 cgroup 的资源配额而言的。有关嵌套 cgroups 和 Apache Cloudberry 资源组限制的信息，参见*使用资源组*文档。

所有用户均可访问此视图。视图的列说明如下：

- `groupid`：资源组的 ID。
- `groupname`：资源组的名称。
- `num_running`：资源组中当前正在运行的事务数量。
- `num_queueing`：资源组中当前排队的事务数量。
- `num_queued`：自 Apache Cloudberry 集群上次启动以来，资源组中排过队的事务总数，不包括 num_queueing。
- `num_executed`：自 Apache Cloudberry 集群上次启动以来，资源组中运行过的事务总数，不包括 num_running。
- `total_queue_duration`：自 Apache Cloudberry 集群上次启动以来，所有事务的排队时间总和。

`gp_resgroup_status` 视图的示例输出：

```sql
select * from gp_toolkit.gp_resgroup_status;

groupid | groupname | num_running | num_queueing | num_queued | num_executed | total_queue_duration 
---------+-----------+-------------+--------------+------------+--------------+----------------------
(0 rows)
```

### gp_resgroup_status_per_host {#gp_resgroup_status_per_host}

`gp_resgroup_status_per_host` 视图按主机显示各资源组的实时 CPU 和内存使用量（MB）。此视图还显示主机上各资源组可用和已授予的组固定内存及共享内存。

视图的列说明如下：

- `groupid`：资源组的 ID。
- `groupname`：资源组的名称。
- `hostname`：Segment 主机的主机名。
- `cpu_usage`：资源组在某台主机上的实时 CPU 核心使用量。此值为资源组在该主机上所用各 CPU 核心的使用百分比之和（浮点值）。
- `memory_usage`：资源组在各数据库 Segment 所在主机上的实时内存使用量，以 MB 为单位。

`gp_resgroup_status_per_host` 视图的示例输出：

```sql
select * from gp_toolkit.gp_resgroup_status_per_host;

groupid | groupname | hostname | cpu_usage | memory_usage 
---------+-----------+----------+-----------+--------------
(0 rows)
```

### gp_resgroup_status_per_segment {#gp_resgroup_status_per_segment}

`gp_toolkit.gp_resgroup_status_per_segment` 视图按资源组显示各 Segment 上的内存使用情况。统计信息由 vmem 跟踪器报告，以 MB 为单位。此视图有助于数据库管理员监控各 Segment 上资源组的内存消耗。

注意

此视图仅在启用基于资源组的资源管理时可用。

列说明：

- `groupid`（类型：`oid`）：资源组的唯一标识符，对应 `pg_resgroup.oid`。
- `groupname`（类型：`name`）：资源组名称，对应 `pg_resgroup.rsgname`。
- `segment_id`（类型：`smallint`）：相应 Segment 实例的内容 ID，取自 `gp_segment_configuration.content`。
- `vmem_usage`（类型：`smallint`）：资源组在相应 Segment 上的实时内存使用量（以 MB 为单位）。

## 检查资源队列活动和状态 {#check-resource-queue-activity-and-status}

> [!NOTE]
> 本节介绍的资源队列活动和状态视图仅在启用基于资源队列的资源管理时有效。

资源队列的目的是限制系统在任意时刻的活动查询数量，避免耗尽内存、CPU 和磁盘 I/O 等系统资源。所有数据库用户都会分配到一个资源队列，用户提交的每条语句在运行前都会先根据资源队列限制进行评估。`gp_resq_*` 系列视图可用于检查当前通过各自资源队列提交到系统的语句的状态。请注意，超级用户发出的语句不受资源排队限制。

- [`gp_resq_activity`](#gp_resq_activity)
- [`gp_resq_activity_by_queue`](#gp_resq_activity_by_queue)
- [`gp_resq_priority_statement`](#gp_resq_priority_statement)
- [`gp_resq_role`](#gp_resq_role)
- [`gp_resqueue_status`](#gp_resqueue_status)

### gp_resq_activity {#gp_resq_activity}

对于有活动工作负载的资源队列，此视图为通过资源队列提交的每条活动语句显示一行。所有用户均可访问此视图。

视图的列说明如下：

- `resqprocpid`：分配给此语句的进程 ID（在 Coordinator 上）。
- `resqrole`：用户名。
- `resqoid`：资源队列的对象 ID。
- `resqname`：资源队列名称。
- `resqstart`：语句提交到系统的时间。
- `resqstatus`：语句的状态：running、waiting 或 cancelled。

### gp_resq_activity_by_queue {#gp_resq_activity_by_queue}

对于有活动工作负载的资源队列，此视图显示队列活动的汇总信息。所有用户均可访问此视图。

视图的列说明如下：

- `resqoid`：资源队列的对象 ID。
- `resqname`：资源队列名称。
- `resqlast`：最后一条语句提交到队列的时间。
- `resqstatus`：最后一条语句的状态：running、waiting 或 cancelled。
- `resqtotal`：此队列中的语句总数。

### gp_resq_priority_statement {#gp_resq_priority_statement}

此视图显示 Apache Cloudberry 系统中当前正在运行的所有语句的资源队列优先级、会话 ID 等信息。所有用户均可访问此视图。

视图的列说明如下：

- `rqpdatname`：会话所连接的数据库名称。
- `rqpusename`：发出语句的用户。
- `rqpsession`：会话 ID。
- `rqpcommand`：语句在此会话中的编号（命令 ID 和会话 ID 共同唯一标识一条语句）。
- `rqppriority`：此语句的资源队列优先级（`MAX`、`HIGH`、`MEDIUM`、`LOW`）。
- `rqpweight`：与此语句优先级关联的整数值。
- `rqpquery`：语句的查询文本。

### gp_resq_role {#gp_resq_role}

此视图显示与角色关联的资源队列。所有用户均可访问此视图。

视图的列说明如下：

- `rrrolname`：角色（用户）名称。
- `rrrsqname`：分配给此角色的资源队列名称。如果未显式为角色分配资源队列，它会位于默认资源队列（*pg_default*）中。

### gp_resqueue_status {#gp_resqueue_status}

此视图允许管理员查看资源队列的状态和活动。它显示特定资源队列中有多少查询正在等待运行，以及有多少查询当前在系统中处于活动状态。

视图的列说明如下：

- `queueid`：资源队列的 ID。
- `rsqname`：资源队列的名称。
- `rsqcountlimit`：资源队列的活动查询阈值。-1 表示无限制。
- `rsqcountvalue`：资源队列中当前正在使用的活动查询槽数量。
- `rsqcostlimit`：资源队列的查询代价阈值。-1 表示无限制。
- `rsqcostvalue`：资源队列中当前所有语句的总代价。
- `rsqmemorylimit`：资源队列的内存限制。
- `rsqmemoryvalue`：资源队列中当前所有语句使用的内存总量。
- `rsqwaiters`：资源队列中当前正在等待的语句数量。
- `rsqholders`：此资源队列中当前正在系统上运行的语句数量。

## 检查查询的磁盘溢出空间使用情况 {#check-query-disk-spill-space-usage}

*gp_workfile\_* 视图显示当前正在使用磁盘溢出空间的所有查询的信息。如果内存不足以完全在内存中运行查询，Apache Cloudberry 会在磁盘上创建工作文件。这些信息可用于查询故障排查和调优。也可以利用视图中的信息来设置 Apache Cloudberry 配置参数 `gp_workfile_limit_per_query` 和 `gp_workfile_limit_per_segment` 的值。

- [`gp_workfile_entries`](#gp_workfile_entries)
- [`gp_workfile_usage_per_query`](#gp_workfile_usage_per_query)
- [`gp_workfile_usage_per_segment`](#gp_workfile_usage_per_segment)

### gp_workfile_entries {#gp_workfile_entries}

此视图为当前在某个 Segment 上使用磁盘空间存放工作文件的每个算子显示一行。所有用户均可访问此视图，但非超级用户只能查看自己有权访问的数据库的信息。

视图的列说明如下：

| 列            | 类型    | 说明                                                                   |
|---------------|---------|------------------------------------------------------------------------|
| `datname`     | name    | 数据库名称。                                                           |
| `pid`         | integer | 服务器进程的进程 ID。                                                  |
| `sess_id`     | integer | 会话 ID。                                                              |
| `command_cnt` | integer | 查询的命令 ID。                                                        |
| `usename`     | name    | 角色名称。                                                             |
| `query`       | text    | 进程当前正在运行的查询。                                               |
| `segid`       | integer | Segment ID。                                                           |
| `slice`       | integer | 查询计划切片，即正在运行的查询计划部分。                               |
| `optype`      | text    | 创建工作文件的查询算子类型。                                           |
| `size`        | bigint  | 工作文件的大小，以字节为单位。                                         |
| `numfiles`    | integer | 已创建的文件数量。                                                     |
| `prefix`      | text    | 为一组相关工作文件命名时使用的前缀。                                   |

### gp_workfile_usage_per_query {#gp_workfile_usage_per_query}

此视图为当前在某个 Segment 上使用磁盘空间存放工作文件的每个查询显示一行。所有用户均可访问此视图，但非超级用户只能查看自己有权访问的数据库的信息。

视图的列说明如下：

| 列            | 类型    | 说明                                       |
|---------------|---------|--------------------------------------------|
| `datname`     | name    | 数据库名称。                               |
| `pid`         | integer | 服务器进程的进程 ID。                      |
| `sess_id`     | integer | 会话 ID。                                  |
| `command_cnt` | integer | 查询的命令 ID。                            |
| `usename`     | name    | 角色名称。                                 |
| `query`       | text    | 进程当前正在运行的查询。                   |
| `segid`       | integer | Segment ID。                               |
| `size`        | numeric | 工作文件的大小，以字节为单位。             |
| `numfiles`    | bigint  | 已创建的文件数量。                         |

### gp_workfile_usage_per_segment {#gp_workfile_usage_per_segment}

此视图为每个 Segment 显示一行。每一行显示相应 Segment 上当前工作文件占用的磁盘空间总量。所有用户均可访问此视图，但非超级用户只能查看自己有权访问的数据库的信息。

视图的列说明如下：

| 列         | 类型     | 说明                                           |
|------------|----------|------------------------------------------------|
| `segid`    | smallint | Segment ID。                                   |
| `size`     | numeric  | Segment 上工作文件的总大小。                  |
| `numfiles` | bigint   | 已创建的文件数量。                             |

## 查看用户和组（角色） {#view-users-and-groups-roles}

将用户（角色）归为一组通常便于管理对象权限：这样就可以向整个组授予权限，或撤销整个组的权限。在 Apache Cloudberry 中，做法是创建一个代表组的角色，再将该组角色的成员资格授予各个用户角色。

`references/sys-catalog/gp-toolkit-schema:gp_roles_assigned` 视图可用于查看系统中的所有角色及其成员（如果该角色也是组角色）。

### gp_roles_assigned {#gp_roles_assigned}

此视图显示系统中的所有角色及其成员（如果该角色也是组角色）。所有用户均可访问此视图。

视图的列说明如下：

- `raroleid`：角色的对象 ID。如果此角色有成员（用户），则视为*组*角色。
- `rarolename`：角色（用户或组）名称。
- `ramemberid`：此角色的成员角色的对象 ID。
- `ramembername`：此角色的成员角色的名称。

## 检查数据库对象大小和磁盘空间 {#check-database-object-sizes-and-disk-space}

`gp_size_*` 系列视图可用于确定分布式 Apache Cloudberry 数据库、模式、表或索引的磁盘空间使用量。以下视图计算对象在所有主 Segment 上的总大小（大小计算不包括镜像）。

- [`gp_size_of_all_table_indexes`](#gp_size_of_all_table_indexes)
- [`gp_size_of_database`](#gp_size_of_database)
- [`gp_size_of_index`](#gp_size_of_index)
- [`gp_size_of_schema_disk`](#gp_size_of_schema_disk)
- [`gp_size_of_table_and_indexes_disk`](#gp_size_of_table_and_indexes_disk)
- [`gp_size_of_table_and_indexes_licensing`](#gp_size_of_table_and_indexes_licensing)
- [`gp_size_of_table_disk`](#gp_size_of_table_disk)
- [`gp_size_of_table_uncompressed`](#gp_size_of_table_uncompressed)
- [`gp_disk_free`](#gp_disk_free)

表和索引大小视图通过对象 ID（而非名称）列出关系。要按名称检查表或索引的大小，必须在 `pg_class` 表中查找关系名称（`relname`）。例如：

```sql
SELECT relname as name, sotdsize as size, sotdtoastsize as 
toast, sotdadditionalsize as other 
FROM gp_size_of_table_disk as sotd, pg_class 
WHERE sotd.sotdoid=pg_class.oid ORDER BY relname;
```

### gp_size_of_all_table_indexes {#gp_size_of_all_table_indexes}

此视图显示某个表的所有索引的总大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的关系。

视图的列说明如下：

- `soatioid`：表的对象 ID。
- `soatisize`：表的所有索引的总大小，以字节为单位。
- `soatischemaname`：模式名称。
- `soatitablename`：表名称。

### gp_size_of_database {#gp_size_of_database}

此视图显示数据库的总大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的数据库。

视图的列说明如下：

- `sodddatname`：数据库名称。
- `sodddatsize`：数据库大小，以字节为单位。

### gp_size_of_index {#gp_size_of_index}

此视图显示索引的总大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的关系。

视图的列说明如下：

- `soioid`：索引的对象 ID。
- `soitableoid`：索引所属表的对象 ID。
- `soisize`：索引大小，以字节为单位。
- `soiindexschemaname`：索引所在模式的名称。
- `soiindexname`：索引名称。
- `soitableschemaname`：表所在模式的名称。
- `soitablename`：表名称。

### gp_size_of_schema_disk {#gp_size_of_schema_disk}

此视图显示当前数据库中 public 模式和用户创建模式的大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的模式。

视图的列说明如下：

- `sosdnsp`：模式名称。
- `sosdschematablesize`：模式中所有表的总大小，以字节为单位。
- `sosdschemaidxsize`：模式中所有索引的总大小，以字节为单位。

### gp_size_of_table_and_indexes_disk {#gp_size_of_table_and_indexes_disk}

此视图显示表及其索引的磁盘大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的关系。

视图的列说明如下：

- `sotaidoid`：父表的对象 ID。
- `sotaidtablesize`：表的磁盘大小。
- `sotaididxsize`：表上所有索引的总大小。
- `sotaidschemaname`：模式名称。
- `sotaidtablename`：表名称。

### gp_size_of_table_and_indexes_licensing {#gp_size_of_table_and_indexes_licensing}

此视图显示用于许可计量的表及其索引的总大小。使用此视图需要超级用户权限。

视图的列说明如下：

- `sotailoid`：表的对象 ID。
- `sotailtablesizedisk`：表的磁盘总大小。
- `sotailtablesizeuncompressed`：如果表是压缩的 AO 表，则显示其未压缩大小，以字节为单位。
- `sotailindexessize`：表中所有索引的总大小。
- `sotailschemaname`：模式名称。
- `sotailtablename`：表名称。

### gp_size_of_table_disk {#gp_size_of_table_disk}

此视图显示表的磁盘大小。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的表。视图的列说明如下：

- `sotdoid`：表的对象 ID。
- `sotdsize`：表的大小，以字节为单位。此值仅包含主表的大小，不包括超大属性（toast）等辅助对象，也不包括 AO 表的额外存储对象。
- `sotdtoastsize`：TOAST 表（超大属性存储）的大小（如果有）。
- `sotdadditionalsize`：AO 表的段表和块目录表的大小。
- `sotdschemaname`：模式名称。
- `sotdtablename`：表名称。

### gp_size_of_table_uncompressed {#gp_size_of_table_uncompressed}

此视图对 AO 表显示未压缩的表大小；对其他表则显示磁盘上的表大小。使用此视图需要超级用户权限。视图的列说明如下：

- `sotuoid`：表的对象 ID。
- `sotusize`：如果是压缩的 AO 表，则为表的未压缩大小，以字节为单位；否则为表的磁盘大小。
- `sotuschemaname`：模式名称。
- `sotutablename`：表名称。

### gp_disk_free {#gp_disk_free}

此外部表在活动 Segment 主机上运行 `df`（disk free）命令，并返回结果。计算不包括非活动镜像。使用此外部表需要超级用户权限。视图的列说明如下：

- `dfsegment`：Segment 的内容 ID（仅显示活动 Segment）。
- `dfhostname`：Segment 主机的主机名。
- `dfdevice`：设备名称。
- `dfspace`：Segment 文件系统中的可用磁盘空间，以千字节为单位。

## 检查缺失和孤立的数据文件 {#check-for-missing-and-orphaned-data-files}

如果关系数据文件在目录中有记录，但磁盘上不存在，Apache Cloudberry 会将其视为缺失文件。相反，如果磁盘上出现未被任何关系引用的意外数据文件，Apache Cloudberry 会将其视为孤立文件。

Apache Cloudberry 提供以下视图，帮助识别当前数据库中是否存在缺失或孤立文件：

- [`gp_move_orphaned_files()`](#move-orphaned-data-files)
- [`gp_check_orphaned_files`](#gp_check_orphaned_files)
- [`gp_check_missing_files`](#gp_check_missing_files)

建议在集群扩容或离线维护前检查这些情况。

默认情况下，本节列出的视图可供 `PUBLIC` 使用。

### gp_check_orphaned_files {#gp_check_orphaned_files}

`gp_check_orphaned_files` 视图扫描默认表空间和用户定义表空间，查找孤立的数据文件。Apache Cloudberry 在此检查中考虑普通数据文件、名称中包含下划线（`_`）的文件，以及带扩展编号的文件（名称中包含 `.<N>` 的文件）。`gp_check_orphaned_files` 从 Apache Cloudberry 的 Coordinator 和所有 Segment 收集结果。

视图的列说明如下：

- `gp_segment_id`：数据库 Segment 标识符。
- `tablespace`：孤立文件所在表空间的标识符。
- `filename`：孤立数据文件的文件名。
- `filepath`：孤立数据文件的文件系统路径，相对于 Coordinator 或 Segment 的数据目录。

注意

此视图应当仅作为识别孤立数据文件的多项依据之一。不要仅凭此视图的查询结果删除文件。

### gp_check_missing_files {#gp_check_missing_files}

`gp_check_missing_files` 视图扫描堆表和列存 AO 表，查找缺失的数据文件。Apache Cloudberry 在此检查中仅考虑普通数据文件（名称中不包含 `.` 或 `_` 的文件）。`gp_check_missing_files` 从 Apache Cloudberry 的 Coordinator 和所有 Segment 收集结果。

视图的列说明如下：

- `gp_segment_id`：数据库 Segment 标识符。
- `tablespace`：表所在表空间的标识符。
- `relname`：存在缺失数据文件的表的名称。
- `filename`：缺失数据文件的文件名。

### gp_check_missing_files_ext {#gp_check_missing_files_ext}

`gp_check_missing_files_ext` 视图仅扫描列存 AO 表，查找缺失的扩展数据文件。Apache Cloudberry 在此检查中既考虑普通数据文件，也考虑带扩展编号的文件（名称中包含 `.<N>` 的文件）。名称中包含 `_` 的文件不在检查范围内。`gp_check_missing_files_ext` 仅从 Apache Cloudberry 的数据库 Segment 收集结果。

视图的列说明如下：

- `gp_segment_id`：数据库 Segment 标识符。
- `tablespace`：表所在表空间的标识符。
- `relname`：存在缺失扩展数据文件的表的名称。
- `filename`：缺失扩展数据文件的文件名。

## 移动孤立的数据文件 {#move-orphaned-data-files}

用户定义函数（UDF）`gp_move_orphaned_files()` 将 [`gp_check_orphaned_files`](#gp_check_orphaned_files) 视图发现的孤立文件移动到指定的文件系统位置。

函数签名为：`gp_move_orphaned_files( <target_directory> TEXT )`。

移动文件之前，`<target_directory>` 必须已存在于所有 Segment 主机上，并且 `gpadmin` 用户必须能够访问该目录。如果为 `<target_directory>` 指定相对路径，则相对于 Coordinator 或 Segment 的数据目录解析。

Apache Cloudberry 会重命名每个移动的数据文件，使其新名称反映文件在数据目录中的原始位置。文件名格式因孤立文件所在的表空间而异：

| 表空间         | 重命名后的文件格式                                                                |
|----------------|-----------------------------------------------------------------------------------|
| `default`      | `seg<num>_base_<database-oid>_<relfilenode>`                                      |
| `global`       | `seg<num>_global_<relfilenode>`                                                   |
| `user-defined` | `seg<num>_pg_tblspc_<tablespace-oid>_<gpdb-version>_<database-oid>_<relfilenode>` |

例如，如果主 Segment 2 上默认表空间中名为 `12345` 的文件是孤立文件，执行：

```sql
SELECT * FROM gp_move_orphaned_files('/home/gpadmin/orphaned');
```

将按如下方式移动并重命名该文件：

- 原始位置：`<data_directory>/base/13700/12345`
- 新位置和文件名：`/home/gpadmin/orphaned/seg2_base_13700_12345`

`gp_move_orphaned_files()` 为每个移动的文件返回原始和新的文件系统位置，同时指出移动操作是否成功。例如：

```sql
SELECT * FROM gp_toolkit.gp_move_orphaned_files('/home/gpadmin/orphaned');
 gp_segment_id | move_success |           oldpath          |         newpath
---------------+--------------+----------------------------+-----------------------------------
            -1 | t            | /<data_dir>/base/13715/99999 | /home/gpadmin/orphaned/seg-1_base_13715_99999
             1 | t            | /<data_dir>/base/13715/99999 | /home/gpadmin/orphaned/seg1_base_13715_99999
             2 | t            | /<data_dir>/base/13715/99999 | /home/gpadmin/orphaned/seg2_base_13715_99999
(3 rows)
```

移动文件后，可以选择删除或备份这些文件。

## 检查数据分布是否均匀 {#check-for-uneven-data-distribution}

Apache Cloudberry 中的所有表都是分布式的，即数据分散在系统的所有 Segment 上。如果数据分布不均，查询处理性能可能下降。以下视图有助于诊断表的数据分布是否不均：

- [`gp_toolkit.gp_skew_coefficients`](#gp_skew_coefficients)
- [`gp_toolkit.gp_skew_idle_fractions`](#gp_skew_idle_fractions)

### gp_skew_coefficients {#gp_skew_coefficients}

此视图通过计算各 Segment 所存储数据的变异系数（CV），显示数据分布倾斜程度。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的表。

视图的列说明如下：

- `skcoid`：表的对象 ID。
- `skcnamespace`：定义表的名字空间。
- `skcrelname`：表名称。
- `skccoeff`：变异系数（CV）等于标准差除以平均值，同时考虑了数据序列的平均值以及围绕平均值的变化程度。此值越低越好，值越高表示数据倾斜越严重。

### gp_skew_idle_fractions {#gp_skew_idle_fractions}

此视图通过计算表扫描期间系统空闲部分的比例来显示数据分布倾斜程度，该比例可作为数据处理倾斜的指标。所有用户均可访问此视图，但非超级用户只能看到自己有权访问的表。

视图的列说明如下：

- `sifoid`：表的对象 ID。
- `sifnamespace`：定义表的名字空间。
- `sifrelname`：表名称。
- `siffraction`：表扫描期间系统空闲部分的比例，可作为数据分布不均或查询处理倾斜的指标。例如，`0.1` 表示 10% 的倾斜，`0.5` 表示 50% 的倾斜，以此类推。倾斜超过 10% 的表应评估其分布策略。

## 维护分区 {#maintain-partitions}

如果数据库使用分区，就需要定期执行一些任务来维护这些分区。Apache Cloudberry 提供了一个视图和多个用户定义函数来协助完成这些任务。

### gp_partitions 视图 {#the-gp_partitions-view}

`gp_partitions` 视图显示数据库中的所有叶子分区。

此视图提供对旧版 `pg_partitions` 视图的向后兼容性（该视图存在于 Apache Cloudberry 的早期主版本中）。视图的列说明如下：

| 列                         | 类型     | 说明                                                                                                            |
|----------------------------|----------|-----------------------------------------------------------------------------------------------------------------|
| `schemaname`               | name     | 分区表所在模式的名称。                                                                                         |
| `tablename`                | name     | 顶层父表的名称。                                                                                               |
| `partitionschemaname`      | name     | 分区表所在的模式。                                                                                             |
| `partitiontablename`       | name     | 分区表的关系名称（直接访问分区时应使用此表名）。                                                                 |
| `parentpartitiontablename` | regclass | 此分区上一级父表的关系名称。                                                                                   |
| `partitiontype`            | text     | 分区类型（range 或 list）。                                                                                    |
| `partitionlevel`           | integer  | 此分区在层级结构中的级别。                                                                                     |
| `partitionrank`            | integer  | 对于范围分区，此分区相对于同级其他分区的排名。                                                                   |
| `partitionlistvalues`      | text     | 对于列表分区，与此分区关联的列表值。                                                                            |
| `partitionrangestart`      | text     | 对于范围分区，此分区的起始值。                                                                                  |
| `partitionrangeend`        | text     | 对于范围分区，此分区的结束值。                                                                                  |
| `partitionisdefault`       | boolean  | 如果是默认分区，则为 T；否则为 F。                                                                              |
| `partitionboundary`        | text     | 此分区的完整分区规范。                                                                                          |
| `parenttablespace`         | name     | 此分区上一级父表的表空间。                                                                                      |
| `partitiontablespace`      | name     | 此分区的表空间。                                                                                               |

### 用于分区维护的用户定义函数 {#user-defined-functions-for-partition-maintenance}

下表汇总了 Apache Cloudberry 提供的分区维护辅助函数：

| 函数                                      | 返回类型    | 说明                                                                                                                                                  |
|-------------------------------------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pg_partition_rank(rp regclass)`          | integer     | 对于范围分区，返回此分区相对于同级其他分区的排名。对于其他分区类型，返回 `NULL`。                                                                      |
| `pg_partition_range_from(rp regclass)`    | text        | 返回范围分区的下界。                                                                                                                                  |
| `pg_partition_range_to(rp regclass)`      | text        | 返回范围分区的上界。                                                                                                                                  |
| `pg_partition_isdefault(rp regclass)`     | boolean     | 判断给定分区是否为默认分区。                                                                                                                           |
| `pg_partition_lowest_child(rp regclass)`  | regclass    | 找出给定分区中排名最低的子分区。                                                                                                                       |
| `pg_partition_highest_child(rp regclass)` | regclass    | 找出给定分区中排名最高的子分区。                                                                                                                       |
