---
title: "日常系统维护任务"
description: "为了使 Apache Cloudberry 系统高效运行，必须定期清理过期数据并更新表统计信息，使查询优化器拥有准确的信息。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/routine-maintain-tasks.md"
---

Apache Cloudberry 要求定期执行某些任务，以获得最佳性能。这里讨论的任务是必需的，但数据库管理员可以使用 `cron` 脚本等标准 UNIX 工具自动执行这些任务。管理员设置相应脚本，并检查脚本是否成功运行。有关可以实施的其他维护活动，请参见[推荐的监控与维护任务](/cloudberry/sys-admin/recommended-maintenance-monitoring-tasks/)，以使 Cloudberry 系统保持最佳运行状态。

## 常规 Vacuum 和 Analyze {#routine-vacuum-and-analyze}

Apache Cloudberry 使用的 MVCC 事务并发模型意味着，已删除或更新的数据行即使对新事务不可见，仍会占用磁盘上的物理空间。如果数据库包含大量更新和删除操作，就会产生许多过期行，必须使用 `VACUUM` 命令回收它们占用的空间。`VACUUM` 命令还会收集表级统计信息，例如行数和页数，因此即使更新或删除的行没有可回收空间，也必须对追加优化表执行 vacuum。

对追加优化表执行 vacuum 的过程与堆表不同。在每个 Segment 上创建一个新的 Segment 文件，并将可见行从当前 Segment 复制到其中。Segment 文件复制完成后，原文件会被安排删除，新 Segment 文件变为可用。这要求有足够的可用磁盘空间，在原 Segment 文件删除之前保存可见行的副本。

如果某个 Segment 文件中隐藏行与总行数的比率低于阈值（默认值为 10），则不会压缩该 Segment 文件。可以使用服务器配置参数 `gp_appendonly_compaction_threshold` 配置阈值。`VACUUM FULL` 会忽略 `gp_appendonly_compaction_threshold` 的值，无论比率如何都会重写 Segment 文件。

可以使用 *gp_toolkit* 模式中的 `__gp_aovisimap_compaction_info()` 函数，调查对追加优化表执行 VACUUM 操作的效果。

有关 `__gp_aovisimap_compaction_info()` 函数的信息，请参见[检查追加优化表](/cloudberry/reference/sys-catalogs/gp_toolkit/#check-append-optimized-tables)。

可以使用服务器配置参数 `gp_appendonly_compaction` 停用追加优化表的 `VACUUM`。

有关数据库 vacuum 的详细信息，请参见[对数据库执行 Vacuum](/cloudberry/reference/sql-stmts/vacuum/)。

### 事务 ID 管理 {#transaction-id-management}

Cloudberry 的 MVCC 事务语义依赖于比较事务 ID（XID）编号，以确定其他事务是否可见。事务 ID 编号使用模 2³² 算术进行比较，因此运行超过约二十亿个事务的 Cloudberry 系统可能发生事务 ID 回卷，此时过去的事务看起来像发生在未来。这会使过去事务的输出不可见。因此，必须在每执行约二十亿个事务后，至少对每个数据库中的每张表执行一次 `VACUUM`。

Apache Cloudberry 仅向涉及 DDL 或 DML 操作的事务分配 XID，而通常只有这些事务需要 XID。

> [!NOTE]
> Apache Cloudberry 会监控事务 ID。如果不定期对数据库执行 vacuum，Apache Cloudberry 会生成警告和错误。

当事务 ID 的很大一部分不再可用、且事务 ID 回卷即将发生时，Apache Cloudberry 会发出以下警告：

`WARNING: database "database_name" must be vacuumed within *number_of_transactions* transactions`

发出警告时，需要执行 `VACUUM` 操作。如果不执行 `VACUUM` 操作，Apache Cloudberry 在达到事务 ID 回卷发生前的某个限制时会停止创建事务。为避免可能的数据丢失，Apache Cloudberry 在停止创建事务时发出以下错误：

```
FATAL: database is not accepting commands to avoid 
wraparound data loss in database "database_name"
```

Apache Cloudberry 配置参数 `xid_warn_limit` 控制显示警告的时机。参数 `xid_stop_limit` 控制 Apache Cloudberry 停止创建事务的时机。

#### 从事务 ID 限制错误中恢复 {#recover-from-a-transaction-id-limit-error}

由于很少执行 `VACUUM` 维护，Apache Cloudberry 达到 `xid_stop_limit` 事务 ID 限制后会变得无响应。要从这种情况中恢复，数据库管理员应执行以下步骤：

1. 关闭 Apache Cloudberry。
2. 暂时将 `xid_stop_limit` 降低 10,000,000。
3. 启动 Apache Cloudberry。
4. 对所有受影响的数据库运行 `VACUUM FREEZE`。
5. 将 `xid_stop_limit` 重置为原始值。
6. 重启 Apache Cloudberry。

有关事务 ID 回卷的信息，请参见 [PostgreSQL 文档](https://www.postgresql.org/docs/12/index.html)。

### 系统目录维护 {#system-catalog-maintenance}

大量使用 `CREATE` 和 `DROP` 命令更新数据库，会增大系统目录并影响系统性能。例如，大量运行 `DROP TABLE` 语句会导致目录表元数据操作期间扫描过多数据，从而降低整个系统的性能。根据系统情况，性能损失可能在执行数千到数万个 `DROP TABLE` 语句后出现。

应定期执行系统目录维护过程，回收已删除对象占用的空间。如果长时间未执行定期过程，可能需要运行更强的过程来清理系统目录。本节介绍这两种过程。

#### 常规系统目录维护 {#regular-system-catalog-maintenance}

建议定期对系统目录执行 `REINDEX` 和 `VACUUM`，清理已删除对象在系统索引和表中占用的空间。如果常规数据库操作包含大量 `DROP` 语句，可以在非高峰时段每天使用 `VACUUM` 安全且适当地执行系统目录维护过程。系统可以在此期间保持可用。

Apache Cloudberry 系统目录维护步骤如下：

1. 对系统目录表执行 `REINDEX`，重建系统目录索引。这会清除索引膨胀并提高 `VACUUM` 性能。

    > [!NOTE]
    > `REINDEX` 会锁定系统目录表，可能影响当前正在运行的查询。为避免干扰正在进行的业务操作，请在低活动时段安排 `REINDEX` 操作。

2. 对系统目录表执行 `VACUUM`。
3. 对系统目录表执行 `ANALYZE`，更新目录表统计信息。

以下示例脚本对 Apache Cloudberry 系统目录执行 `REINDEX`、`VACUUM` 和 `ANALYZE`。在脚本中，将 `<database-name>` 替换为数据库名称。

```shell
#!/bin/bash
DBNAME="<database-name>"
SYSTABLES="' pg_catalog.' || relname || ';' FROM pg_class a, pg_namespace b 
WHERE a.relnamespace=b.oid AND b.nspname='pg_catalog' AND a.relkind='r'"

reindexdb --system -d $DBNAME
psql -tc "SELECT 'VACUUM' || $SYSTABLES" $DBNAME | psql -a $DBNAME
analyzedb -as pg_catalog -d $DBNAME
```

> [!NOTE]
> 如果在维护时段执行目录维护，并且因时间限制需要停止某个进程，请运行 Apache Cloudberry 函数 `pg_cancel_backend(<PID>)`，安全地停止 Apache Cloudberry 进程。

#### 强化系统目录维护 {#intensive-system-catalog-maintenance}

如果长时间未执行系统目录维护，目录可能因死空间而膨胀，导致简单的元数据操作等待时间过长。例如，在 `psql` 中使用 `\d` 元命令列出用户表时，如果等待时间超过两秒，就表明目录可能发生膨胀。

如果发现系统目录膨胀的迹象，必须在计划的停机时段使用 `VACUUM FULL` 执行强化系统目录维护过程。在此期间，应停止系统上的所有目录活动；`VACUUM FULL` 系统目录维护过程会对系统目录加排他锁。

执行常规系统目录维护过程可以避免需要执行这种成本更高的过程。

强化系统目录维护步骤如下：

1. 停止 Apache Cloudberry 系统上的所有目录活动。
2. 对系统目录表执行 `REINDEX`，重建系统目录索引。这会清除索引膨胀并提高 `VACUUM` 性能。
3. 对系统目录表执行 `VACUUM FULL`。请参见下面的说明。
4. 对系统目录表执行 `ANALYZE`，更新目录表统计信息。

> [!NOTE]
> 系统目录表 `pg_attribute` 通常是最大的目录表。如果 `pg_attribute` 表严重膨胀，对该表执行 `VACUUM FULL` 可能需要很长时间，并且可能需要单独执行。以下两个条件同时存在时，表示 `pg_attribute` 表严重膨胀，`VACUUM FULL` 可能需要很长时间：
>
> - `pg_attribute` 表包含大量记录。
> - `gp_toolkit.gp_bloat_diag` 视图中，`pg_attribute` 的诊断消息为 `significant amount of bloat`。

### 用于查询优化的 Vacuum 和 Analyze {#vacuum-and-analyze-for-query-optimization}

Apache Cloudberry 使用基于成本的查询优化器，该优化器依赖数据库统计信息。准确的统计信息有助于查询优化器更好地估算选择率以及查询操作获取的行数。这些估算值有助于它选择最高效的查询计划。`ANALYZE` 命令收集查询优化器所需的列级统计信息。

可以在同一个命令中同时运行 `VACUUM` 和 `ANALYZE` 操作。例如：

```sql
=# VACUUM ANALYZE mytable;
```

如果对严重膨胀的表运行 VACUUM ANALYZE 命令（大量表磁盘空间被已删除或过时的行占用），可能会产生错误的统计信息。对于大型表，`ANALYZE` 命令会从随机行样本计算统计信息。它通过将样本中每页的平均行数乘以表中的实际页数，估算表中的行数。如果样本包含许多空页，估算的行数可能不准确。

可以在 *gp_toolkit* 视图 *gp_bloat_diag* 中查看表中未使用磁盘空间（已删除或过时的行占用的空间）的信息。如果某张表的 `bdidiag` 列包含值 `significant amount of bloat suspected`，说明表磁盘空间中有大量未使用空间。表执行 vacuum 后，条目会添加到 *gp_bloat_diag* 视图。

要从表中删除未使用的磁盘空间，可以对该表运行 VACUUM FULL 命令。由于表锁要求，可能直到维护时段才能运行 VACUUM FULL。

临时解决方法是运行 ANALYZE 计算列统计信息，然后对表运行 VACUUM 生成准确的行数。以下示例先对 *cust_info* 表运行 ANALYZE，再运行 VACUUM：

```sql
ANALYZE cust_info;
VACUUM cust_info;
```

> [!NOTE]
> - 如果打算在启用 GPORCA（默认）的情况下对分区表运行查询，必须使用 ANALYZE 命令收集根分区表的统计信息。有关 GPORCA 的信息，请参见[GPORCA 概述](/cloudberry/performance/optimize-queries/use-orca/use-orca-overview/)。
>
> - 可以使用 Apache Cloudberry 工具 analyzedb 更新表统计信息。可以并行分析多个表。对于追加优化表，只有统计信息不是最新时，analyzedb 才会更新统计信息。请参见 [`analyzedb`](/cloudberry/reference/sys-utilities/analyzedb/) 工具。

## 常规重建索引 {#routine-reindexing}

对于 B-树索引，新构建的索引访问速度略快于多次更新后的索引，因为新构建索引中逻辑相邻的页通常也在物理上相邻。定期重建旧索引可以提高访问速度。如果一个页上除少数索引键外的大多数索引键都已删除，索引页中就会出现空间浪费。重建索引可以回收这些浪费的空间。在 Apache Cloudberry 中，删除索引（`DROP INDEX`）再重新创建索引（`CREATE INDEX`）通常比使用 `REINDEX` 命令更快。

对于带索引的表列，批量更新或向表中插入数据等操作可能由于索引更新而变慢。要提高带索引表的批量操作性能，可以删除索引，执行批量操作，然后重新创建索引。

## 管理 Apache Cloudberry 日志文件 {#manage-apache-cloudberry-log-files}

- [数据库服务器日志文件](#database-server-log-files)
- [管理工具日志文件](#management-utility-log-files)

### 数据库服务器日志文件 {#database-server-log-files}

Apache Cloudberry 的日志输出通常很多，尤其是在较高调试级别下，不需要永久保存。管理员应定期清理较早的日志文件。

Apache Cloudberry 默认对 Coordinator 和 Segment 数据库日志启用日志轮换。日志文件在 Coordinator 数据目录和每个 Segment 数据目录的 `log` 子目录中创建，命名约定如下：`gpdb-*YYYY*-*MM*-*DD_hhmmss*.csv`。管理员需要实现脚本或程序，定期清理 Coordinator 和每个 Segment 实例的 `log` 目录中的旧日志文件。

日志轮换可以由当前日志文件的大小或当前日志文件的存续时间触发。配置参数 `log_rotation_size` 设置触发日志轮换的单个日志文件大小。当日志文件大小等于或大于指定大小时，文件会关闭，并创建新的日志文件。`log_rotation_size` 的值以千字节为单位指定。默认值为 1048576 千字节，即 1GB。如果将 `log_rotation_size` 设置为 0，则停用基于大小的轮换。

配置参数 `log_rotation_age` 指定触发轮换的日志文件存续时间。当日志文件创建后经过指定时间时，文件会关闭，并创建新的日志文件。默认的 `log_rotation_age` 为 1d，即当前日志文件创建 24 小时后创建新的日志文件。如果将 `log_rotation_age` 设置为 0，则停用基于时间的轮换。

有关查看数据库服务器日志文件的信息，请参见[查看数据库服务器日志文件](/cloudberry/sys-admin/recommended-maintenance-monitoring-tasks/)。

### 管理工具日志文件 {#management-utility-log-files}

Apache Cloudberry 管理工具的日志文件默认写入 `~/gpAdminLogs`。管理日志文件的命名约定为：

```
<script_name>_<date>.log
```

日志条目格式为：

```
<timestamp>:<utility>:<host>:<user>:[INFO|WARN|FATAL]:<message>
```

每次运行某个工具时，该次执行的日志条目都会追加到该工具的每日日志文件中。
