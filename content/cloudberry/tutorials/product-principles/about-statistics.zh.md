---
title: "数据库统计信息"
description: "概述 Apache Cloudberry 中 ANALYZE 命令收集的统计信息。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/product-principles/about-statistics.md"
---

统计信息是描述数据库中所存数据的元数据。查询优化器需要最新的统计信息，才能为查询选择最佳执行计划。例如，查询连接两个表，且必须将其中一个表广播到所有 Segment 时，优化器可以选择较小的表，以减少网络流量。

优化器使用的统计信息由 `ANALYZE` 命令计算并保存在系统目录中。有三种方式可以发起统计信息收集操作：

- 直接运行 `ANALYZE` 命令。
- 在数据库外部的命令行中运行 `analyzedb` 管理工具。
- 对没有统计信息的表执行 DML 操作，或者 DML 操作修改的行数超过指定阈值时，触发自动统计信息收集。

以下各节介绍这些方法。`VACUUM ANALYZE` 命令也能发起统计信息收集，但不建议使用，因为清理和统计信息收集是目的不同的两种操作。

计算统计信息需要消耗时间和资源，因此 Apache Cloudberry 对大表采用抽样方式计算统计信息，得到估计值。大多数情况下，默认设置提供的信息足以生成正确的查询执行计划。如果生成的统计信息无法帮助优化器得到最佳执行计划，管理员可以调整配置参数，增大样本量，或细化保存在系统目录中的统计信息，以提高其准确性。更准确的统计信息会增加 CPU 和存储开销，却未必能生成更好的计划。因此，务必查看执行计划并测试查询性能，确认增加的统计开销确实带来了性能改善。

## 系统统计信息 {#system-statistics}

### 表大小 {#table-size}

查询规划器根据需要处理的行数和需要访问的磁盘页数的估计值，尽量减少执行查询所需的磁盘 I/O 与网络流量。这些估计值来自 `pg_class` 系统表的 `reltuples` 和 `relpages` 列，其中记录了上次执行 `VACUUM` 或 `ANALYZE` 命令时的行数和页数。随着行的增加或删除，这些数值会逐渐失准。不过，操作系统始终能提供准确的磁盘页数，因此只要 `reltuples` 与 `relpages` 的比值没有明显变化，优化器就能估算出足够准确的行数，以选择正确的查询执行计划。

如果 `reltuples` 列与 `SELECT COUNT(*)` 返回的行数相差很大，应收集统计信息以更新这些值。

`REINDEX` 命令重建索引后，会将 `relpages` 和 `reltuples` 列设为零。应对基表运行 `ANALYZE` 命令来更新这两列。

### pg_statistic 系统表与 pg_stats 视图 {#the-pg_statistic-system-table-and-pg_stats-view}

`pg_statistic` 系统表保存每个数据库表上次 `ANALYZE` 操作的结果。每个表的每一列都有一条记录，包含以下列：

`starelid`：该列所属表或索引的对象 ID。

`staattnum`：所描述列的编号，从 1 开始。

`stainherit`：如果为真，统计信息还包含通过继承得到的子表列，而不只是指定关系中的值。

`stanullfrac`：该列中空值所占的比例。

`stawidth`：非空值的平均存储宽度，单位为字节。

`stadistinct`：正数表示该列中不同值数量的估计值，预计不会随行数变化。负数则表示不同值数量除以行数后再取负值，即该列不同值数量与行数之比的负值。当不同值数量随行数增加时，采用这种形式。例如，唯一列的 `n_distinct` 值为 -1.0。平均宽度大于 1024 的列视为唯一列。

`stakind<i>N</i>`：代码编号，表示 `pg_statistic` 记录的第 <i>N</i> 个槽中存储的统计信息类型。

`staop<i>N</i>`：用于计算第 <i>N</i> 个槽中统计信息的操作符。例如，直方图槽会记录定义数据排序顺序的 < 操作符。

`stanumbers<i>N</i>`：float4 数组，包含第 <i>N</i> 个槽对应类型的数值统计信息；如果该槽的类型不涉及数值，则为 `NULL`。

`stavalues<i>N</i>`：第 <i>N</i> 个槽对应类型的列数据值；如果该槽的类型不存储数据值，则为 `NULL`。每个数组的元素实际上都采用对应列的数据类型，因此无法将这些列的类型定义得比 `<i>anyarray</i>` 更具体。

不同数据类型的列所收集的统计信息不同，因此 `pg_statistic` 表使用四个槽（`<i>slots</i>`）来存储适合相应数据类型的统计信息，每个槽由四列组成。例如，第一个槽通常保存该列的最常见值，由 `stakind1`、`staop1`、`stanumbers1` 和 `stavalues1` 列组成。

各个 `stakindN` 列包含一个数字代码，用于描述其槽中存储的统计信息类型。`stakind` 的代码 1 到 99 保留给 PostgreSQL 核心数据类型使用。Apache Cloudberry 使用代码 1、2、3、4、5 和 99。值为 0 表示该槽未使用。下文介绍这三种代码所存储的统计信息类型。

**`stakind` 代码 1：最常见值（MCV）槽**

- `staop` 包含 `=` 操作符的对象 ID，用来判断两个值是否相同。
- `stavalues` 包含一个数组，保存该列中最常见的 *K* 个非空值。
- `stanumbers` 包含 `stavalues` 数组中各个值的频率，即占总行数的比例。

这些值按频率降序排列。由于数组大小可变，统计信息收集器可以自行选择 *K* 的值。只有出现不止一次的值才会加入 `stavalues` 数组；唯一列没有 MCV 槽。

**`stakind` 代码 2：直方图槽**

描述标量数据的分布。

- `staop` 是 `<` 操作符的对象 ID，用于描述排序顺序。
- `stavalues` 包含 *M* 个非空值，其中 `M`>=2，将该列的非空数据值划分为 `M`-1 个数量大致相等的区间。第一个 `stavalues` 元素为最小值，最后一个为最大值。
- `stanumbers` 不使用，应为 `NULL`。

如果还提供了最常见值槽，则直方图描述的是移除 MCV 数组中所列值之后的数据分布，技术上称为*压缩直方图*。当某列包含一些出现频率很高的值时，这种方式能更准确地表示其分布。如果某列只有少量不同值，MCV 列表可能已涵盖全部数据；此时直方图为空，应省略。

**`stakind` 代码 3：相关性槽**

描述表元组的物理顺序与该列数据值排序之间的相关性。

- `staop` 是 `<` 操作符的对象 ID。与直方图一样，理论上可以有多个条目。
- `stavalues` 不使用，应为 `NULL`。
- `stanumbers` 只包含一个条目，即数据值序列与其实际元组位置序列之间的相关系数。系数范围为 +1 到 -1。

**`stakind` 代码 4：最常见元素槽**

这与最常见值（MCV）槽类似，但存储的是列值中最常见的非空*元素*。当列的数据类型为数组，或其他具有可识别元素的类型（例如 `tsvector`）时，这种统计信息很有用。

- `staop` 包含适合该元素类型的等值操作符。
- `stavalues` 包含最常见的元素值。
- `stanumbers` 包含常见元素的频率。

频率按该元素值出现的非空行占所有非空行的比例计算，而不是按所有行计算。另外，这些值按元素类型的默认顺序排序，以支持对特定值进行二分查找。因此，最小频率和最大频率在 `stanumbers` 中的位置无法预先确定，`stanumbers` 会额外添加两个元素，分别保存最小频率和最大频率。还可以选择添加第三个额外元素，保存空元素的频率，计算方式相同：包含至少一个空元素的非空行占所有非空行的比例。如果省略此元素，则认为该列不包含 `NULL` 元素。

> **注意：** 对于 `tsvector` 列，`stavalues` 中的元素类型为 `text`，尽管它们在 `tsvector` 中的表示并不完全是 `text`。

**`stakind` 代码 5：不同元素数量直方图槽**

描述数组类型列中每一行所含不同元素值数量的分布。只考虑非空行和非空元素。

- `staop` 包含适合该元素类型的等值操作符。
- `stavalues` 不使用，应为 `NULL`。
- `stanumbers` 包含不同元素的信息。`stanumbers` 的最后一个元素是在所有非空行中，不同元素值数量的平均值。前面的 *M* 个元素（其中 `M` >=2）构成直方图，将不同元素数量的总体划分为 `M`-1 个数量大致相等的区间。其中第一个元素是观测到的最小数量，最后一个是最大数量。

**`stakind` 代码 99：Hyperloglog 槽**

对于分区表的叶子分区，存储根据抽样数据创建的 `hyperloglog_counter`。`hyperloglog_counter` 数据结构会转换为 `bytea`，并存入 `pg_statistic` 系统目录表的 `stavalues5` 槽。

`pg_stats` 视图以更便于阅读的格式呈现 `pg_statistic` 的内容。`pg_stats` 视图包含以下列：

`schemaname`：包含该表的模式名称。

`tablename`：表名。

`attname`：此行所描述的列名。

`inherited`：如果为真，统计信息包含通过继承得到的子表列。

`null_frac`：该列中空值所占的比例。

`avg_width`：该列各项的平均存储宽度，单位为字节，按 `avg(pg_column_size(column_name))` 计算。

`n_distinct`：正数表示该列中不同值数量的估计值，预计不会随行数变化。负数则表示不同值数量除以行数后再取负值，即该列不同值数量与行数之比的负值。当不同值数量随行数增加时，采用这种形式。例如，唯一列的 `n_distinct` 值为 -1.0。平均宽度大于 1024 的列视为唯一列。

`most_common_vals`：包含该列最常见值的数组；如果没有明显更常见的值，则为空。如果 `n_distinct` 列为 -1，`most_common_vals` 为空。数组长度取该列实际不同值数量与 `default_statistics_target` 配置参数值中的较小者。可以使用 `ALTER TABLE table SET COLUMN column SET STATISTICS N` 为某一列覆盖这个数量。

`most_common_freqs`：包含 `most_common_vals` 数组中各个值频率的数组。频率等于某值的出现次数除以总行数。该数组与 `most_common_vals` 数组长度相同。如果 `most_common_vals` 为空，该数组也为空。

`histogram_bounds`：将列值划分为大小大致相同的各组的一组边界值。只有该列存在 `max()` 聚合函数时，才能定义直方图。直方图的分组数与 `most_common_vals` 数组大小相同。

`correlation`：Apache Cloudberry 会为堆表和 AO/AOCO 表计算相关性统计信息，但基于 Postgres 的规划器只对堆表使用这些统计信息。

`most_common_elems`：包含最常见元素值的数组。

`most_common_elem_freqs`：包含常见元素频率的数组。

`elem_count_histogram`：描述数组类型列中每一行所含不同元素值数量分布的数组。

新建的表和索引没有统计信息。可以使用 `gp_toolkit` 模式中的 `gp_stats_missing` 视图，查找缺少统计信息的表：

```sql
SELECT * from gp_toolkit.gp_stats_missing;
```

### 抽样 {#sampling}

计算大表的统计信息时，Apache Cloudberry 会对基表抽样，创建一个较小的表。如果该表是分区表，则从所有分区中抽样。

### 更新统计信息 {#update-statistics}

不带参数运行 `ANALYZE` 会更新数据库中所有表的统计信息。这可能耗时很长，因此最好在数据发生变化后有选择地分析表。也可以只分析表中部分列，例如用于连接、`WHERE` 子句、`SORT` 子句、`GROUP BY` 子句或 `HAVING` 子句的列。

分析严重膨胀的表时，如果样本包含空页，可能会生成质量较差的统计信息。因此，最好先清理膨胀的表，再收集统计信息。

### 分析分区表 {#analyze-partitioned-tables}

在分区表上运行 `ANALYZE` 命令时，它会逐一分析各个叶子分区。可以只对新增或修改过的分区表运行 `ANALYZE`，以避免分析未发生变化的分区。

`analyzedb` 命令行工具会自动跳过未变化的分区。它还会启动并发会话，以便同时分析多个分区。默认启动五个会话，可以通过 `-p` 命令行选项将会话数设为 1 到 10。每次运行时，`analyzedb` 都会将 AO 表和分区的状态信息保存到 Coordinator 数据目录的 `db_analyze` 目录中。下次运行时，`analyzedb` 会将每个表的当前状态与已保存状态比较，如果表或分区未变化，就跳过分析。堆表则始终会被分析。

如果启用了 GPORCA（默认启用），还需要对根分区表（而非叶子分区）运行 `ANALYZE` 或 `ANALYZE ROOTPARTITION`，以刷新根分区统计信息。GPORCA 需要分区表根级别的统计信息。基于 Postgres 的规划器不使用这些统计信息。

分析分区表所需的时间，与分析具有相同数据的非分区表相近。如果所有叶子分区都有统计信息，那么执行 `ANALYZE ROOTPARTITION` 生成根分区统计信息通常很快，只需几秒钟，具体取决于分区数和表的列数。如果某些叶子分区没有统计信息，则会对整个表的数据抽样，以生成根分区统计信息。对表数据抽样耗时更长，生成的根分区统计信息质量也较低。

Apache Cloudberry 服务器配置参数 [optimizer_analyze_root_partition](/cloudberry/reference/config-params-guc-list/) 决定何时收集根分区表的统计信息。如果该参数为 `on`（默认值），运行 `ANALYZE` 时不需要 `ROOTPARTITION` 关键字就能收集根分区统计信息。在根分区上运行 `ANALYZE`，或者对某个叶子分区运行 `ANALYZE` 且其他叶子分区都有统计信息时，都会收集根分区统计信息。如果该参数为 `off`，则必须运行 `ANALYZE ROOTPARTITION` 才能收集根分区统计信息。

如果不打算使用 GPORCA 查询分区表，即将服务器配置参数 [optimizer](/cloudberry/reference/config-params-guc-list/) 设为 `off`，也可以将服务器配置参数 `optimizer_analyze_root_partition` 设为 `off`，以限制 `ANALYZE` 更新根分区统计信息的时机。

## 配置统计信息 {#configure-statistics}

可以通过多种选项配置 Apache Cloudberry 的统计信息收集。

### 统计目标 {#statistics-target}

统计目标是单个列的 `most_common_vals`、`most_common_freqs` 和 `histogram_bounds` 数组的大小，默认值为 25。可以通过服务器配置参数修改默认目标，也可以使用 `ALTER TABLE` 命令为任意列设置目标。较大的值会增加执行 `ANALYZE` 所需的时间，但可能提高基于 Postgres 的规划器的估计质量。

设置 `default_statistics_target` 服务器配置参数，可以修改系统默认统计目标。默认值通常已足够，只有测试表明新目标能改善查询计划时，才应提高或降低该值。例如，可以使用 `gpconfig` 工具将默认统计目标从 100 提高到 150：

```shell
gpconfig -c default_statistics_target -v 150
```

可以使用 `ALTER TABLE` 命令为单个列设置统计目标。例如，提高某些列的目标可能改善部分查询，尤其是数据分布不规则的列。对于从不参与查询优化的列，可以将目标设为零。目标为 0 时，`ANALYZE` 会忽略该列。例如，以下 `ALTER TABLE` 命令将 `emp` 表的 `notes` 列的统计目标设为零：

```sql
ALTER TABLE emp ALTER COLUMN notes SET STATISTICS 0;
```

统计目标可设为 0 到 1000，也可以设为 -1，以恢复使用系统默认统计目标。

在父分区表上设置统计目标会影响子分区。如果将父表中某些列的统计目标设为 0，所有子分区中相同列的统计目标也会设为 0。但是，如果之后添加或交换另一个子分区，新子分区会使用默认统计目标；交换得到的子分区则使用此前的统计目标。因此，添加或交换子分区后，应在新的子表上设置统计目标。

### 自动收集统计信息 {#automate-statistics-collection}

可以配置 Apache Cloudberry，使其在对表执行某些操作时，如果该表没有统计信息或已发生显著变化，就自动运行 `ANALYZE`。对于分区表，只有直接在叶子表上执行操作时，才会触发自动统计信息收集，并且只分析该叶子表。

自动统计信息收集由服务器配置参数控制，有三种模式：

- `none` 关闭自动统计信息收集。
- `on_no_stats`：表没有统计信息，且表所有者对其运行 `CREATE TABLE AS SELECT`、`INSERT` 或 `COPY` 命令时，触发统计信息收集。
- `on_change`：表所有者对其运行 `CREATE TABLE AS SELECT`、`UPDATE`、`DELETE`、`INSERT` 或 `COPY` 命令，且受影响行数超过 `gp_autostats_on_change_threshold` 配置参数定义的阈值时，触发统计信息收集。

在过程语言函数内部执行的命令与在函数外部执行的命令，分别设置自动统计信息收集模式：

- `gp_autostats_mode` 配置参数控制函数外部的自动统计信息收集行为，默认设为 `on_no_stats`。
- `gp_autostats_mode_in_functions` 参数控制在过程语言函数内部操作表时的行为，默认设为 `none`。

在 `on_change` 模式下，只有受影响行数超过 `gp_autostats_on_change_threshold` 配置参数定义的阈值，才会触发 `ANALYZE`。该参数的默认值很大，为 2147483647，实际上相当于关闭了自动统计信息收集；必须将阈值调低才能启用。`on_change` 模式可能触发预料之外的大规模统计信息收集，影响系统运行，因此不建议全局设置。在单个会话中则可能有用，例如在加载数据后自动分析表。

将 `gp_autostats_allow_nonowner` 服务器配置参数设为 `true`，还会使 Apache Cloudberry 在以下情况下触发自动统计信息收集：

- `gp_autostats_mode=on_change`，且表被非所有者修改。
- `gp_autostats_mode=on_no_stats`，且首个向表中执行 `INSERT` 或 `COPY` 的用户不是表所有者。

要关闭函数外部的自动统计信息收集，将 `gp_autostats_mode` 参数设为 `none`：

```shell
gpconfigure -c gp_autostats_mode -v none
```

要为函数中尚无统计信息的表启用自动统计信息收集，将 `gp_autostats_mode_in_functions` 改为 `on_no_stats`：

```shell
gpconfigure -c gp_autostats_mode_in_functions -v on_no_stats
```

如果希望记录自动统计信息收集操作，将 `log_autostats` 系统配置参数设为 on。
