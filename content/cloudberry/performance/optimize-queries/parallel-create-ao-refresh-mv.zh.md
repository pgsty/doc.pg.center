---
title: "并行创建 AO/AOCO 表和刷新物化视图"
description: "Apache Cloudberry 支持使用 `CREATE TABLE AS` 语句并行创建 AO 行存表和 AOCO 列存表，并支持并行刷新基于 AO 或 AOCO 表的物化视图。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/parallel-create-ao-refresh-mv.md"
---

并行处理可以加速表创建和物化视图刷新。

要使用并行功能，首先需要将系统参数 `enable_parallel` 设为 `ON`。

## 使用示例 {#usage-example}

### 并行创建 AO/AOCO 表 {#create-aoaoco-tables-in-parallel}

1. 创建基表 `t_p2`，并在建表语句中使用 `WITH` 指定并行工作进程数量。

    ```sql
    CREATE TABLE t_p2(c1 INT, c2 INT) WITH (parallel_workers=2) DISTRIBUTED BY (c1);
    ```

2. 向 `t_p2` 插入数据，并收集该表的统计信息。

    ```sql
    INSERT INTO t_p2 SELECT i, i+1 FROM generate_series(1, 10000000) i;
    ANALYZE t_p2;
    ```

3. 启用并行处理，并关闭 GPORCA 优化器。

    ```sql
    SET enable_parallel = ON;
    SET optimizer = OFF;
    ```

4. 使用 `CREATE TABLE AS` 基于 `t_p2` 创建表。执行计划中出现并行算子，表明表是并行创建的。

    - 创建 AO 表：

        ```sql
        EXPLAIN(COSTS OFF) CREATE TABLE ctas_ao USING ao_row AS SELECT SUM(a.c2) AS c2, AVG(b.c1) AS c1 FROM t_p2 a JOIN t_p2 b ON a.c1 = b.c1 DISTRIBUTED BY (c2);

                                QUERY PLAN                            
        -----------------------------------------------------------------
        Redistribute Motion 1:3  (slice1; segments: 1)
        Hash Key: (sum(a.c2))
        ->  Finalize Aggregate
                ->  Gather Motion 6:1  (slice2; segments: 6)
                    ->  Partial Aggregate
                            ->  Parallel Hash Join
                                Hash Cond: (a.c1 = b.c1)
                                ->  Parallel Seq Scan on t_p2 a
                                ->  Parallel Hash
                                        ->  Parallel Seq Scan on t_p2 b
        Optimizer: Postgres query optimizer
        (11 rows)
        ```

    - 创建 AOCO 表：

        ```sql
        EXPLAIN(COSTS OFF) CREATE TABLE ctas_aoco USING ao_column AS SELECT SUM(a.c2) AS c2, AVG(b.c1) AS c1 FROM t_p2 a JOIN t_p2 b ON a.c1 = b.c1 DISTRIBUTED BY (c2);

                                QUERY PLAN                            
        -----------------------------------------------------------------
        Redistribute Motion 1:3  (slice1; segments: 1)
        Hash Key: (sum(a.c2))
        ->  Finalize Aggregate
                ->  Gather Motion 6:1  (slice2; segments: 6)
                    ->  Partial Aggregate
                            ->  Parallel Hash Join
                                Hash Cond: (a.c1 = b.c1)
                                ->  Parallel Seq Scan on t_p2 a
                                ->  Parallel Hash
                                        ->  Parallel Seq Scan on t_p2 b
        Optimizer: Postgres query optimizer
        (11 rows)
        ```

### 并行刷新物化视图 {#refresh-materialized-views-in-parallel}

1. 创建基表 `t_p`，并在建表语句中使用 `WITH` 指定并行工作进程数量。

    ```sql
    CREATE TABLE t_p(c1 INT, c2 INT) WITH (parallel_workers=8) DISTRIBUTED BY (c1);
    ```

2. 向 `t_p` 插入数据，并收集该表的统计信息。

    ```sql
    INSERT INTO t_p SELECT i, i+1 FROM generate_series(1, 10000000) i;
    ANALYZE t_p;
    ```

3. 创建物化视图 `matv`，根据参数 `ao_row` 使用行存储（AO 行存）或列存储（AO 列存）。物化视图的内容是从表 `t_p` 得到的聚合查询结果。

    ```sql
    CREATE MATERIALIZED VIEW matv USING ao_row AS SELECT SUM(a.c2) AS c2, AVG(b.c1) AS c1 FROM t_p a JOIN t_p b ON a.c1 = b.c1 WITH NO DATA DISTRIBUTED BY (c2);
    ```

    ```sql
    CREATE MATERIALIZED VIEW matv USING ao_column AS SELECT SUM(a.c2) AS c2, AVG(b.c1) AS c1 FROM t_p a JOIN t_p b ON a.c1 = b.c1 WITH NO DATA DISTRIBUTED BY (c2);
    ```

4. 启用并行处理，并关闭 GPORCA 优化器。

    ```sql
    SET enable_parallel = ON;
    SET optimizer = OFF;
    ```

5. 刷新物化视图。

    ```sql
    REFRESH MATERIALIZED VIEW matv;
    ```

可以使用工具记录刷新耗时，比较启用和关闭并行处理时的差异，从而观察并行处理的加速效果。

## 加速效果 {#acceleration-effect}

| 是否启用并行处理 | 刷新基于 AO 表的物化视图耗时 | 刷新基于 AOCO 表的物化视图耗时 | 使用 `CREATE TABLE AS` 创建 AO 表耗时 | 使用 `CREATE TABLE AS` 创建 AOCO 表耗时 |
| ------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| 非并行 | 6.18 ms | 5.91 ms | 6.56 ms | 6.06 ms |
| 并行，4 个工作进程 | 2.83 ms | 2.81 ms | 2.37 ms | 2.48 ms |

## 另请参见 {#see-also}

- [使用自动物化视图优化查询](/cloudberry/performance/optimize-queries/use-auto-materialized-view-to-answer-queries/)
- [Apache Cloudberry 增量物化视图](/cloudberry/performance/optimize-queries/use-incremental-materialized-view/)
