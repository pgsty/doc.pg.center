---
title: "使用 RuntimeFilter 优化连接查询"
description: "对大型表执行连接查询时，Apache Cloudberry 的 SQL 优化器经常使用 HashJoin 算子。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-runtimefilter-to-optimize-queries.md"
---

HashJoin 根据连接键构建 hash 表并匹配连接键，可能产生内存访问瓶颈和磁盘瓶颈。RuntimeFilter 是一种在 HashJoin 操作期间实时生成过滤器的优化技术，可以在执行 HashJoin 前预先过滤数据，加速 HashJoin。在某些场景中，RuntimeFilter 优化能使执行效率翻倍。

HashJoin 常用于将较小的表与较大的表连接。在 Apache Cloudberry 中，执行 HashJoin 时通常根据待连接的较小表构建 hash 表，再遍历较大表中的元组，在 hash 表中查找匹配项以完成连接。用于构建 hash 表的较小表称为内表，另一个用于遍历匹配的表称为外表。

执行 HashJoin 算子的主要瓶颈包括：

- 内存访问：对于外表中的每个元组，都需要在 hash 表中查找匹配元组，涉及一次或多次内存访问。
- 磁盘 I/O：如果内表过大，无法放入内存，就必须利用磁盘存储分批处理，产生大量磁盘 I/O。

启用 RuntimeFilter 优化后，Apache Cloudberry 会在构建 hash 表的同时构建 RuntimeFilter，即在执行 HashJoin 前过滤较大表中的元组。RuntimeFilter 通过 Bloom 过滤器实现，占用的内存远小于 hash 表。当 Bloom 过滤器能够完整放入 L3 缓存时，其过滤效率是 HashJoin 的两倍，可以大幅降低内存访问代价。

此优化根据 HashJoin 连接条件的过滤率和内表大小，决定是否生成 RuntimeFilter 算子。如果实际执行中的数据量与估算结果偏差过大，Apache Cloudberry 也会及时停止使用 RuntimeFilter。

## 适用场景 {#applicable-scenarios}

如果场景满足以下全部条件，可以考虑在 HashJoin 操作中使用 RuntimeFilter 优化：

- 单个 Segment 中的内表规模不超过 1600 万行。
- 原 HashJoin 连接键的选择率低于 60%，即满足哈希连接条件的结果集少于外表的 60%；也可以理解为过滤率超过 40%。

在上述场景中，Apache Cloudberry 通过 RuntimeFilter 构建的 Bloom 过滤器大小不超过 2 MB，可以完整放入 L3 缓存，以极小的开销过滤掉外表中 40% 的元组，从而产生正面效果。在某些场景中，如果 HashJoin 连接键的选择率低于 10%，RuntimeFilter 优化能使执行效率翻倍。

## 限制 {#limitations}

**目前，只有内表估算行数少于 1600 万时，才支持 RuntimeFilter。**

这一限制是为了防止 Bloom 过滤器占用过多内存，导致执行速度下降或过滤效率降低。未来的更新可能支持在内表极大的场景中使用 RuntimeFilter，以避免分批处理带来的磁盘 I/O 代价。

## 使用示例 {#usage-example}

以下示例展示 HashJoin 算法如何受益于 RuntimeFilter：

此优化仅在 PostgreSQL 优化器中有效。因此，启用 RuntimeFilter 前，需要先禁用 GPORCA 优化器，并手动启用 GUC 参数 `gp_enable_runtime_filter`。

```sql
-- Preparation
SET optimizer TO off; -- Disables the GPORCA optimizer to use the PostgreSQL optimizer.
SET gp_enable_runtime_filter TO on; -- Enables the RuntimeFilter optimization.

-- Creates the test table.
DROP TABLE IF EXISTS fact, dim;
CREATE TABLE fact (fid int, did int, val int);
CREATE TABLE dim (did int, proj_id int, filter_val int);

-- Generates test data, and 80% of fact.did overlaps with dim.did.
INSERT INTO fact SELECT i, i % 8000 + 1, i FROM generate_series(1, 100000) s(i);
INSERT INTO dim SELECT i, i % 10, i FROM generate_series(1, 10000) s(i);
ANALYZE fact, dim;

-- Checks the execution plan.
EXPLAIN (COSTS OFF) SELECT COUNT(*) FROM fact, dim
    WHERE fact.did = dim.did AND proj_id < 2;
                                QUERY PLAN
---------------------------------------------------------------------------
 Finalize Aggregate
   ->  Gather Motion 3:1  (slice1; segments: 3)
         ->  Partial Aggregate
               ->  Hash Join
                     Hash Cond: (fact.did = dim.did)
                     ->  RuntimeFilter
                           ->  Seq Scan on fact
                     ->  Hash
                           ->  Broadcast Motion 3:3  (slice2; segments: 3)
                                 ->  Seq Scan on dim
                                       Filter: (proj_id < 2)
 Optimizer: Postgres query optimizer
(12 rows)
```

在上述执行计划中可以看到 RuntimeFilter 算子。如果希望输出更多执行信息，请使用 `EXPLAIN ANALYZE`。

```sql
->  RuntimeFilter (actual time=0.047..5.976 rows=6682 loops=1)
       Bloom Bits: 1048576
       Extra Text: (seg1)   Inner Processed: 2000, Flase Positive Rate: 0.000000
```

## 优化效果示例 {#example-of-optimization-effect}

使用“使用示例”中的表，将 `fact` 与 `dim` 连接，条件为项目 ID 小于 `2`，并以 `did` 列作为连接键，可以从执行时间中看出 RuntimeFilter 的效果：

```sql
-- Without RuntimeFilter
EXPLAIN ANALYZE SELECT COUNT(*) FROM fact, dim
    WHERE fact.did = dim.did AND proj_id < 2;

Execution Time: 35956.436 ms

-- With RuntimeFilter
SET gp_enable_runtime_filter TO on;
EXPLAIN ANALYZE SELECT COUNT(*) FROM fact, dim
    WHERE fact.did = dim.did AND proj_id < 2;

Execution Time: 18276.112 ms
```

以上是部分 `EXPLAIN ANALYZE` 结果。完整结果中，事实表扫描产生 1 亿个元组，经 RuntimeFilter 过滤后剩下 2200 万个，再经 HashJoin 后恰好剩下预期的 2000 万个。预过滤效果明显，耗时减少了约 50%。
