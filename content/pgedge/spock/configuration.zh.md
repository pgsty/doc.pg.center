---
title: 配置 Spock
description: 配置 Spock 所需的 PostgreSQL 参数、高级选项、连接设置和逻辑槽故障转移行为。
weight: 60
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/configuring.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 参数配置
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



在 Spock 复制场景中的每个节点上，创建 Spock 扩展之前，请在 `postgresql.conf` 中添加以下设置：

```sql
wal_level = 'logical'
max_worker_processes = 20   # supervisor + slot sync worker + one per
                            # database + one per subscription + sync workers,
                            # and shared with parallel query - see the
                            # sizing guide
max_replication_slots = 10  # two per subscriber, per replicated database,
                            # plus one per physical standby; 10 covers a
                            # four-node mesh replicating one database
max_wal_senders = 10        # keep equal to max_replication_slots
shared_preload_libraries = 'spock'
track_commit_timestamp = on # needed for conflict resolution
output_plugin_libraries = 'pgoutput, test_decoding, spock_output'
                            # only on servers that have this parameter; see below
```

这些值适合复制单个数据库的两节点或三节点小集群。订阅，以及随之而来的工作进程、walsender 和槽，随节点数*乘以*被复制数据库数扩展；因此复制多个数据库的实例需要按比例增加每项资源。对于更大的集群，或承载多个数据库或其他使用后台工作进程扩展的实例，请使用[为 Spock 规划 PostgreSQL 资源规模](/zh/pgedge/spock/sizing/)中的公式确定每个参数。修改这三个参数都需要重启服务器。


> [!WARNING] `output_plugin_libraries`
>
> 2026 年的一项 PostgreSQL 安全修复（CVE-2026-6471，已回补到每个受支持主版本）添加了 `output_plugin_libraries` 参数；此后，除非库列在该参数中，否则不能再作为输出插件使用。其默认值 `'pgoutput, test_decoding'` 不包含 `spock_output`，因此在这样的服务器上，逻辑解码会失败并给出：
>
> ```
> ERROR:  library "spock_output" may not be used as an output plugin
> ```
>
> 该检查在每次解码启动时运行，而不只是在创建槽时运行；因此，次要版本升级后，已建立的集群也会停止复制。请在每个节点上把 `spock_output` 加入列表，并像上面所示保留核心默认值——包括备库，因为备库提升后需要它。
>
> 只有服务器存在该参数时才设置它。在早于该修复的 PostgreSQL 版本上，`postgresql.conf` 中出现无法识别的参数会导致服务器完全无法启动。要检查已启动的服务器，请运行：
>
> ```sql
> SELECT current_setting('output_plugin_libraries', true);
> ```
>
> 结果为 NULL 表示该参数不存在，不能设置。在没有服务器运行时，也可以询问二进制文件：
>
> ```bash
> postgres --describe-config | grep '^output_plugin_libraries'
> ```
>

修改参数并使用你的操作系统对应的重启命令重启 Postgres 服务器后，用 psql 连接并创建 Spock 扩展：

```sql
[pg18]$ sudo -u postgres psql -U postgres -p 5432
psql (18.1)
Type "help" for help.

postgres=# CREATE EXTENSION spock;
CREATE EXTENSION
```

你还需要修改 [`pg_hba.conf` 文件](https://www.postgresql.org/docs/18/auth-pg-hba-conf.html)，允许来自 localhost 以及节点之间的逻辑复制连接。`pg_hba.conf` 把逻辑复制连接视为到提供者数据库的普通连接。

在每个节点上修改 `pg_hba.conf` 文件后，重新加载服务器配置以应用变更（无需重启）：

```sql
SELECT pg_reload_conf();
```


## Spock 高级配置选项 {#advanced-configuration-options-for-spock}

你可以在 psql 命令行中通过 `SET` 语句使用以下配置参数（GUC），或在 Postgres 配置文件（例如 `postgresql.conf`）中使用它们来配置 Spock 安装。

### `spock.allow_ddl_from_functions` {#spockallow_ddl_from_functions}

`spock.allow_ddl_from_functions` 让 Spock 自动复制函数内部调用的 DDL 语句。如果预期这些函数会在每个节点上运行，可以把它设为 `off`。设置为 `off` 时，从函数复制的语句遵循前文为 `include_ddl_repset` 描述的相同规则。如果表具有已定义的主键，它会被加入 `default` 复制集；否则会被加入 `default_insert_only` 复制集。

### `spock.apply_change_logging` {#spockapply_change_logging}

`spock.apply_change_logging` 控制应用工作进程按变更记录 JSON 日志。每个变更在本地成功应用后，会把一个 JSON 对象写入 PostgreSQL 服务器日志（级别为 `LOG`），让操作人员能把重放的变更与其复制源和提交时间戳关联起来。它面向调试和审计；日志量会与应用工作负载成比例增加，因此正常运行时应保持默认值。

可能的取值如下：

- `none`（默认）——不按变更记录日志。
- `key_only`——对每个 `INSERT`/`UPDATE`/`DELETE`，记录操作、带模式限定的表、主键值、复制源和提交时间戳。
- `verbose`——包含以上所有内容，外加每个变更的旧行和新行数据。

在 `key_only` 和 `verbose` 两种模式下，被复制的 DDL 都会记录其 SQL 文本。此选项可以由超级用户通过 `SET` 设置，或通过 `SIGHUP` 机制重新加载（例如 `SELECT pg_reload_conf()`）；不需要重启服务器。

### `spock.channel_counters` {#spockchannel_counters}

`spock.channel_counters` 是布尔值（默认为 `true`），用于启用或禁用 Spock 通道统计信息收集。此选项只能在 postmaster 启动时设置。

### `spock.check_all_uc_indexes` {#spockcheck_all_uc_indexes}


> [!NOTE]
>
> 此特性是实验性的，默认为 `OFF`。使用此特性的风险由你自己承担。
>

在表中已存在满足其所定义唯一约束（而不是主键或复制标识）的行的场景中，此参数增强 `INSERT` 操作期间的冲突解析。

如果此 GUC 为 `enabled`，Spock 会在检查主键或复制标识索引之后继续检查唯一约束索引。只解析一个冲突，使用“最后写入者胜出”逻辑，其中包括主键或复制标识索引。如果发生第二个冲突，且启用了 `spock.save_resolutions`，结果会记录到 `spock.resolutions` 表；否则不会持久化。

支持部分唯一约束，但不支持可为空的唯一约束。不支持可延迟约束；它们会被过滤掉、不进行检查，因此在最终提交期间仍可能导致异常。

唯一约束索引会在主键之后按 OID 顺序检查。因此，唯一约束的解析有可能改变主键值。

不检查、也不处理子表/外键。因此，如果解析唯一约束改变了主键值，你可能无意中创建孤立的外键记录。

### `spock.conflict_resolution` {#spockconflict_resolution}

`spock.conflict_resolution` 为本地数据与传入变更之间检测到的任何冲突设置解析方法。当前 Spock 版本只支持以下值：

- `last_update_wins`（默认）——保留提交时间戳最新的数据版本（可以是本地版本，也可以是远程版本）。

要启用冲突解析，必须启用 `track_commit_timestamp` 设置。

### `spock.deny_all_ddl` {#spockdeny_all_ddl}

`spock.deny_all_ddl` 是布尔值（默认为 `false`），用于启用或禁用在 Spock 配置的集群中执行 DDL 语句。此选项可以在 postmaster 启动时设置、通过 SIGHUP 机制设置，或者如果你是超级用户，也可以通过 SQL 在命令行设置。

### `spock.enable_ddl_replication` {#spockenable_ddl_replication}

`spock.enable_ddl_replication` 通过 `default` 复制集启用 DDL 语句的[自动复制](/zh/pgedge/spock/managing/spock-autoddl/)。

### `spock.exception_behaviour` {#spock-exception_behaviour}

使用此 GUC 指定 Postgres 在事务中遇到 ERROR 时的提交行为：

- `transdiscard`（默认）——把 `spock.exception_behaviour` 设置为 `transdiscard`，指示服务器在该事务中任何操作返回 `ERROR` 时丢弃整个事务。
- `discard`——把 `spock.exception_behaviour` 设置为 `discard`，继续处理（和复制）而不中断服务器使用；服务器会提交任何未返回 `ERROR` 语句的操作（事务的任何部分）。
- `sub_disable`——把 `spock.exception_behaviour` 设置为 `sub_disable`，禁用报告异常的节点上的订阅；被禁用节点的事务会加入写入 WAL 日志文件的队列；启用订阅后，复制会从导致异常的事务开始恢复，随后处理其他排队事务；你可以使用 `spock.sub_alter_skiplsn` 函数跳过导致异常的事务，并从队列中的下一笔事务继续处理。

注意，如果允许事务累积，你为 `spock.exception_behaviour` 选择的值可能导致 WAL 日志非常大。

### `spock.event_history_size` {#spockevent_history_size}

`spock.event_history_size` 设置 `spock.events` 视图在共享内存中保留多少近期事件。历史填满后，每新增一个事件就会丢弃最旧的事件。该参数接受 `16` 到 `1048576` 的值（默认为 `1024`），并且只能在 postmaster 启动时设置。

### `spock.exception_logging` {#spockexception_logging}

使用此 GUC 指定哪些操作或事务会写入异常日志表：

- `all`（默认）——把 `spock.exception_logging` 设置为 `all`，指示服务器把包含一个或多个失败操作的所有事务记录到 `spock.exception_log` 表；注意，只要一个操作失败，此设置会记录该事务中的所有操作。
- `discard`——为每个被丢弃的操作在 `spock.exception_log` 表中添加一行；成功的事务不会记录。
- `none`——指示服务器不把任何操作或事务记录到异常日志表。

### `spock.exception_replay_queue_size`——已弃用 {#spockexception_replay_queue_size---deprecated}

此参数在版本 5.X 之后将不受支持。

当 Spock 遇到复制异常时，它会基于 `spock.exception_behaviour` 的值进入异常处理模式来尝试解决异常。然后，Spock 会把事务写入内存，默认大小上限为 `4MB`，应用工作进程从内存重放该事务。这使绝大多数异常的处理速度和性能大幅提升。内存大小可通过 `spock.exception_replay_queue_size` 配置。

现在，Spock 按 [`spock.exception_behaviour`](#spock-exception_behaviour) 参数的指定运行。

### `spock.extra_connection_options` {#spockextra_connection_options}

你可以在 `postgresql.conf` 文件中使用 `spock.extra_connection_options` 参数，为 Spock 建立的所有连接指定连接选项。这里适合设置自定义 keepalive 选项等。

`spock` 默认启用 TCP keepalive，以确保在上游服务器意外消失时能够察觉。要禁用它，请在 `spock.extra_connection_options` 中添加 `keepalives = 0`。

### `wal_sender_timeout` {#wal_sender_timeout}

对于 Spock 复制，请在 `postgresql.conf` 中为每个节点把 `wal_sender_timeout` 设置为保守值，例如 `5min`（300000ms）：

```ini
wal_sender_timeout = '5min'
```

PostgreSQL 默认值 `60s` 可能导致虚假断开：当订阅者忙于应用大事务而无法及时发送反馈时，就会出现这种情况。更高的值为应用工作进程提供足够余量，同时仍能检测真正死亡的连接。存活检测主要由 TCP keepalive 处理，`spock.apply_idle_timeout` 则提供订阅者侧的额外安全网。

### `spock.apply_idle_timeout` {#spockapply_idle_timeout}

应用工作进程重新连接提供者前的最大空闲时间（秒）。它作为安全网，用于检测保持 TCP 连接存活但停止发送数据的挂起 walsender。收到任何消息都会重置计时器。设置为 `0` 可禁用它，仅依靠 TCP keepalive 进行存活检测。默认值：`300`（5 分钟）。

```ini
spock.apply_idle_timeout = 300
```

### `spock.sync_timeout` {#spocksync_timeout}

覆盖节点管理例程中单次同步等待的预算时间（秒）——等待同步事件到达对端、等待节点追上，或等待订阅开始复制。默认值：`0`，表示每个例程保留自己的内置上限（3 分钟）。只有正值会生效，因此不设置它会保持这些例程一直以来的行为。

在大型数据库上应提高该值。内置上限面向小集群，节点在几秒内加入；当追上操作确实需要几分钟或几小时时，例程会在工作完成前很久就超时失败。也可以只针对单个操作提高它，而不是在整个集群范围内提高：

```sql
SET spock.sync_timeout = '2h';
CALL spock.add_node(...);
```

它限制的是整次等待，而不是对远程节点的单次探测。对于额外限制每次远程探测的例程——使一个无响应的对端无法耗尽全部预算——该目的仍由它们自己小得多的限制控制。

```ini
spock.sync_timeout = 0
```

### `spock.read_retry_count` {#spockread_retry_count}

当远程 `UPDATE` 或 `DELETE` 目标的行尚未可见时，应用工作进程重新读取本地关系的次数。每次重试时，应用工作进程会等待任何正在并发应用的事务完成，然后再次搜索本地关系。如果在配置的重试次数后该行仍缺失，应用工作进程会进入标准的行缺失处理路径（根据配置的 [`spock.exception_behaviour`](#spock-exception_behaviour)，执行冲突解析和/或异常处理）。

设置为 `0` 可完全禁用重试（行缺失路径立即运行）。有效范围是 `0` 到 `100`。默认值：`5`。变更在 `SIGHUP` 时生效（例如 `SELECT pg_reload_conf()`）；不需要重启服务器。

```ini
spock.read_retry_count = 5
```

### 逻辑槽故障转移（HA 备库） {#logical-slot-failover-ha-standby}

Spock 在每个提供者节点上创建逻辑复制槽。对于带物理备库的高可用场景，必须把这些槽同步到备库，才能在故障转移后无数据丢失地恢复复制。

完整设置说明参见[逻辑槽故障转移](/pgedge/spock/logical-slot-failover/)，包括故障转移后在已提升节点上清理 `synchronized_standby_slots` 的操作手册步骤。

行为取决于 PostgreSQL 版本：

| PostgreSQL | 槽同步机制 | Spock 工作进程 |
|---|---|---|
| 15、16 | Spock 内置 `spock_failover_slots` 工作进程 | 在每个节点上运行 |
| 17 | Spock 工作进程或原生 `sync_replication_slots` | 如果启用原生机制，Spock 工作进程让位于它 |
| 18+ | 原生 `sync_replication_slots`（必需） | 不注册 |
{.wide .expand}

无论适用哪种机制，每个节点（包括主库和备库）都有槽同步工作进程，因此请在工作进程预算中计入一个；参见[为 Spock 规划 PostgreSQL 资源规模](/zh/pgedge/spock/sizing/)。

#### PostgreSQL 17 及更高版本（原生槽同步） {#postgresql-17-and-later-native-slot-sync}

在 PostgreSQL 17+ 上，Spock 在创建时为每个逻辑槽标记 `FAILOVER` 标志。PostgreSQL 内置 slotsync 工作进程随后会自动同步这些槽。

在 **PostgreSQL 17** 上，只有设置 `sync_replication_slots = on`（见下文）后，Spock 的工作进程才会让位于原生 slotsync。在 **PostgreSQL 18+** 上，不会注册 Spock 自己的故障转移工作进程，因此原生机制是必需的。无论哪种情况，都必须配置 PostgreSQL 自己的槽同步。要切换一个已由 Spock 工作进程同步的 PostgreSQL 17 备库，请遵循[把 PostgreSQL 17 备库从 Spock 工作进程切换出来](/pgedge/spock/logical-slot-failover/#switching-a-postgresql-17-standby-from-the-spock-worker)；仅设置 `sync_replication_slots = on` 并不够。

首先在主库创建物理复制槽。备库通过它流式传输；备库的 `catalog_xmin`（通过 `hot_standby_feedback` 反馈）正是保护已同步逻辑槽不被失效的关键：

```sql
SELECT pg_create_physical_replication_slot('physical_slot_name');
```

**主库（`postgresql.conf`）：**
```ini
# Hold logical walsenders back until the standby has confirmed the changes.
synchronized_standby_slots = 'physical_slot_name'
```

**备库（`postgresql.conf`）：**
```ini
sync_replication_slots = on                      # enable the native slotsync worker
hot_standby_feedback   = on                      # required; pins the primary's catalog vacuum
primary_slot_name      = 'physical_slot_name'    # the physical slot created above
primary_conninfo       = 'host=<primary_host> dbname=<dbname> ...'   # must include dbname
```

只有以 `failover = true` 创建的逻辑槽会被同步。Spock 6.0.0 创建槽时会设置该标志，从 5.x 升级时也会在现有槽上设置；对于任何未设置的槽，参见[把 Spock 升级到 6.0.0](/pgedge/spock/logical-slot-failover/#upgrading-spock-to-600)。

故障转移后，订阅者只需更新连接字符串中的 `host=`——复制会从最后同步的 LSN 恢复，不丢失数据。**但是**，如果已提升节点设置了 `synchronized_standby_slots`，必须先清理或更新它——否则它的 walsender 会永远等待现已孤立的物理槽，到订阅者的逻辑复制会冻结。何时适用以及确切步骤参见[逻辑槽故障转移中的操作手册](/pgedge/spock/logical-slot-failover/#runbook-clear-synchronized_standby_slots-after-promotion)。

#### PostgreSQL 15、16 和 17（Spock 内置工作进程） {#postgresql-15-16-and-17-spock-built-in-worker}

在 PostgreSQL 15、16 和 17 上，Spock 的 `spock_failover_slots` 后台工作进程处理槽同步。在 PostgreSQL 17 上，当启用 `sync_replication_slots = on` 时，它会退让给原生 slotsync 工作进程。请使用下面的 GUC 配置它。

### `spock.synchronize_slot_names` {#spocksynchronize_slot_names}

要从主库同步到物理备库的槽名模式列表。接受名称前缀（`name:foo`）或 LIKE 模式（`name_like:spock%`）。默认值：`name_like:%%`（同步所有逻辑槽）。

```ini
spock.synchronize_slot_names = 'name_like:%%'
```

用于 PostgreSQL 15、16 和 17（未启用 `sync_replication_slots` 时）。在启用了原生 slotsync 的 PostgreSQL 17 上，或在 PostgreSQL 18+ 上，此设置会被忽略。

### `spock.drop_extra_slots` {#spockdrop_extra_slots}

当为 `on`（默认值）时，`spock_failover_slots` 工作进程会删除备库上与 `spock.synchronize_slot_names` 不匹配的任何槽。

```ini
spock.drop_extra_slots = on
```

### `spock.primary_dsn` {#spockprimary_dsn}

`spock_failover_slots` 工作进程用来连接主库并读取槽状态的连接字符串。如果为空，则使用 `postgresql.conf` 中的 `primary_conninfo`。

```ini
spock.primary_dsn = ''
```

### `spock.pg_standby_slot_names` {#spockpg_standby_slot_names}

必须确认某个给定 LSN 已持久刷新之后，walsender 才能复制超过该 LSN 的逻辑变更的物理复制槽名称逗号分隔列表。这可防止物理备库落后于逻辑订阅者。

```ini
spock.pg_standby_slot_names = 'physical_slot_1,physical_slot_2'
```

在每个受支持的 PostgreSQL 版本上都会使用，无论是否启用原生槽同步。PostgreSQL 自己的 `synchronized_standby_slots` 没有等价于 `spock.standby_slots_min_confirmed` 的设置：它会等待其列出的每个槽；因此只要一个备库停机，它就会停止到每个订阅者的逻辑复制。两者只能使用一个；同时设置是冗余的。对于故障转移槽，`synchronized_standby_slots` 先应用并等待其所有槽；因此当它列出了此处的每个槽时，此设置不会增加任何效果，walsender 会记录这一点；只列在此处的槽仍会生效。列出的槽如果不存在，则永远无法确认：在默认 `-1` 下，walsender 会等待到 `wal_sender_timeout`，记录一个指名该槽的警告，然后重新开始；因此提升后，要么在新主库上创建这些槽，要么在那里清除此设置。

### `spock.standby_slots_min_confirmed` {#spockstandby_slots_min_confirmed}

允许逻辑复制继续之前，`spock.pg_standby_slot_names` 中必须确认给定 LSN 的槽数量。默认 `-1` 要求所有列出的槽确认。`0` 禁用检查。

```ini
spock.standby_slots_min_confirmed = -1
```

如果该值低于列出的槽数量，订阅者可能收到某些备库尚没有的变更。发生故障后，提升 `pg_last_wal_receive_lsn()` 最高的备库：它拥有已发送给订阅者的所有变更。提升更落后的备库会使订阅者拥有新主库从未有过的行。

### `spock.failover_slots_naptime` {#spockfailover_slots_naptime}

`spock_failover_slots` 工作进程在两轮槽同步之间休眠的时长，单位毫秒。更小的值让备库的已同步槽更接近主库——缩小提升时可能遇到过期槽的时间窗——代价是更频繁的同步轮次。默认值：`1000`（1 秒）。范围：`1`–`3600000`。可在运行时通过 `SIGHUP`（重新加载）设置。

```ini
spock.failover_slots_naptime = 1000
```

用于 PostgreSQL 15、16 和 17（未启用 `sync_replication_slots` 时）——即由内置工作进程执行同步的版本。

### `spock.failover_slots_feedback_naptime` {#spockfailover_slots_feedback_naptime}

当备库尚未收到或反馈某个槽所需的 WAL 时，用来替代 `spock.failover_slots_naptime` 的较短重试间隔，单位毫秒。默认值：`10000`（10 秒）。范围：`1`–`3600000`。可在运行时通过 `SIGHUP`（重新加载）设置。

```ini
spock.failover_slots_feedback_naptime = 10000
```

### `spock.failover_slots_recreate_invalidated` {#spockfailover_slots_recreate_invalidated}

当某个已同步槽在备库上的副本被失效时——例如备库删除了 WAL，或主库删除了该副本仍需要的目录行——`spock_failover_slots` 工作进程是否删除并重建该槽。这样的副本看起来是新的，但提升后无法服务订阅者。在默认 `on` 下，工作进程会用 WARNING 报告它，删除它，并从主库重新创建。新副本会保持为临时槽，直到主库的槽追上它；在此期间工作进程会继续同步其他槽；如果备库在此之前提升，该副本会被删除。临时副本属于工作进程：如果工作进程因任何原因退出——例如主库正在重启且无法访问——该副本会随之删除；postmaster 一分钟后启动的工作进程会按当时备库的位置重新创建它，而主库的槽必须再次越过该位置。如果工作进程持有临时副本时该副本被失效，PostgreSQL 会终止工作进程以释放槽，效果相同。设置为 `off` 时，工作进程保留该副本原样并报告一次，使你能在删除任何内容之前查看它；把该设置重新打开后的第一轮同步会重建它。可在运行时通过 `SIGHUP`（重新加载）设置。

用于 PostgreSQL 15、16 和 17（未启用 `sync_replication_slots` 时）。在启用了原生 slotsync 的 PostgreSQL 17 上，或在 PostgreSQL 18+ 上，此设置会被忽略。

```ini
spock.failover_slots_recreate_invalidated = on
```

### `spock.failover_slots_database` {#spockfailover_slots_database}

`spock_failover_slots` 工作进程在备库上连接的数据库。已同步槽副本保存主库的位置，但不保存主库为该槽保存的快照；物理复制不会携带该快照。提升后，从这样的副本解码必须构建新快照，而在快照一致之前提交的事务永远不会发送给订阅者。当此设置指定数据库时，工作进程会在备库上解码每个副本的 WAL，就像 PostgreSQL 17 的原生槽同步那样；因此副本只会指向备库已保存自己快照的位置。只有该快照一致后，新副本才会变为持久槽。当主库上仍有早于副本 `restart_lsn` 的事务打开时，解码无法达到一致快照；该副本会被报告一次并保持原样，直到该事务结束，工作进程会继续处理其他槽。

该检查默认关闭。此设置为空时，每个副本都会像早期版本一样在没有检查的情况下同步，并被报告一次（PostgreSQL 16 和 17 为 WARNING，15 为 LOG 条目）；提升后，这样的副本仍可能跳过旧主库在故障转移前不久提交的事务。

在 PostgreSQL 16 上，它必须是已同步槽所属的数据库，通常是 Spock 数据库。其他数据库中的副本会在没有检查的情况下同步，并用 WARNING 报告一次，带有相同风险。工作进程只连接一个数据库；因此在 PostgreSQL 16 上多个数据库运行 Spock 时，请指定最重要的那个；其他数据库的槽不受保护。在 PostgreSQL 17 上，任一数据库都覆盖每个数据库的槽。备库还需要 `wal_level = logical`。PostgreSQL 15 不能在备库上解码 WAL，因此该检查不可用，每个副本只会在日志中记录一次。默认值：空。需要重启。

在 PostgreSQL 16 和 17 上，只要节点上存在此设置，工作进程就会在每个节点上保持连接到该数据库，包括主库（它否则会休眠）以及使用原生槽同步的 PostgreSQL 17 备库。与任何打开的连接一样，此后的 `DROP DATABASE`、`ALTER DATABASE ... RENAME` 和 `CREATE DATABASE ... TEMPLATE` 在该数据库上会失败。停止工作进程只能释放数据库到它 60 秒后重启为止；请使用 `DROP DATABASE ... WITH (FORCE)`，或清除该设置并重启服务器。如果连接失败（例如数据库不存在），工作进程会报告，继续不进行检查，并且在服务器重启前不会重试。数据库在主库上被删除时也会发生同样情况：在备库重放删除会结束工作进程，重启后的工作进程无法连接该数据库，之后的工作进程会继续在不检查的情况下同步槽。

在 PostgreSQL 16 和 17 上会执行该检查（未启用 `sync_replication_slots` 时）。在启用了原生槽同步的 PostgreSQL 17 上，工作进程仍会连接但不检查。在 PostgreSQL 17 上，推荐使用原生槽同步；它无需此设置就能为每个副本提供一致快照。仅打开 `sync_replication_slots` 不足以完成切换：原生槽同步还有其他要求，并且不会接管 Spock 工作进程创建的副本；因此在那些副本删除之前，大多数或全部槽会停止同步。参见[把 PostgreSQL 17 备库从 Spock 工作进程切换出来](/pgedge/spock/logical-slot-failover/#switching-a-postgresql-17-standby-from-the-spock-worker)。在 PostgreSQL 15 和 18+ 上，此设置会被忽略。

在 PostgreSQL 17 上，一旦工作进程从原生槽同步接管，原生槽同步创建的副本会像其他副本一样同步，但备库不能删除它。如果主库删除该槽，工作进程会保留副本并报告一次；它会在提升后的节点上被删除。

```ini
spock.failover_slots_database = 'pgedge'
```

### `spock.include_ddl_repset` {#spockinclude_ddl_repset}

`spock.include_ddl_repset` 让 Spock 在每个节点上创建表时，自动把表加入复制集。带主键的表会加入 `default` 复制集，不带主键的表会加入 `default_insert_only` 复制集。修改表以添加或删除主键时，会正确调整该表所属的复制集。把表设为 unlogged 会把它从复制中移除。分离分区不会把它从复制中移除。

### `spock.log_origin_change` {#spocklog_origin_change}

`spock.log_origin_change` 表示是否把行复制源的变更记录到 PostgreSQL 日志。行可能由常规 SQL 操作在本地更新，也可能由应用工作进程复制更新。注意，本地变更的行（不是来自复制）的复制源值为 `0`。这与不可用或未知复制源不同：`spock.resolutions.local_origin` 中的 `NULL` 值，或 PostgreSQL 日志中的 `unknown`，表示无法确定复制源元数据——并不表示该变更发生在本地。例如：

```sql
-- Rows resolved from a locally-originated conflict (origin = 0)
SELECT * FROM spock.resolutions WHERE local_origin = 0;

-- Rows where origin metadata was unavailable at resolution time
SELECT * FROM spock.resolutions WHERE local_origin IS NULL;
```

建议使用默认的 `none`，否则条目数量可能变得非常多。其他选项允许监控更新是否发生在预期模式之外。

可能的配置值如下：

- `none`（默认）——不记录任何复制源变更信息。
- `remote_only_differs`——仅当现有行来自一个远程发布者，且被另一个远程发布者修改时，才记录复制源变更。
- `since_sub_creation`——无论发布者修改了之前来自另一个发布者的行，还是在本地更新了它，都记录复制源变更，但只从订阅创建时开始。

### `spock.log_verbosity` {#spocklog_verbosity}

`spock.log_verbosity` 控制 Spock 自身调试日志输出的详细程度。Spock 会发出内部 `DEBUG1`/`DEBUG2` 消息；由于 PostgreSQL 的 `log_min_messages` 通常默认为 `warning`，这些消息通常不可见。全局降低 `log_min_messages` 会显示这些消息，但也会让日志充满无关的 PostgreSQL 调试输出。

此设置改为把 Spock 自身的调试消息*提升*到 `LOG` 级别（在任何正常 `log_min_messages` 设置下都会写入服务器日志），而不修改 `log_min_messages`。该值控制提升多少细节：

- `normal`（默认）——不提升任何内容；Spock 的 `DEBUG1`/`DEBUG2` 消息保持其原生级别（通常不可见）。
- `debug1`——把 Spock 的 `DEBUG1` 消息提升为 `LOG`。
- `debug2`——把 Spock 的 `DEBUG1` 和 `DEBUG2` 消息都提升为 `LOG`。

此选项可以由超级用户通过 `SET` 设置，或通过 `SIGHUP` 机制重新加载（例如 `SELECT pg_reload_conf()`）；不需要重启服务器。

### `spock.non_conflicting_inserts` {#spocknon_conflicting_inserts}

`spock.non_conflicting_inserts` 是布尔值（默认为 `off`），你通过它断言：被复制的 `INSERT` 永远不会与本地已存在的行冲突——例如因为每个节点都从自己的键范围生成键。

正常应用 `INSERT` 需要两项只有可能发生冲突才值得执行的工作：查找冲突的本地行，以及进行推测性插入，让唯一索引报告重复而不是抛出重复错误。此参数为 `on` 时，应用工作进程会跳过这两项，直接插入该行。

不会检查这一断言。如果确实发生冲突，索引会抛出 `duplicate key value violates unique constraint`，事务中止，结果由 [`spock.exception_behaviour`](#spock-exception_behaviour) 决定——该行不会由 `spock.conflict_resolution` 解析，也不会记录到 `spock.resolutions`。除非冲突在设计上不可能发生，而不仅仅是很少发生，否则请保持此参数为 `off`。

此选项只能在 postmaster 启动时设置。

### `spock.save_resolutions` {#spocksave_resolutions}

`spock.save_resolutions` 是布尔值（默认为 `false`），把所有冲突解析记录到 `spock.resolutions` 表。此选项只能在 postmaster 启动时设置。

### `spock.resolutions_retention_days` {#spockresolutions_retention_days}

`spock.resolutions_retention_days` 控制行在 `spock.resolutions` 表中保留多久，之后应用工作进程会自动删除它们。默认值为 `100` 天。设置为 `0` 可完全禁用自动清理；此时行会无限累积，直到手动删除。

此设置在 `pg_reload_conf()` 时生效（无需重启）。

```ini
spock.resolutions_retention_days = 100
```

### `spock.stats_max_entries` {#spockstats_max_entries}

`spock.stats_max_entries` 指定 Spock 通道统计中可存储的最大条目数。此选项只能在 postmaster 启动时设置。该参数接受 `-1` 到 `INT_MAX` 的值（默认为 `-1`）。

### `spock.temp_directory` {#spocktemp_directory}

`spock.temp_directory` 定义写入模式同步所需临时文件的系统路径。该路径必须存在，并且可由运行 Postgres 的用户写入。默认值为 `empty`，表示 Spock 使用基于环境或操作系统设置的默认临时目录。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/configuring.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
