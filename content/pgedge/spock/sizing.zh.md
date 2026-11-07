---
title: 为 Spock 规划 PostgreSQL 资源
description: 按节点、数据库和订阅数量规划 Spock 所需的工作进程、复制槽、WAL 发送进程和复制源容量。
weight: 50
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/sizing.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 资源规划
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 复制消耗三种独立且分别配置的 Postgres 资源：后台工作进程槽、WAL 发送进程槽，以及复制槽/复制源。每种资源由不同参数控制，并且每种都根据集群的不同属性来确定大小。

教程中展示的许多值只是小型测试集群的起点，不是生产建议。本页解释 Spock 实际会启动哪些进程，以便你有意识地规划每个参数。


> [!WARNING]
>
> 本页每个有明确建议支撑的参数都需要**重启服务器**才能修改。容量不足不是软失败：当工作进程无法注册时，Spock 会抛出 `ERROR`，supervisor 会循环重试，因此复制完全不会启动。公式中包含少量余量，部分就是为了防止这种情况。
>

## Spock 在每个节点上运行什么 {#what-spock-runs-on-each-node}

| 进程 | 数量 | 计入 |
|---|---|---|
| Supervisor | 每个实例 1 个，始终运行 | `max_worker_processes` |
| 槽同步工作进程 | 每个实例 1 个 | `max_worker_processes` |
| Manager | 实例中每个**可连接数据库** 1 个 | `max_worker_processes` |
| 应用工作进程 | 每个已启用订阅 1 个 | `max_worker_processes` |
| 表同步工作进程 | 每个订阅最多同时 1 个 | `max_worker_processes` |
| Walsender | 从此节点流式传输的每个订阅 1 个；表同步期间每个订阅另加 1 个 | `max_wal_senders` |
{.wide .expand}

其中有四个数量常被误判。

**槽同步工作进程存在于每个节点上，而不只是在备库上。**这些工作进程把逻辑复制槽复制到每个物理备库，使故障转移不会迫使每个订阅者进行完整重新同步。这些工作进程在主节点上保持空闲，但仍占用一个工作进程槽，因此计入公式。更多信息参见下文[槽同步](#slot-synchronization)。

**Manager 会为每个可连接数据库启动，而不只是为使用 Spock 的数据库启动。**Supervisor 必须先连接数据库，才能确定该数据库是否包含 Spock 节点，而后台工作进程不能切换数据库。因此，它会为 `pg_database` 中每个 `datallowconn = true` 的数据库启动一个 manager；未找到 Spock 节点的 manager 会立即退出。在默认集群上，这意味着除了被复制的数据库之外，`postgres` 和 `template1` 各会有一个短暂的 manager。`template0` 被排除，因为它不允许连接。

**Walsender 不是后台工作进程。**它们由 `max_wal_senders` 控制，并单独计入 `MaxBackends`。提高 `max_worker_processes` 对 walsender 耗尽没有任何帮助，反之亦然。

**订阅按数据库计，而不是按节点计。**Spock 节点在单个数据库内创建，每个订阅把此实例上的一个数据库连接到另一个实例上的对应数据库。因此，复制多个数据库的实例中，每个被复制的数据库各有一个 Spock 节点，并且每个节点都携带自己的一整套订阅。订阅数量下游的所有内容，例如应用工作进程、表同步工作进程、walsender、槽和复制源，都随**节点数乘以被复制数据库数**扩展，而不只随节点数扩展。

### 槽同步 {#slot-synchronization}

对于带有物理备库的集群，槽同步不是可选项：没有它，提升会让每个订阅者重建自己的槽并重新同步表。PostgreSQL 版本之间变化的只是*由谁提供工作进程*。

| PostgreSQL | 提供者 | 是否计入 `max_worker_processes` |
|---|---|---|
| 15、16 | Spock 的 `spock_failover_slots` 后台工作进程 | 是 |
| 17 | 二者之一，取决于 `sync_replication_slots` | 是——Spock 仍会注册自己的工作进程；当原生工作进程启用时，它会退出 |
| 18+ | PostgreSQL 的原生 slotsync 工作进程 | 否——它是专用 postmaster 进程，单独计入 `MaxBackends` |
{.wide .expand}

在每个节点和每个版本上都为它预留一个工作进程。如果由 PostgreSQL 提供工作进程，预留的槽只是变成余量；除了少量共享内存外没有成本，并让你避免依赖版本的公式。[逻辑槽故障转移](/pgedge/spock/logical-slot-failover/)介绍每种机制所需的配置。

## 规划 `max_worker_processes` {#sizing-max_worker_processes}

对单个节点，在峰值时：

    spock_workers = 1    # supervisor
                  + 1    # slot sync worker
                  + D    # connectable databases in this instance
                  + S    # apply workers: one per enabled subscription
                  + S    # table sync workers: worst case, one per subscription

    max_worker_processes = spock_workers
                         + max_parallel_workers        # shared pool - see below
                         + other_extension_workers     # pg_cron, pg_squeeze, ...
                         + 2                           # headroom

其中：

- `N` 是集群中的 Spock 节点数。
- `D` 是实例中 `datallowconn = true` 的数据库数量，包括 `postgres` 和 `template1`——而**不只是**参与复制的数据库。
- `R` 是此实例中实际参与 Spock 复制的数据库数量（`R <= D`）。大多数部署中它是 `1`。
- `S` 是实例中所有数据库已启用订阅的总数。在一个每个节点复制相同 `R` 个数据库的 `N` 节点全互联集群中，`S = R * (N - 1)`。单个被复制数据库时，它简化为常见的 `S = N - 1`。


> [!WARNING]
>
> `max_worker_processes` 是**共享池**。并行查询工作进程（`max_parallel_workers`，默认 `8`）、原生逻辑复制工作进程（`max_logical_replication_workers`），以及其他扩展的后台工作进程都从同一分配中占用。并行很重的工作负载可能使复制得不到工作进程槽。Autovacuum 工作进程是例外——它们有独立的 `autovacuum_max_workers` 分配。
>

### 推荐最小值 {#recommended-minimums}

假设只有一个被复制数据库，并且同时存在 `postgres` 和 `template1`（`D = 3`、`R = 1`），默认 `max_parallel_workers = 8`，没有其他使用工作进程的扩展：

| 集群 | Spock 工作进程 | 工作进程总数 |
|---|---|---|
| 2 节点 | 7 | 20 |
| 3 节点 | 9 | 20 |
| 4 节点 | 11 | 24 |
| 5 节点 | 13 | 24 |
| 8 节点 | 19 | 32 |
{.wide .expand}

这些总数向上取整，为增长预留空间；过度配置 `max_worker_processes` 除了少量共享内存外没有明显成本，而且该参数不重启就无法修改。

如果你的实例承载更多数据库、复制多个数据库，或运行其他注册后台工作进程的扩展，请在这些数字上继续增加。每个**额外被复制的数据库**需要 `1` 个 manager（如果该数据库尚未计入 `D`），以及 `2 * (N - 1)` 个用于其应用和同步工作进程的 worker；因此，复制三个数据库的 3 节点集群每个实例需要 `3 * 2 * 2 = 12` 个应用和同步工作进程，而不是 `4` 个。

## 规划 `max_replication_slots` 与 `max_wal_senders` {#sizing-max_replication_slots-and-max_wal_senders}

每个节点为每个从它流式传输的订阅持有一个逻辑复制槽，并为每个进行中的表同步持有一个临时槽。同步槽会创建为持久槽（而不是临时槽），因此在同步完成并删除槽之前，每个同步槽都占用一个槽。流式传输时，每个槽背后都有一个 walsender；因此**把两个参数设置为相同值**，并基于槽数量一次性计算。


> [!NOTE] 默认值
>
> `max_replication_slots` 和 `max_wal_senders` 的默认值都是 10。可将它视为每个参数的最小值。如果任何公式给出的值低于 10，直接保留默认值。
>

其中 `N` 是 Spock 节点数，`R` 是实例中被复制数据库数：

    max_replication_slots = 2 * R * (N - 1)   # apply slot + sync slot per subscription
                          + physical_and_failover_slots
                          + 2                 # headroom for pg_basebackup and ad-hoc tooling

    max_wal_senders = max_replication_slots

大多数部署中 `R` 为 1。一个复制单个数据库的 5 节点全互联集群，如果每个节点有一个物理备库，两个参数都需要 `2 * 1 * 4 + 1 + 2 = 11`；同一个全互联集群复制三个数据库时需要 `2 * 3 * 4 + 1 + 2 = 27`。


> [!NOTE] 为什么两个值相等
>
> PostgreSQL 逻辑复制文档建议把 `max_wal_senders` 设置为至少 `max_replication_slots` 加上同时连接的物理副本数量。这个额外项覆盖没有槽但进行流式传输的物理备库；上面的公式已经在 `physical_and_failover_slots` 中为每个物理备库分配了槽，因此再相加会导致重复计数。用同一公式规划每个节点（包括备库），也满足另一个规则：备库的 `max_wal_senders` 至少要与其主库一样高。
>

并非每条复制连接都是 walsender。表同步工作进程会打开第二条非复制连接来运行 `COPY`，它占用 `max_connections`。备库上的槽同步工作进程同样通过普通连接访问主库。Spock 的工作进程和 PostgreSQL 的原生工作进程都会让主库消耗一个 `max_connections` 槽，而不是 walsender。

## 复制源 {#replication-origins}

Postgres 使用*复制源*跟踪远程复制槽的本地状态。在内部，Postgres 与槽分开跟踪复制源，并在 PostgreSQL 15-17 版本中把复制源数量上限固定为 `max_replication_slots`。我们的公式应使这些 PostgreSQL 版本中复制源不可能多于槽。

不过，Postgres 18 引入了 `max_active_replication_origins`，默认值为 10；对活跃的 Spock 集群来说，这个值可能过低。为简单起见，我们建议对该参数使用以下简单公式：

    max_active_replication_origins = max_replication_slots

这应使 Postgres 18+ 拥有足够大的复制源池运行。

## 示例 {#worked-examples}

由于这些设置涉及许多输入，本文档提供了一些示例。

### 3 节点全互联 {#3-node-mesh}

三个节点，每个都有一个被复制数据库 `app`，另有默认的 `postgres` 和 `template1` 数据库。每个节点订阅另外两个节点，且每个节点有一个物理备库。

每个节点：`D = 3`、`R = 1`、`S = R * (N - 1) = 2`。

```ini
# Background workers:
#   1 supervisor + 1 slot sync + 3 managers + 2 apply + 2 table sync = 9
#   + 8 max_parallel_workers + 2 headroom = 19; 20 to match the table above
max_worker_processes = 20

# Slots and walsenders, set equal:
#   (2 x 1 database x 2 subscribers) + 1 physical standby + 2 headroom = 7;
#   This is lower than the default of 10, so do not reduce.
max_replication_slots = 10
max_wal_senders = 10
```

### 5 节点全互联 {#5-node-mesh}

五个节点，每个都有被复制数据库 `app` 和 `ledger`，另有默认的 `postgres` 和 `template1` 数据库。每个节点订阅另外四个节点，且每个节点有两个物理备库；这在利用安全同步复制的集群中很常见。

每个节点：`D = 4`、`R = 2`、`S = R * (N - 1) = 8`。

```ini
# Background workers:
#   1 supervisor + 1 slot sync + 4 managers + 8 apply + 8 table sync = 22
#   + 8 max_parallel_workers + 2 headroom = 32
max_worker_processes = 32

# Slots and walsenders, set equal:
#   (2 x 2 databases x 4 subscribers) + 2 standbys + 2 headroom = 20
max_replication_slots = 20
max_wal_senders = 20
```

## 验证配置 {#verifying-your-configuration}

列出节点上当前运行的 Spock 工作进程：

```sql
SELECT pid, backend_type, datname
  FROM pg_stat_activity
 WHERE backend_type LIKE 'spock%'
 ORDER BY backend_type;
```

每个 Spock 工作进程都会在 `backend_type` 中报告自己的角色和所服务的 OID——例如 `spock supervisor`、`spock manager 16384` 和 `spock apply 16384:1`。

比较正在使用的后台工作进程数量与上限：

```sql
SELECT current_setting('max_worker_processes')::int AS worker_limit,
       count(*) AS in_use
  FROM pg_stat_activity
 WHERE backend_type NOT IN (
         'client backend', 'walsender', 'autovacuum launcher',
         'autovacuum worker', 'checkpointer', 'background writer',
         'walwriter', 'walreceiver', 'walsummarizer', 'archiver',
         'startup', 'io worker', 'standalone backend');
```

排除列表列出不占用 `max_worker_processes` 的客户端后端和辅助进程；其余进程都会占用。辅助进程类型列表会随主版本变化，因此请按你的版本对照 [`pg_stat_activity`](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)。

## 诊断资源耗尽 {#diagnosing-exhaustion}

**`worker registration failed, you might want to increase max_worker_processes setting`**

Postgres 拒绝注册后台工作进程，因为 `max_worker_processes` 已完全分配。用上面的公式重新计算，记住并行查询工作进程共享该池，然后重启。

**`could not register spock worker: all background worker slots are already used`**

Spock 自己的工作进程跟踪数组——其大小在启动时按 `max_worker_processes` 确定——没有空闲条目。正常退出的工作进程会立即释放条目，但*崩溃*的工作进程会将其条目保留给同一数据库，直到该数据库的 manager（或 supervisor）回收它。因此，跨许多不同数据库反复发生的工作进程崩溃可能耗尽数组，而 Postgres 仍报告有空闲工作进程槽。检查服务器日志中的前一个崩溃并处理它；提高 `max_worker_processes` 会扩大数组，但不会修复底层故障。

**订阅停留在 `initializing`**

通常是*提供者*上的 `max_replication_slots` 或 `max_wal_senders` 不足。正在初始化的订阅除了应用流已持有的槽和 walsender 之外，还需要为其同步工作进程提供一个槽和一个 walsender；这就是稳定状态下复制正常的集群，在添加或重新同步表时可能失败的原因。参见[故障排查](/pgedge/spock/troubleshooting/)。

**复制延迟增加但应用工作进程空闲**

如果 `spock.lag_tracker` 显示延迟增长但应用工作进程没有运行，请检查服务器日志中的工作进程注册失败——manager 会延迟重试注册，因此工作进程池耗尽会表现为间歇性应用，而不是立即停止。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/sizing.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
