---
title: "CALL"
description: "调用一个过程。"
weight: 450
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/call.md"
---

## 概要 {#synopsis}

```sql
CALL <name> ( [ <argument> ] [, ...] )
```

## 描述 {#description}

`CALL` 执行一个过程。

如果该过程有任何输出参数，则会返回一个结果行，其中包含这些参数的值。

## 参数 {#parameters}

**`name`**

过程的名称（可以带模式限定）。

**`argument`**

过程调用的输入参数。

## 注解 {#notes}

用户必须对该过程具有 `EXECUTE` 权限，才能调用它。

要调用函数（而不是过程），请改用 [SELECT](/cloudberry/reference/sql-stmts/select/)。

如果在事务块中调用 `CALL`，则被调用的过程不能运行事务控制语句。只有在 `CALL` 在其自身的事务中被调用时，才允许使用事务控制语句。

PL/pgSQL 对 `CALL` 命令中输出参数的处理方式有所不同；更多信息请参见 PostgreSQL 文档中的[调用过程](https://www.postgresql.org/docs/12/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)。

## 示例 {#examples}

```sql
CALL do_db_maintenance();
```

## 兼容性 {#compatibility}

`CALL` 符合 SQL 标准。

## 另见 {#see-also}

[CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/)
