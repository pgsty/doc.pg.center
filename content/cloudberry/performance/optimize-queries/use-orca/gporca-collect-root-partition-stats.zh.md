---
title: "收集根分区统计信息"
description: "对于分区表，GPORCA 使用表的根分区统计信息生成查询计划。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-orca/gporca-collect-root-partition-stats.md"
---

这些统计信息用于确定连接顺序、拆分和合并聚合节点，以及估算各查询步骤的代价。相比之下，基于 Postgres 的规划器使用各叶子分区的统计信息。

如果要查询分区表，应收集根分区统计信息并定期更新，确保 GPORCA 能够生成最优查询计划。即使根分区统计信息过时或不存在，GPORCA 仍会对该表的查询执行动态分区消除，但查询计划可能不是最优的。

## 运行 ANALYZE {#run-analyze}

默认情况下，对根分区表运行 `ANALYZE` 会采样表中的叶子分区数据，并存储根分区统计信息。`ANALYZE` 收集根分区和叶子分区的统计信息，包括叶子分区的 HyperLogLog（HLL）统计信息。`ANALYZE ROOTPARTITION` 只收集根分区统计信息。服务器配置参数 `optimizer_analyze_root_partition` 控制收集根分区表的根统计信息时是否必须指定 `ROOTPARTITION` 关键字。有关收集分区表统计信息的详情，请参见 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/) 命令。

请注意，`ANALYZE` 在更新根分区统计信息之前总是扫描整张表。如果表非常大，该操作可能耗时很长。`ANALYZE ROOTPARTITION` 还会使用 `ACCESS SHARE` 锁，在运行期间阻止 `TRUNCATE`、`VACUUM` 等某些操作。因此，应定期安排 `ANALYZE`，或在叶子分区数据发生显著变化时运行。

在系统中的分区表上运行 `ANALYZE` 或 `ANALYZE ROOTPARTITION` 时，请遵循以下最佳实践：

- 向新分区表添加初始数据后，运行 `ANALYZE <root_partition_table_name>`。对于新叶子分区或数据发生变化的叶子分区，运行 `ANALYZE <leaf_partition_table_name>`。默认情况下，如果其他叶子分区已有统计信息，对叶子分区运行此命令也会更新根分区统计信息。
- 当该表的 `EXPLAIN` 计划显示查询性能下降，或叶子分区数据发生显著变化时，更新根分区统计信息。例如，生成根分区统计信息后又新增了叶子分区，可以考虑运行 `ANALYZE` 或 `ANALYZE ROOTPARTITION`，将新叶子分区插入的元组纳入根分区统计信息。
- 对于非常大的表，每周运行一次 `ANALYZE` 或 `ANALYZE ROOTPARTITION` 即可，或采用其他长于一天的间隔。
- 避免不带参数运行 `ANALYZE`，否则命令会作用于所有数据库表，包括分区表。对于大型数据库，这类全局 `ANALYZE` 操作难以监控，也难以预估完成时间。
- 如果 I/O 吞吐能力能够承受相应负载，可以考虑并行运行多个 `ANALYZE <table_name>` 或 `ANALYZE ROOTPARTITION <table_name>`，加快统计信息收集。
- 也可以使用 Apache Cloudberry 工具 `analyzedb` 更新表统计信息。如果叶子分区未发生修改，`analyzedb` 可以确保此前已分析过的表不会被重新分析。

## GPORCA 与叶子分区统计信息 {#gporca-and-leaf-partition-statistics}

创建和维护根分区统计信息对 GPORCA 的分区表查询性能至关重要，但维护叶子分区统计信息也同样重要。如果 GPORCA 无法为分区表查询生成计划，就会使用基于 Postgres 的规划器；此时需要叶子分区统计信息，才能为该查询生成最优计划。

对于直接访问叶子分区、而不是通过根分区加谓词消除分区的查询，GPORCA 自身也会使用叶子分区统计信息。例如，如果知道所需元组位于哪些分区，就可以直接查询相应叶子分区；此时 GPORCA 使用叶子分区统计信息。

## 禁用根分区统计信息的自动收集 {#deactivate-automatic-root-partition-statistics-collection}

如果不打算使用 GPORCA 查询分区表（将服务器配置参数 `optimizer` 设为 `off`），可以禁用分区表根分区统计信息的自动收集。服务器配置参数 `optimizer_analyze_root_partition` 控制收集根分区表的根统计信息时是否必须使用 `ROOTPARTITION` 关键字。该参数默认值为 `on`，此时 `ANALYZE` 无需 `ROOTPARTITION` 关键字即可收集根分区统计信息。将参数设为 `off` 可禁用自动收集；值为 `off` 时，必须运行 `ANALZYE ROOTPARTITION` 才能收集根分区统计信息。

1. 以 Apache Cloudberry 管理员 `gpadmin` 身份登录 Coordinator 主机。
2. 设置服务器配置参数。以下 Apache Cloudberry `gpconfig` 命令将参数设为 `off`：

    ```shell
    $ gpconfig -c optimizer_analyze_root_partition -v off --coordinatoronly
    ```

3. 重新启动 Apache Cloudberry。以下 Apache Cloudberry `gpstop` 命令会重新加载 Coordinator 和各 Segment 的 `postgresql.conf` 文件，而不关闭 Apache Cloudberry。

    ```shell
    gpstop -u
    ```
