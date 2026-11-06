---
title: "使用 GPORCA 的注意事项"
description: "为确保 GPORCA 获得最佳查询性能，应仔细检查查询条件。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-orca/gporca-usage-considerations.md"
---

请确保满足以下条件：

- 表未使用多列分区键。
- 查询仅存在于 Coordinator 上的表（例如 *pg_attribute* 等系统表）时，应将服务器参数 `optimizer_enable_coordinator_only_queries` 设为 `on`。

    > [!NOTE]
    > 启用此参数可能降低短时系统表查询的性能。为避免这一问题，建议仅为当前会话或特定查询启用。

- 已收集分区表的根分区统计信息。

如果分区表包含超过 20,000 个分区，应考虑重新设计表结构。

以下服务器配置参数会影响 GPORCA 的查询规划行为：

- `optimizer_cte_inlining_bound` 控制 GPORCA 内联公共表表达式（CTE，即包含 `WITH` 子句的查询）的积极程度。
- `optimizer_force_comprehensive_join_implementation` 控制 GPORCA 是否同时评估嵌套循环和哈希连接计划。默认值为 `false`，表示有可用的哈希连接时，不考虑嵌套循环连接。
- `optimizer_force_multistage_agg` 强制 GPORCA 为带 `DISTINCT` 的标量聚合选择多阶段聚合计划。默认值为 `off`，表示按代价在单阶段与多阶段计划之间选择。
- `optimizer_force_three_stage_scalar_dqa` 在存在可选方案时，强制 GPORCA 为以 distinct 限定的聚合（DQA）选择三阶段计划。
- `optimizer_join_order` 设置连接顺序优化的级别，控制 GPORCA 会评估哪些类型的连接序列。
- `optimizer_join_order_threshold` 定义 GPORCA 使用动态规划连接顺序算法时允许的最大连接关系数。
- `optimizer_nestloop_factor` 调整 GPORCA 估算嵌套循环连接时使用的代价乘数。
- `optimizer_parallel_union` 控制使用 `UNION` 或 `UNION ALL` 的查询的并行度。设为 `on` 时，GPORCA 可能生成在各 Segment 上并行执行并集操作的计划。
- `optimizer_sort_factor` 调整排序操作的代价估算因子。可以调节此值，使估算更符合数据倾斜情况下的实际性能。
- `gp_enable_relsize_collection` 控制 GPORCA（以及 Postgres 规划器）在缺少统计信息时如何估算表大小。默认情况下，统计信息缺失时 GPORCA 使用默认行数；将此参数设为 `on` 后，则改用估算的表大小。

    此参数不适用于根分区。如果根分区缺少统计信息，GPORCA 始终使用默认估算值。可以通过以下命令收集根分区统计信息：

    ```sql
    ANALYZE ROOTPARTITION;
    ```

以下服务器参数控制日志记录和显示行为：

- `optimizer_print_missing_stats` 控制计划输出是否包含缺少统计信息的列的信息（默认值：`true`）。
- `optimizer_print_optimization_stats` 控制 GPORCA 是否记录内部优化指标（默认值：`off`）。

使用 `EXPLAIN ANALYZE` 执行 GPORCA 生成的计划时，只显示被剪枝的分区数量，不列出扫描了哪些分区。要在 Segment 日志中记录被扫描分区的名称，请将服务器参数 `gp_log_dynamic_partition_pruning` 设为 `on`。可以使用以下命令启用：

```sql
SET gp_log_dynamic_partition_pruning = on;
```
