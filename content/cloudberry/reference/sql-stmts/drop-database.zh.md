---
title: "DROP DATABASE"
description: "删除数据库。"
weight: 1050
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-database.md"
---

## 概要 {#synopsis}

```sql
DROP DATABASE [IF EXISTS] <name>
```

## 描述 {#description}

`DROP DATABASE` 删除数据库，包括该数据库的系统目录条目和存放数据的目录。只有数据库所有者才能运行此命令。此外，当你或其他用户连接到目标数据库时，也不能运行此命令。（请连接到 `postgres` 或其他数据库后再发出此命令。）

> [!WARNING]
> `DROP DATABASE` 无法撤销。请谨慎使用！

## 参数 {#parameters}

**`IF EXISTS`**

如果数据库不存在，不报错，而是发出一条提示。

**`name`**

要删除的数据库名称。

## 注意事项 {#notes}

`DROP DATABASE` 不能在事务块中运行。

连接到目标数据库时不能运行此命令。因此，使用封装了此命令的 dropdb 程序可能更方便。

## 示例 {#examples}

删除名为 `testdb` 的数据库：

```sql
DROP DATABASE testdb;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP DATABASE` 语句。

## 另见 {#see-also}

[`ALTER DATABASE`](/cloudberry/reference/sql-stmts/alter-database/), [`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/)
