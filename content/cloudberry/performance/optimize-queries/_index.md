---
title: "Query Performance in Apache Cloudberry"
linkTitle: "Optimize Query Performance"
description: "Apache Cloudberry improves query performance through dynamic partition elimination and adaptive memory allocation."
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/index.md"
---

These mechanisms help reduce the amount of data scanned, speed up query execution, and enhance overall concurrency.

> [!TIP]
> Apache Cloudberry uses the GPORCA optimizer by default, which extends the native Postgres planner with more advanced optimization capabilities.

## Dynamic partition elimination {#dynamic-partition-elimination}

Apache Cloudberry supports dynamic partition elimination (DPE), a feature that prunes partitions at query execution time based on runtime values. This reduces the data scanned and improves query efficiency.

DPE is supported for the following join types:

- `Hash Inner Join`
- `Hash Left Join`
- `Hash Right Join` (since v2.0.0)

DPE is enabled when the following conditions are met:

- The partitioned table is on the outer side of the join.
- The join condition is an equality predicate on the partition key.
- Statistics are collected on the partitioned tables. For example:

    ```sql
    ANALYZE <root partition>;
    ```

The `gp_dynamic_partition_pruning` parameter controls whether DPE is enabled. It is ``ON`` by default but only applies to the Postgres optimizer. You can verify if DPE is in effect by checking the ``EXPLAIN`` plan for the presence of a `Partition Selector` node.

## Memory optimizations {#memory-optimizations}

Apache Cloudberry dynamically allocates memory based on the characteristics of query operators and proactively releases or reallocates memory during different query phases. This leads to more efficient memory usage and faster query execution.

> [!NOTE]
> Apache Cloudberry uses GPORCA by default. GPORCA extends the planning and optimization capabilities of the Postgres optimizer.
