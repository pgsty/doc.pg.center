---
title: gp_stats_collector
description: gp_stats_collector 收集 Apache Cloudberry 查询执行指标，并报告给外部监控代理。
weight: 130
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-stats-collector.md
---

`gp_stats_collector` 模块收集 Apache Cloudberry 的查询执行指标，并报告给外部监控代理。它在 Coordinator 和 Segment 的执行器中安装钩子，为每个查询发送生命周期事件（查询文本、计划、时间戳、用户和数据库），以及系统、性能测量、Interconnect 和溢写指标。事件通过 Unix 域套接字传递，也可以写入数据库内的日志表。

此模块还提供按需获取运行时查询状态的接口（`pg_query_state`），使运行中查询的每个后端报告各计划节点的统计信息，无需等待查询结束。

## 构建与安装 {#build-and-install}

`gp_stats_collector` 默认不构建。要构建它，配置 Apache Cloudberry 时指定 `--with-gp-stats-collector` 选项：

```shell
./configure --with-gp-stats-collector [other options]
```

设置此选项后，`configure` 要求：

- protobuf 库版本不低于 3.0.0（通过 `pkg-config` 检测）。
- `PATH` 中有 `protoc` 编译器。

此模块包含以 `-std=c++17` 编译的 C++ 源码。

## 启用模块 {#enable-the-module}

1. 将库加入 `shared_preload_libraries` 并重启集群。模块在服务器启动时分配共享内存、注册信号处理器，因此必须预加载：

    ```shell
    gpconfig -c shared_preload_libraries -v 'gp_stats_collector'
    gpstop -ra
    ```

    如果 `shared_preload_libraries` 已列出其他库，请在其值中保留它们。

2. 在需要使用 SQL 对象的数据库中创建扩展。创建此扩展需要超级用户权限：

    ```sql
    CREATE EXTENSION gp_stats_collector;
    ```

    扩展会创建 `gpsc` 模式。默认扩展版本为 `1.2`。

3. 开启收集功能。此功能默认关闭：

    ```sql
    SET gpsc.enable TO on;
    ```

## 收集的数据 {#collected-data}

查询经历四个状态，模块会在每个状态分别由派发器进程（Coordinator 上）和执行器进程（Segment 上）发送一条消息：

```text
submit -> ExecutorStart() -> start -> ExecutorRun() -> ExecutorFinish() -> end -> ExecutorEnd() -> done
```

| 数据 | 说明 | 控制参数 |
|---|---|---|
| 查询生命周期 | 查询文本、规范化查询文本、时间戳（提交、开始、结束、完成）、用户和数据库信息。 | `gpsc.enable` |
| `EXPLAIN` 数据 | 查询的 `EXPLAIN (TEXT, COSTS, VERBOSE)` 输出。 | `gpsc.enable` |
| `EXPLAIN ANALYZE` 数据 | `EXPLAIN (TEXT, ANALYZE, BUFFERS, TIMING, VERBOSE)` 输出。仅当执行时间达到 `gpsc.min_analyze_time` 时发送。 | `gpsc.enable`, `gpsc.enable_analyze`, `gpsc.enable_cdbstats`, `gpsc.min_analyze_time` |
| 其他指标 | 性能测量、系统、网络、Interconnect 和溢写指标。 | `gpsc.enable` |

报告事件的注意事项：

- 部分查询跳过 `end` 状态，此时 `end` 统计信息随 `done` 一起发送。
- 查询失败或取消时，其统计信息随 `done` 一起发送。
- 部分统计信息按当前值与 `submit` 时取得的快照之差计算。
- 每个进程（派发器或执行器）发送各自的统计信息。
- 派发器上的嵌套查询在执行器上成为顶层查询。

## 配置参数 {#configuration-parameters}

### 收集器参数 {#collector-parameters}

上下文为 `superuser` 的参数只有超级用户可以更改；上下文为 `user` 的参数，任何角色都可以在自己的会话中更改。

| 参数 | 类型 | 默认值 | 上下文 | 说明 |
|---|---|---|---|---|
| `gpsc.enable` | 布尔值 | `off` | superuser | 启用指标收集器。 |
| `gpsc.uds_path` | 字符串 | `/tmp/gpsc_agent.sock` | superuser | 代理的 Unix 域套接字文件系统路径。 |
| `gpsc.logging_mode` | 枚举 | `uds` | superuser | 收集事件的输出目标。`uds` 将事件发送到 Unix 域套接字；`tbl` 将事件写入通过 `gpsc.log` 视图暴露的日志表。只有超级用户可以查看此设置。 |
| `gpsc.enable_analyze` | 布尔值 | `on` | superuser | 收集 `EXPLAIN ANALYZE` 数据。开启时，派发器会为其运行的查询启用缓冲区、行数和计时测量。 |
| `gpsc.enable_cdbstats` | 布尔值 | `on` | superuser | 将 Cloudberry 特有的执行器统计信息加入 `EXPLAIN ANALYZE` 数据，仅当 `gpsc.enable_analyze` 开启时生效。 |
| `gpsc.min_analyze_time` | 整数（ms） | `10000` | user | 报告 `EXPLAIN ANALYZE` 文本所需的最短执行时间，超过此时长才报告。`0` 对所有查询报告；`-1` 关闭此功能。 |
| `gpsc.report_nested_queries` | 布尔值 | `on` | user | 开启时，Coordinator 报告顶层和嵌套查询，Segment 报告汇总值。关闭时，Coordinator 和 Segment 都只报告顶层查询。 |
| `gpsc.enable_utility` | 布尔值 | `off` | user | 收集工具语句的统计信息。 |
| `gpsc.ignored_users_list` | 字符串 | 空 | superuser | 不报告其查询的角色列表，以逗号分隔。 |
| `gpsc.max_text_size` | 整数（字节） | `1048576` | superuser | 超过此大小的查询文本和错误消息会被截断。范围：`0` 到 `2147483647`。 |
| `gpsc.max_plan_size` | 整数（kB） | `1024` | superuser | 超过此大小的计划文本会被截断。范围：`0` 到 `2097151`。 |

> [!NOTE]
> 不建议将 `gpsc.max_text_size` 或 `gpsc.max_plan_size` 设为超过 1024 kB 的值。

### 运行时查询状态参数 {#runtime-query-state-parameters}

只有通过 `shared_preload_libraries` 加载库时，才会注册这些参数。

| 参数 | 类型 | 默认值 | 上下文 | 说明 |
|---|---|---|---|---|
| `pg_query_state.enable` | 布尔值 | `on` | superuser | 启用运行时查询状态模块（执行器钩子和信号处理）。 |
| `pg_query_state.enable_timing` | 布尔值 | `on` | superuser | 除行数外，还收集计时数据。 |
| `pg_query_state.enable_buffers` | 布尔值 | `on` | superuser | 收集缓冲区使用情况。 |

## SQL 对象 {#sql-objects}

所有对象均创建在 `gpsc` 模式中。该模式的 `USAGE` 权限授予 `PUBLIC`。

`gpsc.log` 和 `gpsc.stat_messages` 视图的访问权限未授予 `PUBLIC`。所有函数都保留 `PUBLIC` 的默认 `EXECUTE` 权限，而 `gpsc.truncate_log()` 和 `gpsc.stat_messages_reset()` 不检查调用者权限。如果只允许管理员运行这些函数，请从 `PUBLIC` 撤销它们的 `EXECUTE` 权限。

只有集群使用 UDPIFC Interconnect 时，才收集 Interconnect 统计信息。

### gpsc.stat_messages {#gpscstat_messages}

此视图显示 Coordinator 和每个 Segment 上收集器尝试发送的消息的计数器。如果未通过 `shared_preload_libraries` 加载库，查询会报错。

| 列 | 类型 | 说明 |
|---|---|---|
| `segid` | `int` | Segment 内容 ID。`-1` 表示 Coordinator。 |
| `total_messages` | `bigint` | 消息总数，包括失败的消息。 |
| `send_failures` | `bigint` | 发送失败的消息数。 |
| `connection_failures` | `bigint` | 连接代理套接字失败的次数。 |
| `other_errors` | `bigint` | 其他错误数。 |
| `max_message_size` | `int` | 最大消息的大小。 |

### gpsc.stat_messages_reset() {#gpscstat_messages_reset}

```sql
gpsc.stat_messages_reset() RETURNS SETOF void
```

重置 Coordinator 和所有 Segment 上 `gpsc.stat_messages` 显示的计数器。

### gpsc.log {#gpsclog}

此视图汇集 Coordinator 和所有 Segment 上的日志表，按 `tmid`、`ssid`、`ccnt` 排序。`gpsc.logging_mode` 为 `tbl` 时填充该表。每行是一个报告事件。

行的插入方式保证即使运行查询的事务回滚，这些行也会保留。

| 列 | 类型 | 说明 |
|---|---|---|
| `query_id` | `bigint` | 查询 ID。 |
| `plan_id` | `bigint` | 规范化计划的哈希。 |
| `nested_level` | `bigint` | 查询的嵌套层级。 |
| `slice_id` | `bigint` | 切片 ID。 |
| `systemstat_vsize`, `systemstat_rss`, `systemstat_vmsizekb`, `systemstat_vmpeakkb` | `bigint` | 来自 `/proc/pid/stat` 和 `/proc/pid/status` 的进程内存数据。 |
| `systemstat_rchar`, `systemstat_wchar`, `systemstat_syscr`, `systemstat_syscw`, `systemstat_read_bytes`, `systemstat_write_bytes`, `systemstat_cancelled_write_bytes` | `bigint` | 来自 `/proc/pid/io` 的进程 I/O 计数器。 |
| `instrumentation_ntuples`, `instrumentation_nloops`, `instrumentation_tuplecount` | `bigint` | 元组和循环计数器。 |
| `instrumentation_shared_blks_hit`, `instrumentation_shared_blks_read`, `instrumentation_shared_blks_dirtied`, `instrumentation_shared_blks_written` | `bigint` | 共享缓冲区块计数器。 |
| `instrumentation_local_blks_hit`, `instrumentation_local_blks_read`, `instrumentation_local_blks_dirtied`, `instrumentation_local_blks_written` | `bigint` | 本地缓冲区块计数器。 |
| `instrumentation_temp_blks_read`, `instrumentation_temp_blks_written` | `bigint` | 临时文件块计数器。 |
| `instrumentation_inherited_calls` | `bigint` | 嵌套查询数量。 |
| `instrumentation_sent_total_bytes`, `instrumentation_sent_tuple_bytes`, `instrumentation_sent_chunks` | `bigint` | 发送的网络数据。 |
| `instrumentation_received_total_bytes`, `instrumentation_received_tuple_bytes`, `instrumentation_received_chunks` | `bigint` | 接收的网络数据。 |
| `interconnect_total_recv_queue_size`, `interconnect_recv_queue_size_counting_time`, `interconnect_total_capacity`, `interconnect_capacity_counting_time`, `interconnect_total_buffers`, `interconnect_buffer_counting_time`, `interconnect_active_connections_num`, `interconnect_retransmits`, `interconnect_startup_cached_pkt_num`, `interconnect_mismatch_num`, `interconnect_crc_errors`, `interconnect_snd_pkt_num`, `interconnect_recv_pkt_num`, `interconnect_disordered_pkt_num`, `interconnect_duplicated_pkt_num`, `interconnect_recv_ack_num`, `interconnect_status_query_msg_num` | `bigint` | Interconnect 统计信息。 |
| `spill_totalbytes` | `bigint` | 已写入的溢写字节数。 |
| `systemstat_runningtimeseconds`, `systemstat_usertimeseconds`, `systemstat_kerneltimeseconds` | `double precision` | 实际经过时间、用户时间和内核时间，单位为秒。 |
| `instrumentation_firsttuple`, `instrumentation_startup`, `instrumentation_total`, `instrumentation_blk_read_time`, `instrumentation_blk_write_time`, `instrumentation_startup_time`, `instrumentation_inherited_time` | `double precision` | 计时数据，单位为秒。 |
| `datetime`, `submit_time`, `start_time`, `end_time` | `timestamp with time zone` | 事件和查询时间戳。 |
| `tmid`, `ssid`, `ccnt` | `int` | 查询键：来自 `gp_gettmid()` 的基于时间的 ID、会话 ID 和命令计数器。 |
| `dbid` | `int` | 报告实例的 `dbid`，与 `gp_segment_configuration` 中一致。 |
| `segid` | `int` | Segment 索引。`-1` 表示 Coordinator。 |
| `spill_filecount` | `int` | 创建的溢写（临时）文件数量。 |
| `generator` | `text` | 生成计划的规划器或优化器。 |
| `query_text`, `template_query_text` | `text` | 查询文本和规范化查询文本。 |
| `plan_text`, `template_plan_text` | `text` | `EXPLAIN` 文本和规范化计划文本。 |
| `analyze_text` | `text` | `EXPLAIN ANALYZE` 文本。 |
| `user_name`, `database_name`, `rsgname` | `text` | 会话用户、数据库和资源组。 |
| `error_message` | `text` | 查询失败时的错误消息。 |
| `query_status` | `text` | 事件状态，例如 `QUERY_STATUS_SUBMIT`、`QUERY_STATUS_START`、`QUERY_STATUS_END`、`QUERY_STATUS_DONE`。 |
| `utility` | `boolean` | 事件是否属于工具语句。 |

### gpsc.truncate_log() {#gpsctruncate_log}

```sql
gpsc.truncate_log() RETURNS SETOF void
```

截断 Coordinator 和所有 Segment 上的日志表。

### gpsc.pg_query_state() {#gpscpg_query_state}

```sql
gpsc.pg_query_state(pid int, trace_id bytea) RETURNS SETOF void
```

为 Coordinator 后端 `pid` 正在运行的查询触发运行时逐节点收集。请求分发到该 Coordinator 后端及参与查询的每个 Segment 后端。各后端遍历自己的计划树，并将一批逐节点统计信息推送到 `gpsc.uds_path` 设置的套接字。Coordinator 还会推送计划文档，并限制发送频率，以免多次轮询长时间运行的查询时重复发送未变的计划。此函数不返回行，也不等待结果。

- `trace_id` 必须恰好为 16 字节，由调用者生成，接收方将其用作此次收集的键。
- 此函数仅在 Coordinator 上运行。
- 后端不能轮询自身。

### gpsc.pg_query_state_backends() {#gpscpg_query_state_backends}

```sql
gpsc.pg_query_state_backends(pid int) RETURNS TABLE(segid int, pid int)
```

列出参与后端 `pid` 所运行查询的 Segment 后端，让收集器知道应等待多少批数据。只在 Coordinator 上运行的查询报告为一行，表示 Coordinator，且 `segid` 小于 `0`。目标未运行查询或已关闭 `pg_query_state.enable` 时，函数返回空集。

### 内部对象 {#internal-objects}

扩展还创建以下对象，但不应直接调用：

- `gpsc.cbdb_mpp_query_state(gpsc.gp_segment_pid[], bytea)` 和复合类型 `gpsc.gp_segment_pid (segid int, pid int)`：由 `gpsc.pg_query_state()` 用于向 Segment 派发请求。
- 名称以两个下划线开头的函数，例如 `gpsc.__stat_messages_f_on_master()` 或 `gpsc.__test_uds_start_server(text)`：为上述视图和函数提供支持，以及供回归测试使用的辅助函数。

### 权限 {#privileges}

`gpsc.pg_query_state()`、`gpsc.pg_query_state_backends()` 和 `gpsc.cbdb_mpp_query_state()` 的 `EXECUTE` 权限授予 `PUBLIC`。访问检查在服务器内部执行：只有当调用者是超级用户，或使用与目标后端相同的角色时，才能轮询该后端。这样监控代理可以使用非超级用户角色，同时无法观察其他角色的查询。

## 示例 {#example}

以下示例将事件写入日志表而非套接字，然后读取这些事件。

```sql
CREATE EXTENSION gp_stats_collector;

-- Helper to sort the events of one query in lifecycle order
CREATE OR REPLACE FUNCTION gpsc_status_order(status text)
RETURNS integer
AS $$
BEGIN
    RETURN CASE status
        WHEN 'QUERY_STATUS_SUBMIT' THEN 1
        WHEN 'QUERY_STATUS_START' THEN 2
        WHEN 'QUERY_STATUS_END' THEN 3
        WHEN 'QUERY_STATUS_DONE' THEN 4
        ELSE 999
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

SET gpsc.ignored_users_list TO '';
SET gpsc.enable TO TRUE;
SET gpsc.report_nested_queries TO TRUE;
SET gpsc.enable_utility TO FALSE;

SET gpsc.logging_mode to 'TBL';

SELECT 1;
SELECT COUNT(*) FROM generate_series(1,10);

RESET gpsc.logging_mode;

SELECT segid, query_text, query_status FROM gpsc.log ORDER BY segid, ccnt, gpsc_status_order(query_status) ASC;
```

```text
 segid |                 query_text                  |    query_status
-------+---------------------------------------------+---------------------
    -1 | SELECT 1;                                   | QUERY_STATUS_SUBMIT
    -1 | SELECT 1;                                   | QUERY_STATUS_START
    -1 | SELECT 1;                                   | QUERY_STATUS_END
    -1 | SELECT 1;                                   | QUERY_STATUS_DONE
    -1 | SELECT COUNT(*) FROM generate_series(1,10); | QUERY_STATUS_SUBMIT
    -1 | SELECT COUNT(*) FROM generate_series(1,10); | QUERY_STATUS_START
    -1 | SELECT COUNT(*) FROM generate_series(1,10); | QUERY_STATUS_END
    -1 | SELECT COUNT(*) FROM generate_series(1,10); | QUERY_STATUS_DONE
(8 rows)
```

清空日志表：

```sql
SELECT gpsc.truncate_log();
```

要轮询运行中的查询，生成一个 16 字节的跟踪 ID，并传入运行该查询的 Coordinator 后端进程 ID：

```sql
SELECT * FROM gpsc.pg_query_state_backends(12345);
SELECT gpsc.pg_query_state(12345, '\x00112233445566778899aabbccddeeff'::bytea);
```

## 使用说明 {#usage-notes}

- 事件采用尽力传递方式。无法写入套接字的消息会被丢弃，不重试，因此代理响应缓慢或不存在时不会增加查询延迟。使用 `gpsc.stat_messages` 检查失败情况。
- 运行时查询状态结果推送至代理套接字，`gpsc.pg_query_state()` 不会将其返回给 SQL 调用者。
- 如果未通过 `shared_preload_libraries` 加载库、不存在指定 `pid` 的后端，或调用者无权轮询目标后端，`gpsc.pg_query_state()` 和 `gpsc.pg_query_state_backends()` 会报错。如果 `pid` 属于 Segment 执行器进程而非会话的 Coordinator 后端，`gpsc.pg_query_state_backends()` 也会报错。
- 进程级系统统计信息从 `/proc` 文件系统读取。
