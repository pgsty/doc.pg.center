---
title: 快速入门与使用
linkTitle: 快速入门
description: 安装 OrioleDB、创建表，并了解压缩、索引、恢复和当前限制。
weight: 10
type: docs
search_keywords: ["OrioleDB", "getting started", "USING orioledb", "installation", "安装"]
upstream_link: https://www.orioledb.com/docs/usage/getting-started
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-play
---


OrioleDB 使用 PostgreSQL 内置的表访问方法 API。创建表时，可以指定 `USING orioledb;`。

## 快速入门 {#quick-start}

### 启动 PostgreSQL {#start-postgresql}

OrioleDB 扩展需要 PostgreSQL 的可插拔存储支持。在 PostgreSQL 社区合并[所需补丁](/zh/orioledb/introduction/#patch-set)之前，可以使用 OrioleDB Docker 镜像在本机启动 PostgreSQL：

``` bash
docker run -d --name orioledb -p 5432:5432 orioledb/orioledb:latest-pg17
```

### 启用扩展 {#enable-the-extension}

执行以下命令启用 OrioleDB 扩展：

``` sql
CREATE EXTENSION orioledb;
```

### 创建表 {#create-tables}

下面定义一个存储博客文章的 `blog_post` 表，包含两个索引：`id` 列上的主键索引和 `published_at` 列上的二级索引。

``` sql
-- Create a table
CREATE TABLE blog_post
(
    id int8 NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    author text NOT NULL,
    published_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    views bigint NOT NULL,
    PRIMARY KEY(id)
) USING orioledb; -- Define the storage engine

-- Create an index
CREATE INDEX blog_post_published_at ON blog_post(published_at);
```

OrioleDB 使用索引组织表，因此主键的选择对性能至关重要。如果没有指定主键，系统会在虚拟的 `ctid` 列上创建一个隐藏的代理主键。

### 查询表 {#query-tables}

使用常规 DML 语句查询和修改表，包括 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 和 `INSERT ON CONFLICT`。

例如：

``` sql
INSERT INTO blog_post (id, title, body, author, views)
VALUES (1, 'Hello, World!', 'This is my first blog post.', 'John Doe', 1000);

SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;
```

### 查看查询计划 {#view-query-plans}

涉及 OrioleDB 表的查询也可以像往常一样使用 `EXPLAIN` 查看执行计划。

``` sql
EXPLAIN SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;
```

结果：

``` bash
                                                 QUERY PLAN
------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.15..1.67 rows=10 width=120)
   ->  Index Scan Backward using blog_post_published_at on blog_post  (cost=0.15..48.95 rows=320 width=120)
(2 rows)
```

``` sql
EXPLAIN SELECT * FROM blog_post WHERE id = 1;
```

结果：

``` bash
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Index Scan using blog_post_pkey on blog_post  (cost=0.15..8.17 rows=1 width=120)
   Index Cond: (id = 1)
(2 rows)
```

`EXPLAIN (ANALYZE, BUFFERS)` 可以显示页面访问统计信息。

``` sql
# EXPLAIN (ANALYZE, BUFFERS)
  SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;
                                                                       QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.29..0.54 rows=10 width=42) (actual time=0.100..0.210 rows=10 loops=1)
   ->  Index Scan Backward using blog_post_published_at on blog_post  (cost=0.29..251.27 rows=9999 width=42) (actual time=0.097..0.202 rows=10 loops=1)
 Planning:
   Buffers: shared hit=35
 Planning Time: 1.147 ms
 Execution Time: 0.284 ms
(6 rows)
```

## 进阶用法 {#advanced-usage}

### 默认使用 OrioleDB 表 {#use-orioledb-tables-by-default}

如果希望所有新建表都使用 `orioledb` 访问方法，而不用每次在 `CREATE TABLE` 中显式指定，请在 PostgreSQL 配置文件中添加：

`default_table_access_method = 'orioledb'`

注意：这不会影响系统目录，它们只能使用 `heap`。设置该参数之前创建的表也会保留原有的访问方法。

### 排序规则 {#collations}

OrioleDB 表支持 ICU、C、POSIX，以及 PostgreSQL 17 及更高版本的内置排序规则。请确保集群或数据库的默认排序规则使用这些提供者之一；否则，需要为表中的每个 `text` 字段指定 `COLLATE`。

对于 OrioleDB 表的字段和索引所使用的排序规则，`ALTER COLLATION REFRESH VERSION` 也被禁用。

### 块级数据压缩 {#block-level-data-compression}

OrioleDB 实现了块级压缩。压缩级别是 `-1` 到 `22` 之间的整数。`-1` 表示不压缩（默认值），`0` 到 `22` 对应 zstd 库的压缩级别。

以下选项控制表的压缩级别：

- `compress`：所有表数据结构的压缩级别。`-1` 表示禁用该表的压缩；未指定时使用 `orioledb.default_compress`。
- `primary_compress`：表主键的压缩级别。值为 `-1` 时，如果表的 `compress` 为正数，则继承该值；否则使用 `orioledb.default_primary_compress`。
- `toast_compress`：表中 TOAST 值的压缩级别。值为 `-1` 时，如果表的 `compress` 为正数，则继承该值；否则使用 `orioledb.default_toast_compress`。

单个索引也有 `compress` 选项，用于控制该索引的压缩级别，并覆盖表的 `compress` 设置。

``` sql
CREATE TABLE compression_test
(
  id int8 NOT NULL,
  value1 float8 NOT NULL,
  value2 text NOT NULL,
  PRIMARY KEY(id)
)  USING orioledb
   WITH (compress = 5, toast_compress = 10, primary_compress = -1);

CREATE INDEX compression_test_value1_idx ON compression_test(value1)
    WITH (compress = 22)
CREATE INDEX compression_test_value2_idx ON compression_test(value2);
```

在这个例子中，`compression_test` 表的主键使用 `orioledb.default_primary_compress` 指定的压缩级别，TOAST 值使用级别 `10`，`compression_test_value1_idx` 索引使用级别 `22`，`compression_test_value2_idx` 索引使用级别 `5`。

### 填充因子 {#fillfactor}

OrioleDB 的表和索引支持 `fillfactor` 选项，其用法类似于 PostgreSQL 的 `heap` 表和索引，参见 [heap 文档](https://www.postgresql.org/docs/current/sql-createtable.html#RELOPTION-FILLFACTOR)和[索引文档](https://www.postgresql.org/docs/current/sql-createindex.html#INDEX-RELOPTION-FILLFACTOR)。适当降低填充因子，可以通过预留一些磁盘空间来加快表数据的修改。对于预计修改频繁的表，建议设置该选项。

``` sql
CREATE TABLE o_test_fillfactor
(
	 f1 text,
	 f2 varchar,
	 f3 integer,
	 PRIMARY KEY(f1)
) USING orioledb WITH (fillfactor = 60);

CREATE INDEX o_test_fillfactor_ix1 ON o_test_fillfactor(f2) WITH (fillfactor = 80);
```

在 `heap` 表中，较低的 `fillfactor` 主要通过为 HOT 更新的元组预留空间来加快更新；它也会把并发修改分散到更多页面，从而减少页锁争用。`orioledb` 表的页面不存储旧元组版本，而且页面分为多个块，因此原本就没有这些限制。不过，OrioleDB 使用索引组织表，会根据 B 树结构将元组插入特定页面。当叶子页没有足够空间容纳新元组时，`fillfactor` 可以减少页面分裂，从而同时加快插入和更新。它对表和索引的作用相同。

填充因子可以随时修改：

``` sql
ALTER TABLE o_test_fillfactor SET (fillfactor = 20);
ALTER INDEX o_test_fillfactor_ix1 SET (fillfactor = 50);
```

### 序列缓存 {#sequence-caching}

当操作严格限定在 OrioleDB 表内时，OrioleDB 会绕过 PostgreSQL 原生的事务 ID（XID）分配和堆表预写日志（WAL），以提高性能。但 PostgreSQL 序列以 `heap` 关系实现，调用 `nextval()` 会修改堆结构，强制分配完整的 PostgreSQL XID，使 OrioleDB 的事务优化失效。

对于使用序列的列，可以为序列配置 `CACHE`，避免不必要的 XID 分配：

``` sql
CREATE SEQUENCE my_seq CACHE 100;
```

启用缓存后，只有首次调用 `nextval()` 获取一批值时，才需要修改 `heap` 并分配 XID。同一会话中的后续调用从内存取值，因而能够保留 OrioleDB 的事务处理优化。

> [!NOTE]
>
> 对于大量小事务的工作负载，这项优化尤其关键。对大事务而言，XID 分配的成本被充分摊薄，性能损失通常可以忽略。

### 计算撤销日志大小 {#undo-log-size-calculation}

OrioleDB 将部分修改数据存放在临时撤销日志（UNDO 日志）中。将这类数据与关系文件分开存储更便于管理，也不容易产生膨胀，但 PostgreSQL 函数报告的表和数据库大小不会包含撤销日志。可以使用专门的函数统计这些临时数据：

``` sql
SELECT * FROM orioledb_undo_size();
```

撤销数据分为三类统计：系统撤销数据、用户页级撤销数据和用户行级撤销数据。

### 验证表的完整性 {#verifying-table-integrity}

`verify_orioledb()` 检查 OrioleDB 关系的所有 B 树，包括主键、二级、TOAST 和桥接索引；每个未通过检查的索引返回一行。结果为空表示该关系正常。

``` sql
SELECT * FROM verify_orioledb('blog_post'::regclass);
```

``` sql
-- thorough_check = true also validates the on-disk free space map
SELECT * FROM verify_orioledb('blog_post'::regclass, true);
```

该函数只获取 `AccessShareLock`，因此不会阻塞并发读写。如果检查点正在运行，它会等待受影响树的检查点完成，避免误报。

`verify_orioledb()` 还接入了 PostgreSQL 的 `amcheck` 集成，因此 [`pg_amcheck`](https://www.postgresql.org/docs/current/app-pgamcheck.html) 可以同时检查 OrioleDB 关系和堆关系：

``` bash
pg_amcheck -d mydb -t public.blog_post
pg_amcheck -d mydb                       # all checkable relations in the database
```

### 删除数据 {#data-deletion}

OrioleDB 会自动合并稀疏页面。因此，大量行被删除后，数据页会释放并可供后续使用。目前这种情况下数据文件还不会缩小，但这一功能计划很快实现。

### 检查点、WAL 与恢复 {#checkpoints-wal--recovery}

OrioleDB 有自己的恢复机制：写时复制检查点和行级 WAL。不过，OrioleDB 的检查点和 WAL 都集成在 PostgreSQL 中。PostgreSQL 的检查点进程也会处理 OrioleDB 表。PostgreSQL WAL 流同时包含内置表的 WAL 记录和 OrioleDB 表的行级 WAL 记录。无论 PostgreSQL 集群的 `data_checksums` 设置如何，OrioleDB 始终存储并验证页面校验和。

根据行级 WAL 记录执行恢复可能需要较多 CPU 资源，因此 OrioleDB 实现了表的并行恢复。它会启动自己的恢复工作进程池，每个进程负责重放一部分 WAL 记录。

OrioleDB 也有自己的后台写进程池，池大小由 GUC 参数 `orioledb.bgwriter_num_workers` 决定。使用多个后台写进程可以提高现代硬件的 I/O 利用率。

### 实验性块设备支持 {#experimental-support-of-the-block-devices}

OrioleDB 实验性地支持直接与块设备交互，以消除文件系统的开销。

在这种模式下，表数据的主要部分存储在文件系统中，而少量元数据仍然保存在数据目录中。

当前的块设备实现存在内存泄漏，即使实际数据量远小于块设备容量，也可能出现 `device file overflow` 错误。遇到这种情况，只能重新初始化数据目录。

我们计划尽快修复内存泄漏，并开发用于监控块设备剩余空间的工具。

启用块设备模式需要指定 `orioledb.device_filename` 和 `orioledb.device_length` 两个 GUC 参数。启用 `orioledb.use_mmap` 后，将通过 `mmap` 连接块设备。这种方式适合直接连接数据总线的 NVRAM。不建议对普通设备使用 `mmap` 模式，因为 Linux 当前的 `mmap` 并发实现存在严重问题。

### B 树以外索引的实验性支持 {#experimental-support-of-indexes-other-than-btree}

OrioleDB 实验性地支持 B 树以外的索引。实现方式是在非 B 树索引与 OrioleDB 表之间增加一个内部“桥接索引”。创建第一个非 B 树索引时，会自动添加桥接索引。

``` sql
CREATE INDEX blog_post_title_gin_idx ON blog_post USING GIN (title);
```

无需手动为表创建桥接索引，但也可以手动创建：

``` sql
ALTER TABLE blog_post SET (index_bridging);
```

删除表上所有使用桥接机制的索引后，内部“桥接索引”不会自动删除。如果不再计划添加非 B 树索引，可以删除这个多余的内部索引：

``` sql
ALTER TABLE blog_post RESET (index_bridging);
```

注意：也可以将 B 树索引构建为使用桥接机制的索引，但仅限测试，不建议这样使用。

``` sql
CREATE INDEX blog_post_title_idx ON blog_post USING btree(title) with (orioledb_index = off);
```

## 当前限制 {#current-limitations}

OrioleDB 仍处于开发阶段，暂时存在以下限制。

1. `pg_rewind` 会完整复制 OrioleDB 表。OrioleDB 计划很快实现通过 `pg_rewind` 增量复制。
2. OrioleDB 支持并行顺序扫描和并行索引扫描，但尚不支持其他类型的并行扫描。
3. OrioleDB 不支持预备事务。
4. 非 B 树索引支持仍处于实验阶段。
5. 位图扫描仅支持主键类型为 int4、int8 或 ctid 的表。
6. OrioleDB 的行级并发存在一些[差异](/zh/orioledb/architecture/row-level-concurrency/)。
7. 尚不支持 `CLUSTER` 和 `VACUUM FULL`，因为还没有实现这两个命令所需的表重写。而且，`CLUSTER` 对索引组织表的意义也不大。
8. 支持 `CREATE INDEX/REINDEX CONCURRENTLY`，但存在[限制](/zh/orioledb/architecture/concurrent-index/)。
9. OrioleDB 表尚不支持 `Sample Scans`。
10. OrioleDB 没有实现真正的可串行化快照隔离。GUC 参数 `orioledb.serializable` 决定如何处理 SERIALIZABLE 事务：
    - `table_lock`（默认）：以粗粒度的重量级 `ExclusiveLock` 保护 SERIALIZABLE 事务访问的每个关系。行为正确，但比较悲观：互不冲突的并发工作负载也会退化为串行执行。
    - `error`：以 `ERRCODE_FEATURE_NOT_SUPPORTED` 拒绝 SERIALIZABLE 事务，这是此前的行为。
    - `repeatable_read`：仅对 OrioleDB 表将 SERIALIZABLE 视为 `REPEATABLE READ`，不获取额外锁。OrioleDB 的 CSN 快照已经提供事务内稳定的读取。同一事务中的堆表仍照常使用 PostgreSQL 的 SSI。
11. 只有声明为 `SCROLL` 的游标才支持向后读取。
12. OrioleDB 始终使用数据页校验和。初始化数据库集群时禁用数据校验和，对 OrioleDB 表没有影响。
13. PostgreSQL 序列以堆关系为基础。访问序列（例如调用 `nextval()`）会强制分配完整的 PostgreSQL 事务 ID（XID）；除非使用序列缓存，否则会绕过 OrioleDB 优化后的事务机制。

## 相关链接 {#links}

参见 [OrioleDB 配置说明](/zh/orioledb/usage/configuration/)、[实验性存算分离模式](/zh/orioledb/usage/decoupled-storage/)和[实验性撤销日志回退](/zh/orioledb/usage/rewind/)。
