---
title: "SELECT INTO"
description: "根据查询结果定义新表。"
weight: 1670
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/select-into.md"
---

## 概要 {#synopsis}

```sql
[ WITH [ RECURSIVE ] <with_query> [, ...] ]
SELECT [ALL | DISTINCT [ON ( <expression> [, ...] )]]
    * | <expression> [ [AS] <output_name> ] [, ...]
    INTO [TEMPORARY | TEMP | UNLOGGED ] [TABLE] <new_table>
    [FROM <from_item> [, ...]]
    [WHERE <condition>]
    [GROUP BY <expression> [, ...]]
    [HAVING <condition> [, ...]]
    [WINDOW <window_name> AS ( <window_definition> ) [, ...]]
    [{UNION | INTERSECT | EXCEPT} [ALL | DISTINCT ] <select>]
    [ORDER BY <expression> [ASC | DESC | USING <operator>] [NULLS {FIRST | LAST}] [, ...]]
    [LIMIT {<count> | ALL}]
    [OFFSET <start> [ ROW | ROWS ] ]
    [FETCH { FIRST | NEXT } [ <count> ] { ROW | ROWS } ONLY ]
    [FOR {UPDATE | SHARE} [OF <table_name> [, ...]] [NOWAIT] [...]]
```

## 描述 {#description}

`SELECT INTO` 创建新表，并用查询计算的数据填充它。数据不会像普通 `SELECT` 那样返回给客户端。新表的列具有与 `SELECT` 输出列对应的名称和数据类型。

## 参数 {#parameters}

**`TEMPORARY`**<br />
**`TEMP`**

如果指定，将表创建为临时表。详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`UNLOGGED`**

如果指定，将表创建为不记录 WAL 的表。详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`new_table`**

要创建的表名称（可带模式限定）。

`SELECT INTO` 的所有其他参数都在 [SELECT](/cloudberry/reference/sql-stmts/select/) 参考页中详细说明。

## 注意事项 {#notes}

[CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/) 在功能上类似于 `SELECT INTO`。推荐使用 `CREATE TABLE AS` 语法，因为 ECPG 或 PL/pgSQL 不支持这种形式的 `SELECT INTO`：它们对 `INTO` 子句的解释不同。另外，`CREATE TABLE AS` 的功能涵盖并超出了 `SELECT INTO`。

与 `CREATE TABLE AS` 不同，`SELECT INTO` 不允许使用 `USING <method>` 指定表访问方法，也不允许使用 `TABLESPACE <tablespace_name>` 指定表空间等属性。必要时请使用 [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/)。因此，新表会采用默认表访问方法。

## 示例 {#examples}

创建新表 `films_recent`，仅包含表 `films` 中的近期记录：

```sql
SELECT * INTO films_recent FROM films WHERE date_prod >= '2016-01-01';
```

## 兼容性 {#compatibility}

SQL 标准使用 `SELECT INTO` 表示将值查询到宿主程序的标量变量中，而不是创建新表。Apache Cloudberry 使用 `SELECT INTO` 创建表是历史遗留用法。新应用程序最好使用 [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/) 完成此操作。

## 另见 {#see-also}

[SELECT](/cloudberry/reference/sql-stmts/select/), [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/)
