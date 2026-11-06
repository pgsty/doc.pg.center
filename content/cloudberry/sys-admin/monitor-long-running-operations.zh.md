---
title: "监控长时间运行的操作"
description: "Apache Cloudberry 可以在命令执行期间报告 `ANALYZE`、`CLUSTER`、`COPY`、`CREATE INDEX`、`REINDEX` 和 `VACUUM` 命令的进度。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/monitor-long-running-operations.md"
---

Cloudberry 还可以报告正在运行的基础备份（在调用 [`gprecoverseg -F`](/cloudberry/reference/sys-utilities/gprecoverseg/) 时启动）的进度，从而可以监控这些可能长时间运行的操作。

Cloudberry 通过临时系统视图报告命令进度；这些视图只在操作运行期间返回数据。Cloudberry 提供两组进度报告视图：

- `gp_stat_progress_<command>`：显示 Coordinator 和所有 Segment 上正在运行的 `<command>` 调用的进度，每个 Segment 实例一行
- `gp_stat_progress_<command>_summary`：汇总 Coordinator 和所有 Segment 上的 `<command>` 进度，每个正在运行的 `<command>` 调用显示一行

Cloudberry 按阶段报告进度，每个阶段都对应具体命令。例如，`acquiring sample rows` 是 analyze 的进度阶段，`building index` 是创建索引的进度阶段。Cloudberry 会同时报告堆表和 AO/CO 表的进度。对于大多数命令，堆表和 AO/CO 表使用相同的阶段。对于 vacuum 和 cluster 操作，Cloudberry 会在不同阶段报告堆表和 AO/CO 表的进度。

## Analyze 进度报告 {#analyze-progress-reporting}

[`pg_stat_progress_analyze`](/cloudberry/reference/sys-catalogs/sys-views/pg-stat-progress-analyze/) 系统视图报告正在运行的 `ANALYZE` 和 `analyzedb` 操作的进度。该视图为当前正在执行 analyze 操作的每个 Segment 实例显示一行。

对于每个活动的 analyze 操作，`gp_stat_progress_analyze_summary` 视图会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_analyze` 报告的指标。

下表说明如何解释这些视图报告的特定阶段信息：

|阶段|描述|
|-----|-----------|
| `initializing` | 命令正在准备开始扫描堆。此阶段预计会非常短。|
| `acquiring sample rows` | 命令正在扫描 `relid` 指定的表，以获取样本行。|
| `acquiring inherited sample rows` | 命令正在扫描子表，以获取样本行。`child_tables_total`、`child_tables_done` 和 `current_child_table_relid` 列包含此阶段的进度信息。|
| `computing statistics` | 命令正在根据表扫描期间获得的样本行计算统计信息。|
| `computing extended statistics` | 命令正在根据表扫描期间获得的样本行计算扩展统计信息。|
| `finalizing analyze` | 命令正在更新 `pg_class`。此阶段完成后，`ANALYZE` 结束。|

## Cluster 和 VACUUM FULL 进度报告 {#cluster-and-vacuum-full-progress-reporting}

[`pg_stat_progress_cluster`](/cloudberry/reference/sys-catalogs/sys-views/pg-stat-progress-cluster/) 系统视图报告正在运行的 `CLUSTER`、`clusterdb` 和（在堆表上运行的）`VACUUM FULL` 操作的进度。（在堆表上运行的 `VACUUM FULL` 与 `CLUSTER` 类似，Cloudberry 会重写表。）该视图为当前正在执行上述任一命令的每个 Segment 实例显示一行。

对于每个活动的 cluster 或 vacuum full 操作，`gp_stat_progress_cluster_summary` 视图会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_cluster` 报告的指标。

### 堆表 Cluster 阶段 {#heap-table-cluster-phases}

下表说明如何解释这些视图报告的*堆表*特定阶段信息：

|阶段|描述|
|-----|-----------|
| `initializing` | 命令正在准备开始扫描堆。此阶段预计会非常短。|
| `seq scanning heap` | 命令正在使用顺序扫描扫描表。|
| `index scanning heap` | `CLUSTER` 正在使用索引扫描扫描表。|
| `sorting tuples` | `CLUSTER` 正在对元组排序。|
| `writing new heap` | `CLUSTER` 正在写入新的堆。|
| `swapping relation files` | 命令正在将新构建的文件交换到目标位置。|
| `rebuilding index` | 命令正在重建索引。|
| `performing final cleanup` | 命令正在执行最后的清理。此阶段完成后，`CLUSTER` 或 `VACUUM FULL` 结束。|

### AO/CO 表 Cluster 阶段 {#aoco-table-cluster-phases}

下表说明如何解释这些视图报告的*AO/CO 表*特定阶段信息：

|阶段|描述|
|-----|-----------|
| `initializing` | 命令正在准备开始扫描。此阶段预计会非常短。|
| `seq scanning append-optimized` | 命令正在使用顺序扫描扫描 AO/CO 表。|
| `index scanning heap` | `CLUSTER` 正在使用索引扫描扫描表。|
| `sorting tuples` | `CLUSTER` 正在对元组排序。|
| `writing new append-optimized` | `CLUSTER` 正在写入新的 AO/CO 表。|
| `swapping relation files` | 命令正在将新构建的文件交换到目标位置。|
| `performing final cleanup` | 命令正在执行最后的清理。此阶段完成后，`CLUSTER` 或 `VACUUM FULL` 结束。|

## Copy 进度报告 {#copy-progress-reporting}

[`gp_stat_progress_copy`](/cloudberry/reference/sys-catalogs/sys-views/pg-stat-progress-copy/) 系统视图报告正在运行的 `COPY` 操作的进度。该视图为当前正在执行 copy 操作的每个 Segment 实例显示一行。

对于每个活动的 copy 操作，`gp_stat_progress_copy_summary` 会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_copy` 报告的指标。

还可以使用这些视图监控底层使用 `COPY` 的工具的数据移动进度，例如 `gpbackup/gprestore`。

对于 `gp_stat_progress_copy_summary` 视图，Apache Cloudberry 会根据表类型和 `COPY` 操作类型，以不同方式计算 `bytes_processed`、`bytes_total`、`tuples_processed` 和 `tuples_excluded` 列的值。下表列出表类型、`COPY` 操作类型，以及 Apache Cloudberry 用于计算最终值的 `sum()` 或 `average()`：

|表类型|COPY TO|COPY FROM|COPY TO/FROM ON SEGMENT|
|-----|-----------|------|------|
|分布式表|`sum()`|`sum()`|`sum()`|
|复制表|`sum()`|`average()`|`sum()`|

由于 `COPY ... ON SEGMENT` 命令明确对每个 Segment 执行，无论表类型如何，Cloudberry 都使用 `sum()`。

对于复制表的 `COPY TO`，Cloudberry 使用 `sum()`，因为实际复制仅从一个 Segment 发起。

## Create INDEX 进度报告 {#create-index-progress-reporting}

[`pg_stat_progress_create_index`](/cloudberry/reference/sys-catalogs/sys-views/pg-stat-progress-create-index/) 系统视图报告正在运行的 `CREATE INDEX` 和 `REINDEX` 操作的进度。该视图为当前正在执行任一命令的每个 Segment 实例显示一行。

对于每个活动的索引操作，`gp_stat_progress_create_index_summary` 视图会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_create_index` 报告的指标。

下表说明如何解释这些视图报告的特定阶段信息：

|阶段|描述|
|-----|-----------|
| `initializing` | `CREATE INDEX` 或 `REINDEX` 正在准备创建索引。此阶段预计会非常短。|
| `waiting for writers before build` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `building index` | 访问方法专用代码正在构建索引。在此阶段，支持进度报告的访问方法会填充自己的进度数据，子阶段会显示在此列中。通常，`blocks_total` 和 `blocks_done` 会包含进度数据，也可能包含 `tuples_total` 和 `tuples_done`。|
| `waiting for writers before validation` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `index validation: scanning index` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `index validation: sorting tuples` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `index validation: scanning table` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `waiting for old snapshots` | 此阶段不适用；Apache Cloudberry 不支持 `CREATE INDEX CONCURRENTLY` 或 `REINDEX CONCURRENTLY`。|
| `waiting for readers before marking dead` | 此阶段不适用；Apache Cloudberry 不支持 `REINDEX CONCURRENTLY`。|
| `waiting for readers before dropping` | 此阶段不适用；Apache Cloudberry 不支持 `REINDEX CONCURRENTLY`。|

由于不支持并发创建索引或并发重建索引，Apache Cloudberry 会跳过若干阶段。

## Vacuum 进度报告 {#vacuum-progress-reporting}

`pg_stat_progress_vacuum` 系统视图报告 AO/CO 表和堆表上正在运行的 `VACUUM` 和 `vacuumdb` 操作，以及 AO/CO 表上正在运行的 `VACUUM FULL` 操作的进度。该视图为当前正在执行 vacuum 操作的每个 Segment 实例显示一行。

对于每个活动的 vacuum 操作，`gp_stat_progress_vacuum_summary` 视图会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_vacuum` 报告的指标。

普通 `VACUUM` 会原地修改堆表。堆表上的 `VACUUM FULL` 会重写表，方式与 `CLUSTER` 操作相同。有关堆表上 `VACUUM FULL` 的进度报告信息，请参见[Cluster 和 VACUUM FULL 进度报告](#copy-progress-reporting)。

在 Apache Cloudberry 中，AO/CO 表的 vacuum 行为与堆表不同。由于 Cloudberry 存储每个 Segment 文件的逻辑 EOF，因此不需要扫描逻辑 EOF 之后的物理块，Cloudberry 可以截断这些物理块。对于 AO/CO 表，Cloudberry 始终将数据重写到新的 Segment 文件中，以清除死元组，并对 `VACUUM FULL` 和 `VACUUM` 执行相同操作。由于这些差异，Cloudberry 使用不同阶段报告堆表和 AO/CO 表的 vacuum 进度。

### 堆表 Vacuum 阶段 {#heap-table-vacuum-phases}

下表说明如何解释这些视图报告的*堆表*特定阶段信息：

|堆表阶段|描述|
|-----|-----------|
| `initializing` | `VACUUM` 正在准备开始扫描堆。此阶段预计会非常短。|
| `scanning heap` | `VACUUM` 正在扫描堆。如果需要，它会清理并整理页面，并可能执行冻结操作。使用 `heap_blks_scanned` 列监控扫描进度。|
| `vacuuming indexes` | `VACUUM` 正在清理索引。如果表有索引，则每次 vacuum 至少会发生一次，并且发生在堆完全扫描之后。如果 `maintenance_work_mem`（或者在设置了该参数时，对 autovacuum 而言为 `autovacuum_work_mem`）不足以存储发现的死元组数量，则每次 vacuum 可能发生多次。|
| `vacuuming heap` | `VACUUM` 正在清理堆。清理堆不同于扫描堆，会在每次索引清理之后发生。如果 `heap_blks_scanned` 小于 `heap_blks_total`，此阶段完成后系统会返回扫描堆；否则，此阶段完成后会开始清理索引。|
| `cleaning up indexes` | `VACUUM` 正在清理索引。这发生在堆完全扫描，并且索引和堆的所有 vacuum 都完成之后。|
| `truncating heap` | `VACUUM` 正在截断堆，以便将关系末尾的空页归还给操作系统。此操作发生在清理索引之后。|
| `performing final cleanup` | `VACUUM` 正在执行最后的清理。在此阶段，`VACUUM` 会清理空闲空间映射，更新 `pg_class` 中的统计信息，并向统计信息收集器报告统计信息。此阶段完成后，`VACUUM` 操作结束。|

### AO/CO 表 Vacuum 阶段 {#aoco-table-vacuum-phases}

下表说明如何解释这些视图报告的*AO/CO 表*特定阶段信息：

|AO/CO 表阶段|描述|
|-----|-----------|
| `initializing` | `VACUUM` 正在准备开始扫描 AO/CO 表。此阶段预计会非常短。|
| `vacuuming indexes` | 对 AO/CO 表而言，如果关系具有索引并且存在不可见且等待删除的 Segment 文件，`vacuuming indexes` 阶段可能会在 `append-optimized pre-cleanup` 和 `append-optimized post-cleanup` 阶段中作为子阶段发生。|
| `append-optimized pre-cleanup` | `VACUUM` 正在执行 AO/CO 表的预清理；包括回收先前 `VACUUM` 操作产生的、对任何对象都不再可见的 `AWAITING_DROP` Segment，以及将所有活动 Segment 文件截断到其逻辑 EOF。使用 `heap_blks_vacuumed` 和 `index_vacuum_count` 监控进度。|
| `append-optimized compact` | `VACUUM` 正在扫描 Segment 文件并仅将存活元组重写到新的 Segment 文件中，以清理（或“压缩”）AO/CO 表。使用 `heap_blks_scanned` 和 `num_dead_tuples` 监控进度。|
| `append-optimized post-cleanup` | `VACUUM` 正在执行 AO/CO 表的后清理；包括回收“压缩”阶段后不再可见的旧 Segment，以及将所有活动 Segment 文件截断到其逻辑 EOF。使用 `heap_blks_vacuumed` 和 `index_vacuum_count` 监控进度。|

## 基础备份进度报告 {#base-backup-progress-reporting}

[`gp_stat_progress_basebackup`](/cloudberry/reference/sys-catalogs/sys-views/pg-stat-progress-basebackup/) 系统视图报告正在运行的基础备份操作进度，该操作由 `gprecoverseg -F`（全量恢复）执行。该视图为当前正在执行复制命令的每个 Segment 实例显示一行。

对于每个活动的基础备份操作，`gp_stat_progress_basebackup_summary` 视图会在 Apache Cloudberry 集群范围内汇总 `gp_stat_progress_basebackup` 报告的指标。

下表说明如何解释这些视图报告的特定阶段信息：

|阶段|描述|
|-----|-----------|
| `initializing` | WAL 发送进程正在准备开始备份。此阶段预计会非常短。|
| `waiting for checkpoint to finish` | WAL 发送进程正在执行 `pg_backup_start` 以准备执行基础备份，并等待备份开始检查点完成。|
| `estimating backup size` | WAL 发送进程正在估算将作为基础备份流式传输的数据库文件总量。|
| `streaming database files` | WAL 发送进程正在将数据库文件作为基础备份流式传输。|
| `waiting for wal archiving to finish` | WAL 发送进程正在执行 `pg_backup_stop` 以完成备份，并等待基础备份所需的全部 WAL 文件成功归档。此阶段完成后备份结束。|
| `transferring wal files` | WAL 发送进程正在传输备份期间生成的全部 WAL 日志。此阶段可能发生在 `waiting for wal archiving to finish` 阶段之后。此阶段完成后备份结束。|

## 示例：查看实时命令进度 {#example-viewing-real-time-command-progress}

以下示例命令每 0.5 秒显示一次所有正在运行的 `VACUUM` 命令的实时进度：

```sql
host$ cat > viewer.sql << EOF
SELECT * FROM gp_stat_progress_vacuum ORDER BY gp_segment_id;
SELECT * FROM gp_stat_progress_vacuum_summary;
EOF

host$ watch -n 0.5 "psql -af viewer.sql"
```

## 其他注意事项 {#additional-considerations}

请注意 Apache Cloudberry 进度报告相关的以下事项：

- 对于 `CREATE INDEX/REINDEX`、`VACUUM` 和 `CLUSTER` 操作，AO/AOCO 表和堆表的进度阶段及属性解释略有不同。更多信息请参阅各个命令主题。
- 分区表上的 `ANALYZE` 操作的进度视图会显示每个叶分区的进度。Cloudberry 当前不提供所有分区合并后的整体进度度量。
- Cloudberry 不支持对分区表执行 `CLUSTER` 操作。
