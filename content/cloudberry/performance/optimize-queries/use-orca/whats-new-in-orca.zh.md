---
title: "GPORCA 优化器更新说明"
description: "本文介绍 Apache Cloudberry 各版本中 GPORCA 优化器的功能增强和行为变化。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-orca/whats-new-in-orca.md"
---

## v2.0.0 {#v200}

从 v2.0.0 开始，GPORCA 优化器新增了以下功能和改进：

- 除此前支持的 B-树索引仅索引扫描之外，GPORCA 现在还支持更多索引类型的仅索引扫描。具体包括：

    - 支持 AO 表和 PAX 表上的仅索引扫描。
    - 支持 PostgreSQL 风格的 `INCLUDE` 列，可以在 AO 和 PAX 表上创建覆盖索引，提高重复读取工作负载的性能。

- GPORCA 现在可以根据查询的排序方向自动选择反向索引扫描，同时适用于普通索引扫描和仅索引扫描。此优化可以减少对 `Sort` 节点的需求，并提升某些 top-N 查询的性能。

- 新增了将 `ScalarArrayOp` 谓词（例如 `col IN (...)` 或 `col = ANY(array)`）下推到索引路径的支持，包括：

    - B-树或 hash 索引；
    - Index Scan 或 Bitmap Index Scan 路径。

    优化器根据代价估算决定是否使用位图扫描。在选择性较低时，仍可能回退到顺序扫描。注意，`ScalarArrayOp` 下推只适用于索引的前导列，不适用于复合索引的非前导列。

    示例：

    ```sql
    CREATE INDEX idx ON t(col1, col2);
    SELECT * FROM t WHERE col1 = ANY('{1,2,3}');  -- Pushdown supported
    SELECT * FROM t WHERE col2 = ANY('{1,2,3}');  -- No pushdown, used as filter only
    ```

- 新增 `FULL JOIN` 支持，采用 `Hash Full Join` 执行策略。该实现无需对连接键排序，适合大型数据集、高基数连接键或分布键不匹配的场景。

    目前不支持 `Merge Full Join`，因此所有 `FULL JOIN` 查询都使用 `Hash Full Join`。

    与传统 `Merge Join` 相比，`Hash Full Join` 具有以下优势：

    - 无需对连接键排序；
    - 减少数据移动（Motion）开销；
    - 当连接键高度倾斜或基数很高时，性能可能更好。

    示例：

    ```sql
    EXPLAIN SELECT * FROM t1 FULL JOIN t2 ON t1.id = t2.id;
    ```

    可能生成以下计划：

    ```sql
    Hash Full Join
    Hash Cond: t1.id = t2.id
    ...
    ```

- GPORCA 引入了查询改写规则，可将 `JOIN` 操作下推到 `UNION ALL` 的各个分支之下。启用后，优化器可能将 `UNION ALL` 上方的 `JOIN` 改写为多个较小的连接，从而通过以下方式显著提高性能：

    - 将 `UNION ALL` 上方的大连接转换为多个小连接。
    - 让每个子连接独立使用索引，减少 Motion 和 `Hash Join` 开销。
    - 将 `JOIN` 下推到 `UNION ALL` 的左侧或右侧，支持更灵活的查询结构。

    此优化默认禁用，可以通过以下 GUC 启用：

    ```sql
    SET optimizer_enable_push_join_below_union_all = on;
    ```

    以下示例展示启用优化后，优化器如何将 `JOIN` 下推到每个 `UNION ALL` 分支之下：

    ```sql
    -- Creates test tables
    CREATE TABLE dist_small_1(c1 int);
    INSERT INTO dist_small_1 SELECT generate_series(1, 1000);
    CREATE INDEX dist_small_1_index ON dist_small_1 USING btree (c1);
    ANALYZE dist_small_1;

    CREATE TABLE dist_small_2(c1 int);
    INSERT INTO dist_small_2 SELECT generate_series(1, 1000);
    ANALYZE dist_small_2;

    CREATE TABLE inner_1(cc int);
    INSERT INTO inner_1 VALUES(1);
    ANALYZE inner_1;

    -- Creates a view
    CREATE VIEW dist_view_small AS
    SELECT c1 FROM dist_small_1
    UNION ALL
    SELECT c1 FROM dist_small_2;

    -- Enables the optimization and run the query
    SET optimizer_enable_push_join_below_union_all = on;
    EXPLAIN ANALYZE
    SELECT c1 FROM dist_view_small JOIN inner_1 ON c1 < cc;
    ```

    优化器可能生成如下计划：

    ```sql
    ->  Append
        ->  Nested Loop
                ...
                ->  Index Scan using dist_small_1_index on dist_small_1
        ->  Nested Loop
                ...
                ->  Seq Scan on dist_small_2
    ```

    此优化尤其适用于以下查询：

    - 对大型表执行 `UNION ALL`，再与小表连接。
    - 每个分支都有优化器可以使用的索引。
    - `JOIN` 应用于包含 `UNION ALL` 的视图或子查询。

    > [!NOTE]
    > - 此优化不支持 `FULL JOIN` 或公共表表达式（CTE）。
    > - 也不支持 `JOIN of UNION ALL` 或 `UNION ALL of JOIN` 结构。

- 默认情况下，GPORCA 通过 GUC 参数 `optimizer_penalize_broadcast_threshold` 为广播路径（Broadcast Motion）设置较高代价，避免在数据量较大时选择昂贵的计划。

    自 v2.0.0 起，对于 `NOT IN` 查询（例如左反半连接，LASJ），不再惩罚广播路径。这可以防止优化器将大型表集中到 Coordinator 上，避免由此导致的严重性能问题甚至内存不足（OOM）错误。

    允许广播路径有助于保留并行执行，并显著提高大型数据集上 `NOT IN` 查询的性能。

    功能详情：

    - 仅适用于 `NOT IN` 查询（LASJ）。
    - 忽略 `optimizer_penalize_broadcast_threshold` 的设置。
    - 其他连接类型（例如 `IN` 或 `EXISTS`）仍保留惩罚策略。

    示例：

    ```sql
    SELECT * FROM foo WHERE a NOT IN (SELECT a FROM bar);
    ```

    查询计划示例：

    ```sql
    Gather Motion 2:1
    -> Hash Left Anti Semi (Not-In) Join
        -> Seq Scan on foo
        -> Broadcast Motion
                -> Seq Scan on bar
    ```

- GPORCA 现在支持在公共表表达式（CTE）内部执行仅索引扫描。下例中的 CTE 查询可以触发仅索引扫描：

    ```sql
    CREATE TABLE t(a int, b int);
    CREATE INDEX i ON t(a);
    INSERT INTO t SELECT i, i+i FROM generate_series(1, 10)i;
    VACUUM ANALYZE t;

    EXPLAIN WITH cte AS (SELECT a FROM t WHERE a > 42) SELECT * FROM cte;
    ```

### 包含多个外连接的自连接优化 {#optimization-for-self-joins-with-multiple-outer-joins}

自 v2.0.0 起，GPORCA 可以识别涉及多个外连接的特定模式，跳过不必要的 Redistribute Motion 操作，提高执行效率：

- 查询包含多个 LEFT OUTER JOIN 或 RIGHT OUTER JOIN 操作。
- 所有参与连接的表都是同一基表的别名。
- 连接条件对称（例如 `t1.a = t2.a`）。
- 所有表使用相同的分布键，并满足局部性约束。

示例：

```sql
CREATE TABLE o1 (a1 int, b1 int) DISTRIBUTED BY (a1);

EXPLAIN (COSTS OFF)
SELECT * FROM (SELECT DISTINCT a1 FROM o1) t1
             LEFT OUTER JOIN o1 t2 ON t1.a1 = t2.a1
             LEFT OUTER JOIN o1 t3 ON t2.a1 = t3.a1;
```

在早期版本中，此查询会在每层连接之间插入 Redistribute Motion。从 v2.0.0 开始，GPORCA 能识别这种多层自连接模式，避免不必要的数据重分布，从而提高整体查询性能。
