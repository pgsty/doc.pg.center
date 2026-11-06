---
title: "GPORCA 功能与增强"
description: "GPORCA 可优化分区表查询、子查询、公共表表达式及数据操作。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-orca/orca-features.md"
---

GPORCA 为某些类型的查询和操作提供了增强支持：

- 分区表查询
- 包含子查询的查询
- 包含公共表表达式（CTE）的查询
- 优化后的 DML 操作

## 分区表查询增强 {#enhancements-for-partitioned-table-queries}

GPORCA 处理分区表查询时，会应用以下优化：

- 增强分区剪枝能力。

- 查询计划可以包含 Partition Selector 算子。

- `EXPLAIN` 计划不再枚举所有分区。

    对于使用静态分区剪枝的查询（例如将分区键与常量比较），GPORCA 在 `EXPLAIN` 输出中显示 Partition Selector 算子，包括过滤条件和选中的分区数量。例如：

    ```sql
    Partition Selector for Part_Table (dynamic scan id: 1) 
            Filter: a > 10
            Partitions selected:  1 (out of 3)
    ```

    对于动态分区剪枝（例如将分区键与变量比较），分区在执行时确定，`EXPLAIN` 输出不列出选中的分区。

- 查询计划的大小不会随分区数量增加而增长。

- 显著降低因分区数量过多而发生内存不足错误的风险。

以下 `CREATE TABLE` 示例创建范围分区表：

```sql
CREATE TABLE sales(order_id int, item_id int, amount numeric(15,2), 
      date date, yr_qtr int)
   PARTITION BY RANGE (yr_qtr) (start (201501) INCLUSIVE end (201504) INCLUSIVE, 
   start (201601) INCLUSIVE end (201604) INCLUSIVE,
   start (201701) INCLUSIVE end (201704) INCLUSIVE,     
   start (201801) INCLUSIVE end (201804) INCLUSIVE,
   start (201901) INCLUSIVE end (201904) INCLUSIVE,
   start (202001) INCLUSIVE end (202004) INCLUSIVE);
```

GPORCA 可优化以下分区表查询：

- 全表扫描：计划中不枚举分区。

    ```sql
    SELECT * FROM sales;
    ```

- 带常量过滤条件的查询：应用分区剪枝。

    ```sql
    SELECT * FROM sales WHERE yr_qtr = 201501;
    ```

- 范围查询：同样触发分区剪枝。

    ```sql
    SELECT * FROM sales WHERE yr_qtr BETWEEN 201601 AND 201704;
    ```

- 分区表上的连接：例如连接维度表 `date_dim` 与事实表 `catalog_sales`。

    ```sql
    SELECT * FROM catalog_sales
        WHERE date_id IN (SELECT id FROM date_dim WHERE month=12);
    ```

## 子查询优化 {#subquery-optimization}

GPORCA 能更高效地处理子查询。子查询是嵌套在外层查询块中的查询，例如下面 `WHERE` 子句中的 `SELECT`：

```sql
SELECT * FROM part
  WHERE price > (SELECT avg(price) FROM part);
```

GPORCA 还会优化引用外层查询列的相关子查询（CSQ）。例如，以下语句中的内层和外层查询都使用了 `price` 列：

```sql
SELECT * FROM part p1 WHERE price > (SELECT avg(price) FROM part p2 WHERE p2.brand = p1.brand);
```

GPORCA 可以为以下类型的子查询生成更高效的计划：

- `SELECT` 列表中的相关子查询：

    ```sql
    SELECT *,
    (SELECT min(price) FROM part p2 WHERE p1.brand = p2.brand)
    AS foo
    FROM part p1;
    ```

- `OR` 条件中的相关子查询：

    ```sql
    SELECT FROM part p1 WHERE p_size > 40 OR 
        p_retailprice > 
        (SELECT avg(p_retailprice) 
            FROM part p2 
            WHERE p2.p_brand = p1.p_brand)
    ```

- 包含跨层关联的嵌套子查询：

    ```sql
    SELECT * FROM part p1 WHERE p1.p_partkey 
    IN (SELECT p_partkey FROM part p2 WHERE p2.p_retailprice = 
        (SELECT min(p_retailprice)
            FROM part p3 
            WHERE p3.p_brand = p1.p_brand)
    );
    ```

    > [!NOTE]
    > PostgreSQL 规划器不支持包含跨层关联的嵌套相关子查询。

- 包含聚合和不等式的相关子查询：

    ```sql
    SELECT * FROM part p1 WHERE p1.p_retailprice =
    (SELECT min(p_retailprice) FROM part p2 WHERE p2.p_brand <> p1.p_brand);
    ```

- 预期返回单行的相关子查询：

    ```sql
    SELECT p_partkey, 
    (SELECT p_retailprice FROM part p2 WHERE p2.p_brand = p1.p_brand )
    FROM part p1;
    ```

## 公共表表达式（CTE）优化 {#common-table-expression-cte-optimization}

GPORCA 能高效处理包含 `WITH` 子句的查询。`WITH` 子句也称公共表表达式（CTE），定义了查询中使用的临时逻辑表。以下是包含 CTE 的查询示例：

```sql
WITH v AS (SELECT a, sum(b) as s FROM T WHERE c < 10 GROUP BY a)
  SELECT * FROM  v AS v1, v AS v2
  WHERE v1.a <> v2.a AND v1.s < v2.s;
```

作为查询优化的一部分，GPORCA 支持将谓词下推到 CTE 中。在下例中，等值谓词被下推到 CTE：

```sql
WITH v AS (SELECT a, sum(b) as s FROM T GROUP BY a)
  SELECT *
  FROM v as v1, v as v2, v as v3
  WHERE v1.a < v2.a
    AND v1.s < v3.s
    AND v1.a = 10
    AND v2.a = 20
    AND v3.a = 30;
```

GPORCA 支持以下类型的 CTE：

- 定义多个逻辑表的 CTE。下例中的 CTE 定义了两张逻辑表：

    ```sql
    WITH cte1 AS (SELECT a, sum(b) as s FROM T 
                   WHERE c < 10 GROUP BY a),
          cte2 AS (SELECT a, s FROM cte1 WHERE s > 1000)
      SELECT *
      FROM cte1 as v1, cte2 as v2, cte2 as v3
      WHERE v1.a < v2.a AND v1.s < v3.s;
    ```

## DML 操作优化 {#dml-operation-optimization}

GPORCA 还增强了 `INSERT`、`UPDATE`、`DELETE` 等 DML 操作：

- DML 操作在执行计划中表现为普通算子节点。

    - 它们可以出现在计划的任意位置（目前限于顶层切片）。
    - 它们可以有下游节点（消费者）。

- `UPDATE` 操作通过 `Split` 算子实现，支持以下功能：

    - 更新分布键列。
    - 更新分区键列。以下示例展示包含 `Split` 算子的计划：

    ```sql
    QUERY PLAN
    --------------------------------------------------------------
    Update  (cost=0.00..5.46 rows=1 width=1)
       ->  Redistribute Motion 2:2  (slice1; segments: 2)
             Hash Key: a
             ->  Result  (cost=0.00..3.23 rows=1 width=48)
                   ->  Split  (cost=0.00..2.13 rows=1 width=40)
                         ->  Result  (cost=0.00..1.05 rows=1 width=40)
                               ->  Seq Scan on dmltest
    ```

## 其他优化能力 {#other-optimization-capabilities}

GPORCA 还包含以下优化功能：

- 改进连接顺序选择。
- 支持调整连接和聚合操作的顺序。
- 优化排序顺序。
- 优化时考虑数据倾斜估算。
