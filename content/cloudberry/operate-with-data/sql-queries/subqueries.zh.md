---
title: "子查询"
description: "子查询允许将一个查询嵌入另一个查询，从而在定义查询时实现动态和条件逻辑。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/subqueries.md"
---

子查询可用于筛选、计算中间值或表达相关关系。

本文区分标量子查询和相关子查询，并说明何时以及如何有效地使用它们。

标量子查询是一个放在括号中的 `SELECT` 查询，它恰好返回一行一列。不要将返回多行或多列的 `SELECT` 查询用作标量子查询。该查询会运行，并在外层值表达式中使用返回的值。相关标量子查询包含对外层查询块的引用。

## 相关子查询 {#correlated-subqueries}

相关子查询（CSQ）是一个 `SELECT` 查询，其 `WHERE` 子句或目标列表包含对外层父子句的引用。CSQ 可以用另一个查询的结果高效地表达查询结果。Apache Cloudberry 支持相关子查询，以便兼容许多现有应用。CSQ 根据返回一行还是多行，可以是标量子查询或表子查询。Apache Cloudberry 不支持跨层级关联的相关子查询。

## 相关子查询示例 {#correlated-subquery-examples}

### 示例 1——标量相关子查询 {#example-1--scalar-correlated-subquery}

```sql
SELECT * FROM t1 WHERE t1.x 
            > (SELECT MAX(t2.x) FROM t2 WHERE t2.y = t1.y);
```

### 示例 2——相关 EXISTS 子查询 {#example-2--correlated-exists-subquery}

```sql
SELECT * FROM t1 WHERE 
EXISTS (SELECT 1 FROM t2 WHERE t2.x = t1.x);
```

Apache Cloudberry 使用以下方法之一运行 CSQ：

- 将 CSQ 展开为连接操作——这种方法效率最高，Apache Cloudberry 运行大多数 CSQ（包括来自 TPC-H 基准测试的查询）时都采用这种方法。
- 对外层查询的每一行运行 CSQ——这种方法效率相对较低，Apache Cloudberry 运行包含 `SELECT` 列表中的 CSQ 或由 `OR` 条件连接的查询时采用这种方法。

以下示例说明如何重写其中一些类型的查询，以提高性能。

### 示例 3——选择列表中的 CSQ {#example-3---csq-in-the-select-list}

*原始查询*

```sql
SELECT T1.a,
      (SELECT COUNT(DISTINCT T2.z) FROM t2 WHERE t1.x = t2.y) dt2 
FROM t1;
```

重写此查询：先对 `t1` 执行内连接，然后再次对 `t1` 执行左连接。此重写仅适用于相关条件中的等值连接。

*重写后的查询*

```sql
SELECT t1.a, dt2 FROM t1 
       LEFT JOIN 
        (SELECT t2.y AS csq_y, COUNT(DISTINCT t2.z) AS dt2 
              FROM t1, t2 WHERE t1.x = t2.y 
              GROUP BY t1.x) 
       ON (t1.x = csq_y);
```

### 示例 4——由 OR 子句连接的 CSQ {#example-4---csqs-connected-by-or-clauses}

*原始查询*

```sql
SELECT * FROM t1 
WHERE 
x > (SELECT COUNT(*) FROM t2 WHERE t1.x = t2.x) 
OR x < (SELECT COUNT(*) FROM t3 WHERE t1.y = t3.y)
```

重写此查询，将其按 `OR` 条件拆分为两部分，并使用 union 连接。

*重写后的查询*

```sql
SELECT * FROM t1 
WHERE x > (SELECT count(*) FROM t2 WHERE t1.x = t2.x) 
UNION 
SELECT * FROM t1 
WHERE x < (SELECT count(*) FROM t3 WHERE t1.y = t3.y)
```

要查看查询计划，请使用 `EXPLAIN SELECT` 或 `EXPLAIN ANALYZE SELECT`。查询计划中的子计划节点表明查询将对外层查询的每一行运行，因此可以考虑重写该查询。有关这些语句的更多信息，请参见[分析查询性能](/cloudberry/performance/optimize-queries/analyze-query-performance/)。
