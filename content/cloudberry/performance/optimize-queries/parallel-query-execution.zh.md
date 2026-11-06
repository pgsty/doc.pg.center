---
title: "使用并行查询执行"
linkTitle: "并行查询执行"
description: "本文介绍 Apache Cloudberry 并行查询执行的使用场景、示例、限制和常见问题。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/parallel-query-execution.md"
---

Apache Cloudberry 执行查询时，会使用多个 CPU 核处理单个查询，从而提高查询性能。数据库根据数据量变化，动态调整计算节点（包括 `SeqScan` 算子）的数量。

## 适用场景 {#applicable-scenarios}

适用于在一台物理机上部署少量 Segment 的场景。在这种情况下，使用并行查询执行可以动态调整并行会话，无需部署更多 Segment 即可提高性能。

当主机的 CPU 和磁盘负载不高时，为算子启用并行会话可以获得更好的性能。

## 使用方法 {#how-to-use}

Apache Cloudberry 支持对 AO/AOCO 表和堆表执行并行查询。

### 堆表上的并行查询 {#parallel-queries-on-heap-tables}

1. 启用并行查询前，需要关闭 GPORCA 优化器。

    ```sql
    SET enable_parallel = ON;
    SET optimizer = OFF;
    ```

2. 设置并行会话数量的最大值。

    ```sql
    -- When setting this parameter
    -- you need to consider the number of CPU cores and segments.
    SET max_parallel_workers_per_gather = 4;
    ```

    查询示例：

    ```sql
    CREATE TABLE t1 (c1 int,c2 int, c3 int, c4 box) distributed by (c1);
    INSERT INTO t1 SELECT x, 2*x, 3*x, box('6,6,6,6') FROM generate_series(1,1000000) AS x;
    SELECT count(*) from t1;
    ```

### AO/AOCO 表上的并行查询 {#parallel-queries-on-aoaoco-tables}

1. 启用并行查询前，需要关闭 GPORCA 优化器。

    ```sql
    SET enable_parallel = ON;
    SET optimizer = OFF;
    ```

2. 设置并行会话数量的最大值。

    ```sql
    -- When setting this parameter
    -- you need to consider the number of CPU cores and segments.
    SET max_parallel_workers_per_gather = 4;

    -- Sets how many files the data will be inserted into in a transaction.
    -- Larger values might lead to performance degradation, especially for AOCO tables.
    SET gp_appendonly_insert_files = 8;

    -- Switches to the next file to insert data every 100,000 rows.
    -- This number of rows can be adjusted,
    -- to make the data as evenly distributed as possible across multiple files.
    SET gp_appendonly_insert_files_tuples_range = 100000;
    ```

3. 插入数据并运行查询。

    ```sql
    CREATE TABLE ao(x INT) USING ao_row;
    INSERT INTO ao SELECT i FROM generate_series(1, 1000000) i;
    -- It is recommended to update statistics first.
    ANALYZE ao;
    SELECT COUNT(*) FROM ao;
    ```

## 参数说明 {#parameter-description}

| 参数名 | 说明 | 默认值 | 是否必需 | 示例 |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------- | --------------- | --------------------------------------------------------- |
| `enable_parallel` | 是否启用并行执行。 | `OFF` | 是 | `SET enable_parallel = ON;` |
| `optimizer` | 是否启用 GPORCA 优化器。 | `ON` | 是 | `SET optimizer = OFF;` |
| `gp_appendonly_insert_files` | 指定一个事务中将数据插入多少个文件。 | `4` | 否 | `SET gp_appendonly_insert_files = 8;` |
| `gp_appendonly_insert_files_tuples_range` | 指定单个文件的行数阈值，超过后将数据插入新文件。 | `100000` | 否 | `SET gp_appendonly_insert_files_tuples_range = 100000;` |

## 常见问题 {#frequently-asked-questions}

- 目前，Apache Cloudberry 支持并行执行包含以下算子的查询。如果查询包含其他算子，则不会并行执行。

    ```sql
    sequence scan      
    index scan      
    index only scan      
    bitmap heap scan      
    append
    hash join      
    nestloop join      
    merge join
    ```

- 并行查询不一定能提高查询性能。并行会话过多会造成过载，导致性能下降。
- 为查询启用并行会话会显著增加内存开销，可能因内存不足而报错。
