---
title: "排查性能问题"
description: "本文提供识别和排查 Apache Cloudberry 系统性能问题的指导。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/investigate-performance-issues.md"
---

本文列出可用于查明性能问题原因的步骤。如果问题仅影响特定工作负载或查询，可以集中调优该工作负载。如果问题影响整个系统，则可能由硬件问题、系统故障或资源争用引起。

## 检查系统状态 {#check-system-state}

使用 `gpstate` 工具识别故障 Segment。Segment 实例停止运行时，其他主机必须接管其处理工作，因此 Apache Cloudberry 系统的性能会下降。

Segment 故障可能表明存在硬件故障，例如磁盘驱动器或网卡故障。Apache Cloudberry 提供硬件验证工具 `gpcheckperf`，帮助识别存在硬件问题的 Segment 主机。

## 检查数据库活动 {#check-database-activity}

- [检查活动会话（工作负载）](#check-for-active-sessions-workload)
- [检查锁（争用）](#check-for-locks-contention)
- [检查查询状态与系统利用率](#check-query-status-and-system-utilization)

### 检查活动会话（工作负载） {#check-for-active-sessions-workload}

`pg_stat_activity` 系统目录视图为每个服务器进程显示一行，包含数据库 OID、数据库名、进程 ID、用户 OID、用户名、当前查询、当前查询开始执行的时间、进程启动时间、客户端地址和端口号。要获取当前系统工作负载的完整信息，请以数据库超级用户身份查询此视图。例如：

```sql
SELECT * FROM pg_stat_activity;
```

注意，这些信息并非即时更新。

### 检查锁（争用） {#check-for-locks-contention}

通过 `pg_locks` 系统目录视图，可以查看当前锁的信息。如果某个事务持有对象上的锁，其他查询必须等待该锁释放后才能继续。从用户角度看，查询可能像是挂起了。

检查 `pg_locks` 中尚未授予的锁，有助于识别数据库客户端会话之间的争用。`pg_locks` 提供数据库系统所有锁的全局视图，而不仅限于当前数据库的锁。可以将其中的 relation 列与 `pg_class.oid` 连接，识别被锁定的关系（例如表），但这种方法只对当前数据库中的关系有效。还可以将 `pid` 列与 `pg_stat_activity.pid` 连接，查看持有锁或等待获取锁的会话的更多信息。例如：

```sql
SELECT locktype, database, c.relname, l.relation, 
l.transactionid, l.pid, l.mode, l.granted, 
a.query 
        FROM pg_locks l, pg_class c, pg_stat_activity a 
        WHERE l.relation=c.oid AND l.pid=a.pid
        ORDER BY c.relname;
```

如果使用资源组，等待中的查询也会显示在 `pg_locks` 中。要查看资源组中有多少查询等待运行，请使用 `gp_resgroup_status` 系统目录视图。例如：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_status;
```

同样，如果使用资源队列，在队列中等待的查询也会显示在 `pg_locks` 中。要查看资源队列中有多少查询等待运行，请使用 `gp_resqueue_status` 系统目录视图。例如：

```sql
SELECT * FROM gp_toolkit.gp_resqueue_status;
```

### 检查查询状态与系统利用率 {#check-query-status-and-system-utilization}

可以使用 `ps`、`top`、`iostat`、`vmstat`、`netstat` 等系统监控工具，监控 Apache Cloudberry 阵列各主机上的数据库活动。这些工具可以识别系统当前运行的 Apache Cloudberry 进程（`postgres` 进程），以及 CPU、内存、磁盘 I/O 或网络活动方面最消耗资源的任务。查看这些系统统计信息，可找出因系统过载或资源消耗过多而降低数据库性能的查询。Apache Cloudberry 管理工具 `gpssh` 可以在多台主机上同时运行这些系统监控命令。

可以创建并使用 Apache Cloudberry 的 `session_level_memory_consumption` 视图，了解当前在 Apache Cloudberry 上运行查询的会话的内存使用量和空闲时间。有关该视图的详情，请参见[查看会话内存使用信息](/cloudberry/sys-admin/check-database-system/)。

## 排查问题查询 {#troubleshoot-problem-queries}

如果查询性能不佳，可以查看其查询计划来识别问题。`EXPLAIN` 命令显示给定查询的查询计划。有关解读查询计划和识别问题的更多信息，请参见[分析查询性能](/cloudberry/performance/optimize-queries/analyze-query-performance/)。

查询执行期间发生内存不足事件时，Apache Cloudberry 的内存记账框架会报告当时所有正在运行的查询的详细内存消耗。这些信息会写入 Apache Cloudberry Segment 日志。

## 检查错误消息 {#investigate-error-messages}

Apache Cloudberry 日志消息写入 Coordinator 或 Segment 数据目录下的 `log` 目录。Coordinator 日志文件包含的信息最全面，应始终首先检查它。日志文件每天轮转，命名约定为 `gpdb-YYYY-MM-DD_hhmmss.csv`。要查找 Coordinator 主机上的日志文件：

```shell
$ cd $COORDINATOR_DATA_DIRECTORY/log
```

日志行的格式如下：

```shell
<timestamp> | <user> | <database> | <statement_id> | <con#><cmd#> 
|:-<LOG_LEVEL>: <log_message>
```

可以重点搜索日志级别为 `WARNING`、`ERROR`、`FATAL` 或 `PANIC` 的消息。Apache Cloudberry 工具 `gplogfilter` 可用于搜索 Apache Cloudberry 日志文件。例如，在 Coordinator 主机上运行以下命令，会检查标准日志位置中提示问题的日志消息：

```shell
$ gplogfilter -t
```

要搜索 Segment 日志文件中的相关条目，可以使用 `gpssh` 在 Segment 主机上运行 `gplogfilter`。通过 `statement_id` 或 `con`#（会话标识符），可以识别相互对应的日志条目。例如，以下命令搜索 Segment 日志文件中包含字符串 `con6` 的消息，并将输出保存到文件：

```shell
gpssh -f seg_hosts_file -e 'source 
/usr/local/cloudberry-db/greenplum_path.sh ; gplogfilter -f 
con6 /gpdata/*/log/gpdb*.csv' > seglog.out
```
