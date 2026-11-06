---
title: "EXPLAIN"
description: "显示语句的查询计划。"
weight: 1460
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/explain.md"
---

## 语法概要 {#synopsis}

```sql
EXPLAIN [ ( <option> [, ...] ) ] <statement>
EXPLAIN [ANALYZE] [VERBOSE] <statement>
```

其中 option 可以是以下选项之一：

```sql
    ANALYZE [ <boolean> ]
    VERBOSE [ <boolean> ]
    COSTS [ <boolean> ]
    BUFFERS [ <boolean> ]
    TIMING [ <boolean> ]
    FORMAT { TEXT | XML | JSON | YAML }
```

## 说明 {#description}

`EXPLAIN` 显示 Apache Cloudberry 查询优化器或 Postgres 规划器为给定语句生成的查询计划。查询计划是一棵由节点组成的树。计划中的每个节点代表一种操作，例如表扫描、连接、聚合或排序。

应自下而上阅读计划，因为每个节点都会将行传给它正上方的节点。计划最底层的节点通常是表扫描操作（顺序扫描、索引扫描或位图索引扫描）。如果查询需要连接、聚合、排序或其他针对原始行的操作，扫描节点上方就会有额外的节点执行这些操作。最顶层的计划节点通常是 Apache Cloudberry 的 Motion 节点（重分布、显式重分布、广播或汇集 Motion）。这些操作负责在查询处理期间在 Segment 实例之间移动行。

`EXPLAIN` 的输出为计划树中的每个节点显示一行，包含节点的基本类型，以及优化器对该计划节点执行成本的以下估计：

- **cost** — 优化器对运行语句所需时间的估计（以任意定义的成本单位衡量，通常以读取磁盘页面的成本为单位）。这里显示两个成本值：返回第一行之前的启动成本，以及返回所有行的总成本。注意，总成本假定会取回所有行，但实际情况不一定如此（例如使用 `LIMIT` 时）。
- **rows** — 此计划节点输出的总行数。它通常小于该节点实际处理或扫描的行数，反映了对各个 `WHERE` 子句条件选择率的估计。理想情况下，顶层节点的估计值应接近查询实际返回、更新或删除的行数。
- **width** — 此计划节点输出的所有行的总字节数。

需要注意，上层节点的成本包含其所有子节点的成本。计划最顶层节点的成本是整个计划的估计执行总成本，优化器力求将这个值降到最低。还应了解，成本只反映查询优化器所关注的因素，尤其不包括将结果行传送给客户端所花费的时间。

`EXPLAIN ANALYZE` 会实际运行语句，而不只是制定计划。`EXPLAIN ANALYZE` 计划会同时显示实际结果和优化器的估计值，有助于判断估计值是否接近实际情况。除 `EXPLAIN` 计划中的信息外，`EXPLAIN ANALYZE` 还会显示以下信息：

- 运行查询所用的总时间（毫秒）。
- 参与计划节点操作的 *worker*（Segment）数量。只统计返回行的 Segment。
- 对于某项操作，产出行数最多的 Segment 返回的最大行数。如果多个 Segment 产出的行数相同，则选择其中*完成时间*最长的一个。
- 对于某项操作，产出行数最多的 Segment 的 ID。
- 对于适用的操作，显示该操作使用的 work_mem。如果 `work_mem` 不足以在内存中执行该操作，计划会显示性能最差的 Segment 溢出到磁盘的数据量，以及需要对数据扫描多少遍。例如：

    ```
    Work_mem used: 64K bytes avg, 64K bytes max (seg0).
    Work_mem wanted: 90K bytes avg, 90K bytes max (seg0) to abate workfile 
    I/O affecting 2 workers.
    [seg0] pass 0: 488 groups made from 488 rows; 263 rows written to 
    workfile
    [seg0] pass 1: 263 groups made from 263 rows
    ```

- 从产出行数最多的 Segment 取回第一行所需的时间（毫秒），以及取回该 Segment 所有行所需的总时间。如果 `<time\> to first row` 与 `<time\> to end` 相同，则可能省略前者。

> **重要** 请记住，使用 `ANALYZE` 时会实际运行语句。虽然 `EXPLAIN ANALYZE` 会丢弃 `SELECT` 返回的所有输出，但语句的其他副作用仍会照常发生。如果希望对 DML 语句使用 `EXPLAIN ANALYZE`，又不希望命令影响数据，可以采用以下方法：

```sql
BEGIN;
EXPLAIN ANALYZE ...;
ROLLBACK;
```

不使用括号括起选项列表时，只能指定 `ANALYZE` 和 `VERBOSE` 选项，而且必须按此顺序指定。

## 参数 {#parameters}

**`ANALYZE`**

执行命令并显示实际运行时间和其他统计信息。省略此参数时，默认值为 `FALSE`；指定 `ANALYZE true` 可启用它。

**`VERBOSE`**

显示有关计划的额外信息。具体包括：计划树中每个节点的输出列列表；以模式限定表名和函数名；始终用范围表别名标注表达式中的变量；以及始终打印所显示统计信息对应的每个触发器的名称。省略此参数时，默认值为 `FALSE`；指定 `VERBOSE true` 可启用它。

**`COSTS`**

包含每个计划节点的估计启动成本和总成本，以及估计行数和每行的估计宽度。省略此参数时，默认值为 `TRUE`；指定 `COSTS false` 可禁用它。

**`BUFFERS`**

包含缓冲区使用情况。只有同时指定 `ANALYZE` 时才能指定此参数。省略时，默认值为 `false`，不包含缓冲区使用情况。
> **注意**
> Apache Cloudberry 不支持对分布式查询指定 `BUFFERS [true]`；请忽略显示的任何缓冲区使用信息。

**`TIMING`**

在输出中包含实际启动时间以及每个节点花费的时间。在某些系统上，反复读取系统时钟的开销可能使查询显著变慢，因此如果只需要实际行数而不需要准确时间，将此参数设为 `FALSE` 可能更合适。即使此选项关闭了节点级计时，也始终会测量整个语句的运行时间。只有同时启用 `ANALYZE` 时才能使用此参数。默认值为 `TRUE`。

**`FORMAT`**

指定输出格式，可以是 `TEXT`、`XML`、`JSON` 或 `YAML`。非文本格式包含的信息与文本格式相同，但更易于程序解析。此参数的默认值为 `TEXT`。

**`boolean`**

指定打开还是关闭所选选项。可以写 `TRUE`、`ON` 或 `1` 来启用选项，写 `FALSE`、`OFF` 或 `0` 来禁用选项。也可以省略布尔值，此时假定为 `TRUE`。

**`statement`**

要查看其执行计划的任意 `SELECT`、`INSERT`、`UPDATE`、`DELETE`、`VALUES`、`EXECUTE`、`DECLARE` 或 `CREATE TABLE AS` 语句。

## 注意事项 {#notes}

为了让查询优化器在优化查询时有充分的信息作出合理决策，应运行 `ANALYZE` 语句来记录表内数据分布的统计信息。如果没有这样做（或者自上次运行 `ANALYZE` 以来，表内数据的统计分布发生了显著变化），估计成本就不太可能符合查询的实际特征，因而可能选择较差的查询计划。

执行 `EXPLAIN ANALYZE` 命令期间运行的 SQL 语句不受 Apache Cloudberry 资源队列的约束。

有关查询性能分析的更多信息，请参阅《Apache Cloudberry 管理员指南》中的“查询性能分析”。有关资源队列的更多信息，请参阅《Apache Cloudberry 管理员指南》中的“使用资源队列管理资源”。

## 示例 {#examples}

下面用一个非常简单的查询说明如何阅读 `EXPLAIN` 查询计划：

```sql
EXPLAIN SELECT * FROM names WHERE name = 'Joelle';
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=0.00..431.27 rows=1 width=58)
   ->  Seq Scan on names  (cost=0.00..431.27 rows=1 width=58)
         Filter: (name = 'Joelle'::text)
 Optimizer: Pivotal Optimizer (GPORCA) version 3.23.0
(4 rows)
```

自下而上阅读计划，可以看到查询优化器首先对 `names` 表执行顺序扫描。注意，`WHERE` 子句被用作*过滤*条件。这意味着扫描操作会检查所扫描的每一行，只输出满足条件的行。

扫描操作的结果向上传给*汇集 Motion* 操作。在 Apache Cloudberry 中，汇集 Motion 表示 Segment 将行发送给 Coordinator。此例中，3 个 Segment 实例向 1 个 Coordinator 实例发送数据（3:1）。此操作位于并行查询执行计划的 `slice1` 中。在 Apache Cloudberry 中，查询计划被划分为多个*查询切片*，使 Segment 可以并行处理计划的不同部分。

此计划的估计启动成本为 `00.00`（无成本），总成本为 `431.27`。优化器估计该查询将返回一行。

以下为隐藏成本估计后的同一查询：

```sql
EXPLAIN (COSTS FALSE) SELECT * FROM names WHERE name = 'Joelle';
                QUERY PLAN
------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)
   ->  Seq Scan on names
         Filter: (name = 'Joelle'::text)
 Optimizer: Pivotal Optimizer (GPORCA) version 3.23.0
(4 rows)
```

以下为采用 JSON 格式的同一查询：

```sql
EXPLAIN (FORMAT JSON) SELECT * FROM names WHERE name = 'Joelle';
                  QUERY PLAN
-----------------------------------------------
 [                                            +
   {                                          +
     "Plan": {                                +
       "Node Type": "Gather Motion",          +
       "Senders": 3,                          +
       "Receivers": 1,                        +
       "Slice": 1,                            +
       "Segments": 3,                         +
       "Gang Type": "primary reader",         +
       "Startup Cost": 0.00,                  +
       "Total Cost": 431.27,                  +
       "Plan Rows": 1,                        +
       "Plan Width": 58,                      +
       "Plans": [                             +
         {                                    +
           "Node Type": "Seq Scan",           +
           "Parent Relationship": "Outer",    +
           "Slice": 1,                        +
           "Segments": 3,                     +
           "Gang Type": "primary reader",     +
           "Relation Name": "names",          +
           "Alias": "names",                  +
           "Startup Cost": 0.00,              +
           "Total Cost": 431.27,              +
           "Plan Rows": 1,                    +
           "Plan Width": 58,                  +
           "Filter": "(name = 'Joelle'::text)"+
         }                                    +
       ]                                      +
     },                                       +
     "Settings": {                            +
       "Optimizer": "Pivotal Optimizer (GPORCA) version 3.23.0"      +
     }                                        +
   }                                          +
 ]
(1 row)
```

如果存在索引，并且查询的 `WHERE` 条件可以使用索引，`EXPLAIN` 可能会显示不同的计划。下面的查询会生成使用索引扫描的计划，并采用 YAML 格式输出：

```sql
EXPLAIN (FORMAT YAML) SELECT * FROM NAMES WHERE LOCATION='Sydney, Australia';
                          QUERY PLAN
--------------------------------------------------------------
 - Plan                                                +
     Node Type: "Gather Motion"                              +
     Senders: 3                                              +
     Receivers: 1                                            +
     Slice: 1                                                +
     Segments: 3                                             +
     Gang Type: "primary reader"                             +
     Startup Cost: 0.00                                      +
     Total Cost: 10.81                                       +
     Plan Rows: 10000                                        +
     Plan Width: 70                                          +
     Plans                                             +
       - Node Type: "Index Scan"                             +
         Parent Relationship: "Outer"                        +
         Slice: 1                                            +
         Segments: 3                                         +
         Gang Type: "primary reader"                         +
         Scan Direction: "Forward"                           +
         Index Name: "names_idx_loc"                         +
         Relation Name: "names"                              +
         Alias: "names"                                      +
         Startup Cost: 0.00                                  +
         Total Cost: 7.77                                    +
         Plan Rows: 10000                                    +
         Plan Width: 70                                      +
         Index Cond: "(location = 'Sydney, Australia'::text)"+
   Settings                                            +
     Optimizer: "Pivotal Optimizer (GPORCA) version 3.23.0"
(1 row)
```

## 兼容性 {#compatibility}

SQL 标准没有定义 `EXPLAIN` 语句。

## 另请参阅 {#see-also}

[ANALYZE](/cloudberry/reference/sql-stmts/analyze/)
