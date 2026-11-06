---
title: "Apache Cloudberry 查询性能"
linkTitle: "优化查询性能"
description: "Apache Cloudberry 通过动态分区消除和自适应内存分配提高查询性能。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/index.md"
---

这些机制有助于减少扫描的数据量、加快查询执行，并提高整体并发能力。

> [!TIP]
> Apache Cloudberry 默认使用 GPORCA 优化器，它在原生 Postgres 规划器的基础上扩展了更高级的优化能力。

## 动态分区消除 {#dynamic-partition-elimination}

Apache Cloudberry 支持动态分区消除（DPE）：在查询执行时，根据运行时的值进行分区剪枝。这可以减少扫描的数据量，提高查询效率。

以下连接类型支持 DPE：

- `Hash Inner Join`
- `Hash Left Join`
- `Hash Right Join`（自 v2.0.0 起）

满足以下条件时，会启用 DPE：

- 分区表位于连接的外侧。
- 连接条件是分区键上的等值谓词。
- 已为分区表收集统计信息。例如：

    ```sql
    ANALYZE <root partition>;
    ```

`gp_dynamic_partition_pruning` 参数控制是否启用 DPE，默认值为 ``ON``，但仅适用于 Postgres 优化器。可以检查 ``EXPLAIN`` 计划中是否存在 `Partition Selector` 节点，确认 DPE 是否生效。

## 内存优化 {#memory-optimizations}

Apache Cloudberry 根据查询算子的特点动态分配内存，并在查询的不同阶段主动释放或重新分配内存，从而更高效地利用内存并加快查询执行。

> [!NOTE]
> Apache Cloudberry 默认使用 GPORCA。GPORCA 扩展了 Postgres 优化器的规划与优化能力。
