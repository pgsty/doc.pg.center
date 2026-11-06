---
title: "更新 Apache Cloudberry 统计信息"
linkTitle: "更新统计信息"
description: "获得良好查询性能最重要的前提，是为表提供准确的统计信息。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/update-stats-using-analyze.md"
---

使用 `ANALYZE` 语句更新统计信息，可以帮助查询规划器生成最优查询计划。分析表时，数据相关信息会存储在系统目录表中。如果这些信息过时，规划器就可能生成低效的计划。

## 查看统计信息是否已更新 {#view-whether-statistics-are-updated}

要查看表的统计信息是否为最新，请使用 `pg_stat_all_tables` 系统视图。`last_analyze` 列显示上次分析该表的时间，`last_autoanalyze` 列显示上次自动分析该表的时间。对表运行 `ANALYZE` 语句时，`last_analyze` 和 `last_autoanalyze` 列会更新。

例如，要查看 `test_analyze` 表的统计信息是否为最新，请运行以下查询：

```sql
SELECT schemaname, relname, last_analyze, last_autoanalyze 
FROM pg_stat_all_tables 
WHERE relname = 'test_analyze';
```

## 有选择地生成统计信息 {#generate-statistics-selectively}

不带参数运行 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/) 会更新数据库中所有表的统计信息。这个过程可能耗时很长，不建议这样做。应在数据变化后有选择地对表运行 `ANALYZE`，或使用 [analyzedb](/cloudberry/reference/sys-utilities/analyzedb/) 工具。

对大型表运行 `ANALYZE` 可能耗时很长。如果无法对超大表的所有列运行 `ANALYZE`，可以使用 `ANALYZE table(column, ...)` 仅为选定列生成统计信息。务必包含连接以及 `WHERE`、`SORT`、`GROUP BY` 或 `HAVING` 子句使用的列。

对于分区表，可以仅对发生变化的分区运行 `ANALYZE`，例如新增分区后。注意，可以对分区表的根分区表或叶子分区（实际存储数据和统计信息的文件）运行 `ANALYZE`。在 Apache Cloudberry 中，对分区表的单个分区运行 `ANALYZE` 也会更新根表的统计信息，这意味着收集一个分区的统计信息可能影响整个分区表的优化器统计信息。可以使用 `pg_partition_tree()` 函数查找叶子分区的名称：

```sql
SELECT * FROM pg_partition_tree( 'parent_table' );
```

## 提高统计信息质量 {#improve-statistics-quality}

生成统计信息所需的时间与统计信息的质量或准确度之间存在权衡。

为了能在合理时间内分析大型表，`ANALYZE` 会对表内容随机采样，而不逐行检查。要增加所有表列的采样值数量，请调整 `default_statistics_target` 配置参数。目标值范围为 `1` 到 `10000`，默认值为 `100`。

`default_statistics_target` 默认适用于所有列，指定最常见值列表中保存的值的数量。较大的目标值可能提高查询规划器估算的质量，特别是对于数据分布不规则的列。

可以使用 `SET default_statistics_target` 语句在会话级设置 `default_statistics_target`。要设置此配置参数的默认值，需要在 `postgresql.conf` 文件中设置并重新加载配置。

## 何时运行 ANALYZE {#when-to-run-analyze}

应在以下情况运行 `ANALYZE`：

- 加载数据后；
- 执行 `CREATE INDEX` 后；
- 执行显著改变底层数据的 `INSERT`、`UPDATE` 和 `DELETE` 后。

`ANALYZE` 只需获取表的读锁，因此可以与其他数据库活动并行运行。但出于性能考虑，不建议在加载数据或执行 `INSERT`、`UPDATE`、`DELETE`、`CREATE INDEX` 时运行 `ANALYZE`。

> [!NOTE]
> Apache Cloudberry 改进了 `ANALYZE` 对分区表的处理方式。显式对叶子分区收集统计信息（例如 `ANALYZE sales_1_prt_p2023`）时，系统不再更新根表或其他分区的统计信息。只有对根表运行 `ANALYZE`（例如 `ANALYZE sales`）时，才会刷新整张表（包括所有子分区）的统计信息。
>
> 这一变化让统计信息维护更加精细，并避免不必要的更新。实际使用时，建议根据数据变化情况，有选择地分析特定分区或整张表。

## 配置自动统计信息收集 {#configure-automatic-statistics-collection}

`gp_autostats_mode` 配置参数与 `gp_autostats_on_change_threshold` 参数共同决定何时触发自动分析。触发自动统计信息收集时，规划器会在查询中加入一个 `ANALYZE` 步骤。

默认情况下，`gp_autostats_mode` 的值为 `none`。将其设为 `on_no_stats` 后，如果表没有现有统计信息，表的所有者对其执行 `CREATE TABLE AS SELECT`、`INSERT` 或 `COPY` 时，就会触发统计信息收集。

将 `gp_autostats_mode` 设为 `on_change` 后，只有受影响的行数超过 `gp_autostats_on_change_threshold` 定义的阈值时，才会触发统计信息收集。该阈值的默认值为 `2147483647`。表的所有者对表执行以下操作时，可以通过 `on_change` 触发自动统计信息收集：`CREATE TABLE AS SELECT`、`UPDATE`、`DELETE`、`INSERT` 和 `COPY`。

将服务器配置参数 `gp_autostats_allow_nonowner` 设为 `true`，也会指示 Apache Cloudberry 在以下情况下对表触发自动统计信息收集：

- `gp_autostats_mode=on_no_stats`，且首次向表中执行 `INSERT` 或 `COPY` 的用户不是表的所有者。

将 `gp_autostats_mode` 设为 `none` 可禁用自动统计信息收集。

对于分区表，如果通过顶层父表插入数据，不会触发自动统计信息收集。但如果直接向分区表的叶子表（数据存储的位置）插入数据，*会*触发自动统计信息收集。
