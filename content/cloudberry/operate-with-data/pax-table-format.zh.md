---
title: "PAX 存储格式"
description: "Apache Cloudberry 支持 PAX（Partition Attributes Across）存储格式。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/pax-table-format.md"
---

PAX 是一种数据库存储格式，兼具行存（NSM，N 元存储模型）和列存（DSM，分解存储模型）的优势，旨在改善查询性能，尤其是缓存效率。在 OLAP 场景中，PAX 提供接近行存的批量写入性能，以及接近列存的读取性能。PAX 既适用于采用对象存储模型的云环境，也适用于传统的离线物理文件存储方式。

与传统存储格式相比，PAX 具有以下特点：

- 数据更新和删除：PAX 采用标记删除的方式处理数据更新与删除，无需立即重写整个数据文件，就能有效管理物理文件中的更改。
- 并发控制与读写隔离：PAX 使用多版本并发控制（MVCC），实现高效的并发控制与读写隔离。控制粒度达到单个数据文件级别，提高了操作的安全性和效率。
- 索引支持：PAX 支持 B-树索引，以加速查询操作，对提升大量数据场景下的检索速度尤其有用。
- 数据编码与压缩：PAX 提供多种数据编码方式（如游程编码和差分编码），以及支持不同压缩级别的压缩选项（如 zstd 和 zlib），在减少存储空间需求的同时优化读取性能。
- 统计信息：数据文件包含详细的统计信息，用于快速过滤和查询优化，减少不必要的数据扫描，加快查询处理。

## 适用场景 {#applicable-scenarios}

PAX 的混合存储能力适合需要处理大量数据写入和频繁查询的复杂 OLAP 应用。无论是在云基础设施中构建高性能数据分析方案，还是在传统数据中心环境中处理大型数据集，PAX 都能提供有力支持。

## 从源码构建 Cloudberry 时启用 PAX {#enable-pax-when-building-cloudberry-from-source-code}

从源码构建 Apache Cloudberry 时，要启用 PAX，需要执行以下步骤：

1. 确保满足以下依赖要求：

    - C/C++ 编译器：GCC/GCC-C++ 11 或更高版本
    - CMake：3.11 或更高版本
    - Protobuf：3.5.0 或更高版本
    - ZSTD（libzstd）：1.4.0 或更高版本

2. 在 Cloudberry 源码目录的顶层运行以下命令，下载子模块：

   ```bash
   git submodule update --init --recursive
   ```

   将下载以下子模块，用于构建和测试 PAX：

    - yyjson（`dependency/yyjson`）
    - cpp-stub（`contrib/pax_storage/src/cpp/contrib`）
    - googlebench（`contrib/pax_storage/src/cpp/contrib`）（目前是可选依赖，默认会下载但不构建。如有需要，可以手动构建。）
    - googletest（`contrib/pax_storage/src/cpp/contrib`）
    - tabulate（`contrib/pax_storage/src/cpp/contrib`）

    > [!NOTE] 注意
    > 最新发布的源码归档已包含上述子模块，因此解压归档后无需手动下载。

3. 运行 `configure` 命令时，添加 `--enable-pax` 选项。例如：

    ```bash
    ./configure --enable-pax --with-perl --with-python --with-libxml --with-gssapi --prefix=/usr/local/cloudberrydb
    ```

    此外，要以 `DEBUG` 模式启用 PAX，请在 `configure` 命令中同时添加 `--enable-cassert` 和 `--enable-pax` 选项，这样还会构建 PAX 中的 `GTEST`。按以下方式运行 `GTEST`：

    ```bash
    cd contrib/pax_storage/build
    ./src/cpp/test_main
    ```

> [!TIP] 提示
> 如果对 PAX 的实现细节感兴趣，可以参阅 [GitHub 仓库中的设计文档](https://github.com/apache/cloudberry/tree/main/contrib/pax_storage/doc)。

## 使用方法 {#usage}

### 创建 PAX 表 {#create-a-pax-table}

要创建 PAX 格式的表，需要将表访问方法设为 PAX。可以使用以下任一方式：

- 创建表时显式使用 `USING PAX` 子句，例如：

    ```sql
    CREATE TABLE t1(a int, b int, c text) USING PAX;
    -- t1 is a PAX table and can be used like a normal heap table.
    ```

- 将默认表访问方法设为 PAX，再创建表：

    ```sql
    -- Set the default table access method. From now on, newly created tables will use PAX format.
    SET default_table_access_method = pax;

    -- Implicitly use the default access method, which is PAX.
    CREATE TABLE t1(a int, b int, c text);
    ```

创建表时，还可以为某些列指定最小值和最大值信息，以加速查询：

```sql
-- Use WITH(minmax_columns='b,c') to specify that columns b and c
-- should record min and max statistics.
-- This helps optimize queries involving these two columns,
-- because the system can quickly determine which data blocks might contain matching data.
CREATE TABLE p2(a INT, b INT, c INT) USING pax WITH(minmax_columns='b,c');

INSERT INTO p2 SELECT i, i * 2, i * 3 FROM generate_series(1,10)i;

-- because column b has minmax statistics,
-- the system can quickly locate the data blocks that might contain the value, speeding up the query.
SELECT * FROM p2 WHERE b = 4;

-- Similarly, because of the minmax information on column b, the system can quickly determine that no data blocks can meet this condition
-- (if all generated values are positive), possibly returning no data immediately and avoiding unnecessary data scans.
SELECT * FROM p2 WHERE b < 0;

-- Modify the minmax statistics settings for table p2 to apply only to column b. For data inserted later,
-- only column b will maintain this statistical information, and it won't affect existing data or trigger any rewrites or adjustments.
ALTER TABLE p2 SET(minmax_columns='b');
```

### 查看现有表的格式 {#view-the-format-of-an-existing-table}

要检查表是否采用 PAX 格式，可以使用以下任一方法：

- 使用 `psql` 命令 `\d+`：

    ```sql
    gpadmin=# \d+ t1
                                                Table "public.t1"
    Column |  Type   | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
    --------+---------+-----------+----------+---------+----------+-------------+--------------+-------------
    a      | integer |           |          |         | plain    |             |              |
    b      | integer |           |          |         | plain    |             |              |
    c      | text    |           |          |         | extended |             |              |
    Distributed by: (a)
    Access method: pax
    ```

- 查询系统目录表 `pg_class` 和 `pg_am`：

    ```sql
    SELECT relname, amname FROM pg_class, pg_am WHERE relam = pg_am.oid AND relname = 't1';

    relname | amname
    ---------+--------
    t1      | pax
    (1 row)
    ```

## TOAST 支持 {#support-for-toast}

如果 PAX 表的某些列包含大值，可以启用 TOAST 存储，将这些大值存放在单独的 TOAST 文件中。这样可以使主数据文件中的数据更加紧凑，在扫描相同大小的数据时读取更多元组。

PAX 表默认启用 TOAST 存储。与 PostgreSQL 不同，PAX 的 TOAST 存储不依赖页管理，因此能够存储大于 2 MiB 的数据。

可以通过以下参数配置 TOAST 相关阈值。详情请参阅 [PAX 相关系统参数](#pax-related-system-parameters)。

- `pax_enable_toast`
- `pax_min_size_of_compress_toast`
- `pax_min_size_of_external_toast`

## 聚簇支持 {#support-for-clustering}

Apache Cloudberry 支持对 PAX 表进行 Z 序排序，可显著提高多维数据的管理和查询性能。使用聚簇功能时，可以通过两种排序策略组织 PAX 表中的数据：基于索引的聚簇和基于 `reloptions` 的聚簇。请注意，两种策略互斥，只能选择一种。

### 聚簇策略 {#clustering-strategies}

Apache Cloudberry 的聚簇功能可以对表数据进行物理排序和优化，通过重新组织数据的物理存储顺序来改善查询性能。PAX 表的聚簇功能提供两种数据排序策略：

- 基于索引的聚簇。这种策略基于 B-树索引，工作方式类似于 PostgreSQL 原生的聚簇方法，适用于表上已有索引的情况。

    示例：

    ```sql
    CREATE TABLE t2(c1 int, c2 int) USING PAX;
    CREATE INDEX c1_idx ON t2(c1);
    CLUSTER t2 USING c1_idx;
    DROP TABLE t2;
    ```

- 基于 `reloptions` 的聚簇。PAX 表支持通过在 `reloptions` 中指定 `cluster_columns` 来执行聚簇操作，并提供以下排序方式：

    - Z 序聚簇：将多列的值编码为字节数组，再按该字节数组排序。适合将多列用作查询条件、且这些列在查询中没有固定顺序的情况。这种方法能够显著提升多维数据查询性能，但不适合具有相同前缀的字符串列。未指定 `cluster_type` 时，PAX 默认采用 Z 序排序作为聚簇策略：

        ```sql
        CREATE TABLE t2(c1 int, c2 float, c3 text) USING PAX WITH (cluster_columns='c1,c2');
        INSERT INTO t2 SELECT i, i, i::text FROM generate_series(1, 100000) i;
        CLUSTER t2;
        DROP TABLE t2;
        ```

        本例按 `c1` 和 `c2` 列对表 `t2` 中的数据进行 Z 序排序。这种排序方式能显著改善多维查询场景下的性能。

    - 字典序聚簇：按列的值及列的顺序排序，主要用于对具有相同前缀的字符串列进行排序和查询优化。例如：

        ```sql
        CREATE TABLE t2(c1 int, c2 float, c3 text) USING PAX WITH (cluster_columns='c1,c2', cluster_type='lexical');
        INSERT INTO t2 SELECT i, i, i::text FROM generate_series(1, 100000) i;
        CLUSTER t2;
        DROP TABLE t2;
        ```

        本例按 `c1` 和 `c2` 列对表 `t2` 中的数据进行字典序排序。这种排序方式很适合具有相同前缀的列。

### 聚簇类型之间的冲突 {#conflicts-between-clustering-types}

基于索引的聚簇与基于 `cluster_columns` 的聚簇不能同时使用。如果表已经基于索引（或 `cluster_columns`）进行聚簇，就不能再指定 `cluster_columns`（或索引）进行聚簇。

处理聚簇冲突的示例：

```sql
-- Creates a table and uses index-based clustering
CREATE TABLE t2(c1 int, c2 float, c3 text) USING PAX;
CREATE INDEX t2_idx ON t2(c1);
CLUSTER t2 USING t2_idx;

-- Tries to use cluster columns (will fail)
ALTER TABLE t2 SET (cluster_columns='c1,c2', cluster_type='zorder');
-- Tries to use lexical clustering (will fail)
ALTER TABLE t2 SET (cluster_columns='c1,c2', cluster_type='lexical');

-- Drops the index and successfully use lexical clustering
DROP INDEX t2_idx;
ALTER TABLE t2 SET (cluster_columns='c1,c2', cluster_type='lexical');
```

上例中，表 `t2` 基于索引完成聚簇后，在删除该索引之前，尝试通过 `cluster_columns` 设置 Z 序或字典序聚簇都会失败。

## 布隆过滤器支持 {#bloom-filter-support}

Apache Cloudberry 支持布隆过滤器，可以按列生成和维护布隆过滤器信息。这有助于快速过滤数据块、提升查询性能，尤其是在使用包含多个值的 `IN` 条件时，能够大幅减少不必要的数据扫描。

### 布隆过滤器选项 {#bloom-filter-options}

通过设置 `bloomfilter_columns` 选项，可以指定需要记录布隆过滤器信息的列。例如：

```sql
CREATE TABLE p1 (
    a int,
    b int,
    c text
) USING PAX WITH (bloomfilter_columns='b,c,a');
```

本例会为表 `p1` 的 `b`、`c` 和 `a` 列生成布隆过滤器。

布隆过滤器的大小由以下 GUC（全局用户配置）参数控制：

- `pax_max_tuples_per_file`：控制每个数据文件中存储的最大元组数。
- `pax_bloom_filter_work_memory_bytes`：控制布隆过滤器允许使用的最大内存量。

例如：

```sql
-- Sets the maximum number of tuples per file.
SET pax_max_tuples_per_file = 131073;

-- Sets the maximum bloom filter memory.
SET pax_bloom_filter_work_memory_bytes = 1048576;  -- 1MB

-- Creates a table and specifies bloom filter options for columns.
CREATE TABLE p1 (
    a int,
    b int,
    c text
) USING PAX WITH (bloomfilter_columns='b,c,a');
```

生成的布隆过滤器大小按以下方式计算：

```sql
ceil(min(pax_max_tuples_per_file * 2, pax_bloom_filter_work_memory_bytes))
```

`ceil` 是取整函数，确保布隆过滤器的大小始终为 `2` 的幂。

## 稀疏过滤 {#sparse-filtering}

稀疏过滤是 PAX 存储格式提供的一种数据扫描优化：跳过不满足条件的文件扫描，并减少文件内部需要扫描的数据块，从而改善查询性能。

使用稀疏过滤前，请确保满足以下条件：

- 系统参数 `pax_enable_sparse_filter` 设为 `ON`（默认值）。
- 已为相关列配置统计信息（`min`/`max` 或布隆过滤器）。
- 查询包含针对这些列的过滤条件（`WHERE` 子句）。

### 支持的表达式示例 {#expression-support-examples}

PAX 支持基本条件表达式。例如：

```sql
-- Creates test table
CREATE TABLE a(v1 int, v2 int, v3 int) USING PAX WITH(minmax_columns='v1, v2, v3');

-- Basic conditions
SELECT * FROM a WHERE v1 <= 3;                                    -- Full condition support. root is OpExpr.
SELECT * FROM a WHERE v1 != NULL;                                -- Full condition support. root is NULLTest.

-- Multiple conditions
SELECT * FROM a WHERE v1 <= 3 AND v2 >= 3;                       -- Full condition support. Tree structure has only one level.
SELECT * FROM a WHERE v1 <= 3 AND v2 >= 3 AND v3 >= 3;          -- Full condition support.
SELECT * FROM a WHERE v1 <= 3 AND v2 >= 3 AND v3 != NULL;       -- Full condition support.
```

PAX 还支持嵌套表达式结构和某些操作符。例如：

```sql
-- Creates test table.
CREATE TABLE a(v1 int, v2 int, v3 int) USING PAX WITH(minmax_columns='v1, v2, v3');

-- Nested expressions.
SELECT * FROM a WHERE (v1 <= 3 OR v2 > 3) AND v3 >= 10;         -- Full support for all conditions.
SELECT * FROM a WHERE (v1 <= 3 AND v2 > 3) OR v3 >= 10;         -- Supports complete nested expressions.

-- Operators.
SELECT * FROM a WHERE v1 + v2 <= 3;
SELECT * FROM a WHERE v1 + 10 <= 3;
```

PAX 能够处理完整的表达式树，包括嵌套的 `AND`/`OR` 条件。因此，上述查询都可以得到优化，Apache Cloudberry 会使用所有可用的过滤条件来提高查询效率。

### 支持的表达式类型 {#supported-expression-types}

PAX 稀疏过滤支持以下表达式类型：

- 算术操作符（`OpExpr`）

    - 支持加法（`+`）、减法（`-`）和乘法（`*`）。
    - 不支持除法运算，因为难以估算负数范围。
    - 示例：`a + 1`、`1 - a`、`a * b`。

- 比较操作符（`OpExpr`）

    - 支持 `<`、`<=`、`=`、`>=`、`>`。
    - 示例：`a < 1`、`a + 1 < 10`、`a = b`。

- 逻辑操作符（`BoolExpr`）

    - 支持 `AND`、`OR`、`NOT`。
    - 示例：`a < 10 AND b > 10`。

- NULL 值测试（`NullTest`）

    - 支持 `IS NULL`、`IS NOT NULL`。
    - 示例：`a IS NULL`、`a IS NOT NULL`。

- 类型转换（`FuncExpr`）

    - 仅支持基本的类型转换。
    - 示例：`a::float8 < 1.1`。
    - 不支持自定义函数，例如 `func(a) < 10`。

- `IN` 操作符（`ScalarArrayOpExpr`）

    - 支持 `IN` 表达式。
    - 示例：`a IN (1, 2, 3)`。

### 部分条件支持 {#partial-condition-support}

当查询包含不受支持的表达式（如自定义函数）时，PAX 采用部分条件支持策略：

- 识别并提取受支持的条件。
- 使用这些条件进行稀疏过滤。

例如：

```sql
-- Creates custom function v2
CREATE OR REPLACE FUNCTION func(v2 double precision)
RETURNS double precision AS $$
BEGIN
  RETURN v2 * 2;
END;
$$ LANGUAGE plpgsql;

-- Uses custom function in query
SELECT * FROM a WHERE v1 < 3 AND func(v2) < 10;  -- PAX will use v1 < 3 for filtering
```

本例中，虽然 `func(v2) < 10` 无法用于稀疏过滤，Apache Cloudberry 仍会利用 `v1 < 3` 优化查询性能。这样，即使是复杂查询，也能获得部分性能优化。

> [!NOTE] 注意
> - 稀疏过滤的效果取决于数据分布和查询条件。
> - 建议为经常用作过滤条件的列启用统计信息。
> - 某些条件（如自定义函数）会被忽略。

## 在 WAL 日志中查看 PAX 表的数据变更记录 {#view-data-change-records-on-pax-tables-in-wal-logs}

PAX 表相关的数据操作会记录在预写式日志（WAL）系统中，以确保主节点与镜像节点之间的可靠备份，为故障切换提供支持。

可以使用 `pg_waldump` 工具查看 PAX 表的 WAL 日志。日志存放在 `$COORDINATOR_DATA_DIRECTORY/pg_wal` 目录，或 Segment 节点数据目录下的 `pg_wal` 目录中。

PAX 表的 WAL 日志可用于：

- **数据恢复**：在系统故障或数据不一致时帮助恢复数据。
- **支持故障切换**：确保主节点与镜像节点之间的数据同步。
- **调试与分析**：识别和分析对 PAX 表执行的具体操作。

### 示例：操作 PAX 表并查看 WAL 日志 {#example-operate-pax-tables-and-view-wal-logs}

1. 创建 PAX 表。

    ```sql
    CREATE TABLE a (
       v1 int,
       v2 int,
       v3 int
    ) USING PAX;
    ```

    这会创建 PAX 表 `a`，包含 `v1`、`v2` 和 `v3` 三列。

2. 向表中插入数据：

    ```sql
    INSERT INTO a VALUES (1, 2, 3);
    ```

3. 定位 PAX 表所在的节点：

    ```sql
    -- Views the IDs and data directory locations of all nodes in the cluster
    SELECT * FROM gp_segment_configuration;

    -- Identifies the Segment ID of table a based on the results of the above query
    -- This helps determine the segment and data directory location of table a
    SELECT gp_segment_id FROM gp_distribution_policy WHERE localoid = 'a'::regclass;
    ```

4. 在该节点的 `pg_wal` 目录中查找相应的 WAL 日志。例如：

    ``` bash
    ls $COORDINATOR_DATA_DIRECTORY/pg_wal
    ```

    找到最新的 WAL 文件，以分析相关操作。本例假设 WAL 日志文件名为 `00000001000000000000000A`。

5.  查询 PAX 表的 `relfilenode`，将 WAL 日志与该表关联：

    ```sql
    SELECT relfilenode FROM pg_class WHERE relname = 'a';
    ```

    `relfilenode` 是该表在 WAL 日志中的唯一标识符。

6.  使用 `pg_waldump` 工具解析 WAL 日志，识别与 PAX 表相关的操作：

    ```bash
    pg_waldump -f $COORDINATOR_DATA_DIRECTORY/pg_wal/00000001000000000000000A
    ```

    在输出中搜索之前获得的 `relfilenode`，找到与 PAX 表关联的操作。

    `pg_waldump` 的输出示例：

    ```text
    rmgr: PAX       len (rec/tot):     68/   104, tx:    593, lsn: 0/016E1D98, prev 0/016E1D60, desc: INSERT off 3, blkref #0: rel 1663/16384/19780 blk 0
    ```

    本例中：

    - `rmgr: PAX` 表示记录类型。
    - `rel 1663/16384/19780` 对应 PAX 表的 `relfilenode`。
    - `INSERT` 表示记录了一次插入操作。

通过上述步骤，可以跟踪和分析 Apache Cloudberry 中与 PAX 表相关的 WAL 日志，用于调试、恢复或性能优化。

## PAX 表的限制 {#limitations-for-pax-tables}

- PAX 存储格式目前只支持 B-树（`btree`）索引。使用 GiST、SP-GiST（`gist/spgist`）或 BRIN 索引可能出现缺陷。其他索引类型的支持仍处于实验阶段，可能不可用。
- 目前，过长的字段会存储在 TOAST 文件中。这里的 TOAST 与 PostgreSQL 的 TOAST 表不同，只是名称相同。
- 与传统堆表不同，PAX 格式不支持 `TOAST` 字段。目前，所有列数据都存放在同一个数据文件中。
- PAX 格式不支持使用 `pg_dump` 或 `pg_restore` 备份和恢复数据；这些操作会忽略 PAX 表。可以使用 `pg_basebackup` 备份和恢复 PAX 表。

## PAX 相关 SQL 选项 {#pax-related-sql-options}

PAX 提供用于控制其行为的 SQL 选项。可以在 `WITH()` 子句中使用这些选项，例如 `WITH(minmax_columns='b,c', storage_format=porc)`。

| 名称 | 类型 | 有效值 | 说明 |
|------------------------|---------|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `storage_format` | `string` | •  `porc`<br />•  `porc_vec` | 控制内部存储格式。默认值为 `porc`，以常规格式存储数据，不保留空值。`porc_vec` 以向量格式存储数据，对于定长字段，无论列值是否为空，都保留空值。 |
| `compresstype` | `string` | •  `none`<br />•  `rle`<br />•  `delta`<br />•  `zstd`<br />•  `zlib`<br />•  `dict` | 指定列值的压缩方式，只能选择一种，默认值为 `none`。<br /><br />•  `none` 表示不压缩。<br />•  `rle` 使用游程编码压缩连续重复的数据。<br />•  `delta` 用于数值列，存储相邻值之差。<br />•  `zstd` 使用 zstd 算法，具有较高压缩率和较快压缩速度。<br />•  `zlib` 是适合一般数据的通用压缩算法。<br />•  `dict` 使用字典编码，加快大量重复字符串的处理。目前仍为实验性功能，不建议用于生产环境。 |
| `compresslevel` | `int` | 范围 `[0, 19]` | 指定压缩级别，默认值为 `0`。值越小，压缩越快；值越大，压缩程度越高。仅与 `compresstype` 一起使用时生效。 |
| `partition_by` | `string` | 表中的有效列名 | 写入批量数据时，尝试按指定列对数据分区，并将其存储在同一数据文件中，以改善数据局部性。只支持整数类型。该分区键独立于表分区，仅作为 PAX 内部组织数据的建议。 |
| `partition_ranges` | `string` | `FROM(XX) TO(YY) [every(DD)]` | 必须与 `partition_by` 一起使用，用于设置分区范围。可以定义一个范围，也可以将大范围划分为多个不连续的小范围。PAX 会尝试将每个范围内的数据存储在同一数据文件中，范围之外的数据则存储在默认数据文件中。 |
| `minmax_columns` | `string` | 表中的有效列名，以逗号分隔 | 为指定列记录 `minmax` 统计信息，以加速数据查询。列重命名后，将不再记录该列的统计信息。通过 `ALTER TABLE` 修改 `minmax_columns` 时，更改仅适用于之后写入的数据文件，不影响已有数据文件。 |
| `cluster_columns` | `string` | 表中有效列名的逗号分隔列表 | 指定 PAX 表以聚簇方式存储内部数据。执行 `cluster` 命令时，可按这些列对数据排序，排序方式由 `cluster_type` 参数控制。 |
| `bloomfilter_columns` | `string` | 表中有效列名的逗号分隔列表 | 为指定列的数据计算布隆过滤器，以帮助过滤数据。 |
| `parallel_workers` | `int` | `[0,64]` | PostgreSQL 选项，用于设置并发扫描时的并行进程数。 |
| `cluster_type` | `string` | `lexical` 和 `zorder` | 当聚簇基于 `reloptions` 中定义的自定义列而非索引时，指定聚簇类型。有效值为 `lexical` 和 `zorder`。`lexical` 按列的值及列的顺序排序；`zorder` 将多列的值编码成字节数组，再按该数组排序。 |

这些选项的值仅影响新插入和更新的数据，不改变已有数据。

## PAX 相关系统参数 {#pax-related-system-parameters}

以下系统参数（GUC）用于设置当前会话中 PAX 表的行为。使用 `SET <parameter>=<value>` 命令配置，例如 `SET pax_enable_sparse_filter=on`。

| 参数名 | 值类型 | 有效值 | 说明 |
|--------------------------------------|------------|------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pax_enable_sparse_filter` | `bool` | `on` 和 `off` | 是否启用基于统计信息的稀疏过滤。默认值为 `on`，即默认启用稀疏过滤。 |
| `pax_enable_row_filter` | `bool` | `on` 和 `off` | 是否启用行过滤。默认值为 `off`，即禁用行过滤。不建议启用此参数。 |
| `pax_scan_reuse_buffer_size` | `int` | 范围 `[1048576, 33554432]`（1MiB 至 32MiB） | 扫描时使用的缓冲块大小。默认值为 `8388608`（8MiB）。 |
| `pax_max_tuples_per_group` | `int` | 范围 `[5, 524288]` | 每组允许的最大元组数。默认值为 `131072`。 |
| `pax_max_tuples_per_file` | `int` | 范围 `[131072, 8388608]` | 每个数据文件允许的最大元组数。最大值为 `8388608`，默认值为 `1310720`。 |
| `pax_max_size_per_file` | `int` | 范围 `[8388608, 335544320]`（8MiB 至 320MiB） | 每个数据文件允许的最大物理大小。默认值为 `67108864`（64MiB）。实际文件大小可能略大于设定值。值过大或过小都可能对性能产生不利影响。 |
| `pax_enable_toast` | `bool` | `on` 和 `off`，默认值为 `on`。 | 是否启用 TOAST 支持。 |
| `pax_min_size_of_compress_toast` | `int` | 范围 `[524288, 1073741824]`（512KiB 至 1GiB），默认值为 `524288`（512KiB）。 | 创建压缩 TOAST 表的阈值。如果字符长度超过此阈值，Apache Cloudberry 会创建压缩 TOAST 表进行存储。 |
| `pax_min_size_of_external_toast` | `int` | 范围 `[10485760, 2147483647]`（10MiB 至 2GiB），默认值为 `10485760`（10MiB）。 | 创建外置 TOAST 表的阈值。如果字符长度超过此阈值，Apache Cloudberry 会创建外置 TOAST 表进行存储。 |
| `pax_default_storage_format` | `string` | `porc`（默认值） | 控制默认存储格式。 |
| `pax_bloom_filter_work_memory_bytes` | `int` | 范围 `[1024, 2147483647]`（1KiB 至 2GiB），默认值为 `10240`（10KiB）。 | 控制布隆过滤器允许使用的最大内存量。 |

## 最佳实践 {#best-practices}

- 使用分区选项：

    - 如果需要按整数列导入数据，且满足以下条件，建议使用分区选项：

        - 数据在该列上分布均匀、取值范围较大，且不存在极端集中。
        - 该列经常用作查询过滤条件或连接键。

    - 请注意，PAX 分区键只在单次批量数据导入过程中生效，不能在多次数据写入之间调整。分区键设置只适用于后续插入或更新，因此更改分区键后，新导入的数据会遵循新的分区键。

- 使用 `minmax` 统计信息：

    - 对于数据范围较大、且经常用于查询过滤的列，设置 `minmax` 值可以显著加快查询。
    - 利用 `minmax` 统计信息，如果数据文件中的某列不满足 `minmax` 值或空值测试条件，就可以快速跳过整个文件，避免不必要的数据扫描。
    - 请特别注意，`minmax` 的效果取决于数据的插入方式。如果 PAX 表的数据按批次插入（例如通过 `batch insert` 或 `copy`），且每批数据的取值范围连续，`minmax` 就非常有效。如果随机插入数据，`minmax` 的过滤效果可能降低。

- 如果 PAX 表中有多列用于查询过滤，可以使用 `with(cluster_columns='b,c,d', cluster_type='zorder')`。通过 `zorder` 编码对数据排序后，任何一个 `cluster_columns` 列都能从过滤中受益。相比之下，基于单列的聚簇排序只对排序键的过滤有效，对其他列的影响很小。聚簇排序会影响基于 `minmax` 的过滤，但不影响基于 `bloom filter` 的过滤。

- 如果查询使用 `column1 in (12, 11, 13)` 或 `column1 = 'X'` 这样的过滤条件，可以考虑使用 `bloom filter (with(bloomfilter_columns='b,c'))`。在内部实现中，PAX 会为某些数据计算布隆过滤器。如果布隆过滤器能够确定数据不在当前数据块中，PAX 就可以跳过该块。请注意，布隆过滤器的效果取决于多个因素：

    - `group` 中的数据量。
    - `bloom filter` 使用的空间。
