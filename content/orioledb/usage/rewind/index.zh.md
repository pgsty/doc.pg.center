---
title: 基于撤销日志的回退
linkTitle: 撤销日志回退
description: 使用实验性回退功能，将数据库集群恢复到此前的一致状态。
weight: 30
type: docs
search_keywords: ["OrioleDB", "rewind", "undo", "回退"]
upstream_link: https://www.orioledb.com/docs/usage/rewind
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-clock-rotate-left
---


OrioleDB 提供基于撤销日志的回退能力，可将数据库集群恢复到此前的一致状态。时间点恢复（PITR）依赖预写日志（WAL）的重放，而 OrioleDB 回退利用撤销日志逆转修改。对于较近的数据库状态，这种机制通常比基于 WAL 的恢复更快，因为它通过撤销链直接逆转最近的修改。

对于 `orioledb` 表，回退使用引擎原生的撤销日志。对于 PostgreSQL 标准 `heap` 表，则通过延迟清理来支持回退：旧元组版本保留在堆中，直到超出配置的回退保留窗口。

> [!WARNING]
>
> 此功能处于实验阶段，会带来明显的性能损失。它默认关闭，应谨慎使用。

## 配置 {#configuration}

> [!WARNING]
>
> 回退仅在开发构建（`IS_DEV=1`）中可用。生产构建无法开启 `orioledb.enable_rewind`。

以下参数控制回退子系统，必须在 `postgresql.conf` 中或通过 `ALTER SYSTEM` 设置。

| 参数 | 类型 | 默认值 | 范围 | 说明 |
|----|----|----|----|----|
| `orioledb.enable_rewind` | `boolean` | `off` | on/off | 启用回退数据收集，并启动回退工作进程。 |
| `orioledb.rewind_max_time` | `integer` | `3600` | 1 - 86400 | 为回退保留事务记录的最大年龄，单位为秒。 |
| `orioledb.rewind_max_transactions` | `integer` | `100000` | 1 - `INT_MAX` | 回退队列保留的事务数上限。 |
| `orioledb.rewind_buffers` | `integer` | `1024` | 6 - `INT_MAX` | 用于回退元数据的共享内存缓冲区数量。 |
{.wide .expand}

> [!NOTE]
>
> 启用回退会增加后台进程数。请确保 `max_worker_processes` 留有足够余量，以容纳回退工作进程。

## 回退工作进程 {#the-rewind-worker}

当 `orioledb.enable_rewind` 设为 `on` 时，OrioleDB 会启动后台的**回退工作进程**，负责管理事务历史和撤销日志的生命周期。

### 主要职责 {#key-responsibilities}

- 监控回退队列。事务超过保留阈值后，将其条目标记为完成，使系统可以安全删除旧撤销文件，并清理 `heap` 中的死元组。
- 维护“回退边界”，即数据库可以安全回退到的最早时间点。
- 即使数据库空闲，也定期处理队列，防止存储膨胀。

> [!WARNING]
>
> 回退工作进程虽然用固定大小的环形缓冲区管理待办事项，但如果无法推进，会产生两个严重后果：
>
> - 如果工作进程落后，OrioleDB 就无法回收物理撤销日志中的空间。这些日志会从内存溢出到磁盘上的 `orioledb_undo` 目录，使该目录持续增长，直到工作进程追上进度。
>
> - 工作进程负责推进全局 xmin 边界。如果它卡在某个旧事务上，PostgreSQL 和 OrioleDB 会将所有后续行版本视为“可能仍然需要”。这会阻止 VACUUM 删除死元组，导致明显的表膨胀和查询性能下降。

## 回退函数 {#rewind-functions}

### `orioledb_rewind_by_time(seconds int4[, attempt_restart bool])` {#orioledb_rewind_by_timeseconds-int4-attempt_restart-bool}

从当前时间向前回退指定秒数，恢复集群状态。

- **参数：**
  - `seconds`：集群状态需要回退的秒数。
  - `attempt_restart`：为 `true` 时，回退后自动重启数据库系统；为 `false` 时，只关闭数据库。默认为 `false`。
- **示例：**
  - `SELECT orioledb_rewind_by_time(600);`：回退 10 分钟，然后关闭数据库，不重启。
  - `SELECT orioledb_rewind_by_time(600, true);`：回退 10 分钟，然后重启数据库。

### `orioledb_rewind_to_timestamp(target_time timestamptz[, attempt_restart bool])` {#orioledb_rewind_to_timestamptarget_time-timestamptz-attempt_restart-bool}

将集群回退到指定时间点。

- **参数：**
  - `target_time`：集群状态要回退到的精确时间戳。
  - `attempt_restart`：为 `true` 时，回退后自动重启数据库系统；为 `false` 时，只关闭数据库。默认为 `false`。
- **示例：**
  - `SELECT orioledb_rewind_to_timestamp('2025-01-01 12:00:00 UTC', true);`：回退到 UTC 时间 2025 年 1 月 1 日 12:00:00，并重启数据库。
  - `SELECT orioledb_rewind_to_timestamp('2025-01-01 12:00:00 UTC');`：回退到指定时间戳，然后关闭数据库，不重启。

------------------------------------------------------------------------

### `orioledb_rewind_to_transaction(xid int4, oxid int8[, attempt_restart bool])` {#orioledb_rewind_to_transactionxid-int4-oxid-int8-attempt_restart-bool}

将集群回退到由 PostgreSQL 事务 ID（`xid`）和 OrioleDB 事务 ID（`oxid`）共同标识的事务对**之前**的状态。

- **参数：**
  - `xid`：PostgreSQL 事务 ID。
  - `oxid`：OrioleDB 事务 ID。
  - `attempt_restart`：为 `true` 时，回退后自动重启数据库系统；为 `false` 时，只关闭数据库。默认为 `false`。
- **示例：**
  - `SELECT orioledb_rewind_to_transaction(1750, 555, true);`：将集群回退到事务对 `1750`/`555` 开始之前，并重启数据库。
  - `SELECT orioledb_rewind_to_transaction(1750, 555);`：回退到指定事务对之前，然后关闭数据库，不重启。

### 查看回退边界 {#examining-the-rewind-horizon}

使用以下函数检查可回退范围：

- `orioledb_get_current_oxid()`：返回当前 OrioleDB 事务 ID。如果当前事务尚未分配 ID，会分配一个新 ID。
- `orioledb_get_complete_xid()`：返回可用于回退的最早 PostgreSQL `xid`。
- `orioledb_get_complete_oxid()`：返回可用于回退的最早 OrioleDB `oxid`。

## 执行流程 {#operational-workflow}

调用回退函数后，系统执行以下步骤：

1. 验证目标在保留窗口（`rewind_max_time`）内，且 `orioledb.enable_rewind` 已启用。
2. 通知回退工作进程停止向缓冲区添加新事务。
3. 通知其他所有活动后端终止，最多等待 100 秒让它们退出。
4. 将数据页恢复到请求的状态。
5. 回退完成后，根据 `attempt_restart` 参数关闭数据库，或尝试重启 PostgreSQL 实例，以完成状态切换。

> [!WARNING]
>
> 自动重启只会尽力尝试一次。如果因配置错误等原因失败，必须人工介入才能让服务器重新上线。回退完成后 SQL 连接会立即断开，因此请确保拥有服务器的系统级访问权限，能够手动启动服务。

## 示例 {#examples}

若要回退到特定事务状态，必须先在期望的“恢复点”记录事务标识符。

1. **确定恢复点：**

``` sql
-- Record these values
SELECT pg_current_xact_id(), orioledb_get_current_oxid();

 pg_current_xact_id | orioledb_get_current_oxid
--------------------+---------------------------
               1750 |                       555
```

2. **执行修改：**

``` sql
-- Accidental data loss or undesired changes occur here
DROP TABLE important_data;
```

3. **执行回退：**

``` sql
-- Revert to the IDs recorded in step 1
SELECT orioledb_rewind_to_transaction(1750, 555);
```

*服务器会记录“Rewind complete”，随后关闭。*

> [!NOTE]
>
> 对于需要强一致性保证的应用，建议在作为回退目标的事务内显式锁定相关表，即上述示例的第 1 步。

## 限制与注意事项 {#limitations-and-caveats}

- 回退缓冲区位于共享内存中，重启后不会保留。无法回退到本次集群启动之前的时间点。
- 回退会破坏目标时间点之后的所有数据修改。建议在回退前备份。
- 回退需要保留 `heap` 表中的旧版本，因此回退窗口内的数据不能正常清理。大量写入 `heap` 表可能导致严重膨胀。
- 回退目前与物理复制不兼容。备库不会反映回退操作，将与主库失去一致性。
- 如果系统在回退阶段崩溃或被中断，数据库可能处于不一致状态。
