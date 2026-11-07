---
title: 表管理
description: 了解 Citus 中的表管理，包括如何确定表和关系大小、使用分布式表和使用列式存储。
weight: 20
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/table-management?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

Citus 将表分布到多个节点上，实现水平扩展。本文介绍 Citus 的主要表管理任务，包括测量分布式表大小、通过清理和分析维护表，以及使用列式存储处理分析工作负载。了解这些操作有助于优化 Citus 集群的性能和存储效率。

## 确定表和关系大小 {#determining-table-and-relation-size}

在 PostgreSQL 中通常使用 `pg_total_relation_size` 查询表大小，但它会严重低估分布式表的大小。在 Citus 集群中，该函数返回的是协调节点上表的大小。实际上，分布式表的数据存储在工作节点的分片中，而不在协调节点上。要得到分布式表的实际大小，应将各分片的大小相加。Citus 提供了查询这些信息的辅助函数。

这些函数分别对应 PostgreSQL 的三个标准[对象大小函数](https://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE)，并增加了无法连接节点时报错的行为。

下面是一个使用辅助函数来列出所有分布式表大小的示例：

```sql
SELECT logicalrelid AS name,
       pg_size_pretty(citus_table_size(logicalrelid)) AS size
  FROM pg_dist_partition;
```

输出：

```text
┌───────────────┬───────┐
│     name      │ size  │
├───────────────┼───────┤
│ github_users  │ 39 MB │
│ github_events │ 37 MB │
└───────────────┴───────┘
```

## 清理分布式表 {#vacuuming-distributed-tables}

在 PostgreSQL 及其他多版本并发控制（MVCC）数据库中，对行执行 UPDATE 或 DELETE 并不会立即删除旧行版本。过期行版本的累积称为膨胀，必须加以清理，以免查询性能下降、磁盘空间需求无限增长。PostgreSQL 的 autovacuum 守护进程会定期清理（移除）过期行版本。

在分布式数据库中，清理操作也能像用户查询一样扩展。在 PostgreSQL 中，大型繁忙表容易膨胀：一方面，这类表对清理比例因子参数的敏感度较低；另一方面，行数据的变动通常很多。将表拆成分布式分片后，单个分片就是较小的表，autovacuum 工作进程也能在不同机器上并行处理同一张表的不同部分。通常，autovacuum 对每张表只能运行一个工作进程。

出于此考虑，Citus 集群上的 autovacuum 操作在大多数情况下已经足够好。 但是，对于具有特定工作负荷的表，或者对于那些有特定“安全”时段可供安排清理操作的公司而言，手动对表进行清理可能比让 autovacuum 自动执行清理操作更为合理。

要清理表，请在协调节点上运行以下命令：

```sql
VACUUM my_distributed_table;
```

对分布式表执行 VACUUM，会向该表的每个分片放置发送 VACUUM 命令，每个放置使用一个连接，并行执行。除 `VERBOSE` 外，所有[选项](https://www.postgresql.org/docs/current/static/sql-vacuum.html)均受支持，包括 `column_list` 参数。VACUUM 也会先在协调节点上执行，然后才通知工作节点。未指定表的 VACUUM 命令不会传播到工作节点。

> [!TIP]
> PostgreSQL 18 引入 `VACUUM/ANALYZE ONLY`，仅针对父表（用于分区/继承层次结构）。 Citus 14 在传播维护命令时会考虑到这种范围限制。
> 
> ```sql
> VACUUM (ANALYZE) ONLY metrics;
> ANALYZE ONLY metrics;
> ```
> 
> 若只需要轻量的维护操作，而不希望递归处理所有子分区或分片放置，可使用 `ONLY`。

## 分析分布式表 {#analyzing-distributed-tables}

PostgreSQL 的 `ANALYZE` 命令收集数据库中表内容的统计信息。查询规划器利用这些统计信息确定最高效的查询执行计划。

上一节介绍的 autovacuum 守护进程会在表内容变化达到一定程度时自动执行 `ANALYZE`。它完全根据插入或更新的行数安排 `ANALYZE`，并不知道这些变化是否会显著影响统计信息。管理员也可以手动安排 `ANALYZE`，使其与对统计信息有实际影响的表变更相配合。

若要分析表，请在协调节点上运行以下命令：

```sql
ANALYZE my_distributed_table;
```

Citus 将 `ANALYZE` 命令传播到所有工作节点上的分片放置。

## 列式存储 {#columnar-storage}

Citus 10 引入了仅追加的列式表存储，用于分析和数据仓库工作负载。按列而不是按行连续存储数据，可以提高压缩率，也能更快地查询部分列。

### 用法 {#usage}

要使用列式存储，请在创建表时指定 `USING columnar`：

```sql
CREATE TABLE contestant (
    handle TEXT,
    birthdate DATE,
    rating INT,
    percentile FLOAT,
    region CHAR(3),
    achievements TEXT[]
) USING columnar;
```

还可以在基于行的（堆）和列式存储之间进行转换。

```sql
-- Convert to row-based (heap) storage
SELECT alter_table_set_access_method('contestant', 'heap');

-- Convert to columnar storage (indexes will be dropped)
SELECT alter_table_set_access_method('contestant', 'columnar');
```

插入时，Citus 将行数据按“条带”转换为列式存储。每个条带包含一个事务的数据，或最多 150,000 行，以较少者为准。可以使用 `alter_columnar_table_set` 函数修改列式表的条带大小及其他参数。

例如，以下语句在单个事务中插入所有值，因此这五行会放入同一个条带：

```sql
-- insert these values into a single columnar stripe

INSERT INTO contestant VALUES
  ('a','1990-01-10',2090,97.1,'XA','{a}'),
  ('b','1990-11-01',2203,98.1,'XA','{a,b}'),
  ('c','1988-11-01',2907,99.4,'XB','{w,y}'),
  ('d','1985-05-05',2314,98.3,'XB','{}'),
  ('e','1995-05-05',2236,98.2,'XC','{a}');
```

应尽量使用较大的条带，因为 Citus 按条带分别压缩列式数据。使用 `VACUUM VERBOSE` 可以查看压缩比、条带数和每个条带的平均行数等信息：

```sql
VACUUM VERBOSE contestant;
```

```text
INFO: statistics for "contestant":
storage id: 10000000000
total file size: 24576, total data size: 248
compression rate: 1.31x
total row count: 5, stripe count: 1, average rows per stripe: 5
chunk count: 6, containing data for dropped columns: 0, zstd compressed: 6
```

输出显示，Citus 使用 zstd 压缩算法获得了 1.31 倍的压缩比。该压缩比是数据插入时暂存在内存中的大小与最终条带中压缩后大小的比值。

由于压缩比的测量方式如此，它不一定等于同一张表使用行式存储和列式存储时的大小之比。要确定实际差异，必须创建包含相同数据的行式表和列式表，再比较其大小。

### 测量压缩 {#measuring-compression}

要测试压缩能够节省多少空间，创建一个数据量更大的示例。

```sql
-- first a wide table using row storage
CREATE TABLE perf_row(
  c00 int8, c01 int8, c02 int8, c03 int8, c04 int8, c05 int8, c06 int8, c07 int8, c08 int8, c09 int8,
  c10 int8, c11 int8, c12 int8, c13 int8, c14 int8, c15 int8, c16 int8, c17 int8, c18 int8, c19 int8,
  c20 int8, c21 int8, c22 int8, c23 int8, c24 int8, c25 int8, c26 int8, c27 int8, c28 int8, c29 int8,
  c30 int8, c31 int8, c32 int8, c33 int8, c34 int8, c35 int8, c36 int8, c37 int8, c38 int8, c39 int8,
  c40 int8, c41 int8, c42 int8, c43 int8, c44 int8, c45 int8, c46 int8, c47 int8, c48 int8, c49 int8,
  c50 int8, c51 int8, c52 int8, c53 int8, c54 int8, c55 int8, c56 int8, c57 int8, c58 int8, c59 int8,
  c60 int8, c61 int8, c62 int8, c63 int8, c64 int8, c65 int8, c66 int8, c67 int8, c68 int8, c69 int8,
  c70 int8, c71 int8, c72 int8, c73 int8, c74 int8, c75 int8, c76 int8, c77 int8, c78 int8, c79 int8,
  c80 int8, c81 int8, c82 int8, c83 int8, c84 int8, c85 int8, c86 int8, c87 int8, c88 int8, c89 int8,
  c90 int8, c91 int8, c92 int8, c93 int8, c94 int8, c95 int8, c96 int8, c97 int8, c98 int8, c99 int8
);

-- next a table with identical columns using columnar storage
CREATE TABLE perf_columnar(LIKE perf_row) USING COLUMNAR;
```

使用同一大型数据集填充这两个表。

```sql
INSERT INTO perf_row
  SELECT
    g % 00500, g % 01000, g % 01500, g % 02000, g % 02500, g % 03000, g % 03500, g % 04000, g % 04500, g % 05000,
    g % 05500, g % 06000, g % 06500, g % 07000, g % 07500, g % 08000, g % 08500, g % 09000, g % 09500, g % 10000,
    g % 10500, g % 11000, g % 11500, g % 12000, g % 12500, g % 13000, g % 13500, g % 14000, g % 14500, g % 15000,
    g % 15500, g % 16000, g % 16500, g % 17000, g % 17500, g % 18000, g % 18500, g % 19000, g % 19500, g % 20000,
    g % 20500, g % 21000, g % 21500, g % 22000, g % 22500, g % 23000, g % 23500, g % 24000, g % 24500, g % 25000,
    g % 25500, g % 26000, g % 26500, g % 27000, g % 27500, g % 28000, g % 28500, g % 29000, g % 29500, g % 30000,
    g % 30500, g % 31000, g % 31500, g % 32000, g % 32500, g % 33000, g % 33500, g % 34000, g % 34500, g % 35000,
    g % 35500, g % 36000, g % 36500, g % 37000, g % 37500, g % 38000, g % 38500, g % 39000, g % 39500, g % 40000,
    g % 40500, g % 41000, g % 41500, g % 42000, g % 42500, g % 43000, g % 43500, g % 44000, g % 44500, g % 45000,
    g % 45500, g % 46000, g % 46500, g % 47000, g % 47500, g % 48000, g % 48500, g % 49000, g % 49500, g % 50000
  FROM generate_series(1,50000000) g;

INSERT INTO perf_columnar
  SELECT
    g % 00500, g % 01000, g % 01500, g % 02000, g % 02500, g % 03000, g % 03500, g % 04000, g % 04500, g % 05000,
    g % 05500, g % 06000, g % 06500, g % 07000, g % 07500, g % 08000, g % 08500, g % 09000, g % 09500, g % 10000,
    g % 10500, g % 11000, g % 11500, g % 12000, g % 12500, g % 13000, g % 13500, g % 14000, g % 14500, g % 15000,
    g % 15500, g % 16000, g % 16500, g % 17000, g % 17500, g % 18000, g % 18500, g % 19000, g % 19500, g % 20000,
    g % 20500, g % 21000, g % 21500, g % 22000, g % 22500, g % 23000, g % 23500, g % 24000, g % 24500, g % 25000,
    g % 25500, g % 26000, g % 26500, g % 27000, g % 27500, g % 28000, g % 28500, g % 29000, g % 29500, g % 30000,
    g % 30500, g % 31000, g % 31500, g % 32000, g % 32500, g % 33000, g % 33500, g % 34000, g % 34500, g % 35000,
    g % 35500, g % 36000, g % 36500, g % 37000, g % 37500, g % 38000, g % 38500, g % 39000, g % 39500, g % 40000,
    g % 40500, g % 41000, g % 41500, g % 42000, g % 42500, g % 43000, g % 43500, g % 44000, g % 44500, g % 45000,
    g % 45500, g % 46000, g % 46500, g % 47000, g % 47500, g % 48000, g % 48500, g % 49000, g % 49500, g % 50000
  FROM generate_series(1,50000000) g;

VACUUM (FREEZE, ANALYZE) perf_row;
VACUUM (FREEZE, ANALYZE) perf_columnar;
```

对于这些数据，可以在列式表中看到压缩比超过 8 倍。

```sql
SELECT pg_total_relation_size('perf_row')::numeric/
       pg_total_relation_size('perf_columnar') AS compression_ratio;
```

```text
 compression_ratio
--------------------
 8.0196135873627944
(1 row)
```

### 示例 {#example}

列式存储适用于表分区。 有关示例，请参阅 `columnar_example`。

### 注意事项 {#gotchas}

- 列式存储按条带压缩数据。条带按事务创建，因此如果每个事务只插入一行，每行就会独占一个条带。单行条带的压缩效果和性能都比行式表差。应始终向列式表批量插入数据。

- 即使已经创建了很多小条带，也可以修复。在表上执行 `VACUUM (FULL)`：

  ```sql
  VACUUM (FULL) foo_table;
  ```

  某些情况下，创建新表、迁移数据后删除旧表可能更合适。操作如下：

  ```sql
  BEGIN;
  CREATE TABLE foo_compacted (LIKE foo) USING columnar;
  INSERT INTO foo_compacted SELECT * FROM foo;
  DROP TABLE foo;
  ALTER TABLE foo_compacted RENAME TO foo;
  COMMIT;
  ```

- 本身不可压缩的数据可能会带来问题，但列式存储仍可能有用：查询特定列时，载入内存的数据更少。
- 对于同时包含行式分区和列式分区的分区表，必须谨慎指定更新目标或过滤条件，确保只更新行式分区。

  - 如果操作针对特定的行式分区（例如 `UPDATE p2 SET i = i + 1`），就会成功；如果针对特定的列式分区（例如 `UPDATE p1 SET i = i + 1`），则会失败。
  - 如果操作针对分区表，且 WHERE 子句排除了所有列式分区（例如 `UPDATE parent SET i = i + 1 WHERE timestamp = '2020-03-15'`），就会成功。
  - 如果操作针对分区表，却没有排除所有列式分区，则会失败，即使实际要更新的数据只涉及行式表也不例外（例如 `UPDATE parent SET i = i + 1 WHERE n = 300`）。

### 局限性 {#limitations}

Citus 的未来版本将逐步消除以下限制：

- 仅追加（无 UPDATE 或 DELETE 支持）。
- 不支持空间回收（例如，回滚的事务可能仍占用磁盘空间）。
- 无位图索引扫描。
- 不支持 TID 扫描（tidscans）。
- 不支持采样扫描。
- 不支持 TOAST（以内联形式支持较大值）。
- 不支持 ON CONFLICT 语句（未指定目标的 DO NOTHING 操作除外）。
- 不支持元组锁（SELECT ... FOR SHARE、SELECT ... FOR UPDATE）。
- 不支持可串行化隔离级别。
- 仅支持 PostgreSQL 服务器版本 12 及更高版本。
- 不支持外键。
- 不支持逻辑解码。
- 不支持节点内并行扫描。
- 不支持 AFTER ... FOR EACH ROW 触发器。
- 不支持 UNLOGGED 列式表。

## 相关内容 {#related-content}

- [Citus 中的集群管理](/citus/operations/cluster-management/)
- [升级 Citus](/citus/operations/upgrade-citus/)
- [Citus 的诊断查询](/citus/operations/diagnostic-queries/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
