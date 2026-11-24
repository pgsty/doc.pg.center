---
title: "Spock 故障排查"
description: "本页介绍使用 Spock 进行 PostgreSQL 逻辑复制时的常见问题及处理方法。"
weight: 120
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/troubleshooting.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: "故障排查"
type: docs
translation_notice: en
translation_status: translated
---



本页介绍使用 Spock 进行 PostgreSQL 逻辑复制时的常见问题及处理方法。

## 先查看状态视图 {#start-with-the-status-views}

查服务器日志前，先查询[状态视图](/zh/pgedge/spock/monitoring/node-monitoring/)。各视图保留应用工作进程最近一次错误及节点近期事件。

```sql
SELECT * FROM spock.node_status;
SELECT subscription_name, status, worker_status, last_error_message
  FROM spock.subscription_status;
SELECT event_time, event_type, severity, detail
  FROM spock.events WHERE severity <> 'info' ORDER BY event_id DESC LIMIT 20;
```

## 常见复制问题 {#common-replication-issues}

以下问题会妨碍复制正常运行，可按对应方法排查。

### 复制未启动 {#replication-not-starting}

如果复制未能启动，请检查以下项目。

- 确认 `pg_hba.conf` 中的规则允许节点之间安全连接。
- 用以下命令测试节点间的网络连通性。

  ```bash
  psql -h <remote_node_ip> -U postgres -d <database_name>
  ```

- 用以下命令查看 PostgreSQL 日志中的详细错误。

  ```bash
  tail -f /var/lib/pgsql/18/data/log/postgresql-*.log
  ```

- 用以下查询确认两个节点均已创建 Spock 扩展。

  ```sql
  SELECT extname, extversion FROM pg_extension WHERE extname = 'spock';
  ```

### 订阅一直处于初始化状态 {#subscription-stuck-in-initializing-state}

如果订阅长期停在初始化状态，请检查下列配置参数。

- 确认 `max_replication_slots` 足够大。

  ```sql
  SHOW max_replication_slots;
  ```

  正在初始化的订阅在提供方需要*两个*槽，一个供应用流使用，另一个供复制表数据的同步工作进程使用。订阅按数据库建立，因此每个节点按 `2 x subscribers x replicated databases` 计算，并另计物理槽或故障切换槽。PostgreSQL 15 至 17 中，此参数也限制复制来源数。

- 确认 `max_wal_senders` 足够大。

  ```sql
  SHOW max_wal_senders;
  ```

  可将其设为与 `max_replication_slots` 相同的值：每个槽在传输期间都需要一个 walsender，因此沿用上述计算。如果集群平时复制正常，却无法新增或重新同步表，walsender 数不足是最常见的原因。

- PostgreSQL 18 及以上版本还需检查 `max_active_replication_origins`。

  ```sql
  SHOW max_active_replication_origins;
  ```

  该值至少应覆盖本节点应用的订阅数，并预留余量。在全互联拓扑中，订阅数为 `(nodes - 1) x replicated databases`。

- 如修改了需要重启的参数，使用下列命令重启 PostgreSQL。

  ```bash
  sudo systemctl restart postgresql-18
  ```

- 用下列查询检查订阅状态。

  ```sql
  SELECT * FROM spock.sub_show_status();
  ```

### DDL 未复制 {#ddl-not-replicating}

若节点间未复制 DDL，请检查以下设置。

- 使用下列查询确认已启用自动 DDL 复制。

  ```sql
  SHOW spock.enable_ddl_replication;
  ```

  预期值为 `on`。

- 检查 `include_ddl_repset` 是否已启用。

  ```sql
  SHOW spock.include_ddl_repset;
  ```

- 启用自动 DDL 之前，应确认两个节点的模式结构一致。
- 若需要复制函数中执行的 DDL，确认已启用下列设置。

  ```sql
  SHOW spock.allow_ddl_from_functions;
  ```


> [!WARNING]
>
> 有些 DDL 本来就不复制，例如 `CREATE DATABASE`。执行 `CREATE TABLE...AS...` 时会收到警告 "DDL statement replicated, but could be unsafe."
>

### UPDATE 或 DELETE 失败 {#update-or-delete-operations-fail}

若 `UPDATE` 或 `DELETE` 报 *unable to find tuple*，表可能缺少主键或复制标识。

可采用下列一种方式处理。

- 使用下列命令为表添加主键。

  ```sql
  ALTER TABLE table_name ADD PRIMARY KEY (column_name);
  ```

- 也可以使用唯一索引作为复制标识。

  ```sql
  ALTER TABLE table_name REPLICA IDENTITY USING INDEX index_name;
  ```

唯一索引须为非部分索引、不可延迟，所用列均满足 `NOT NULL`。


> [!NOTE]
>
> `REPLICA IDENTITY FULL` 仅支持在具有主键的表上配合增量应用列使用。
>

### 唯一约束冲突 {#unique-constraint-conflicts}

若复制期间报告唯一约束违例，请检查下游表是否只有一个 `UNIQUE` 索引或约束。

可延迟索引约束的报错示例如下。

```text
ERROR: spock doesn't support index rechecks needed for deferrable indexes
DETAIL: relation "public"."test_relation" has deferrable indexes: "index1"
```

可将可延迟约束改为不可延迟约束。

```sql
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
ALTER TABLE table_name ADD CONSTRAINT constraint_name UNIQUE (column_name);
```

### 增量应用列错误 {#delta-apply-column-errors}

若报 *delta apply column can't operate NULL values*，请确保所有增量应用列均有 NOT NULL 约束。

```sql
ALTER TABLE table_name ALTER COLUMN column_name SET NOT NULL;
```

再用下列命令配置增量应用列。

```sql
ALTER TABLE table_name ALTER COLUMN column_name
  SET (log_old_value=true, delta_apply_function=spock.delta_apply);
```

## 配置问题 {#configuration-issues}

PostgreSQL 或 Spock 的以下参数设置可能导致复制问题。

### 缺少必需参数 {#missing-required-parameters}

请在 `postgresql.conf` 中按需配置 Spock 运行所需的下列参数。

```sql
wal_level = logical
max_worker_processes = 20
max_replication_slots = 10
max_wal_senders = 10
shared_preload_libraries = 'spock'
track_commit_timestamp = on
```

示例中的三个数值仅作为小集群的起点。若工作进程注册失败、订阅停滞或应用进程无法启动，应按实际拓扑计算，见 [Spock 的 PostgreSQL 资源规划](/zh/pgedge/spock/sizing/)。教程默认值没有计入与复制共享 `max_worker_processes` 的并行查询进程，也没有计入每库一个的管理进程、监督进程及槽同步工作进程。

修改 `postgresql.conf` 后，按以下命令重启 PostgreSQL。

```bash
sudo systemctl restart postgresql-18
```

### `spock_output` 解码失败 {#decoding-fails-on-spock_output}

新订阅始终无法完成初始化，或既有订阅在小版本升级后停止应用，同时提供方的日志中出现：

```
ERROR:  library "spock_output" may not be used as an output plugin
HINT:   If it is safe for all REPLICATION users to use this library as an
        output plugin, add it to "output_plugin_libraries" and reload the
        server configuration.
```

2026 年的 PostgreSQL 安全修复（CVE-2026-6471，已回补到所有受支持主版本）增加了 `output_plugin_libraries`。只有列入该参数的库才能作为输出插件使用。默认值 `'pgoutput, test_decoding'` 不含 `spock_output`。

每次开始逻辑解码都会检查允许列表，所以既有订阅也受影响。即使集群已正常运行数月，升级后 walsender 首次开始解码时仍可能停止。在**每个**可能被订阅连接的节点上保留核心默认项并加上这个插件；在全互联集群中即所有节点。

```sql
output_plugin_libraries = 'pgoutput, test_decoding, spock_output'
```

持有已同步故障切换槽的物理备库和 Patroni 副本也应配置。复制过去的槽仍使用 `spock_output`；若备库缺少该设置，提升后将无法提供相应的逻辑复制。

参数属于 `PGC_SUSET`，执行 `SELECT pg_reload_conf();` 即可重载。订阅方的应用工作进程将此错误视为连接中断。提供方重载后会自动重连，订阅不会被禁用。

应先确认服务器有这个参数。修复之前的版本会因 `postgresql.conf` 中出现未识别的参数而无法启动。可以这样检查：

```sql
SELECT current_setting('output_plugin_libraries', true);
```

结果为 NULL，表示此版本没有该参数，不应设置。

### 冲突处理问题 {#conflict-resolution-issues}

若冲突导致复制停止，用以下查询检查冲突处理设置。

```sql
SHOW spock.conflict_resolution;
```

唯一受支持的值如下。

- `last_update_wins`：保留提交时间戳最新的版本。

可用以下命令修改设置。

```sql
ALTER SYSTEM SET spock.conflict_resolution = 'last_update_wins';
SELECT pg_reload_conf();
```


> [!NOTE]
>
> `last_update_wins` 要求 `track_commit_timestamp = on`。
>

### 异常处理行为 {#exception-handling-behavior}

若复制因错误停止，可用以下查询查看异常处理设置。

```sql
SHOW spock.exception_behaviour;
```

可选值如下。

- `transdiscard`：发生 ERROR 时丢弃整个事务。
- `discard`：跳过引发 ERROR 的语句，继续处理。
- `sub_disable`：禁用订阅，将事务排队等待。

可用以下命令修改设置。

```sql
ALTER SYSTEM SET spock.exception_behaviour = 'discard';
SELECT pg_reload_conf();
```

用以下查询查看异常日志表的详细记录。

```sql
SELECT * FROM spock.exception_log ORDER BY timestamp DESC LIMIT 10;
```

## 性能问题 {#performance-issues}

以下因素可能影响复制速度和效率。

### 复制延迟过高 {#high-replication-lag}

若延迟持续增长，使用下列查询检查进度。

```sql
SELECT subscription_name, provider_node, replication_lag_bytes,
       replication_lag, worker_status
  FROM spock.subscription_status;
```

该查询按订阅显示 `replication_lag_bytes` 和 `replication_lag`，`spock.lag_tracker` 则按节点对列出相同指标。在提供方，`spock.slot_status` 中的 `pending_wal_bytes` 显示各订阅方尚需取得的 WAL 量。

可能原因及处理方法如下。

- `max_worker_processes` 不足：提高该值，计算方法见 [Spock 的 PostgreSQL 资源规划](/zh/pgedge/spock/sizing/)。并行查询与应用工作进程共享同一资源池，因此即使上限看似宽裕，繁重的并行查询也可能耗尽槽位。应用进程启动前，监督进程、各数据库的管理进程和槽同步工作进程也已分别占用槽位。
- 网络带宽有限：检查实际吞吐量。
- 事务过大：可行时拆为较小的事务。
- 订阅方硬件较慢：升级硬件或降低负载。

## 节点故障与恢复 {#node-failure-and-recovery}

以下说明如何在节点不可用后恢复数据并重新建立复制。

### 灾难性节点故障 {#catastrophic-node-failure}

若节点发生灾难性故障，使用 ACE（Active Consistency Engine）恢复缺失的数据。

恢复分为五个阶段。

1. 检查幸存节点上的订阅状态，评估影响。

2. 删除与故障节点相关的订阅，清理 Spock 元数据。

   ```sql
   SELECT spock.sub_drop(subscription_name := 'sub_to_failed_node');
   SELECT spock.node_drop(node_name := 'failed_node');
   ```

3. 用 ACE table-diff 配合以下选项找出缺失数据。

   ```bash
   ./ace table-diff --nodes n2,n3,n4 --preserve-origin n1 \
     --until 2026-02-11T14:30:00Z --output json cluster public.table_name
   ```

4. 使用 ACE table-repair 修复受影响的表。

   ```bash
   ./ace table-repair --diff-file=diff_file.json \
     --nodes n2,n3,n4 --recovery-mode --source-of-truth n3 \
     --preserve-origin cluster public.table_name
   ```

5. 最后去掉限定选项，重新运行 table-diff，确认完整表数据一致。


> [!WARNING]
>
> 恢复时应始终使用 `--preserve-origin` 保留复制元数据。否则修复行会获得错误的来源 ID 和新的时间戳，可能引发冲突。
>

### 订阅处于 down 状态 {#subscription-down-status}

若订阅显示 `down`，请检查以下项目。

- 读取应用工作进程最近一次错误及订阅的近期事件。

  ```sql
  SELECT worker_status, worker_terminated_at, last_error_message
    FROM spock.subscription_status WHERE subscription_name = 'sub_name';
  SELECT event_time, event_type, detail FROM spock.events
   WHERE subscription_name = 'sub_name' ORDER BY event_id DESC LIMIT 20;
  ```

  `worker_status` 为 `restart pending` 表示工作进程已失败，管理进程将在 `worker_restart_delay` 毫秒后重试。
- 确认提供方节点正在运行且可访问。
- 执行下列查询检查提供方的复制槽。

  ```sql
  SELECT slot_name, active, retained_wal_bytes FROM spock.slot_status;
  ```

- 若视图仍不足以解释故障，请检查提供方和订阅方的 PostgreSQL 日志。
- 使用以下命令重新启动订阅。

  ```sql
  SELECT spock.sub_disable(subscription_name := 'sub_name');
  SELECT spock.sub_enable(subscription_name := 'sub_name');
  ```

## 升级问题 {#upgrade-issues}

升级 Spock 后，可按以下步骤核实安装情况并排查问题。

### 升级后验证 {#post-upgrade-verification}

完成升级后执行以下检查。

1. 确认扩展版本与安装的共享库一致，并检查是否记录了升级事件。

   ```sql
   SELECT spock_version, extension_version, extension_update_pending
     FROM spock.node_status;
   SELECT event_time, detail FROM spock.events
    WHERE event_type = 'extension_upgraded';
   ```

2. 用下列查询验证订阅状态。

   ```sql
   SELECT subscription_name, enabled, status, worker_status
     FROM spock.subscription_status;
   ```

3. 在各提供方上检查复制槽。

   ```sql
   SELECT slot_name, active, state, retained_wal_bytes FROM spock.slot_status;
   ```

4. 用下列查询监控复制延迟。

   ```sql
   SELECT subscription_name, replication_lag_bytes, replication_lag
     FROM spock.subscription_status;
   ```

### 升级后的 DDL 复制 {#ddl-replication-after-upgrade}

如果为升级而禁用了 DDL 复制，完成升级后用以下命令在所有节点重新启用。

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = on;
SELECT pg_reload_conf();
```

## 特定功能问题 {#special-feature-issues}

以下涉及行过滤、列过滤和分区表等功能。

### 行过滤错误 {#row-filter-errors}

若行过滤导致复制停止，请检查表达式所用函数的易变性。

`random()` 属于 `VOLATILE`，多次调用可能得到不同结果。`now()` 属于 `STABLE`，在同一事务中稳定，跨事务可能不同。应检查过滤条件的实际求值时机。

可将易变函数改为适合业务语义的稳定或不可变函数，或从过滤条件中移除它。

### 列过滤问题 {#column-filter-issues}

过滤后若缺少列，请留意以下行为。

- 系统列（如 `oid`、`xmin`）不能用于列过滤。
- 参与过滤的列被删除时，也会自动从过滤列表移除。
- 新列不会自动加入已有的过滤列表。

使用下列命令更新过滤列表，将新列纳入其中。

```sql
SELECT spock.repset_alter_table(
    set_name := 'default',
    relation := 'public.table_name',
    columns := ARRAY['col1', 'col2', 'new_col']
);
```

### 分区表复制 {#partitioned-table-replication}

若新增分区未参与复制，可使用下列命令手动添加。

```sql
SELECT spock.repset_add_partition(
    parent := 'public.parent_table',
    partition := 'public.new_partition'
);
```

初始同步会同步父表，但同步之后创建的新分区需要显式添加。传入 `partition := NULL` 或省略该参数，可一次加入父表的所有现有分区。也可提供可选的 `row_filter`，限制从分区复制哪些行。


## 查看日志 {#checking-logs}

多数复制错误在视图中即可看到。各应用工作进程最近一次错误位于 `spock.subscription_status.last_error_message`；Spock 工作进程产生的错误会以 `worker_error` 事件记录在 `spock.events` 中。

视图中未必包含所有错误。连接失败和 PANIC 不在其中；事件缓冲区短暂被锁时，记录方会放弃写入该事件。要查看出错语句和详细上下文，或排查视图未说明原因的工作进程故障，仍需查看服务器日志。

PostgreSQL 日志提供复制错误和问题的详细信息。

用下列查询定位日志文件。

```sql
SHOW log_directory;
SHOW log_filename;
```

在 RHEL 或 Rocky Linux 上，日志通常位于以下位置。

```text
/var/lib/pgsql/18/data/log/
```

用下列命令实时跟踪日志。

```bash
tail -f /var/lib/pgsql/18/data/log/postgresql-*.log
```

使用下列命令筛选 Spock 相关消息。

```bash
grep -i spock /var/lib/pgsql/18/data/log/postgresql-*.log
```

## 寻求帮助 {#getting-help}

若以上方法未能解决问题，联系支持人员前请收集以下信息。

- Spock 版本，可用 `SELECT extversion FROM pg_extension WHERE extname = 'spock';` 查询。
- PostgreSQL 版本，可用 `SELECT version();` 查询。
- 操作系统及版本。
- `postgresql.conf` 中的配置。
- PostgreSQL 日志中的相关错误。
- 订阅状态，可用 `SELECT * FROM spock.sub_show_status();` 查询。
- 节点状态，可用 `SELECT * FROM spock.node;` 查询。
- 复制延迟，可用 `SELECT * FROM spock.lag_tracker;` 查询。

更多资料见以下各页。

- [Spock 函数参考](/zh/pgedge/spock/reference/) 详细说明各函数。
- [配置 Spock](/zh/pgedge/spock/configuration/) 介绍配置参数及其设置。
- [限制与约束](/zh/pgedge/spock/limitations/) 说明可能影响复制部署的已知限制。
- [常见问题](/zh/pgedge/spock/faq/) 解答常见的使用问题。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/troubleshooting.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
