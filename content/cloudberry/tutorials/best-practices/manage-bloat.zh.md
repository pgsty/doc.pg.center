---
title: "管理数据库膨胀"
description: "数据库膨胀会出现在堆表、AO 表、索引和系统目录中，并影响数据库性能和磁盘使用率。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/manage-bloat.md"
---

可以检测数据库膨胀，并将其从数据库中清除。

- [关于膨胀](#about-bloat)
- [检测膨胀](#detect-bloat)
- [清除数据库表膨胀](#remove-bloat-from-database-tables)
- [清除 AO 表膨胀](#remove-bloat-from-append-optimized-tables)
- [清除索引膨胀](#remove-bloat-from-indexes)
- [清除系统目录膨胀](#remove-bloat-from-system-catalogs)

## 关于膨胀 {#about-bloat}

数据库膨胀是曾被表或索引使用、现在可以由数据库重新使用、但尚未回收的磁盘空间。更新表或索引时会产生膨胀。

由于 Apache Cloudberry 堆表使用 PostgreSQL 多版本并发控制（MVCC）存储实现，被删除或更新的行会从数据库中逻辑删除，但该行的不可见副本仍然保留在表中。此外，如果表有索引，指向这些不可见行的索引条目也会保留。运行 `VACUUM` 会将过期行标记为空闲空间，供后续插入重新使用；如果存在对应的索引条目，也会删除这些条目。

频繁更新的表包含少量或中等数量的过期行和可用空间是正常现象；随着新数据添加，这些空间会重新使用。但如果表持续增长，导致活动数据只占空间的一小部分，表就会出现严重膨胀。膨胀的表需要更多磁盘存储和额外 I/O，可能拖慢查询执行。如果膨胀表具有唯一索引，还可能拖慢数据摄取，因为唯一性验证会读取前述索引条目。

> **重要** 大量执行 `UPDATE` 和 `DELETE` 操作后，对单个表运行 `VACUUM` 非常重要，这样可以避免以后必须运行 `VACUUM FULL`。

定期对表运行 `VACUUM` 可以防止表增长过大。如果表确实严重膨胀，则必须使用 `VACUUM FULL` 压缩表数据。

如果空闲空间映射不能容纳所有过期行，`VACUUM` 就无法回收溢出空闲空间映射的过期行所占空间。只有运行 `VACUUM FULL` 才能回收磁盘空间。该命令会锁定表、创建新表、将表数据复制到新表，然后删除旧表。这是高成本操作，对大型表可能需要非常长的时间才能完成。

> **警告** `VACUUM FULL` 会获取表的 `ACCESS EXCLUSIVE` 锁。不应运行 `VACUUM FULL`。如果要对表运行 `VACUUM FULL`，应在用户和应用不需要访问被清理表的时段运行，例如低活动时段或维护窗口。

## 检测膨胀 {#detect-bloat}

`ANALYZE` 语句收集的统计信息可以用来计算存储表所需的预期磁盘页数。预期页数与实际页数之差可以衡量膨胀程度。`gp_toolkit` 模式提供 [`gp_bloat_diag`](/cloudberry/reference/sys-catalogs/gp_toolkit/#gp_bloat_diag) 视图，通过比较预期页数与实际页数的比率识别表膨胀。使用该视图前，确保数据库中所有表的统计信息都是最新的，然后运行以下 SQL：

```sql
gpadmin=# SELECT * FROM gp_toolkit.gp_bloat_diag;
 bdirelid | bdinspname | bdirelname | bdirelpages | bdiexppages |                bdidiag                
----------+------------+------------+-------------+-------------+---------------------------------------
    21488 | public     | t1         |          97 |           1 | significant amount of bloat suspected
(1 row)
```

结果只包含存在中度或严重膨胀的表。当实际页数与预期页数之比大于 4 且小于 10 时，报告为中度膨胀；比率大于 10 时，报告为严重膨胀。

`gp_toolkit.gp_bloat_expected_pages` 视图列出每个数据库对象实际使用的页数和预期使用的页数。

```sql
gpadmin=# SELECT * FROM gp_toolkit.gp_bloat_expected_pages LIMIT 5;
 btdrelid | btdrelpages | btdexppages 
----------+-------------+-------------
    10789 |           1 |           1
    10794 |           1 |           1
    10799 |           1 |           1
     5004 |           1 |           1
     7175 |           1 |           1
(5 rows)
```

`btdrelid` 是表的对象 ID。`btdrelpages` 列报告表使用的页数；`btdexppages` 列报告预期页数。同样，这些数字基于表统计信息，因此务必对发生变化的表运行 `ANALYZE`。

## 清除数据库表膨胀 {#remove-bloat-from-database-tables}

`VACUUM` 命令将过期行加入空闲空间映射，使空间能够重新使用。对频繁更新的表定期运行 `VACUUM` 时，过期行占用的空间可以及时重新使用，从而防止表文件继续增大。在空闲空间映射填满前运行 `VACUUM` 同样很重要。对于频繁更新的表，可能需要每天至少运行一次 `VACUUM`，防止表发生膨胀。

> **警告** 表严重膨胀时，最好先运行 `VACUUM`，再运行 `ANALYZE`。如果样本包含空页，分析严重膨胀的表可能生成质量较差的统计信息，因此应在分析前清理膨胀的表。

表积累了严重膨胀时，单独运行 `VACUUM` 命令是不够的。对于小表，运行 `VACUUM FULL <table_name>` 可以回收溢出空闲空间映射的行所占空间，缩小表文件大小。但是，`VACUUM FULL` 是高成本操作，需要 `ACCESS EXCLUSIVE` 锁；对大型表而言，完成时间可能很长且无法预测。应在用户和应用不需要访问被清理表的时段运行 `VACUUM FULL`，例如低活动时段或维护窗口。

## 清除 AO 表膨胀 {#remove-bloat-from-append-optimized-tables}

AO 表的处理方式与堆表大不相同。虽然 AO 表允许更新、插入和删除操作，但这些操作没有经过优化，并不建议在 AO 表上执行。如果遵循这一建议，将 AO 表用于*一次加载、多次读取*的工作负载，那么对 AO 表运行 `VACUUM` 几乎会立即完成。

如果确实对 AO 表运行 `UPDATE` 或 `DELETE` 命令，过期行会记录在辅助位图中，而不是空闲空间映射中。`VACUUM` 是回收空间的唯一方式。对包含过期行的 AO 表运行 `VACUUM` 时，会通过重写整个表来压缩表，并去除过期行。但是，如果表中过期行的百分比超过配置参数 `gp_appendonly_compaction_threshold` 的值，则不会执行任何操作；该参数默认值为 10（10%）。每个 Segment 都会单独检查此阈值，因此某条 `VACUUM` 语句可能在部分 Segment 上压缩 AO 表，而在其他 Segment 上不压缩。将 `gp_appendonly_compaction` 参数设为 `no` 可以停用 AO 表压缩。

## 清除索引膨胀 {#remove-bloat-from-indexes}

`VACUUM` 命令只能从表中回收空间。要从索引中回收空间，应使用 `REINDEX` 命令重新创建索引。

要重建表上的所有索引，运行 `REINDEX *table_name*;`。要重建特定索引，运行 `REINDEX *index_name*;`。`REINDEX` 会将索引的 `reltuples` 和 `relpages` 设为 0（零）。要更新这些统计信息，请在重建索引后对表运行 `ANALYZE`。

## 清除系统目录膨胀 {#remove-bloat-from-system-catalogs}

Apache Cloudberry 系统目录表是堆表，可能会随时间膨胀。创建、更改或删除数据库对象时，过期行会留在系统目录中。使用 `gpload` 加载数据会加剧膨胀，因为 `gpload` 会创建和删除外部表。（建议使用 `gpfdist` 加载数据，而不是使用 `gpload`。）

系统目录膨胀会增加扫描表所需的时间，例如生成执行计划时。系统目录会被频繁扫描；如果发生膨胀，系统整体性能就会下降。

建议每晚、至少每周对系统目录表运行 `VACUUM`。同时对系统目录表运行 `REINDEX SYSTEM` 可以清除索引膨胀。也可以使用带 `-s`（`--system`）选项的 `reindexdb` 工具重建系统表索引。清除目录膨胀后，运行 `ANALYZE` 更新目录表统计信息。

以下是 Apache Cloudberry 系统目录维护步骤。

1. 对系统目录表执行 `REINDEX`，重建系统目录索引。这样可以清除索引膨胀并改善 `VACUUM` 性能。

    > **注意** 对系统目录表执行 `REINDEX` 时会发生锁定，可能影响当前运行的查询。可以在低活动时段安排 `REINDEX` 操作，避免中断正在进行的业务操作。

2. 对系统目录表执行 `VACUUM`。
3. 对系统目录表执行 `ANALYZE`，更新表统计信息。

如果在维护窗口期间执行系统目录维护，并且因时间限制需要停止进程，请运行 Apache Cloudberry 函数 `pg_cancel_backend(<PID>)`，安全地停止 Apache Cloudberry 进程。

以下脚本会对系统目录运行 `REINDEX`、`VACUUM` 和 `ANALYZE`。

```shell
#!/bin/bash
DBNAME="<database_name>"
SYSTABLES="' pg_catalog.' || relname || ';' from pg_class a, pg_namespace b \
where a.relnamespace=b.oid and b.nspname='pg_catalog' and a.relkind='r'"

reindexdb -s -d $DBNAME
psql -tc "SELECT 'VACUUM' || $SYSTABLES" $DBNAME | psql -a $DBNAME
analyzedb -a -s pg_catalog -d $DBNAME
```

如果系统目录发生严重膨胀，必须在计划的停机窗口期间运行 `VACUUM FULL`。在此期间，停止系统上的所有目录活动；`VACUUM FULL` 会对系统目录获取 `ACCESS EXCLUSIVE` 锁。定期对系统目录表运行 `VACUUM` 可以避免执行这一成本更高的过程。

以下是进行密集系统目录维护的步骤。

1. 停止 Apache Cloudberry 系统上的所有目录活动。
2. 对系统目录表执行 `VACUUM FULL`。参见下面的注意事项。
3. 对系统目录表执行 `ANALYZE`，更新目录表统计信息。

> **注意** 系统目录表 `pg_attribute` 通常是最大的目录表。如果 `pg_attribute` 表严重膨胀，对其执行 `VACUUM FULL` 可能需要很长时间，可能需要单独执行。以下两个条件同时存在时，说明 `pg_attribute` 表严重膨胀，并且 `VACUUM FULL` 可能需要很长时间：

- `pg_attribute` 表包含大量记录。
- `gp_toolkit.gp_bloat_diag` 视图中 `pg_attribute` 的诊断消息为 `significant amount of bloat`。
