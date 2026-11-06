---
title: "查询计划提示"
description: "Apache Cloudberry 使用两种查询优化器：基于 Postgres 的优化器和 GPORCA。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/query-hints.md"
---

各优化器针对不同类型的工作负载进行了调优：

- 基于 Postgres 的优化器：适用于事务型工作负载。
- GPORCA：适用于分析型和事务分析混合型工作负载。

处理查询时，优化器会探索由等价执行计划构成的庞大搜索空间。它利用表统计信息和基数估算模型估算各操作的行数，再据此为每个计划计算代价，并选择代价最低的计划作为最终执行计划。

查询计划提示（也称优化器提示）是用户提供的指令，用于影响优化器的执行策略。提示允许用户覆盖优化器的默认行为，解决行数估算不准确、扫描方式不佳、连接类型不当或连接顺序低效等问题。本文介绍各类提示及其适用场景。

> [!NOTE]
> Apache Cloudberry 目前不支持控制 Motion 算子的提示。

## 简单示例 {#quick-example}

> [!NOTE]
> 要启用查询计划提示，必须先在 psql 会话中加载相关模块：
>
> ```sql
> LOAD 'pg_hint_plan';
> ```
>
> 也可以配置数据库或用户，使其自动加载该模块：
>
> ```sql
> ALTER DATABASE a_database SET session_preload_libraries='pg_hint_plan';
> ALTER USER a_user SET session_preload_libraries='pg_hint_plan';
> ```

```sql
CREATE TABLE foo(a int);
CREATE INDEX ON foo(a);
INSERT INTO foo SELECT i FROM generate_series(1, 100000)i;

LOAD 'pg_hint_plan';
SHOW pg_hint_plan.enable_hint;
pg_hint_plan.enable_hint
--------------------------
on
(1 row)

EXPLAIN SELECT count(*) FROM foo WHERE a > 6;
                                    QUERY PLAN
--------------------------------------------------------------------------------------
Finalize Aggregate  (cost=537.05..537.06 rows=1 width=8)
   ->  Gather Motion 3:1  (slice1; segments: 3)  (cost=536.99..537.04 rows=3 width=8)
         ->  Partial Aggregate  (cost=536.99..537.00 rows=1 width=8)
               ->  Seq Scan on foo  (cost=0.00..453.67 rows=33330 width=0)
                     Filter: (a > 6)
Optimizer: Postgres-based planner
(6 rows)

/*+ IndexScan(foo foo_a_idx) */
EXPLAIN SELECT count(*) FROM foo WHERE a > 6;
                                       QUERY PLAN
---------------------------------------------------------------------------------------------
Finalize Aggregate  (cost=809.00..809.01 rows=1 width=8)
   ->  Gather Motion 3:1  (slice1; segments: 3)  (cost=808.94..808.99 rows=3 width=8)
         ->  Partial Aggregate  (cost=808.94..808.95 rows=1 width=8)
               ->  Index Scan using foo_a_idx on foo  (cost=0.17..725.61 rows=33330 width=0)
                     Index Cond: (a > 6)
Optimizer: Postgres-based planner
(6 rows)
```

还可以同时指定多个提示，例如同时控制扫描方式和行数估算：

```sql
/*+ IndexScan(t1 my_index) Rows(t1 t2 #1000) */
SELECT * FROM t1 JOIN t2 ON t1.a = t2.a WHERE t1.a < 100;
```

## 基数提示 {#cardinality-hints}

优化器对连接操作的行数估算不准确时，可能选择低效的计划，例如使用 Broadcast 而不是 Redistribute，或者错误地优先选择归并连接而非哈希连接。基数提示允许调整特定操作的估算行数，在统计信息缺失或过时的情况下尤其有用。

示例：

```sql
/*+ Rows(t1 t2 t3 #42) */ SELECT * FROM t1, t2, t3;  -- set row estimate to 42
/*+ Rows(t1 t2 t3 +42) */ SELECT * FROM t1, t2, t3; -- increase original estimate by 42
/*+ Rows(t1 t2 t3 -42) */ SELECT * FROM t1, t2, t3; -- decrease original estimate by 42
/*+ Rows(t1 t2 t3 *42) */ SELECT * FROM t1, t2, t3; -- multiply original estimate by 42
```

> [!NOTE]
> 基数提示目前仅对 ORCA 优化器有效，Postgres 优化器不识别此类提示。

## 表访问提示 {#table-access-hints}

由于统计信息不准确或代价估算有偏差，优化器可能选择不理想的扫描策略。与全局配置参数（GUC）相比，表访问提示可以更精细地控制查询中每张表的扫描方式。可以选择是否使用索引，或强制使用指定索引。

示例：

```sql
/*+ SeqScan(t1) */ SELECT * FROM t1 WHERE t1.a > 42;  -- force sequential scan
/*+ IndexScan(t1 my_index) */ SELECT * FROM t1 WHERE t1.a > 42;  -- force index scan
/*+ IndexOnlyScan(t1) */ SELECT * FROM t1 WHERE t1.a > 42;  -- force index-only scan
/*+ BitmapScan(t1 my_bitmap_index) */ SELECT * FROM t1 WHERE t1.a > 42;  -- force bitmap index scan
```

> [!NOTE]
> 自 v2.0.0 起，ORCA 优化器支持 `IndexScan`、`SeqScan` 等扫描方式提示，并据此生成计划。此功能同时依赖 ORCA 优化器和 `pg_hint_plan` 扩展。

## 连接类型提示 {#join-type-hints}

使用哈希连接时，部分中间结果可能溢出到磁盘，影响性能。如果用户知道某个查询使用嵌套循环连接更有利，就可以通过提示显式指定连接类型及内外表顺序。

示例：

```sql
/*+ HashJoin(t1 t2) */ SELECT * FROM t1, t2;
/*+ NestLoop(t1 t2) */ SELECT * FROM t1, t2;
/*+ MergeJoin(t1 t2) */ SELECT * FROM t1 FULL JOIN t2 ON t1.a = t2.a;
```

## 连接顺序提示 {#join-order-hints}

优化器因统计信息缺失或估算不准确而选择了不理想的连接顺序时，可以使用 `Leading(...)` 提示指定表之间的连接顺序。

示例：

```sql
/*+ Leading(t1 t2 t3) */ SELECT * FROM t1, t2, t3;
/*+ Leading(t1 (t3 t2)) */ SELECT * FROM t1, t2, t3;
```

还可以使用 `Leading(...)` 控制包含 `LEFT OUTER JOIN` 或 `RIGHT OUTER JOIN` 的查询的连接顺序，但需遵循以下约束：

- 提示中的连接顺序必须与原 SQL 的连接结构一致。例如：

    ```sql
    SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a;
    ```

    提示 `/*+ Leading((t1 t2)) */` 保留左连接。提示 `/*+ Leading((t2 t1)) */` 将其转换为右连接，两者语义等价，但生成的计划不同。

- 对于嵌套外连接，必须按相同的语义嵌套顺序指定提示。

- 非等值连接条件（例如 `t1.a > t2.a`）不支持改变连接方向，否则会破坏查询语义。

    示例：以下提示要求优化器先将 `t2` 与 `t1` 连接，再将结果与 `t3` 连接：

    ```sql
    /*+ Leading((t3 (t2 t1))) */
    SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a LEFT JOIN t3 ON t2.b = t3.b;
    ```

## 支持范围与限制 {#supported-scope-and-limitations}

- 查询计划提示依赖 `pg_hint_plan` 扩展，必须显式加载该扩展。
- 尚不支持控制数据重分布策略的提示。

## 查询计划提示的最佳实践 {#best-practices-for-using-query-plan-hints}

使用提示时，请遵循以下最佳实践：

- 着重解决具体问题，例如行数估算不准确、扫描方式不佳、连接类型不当或连接顺序低效。
- 部署前充分测试，确保提示能提高性能并减少资源使用量。
- 将提示作为临时措施。提示用于短期调优，应随着数据变化进行审查和调整。
- 避免与 GUC 设置冲突。如果 GUC 禁用了提示试图启用的功能（例如 `IndexScan`），该提示会被忽略。请确保全局设置与提示一致。

> [!NOTE]
> `pg_hint_plan` 允许直接在提示中加入 GUC 设置。例如：
>
> ```sql
> /*+ SeqScan(mytable) optimizer_enable_seqscan=on *//*Set(enable_indexscan off)*/
> EXPLAIN (COSTS false) SELECT * FROM t1, t2 WHERE t1.id = t2.id;
> ```
