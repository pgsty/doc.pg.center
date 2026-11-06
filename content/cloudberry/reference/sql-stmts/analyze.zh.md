---
title: "ANALYZE"
description: "收集数据库的统计信息。"
weight: 430
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/analyze.md"
---

## 概要 {#synopsis}

```sql
ANALYZE [VERBOSE] [SKIP_LOCKED] [<table> [ (<column> [, ...] ) ]]

ANALYZE [VERBOSE] [SKIP_LOCKED] {<root_partition_table_name>|<leaf_partition_table_name>} [ (<column> [, ...] )] 

ANALYZE [VERBOSE] [SKIP_LOCKED] ROOTPARTITION {ALL | <root_partition_table_name> [ (<column> [, ...] )]}
```

## 描述 {#description}

`ANALYZE` 收集数据库中表内容的统计信息，并将结果存储在系统表 *pg_statistic* 中。随后，Apache Cloudberry 会利用这些统计信息帮助确定查询最高效的执行计划。有关所收集的表统计信息，参见[注解](#notes)。

不带参数时，`ANALYZE` 会收集当前数据库中每个表的统计信息。可以指定表名，只收集单个表的统计信息。也可以指定某个表中的一组列名，此时只收集该表中这些列的统计信息。

`ANALYZE` 不会收集外部表的统计信息。

对于分区表，`ANALYZE` 会在叶子分区上额外收集 HyperLogLog（HLL）统计信息。HLL 统计信息用于推导针对分区表的查询的不同值个数（NDV）。

- 在汇总多个叶子分区的 NDV 估计值时，HLL 统计信息生成的 NDV 估计值比标准表统计信息更准确。
- 更新 HLL 统计信息时，只需要对发生变化的叶子分区执行 `ANALYZE`。例如，叶子分区数据发生变化，或者叶子分区已与另一个表交换时，就需要执行 `ANALYZE`。有关更新分区表统计信息的更多信息，参见[注解](#notes)。

> **重要** 如果打算在启用 GPORCA（默认启用）的情况下对分区表运行查询，则必须使用 `ANALYZE` 或 `ANALYZE ROOTPARTITION` 命令收集该分区表根分区的统计信息。有关收集分区表统计信息以及何时需要 `ROOTPARTITION` 关键字，参见[注解](#notes)。有关 GPORCA 的信息，参见《Apache Cloudberry 管理员指南》中的 GPORCA 概述。

> **注意** 也可以使用 Apache Cloudberry 工具 `analyzedb` 更新表统计信息。`analyzedb` 工具可以并发更新多个表的统计信息，还可以检查表统计信息，并且仅在统计信息已过期或不存在时才进行更新。有关该工具的信息，参见《Apache Cloudberry 工具指南》。

## 参数 {#parameters}

**`{ root_partition_table_name | leaf_partition_table_name } [ (column [, ...] ) ]`**

收集分区表的统计信息，包括 HLL 统计信息。HLL 统计信息仅在叶子分区上收集。

`ANALYZE root_partition_table_name` 会收集所有叶子分区和根分区的统计信息。

`ANALYZE leaf_partition_table_name` 会收集该叶子分区的统计信息。

默认情况下，如果指定了某个叶子分区，并且所有其他叶子分区都已有统计信息，则 `ANALYZE` 会更新根分区的统计信息。如果并非所有叶子分区都有统计信息，`ANALYZE` 会记录没有统计信息的叶子分区的相关信息。有关何时收集根分区统计信息，参见[注解](#notes)。

**`ROOTPARTITION [ALL]`**

仅根据分区表中的数据收集分区表根分区的统计信息。如有可能，`ANALYZE` 会使用叶子分区的统计信息生成根分区统计信息；否则，`ANALYZE` 通过对叶子分区数据采样来收集统计信息。不会收集叶子分区上的统计信息，只对数据进行采样。不会收集 `ALL` 统计信息。

有关何时需要 `ROOTPARTITION` 关键字，参见[注解](#notes)。

指定 `ROOTPARTITION` 时，必须指定 `ALL` 或某个分区表的名称。

如果对 `ROOTPARTITION` 指定 `ALL`，Apache Cloudberry 会收集数据库中所有分区表根分区的统计信息。如果数据库中没有分区表，则返回一条说明没有分区表的消息。对于不是分区表的表，不会收集统计信息。

如果对 `ROOTPARTITION` 指定了表名，而该表不是分区表，则不会收集该表的统计信息，并返回一条警告消息。

`ROOTPARTITION` 子句对 `VACUUM ANALYZE` 无效。命令 `VACUUM ANALYZE ROOTPARTITION` 会返回错误。

如果所有叶子分区都有统计信息，则执行 `ANALYZE ROOTPARTITION` 生成根分区统计信息应当很快（取决于分区数量和表的列数，只需几秒钟）。如果某些叶子分区没有统计信息，则需要对全部表数据采样来生成根分区统计信息。对表数据采样耗时更长，并且得到的根分区统计信息质量较低。

对于分区表 *sales_curr_yr*，以下示例命令仅收集该分区表根分区的统计信息。

**`ANALYZE ROOTPARTITION sales_curr_yr;`**

以下示例 `ANALYZE` 命令收集数据库中所有分区表根分区的统计信息。

```sql
ANALYZE ROOTPARTITION ALL;
```

**`VERBOSE`**

启用进度消息的显示。指定后，`ANALYZE` 会输出以下信息：

- 正在处理的表。
- 为生成样本表而运行的查询。
- 正在计算统计信息的列。
- 为收集单个列的各种统计信息而发出的查询。
- 所收集的统计信息。

**`SKIP_LOCKED`**

指定 `ANALYZE` 在开始处理某个关系时不等待任何冲突锁被释放：如果无法在不等待的情况下立即锁定某个关系，就跳过该关系。注意，即使使用此选项，在打开关系的索引，或者从分区、表继承子表以及某些类型的外表获取样本行时，`ANALYZE` 仍可能被阻塞。另外，`ANALYZE` 通常会处理所指定分区表的所有分区，但如果分区表上存在冲突锁，此选项会使 `ANALYZE` 跳过所有分区。

**`table`**

要分析的特定表的名称（可以带模式限定）。如果省略，则分析当前数据库中的所有普通表（不包括外表）。

**`column`**

要分析的特定列的名称。默认为所有列。

## 注解 {#notes}

外表仅在被显式选中时才会被分析。并非所有外部数据包装器都支持 `ANALYZE`。如果表的包装器不支持 `ANALYZE`，该命令会打印一条警告并且不执行任何操作。

最好定期运行 `ANALYZE`，或者在对表内容做了大量更改之后立即运行。准确的统计信息有助于 Apache Cloudberry 选择最合适的查询计划，从而提高查询处理速度。对于以读为主的数据库，常见的策略是在每天使用量较低的时段运行一次 [VACUUM](/cloudberry/reference/sql-stmts/vacuum/) 和 `ANALYZE`。（如果更新活动频繁，这样做就不够了。）可以使用 `gp_toolkit` 模式中的 `gp_stats_missing` 视图检查缺少统计信息的表：

```sql
SELECT * from gp_toolkit.gp_stats_missing;
```

`ANALYZE` 需要对目标表持有 `SHARE UPDATE EXCLUSIVE` 锁。该锁与以下锁冲突：`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE`、`ACCESS EXCLUSIVE`。

如果对不包含数据的表运行 `ANALYZE`，则不会收集该表的统计信息。例如，如果对一个已有统计信息的表执行 `TRUNCATE` 操作，然后对该表运行 `ANALYZE`，统计信息不会改变。

对于分区表，如果分区表有大量已被分析过的分区，而只有少数叶子分区发生了变化，则指定要分析表的哪一部分（根分区还是子分区，即叶子分区）会很有用。

> **注意** 使用 `CREATE TABLE` 命令创建分区表时，Apache Cloudberry 会创建所指定的表（根分区或父表），并且还会根据所指定的分区层次结构创建一个表的层次结构（子表）。

- 对根分区表运行 `ANALYZE` 时，会收集所有叶子分区的统计信息。叶子分区是 Apache Cloudberry 为分区表创建的子表层次结构中最底层的表。
- 对叶子分区运行 `ANALYZE` 时，只收集该叶子分区和根分区的统计信息。如果叶子分区中的数据发生了变化（例如对叶子分区数据做了大量更新，或者交换了叶子分区），则可以对该叶子分区运行 ANALYZE 以收集表统计信息。默认情况下，如果所有其他叶子分区都有统计信息，该命令会更新根分区的统计信息。

    例如，如果已经收集了一个具有大量分区的分区表的统计信息，之后只更新了少数叶子分区中的数据，则可以只对这些分区运行 `ANALYZE`，以更新这些分区的统计信息以及根分区的统计信息。

- 对不是叶子分区的子表运行 `ANALYZE` 时，不会收集统计信息。

    例如，可以创建一个分区表，其分区对应 2006 年到 2016 年，每年又有按月划分的子分区。如果对 2013 年的子表运行 `ANALYZE`，则不会收集任何统计信息。如果对 2013 年 3 月的叶子分区运行 `ANALYZE`，则只收集该叶子分区的统计信息。

对于包含已被交换为使用外部表的叶子分区的分区表，`ANALYZE` 不会收集该外部表分区的统计信息：

- 如果对外部表分区运行 `ANALYZE`，则不会分析该分区。
- 如果对根分区运行 `ANALYZE` 或 `ANALYZE ROOTPARTITION`，则不会对外部表分区采样，根表统计信息也不包含外部表分区。
- 如果指定了 `VERBOSE` 子句，则会显示一条信息性消息：`skipping external table`。

Apache Cloudberry 服务器配置参数 optimizer_analyze_root_partition 决定何时收集根分区表的统计信息。如果该参数为 `on`（默认值），则运行 `ANALYZE` 时无需 `ROOTPARTITION` 关键字即可收集根分区的统计信息。对根分区运行 `ANALYZE` 时，或者对分区表的某个叶子分区运行 `ANALYZE` 且其他叶子分区都有统计信息时，会收集根分区统计信息。如果该参数为 `off`，则必须运行 `ANALZYE ROOTPARTITION` 才能收集根分区统计信息。

`ANALYZE` 所收集的统计信息通常包括每列中一些最常见值的列表，以及显示每列中数据近似分布的直方图。如果 `ANALYZE` 认为这两者中的某一个或两个没有意义（例如，在唯一键列中没有常见值），或者列的数据类型不支持相应的操作符，则可能会省略其中一个或两个。

对于大表，`ANALYZE` 会对表内容进行随机采样，而不是检查每一行。这使得即使非常大的表也能在很短时间内完成分析。但要注意，统计信息只是近似值，即使表的实际内容没有变化，每次运行 `ANALYZE` 时统计信息也会略有变化。这可能会使 `EXPLAIN` 所显示的规划器估计代价出现小幅变化。在少数情况下，这种不确定性会导致查询优化器在两次 `ANALYZE` 之间选择不同的查询计划。为避免这种情况，可以通过调整配置参数 default_statistics_target 来提高 `ANALYZE` 收集的统计信息量，或者通过 `ALTER TABLE ... ALTER COLUMN ... SET (n_distinct ...)` 逐列设置每列的统计目标（参见 `ALTER TABLE`）。目标值设定最常见值列表中的最大条目数以及直方图中的最大桶数。默认目标值为 100，但可以调高或调低，以便在规划器估计的准确度与 `ANALYZE` 所需时间以及 `pg_statistic` 所占空间之间进行权衡。特别地，将统计目标设置为零会停用该列的统计信息收集。对于从不用于查询的 `WHERE`、`GROUP BY` 或 `ORDER BY` 子句的列，这样做可能有用，因为规划器用不到这类列的统计信息。

所分析的各列中最大的统计目标决定了为准备统计信息而采样的表行数。提高目标值会使 `ANALYZE` 所需的时间和空间按比例增加。

`ANALYZE` 估计的值之一是每列中出现的不同值的个数。由于只检查了行的一个子集，即使使用最大可能的统计目标，这一估计有时也可能相当不准确。如果这种不准确导致了糟糕的查询计划，可以手动确定一个更准确的值，然后用 `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS DISTINCT` 将其设置进去（参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)）。

当 Apache Cloudberry 执行 `ANALYZE` 操作以收集某个表的统计信息，并检测到所有被采样的表数据页都是空的（不包含有效数据）时，Apache Cloudberry 会显示一条消息，提示应执行 `VACUUM FULL` 操作。如果被采样的页是空的，则表统计信息将不准确。在对表进行大量更改（例如删除大量行）之后，页会变空。`VACUUM FULL` 操作会移除空页，使 `ANALYZE` 操作能够收集准确的统计信息。

如果表没有统计信息，则服务器配置参数 gp_enable_relsize_collection 控制 Postgres 规划器是使用默认统计信息文件，还是使用 `pg_relation_size` 函数估算表的大小。默认情况下，如果没有可用的统计信息，Postgres 规划器使用默认统计信息文件来估计行数。

## 示例 {#examples}

收集表 `mytable` 的统计信息：

```sql
ANALYZE mytable;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ANALYZE` 语句。

## 另见 {#see-also}

[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)、[EXPLAIN](/cloudberry/reference/sql-stmts/explain/)、[VACUUM](/cloudberry/reference/sql-stmts/vacuum/)、analyzedb。
