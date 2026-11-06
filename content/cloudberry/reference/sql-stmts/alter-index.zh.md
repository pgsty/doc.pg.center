---
title: "ALTER INDEX"
description: "更改索引的定义。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-index.md"
---

## 概要 {#synopsis}

```sql
ALTER INDEX [ IF EXISTS ] <name> RENAME TO <new_name>
ALTER INDEX [ IF EXISTS ] <name> SET TABLESPACE <tablespace_name>
ALTER INDEX <name> ATTACH PARTITION <index_name>
ALTER INDEX <name DEPENDS ON EXTENSION <extension_name>
ALTER INDEX [ IF EXISTS ] <name> SET ( <storage_parameter> [= <value>] [, ...] )
ALTER INDEX [ IF EXISTS ] <name> RESET ( <storage_parameter>  [, ...] )
ALTER INDEX [ IF EXISTS ] <name> ALTER [ COLUMN ] <column_number>
    SET STATISTICS <integer>
ALTER INDEX ALL IN TABLESPACE <name> [ OWNED BY <role_name> [, ... ] ]
    SET TABLESPACE <new_tablespace> [ NOWAIT ]
```

## 描述 {#description}

`ALTER INDEX` 更改现有索引的定义。下文描述了几种子形式。请注意，每种子形式所需的锁级别可能不同。除非明确说明，否则持有 `ACCESS EXCLUSIVE` 锁。当列出多个子命令时，所持有的锁将是所有子命令所需锁中最严格的那个。

**`RENAME`**

更改索引的名称。如果该索引与某个表约束（`UNIQUE`、`PRIMARY KEY` 或 `EXCLUDE`）相关联，该约束也会被重命名。这对已存储的数据没有影响。

重命名索引会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`SET TABLESPACE`**

将索引的表空间更改为指定的表空间，并把与该索引相关联的数据文件移动到新的表空间。要更改索引的表空间，你必须拥有该索引，并且在新表空间上具有 `CREATE` 权限。使用 `ALL IN TABLESPACE` 形式可以移动当前数据库中某个表空间内的所有索引，该形式会锁定所有要移动的索引，然后逐个移动。此形式还支持 `OWNED BY`，它只会移动由所指定角色拥有的索引。如果指定了 `NOWAIT` 选项，则当命令无法立即获取所需的全部锁时，命令将失败。请注意，系统目录不会被此命令移动；如有需要，请改用 `ALTER DATABASE` 或显式的 `ALTER INDEX` 调用。另请参见 [CREATE TABLESPACE](/cloudberry/reference/sql-stmts/create-tablespace/)。

**`ATTACH PARTITION`**

使指定名称的索引附加到被更改的索引上。该指定索引必须位于包含被更改索引的表的某个分区上，并且具有等价的定义。已附加的索引不能被单独删除，并且如果其父索引被删除，它将被自动删除。

**`DEPENDS ON EXTENSION`**

此形式将索引标记为依赖于扩展，这样，如果扩展被删除，该索引也会被自动删除。

**`SET ( storage_parameter [= value] [, ... ] )`**

更改索引的一个或多个索引方法特定的存储参数。关于可用的参数，详情请参见 [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/)。请注意，此命令不会立即修改索引内容；根据参数的不同，你可能需要使用 [REINDEX](/cloudberry/reference/sql-stmts/reindex/) 重建索引才能获得期望的效果。

**`RESET ( storage_parameter [, ... ] )`**

将索引的一个或多个索引方法特定的存储参数重置为其默认值。与 `SET` 一样，可能需要执行 `REINDEX` 才能完全更新索引。

**`ALTER [ COLUMN ] column_number SET STATISTICS integer`**

此形式为后续的 `ANALYZE` 操作设置每列的统计信息收集目标，但只能用于定义为表达式的索引列。由于表达式没有唯一的名称，我们使用索引列的序号来引用它们。目标可以设置在 0 到 10000 的范围内；或者将其设置为 `-1`，以恢复使用系统默认的统计目标（`default_statistics_target`）。

## 参数 {#parameters}

**`IF EXISTS`**

如果索引不存在，不要抛出错误。在这种情况下，Apache Cloudberry 会发出一个通知。

**`column_number`**

序号指的是索引列的序数（从左到右）位置。

**`name`**

要更改的现有索引的名称（可以是模式限定的）。

**`new_name`**

索引的新名称。

**`tablespace_name`**

索引将被移动到的表空间。

**`storage_parameter`**

索引方法特定的存储参数的名称。

**`value`**

索引方法特定的存储参数的新值。根据参数的不同，它可能是一个数字或一个单词。

## 注解 {#notes}

这些操作也可以通过 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 完成。实际上，`ALTER INDEX` 只是 `ALTER TABLE` 中适用于索引的那些形式的别名。

以前有一个 `ALTER INDEX OWNER` 变体，但现在它会被忽略（并给出警告）。索引不能拥有与其表不同的所有者。更改表的所有者会自动一并更改索引的所有者。

不允许更改系统目录索引的任何部分。

## 示例 {#examples}

重命名一个现有索引：

```sql
ALTER INDEX distributors RENAME TO suppliers;
```

将索引移动到另一个表空间：

```sql
ALTER INDEX distributors SET TABLESPACE fasttablespace;
```

更改索引的填充因子（假设该索引方法支持）：

```sql
ALTER INDEX distributors SET (fillfactor = 75);
REINDEX INDEX distributors;
```

为表达式索引设置统计信息收集目标：

```sql
CREATE INDEX coord_idx ON measured (x, y, (z + t));
ALTER INDEX coord_idx ALTER COLUMN 3 SET STATISTICS 1000;
```

## 兼容性 {#compatibility}

`ALTER INDEX` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/)、[REINDEX](/cloudberry/reference/sql-stmts/reindex/)、[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)
