---
title: "使用聚合下推加速查询执行"
linkTitle: "使用聚合下推加速查询执行"
description: "聚合下推是一种将聚合操作移近数据源的优化技术。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-aggre-pushdown-to-speed-up-queries.md"
---

Apache Cloudberry 支持下推聚合操作，即在连接算子之前执行聚合算子。

在[适用场景](#applicable-scenarios)中，聚合下推可以大幅缩小连接或聚合算子的输入集，从而提高性能。

> [!TIP]
> - 在原生 PostgreSQL 内核的优化逻辑中，每个查询的聚合操作总是在全部连接操作完成后执行（不包括子查询）。因此，Apache Cloudberry 引入聚合下推，允许在适用场景中提前执行聚合操作。
> - 要判断优化器选择的执行计划是否应用了聚合下推，可以查看计划树中聚合与连接的位置关系。如果计划先执行 `Partial Aggregation`，再执行 `Join`，最后执行 `Final Aggregation`，就表明优化器应用了聚合下推。

## 使用示例 {#usage-example}

使用聚合下推优化前，需要手动启用 GUC 参数 `gp_enable_agg_pushdown`。

此外，需要手动设置 `optimizer=off`，禁用 GPORCA 优化器，因为此优化目前仅适用于 PostgreSQL 优化器。

以下示例演示聚合下推优化的用法。

```sql
-- Creates tables t1 and t2.
CREATE TABLE t1(id INT, val1 INT);
CREATE TABLE t2(id INT, val2 INT);

SET OPTIMIZER=OFF; -- Disables the GPORCA optimizer.
SET gp_enable_agg_pushdown=ON; -- Enables the GUC parameter.

-- Executes a query with aggregation and join operations.
EXPLAIN (COSTS OFF) SELECT id, SUM(val1) FROM t1 NATURAL JOIN t2 GROUP BY id;
                     QUERY PLAN
-----------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)
   ->  Finalize GroupAggregate
         Group Key: t1.id
         ->  Sort
               Sort Key: t1.id
               ->  Hash Join
                     Hash Cond: (t2.id = t1.id)
                     ->  Seq Scan on t2
                     ->  Hash
                           ->  Partial HashAggregate
                                 Group Key: t1.id
                                 ->  Seq Scan on t1
Optimizer: Postgres query optimizer
(13 rows)
```

从上述示例的执行计划可见，Apache Cloudberry 在执行 HashJoin 前，先按 `id` 列对表 `t1` 执行聚合。该聚合不会影响语句结果的正确性，并且有望减少进入 HashJoin 的数据量，从而提高语句执行效率。

## 适用场景 {#applicable-scenarios}

在以下场景中，使用聚合下推预期可以明显提高查询性能。

### 适用场景 1 {#applicable-scenario-1}

一张表中的每条记录对应另一张表中的多条记录，需要连接两张表并进行分组聚合。

例如，通过订单表（`order_tbl`）和订单明细表（`order_line_tbl`）汇总每个订单中商品的价格，也就是计算每个订单的总金额 `SUM(price)`：

```sql
SELECT o.order_id, SUM(price)
  FROM order_tbl o, order_line_tbl ol
  WHERE o.order_id = ol.order_id
  GROUP BY o.order_id;
```

- 原生 PostgreSQL 优化器的执行方式：只能在连接表之后执行聚合。由于 `order_line_tbl` 中的每件商品都对应 `order_tbl` 中的一个订单，Join 算子不会过滤掉任何数据。
- Apache Cloudberry 的执行方式：假设每个订单平均包含 10 件商品，聚合后的数据量预期会减少到原来的十分之一。启用聚合下推后，数据库先按 `order_id` 聚合 `order_line_tbl` 中的数据，使进入 Join 算子的数据量减少到原来的十分之一，显著降低 Join 算子的代价。相应的执行计划如下：

```sql
EXPLAIN SELECT o.order_id, SUM(price)
  FROM order_tbl o, order_line_tbl ol
  WHERE o.order_id = ol.order_id
  GROUP BY o.order_id;
                                          QUERY PLAN
-----------------------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=712.89..879.56 rows=10000 width=12)
   ->  Finalize HashAggregate  (cost=712.89..746.23 rows=3333 width=12)
         Group Key: o.order_id
         ->  Hash Join  (cost=617.00..696.23 rows=3333 width=12)
               Hash Cond: (ol.order_id = o.order_id)
               ->  Partial HashAggregate  (cost=538.00..571.38 rows=3338 width=12)
                     Group Key: ol.order_id
                     ->  Seq Scan on order_line_tbl ol  (cost=0.00..371.33 rows=33333 width=8)
               ->  Hash  (cost=37.33..37.33 rows=3333 width=4)
                     ->  Seq Scan on order_tbl o  (cost=0.00..37.33 rows=3333 width=4)
 Optimizer: Postgres query optimizer
```

类似场景还包括：连接项目表（`project`）与实验表（`experiment`），计算每个 `project` 在过去一年中的实验总成本。相应的参考 SQL 语句如下：

```sql
SELECT proj_name, sum(cost)
    FROM experiment e, project p
    WHERE e.e_pid = p.p_pid AND e.start_time > now() - interval '1 year'
    GROUP BY proj_name;
```

对于此查询，启用聚合下推后，Apache Cloudberry 会先按 `e_pid` 列对实验表预聚合，将同一项目的信息汇总在一起。

不过，如果查询还在项目表上应用了大量过滤条件，连接的选择性可能很强，导致执行低效。因此，聚合下推可能不适合这种情况。

### 适用场景 2 {#applicable-scenario-2}

查询中的 Join 算子会大幅增大结果集，之后还需要分组计算。

例如，连接 `person_1` 表和 `person_2` 表，计算两个表中都出现的每个姓名可以形成多少个不同的配对。SQL 查询如下：

```sql
SELECT p1.name, COUNT(p1.name) FROM person_1 p1, person_2 p2 WHERE p1.name = p2.name GROUP BY p1.name;
```

本例中，如果某个 `name` 在 `p1` 表出现 X 次，在 `p2` 表出现 Y 次，那么它在最终结果中就会出现 X*Y 次。如果大量数据都符合这种情况，连接后的结果集可能变得非常大。

在上述示例中，如果提前将聚合操作下推到 `p1` 或 `p2` 一侧，则该侧聚合后每个姓名最多出现一次。这能有效减少 Join 算子的工作量，以及后续聚合算子的输入集大小。相应的执行计划如下：

```sql
EXPLAIN SELECT p1.name, COUNT(p1.name) FROM person_1 p1, person_2 p2 WHERE p1.name = p2.name GROUP BY p1.name;
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=1758.62..1925.23 rows=9997 width=12)
   ->  Finalize HashAggregate  (cost=1758.62..1791.94 rows=3332 width=12)
         Group Key: p1.name
         ->  Hash Join  (cost=762.93..1592.17 rows=33290 width=12)
               Hash Cond: (p2.name = p1.name)
               ->  Seq Scan on p2  (cost=0.00..371.33 rows=33333 width=4)
               ->  Hash  (cost=637.97..637.97 rows=9997 width=12)
                     ->  Partial HashAggregate  (cost=538.00..637.97 rows=9997 width=12)
                           Group Key: p1.name
                           ->  Seq Scan on p1  (cost=0.00..371.33 rows=33333 width=4)
 Optimizer: Postgres query optimizer
(11 rows)
```

## 不适用场景 {#unsuitable-scenarios}

在以下场景中，聚合下推不太可能提升性能，不建议启用。

### 不适用场景 1 {#unsuitable-scenario-1}

聚合前后数据量变化不大。

与[适用场景 1](#applicable-scenario-1) 和[适用场景 2](#applicable-scenario-2) 相反，如果提前聚合不会明显改变数据量，也无法缩小后续计算的输入集，建议先执行 Join 算子，避免不必要的开销。

### 不适用场景 2 {#unsuitable-scenario-2}

如果连接键与分组键不同，下推聚合会改变下推后使用的分组键。此时，改写了分组键的聚合下推可能无法减少数据量，导致下推后的聚合性能不佳：

```sql
SELECT t1.value, COUNT(*) FROM t1, t2 WHERE t1.key = t2.key GROUP BY t1.value;
```

对于上述查询示例，直接将聚合下推到 `t1` 一侧会产生错误结果，其细节类似于[不适用场景 1](#unsuitable-scenario-1) 中的限制。为确保结果正确，实际下推聚合所用的等价分组键变为 `GROUP BY t1.key, t1.value`。

这种情况下，如果 `t1` 表中的 key 与 value 完全不相关，每组可能只有一个元组，聚合下推就不会产生任何正面效果。但如果 key 与 value 高度相关，或者相同的 key 始终对应相同的 value，则分组效果不受影响。

在上述示例中，原查询显然按 `t1.value` 分组。但聚合下推后，分组键变为 `t1.key, t1.value`；如果 key 与 value 相关性较弱，聚合中的分组效果就会下降。

## 限制 {#limitations}

本节介绍聚合下推功能的部分限制，包括逻辑上无法应用此优化的情况，以及工程实现尚不支持的情况。

### 限制 1 {#limitation-1}

如果连接及后续计算过程中对 `GROUP BY` 子句之外的列进行过滤，就不能应用聚合下推。考虑以下 SQL 查询：

```sql
SELECT id, SUM(val) FROM t1, t2 WHERE t1.id = t2.id AND t1.val > t2.val GROUP BY id;
```

在上述示例中，假设表 `t1` 中有两个元组 A 和 B，其 `id` 值都为 `100`；表 `t2` 中有一个元组 C，其 `id` 值也为 `100`。

将 AB 与 C 连接时，虽然 A 和 B 的 `id` 相同，但不能保证它们同时满足或同时不满足过滤条件 `AB.val > C.val`。此时，按 `id` 预先计算 `val` 的和，必然会合并 A 和 B 的 `val`。但两者未必同时通过或同时未通过过滤，因此会产生错误结果。

相比之下，以下查询与之类似，却适合聚合下推：

```sql
SELECT id, SUM(val) FROM t1, t2 WHERE t1.id = t2.id AND t1.id < t2.id_thre GROUP BY id;
```

本例仍考虑前例中的 ABC 元组。由于额外的过滤条件只使用了 `t1` 的 `id` 列，具有相同 `id` 的 AB 两个元组与给定的 C 元组连接时，要么都通过过滤，要么都不通过。因此，可以预先聚合 AB 元组的 `val` 之和。

### 限制 2 {#limitation-2}

不支持在 Join 的两侧同时下推聚合。考虑以下 SQL 查询：

```sql
SELECT id, SUM(val) FROM t1, t2 WHERE t1.id = t2.id GROUP BY id;
```

可以将语句改写为以下等价形式：

```sql
SELECT id, sum1 * cnt2 FROM
    (SELECT id, SUM(val) FROM t1 GROUP BY id) AT1(id, sum1),
    (SELECT id, COUNT(*) FROM t2 GROUP BY id) AT2(id, cnt2)
WHERE AT1.id = AT2.id GROUP BY id;
```

本例将聚合操作下推到连接两侧。对于 `t1` 表中 `id` 为 100 的所有元组，Apache Cloudberry 先聚合其 `val`，得到对应的 `sum1`。

实际连接时，`t2` 表中每个 `id` 为 100 的元组都会与 `sum1` 对应的元组连接，生成相应元组。这意味着 `t2` 中每出现一个 `id` 为 100 的元组，最终求和中就会出现一次 `sum1`。因此，Apache Cloudberry 可以预聚合 `t2`，将 `id` 为 100 的元组总数计算为 `cnt2`，再通过 `sum1 * cnt2` 计算最终结果。

这种场景涉及较复杂的语句和表达式改写，目前 Apache Cloudberry 尚不支持。
