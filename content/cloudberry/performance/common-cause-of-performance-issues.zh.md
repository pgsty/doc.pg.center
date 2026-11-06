---
title: "性能问题的常见原因"
description: "本文介绍常见性能问题的排查过程及可能的解决方法。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/common-cause-of-performance-issues.md"
---

## 识别硬件和 Segment 故障 {#identify-hardware-and-segment-failures}

Apache Cloudberry 的性能取决于运行它的硬件和 IT 基础设施。Apache Cloudberry 由多台服务器（主机）协同组成一个完整的系统（阵列）；诊断性能问题的第一步是确认所有 Apache Cloudberry Segment 均处于在线状态。Apache Cloudberry 的性能取决于阵列中最慢的主机。CPU 利用率、内存管理、I/O 处理或网络负载方面的问题都会影响性能。常见的硬件相关问题包括：

- **磁盘故障**——使用 RAID 时，单个磁盘故障通常不会显著影响数据库性能，但磁盘重新同步会消耗故障磁盘所在主机的资源。`gpcheckperf` 工具可以帮助识别存在磁盘 I/O 问题的 Segment 主机。
- **主机故障**——主机离线时，其上的 Segment 将无法运行。这意味着阵列中的其他主机必须承担平时两倍的工作负载，因为它们既要运行主 Segment，又要运行多个镜像。如果没有启用镜像，服务就会中断。恢复故障 Segment 时，服务会暂时中断。`gpstate` 工具可以帮助识别故障 Segment。
- **网络故障**——网卡、交换机或 DNS 服务器故障可能导致 Segment 停止运行。如果 Cloudberry 阵列中的主机名或 IP 地址无法解析，在 Apache Cloudberry 中就会表现为 Interconnect 错误。`gpcheckperf` 工具可以帮助识别存在网络问题的 Segment 主机。
- **磁盘容量**——Segment 主机的磁盘使用率不应超过 70%。Apache Cloudberry 需要保留一定的可用空间用于运行时处理。加载或更新数据后，请运行 `VACUUM`，回收已删除行占用的磁盘空间。`gp_toolkit` 管理模式提供了许多视图，可用于检查分布式数据库对象的大小。

## 管理工作负载 {#manage-workload}

数据库系统的 CPU 能力、内存和磁盘 I/O 资源都是有限的。多个工作负载竞争这些资源时，数据库性能就会下降。资源管理旨在满足不同业务需求的同时，尽可能提高系统吞吐量。Apache Cloudberry 提供资源队列和资源组，帮助管理这些系统资源。

资源队列和资源组限制资源使用量，以及特定队列或组中运行的并发查询总数。管理员可以将数据库角色分配给适当的队列或组，控制并发用户查询，防止系统过载。有关资源队列和资源组的更多信息，包括如何为 Apache Cloudberry 环境选择适当的方案，请参见[资源管理](/cloudberry/performance/manage-resources/manage-resources-using-resource-queues/)。

Apache Cloudberry 管理员应在非工作时间运行数据加载、`VACUUM ANALYZE` 等维护工作负载。不要与数据库用户争抢系统资源，应在使用量较低的时段执行管理任务。

## 避免争用 {#avoid-contention}

多个用户或工作负载尝试以相互冲突的方式使用系统时，就会产生争用；例如，两个事务尝试同时更新一张表。请求表级锁或行级锁的事务会一直等待，直到冲突的锁被释放。应用程序不应让事务长时间保持打开状态，例如在等待用户输入期间仍不结束事务。

## 维护数据库统计信息 {#maintain-database-statistics}

Apache Cloudberry 使用基于代价的查询优化器，它依赖数据库统计信息。准确的统计信息有助于查询优化器更好地估算查询检索出的行数，从而选择最高效的查询计划。缺少数据库统计信息时，查询优化器无法估算将返回多少条记录。优化器不会假定有足够的内存执行聚合等特定操作，因此会采取最保守的策略，通过磁盘读写执行这些操作。这比在内存中执行慢得多。ANALYZE 用于收集查询优化器所需的数据库统计信息。

> [!NOTE]
> 使用 GPORCA 运行 SQL 命令时，如果收集该命令所引用的一列或多列的统计信息能够提高性能，Apache Cloudberry 就会发出警告。警告会显示在命令行中，相关信息也会写入 Apache Cloudberry 日志文件。有关收集表列统计信息的详情，请参见 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/) 命令。

### 从查询计划中识别统计信息问题 {#identify-statistics-problems-in-query-plans}

在使用 EXPLAIN 或 `EXPLAIN ANALYZE` 解读查询计划之前，应先熟悉数据，以便发现可能的统计信息问题。检查计划中是否存在以下统计信息不准确的迹象：

- **优化器的估算是否接近实际情况？** 运行 `EXPLAIN ANALYZE`，查看优化器估算的行数是否接近查询操作实际返回的行数。
- **选择性强的谓词是否在计划早期应用？** 选择性最强的过滤条件应尽早应用，以减少沿计划树向上传递的行数。
- **优化器是否选择了最佳连接顺序？** 对于连接多个表的查询，应确认优化器选择了选择性最强的连接顺序。能排除最多行的连接应在计划中更早执行，以减少沿计划树向上传递的行数。

有关解读查询计划的更多信息，请参见[分析查询性能](/cloudberry/performance/optimize-queries/analyze-query-performance/)。

### 调整统计信息收集 {#tune-statistics-collection}

以下配置参数控制收集统计信息时采样的数据量：

- `default_statistics_target`

这些参数在系统级控制统计信息采样。更好的做法是仅对查询谓词中最常用的列增加统计信息采样量。可以使用以下命令调整特定列的统计信息：

`ALTER TABLE...SET STATISTICS`

例如：

```sql
ALTER TABLE sales ALTER COLUMN region SET STATISTICS 50;
```

这相当于为某一列单独修改 `default_statistics_target`。后续的 `ANALYZE` 操作将为该列收集更多统计数据，从而生成更好的查询计划。

## 优化数据分布 {#optimize-data-distribution}

在 Apache Cloudberry 中创建表时，必须声明一个分布键，使数据能够均匀分布到系统的所有 Segment 上。由于各个 Segment 并行执行查询，Apache Cloudberry 的速度始终受最慢的 Segment 限制。如果数据分布不均，数据较多的 Segment 返回结果就会更慢，从而拖慢整个系统。

## 优化数据库设计 {#optimize-your-database-design}

许多性能问题都可以通过改进数据库设计来解决。请检查数据库设计并考虑以下问题：

- 模式是否反映了数据的访问方式？
- 能否将较大的表拆分为分区？
- 是否使用了能够存储列值的最小数据类型？
- 用于连接表的列是否具有相同的数据类型？
- 索引是否得到使用？

### Apache Cloudberry 的上限 {#apache-cloudberry-maximum-limits}

为优化数据库设计，请了解 Apache Cloudberry 支持的上限：

|维度|上限|
|---------|-----|
|数据库大小|无限制|
|表大小|无限制，每个 Segment 上的每个分区最多 128 TB|
|行大小|1.6 TB（1600 列 * 1 GB）|
|字段大小|1 GB|
|每张表的行数|281474976710656 (2^48)|
|每张表／视图的列数|1600|
|每张表的索引数|无限制|
|每个索引的列数|32|
|每张表的表级约束数|无限制|
|表名长度|63 字节（受 *name* 数据类型限制）|

标为无限制的维度在 Apache Cloudberry 内部没有固有上限。但实际使用时，仍受可用磁盘空间、内存和交换空间的限制。当这些值异常大时，性能可能下降。

> [!NOTE]
> 同时存在的对象（表、索引和视图，不包括行）数量有上限，为 `4294967296` (2^32)。
