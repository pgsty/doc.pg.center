---
title: "使用自动物化视图优化查询"
linkTitle: "使用自动物化视图优化查询"
description: "Apache Cloudberry 支持在查询规划阶段自动使用物化视图处理部分或全部查询，此功能称为 AQUMV。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-auto-materialized-view-to-answer-queries.md"
---

此功能适用于大型表查询，可以大幅缩短查询处理时间。AQUMV 使用增量物化视图（IMV），因为相关表发生写操作时，IMV 通常能够保持数据最新。

## 使用场景 {#usage-scenarios}

- 大型数据集上的聚合查询：对于需要聚合数百万条记录的查询，AQUMV 可以显著缩短查询时间。
- 频繁更新的大型表：在数据频繁更新的环境中，使用 IMV 可以保证查询结果的实时性和准确性。
- 复杂计算：对于包含平方根、绝对值等复杂计算的查询，AQUMV 可以在物化视图中预先计算这些值，从而加速查询。

## 使用示例 {#usage-example}

要启用 AQUMV，需要创建物化视图，并将系统参数 `enable_answer_query_using_materialized_views` 设为 `ON`。以下示例比较同一个复杂查询在未启用和启用 AQUMV 时的结果。

1. 关闭 GPORCA 规划器，使用基于 Postgres 的规划器。

    ```sql
    SET optimizer TO off;
    ```

2. 创建表 `aqumv_t1`。

    ```sql
    CREATE TABLE aqumv_t1(c1 INT, c2 INT, c3 INT) DISTRIBUTED BY (c1);
    ```

3. 向表中插入数据，并收集表统计信息。

    ```sql
    INSERT INTO aqumv_t1 SELECT i, i+1, i+2 FROM generate_series(1, 100000000) i;
    ANALYZE aqumv_t1;
    ```

4. 在未启用 AQUMV 的情况下执行查询，耗时 7384.329 ms。

    ```sql
    SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;

        sqrt
    -------------------66.0827625302982196.2449979983983985.9160797830996166.1644140029689766.3245553203367595.830951894845301
    (7 rows)

    Time: 7384.329 ms (00:07.384)
    ```

    从以下查询计划可以看到，优化器扫描了表（`Seq Scan on aqumv_t1 `）。

    ```sql
    EXPLAIN(COSTS OFF) SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;

                                                    QUERY PLAN

    -------------------------------------------------------------------------------------------------------------
    Gather Motion 3:1  (slice1; segments: 3)
    ->  Seq Scan on aqumv_t1
            Filter: ((c1 > 30) AND (c1 < 40) AND (sqrt((abs(c2))::double precision) > '5.8'::double pre
    cision))
    Optimizer: Postgres query optimizer
    (4 rows)
    ```

5. 基于 `aqumv_t1` 创建物化视图 `mvt1`，并收集视图的统计信息。

    ```sql
    CREATE INCREMENTAL MATERIALIZED VIEW mvt1 AS SELECT c1 AS mc1, c2 AS mc2, ABS(c2) AS mc3, ABS(ABS(c2) - c1 - 1) AS mc4
    FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40;

    ANALYZE mvt1;
    ```

6. 启用 AQUMV 相关配置参数。

    ```sql
    SET enable_answer_query_using_materialized_views = ON;
    ```

7. 此时 AQUMV 已启用。再次执行相同的查询，仅耗时 45.701 ms。

    ```sql
    SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;

        sqrt
    -------------------66.0827625302982196.2449979983983985.8309518948453015.9160797830996166.1644140029689766.324555320336759
    (7 rows)

    Time: 45.701 ms
    ```

    从以下查询计划可以看到，优化器没有扫描 `aqumv_t1` 表，而是扫描物化视图 `mvt1`（`Seq Scan on public.mvt1`）。

    ```sql
    EXPLAIN(VERBOSE, COSTS OFF) SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;

                                    QUERY PLAN
    --------------------------------------------------------------------------------
    Gather Motion 3:1  (slice1; segments: 3)
    Output: (sqrt(((mc4 + mc3))::double precision))
    ->  Seq Scan on public.mvt1
            Output: sqrt(((mc4 + mc3))::double precision)
            Filter: (sqrt((mvt1.mc3)::double precision) > '5.8'::double precision)
    Settings: enable_answer_query_using_materialized_views = 'on', optimizer = 'off'
    Optimizer: Postgres query optimizer
    (7 rows)
    ```

    在上述示例中，未启用 AQUMV、未使用物化视图时，查询耗时 7384.329 ms；启用 AQUMV 并使用物化视图后，相同查询仅耗时 45.701 ms。这意味着物化视图预先计算并存储了相关计算结果，因此视图只包含满足特定条件（`c1 > 30 AND c1 < 40`）的行。

    因此，上述表查询 `SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;` 等价于从物化视图查询 `SELECT SQRT(ABS(ABS(c2) - c1 - 1) + ABS(c2)) FROM aqumv_t1 WHERE c1 > 30 AND c1 < 40 AND SQRT(ABS(c2)) > 5.8;`。

执行相同查询时，可以直接从物化视图获取数据，而无需访问原表。通过这种方式，AQUMV 可以显著提高查询性能，尤其是在处理大量数据和复杂计算时。

## 实现方式 {#implementation}

AQUMV 通过对查询树进行等价变换实现查询优化。

只有表查询满足以下条件时，Apache Cloudberry 才会自动使用物化视图：

- 物化视图必须包含查询表达式所需的所有行。
- 如果物化视图包含的行多于查询所需，可能需要添加额外过滤条件。
- 所有输出表达式都必须能根据视图的输出计算得到。
- 输出表达式可以完全或部分匹配物化视图的目标列表。

如果存在多个有效的候选物化视图，或者查询物化视图的代价高于直接查询原表的代价（例如原表有索引），可以让规划器根据代价估算作出最佳选择。

## 限制 {#restrictions}

- 仅支持单个关系上的 `SELECT` 查询，此限制同时适用于物化视图查询和原查询。
- **不支持**的功能包括：

    - 聚合（AGG）
    - 子查询
    - 原查询排序（`ORDER BY`）
    - 连接（`JOIN`）
    - 子链接（`SUBLINK`）
    - 分组（`GROUP BY`）
    - 窗口函数
    - 公共表表达式（CTE）
    - 去重（`DISTINCT ON`）
    - 刷新物化视图（`REFRESH MATERIALIZED VIEW`）
    - `CREATE AS` 语句

## 另请参见 {#see-also}

- [并行创建 AO/AOCO 表和刷新物化视图](/cloudberry/performance/optimize-queries/parallel-create-ao-refresh-mv/)
- [Apache Cloudberry 增量物化视图](/cloudberry/performance/optimize-queries/use-incremental-materialized-view/)
