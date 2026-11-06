---
title: "REINDEX"
description: "重建索引。"
weight: 1590
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/reindex.md"
---

## 语法概要 {#synopsis}

```sql
REINDEX [ (VERBOSE) ] { INDEX | TABLE | SCHEMA | DATABASE | SYSTEM } <name>
```

## 说明 {#description}

`REINDEX` 使用索引所属表中存储的数据重建索引，替换旧的索引副本。以下几种情况适合使用 `REINDEX`：

- 索引已损坏，不再包含有效数据。尽管理论上这种情况不应发生，但实际上软件缺陷或硬件故障可能导致索引损坏。`REINDEX` 提供了一种恢复方法。
- 索引发生膨胀，即包含许多空页或几乎为空的页。在某些不常见的访问模式下，Apache Cloudberry 中的 B-树索引可能出现这种情况。`REINDEX` 通过写入一个不含无效页的新索引版本来减少索引占用的空间。
- 更改了索引的某个存储参数（例如 `fillfactor`），并希望确保更改已完全生效。

## 参数 {#parameters}

**`INDEX`**

重建指定的索引。

**`TABLE`**

重建指定表的所有索引。如果表具有辅助的“TOAST”表，也会重建其索引。

**`SCHEMA`**

重建指定模式的所有索引。如果该模式中的表具有辅助的“TOAST”表，也会重建其索引。共享系统目录上的索引也会处理。不能在事务块内执行这种形式的 `REINDEX`。

**`DATABASE`**

重建当前数据库内的所有索引。共享系统目录上的索引也会处理。不能在事务块内执行这种形式的 `REINDEX`。

**`SYSTEM`**

重建当前数据库内系统目录上的所有索引，包括共享系统目录上的索引。不处理用户表上的索引。不能在事务块内执行这种形式的 `REINDEX`。

**`name`**

要重建索引的具体索引、表或数据库的名称。索引名和表名可以用模式名限定。目前，`REINDEX DATABASE` 和 `REINDEX SYSTEM` 只能重建当前数据库的索引，因此其参数必须与当前数据库名称一致。

**`VERBOSE`**

在重建每个索引时打印进度报告。

## 注意事项 {#notes}

`REINDEX` 会对系统目录表加锁，可能影响当前运行的查询。为避免干扰正在进行的业务操作，应安排在活动较少的时段执行 `REINDEX`。

`REINDEX` 与删除并重建索引类似，都会从头重建索引内容。不过，加锁方面的考虑有很大不同。`REINDEX` 会阻止对索引所属表的写入，但不阻止读取。它还会对正在处理的特定索引获取 `ACCESS EXCLUSIVE` 锁，阻塞尝试使用该索引的读取。相比之下，`DROP INDEX` 会短暂地对所属表获取 `ACCESS EXCLUSIVE` 锁，同时阻塞写入和读取。后续的 `CREATE INDEX` 会阻止写入，但不阻止读取；由于索引不存在，读取不会尝试使用它，因此不会因此阻塞，但读取可能被迫进行代价高昂的顺序扫描。

重建单个索引或表的索引要求执行者是该索引或表的所有者。重建模式或数据库的索引要求执行者是该模式或数据库的所有者。因此，非超级用户有时也可以重建其他用户所拥有表的索引。不过，有一个特殊例外：当非超级用户执行 `REINDEX DATABASE`、`REINDEX SCHEMA` 或 `REINDEX SYSTEM` 时，Apache Cloudberry 会跳过共享目录上的索引，除非该用户拥有该目录（通常并非如此）。当然，超级用户始终可以重建任何索引。

`REINDEX` 不会更新索引的 `reltuples` 和 `relpages` 统计信息。要更新这些统计信息，请在重建索引后对表执行 `ANALYZE`。

## 示例 {#examples}

重建单个索引：

```sql
REINDEX INDEX my_index;
```

重建表 `my_table` 上的所有索引：

```sql
REINDEX TABLE my_table;
```

在不信任系统索引当前有效性的情况下，重建特定数据库中的所有索引：

```sql
$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

## 兼容性 {#compatibility}

SQL 标准中没有 `REINDEX` 命令。

## 另请参阅 {#see-also}

[CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/), [DROP INDEX](/cloudberry/reference/sql-stmts/drop-index/), [VACUUM](/cloudberry/reference/sql-stmts/vacuum/), reindexdb
