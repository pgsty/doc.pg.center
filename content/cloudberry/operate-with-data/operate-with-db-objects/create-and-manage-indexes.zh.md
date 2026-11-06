---
title: "创建和管理索引"
linkTitle: "创建和管理索引"
description: "在传统数据库中，索引通常用于显著提高数据访问性能。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-indexes.md"
---

然而，在 Apache Cloudberry 这样的分布式系统中，使用索引需要更加谨慎。Apache Cloudberry 提供高速顺序扫描，而索引查找依赖随机磁盘访问。由于数据分布在多个 Segment 上，每个 Segment 只需扫描本地的数据子集即可返回结果。结合表分区，还可以进一步减少查询期间扫描的数据量。因此，对于通常返回大型结果集的商业智能（BI）工作负载，索引可能带来性能开销，而非收益。

建议先在没有索引的情况下运行查询，再根据实际性能观察结果，在必要时添加索引。索引通常更适合 OLTP 场景，这类查询往往只检索单行或小范围的数据。对于返回特定目标行的查询，索引也可以提高 AO 表的性能。在适当的情况下，规划器可能选择使用索引，而不是扫描整张表。对于压缩数据，索引访问使系统只需解压所需的行，从而提高整体效率。

表定义主键时，Apache Cloudberry 会自动创建 `PRIMARY KEY` 约束。对于分区表，必须在根表上创建索引；系统会自动将索引传播到所有子表。请注意，不能手动为系统创建的子表添加索引。

此外，`UNIQUE CONSTRAINT`（例如 `PRIMARY KEY CONSTRAINT`）会隐式创建 `UNIQUE INDEX`。此索引必须包含分布键和分区键中的所有列，并且必须在整个表（包括所有分区）上强制保证唯一性。

索引会引入额外开销：它们占用存储空间，并且需要在数据更新时维护。因此，务必确认查询工作负载确实使用了所创建的索引，并验证索引带来了可衡量的性能提升。可以使用 `EXPLAIN` 查看查询执行计划来检查这一点。

## 索引类型 {#index-types}

Apache Cloudberry 支持多种 PostgreSQL 索引类型，包括 B-树、哈希、GiST、SP-GiST、GIN 和 [BRIN 索引](/cloudberry/operate-with-data/operate-with-db-objects/brin-indexes/)。每种类型适用于不同的查询模式。B-树是默认的索引类型，也是适用范围最广的索引类型。有关各索引类型的详细说明，请参阅 PostgreSQL 文档中的[索引类型](https://www.postgresql.org/docs/14/indexes-types.html)。

> [!NOTE]
> 在 Apache Cloudberry 中，唯一索引的索引列必须与分布键相同，或包含分布键的所有列。在分区表上，唯一索引仅在各个子表内部强制保证唯一性，而不跨所有分区保证唯一性。

### 位图索引 {#bitmap-indexes}

位图索引特别适合数据量大、查询频繁、更新较少的典型数据仓库场景。与普通索引相比，位图索引既能节省存储空间，又能高效处理多条件查询。

位图索引为每个键值维护一个位图。位图中的每一位表示相应行是否包含该值。可以通过布尔运算（例如 `AND` 和 `OR`）组合位图，从而高效地按多个条件筛选。在访问数据之前，位图运算就可以排除大量无关行，显著提高查询性能。

建议的使用场景：

- 适合数据仓库中的分析工作负载。

- 最适合中等基数的列（约 100 到 100,000 个不同值）。

- 对于 `WHERE` 子句中包含多个 `AND` 或 `OR` 条件的查询尤其有效。

- 从 v2.0.0 开始，数组谓词（例如 `col IN (...)` 或 `col = ANY(array)`）可以触发位图索引扫描：

    - 同时适用于 B-树索引和哈希索引。
    - 哈希索引原先只支持等值匹配，现在也支持数组比较谓词。
    - 规划器使用基于代价的模型来决定是否使用位图路径。

    示例：以下查询触发位图索引扫描，使哈希索引能够高效处理大型数据集中的多值条件。

    ```sql
    CREATE TABLE users(id int, name text) DISTRIBUTED BY (id);
    CREATE INDEX ON users USING hash (name);

    SELECT * FROM users WHERE name IN ('alice', 'bob', 'carol');
    ```

限制：

- 不适合值唯一或基数较高的列（例如用户 ID 或电话号码）。
- 不建议用于频繁更新的 OLTP 工作负载。
- 添加位图索引之前，务必通过测试验证其性能收益。

## 管理索引 {#manage-indexes}

### 按索引聚簇表 {#cluster-a-table-by-index}

可以使用 `CLUSTER` 命令，根据索引对表数据进行物理重排。然而，对于非常大的表，此操作可能耗时较长。更高效的替代方法是创建中间表，按所需顺序插入数据，从而手动重排数据。例如：

```sql
CREATE TABLE new_table (LIKE old_table) 
    AS SELECT * FROM old_table ORDER BY myixcolumn;
DROP old_table;
ALTER TABLE new_table RENAME TO old_table;
CREATE INDEX myixcolumn_ix ON old_table;
VACUUM ANALYZE old_table;
```

### 创建索引 {#create-indexes}

使用 `CREATE INDEX` 命令在表上创建索引。默认索引类型是 B-树。例如，在 *employee* 表的 *gender* 列上创建 B-树索引：

```sql
CREATE INDEX gender_idx ON employee (gender);
```

在 *films* 表的 *title* 列上创建位图索引：

```sql
CREATE INDEX title_bmp_idx ON films USING bitmap (title);
```

### 重建表上的所有索引 {#rebuild-all-indexes-on-a-table}

可以使用 `REINDEX` 命令重建表上的所有索引或某个特定索引：

```sql
REINDEX my_table;
```

重建表上的单个索引：

```sql
REINDEX my_index;
```

### 删除索引 {#drop-indexes}

使用 `DROP INDEX` 命令删除索引。例如：

```sql
DROP INDEX title_idx;
```

加载数据时，事先删除所有索引，并在加载完成后重新创建它们，通常可以提高整体性能。

## 仅索引扫描与覆盖索引 {#index-only-scan-and-covering-index}

> [!NOTE]
> Apache Cloudberry 仅在新创建的表上支持仅索引扫描和覆盖索引。

### 什么是仅索引扫描 {#what-is-an-index-only-scan}

在 Apache Cloudberry 中，所有索引都是二级索引，与主数据（堆）分开存储。

在典型的索引扫描中，规划器使用索引定位匹配元组的位置，然后通过元组指针访问堆，以获取实际数据。由于堆中的数据通常不是连续存储的，这种方式可能产生大量随机 I/O，在传统机械磁盘上尤其明显。虽然位图扫描可以在一定程度上减少这类开销，但仍然需要访问堆。

仅索引扫描是一种完全从索引返回结果、无需访问堆的扫描方法，可以显著提高查询性能。

> [!NOTE]
> 从 v2.0.0 开始，Apache Cloudberry（使用 ORCA 优化器）支持在追加优化表（AO 表）和 PAX 表上进行仅索引扫描，从而提高此类表上重复读取查询工作负载的性能。

### 要求 {#requirements}

要使用仅索引扫描，必须满足两个条件：

- 索引类型必须支持仅索引扫描：

    - B-树索引始终支持。
    - GiST 和 SP-GiST 索引在使用某些操作符类时支持。
    - GIN 索引不支持（它们仅存储部分字段数据）。
    - 其他索引类型通常不支持。

- 查询引用的所有列都必须包含在索引中：

    可以使用仅索引扫描的查询示例：

    ```sql
    SELECT x, y FROM tab WHERE x = 'key';
    SELECT x FROM tab WHERE x = 'key' AND y < 42;
    ```

    不能使用仅索引扫描的查询示例：

    ```sql
    SELECT x, z FROM tab WHERE x = 'key';
    SELECT x FROM tab WHERE x = 'key' AND z < 42;
    ```

### 补充说明：MVCC 可见性检查 {#additional-note-mvcc-visibility-checks}

即使满足上述两个条件，系统仍必须按照多版本并发控制（MVCC）规则，验证每条记录对当前事务是否可见。由于索引中不存储可见性信息，系统通常需要访问堆来确认。

为减少堆访问的性能开销，Apache Cloudberry 使用可见性映射机制：

- 如果堆页中的所有元组对所有事务都可见，则将该页标记为“全部可见”。
- 查询执行期间，系统首先检查可见性映射。
- 如果该页“全部可见”，则跳过堆访问，直接返回结果。
- 否则，仍然必须访问堆以检查可见性。

可见性映射很轻量，通常能够完整缓存在内存中，从而显著降低查询期间随机 I/O 的代价。因此，只有大部分堆页都标记为“全部可见”时，仅索引扫描才能带来实际的性能收益。

### 覆盖索引的用途 {#purpose-of-covering-indexes}

为了更好地支持仅索引扫描，可以显式创建覆盖索引，包含查询引用的所有列。Apache Cloudberry 支持 `INCLUDE` 子句，允许向索引添加不用于筛选的列：

示例：

```sql
-- Traditional index: accelerates only the WHERE clause, does not support index-only scan
CREATE INDEX tab_x ON tab(x);

-- Covering index: includes column y in the index, supports index-only scan
CREATE INDEX tab_x_y ON tab(x) INCLUDE (y);

-- Example query
SELECT y FROM tab WHERE x = 'key';
```

使用 `INCLUDE` 添加的列不参与索引匹配，只用于覆盖查询返回的列。因此：

- 这些列无需支持可索引的操作。
- 在唯一索引中，强制保证唯一性时不考虑这些列。

示例：

```sql
CREATE UNIQUE INDEX tab_x_y ON tab(x) INCLUDE (y);
-- Uniqueness is enforced on column x only, not on y
```

限制与注意事项：

- 索引元组的大小有限制。包含较宽的列可能导致索引过大，甚至插入失败。
- 添加非键列会增大索引，并可能影响读取或更新性能。
- 只有表很少更新（即大部分页标记为全部可见）时，覆盖索引才有助于触发仅索引扫描。
- 目前 `INCLUDE` 子句不支持表达式。
- 目前只有 B-树和 GiST 索引类型支持 `INCLUDE`。

> [!NOTE]
> 从 v2.0.0 开始，Apache Cloudberry（使用 ORCA 优化器）支持在 AO 表和 PAX 表上使用 PostgreSQL 风格的 `INCLUDE` 子句，从而可以创建覆盖索引。

从 v2.0.0 开始，GPORCA 优化器在选择仅索引扫描路径时，会同时考虑包含列的宽度和数量。如果多个索引都满足查询谓词和输出要求，优化器会优先选择字段更少、更窄的索引，以降低 I/O 代价。

示例：

```sql
CREATE TABLE t1 (c1 int, c2 int, c3 int, c4 int, c5 int);

CREATE INDEX idx_large ON t1 USING btree(c1) INCLUDE (c2, c3, c4, c5);
CREATE INDEX idx_c1 ON t1 USING btree(c1);

EXPLAIN ANALYZE SELECT c1 FROM
```

### 动态仅索引扫描 {#dynamic-index-only-scan}

动态仅索引扫描是 Apache Cloudberry（使用 ORCA 优化器）查询分区表时采用的一种高效查询策略。它结合了两项关键技术：

- **仅索引扫描**：只要索引覆盖所有引用的列，并且相应的页标记为“全部可见”（例如，在执行 `VACUUM` 操作后），查询就只访问索引，避免访问堆。
- **动态扫描**：在执行期间，根据查询条件只选择相关分区，避免不必要的分区访问（即分区剪枝）。

动态仅索引扫描的核心思想是将仅索引访问与分区剪枝相结合。这样，系统既可以只扫描相关分区，又可以跳过堆访问，大幅提高查询效率。

它适用于以下场景：

- 目标是分区表。
- 查询只引用索引包含的列（即使用覆盖索引）。
- 表已执行清理，相关页已标记为全部可见。
- 表较宽，但索引紧凑，且只包含必要的列。

动态仅索引扫描可以显著提高性能、减少 I/O，并自动适应分区结构，对用户完全透明。

此功能默认启用。如果已禁用，请运行以下命令启用它：

```sql
SET optimizer_enable_dynamicindexonlyscan = on;
```

示例：

```sql
CREATE TABLE pt(a int, b text, c text) 
PARTITION BY RANGE(a) (START (0) END (100) EVERY (20));

CREATE INDEX idx ON pt(a);  -- Covering index, includes only column a

-- Insert a large volume of data and clean up
INSERT INTO pt ...
VACUUM pt;

-- Query involves only column a and supports partition pruning
SELECT a FROM pt WHERE a < 42;
```

## 反向索引扫描 {#backward-index-scan}

对于包含 `ORDER BY ... DESC` 的查询，GPORCA 优化器可能选择使用 B-树索引的反向索引扫描路径，以避免额外的排序操作。

示例：

```sql
CREATE TABLE foo (a int, b int, c int) DISTRIBUTED BY (a);
CREATE INDEX foo_b ON foo(b);
INSERT INTO foo SELECT i, i, i FROM generate_series(1,10000) i;
ANALYZE foo;

EXPLAIN SELECT * FROM foo ORDER BY b DESC LIMIT 1;
```

在此查询中，虽然 `foo_b` 索引默认按升序排列，但查询要求降序。优化器会自动选择反向索引扫描（Backward IndexScan），以降序扫描索引，从而无需 `Sort` 节点：

```sql
Limit
  ->  Gather Motion 3:1
        Merge Key: b
        ->  Limit
              ->  Index Scan Backward using foo_b on foo
```

这项优化同时适用于普通索引扫描（`IndexScan`）和仅索引扫描（`IndexOnlyScan`）。

必须满足以下条件，优化才能生效：

- 使用 B-树索引。
- 查询包含与索引列匹配的 `ORDER BY` 子句。
- 查询中的排序方向与索引默认顺序相反。
- 如果指定了 `NULLS FIRST` 或 `NULLS LAST`，排序行为也必须匹配。

反向索引扫描可以显著减少排序操作的开销，对于分页查询或前 N 项查询尤其有效。

## 检查索引使用情况 {#check-index-usage}

Apache Cloudberry 中的索引无需手动调优或维护。不过，可以通过检查实际查询执行计划来评估索引的效果。使用 `EXPLAIN` 命令查看查询是否使用索引。

查询计划展示数据库执行查询的方式（称为*计划节点*），并提供每个步骤的代价估计。要检查是否使用了索引，请在 `EXPLAIN` 输出中查找以下节点：

- **Index Scan**：直接使用索引检索数据。
- **Bitmap Index Scan**：根据查询条件构建位图并执行位图扫描。
- **Bitmap Heap Scan**：使用位图从堆中获取行。
- **BitmapAnd** / **BitmapOr**：为复合条件合并多个位图。

以下是评估和优化索引使用情况的一些建议：

- 创建或修改索引后，务必运行 `ANALYZE`。这会更新表统计信息，优化器利用这些信息来估计行数并选择最佳计划。

- 使用真实数据测试。测试数据仅反映测试环境，不能代表实际生产数据的分布或行为。

- 避免使用小数据集测试。它们的行为往往与大规模数据有显著差异，结果可能没有意义。

- 生成测试数据时，应注意数据分布。随机值和倾斜值都可能影响统计信息的准确性。

- 可以调整 GUC 参数，强制优化器使用特定计划，以评估索引的行为。例如：

    ```sql
    SET enable_seqscan = off;
    SET enable_nestloop = off;
    ```

    禁用顺序扫描和嵌套循环连接，可以促使系统选择基于索引的路径。分别对使用索引和不使用索引的查询运行 `EXPLAIN ANALYZE`，比较执行时间和计划，以确定索引是否改善了性能。
