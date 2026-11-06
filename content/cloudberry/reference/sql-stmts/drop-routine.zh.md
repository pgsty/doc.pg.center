---
title: "DROP ROUTINE"
description: "删除例程。"
weight: 1260
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-routine.md"
---

## 概要 {#synopsis}

```sql
DROP ROUTINE [IF EXISTS] name ( [ [argmode] [argname] argtype [, ...] ] )
    [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP ROUTINE` 删除现有例程的定义，例程可以是聚合函数、普通函数或过程。参数说明、更多示例和详细信息见 [DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/)、[DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/) 和 [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/)。

## 示例 {#examples}

删除用于 `integer` 类型的例程 `foo`：

```sql
DROP ROUTINE foo(integer);
```

无论 `foo` 是聚合函数、函数还是过程，此命令都有效。

## 兼容性 {#compatibility}

此命令符合 SQL 标准，但包含以下 Apache Cloudberry 扩展：

- 标准只允许每条命令删除一个例程。

- `IF EXISTS` 选项。

- 可以指定参数模式和名称。

- 聚合函数属于扩展。

## 另见 {#see-also}

[DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/), [DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/), [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/), [ALTER ROUTINE](/cloudberry/reference/sql-stmts/alter-routine/)
