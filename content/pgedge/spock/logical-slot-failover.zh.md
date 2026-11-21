---
title: 逻辑复制槽故障切换
description: 将 Spock 提供者上的逻辑复制槽同步到物理备库，支持故障切换后继续复制。
weight: 100
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/logical_slot_failover.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: 复制槽故障切换
type: docs
---

Spock 在每个提供者节点上创建逻辑复制槽。使用物理备库实现高可用时，必须将这些槽同步到备库，才能在故障切换后恢复复制而不丢失数据。

## 工作原理 {#how-it-works}

主服务器故障、物理备库被提升后，所有活动的逻辑订阅者都必须能从新主库继续复制。这要求跟踪各订阅者复制位置的逻辑复制槽在故障切换发生前就已存在于备库上，并保持最新。

如果不进行复制槽同步，故障切换后就必须手动重建复制槽，并完整重新同步订阅者的所有表。

## 各 PostgreSQL 版本的行为 {#postgresql-version-behaviour}

| PostgreSQL | 复制槽同步机制 | Spock 工作进程 |
|---|---|---|
| 15、16 | Spock 内置的 `spock_failover_slots` 工作进程 | 在每个节点注册；仅在恢复期间同步 |
| 17 | Spock 工作进程**或**原生 `sync_replication_slots` | 如果启用原生机制，则让其接管 |
| 18+ | 原生 `sync_replication_slots`（必需） | 不注册 |
{.wide .expand}

机制随版本变化，但要求不变：集群的每个节点上都运行复制槽同步工作进程，包括主库和备库。进程在服务器知道自身角色之前启动，因此在主库上会常驻并保持空闲，仅醒来检查服务器是否已进入恢复。Spock 自己的工作进程通过 `shared_preload_libraries` 注册，占用一个 `max_worker_processes` 槽位；PostgreSQL 原生工作进程则是该进程池之外的专用 postmaster 子进程。无论哪种机制，都要在每个节点上为它预留进程资源，参见[为 Spock 规划 PostgreSQL 资源](/pgedge/spock/sizing/)。

在 **PostgreSQL 17+** 上，Spock 创建每个逻辑复制槽时都会设置 `FAILOVER` 标志，使 PostgreSQL 内置的 slotsync 工作进程能自动同步它们。

在 **PostgreSQL 18+** 上，Spock 完全不注册自己的故障切换工作进程。只有原生 slotsync 工作进程负责复制这些槽。Spock 的 walsender 等待机制（`spock.pg_standby_slot_names` 配合 `spock.standby_slots_min_confirmed`）仍可在所有版本使用，因为 `synchronized_standby_slots` 只能等待列表中的所有槽。

## 所需设置 {#which-settings-you-need}

两条同步路径需要不同的设置，但都假定已完成 Spock 的基础设置。

### 基础设置（所有版本、每个节点） {#base-settings-all-versions-every-node}

这些设置是 Spock 能够执行复制的基础要求，详见[安装与配置 Spock](/pgedge/spock/installation/)。

```ini
wal_level = logical
shared_preload_libraries = 'spock'
track_commit_timestamp = on
max_worker_processes = 20
max_replication_slots = 10
max_wal_senders = 10
```

请按集群规模规划这些值，不要直接照抄数字，参见[为 Spock 规划 PostgreSQL 资源](/pgedge/spock/sizing/)。复制槽、walsender 和复制源的数量随其他节点数与实例中参与复制的数据库数的乘积增长，`max_replication_slots` 和 `max_wal_senders` 应设为相同值。注意，物理备库会使主库所需的槽数再增加一个；复制槽同步工作进程在每个节点上占用一个 `max_worker_processes` 槽位。

在 PostgreSQL 18 上，还要将 `max_active_replication_origins`（默认 10）设为至少等于此节点应用的订阅数，并留出一定余量；全网状拓扑中的订阅数为 `(nodes - 1) x replicated
databases`。将其设为与 `max_replication_slots` 相同，是最简单的安全选择。

### 原生路径（启用 `sync_replication_slots = on` 的 PostgreSQL 17，以及 PostgreSQL 18） {#native-path-postgresql-17-with-sync_replication_slots--on-and-postgresql-18}

由 PostgreSQL 内核复制这些槽。在基础设置之外，还需配置以下参数。

| 设置 | 节点 | 值 | 用途 |
|---|---|---|---|
| `sync_replication_slots` | 备库 | `on` | 启用内核复制槽同步工作进程。18 上必需，17 上可选。 |
| `hot_standby_feedback` | 备库 | `on` | 阻止主库删除复制槽仍需要的系统目录行。 |
| `primary_slot_name` | 备库 | 物理槽名称 | 备库进行流复制时使用的物理槽。 |
| `primary_conninfo` | 备库 | 含 `dbname` 的连接字符串 | 备库连接主库的方式。 |
| `synchronized_standby_slots` | 主库 | 物理槽名称 | 暂缓逻辑 walsender，直到列表中的所有备库均已接收变更。存在多个备库、希望“任意 N 个”确认即可时，改用下方两个 Spock 设置；两种机制只能选其一。 |
| `spock.pg_standby_slot_names` | 主库 | `''` | 逻辑复制前进前必须确认 LSN 的物理槽。可选。 |
| `spock.standby_slots_min_confirmed` | 主库 | `-1` | 上述槽中必须确认的数量。`-1` 表示全部；`1` 可在多个备库中的一个停机时继续复制。 |
| 槽的 `failover = true` | 主库 | 按槽设置 | 只有带此标志的槽才会同步。Spock 6.0.0 在创建时设置；旧槽在升级时处理。 |
{.wide .expand}

当 `spock.standby_slots_min_confirmed` 小于列表中的槽数时，订阅者可能收到某些备库尚未接收的变更。故障后，应提升 `pg_last_wal_receive_lsn()` 最大的备库：它包含已发送给订阅者的所有变更。提升更落后的备库，会使订阅者持有新主库从未拥有过的行。

备库会从包含 `spock.pg_standby_slot_names` 的文件继承该设置，包括 `pg_basebackup` 复制的 `postgresql.conf` 或 `postgresql.auto.conf`。提升后，新主库并不具备该设置列出的物理槽，因此值为 `-1` 时，每个逻辑 walsender 都会等待这些槽，直到 `wal_sender_timeout` 超时并发出警告。请在新主库上创建这些槽，或清空该设置，处理方式与下面操作手册中的 `synchronized_standby_slots` 相同。正在等待的 walsender 在超时前也无法察觉服务器关闭。

备库连接之前，物理槽必须已经在主库上创建：

```sql
SELECT pg_create_physical_replication_slot('spock_standby_slot');
```

### Spock 工作进程路径（PostgreSQL 15、16，以及关闭 `sync_replication_slots` 的 17） {#spock-worker-path-postgresql-15-16-and-17-when-sync_replication_slots-is-off}

由备库上的 Spock 后台工作进程复制这些槽。在基础设置之外，还需配置以下参数。

| 设置 | 节点 | 默认值 | 用途 |
|---|---|---|---|
| `hot_standby_feedback` | 备库 | `on`（需要设置） | 工作进程开始任何同步前的必要条件，并阻止主库删除所需的系统目录行。 |
| `primary_slot_name` | 备库 | 物理槽名称 | 备库进行流复制时使用的物理槽。 |
| `primary_conninfo` | 备库 | 连接字符串 | 备库连接主库的方式。 |
| `spock.synchronize_slot_names` | 备库 | `name_like:%%` | 要同步哪些槽。默认全部。 |
| `spock.drop_extra_slots` | 备库 | `on` | 删除主库上已不存在的备库槽。 |
| `spock.primary_dsn` | 备库 | `''` | 连接主库的字符串。为空时使用 `primary_conninfo`。 |
| `spock.pg_standby_slot_names` | 主库 | `''` | 逻辑复制前进前必须确认 LSN 的物理槽。可选。 |
| `spock.standby_slots_min_confirmed` | 主库 | `-1` | 上述槽中必须确认的数量。`-1` 表示全部。 |
| `spock.failover_slots_naptime` | 备库 | `1000` | 两轮槽同步之间工作进程的休眠时间，单位毫秒（SIGHUP；范围 1–3600000）。 |
| `spock.failover_slots_feedback_naptime` | 备库 | `10000` | 等待备库 WAL 反馈时采用的较短重试间隔，单位毫秒（SIGHUP；范围 1–3600000）。 |
| `spock.failover_slots_recreate_invalidated` | 备库 | `on` | 当备库上的同步槽副本失效时，删除并重建该槽。`off` 保持原状并报告一次。仅用于 PG15–17；PG17 使用原生槽同步时及 PG18+ 均忽略（SIGHUP）。 |
| `spock.failover_slots_database` | 备库 | `''` | 工作进程连接的数据库，以便在备库上解码每个副本并为其建立一致快照。默认关闭；不设置时，提升后可能丢失事务。仅用于 PG16–17，PG18+ 忽略；PG16 上必须是槽所属的数据库（需要重启）。 |
{.wide .expand}

关键是同时配置 `hot_standby_feedback = on` 和 `primary_slot_name` 指定的物理槽。缺少其中任一项，主库都可能删除槽仍需要的系统目录行，导致槽失效，并出现与恢复冲突的消息。

## 配置：PostgreSQL 17 和 18（原生机制） {#setup-postgresql-17-and-18-native}

这是原生槽同步路径，也是 PostgreSQL 18 上唯一的选择。PostgreSQL 17 上可选：默认运行 Spock 工作进程；在备库设置 `sync_replication_slots = on` 后，Spock 会让 PostgreSQL 内核接管同步。原生同步只复制 `failover = true` 的槽。Spock 6.0.0 在创建槽时设置该标志；旧版 Spock 创建的槽请参见下方升级部分。如果 PostgreSQL 17 备库此前已由 Spock 工作进程同步，请改按[将 PostgreSQL 17 备库从 Spock 工作进程切换到原生机制](#switching-a-postgresql-17-standby-from-the-spock-worker)操作：只设置 `sync_replication_slots = on` 会使大部分或全部槽无法同步。

### 1. 在主库上创建物理复制槽 {#1-create-a-physical-replication-slot-on-the-primary}

```sql
SELECT pg_create_physical_replication_slot('spock_standby_slot');
```

### 2. 配置主库（`postgresql.conf`） {#2-configure-the-primary-postgresqlconf}

```ini
# Hold walsenders back until the standby has confirmed this LSN,
# preventing logical subscribers from getting ahead of the standby.
synchronized_standby_slots = 'spock_standby_slot'
```

### 3. 配置备库（`postgresql.conf`） {#3-configure-the-standby-postgresqlconf}

```ini
sync_replication_slots = on
primary_conninfo = 'host=<primary_host> port=5432 dbname=<dbname> user=replicator'
primary_slot_name = 'spock_standby_slot'
hot_standby_feedback = on
```

### 4. 验证复制槽同步 {#4-verify-slot-synchronization}

在备库上确认 Spock 的逻辑槽已同步：

```sql
SELECT slot_name, synced, failover, invalidation_reason
FROM pg_replication_slots
WHERE NOT temporary;
```

所有 Spock 槽都应显示 `synced = true` 和 `failover = true`。

### 5. 故障切换后 {#5-after-failover}

提升备库后，订阅者只需更新连接字符串，将其指向新主库。复制会从最后同步的 LSN 恢复，无需重建槽，也不会丢失数据。

**重要：** 如果被提升的节点设置了 `synchronized_standby_slots` 或 `spock.pg_standby_slot_names`，必须先调整该设置，复制才能恢复：两者都引用了新主库并不具备的物理槽。参见下面的[操作手册：提升后清空 `synchronized_standby_slots`](#runbook-clear-synchronized_standby_slots-after-promotion)。

## 将 PostgreSQL 17 备库从 Spock 工作进程切换到原生机制 {#switching-a-postgresql-17-standby-from-the-spock-worker}

Spock 工作进程在备库上创建的副本具有 `synced = false`。原生槽同步不会接管同名槽，只要这些副本仍存在，就会不断失败。切换步骤如下：

1. 在主库上列出备库应该保留的槽。Spock 工作进程复制所有匹配 `spock.synchronize_slot_names` 的逻辑槽（默认全部），而原生同步只复制 `failover = true` 的槽：

    ```sql
    SELECT slot_name, plugin, failover
    FROM pg_replication_slots
    WHERE slot_type = 'logical' AND NOT temporary;
    ```

    `spock.slot_enable_failover()` 为 Spock 自己的槽设置该标志（参见[将 Spock 升级到 6.0.0](#upgrading-spock-to-600)）。其他需要保留的槽也要设置，例如在 PostgreSQL 订阅者上禁用订阅后，执行 `ALTER SUBSCRIPTION ... SET (failover = true)`。没有该标志的槽在切换后不会被同步。
    保持主库上等待备库确认的设置（`spock.pg_standby_slot_names` 或 `synchronized_standby_slots`）不变；如果两者均未设置，参见[原生配置的步骤 2](#2-configure-the-primary-postgresqlconf)。
2. 在备库上检查 `wal_level = logical`，并确认 `primary_conninfo` 包含 `dbname`。原生槽同步使用 `primary_conninfo` 建立普通数据库连接，而非复制连接，因此其用户需要在主库上有相应的 `pg_hba.conf` 条目和该数据库的 `CONNECT` 权限；Spock 工作进程此前可能通过 `spock.primary_dsn` 使用其他用户连接。然后设置 `sync_replication_slots = on` 并重新加载配置。Spock 工作进程将停止同步。
3. 等待一个 `spock.failover_slots_naptime` 间隔，再列出 Spock 工作进程在备库上创建的副本。已经开始的一轮同步可能持续超过该等待时间，并在删除之后又创建副本；步骤 4 会发现它。

    ```sql
    SELECT slot_name, plugin, active, active_pid
    FROM pg_replication_slots
    WHERE slot_type = 'logical' AND NOT synced AND NOT temporary;
    ```

    副本与主库上的槽同名。仅存在于备库上的槽，例如为备库解码而在备库创建的槽，不属于副本，应予保留。如果副本显示 `active = true`，说明它正在使用中；在 `active_pid` 对应的进程停止使用它之前，删除会失败。请停止该客户端，或使用 `pg_terminate_backend(active_pid)` 终止它。按名称逐个删除副本：

    ```sql
    SELECT pg_drop_replication_slot('<slot_name>');
    ```

4. 重复执行[验证复制槽同步](#4-verify-slot-synchronization)中的查询，直到主库上所有 `failover = true` 的槽都出现在备库上，且 `synced = true`、没有 `invalidation_reason`。如果步骤 3 的删除失败，或副本仍显示 `synced = false`，再次删除。若没有槽出现，检查备库日志中的槽同步连接错误。原生槽同步会将新副本暂时保留为临时槽，不出现在此查询结果中，直到主库上该槽的消费者前进到备库为它保留的位置之后；此时备库会记录 "could not synchronize replication slot"。如果订阅者空闲、暂停或停机，该槽可能一直保持此状态，直到订阅者追上。

在原生槽同步重建某个槽之前，备库上没有该槽的可用副本，因此期间不要提升备库。

## 操作手册：提升后清空 `synchronized_standby_slots` {#runbook-clear-synchronized_standby_slots-after-promotion}

配置 `synchronized_standby_slots` 后（上面的配置步骤 2），提供者的 walsender 会暂缓逻辑解码，直到列表中的每个物理槽都确认相关 LSN 已刷盘。这能防止物理备库落后于逻辑订阅者，但在故障切换时有一个陷阱。

该设置本应作用于主库，但备库往往也有：

- 使用 `pg_basebackup` 创建备库时，它已存在于主库的 `postgresql.auto.conf` 中，而该文件也会被复制；
- 所有节点部署了同一份 `postgresql.conf`；或
- Patroni 等集群管理器对每个成员应用同一份配置（参见[在 Patroni 下运行](#running-under-patroni-postgresql-17)）。

如果备库也有此设置，被提升后，列表仍指向提升前为*该节点*输送复制数据的物理槽。这些槽现已孤立：没有任何消费者，也就永远不会确认，新主库的 walsender 会无限期阻塞等待。实际症状是，看似成功的提升之后，面向订阅者的逻辑复制立即**停住**。在被提升的节点上执行 `SHOW synchronized_standby_slots;` 检查。

如果设置了该参数，清空它是提升后的必做步骤，而非可选清理：

```sql
-- On the newly promoted node:
ALTER SYSTEM SET synchronized_standby_slots = '';
SELECT pg_reload_conf();
```

物理槽本身位于创建它的服务器上。在上述配置中就是旧主库，因此该节点重建或退役后，请在那里删除 `spock_standby_slot`：

```sql
-- On the old primary, once it is no longer needed:
SELECT pg_drop_replication_slot('spock_standby_slot');
```

在 Patroni 下，成员槽由 Patroni 管理：它会在 `member_slots_ttl` 到期后移除离开成员的槽，因此不要手动删除。

如果新拓扑也有物理备库，请将 `synchronized_standby_slots` 设为*新备库*的物理槽，而非清空为 `''`。目的是去除对孤立槽的引用，避免设置仍指向永远没有消费者的槽。

将此步骤与前述订阅者 DSN 更新一起加入故障切换操作手册。使用原生故障切换槽时，遗漏此步骤是“故障切换成功但复制停止”报告中最常见的原因。

## 在 Patroni 下运行（PostgreSQL 17+） {#running-under-patroni-postgresql-17}

Patroni 自行管理复制槽，其管理方式决定了 Spock 的两种机制中哪一种能在它下面工作。

- **成员槽。** 当 `postgresql.use_slots: true`（默认值）时，Patroni 在每个副本的上游为其创建一个以成员命名的物理槽（见下方[槽名称](#slot-names)），并在成员离开 `member_slots_ttl`（默认 `30min`）后删除。主备切换时，新领导者为其他成员创建新槽。
- **永久槽。** 动态配置中 `slots:` 下列出的槽在主备切换后仍保留。永久*逻辑*槽通过停止并重新启动副本，从领导者复制到每个副本，然后每隔 `loop_wait` 秒推进一次。这是 PostgreSQL 尚无原生机制时 Patroni 自己实现的逻辑槽故障切换方案。
- **未知槽。** 在副本上，Patroni 会删除不由它管理的逻辑槽。自 Patroni 4.1.0 起，它不再处理以 `failover = true` 创建的槽，但 PostgreSQL 17 及之后的版本有一个例外：它会在副本上移除 `synced` 为 false 的故障切换槽。旧领导者自己的槽在主备切换后就是此状态；删除它们是为了让 PostgreSQL 的 slotsync 工作进程将其重建为新领导者槽的同步副本。Patroni 4.1.4 修复了此路径中的崩溃。

Spock 内置的 `spock_failover_slots` 工作进程在 Patroni 下并不可靠。它手动将逻辑槽复制到备库，并依赖备库的物理槽，通过 `hot_standby_feedback` 固定主库上的 `catalog_xmin`。拓扑变化时，Patroni 会删除并重建这个物理槽，使繁忙主库上的 vacuum 得以删除复制槽仍需要的系统目录行。槽随后失效（`invalidation_reason =
rows_removed`），订阅者必须从头重新同步。

可行的路径是 PostgreSQL 自己的机制：Spock 创建逻辑槽时设置 `FAILOVER` 标志，因此在 `sync_replication_slots = on` 时，slotsync 工作进程使每个成员上的槽保持最新，而 Patroni 从 4.1.0 起不会干预。PostgreSQL 18 上只有此路径，因为 Spock 不在那里注册自己的工作进程。PostgreSQL 17 上，除非设置 `sync_replication_slots = on`，否则 Spock 工作进程会运行，因此在 Patroni 下请启用该设置。如果成员此前已由 Spock 工作进程同步，请按照[将 PostgreSQL 17 备库从 Spock 工作进程切换到原生机制](#switching-a-postgresql-17-standby-from-the-spock-worker)操作。具体机制见[配置：PostgreSQL 17 和 18（原生机制）](#setup-postgresql-17-and-18-native)；本节说明这些设置在 Patroni 配置中的位置，以及主备切换对它们的影响。

**要求：** PostgreSQL 17 或更新版本，以及 Patroni 4.1.4 或更新版本。使用更早的 Patroni 时，请在动态配置中加入 `ignore_slots` 条目保护这些槽，使 Patroni 既不删除也不复制它们：

```yaml
ignore_slots:
  - plugin: spock_output
    type: logical
```

### 必需设置 {#required-settings}

| 设置 | 值 | 位置 | 需要重启？ | 原因 |
|---|---|---|---|---|
| `sync_replication_slots` | `on` | 动态配置 | 否（重新加载） | PostgreSQL 的 slotsync 工作进程将带标志的槽复制到每个副本 |
| `hot_standby_feedback` | `on` | 动态配置 | 否（重新加载） | 槽同步所必需；固定 `catalog_xmin`，防止 vacuum 删除槽所需的行。只有配置永久逻辑槽时 Patroni 才会自行启用它，因此需要显式设置 |
| `wal_level` | `logical` | 动态配置 | 是 | 逻辑解码和槽同步所必需 |
| `output_plugin_libraries` | 包含 `spock_output` | 动态配置，**每个成员** | 否（重新加载） | 仅用于具有此参数的服务器（见下文）。同步槽仍使用 `spock_output` 作为插件，因此缺少此设置的成员在提升后无法提供复制服务 |
| `postgresql.use_slots` | `true` | Patroni 配置 | 不适用 | 默认值。Patroni 创建每个副本进行流复制所用的成员槽，并将 `primary_slot_name` 设为该槽，这是槽同步的要求 |
| `max_replication_slots` / `max_wal_senders` | 按集群规模设置 | 动态配置 | 是 | 每个节点上的成员槽加 Spock 逻辑槽；参见[资源规划](/pgedge/spock/sizing/) |
| `synchronized_standby_slots` | 备库成员槽名称 | 动态配置或回调 | 否（重新加载） | 可选但建议设置；让领导者的 walsender 等待备库收到 WAL。参见[主备切换的陷阱](#the-switchover-sharp-edge-synchronized_standby_slots) |
{.wide .expand}

在 Patroni 下，槽同步的两个要求无需额外操作：Patroni 为副本写入的 `primary_conninfo` 始终包含 `dbname`，而 `primary_slot_name` 就是成员槽。

“动态配置”指 Patroni 存储在 DCS 中的配置：首次初始化集群时使用 `bootstrap.dcs.postgresql.parameters`，集群运行后使用 `patronictl edit-config`。下一节给出完整的初始化配置块。

### 设置位置（初始化时） {#where-the-settings-go-bootstrap}

集群范围的 PostgreSQL 参数应放在 Patroni 动态配置中（初始化时用 `bootstrap.dcs.postgresql.parameters`，之后用 `patronictl edit-config`），使所有成员，包括当前和未来的领导者，使用一致设置。请在此处配置，不要写入各节点独立的 `postgresql.conf`。

```yaml
bootstrap:
  dcs:
    postgresql:
      use_slots: true
      parameters:
        wal_level: logical
        hot_standby_feedback: "on"          # required by slot synchronization
        sync_replication_slots: "on"        # PG slotsync worker copies FAILOVER slots
        max_replication_slots: 10
        max_wal_senders: 10
        # Only on servers that have this parameter -- see the note below
        output_plugin_libraries: "pgoutput, test_decoding, spock_output"
```

`output_plugin_libraries` 随 PostgreSQL 2026 年安全修复引入（CVE-2026-6471，已回补至所有受支持的大版本）：未列在其中的库不得用作输出插件，默认列表不含 `spock_output`。同步槽仍使用 `spock_output` 作为插件，因此缺少此设置的成员作为副本时看似健康，一旦提升就无法提供复制服务；问题恰好在主备切换时暴露。该参数属于 `PGC_SUSET`，Patroni 可重新加载，无需重启。

不要在早于此修复的版本上设置它：无法识别的参数会阻止服务器启动，通过 DCS 推送则会使*每个*成员都无法启动。先在每个成员上执行 `SELECT current_setting('output_plugin_libraries', true)` 检查；结果为 NULL 表示不存在此参数。

**不要**将 Spock 逻辑槽声明为 Patroni 的*永久逻辑槽*（`slots:` 配置块）。原生路径正是为了取代这种手动复制：Patroni 会重启副本以复制槽，并自行推进槽，与 slotsync 工作进程相互竞争。`slots:` 配置块只用于需要保留的物理槽，逻辑槽交由 PostgreSQL 管理。

### 槽名称 {#slot-names}

Patroni 从成员名称派生槽名称：转换为小写，将 `-` 和 `.` 替换为 `_`，将 `[a-z0-9_]` 以外的其他字符表示为 `u` 加四位码点，并截断为 63 个字符。成员 `pg-node.1` 通过槽 `pg_node_1` 进行流复制。设置 `synchronized_standby_slots` 中的槽名称时必须遵循同一规则，因此下方示例回调向 Patroni 获取名称，而不自行计算。

### 主备切换的陷阱：`synchronized_standby_slots` {#the-switchover-sharp-edge-synchronized_standby_slots}

`synchronized_standby_slots` 指定领导者的 walsender 必须等待哪些物理槽，以免逻辑订阅者超前于可能被提升的备库。在 Patroni 下，这些就是成员槽；因此，在领导者为 `n2`、副本为 `r1` 的双成员集群中，领导者需要：

```
synchronized_standby_slots = 'r1'
```

陷阱在于，这个值*取决于节点角色*，而 Patroni 的动态配置却是*集群范围*的。若硬编码为 `'r1'`，之后切换使 `r1` 成为领导者，新领导者就会等待以自身命名、却并不存在于自身上的槽：walsender 阻塞，逻辑复制停住。这正是[提升后操作手册](#runbook-clear-synchronized_standby_slots-after-promotion)描述的故障；在 Patroni 下，如果不处理，每次主备切换都会重现。

列表中任何停机成员也会触发同样的等待。它的槽在领导者上保持非活动状态，直到 `member_slots_ttl` 到期后被 Patroni 删除；槽无论不活动还是不存在，都会造成阻塞。因此，一个备库停止，就会使逻辑复制停止，直到它恢复或从列表中移除。

有三种处理方式：

- **使用回调和定期核对自动处理。** Patroni 在提升和降级时执行 `on_role_change` 回调，参数为 `on_role_change <role> <scope>`；角色为 `primary` 或 `replica`（4.0 之前使用 `master`）。成为领导者时，脚本将 `synchronized_standby_slots` 设为其他正常运行成员的槽，并重新加载；成为副本时清空。

  ```yaml
  postgresql:
    callbacks:
      on_role_change: /etc/patroni/set_synchronized_standby_slots.sh
  ```

  仅有该回调还不够，因为停机备库恢复或备库离开时，Patroni 不会执行它。提升后重新加入的备库可能仍不在列表中，使订阅者超前。因此，还要在每个成员上通过 cron 或 systemd 定时器，定期以 `set_synchronized_standby_slots.sh reconcile <scope>` 运行同一脚本：它向 Patroni 查询当前成员角色，并更新该设置，仅在值不同时修改。备库恢复流复制后的第一次核对起才受到保护，请据此选择间隔。

  Spock 附带参考实现 [`samples/set_synchronized_standby_slots.sh`](https://github.com/pgEdge/spock/blob/main/samples/set_synchronized_standby_slots.sh)。它从 `patroni.yml` 读取成员名称，使用 Patroni 自己的函数派生槽名，跳过未运行或未进行流复制的成员，并在无法读取成员列表时保持设置不变。它只支持 Patroni 自己管理的成员槽，要求开启 `use_slots`，且没有手动设置的 `primary_slot_name`。用于生产之前请审查并按需调整。

- **交由 Patroni 管理。** Patroni 开发分支提供 `manage_synchronized_standby_slots` 选项，使 `synchronized_standby_slots` 始终等于 `synchronous_standby_names` 中的同步备库。它要求启用 `synchronous_mode`；本文撰写时尚未随正式版本发布（当时最新版本为 4.1.5）。发布后，对于采用同步复制的集群，应优先使用它而非回调。

- **不设置，并接受相应取舍。** 主备切换时不会停住，但领导者在允许订阅者前进之前不再等待备库。因此，在提升瞬间，订阅者可能略微领先于备库，新领导者也就略微落后于订阅者。若要求零数据丢失，请采用前两种方案之一。

### 主备切换的过程 {#what-a-switchover-does}

1. `patronictl switchover` 将领导者降级，并提升一个副本。
2. 新领导者上的同步 Spock 槽变为可用；订阅者只需将 DSN 指向它，见[故障切换后](#5-after-failover)。
3. 旧领导者作为副本重新加入。它自己的 Spock 槽带有 `failover = true` 和 `synced = false`；Patroni 4.1.0 及之后的版本会在该副本上删除这些槽，再由 slotsync 工作进程从新领导者重建同步副本。
4. 必须运行管理 `synchronized_standby_slots` 的操作：在两个节点上触发回调，或手动执行操作手册。

### 验证 {#verify}

初始化之后，以及每次主备切换之后，确认每个副本都具有带标志且已同步的槽：

```sql
-- on each replica
SELECT slot_name, synced, failover, invalidation_reason
FROM pg_replication_slots
WHERE plugin = 'spock_output' AND NOT temporary;
```

`synced` 和 `failover` 都应为 `true`，`invalidation_reason` 应为 `NULL`。如果 `failover` 为 `false`，说明槽由 Spock 6.0.0 之前的版本创建，且升级时未能设置标志。处理方法见[将 Spock 升级到 6.0.0](#upgrading-spock-to-600)。在领导者上，`SHOW synchronized_standby_slots` 应列出正常运行副本的槽，`patronictl list` 应显示它们正在进行流复制。

## 配置：PostgreSQL 15 和 16（Spock 工作进程） {#setup-postgresql-15-and-16-spock-worker}

在 PostgreSQL 15 和 16 上，`spock_failover_slots` 后台工作进程定期从主库复制槽状态。该进程在每个节点上注册，但仅在服务器处于恢复状态时执行这项工作；在主库上保持空闲。

### 要求 {#requirements}

- 备库设置 `hot_standby_feedback = on`（工作进程开始任何同步前的必要条件）
- 备库必须能够连接主库

### 配置参数 {#configuration-gucs}

| GUC | 默认值 | 说明 |
|---|---|---|
| `spock.synchronize_slot_names` | `name_like:%%` | 要同步的槽名模式（默认全部） |
| `spock.drop_extra_slots` | `on` | 删除不匹配模式的备库槽 |
| `spock.primary_dsn` | `''` | 连接主库的 DSN（为空时使用 `primary_conninfo`） |
| `spock.pg_standby_slot_names` | `''` | 逻辑复制前进前必须确认 LSN 的物理槽 |
| `spock.standby_slots_min_confirmed` | `-1` | `pg_standby_slot_names` 中必须确认的槽数（`-1` 表示全部） |
| `spock.failover_slots_naptime` | `1000` | 两轮槽同步之间工作进程的休眠时间，单位毫秒（SIGHUP；范围 1–3600000） |
| `spock.failover_slots_feedback_naptime` | `10000` | 等待备库 WAL 反馈时采用的较短重试间隔，单位毫秒（SIGHUP；范围 1–3600000） |
| `spock.failover_slots_recreate_invalidated` | `on` | 当备库上的同步槽副本失效时，删除并重建该槽；`off` 保持原状并报告一次。仅用于 PG15–17；PG17 使用原生槽同步时及 PG18+ 均忽略（SIGHUP） |
| `spock.failover_slots_database` | `''` | 工作进程连接的数据库，以便在备库上解码每个副本并为其建立一致快照；默认关闭。仅用于 PG16–17，PG18+ 忽略；PG16 上为槽所属的数据库（需要重启） |
{.wide .expand}

### 示例（备库的 `postgresql.conf`） {#example-postgresqlconf-on-standby}

```ini
hot_standby_feedback = on
spock.synchronize_slot_names = 'name_like:%%'
spock.drop_extra_slots = on

# Optional: hold walsenders on primary until this standby confirms
# (set this on the PRIMARY, not the standby)
# spock.pg_standby_slot_names = 'physical_slot_name'
```

## 将 Spock 升级到 6.0.0 {#upgrading-spock-to-600}

Spock 6.0.0 新建的槽已具有 `failover = true`。旧版 Spock 创建的槽没有该标志，PostgreSQL 17 和 18 的原生槽同步会忽略它们。升级会为这些现有槽开启该标志。

本节只涵盖升级中与故障切换相关的部分。完整流程（禁用自动 DDL、安装新二进制文件、逐个重启节点）请先按[升级 Spock 扩展](/pgedge/spock/upgrading/)执行。以下步骤在安装 6.0.0 二进制文件后进行。

### 1. 执行扩展更新 {#1-run-the-extension-update}

```sql
ALTER EXTENSION spock UPDATE TO '6.0.0';
```

PostgreSQL 沿版本链（5.0.8 → 5.0.9 → 5.0.10 → 5.0.11 → 5.0.12 → 5.0.13 → 5.0.14 → 6.0.0）依次执行每一步。5.0.14 到 6.0.0 的步骤会自动调用 `spock.slot_enable_failover()`。

`spock.slot_enable_failover()` 的行为如下：

- PostgreSQL 16 及更早版本没有此标志，因此不执行任何操作。
- 在备库上不执行任何操作，因为该标志只能在主库设置。
- 为尚无此标志的每个 Spock 逻辑槽设置 `failover = true`。
- 跳过当时正在使用的槽，并输出含槽名称的 NOTICE。
- 返回修改的槽数。

### 2. 处理被跳过的槽 {#2-handle-any-skipped-slots}

正在向订阅者发送数据流的槽处于占用状态，无法修改，因此函数会跳过并告知其名称。要为这些槽设置标志，请暂停占用它们的订阅者，然后在主库再次运行该函数：

```sql
SELECT spock.slot_enable_failover();
```

### 3. 验证 {#3-verify}

主库上每个 Spock 槽的 `failover` 现在都应为 true：

```sql
SELECT slot_name, failover
FROM pg_replication_slots
WHERE plugin = 'spock_output';
```

升级不会修改任何 PostgreSQL 设置。在 PostgreSQL 18 上，需要自行按[配置：PostgreSQL 17 和 18（原生机制）](#setup-postgresql-17-and-18-native)配置备库原生槽同步：`sync_replication_slots = on`、在 `primary_conninfo` 中指定 `dbname`，并在主库的 `synchronized_standby_slots` 中列出物理槽。将 PostgreSQL 17 备库切换到原生路径时，请按[将 PostgreSQL 17 备库从 Spock 工作进程切换到原生机制](#switching-a-postgresql-17-standby-from-the-spock-worker)执行。

## 监控 {#monitoring}

### 检查槽同步状态（PG17+） {#check-slot-sync-status-pg17}

```sql
SELECT slot_name,
       failover,
       synced,
       active,
       invalidation_reason,
       confirmed_flush_lsn
FROM pg_replication_slots
WHERE NOT temporary
ORDER BY slot_name;
```

### 检查原生 slotsync 工作进程是否活动（PG17+） {#check-if-native-slotsync-worker-is-active-pg17}

```sql
SELECT pid, wait_event_type, wait_event, state
FROM pg_stat_activity
WHERE backend_type = 'slot sync worker';
```

### 检查 Spock 工作进程是否运行（PG15/16） {#check-spock-worker-is-running-pg1516}

```sql
SELECT pid, application_name, state
FROM pg_stat_activity
WHERE application_name = 'spock_failover_slots worker';
```

主库上也有这条记录，因为工作进程在那里常驻但空闲。因此查询命中只证明已注册该进程，不代表正在同步槽。请在备库上将 `confirmed_flush_lsn` 与主库比较，确认实际同步，并在备库日志中查找 `slot synchronization from primary now active` 消息。

## 常见问题 {#faq}

**问：故障切换后需要做什么？**

PG17+：更新订阅者 DSN 中的 `host=`；如果被提升的节点设置了 `synchronized_standby_slots`，还需按[上面的操作手册](#runbook-clear-synchronized_standby_slots-after-promotion)清空或调整。无需重建槽。

PG15/16：备库（现为主库）上的 Spock 工作进程停止同步槽，因为服务器不再处于恢复状态。工作进程本身仍然存在并保持空闲，继续占用其 `max_worker_processes` 槽位。订阅者会自动重连。

**问：PG18 上不配置 `sync_replication_slots` 会怎样？**

Spock 不在 PG18 上注册自己的工作进程。如果未设置 `sync_replication_slots = on`，逻辑槽**不会**同步到备库；故障切换后就需要手动重建槽并重新同步表。

**问：PG17 上能同时使用两种机制吗？**

不能。PG17 上设置 `sync_replication_slots = on` 后，Spock 工作进程会检测到它并跳过自身同步循环，完全交由原生工作进程处理。如果备库此前由 Spock 工作进程同步，请按[将 PostgreSQL 17 备库从 Spock 工作进程切换到原生机制](#switching-a-postgresql-17-standby-from-the-spock-worker)操作。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/logical_slot_failover.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/pgedge/about/license/)。
