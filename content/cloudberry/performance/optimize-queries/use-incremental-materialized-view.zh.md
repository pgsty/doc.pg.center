---
title: "Apache Cloudberry 增量物化视图"
linkTitle: "增量物化视图"
description: "本文介绍 Apache Cloudberry 增量物化视图的使用场景、用法、限制和注意事项。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-incremental-materialized-view.md"
---

增量物化视图是一种特殊的物化视图。当 Apache Cloudberry 中的基表数据发生插入、更新、删除等变化时，增量物化视图无需重新计算整个视图的全部数据，只更新自上次刷新以来发生变化的部分。这可以节省大量计算资源和时间，显著提高性能，尤其适合大型数据集。

> [!TIP]
> 增量物化视图与普通视图的比较：
>
> - 普通视图：不存储数据，每次执行查询时都根据定义的 SQL 语句动态生成结果。这意味着每次查询都需要重新计算视图中的数据，处理大量数据时可能耗时较长。
> - 增量物化视图：预先计算并存储结果集，减少查询执行时的计算工作量。此外，由于采用“增量”更新，底层数据发生变化时，只需更新受影响的部分，无需重新计算整个数据集。

## 使用场景 {#usage-scenarios}

- 查询执行过程中需要加速中间结果集的处理。
- 读操作多、写操作少。

## 使用示例 {#usage-example}

可以使用 SQL 命令 `CREATE INCREMENTAL MATERIALIZED VIEW` 创建增量物化视图。完整支持语法如下：

```sql
CREATE [INCREMENTAL] MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

以下示例展示如何为 Apache Cloudberry 中的表创建增量物化视图。

1. 创建表 `t0` 和 `t1`。

    ```sql
    CREATE TABLE t0 (a int) DISTRIBUTED BY (a);
    CREATE TABLE t1 (a int) DISTRIBUTED BY (a);
    ```

2. 基于这两张表创建增量物化视图 `m`。

    - 创建简单物化视图。以下语句创建增量物化视图 `m`，选择表 `t0` 的所有列，并按列 `a` 的值分布数据。这意味着视图 `m` 存储表 `t0` 的数据快照，并能根据 `t0` 的数据变化进行增量更新。

        ```sql
        CREATE INCREMENTAL MATERIALIZED VIEW m AS SELECT * FROM t0 DISTRIBUTED BY (a);
        ```

    - 创建包含连接操作的物化视图。以下语句同样创建名为 `m` 的增量物化视图，但这次会连接表 `t0` 和 `t1`。它选择所有满足 `t0.a` 等于 `t1.a` 条件的 `t0.a` 值。同样，视图按列 `a` 的值分布数据。

        ```sql
        CREATE INCREMENTAL MATERIALIZED VIEW m AS SELECT t0.a FROM t0, t1 WHERE t0.a = t1.a DISTRIBUTED BY (a);
        ```

3. 向表中插入数据。`RETURNING *` 子句会在数据插入后返回插入的行。

    ```sql
    INSERT INTO t0 VALUES (5);
    INSERT INTO t1 VALUES (5);
    INSERT INTO t0 VALUES (8) RETURNING *;
    ```

4. 检查物化视图 `m` 的结构和数据：

    ```sql
    postgres=# \d+ m
                                        MATERIALIZED VIEW "public.m"
    Column |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description 
    --------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
    a      | integer |           |          |         | plain   |             |              | 
    VIEW definition:
    SELECT t0.a
    FROM t0;
    DISTRIBUTED BY: (a)
    Access method: heap
    ```

5. 查看视图 `m` 中的数据。

    ```sql
    postgres=# TABLE m;
    a 
    ---
    5
    (1 row)
    ```

要调试与增量物化视图相关的语句执行，可以将系统参数 `debug_print_ivm ` 设为 `ON`，即执行 `SET debug_print_ivm = ON;`。参数详情如下：

| 参数名 | 说明 | 默认值 | 是否必需 | 示例 |
| --------------- | ------------------------------- | ------------- | --------------- | ------------------------- |
| debug_print_ivm | 是否启用 IVM 调试 | OFF | 否 | SET debug_print_ivm = ON; |

## 与普通视图的查询性能比较 {#query-performance-comparison-with-regular-view}

以下示例比较 Apache Cloudberry 处理大型数据集时，普通视图与增量物化视图的查询性能，使用的是 TPC-H 的 Query 15 测试数据集。

### 使用普通视图 {#with-regular-view}

1. 创建普通视图 `revenue0`。

    ```sql
    CREATE VIEW revenue0 (supplier_no, total_revenue) AS
            SELECT
                    l_suppkey,
                    SUM(l_extendedprice * (1 - l_discount))
            FROM
                    lineitem
            WHERE
                    l_shipdate >= DATE '1996-01-01'
                    AND l_shipdate < DATE '1996-01-01' + INTERVAL '3' MONTH
            GROUP BY
                    l_suppkey;
    ```

2. 从 `supplier` 表和 `revenue0` 视图中查询供应商详情及其最高收入。

    ```sql
    SELECT
            s_suppkey,
            s_name,
            s_address,
            s_phone,
            total_revenue
    FROM
            supplier,
            revenue0
    WHERE
            s_suppkey = supplier_no
            AND total_revenue = (
                    SELECT
                            MAX(total_revenue)
                    FROM
                            revenue0
            )
    ORDER BY s_suppkey;

    s_suppkey |          s_name           |     s_address     |     s_phone     | total_revenue 
    -----------+---------------------------+-------------------+-----------------+---------------
        8449 | Supplier#000008449        | Wp34zim9qYFbVctdW | 20-469-856-8873 |  1772627.2087
    (1 row)

    Time: 3040.23 ms
    ```

    在上述查询中，视图 `revenue0` 的结果实时计算，查询耗时 3040.23 ms。

### 使用增量物化视图 {#with-incremental-materialized-view}

也可以在 DDL 阶段创建增量物化视图，从而大幅缩短查询时间。

1. 创建增量物化视图 `revenue0`。

    ```sql
    CREATE INCREMENTAL MATERIALIZED VIEW revenue0 (supplier_no, total_revenue) AS
            SELECT
                    l_suppkey,
                    SUM(l_extendedprice * (1 - l_discount))
            FROM
                    lineitem
            WHERE
                    l_shipdate >= DATE '1996-01-01'
                    AND l_shipdate < DATE '1996-01-01' + INTERVAL '3' MONTH
            GROUP BY
                    l_suppkey;
    ```

2. 从 `supplier` 表和 `revenue0` 视图中查询供应商详情及其最高收入，查询仅耗时 65 ms。

    ```sql
    SELECT                
            s_suppkey,
            s_name,
            s_address,
            s_phone,
            total_revenue
    FROM
            supplier,
            revenue0
    WHERE
            s_suppkey = supplier_no
            AND total_revenue = (
                    SELECT
                            MAX(total_revenue)
                    FROM
                            revenue0
            )
    ORDER BY s_suppkey;

    s_suppkey |          s_name           |     s_address     |     s_phone     | total_revenue 
    -----------+---------------------------+-------------------+-----------------+---------------
        8449 | Supplier#000008449        | Wp34zim9qYFbVctdW | 20-469-856-8873 |  1772627.2087
    (1 row)

    Time: 65.731 ms
    ```

### TPC-H 对比 {#tpc-h-comparison}

我们进行了 TPC-H 测试，比较在不同数据量下，分别使用普通视图和增量物化视图时插入与查询的执行时间，结果如下。

| 数据量 | 普通插入 | 使用增量物化视图的插入 | 使用普通视图的查询 | 使用增量物化视图的查询 |
| ----------- | -------------- | ------------------------------------------ | ------------------------ | ------------------------------------------ |
| 1 GB        | 2712 ms        | 3777 ms                                    | 813 ms                   | 43 ms                                      |
| 5 GB        | 15681 ms       | 29363 ms                                   | 3040 ms                  | 63 ms                                      |
| 10 GB       | 43011 ms       | 73188 ms                                   | 7057 ms                  | 102 ms                                     |

从上表可以看出：

- 在不同数据量下，使用增量物化视图的查询都明显快于普通查询。增量物化视图显著提升了查询性能。
- 在不同数据量下，使用增量物化视图的插入都不如普通插入快。这是因为向表插入数据后，数据库需要同步更新物化视图，因此增量物化视图不适用于频繁写入的场景。

## 限制与注意事项 {#restrictions-and-notes}

目前，Apache Cloudberry 的增量物化视图有以下使用限制：

- 不支持为 AO 表创建增量物化视图。
- 不支持为分区表创建增量物化视图。
- 不支持在 PAX 存储上创建增量物化视图。
- 定义增量物化视图时，不支持以下子句或操作。

    - `min`、`max` 函数，以及自定义聚合函数
    - 左连接和右连接，即 `LEFT JOIN` 和 `OUTER JOIN`
    - 窗口函数、`HAVING` 子句
    - 子查询、CTE 查询
    - 集合操作（`UNION`、`INTERSECT`、`EXCEPT`）
    - `DISTINCT ON`, `ORDER BY`, `LIMIT`, `OFFSET`

- 不支持在物化视图上创建增量物化视图。

此外，在 Apache Cloudberry 中使用增量物化视图时，还需注意以下问题：

- 增量物化视图会降低数据插入、删除和更新的速度。此外，一张基表可能有多个增量物化视图，性能下降程度与增量物化视图数量成正比。
- 增量物化视图会生成临时文件，存储计算得到的增量视图，可能占用一定的存储空间。
- 物化视图可能增加存储成本，具体取决于视图定义。

### 另请参见 {#see-also}

- [使用自动物化视图优化查询](/cloudberry/performance/optimize-queries/use-auto-materialized-view-to-answer-queries/)
- [并行创建 AO/AOCO 表和刷新物化视图](/cloudberry/performance/optimize-queries/parallel-create-ao-refresh-mv/)
