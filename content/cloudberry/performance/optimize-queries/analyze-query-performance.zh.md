---
title: "分析查询性能"
description: "检查性能不佳的查询的执行计划，识别可能的性能调优机会。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/analyze-query-performance.md"
---

Apache Cloudberry 为每个查询制定查询计划。选择与查询和数据结构相匹配的计划，是获得良好性能的必要条件。查询计划定义了 Apache Cloudberry 如何在并行执行环境中运行查询。

查询优化器利用数据库维护的数据统计信息，选择代价尽可能低的查询计划。代价以磁盘 I/O 衡量，单位为磁盘页读取次数，目标是尽可能降低计划的总执行代价。

使用 `EXPLAIN` 命令查看给定查询的计划。`EXPLAIN` 显示查询优化器对查询计划的代价估算。例如：

```sql
EXPLAIN SELECT * FROM names WHERE id=22;
```

`EXPLAIN ANALYZE` 不仅显示计划，还会执行语句，可用于判断优化器的估算与实际情况有多接近。例如：

```sql
EXPLAIN ANALYZE SELECT * FROM names WHERE id=22;
```

> [!NOTE]
> 在 Apache Cloudberry 中，默认的 GPORCA 优化器与基于 Postgres 的规划器共存。GPORCA 生成的 EXPLAIN 输出与基于 Postgres 的规划器生成的输出不同。
>
> 默认情况下，只要能够使用，Apache Cloudberry 就会用 GPORCA 为查询生成执行计划。
>
> `EXPLAIN ANALYZE` 命令使用 GPORCA 时，`EXPLAIN` 计划只显示被消除的分区数量，不显示扫描了哪些分区。要在 Segment 日志中显示被扫描分区的名称，请将服务器配置参数 `gp_log_dynamic_partition_pruning` 设为 `on`。以下 `SET` 命令示例启用该参数。
>
> ```sql
> SET gp_log_dynamic_partition_pruning = on;
> ```
>
> 有关 GPORCA 的信息，请参见 [GPORCA 概述](/cloudberry/performance/optimize-queries/use-orca/use-orca-overview/)。

## 解读 EXPLAIN 输出 {#read-explain-output}

查询计划是一棵节点树。计划中的每个节点代表一项操作，例如表扫描、连接、聚合或排序。

从下往上解读计划：每个节点将行传给其正上方的节点。计划底部通常是表扫描操作，包括顺序扫描、索引扫描或位图索引扫描。如果查询需要对行执行连接、聚合、排序或其他操作，扫描节点上方还会有执行这些操作的节点。最顶层的计划节点通常是 Apache Cloudberry 的 Motion 节点：重分布、显式重分布、广播或汇集 Motion。这些操作在查询处理期间于 Segment 实例之间移动行。

`EXPLAIN` 输出为计划树中的每个节点显示一行，包含节点的基本类型及该计划节点的以下执行代价估算：

- **cost**——以磁盘页读取次数为单位，1.0 表示一次顺序磁盘页读取。第一个估算值是取得第一行的启动代价，第二个是取得所有行的总代价。总代价假定会检索所有行，但实际情况并非总是如此；例如，查询使用 `LIMIT` 时就不会检索所有行。

    > [!NOTE]
    > GPORCA 与基于 Postgres 的规划器生成的代价值不能直接比较。两个优化器采用不同的代价模型和算法来计算执行计划的代价。不能、也不应通过比较两个优化器的代价值得出任何结论。

    此外，任一优化器生成的代价，都只适用于在同一查询、同一组统计信息下比较不同候选计划。即使使用同一个优化器，不同查询也可能生成代价不同的计划。

    因此，代价本质上是特定优化器内部使用的数值，不应仅凭 `EXPLAIN` 计划显示的代价值作出推断。

- **rows**——该计划节点输出的总行数。这个数通常小于节点处理或扫描的行数，反映了对 `WHERE` 子句条件选择性的估算。理想情况下，顶层节点的估算行数应接近查询实际返回、更新或删除的行数。
- **width**——该计划节点输出的所有行的总字节数。

请注意以下几点：

- 节点的代价包含其子节点的代价。最顶层计划节点的代价是整个计划估算的总执行代价，也是优化器试图尽可能降低的数值。
- 代价仅反映查询优化器所考虑的计划执行因素。例如，它不包含向客户端传输结果行所花费的时间。

### EXPLAIN 示例 {#explain-example}

以下示例介绍如何解读查询的 `EXPLAIN` 计划：

```sql
EXPLAIN SELECT * FROM names WHERE name = 'Joelle';
                     QUERY PLAN
------------------------------------------------------------
Gather Motion 2:1 (slice1) (cost=0.00..20.88 rows=1 width=13)

   -> Seq Scan on 'names' (cost=0.00..20.88 rows=1 width=13)
         Filter: name::text ~~ 'Joelle'::text
```

从下往上解读计划。首先，查询优化器顺序扫描 *names* 表。注意，`WHERE` 子句以*过滤*条件的形式应用。这意味着扫描操作会逐行检查条件，只输出满足条件的行。

扫描结果会传给*汇集 Motion* 操作。在 Apache Cloudberry 中，汇集 Motion 是指 Segment 将行发送给 Coordinator。本例中，两个 Segment 实例向一个 Coordinator 实例发送数据。此操作位于并行查询执行计划的 `slice1` 中。查询计划划分为*切片*，使各个 Segment 可以并行处理查询计划的不同部分。

此计划的估算启动代价为 `00.00`（无代价），总代价为 `20.88` 次磁盘页读取。优化器估算此查询将返回一行。

## 解读 EXPLAIN ANALYZE 输出 {#read-explain-analyze-output}

`EXPLAIN ANALYZE` 会规划并执行语句。`EXPLAIN ANALYZE` 计划同时显示实际执行代价和优化器估算值，便于判断估算是否接近实际情况。`EXPLAIN ANALYZE` 还显示以下信息：

- 查询运行的总时间，单位为毫秒。
- 查询计划每个切片使用的内存，以及为整个查询语句预留的内存。
- 参与计划节点操作的*工作进程*（Segment）数量。只统计返回行的 Segment。
- 在该操作中输出行数最多的 Segment 所返回的最大行数。如果多个 Segment 输出相同的行数，`EXPLAIN ANALYZE` 会显示结束 `time` 最长的 Segment。
- 在该操作中输出行数最多的 Segment 的 ID。
- 对于相关操作，显示操作使用的内存量（`work_mem`）。如果 `work_mem` 不足以在内存中完成操作，计划会显示性能最差的 Segment 溢出到磁盘的数据量。例如：

    ```
    Work_mem used: 64K bytes avg, 64K bytes max (seg0).
    Work_mem wanted: 90K bytes avg, 90K byes max (seg0) to lessen 
    workfile I/O affecting 2 workers.
    ```

- 输出行数最多的 Segment 取得第一行所花的时间，以及取得所有行所花的时间，单位为毫秒。如果取得第一行的 `time` 与结束 `time` 相同，结果可能省略前者。

### EXPLAIN ANALYZE 示例 {#explain-analyze-examples}

本例使用同一查询，介绍如何解读 `EXPLAIN ANALYZE` 计划。计划中标为 `bold` 的部分显示每个计划节点的实际耗时和返回行数，以及整个查询的内存和时间统计信息。

```sql
EXPLAIN ANALYZE SELECT * FROM names WHERE name = 'Joelle';
                     QUERY PLAN
------------------------------------------------------------
Gather Motion 2:1 (slice1; segments: 2) (cost=0.00..20.88 rows=1 width=13)
    Rows out: 1 rows at destination with 0.305 ms to first row, 0.537 ms to end, start offset by 0.289 ms.
        -> Seq Scan on names (cost=0.00..20.88 rows=1 width=13)
             Rows out: Avg 1 rows x 2 workers. Max 1 rows (seg0) with 0.255 ms to first row, 0.486 ms to end, start offset by 0.968 ms.
                 Filter: name = 'Joelle'::text
 Slice statistics:

      (slice0) Executor memory: 135K bytes.

    (slice1) Executor memory: 151K bytes avg x 2 workers, 151K bytes max (seg0).

Statement statistics:
 Memory used: 128000K bytes
 Total runtime: 22.548 ms
```

从下往上解读计划。此查询的总运行时间为 *22.548* 毫秒。

*顺序扫描*操作中只有一个 Segment（*seg0*）返回了行，而且只返回了 *1 行*。找到第一行花费 *0.255* 毫秒，扫描所有行花费 *0.486* 毫秒。该结果接近优化器的估算：查询优化器估算此查询会返回一行。*汇集 Motion*（Segment 向 Coordinator 发送数据）收到了 1 行，此操作总共花费 *0.537* 毫秒。

#### 确定查询优化器 {#determine-the-query-optimizer}

可以查看 `EXPLAIN` 输出，确定该查询计划是否启用了 GPORCA，以及解释计划由 GPORCA 还是基于 Postgres 的规划器生成。这些信息位于 EXPLAIN 输出的末尾。`Settings` 行显示服务器配置参数 `OPTIMIZER` 的设置；`Optimizer:` 行显示解释计划由 GPORCA 还是基于 Postgres 的规划器生成。

以下两个查询计划示例都启用了 GPORCA，即服务器配置参数 `OPTIMIZER` 为 `on`。第一个 EXPLAIN 计划由 GPORCA 生成；第二个则是 Apache Cloudberry 回退到基于 Postgres 的规划器后生成的。

```sql
                       QUERY PLAN
------------------------------------------------------------------------------------
 Aggregate  (cost=0.00..296.14 rows=1 width=8)
   ->  Gather Motion 2:1  (slice1; segments: 2)  (cost=0.00..295.10 rows=1 width=8)
         ->  Aggregate  (cost=0.00..294.10 rows=1 width=8)
               ->  Seq Scan on part  (cost=0.00..97.69 rows=100040 width=1)
 Settings:  optimizer=on
 Optimizer: GPORCA
(5 rows)
```

```sql
explain select count(*) from part;

                       QUERY PLAN
----------------------------------------------------------------------------------------
 Aggregate  (cost=3519.05..3519.06 rows=1 width=8)
   ->  Gather Motion 2:1  (slice1; segments: 2)  (cost=3518.99..3519.03 rows=1 width=8)
         ->  Aggregate  (cost=3518.99..3519.00 rows=1 width=8)
               ->  Seq Scan on part  (cost=0.00..3018.79 rows=100040 width=1)
 Settings:  optimizer=on
 Optimizer: Postgres-based planner
(5 rows)
```

对于以下查询，服务器配置参数 `OPTIMIZER` 为 `off`。

```sql
explain select count(*) from part;

                       QUERY PLAN
----------------------------------------------------------------------------------------
 Aggregate  (cost=3519.05..3519.06 rows=1 width=8)
   ->  Gather Motion 2:1  (slice1; segments: 2)  (cost=3518.99..3519.03 rows=1 width=8)
         ->  Aggregate  (cost=3518.99..3519.00 rows=1 width=8)
               ->  Seq Scan on part  (cost=0.00..3018.79 rows=100040 width=1)
 Settings: optimizer=off
 Optimizer: Postgres-based planner
(5 rows)
```

## 检查查询计划以解决问题 {#examine-query-plans-to-solve-problems}

如果查询性能不佳，请检查其查询计划，并考虑以下问题：

- **计划中是否有操作耗时异常长？** 查找占用大部分查询处理时间的操作。例如，索引扫描耗时超过预期，可能是索引过时，需要重建索引。也可以调整 `enable_<operator>` 参数，针对该查询禁用某个计划算子，观察是否能迫使基于 Postgres 的规划器选择不同的计划。
- **查询规划时间是否超过执行时间？** 当查询涉及许多表连接时，基于 Postgres 的规划器会使用动态算法规划查询，其中部分依据是表连接数量。可以将服务器配置参数 `join_collapse_limit` 和 `from_collapse_limit` 设为较小的值，例如 `8`，减少规划器用于规划查询的时间。注意，较小的值虽然能缩短规划时间，但也可能产生较差的查询计划。
- **优化器的估算是否接近实际情况？** 运行 `EXPLAIN ANALYZE`，查看优化器估算的行数是否接近查询操作实际返回的行数。如果差异很大，请为相关列收集更多统计信息。
- **选择性强的谓词是否在计划早期应用？** 尽早应用选择性最强的过滤条件，减少沿计划树向上传递的行数。如果查询计划未能正确估算查询谓词的选择性，请为相关列收集更多统计信息。有关收集统计信息的更多信息，请参见《Apache Cloudberry 参考指南》中的 `ANALYZE` 命令。也可以尝试调整 SQL 语句中 `WHERE` 子句的条件顺序。
- **优化器是否选择了最佳连接顺序？** 对于连接多个表的查询，应确认优化器选择了选择性最强的连接顺序。能排除最多行的连接应更早执行，以减少沿计划树向上传递的行数。

    如果计划未选择最佳连接顺序，可以设置 `join_collapse_limit=1`，并在 SQL 语句中使用显式 `JOIN` 语法，强制基于 Postgres 的规划器采用指定的连接顺序。也可以为相关连接列收集更多统计信息。

- **优化器是否有选择地扫描分区表？** 使用表分区时，优化器是否只扫描满足查询谓词所需的子表？父表不包含任何数据，因此扫描父表应返回 0 行。有关选择性分区扫描的查询计划示例，请参见[确定分区策略](/cloudberry/operate-with-data/operate-with-db-objects/about-table-partitioning/#decide-on-a-partitioning-strategy)。
- **优化器是否在适用时选择 hash 聚合和哈希连接？** hash 操作通常比其他类型的连接或聚合快得多。行比较和排序在内存中进行，而无需读写磁盘。要让查询优化器选择 hash 操作，必须有足够的内存容纳估算的行数。可以尝试增加工作内存，以提高查询性能。如果可以，请对查询运行 `EXPLAIN ANALYZE`，查看哪些计划操作溢出了磁盘、使用了多少工作内存，以及避免磁盘溢出需要多少内存。例如：

    `Work_mem used: 23430K bytes avg, 23430K bytes max (seg0). Work_mem wanted: 33649K bytes avg, 33649K bytes max (seg0) to lessen workfile I/O affecting 2 workers.`

    `EXPLAIN ANALYZE` 的“bytes wanted”消息根据写入工作文件的数据量计算，并不精确。所需的最小 `work_mem` 可能与建议值不同。
