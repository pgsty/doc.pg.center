---
title: 调优查询
linkTitle: 调优查询
description: Cypher 查询由 PostgreSQL 的规划器制定计划。
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/performance.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


Cypher 查询由 PostgreSQL 的规划器制定计划。没有带独立规则的图引擎，所以 `EXPLAIN` 可用、统计信息重要，你已经掌握的调优方法也适用。

AgensGraph 特有的部分，是少量用于遍历的计划节点、一个会影响每个新图的统计问题，以及五个改变计划形状的设置。

本页只讨论计划形状。面向资源的调优涵盖 `shared_buffers`、`work_mem`、`effective_cache_size`、并行和 autovacuum；它们都不是图特有的，见[配置](/zh/agensgraph/operations/configuration/)。

## 用于测量的图 {#a-graph-to-measure-on}

[示例数据集](/zh/agensgraph/get-started/example-dataset/)有 46 个元素，不足以让规划器做出有趣决策。构建一个带度分布的图，并在末尾删除：

```sql
CREATE TABLE seed_account AS SELECT g AS n, 'user' || g AS handle FROM generate_series(1, 20000) g;
CREATE TABLE seed_follows AS SELECT (1 + (g % 20000)) AS src, (1 + ((g * 7919) % 20000)) AS dst FROM generate_series(1, 120000) g;
```

```cypher
CREATE GRAPH perflab;
SET graph_path = perflab;
CREATE VLABEL account;
CREATE ELABEL follows;
LOAD FROM seed_account AS r CREATE (:account {handle: r.handle, n: r.n});
CREATE PROPERTY INDEX ON account (handle);
```

```cypher
LOAD FROM seed_follows AS r MATCH (a:account {n: r.src}), (b:account {n: r.dst}) CREATE (a)-[:follows]->(b);
```

```sql
ANALYZE perflab.account;
```

20,000 个账户，120,000 条 `follows` 边。只有顶点标签被分析；这个遗漏正是[后文一节](#statistics-on-edge-labels)的主题。

## 读取 Cypher EXPLAIN {#reading-a-cypher-explain}

```cypher
EXPLAIN (COSTS OFF) MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN c.handle;
```

```
                                                                                                 QUERY PLAN                                                                                                 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r2."end" = c.id)
   ->  Nested Loop
         ->  Nested Loop
               ->  Index Scan using account_handle_idx on account a
                     Index Cond: (properties.'handle' = '"user42"'::jsonb)
               ->  Bitmap Heap Scan on follows r1
                     Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     ->  Bitmap Index Scan on follows_start_idx
                           Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Index Scan using follows_start_idx on follows r2
               Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               Filter: (r1.id <> id)
   ->  Hash
         ->  Seq Scan on account c
```

其中四点是 AgensGraph 特有的，其余都是你已经读过的计划。

**属性读取显示为 `properties.'key'`。** 这是 Cypher 解析器书写属性访问的方式，不是你可以输入的 SQL。它出现在 `Index Cond` 中，表示正在匹配表达式索引；出现在 `Filter` 中，表示逐行求值。你会得到哪种情况是[索引页](/zh/agensgraph/querying/indexes-and-constraints/)的主题。

**`graphid` 范围测试就是标签测试。** `start >= '3.0' AND start <= '3.281474976710655'` 表示“边这一端的顶点是 `account`”。标签 id 位于 `graphid` 高位，因此一个标签的 id 构成连续范围，测试可以由边自身列回答。参见[身份：graphid](/zh/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid)。

第二条边上的 **`Filter: (r1.id <> id)`** 是唯一性规则：路径不得两次使用同一条边。

**未命名的模式元素会得到合成别名**，显示为 `"<0000000002>"`。其背后的计数器每条语句都会前进，因此包含它的计划每次运行都不同。要比较基线计划，就命名模式中的每个元素。

`EXPLAIN (ANALYZE)` 可用，而且是查看估计值与真实值对比的唯一方式：

```cypher
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF, BUFFERS OFF)
MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account) RETURN count(b);
```

```
                                                                                                 QUERY PLAN                                                                                                 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate (actual rows=1.00 loops=1)
   ->  Nested Loop (actual rows=6.00 loops=1)
         ->  Nested Loop (actual rows=6.00 loops=1)
               ->  Index Scan using account_handle_idx on account a (actual rows=1.00 loops=1)
                     Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     Index Searches: 1
               ->  Bitmap Heap Scan on follows r1 (actual rows=6.00 loops=1)
                     Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Heap Blocks: exact=1
                     ->  Bitmap Index Scan on follows_start_idx (actual rows=6.00 loops=1)
                           Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           Index Searches: 6
         ->  Index Only Scan using account_pkey on account b (actual rows=1.00 loops=6)
               Index Cond: (id = r1."end")
               Heap Fetches: 6
               Index Searches: 6
```

> [!NOTE]
> 变长或最短路径计划请使用默认文本格式阅读。三者中只有 `Dijkstra` 的计划通过 `EXPLAIN (FORMAT JSON)` 也能正确阅读。

## 遍历的计划节点 {#plan-nodes-for-a-traversal}

固定长度模式不需要特殊节点：如上所述，就是扫描和连接。下面这些节点出现在 SQL 没有对应运算符的场景。

`Graph VLE` 是变长边，并写明边标签和范围：

```cypher
SET graph_path = moviekb;
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r:related_to*1..3]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on related_to [1..3]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`on related_to` 是要读的一行。无类型变长边会变成 `Graph VLE on ag_edge`，每一跳都遍历图中每个边标签。这是路径查询中最大的可避免成本。[路径](/zh/agensgraph/querying/paths/#what-a-path-costs)有对比。

`Shortestpath VLE [min..max]` 是 `shortestpath` 或 `allshortestpaths`，位于两个 `Hash2Side` 节点之上：双向搜索的两个前沿，分别从两端增长。

`Dijkstra` 是加权搜索。它的子节点是搜索扩展所经过的扫描，因此边标签 `start` 列上的索引就是它走的内容。

`Graph Create`、`Graph Set` 和 `Graph Delete` 是写入节点：

```cypher
SET graph_path = perflab;
EXPLAIN (COSTS OFF) MATCH (a:account {handle: 'user42'}) SET a.seen = 1;
```

```
                          QUERY PLAN                           
---------------------------------------------------------------
 Graph Set
   ->  Index Scan using account_handle_idx on account a
         Index Cond: (properties.'handle' = '"user42"'::jsonb)
```

标记为 **`eager`** 的写入节点必须先完成，其上任何内容才能运行，因为上方某些内容读取该写入改变的数据：

```cypher
EXPLAIN (COSTS OFF)
MATCH (a:account {handle: 'user42'}) SET a.seen = 1
WITH a MATCH (a)-[r:follows]->(b:account) RETURN count(b);
```

```
                                                                  QUERY PLAN                                                                   
-----------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate
   ->  Nested Loop
         ->  Nested Loop
               ->  Subquery Scan on _agens_default_s
                     ->  Graph Set eager
                           ->  Index Scan using account_handle_idx on account a
                                 Index Cond: (properties.'handle' = '"user42"'::jsonb)
               ->  Index Only Scan using follows_start_idx on follows r
                     Index Cond: ((start = (_agens_default_s.a).id) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Index Only Scan using account_pkey on account b
               Index Cond: (id = r."end")
```

 eagerness 使[同一语句中后续读取能看到写入](/zh/agensgraph/querying/writing/#reading-what-you-just-wrote)。它的代价是物化写入输出，规模受 `eager_mem` 限制。`MERGE` 始终 eager；不是语句最后子句的任何 `SET`、`REMOVE` 或 `DELETE` 也如此。

以 `_agens_default_s` 开头的名称是流水线阶段生成的别名，大约每个 `WITH` 一个。它们在同一计划内稳定，不是可调优项。

## 边标签统计 {#statistics-on-edge-labels}

这是任何新图上首先检查的内容，其价值高于任何索引。

遍历成本是度数的乘积：起始顶点有多少条边、到达的顶点又有多少条边，依此类推。边标签 `start` 和 `end` 列上的统计信息描述这些度数。创建标签时，AgensGraph 把两列的统计目标都设为最大值 1,000：

```sql
SELECT attname, attstattarget FROM pg_attribute
WHERE attrelid = 'perflab.follows'::regclass AND attnum > 0 ORDER BY attnum;
```

```
  attname   | attstattarget 
------------+---------------
 id         |              
 start      |          1000
 end        |          1000
 properties |              
```

目标不是样本。在某个操作分析该标签之前，那里没有任何统计：

```sql
SELECT count(*) AS stats_rows FROM pg_stats WHERE schemaname = 'perflab' AND tablename = 'follows';
```

```
 stats_rows 
------------
          0
```

于是估计值只是猜测。这是刚加载图上的两跳计数：

```cypher
EXPLAIN MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c);
```

```
                                                                                                    QUERY PLAN                                                                                                    
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=10088.00..10088.01 rows=1 width=32)
   ->  Hash Join  (cost=677.81..9622.10 rows=186358 width=8)
         Hash Cond: (r2."end" = c.id)
         ->  Nested Loop  (cost=20.81..8475.81 rows=186358 width=24)
               ->  Nested Loop  (cost=20.39..779.08 rows=433 width=16)
                     ->  Index Scan using account_handle_idx on account a  (cost=0.29..8.30 rows=1 width=8)
                           Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     ->  Bitmap Heap Scan on follows r1  (cost=20.10..766.44 rows=433 width=24)
                           Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           ->  Bitmap Index Scan on follows_start_idx  (cost=0.00..20.00 rows=433 width=0)
                                 Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Index Scan using follows_start_idx on follows r2  (cost=0.42..13.48 rows=430 width=24)
                     Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Filter: (r1.id <> id)
         ->  Hash  (cost=407.00..407.00 rows=20000 width=8)
               ->  Seq Scan on account c  (cost=0.00..407.00 rows=20000 width=8)
```

一个账户 433 条边，186,358 个两跳对，并对全部 20,000 个账户做哈希来解析远端点。现在分析边标签：

```sql
ANALYZE perflab.follows;
```

```cypher
EXPLAIN MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c);
```

```
                                                                                                    QUERY PLAN                                                                                                    
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=51.17..51.18 rows=1 width=32)
   ->  Nested Loop  (cost=5.52..51.08 rows=36 width=8)
         ->  Nested Loop  (cost=5.23..39.78 rows=36 width=24)
               ->  Nested Loop  (cost=4.81..35.54 rows=6 width=16)
                     ->  Index Scan using account_handle_idx on account a  (cost=0.29..8.30 rows=1 width=8)
                           Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     ->  Bitmap Heap Scan on follows r1  (cost=4.52..27.18 rows=6 width=24)
                           Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           ->  Bitmap Index Scan on follows_start_idx  (cost=0.00..4.52 rows=6 width=0)
                                 Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Index Scan using follows_start_idx on follows r2  (cost=0.42..0.65 rows=6 width=24)
                     Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Filter: (r1.id <> id)
         ->  Index Only Scan using account_pkey on account c  (cost=0.29..0.31 rows=1 width=8)
               Index Cond: (id = r2."end")
```

6 条边、36 个对、远端点使用 index-only 扫描，估计成本 51 对 10,088。36 恰好完全正确：

```cypher
MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c) AS pairs;
```

```
 pairs 
-------
    36
```

结论是：**任何批量加载后，都要 `ANALYZE` 边标签，而不只是顶点标签。** Autovacuum 最终会做，但“最终”是在第一批用户运行查询之后。如果一个图的度数形状发生变化，例如出现枢纽顶点，值得显式重新分析，而不是等待行数阈值。

## 改变计划形状的设置 {#the-settings-that-change-plan-shape}

五个设置影响图查询计划。以下是它们从 `pg_settings` 读到的真实值：

| 设置 | 默认 | 作用域 | 作用 |
| --- | --- | --- | --- |
| `enable_eager` | `on` | session | 关闭时，需要 eager 计划的语句会被拒绝，而不是制定计划。 |
| `eager_mem` | 4 MB | session | eager 节点溢出前可用的内存。 |
| `enable_graph_endpoint_elision` | `on` | session | 删除查询从不读取其值的模式端点扫描。 |
| `enable_property_promotion` | `on` | session | 存在提升类型列时，把 Cypher 属性读取解析到该列。 |
| `auto_gather_graphmeta` | `off` | superuser | 维护 `ag_graphmeta` 边连接性，让规划器能从扫描中剪除不可达标签。 |

> [!NOTE]
> `postgresql.conf.sample` 对 `enable_eager` 和 `enable_multiple_update` 给出了错误默认值。两者都是开启的。读 `pg_settings`，不要读示例文件。

它们都不是生产环境随手拧的旋钮。四个已经开启，第五个是是否维护目录的决策。了解它们是为了诊断：关闭一个设置能告诉你它是否导致意外计划。

### 端点省略 {#endpoint-elision}

查询从不读取其值的端点根本不会扫描。这里 `b` 被绑定、带标签，但从未投影：

```cypher
EXPLAIN (COSTS OFF) MATCH (a:account)-[r:follows]->(b:account) RETURN a.handle;
```

```
                                                                            QUERY PLAN                                                                             
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = a.id)
   ->  Seq Scan on follows r
         Filter: (("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid))
   ->  Hash
         ->  Seq Scan on account a
```

只有一个连接；`(b:account)` 只作为边 `"end"` 列上的范围测试存在。关闭省略后，第二个扫描和连接会回来：

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (a:account)-[r:follows]->(b:account) RETURN a.handle;
RESET enable_graph_endpoint_elision;
```

```
                                                                               QUERY PLAN                                                                                
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r."end" = b.id)
   ->  Hash Join
         Hash Cond: (r.start = a.id)
         ->  Seq Scan on follows r
               Filter: ((start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on account a
   ->  Hash
         ->  Seq Scan on account b
```

结论与设置无关。投影不需要的端点，每次都会多一个扫描和一个连接。所以 `RETURN` 只保留调用者读取的内容。

### 从 ag_graphmeta 剪除扫描 {#scan-pruning-from-ag_graphmeta}

`ag_graphmeta` 为图中实际出现的每个起点标签、边标签、终点标签三元组保存一行，并记录构成它的边数。有了这些信息，无标签模式端点可以收窄到已知该边可达的标签。只有 `auto_gather_graphmeta` 开启时才维护；默认情况下，无标签端点扫描整个 `ag_vertex` 家族：

```cypher
EXPLAIN (COSTS OFF) MATCH (n)-[r:follows]->(m) RETURN n, m;
```

```
                    QUERY PLAN                     
---------------------------------------------------
 Hash Join
   Hash Cond: (m.id = r."end")
   ->  Append
         ->  Seq Scan on ag_vertex m_1
         ->  Seq Scan on account m_2
   ->  Hash
         ->  Hash Join
               Hash Cond: (n.id = r.start)
               ->  Append
                     ->  Seq Scan on ag_vertex n_1
                     ->  Seq Scan on account n_2
               ->  Hash
                     ->  Seq Scan on follows r
```

打开收集后，两个 `Append` 都会折叠。收集会为数据库中的每个图建立基线，所以要有意识地做：

```cypher
SET auto_gather_graphmeta = on;
EXPLAIN (COSTS OFF) MATCH (n)-[r:follows]->(m) RETURN n, m;
RESET auto_gather_graphmeta;
```

```
               QUERY PLAN                
-----------------------------------------
 Hash Join
   Hash Cond: (r."end" = m.id)
   ->  Hash Join
         Hash Cond: (r.start = n.id)
         ->  Seq Scan on follows r
         ->  Hash
               ->  Seq Scan on account n
   ->  Hash
         ->  Seq Scan on account m
```

`follows` 只运行 `account` → `account`，所以两个无标签端点只能是账户。在多标签图上，这就是每个端点一次扫描与每个标签一次扫描的区别。代价是每次边写入的维护，以及基线失效后的重扫。

这个示例只有两个标签，所以节省不大；形状才是重点。`pg_catalog.ag_graphmeta` 保存计数，`ag_graph.graphmeta_valid` 控制是否使用它们。参见[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)。

最直接的替代方法是在模式中命名标签。`MATCH (n:account)-[r:follows]->(m:account)` 完全不需要目录。

### 禁止 eager 计划 {#forbidding-an-eager-plan}

`enable_eager = off` 不会生成另一个计划，而是拒绝生成计划：

```cypher
SET enable_eager = off;
EXPLAIN (COSTS OFF)
MATCH (a:account {handle: 'user42'}) SET a.seen = 1
WITH a MATCH (a)-[r:follows]->(b:account) RETURN count(b);
RESET enable_eager;
```

```
ERROR:  eagerness plan is not allowed.
```

用它找出工作负载中哪些语句依赖 eagerness。不要保持关闭运行。对这类语句，eagerness 是正确性要求，而不是成本选择；没有更便宜的计划可以回退，因此服务器直接报错。

### 解析到提升列 {#resolution-to-a-promoted-column}

`enable_property_promotion = off` 会把属性读取送回 `jsonb` 属性包，即使类型列存在。计划改变，答案不变，因为值同时在两处。它可以在不删除列的情况下判断提升是否导致意外计划。[关闭解析](/zh/agensgraph/querying/typed-columns/#turning-resolution-off)有前后对比。

## 按顺序做什么 {#what-to-do-in-order}

1. **`ANALYZE` 查询触碰的每个标签，包括边标签。** 在此之前，清单上的其他事项都不重要。
2. **检查锚点。** 遍历需要一个有选择性且有索引的起点。挑选起点的属性在 `EXPLAIN` 中应显示为 `Index Cond`，不是 `Filter`；[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)说明哪些谓词可以。
3. **在每个变长模式中命名边标签。** 计划中的 `Graph VLE on ag_edge` 指向查询问题，而不是规划器问题。
4. **限制变长模式长度。**
5. **只投影调用者读取的内容**，让未使用端点省略。
6. **考虑提升持续过滤、连接或排序的属性**——见[把属性提升为列](/zh/agensgraph/querying/typed-columns/#when-to-promote)。
7. **然后再看资源。** 见[配置](/zh/agensgraph/operations/configuration/)。

## 清理 {#clean-up}

```cypher
DROP GRAPH perflab CASCADE;
```

```sql
DROP TABLE seed_account;
DROP TABLE seed_follows;
```

## 接下来去哪里 {#where-to-go-next}

* [索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)——索引可以服务哪些谓词。
* [路径](/zh/agensgraph/querying/paths/#what-a-path-costs)——本页的遍历专项版本。
* [把属性提升为列](/zh/agensgraph/querying/typed-columns/)——当读取本身成为成本时。
* [配置](/zh/agensgraph/operations/configuration/)——内存、I/O 和 autovacuum。
