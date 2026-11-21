---
title: gp_internal_tools
description: gp_internal_tools 是 Apache Cloudberry 的一组诊断工具。
weight: 90
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-internal-tools.md
---

`gp_internal_tools` 模块是 Apache Cloudberry 的一组诊断工具。扩展安装 `session_state` 模式，其中的视图显示各个会话在 Coordinator 和每个 Segment 上的内存消耗。此模块还附带共享库，为工作文件管理器、性能测量共享内存和 AO 表提供底层诊断函数。

> [!NOTE]
> 此模块用于故障排查。它暴露服务器内部状态，日常操作无需使用。

## 构建与安装 {#build-and-install}

`gp_internal_tools` 默认随 Apache Cloudberry 构建和安装，不需要任何 `configure` 选项。

构建会在安装目录的库目录中安装四个共享库：`gp_session_state_memory_stats`、`gp_workfile_mgr`、`gp_instrument_shmem` 和 `gp_ao_co_diagnostics`。

## 启用模块 {#enable-the-module}

在每个需要使用它的数据库中创建扩展。创建扩展需要超级用户权限，不需要 `shared_preload_libraries`。

```sql
CREATE EXTENSION gp_internal_tools;
```

扩展在 `session_state` 模式中创建对象。

## 扩展安装的对象 {#objects-installed-by-the-extension}

### session_state.session_level_memory_consumption {#session_statesession_level_memory_consumption}

此视图针对每个会话在每个实例（Coordinator 和各个 Segment）上返回一行，显示该会话在该实例上的内存使用量。视图的 `SELECT` 权限授予 `PUBLIC`。

| 列 | 类型 | 说明 |
|---|---|---|
| `datname` | `name` | 会话连接的数据库名称。 |
| `sess_id` | `integer` | 会话 ID。 |
| `usename` | `name` | 会话用户名。 |
| `query` | `text` | 会话的当前查询，与 `pg_stat_activity` 中显示的相同。 |
| `segid` | `integer` | Segment 内容 ID。`-1` 表示 Coordinator。 |
| `vmem_mb` | `integer` | 会话在此实例上使用的虚拟内存，单位为 MB。 |
| `is_runaway` | `boolean` | 会话在此实例上是否被标记为失控会话。 |
| `qe_count` | `integer` | 会话在此实例上的查询执行器进程数。 |
| `active_qe_count` | `integer` | 会话在此实例上的活跃查询执行器进程数。 |
| `dirty_qe_count` | `integer` | 会话的内部清理计数器（会话状态的 `cleanupCountdown` 字段）。 |
| `runaway_vmem_mb` | `integer` | 会话被标记为失控时的虚拟内存计数器值。 |
| `runaway_command_cnt` | `integer` | 会话被标记为失控时的命令计数。 |
| `idle_start` | `timestamp with time zone` | 此会话的查询执行器进程最近一次变为空闲的时间。 |

`datname`、`usename` 和 `query` 列来自按会话 ID 与 `pg_stat_activity` 进行的左连接，因此当其中找不到该会话时，这些列为 `NULL`。

### 函数 {#functions}

此视图基于两个集合返回函数。两者的 `EXECUTE` 权限均授予 `PUBLIC`。

| 函数 | 运行位置 | 说明 |
|---|---|---|
| `session_state.session_state_memory_entries_f_on_master()` | Coordinator | 返回 Coordinator 的会话内存条目。 |
| `session_state.session_state_memory_entries_f_on_segments()` | 所有 Segment | 返回每个 Segment 的会话内存条目。 |

两个函数均返回 `SETOF record`，包含列 `(segid int, sessionid int, vmem_mb int, runaway_status int, qe_count int, active_qe_count int, dirty_qe_count int, runaway_vmem_mb int, runaway_command_cnt int, idle_start timestamp with time zone)`。应查询视图，不要直接调用它们。

## 示例 {#example}

```sql
CREATE EXTENSION gp_internal_tools;

SELECT * FROM session_state.session_level_memory_consumption LIMIT 0;
```

```text
 datname | sess_id | usename | query | segid | vmem_mb | is_runaway | qe_count | active_qe_count | dirty_qe_count | runaway_vmem_mb | runaway_command_cnt | idle_start
---------+---------+---------+-------+-------+---------+------------+----------+-----------------+----------------+-----------------+---------------------+------------
(0 rows)
```

查看当前会话在每个实例上使用的内存：

```sql
SELECT m.segid, m.vmem_mb, m.is_runaway
FROM session_state.session_level_memory_consumption m, pg_stat_activity a
WHERE a.pid = pg_backend_pid()
  AND m.sess_id = a.sess_id;
```

## 其他诊断库 {#additional-diagnostic-libraries}

此模块还构建并安装以下共享库。扩展脚本不为它们创建 SQL 函数：`CREATE EXTENSION gp_internal_tools` 只安装上文所述的 `session_state` 对象。这些库中的 C 函数是服务器内部函数的简单包装，供支持和开发工作使用。

| 库 | C 函数 | 用途 |
|---|---|---|
| `gp_workfile_mgr` | `gp_workfile_mgr_cache_entries`, `gp_workfile_mgr_used_diskspace` | 工作文件管理器诊断。`gp_workfile_mgr_cache_entries` 返回一个 Segment 的工作文件缓存条目。`gp_workfile_mgr_used_diskspace` 返回一行 `(segid int4, bytes int8)`，包含 Segment 上工作文件使用的字节数。 |
| `gp_instrument_shmem` | `gp_instrument_shmem_summary`, `gp_instrument_shmem_detail` | 诊断共享内存中的性能测量槽。`gp_instrument_shmem_summary` 返回 `(segid int4, num_free int8, num_used int8)`。`gp_instrument_shmem_detail` 为每个已用槽返回一行，包含 `(tmid int4, ssid int4, ccnt int2, segid int2, pid int4, nid int2, tuplecount int8, nloops int8, ntuples int8)`。 |
| `gp_ao_co_diagnostics` | `gp_aoseg_wrapper`、`gp_aoseg_history_wrapper`、`gp_aocsseg_wrapper`、`gp_aocsseg_history_wrapper`、`gp_aoblkdir_wrapper`、`gp_aovisimap_wrapper`、`gp_aovisimap_entry_wrapper`、`gp_aovisimap_hidden_info_wrapper` 等 | AO 行存表和 CO 列存表诊断：段文件元数据（包括历史不可见条目）、块目录条目，以及每个段文件的隐藏元组数等可见性映射信息。 |

## 使用说明 {#usage-notes}

- 视图会在每个 Segment 上调用函数，因此对它的每次查询都会派发至整个集群。
- 删除扩展会移除 `session_state` 模式中的视图和函数。
