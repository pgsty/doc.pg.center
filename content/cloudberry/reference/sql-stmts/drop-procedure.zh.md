---
title: "DROP PROCEDURE"
description: "删除过程。"
weight: 1210
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-procedure.md"
---

## 概要 {#synopsis}

```sql
DROP PROCEDURE [IF EXISTS] name ( [ [argmode] [argname] argtype [, ...] ] )
    [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP PROCEDURE` 删除现有过程的定义。用户必须是该过程的所有者才能运行此命令。必须指定过程的参数类型，因为可能存在多个名称相同但参数列表不同的过程。

## 参数 {#parameters}

**`IF EXISTS`**

如果过程不存在，不报错，而是发出一条提示。

**`name`**

现有过程的名称（可带模式限定）。如果未指定参数列表，此名称在所属模式中必须唯一。

**`argmode`**

参数模式：`IN` 或 `VARIADIC`。省略时默认为 `IN`。

**`argname`**

参数名称。注意，`DROP PROCEDURE` 实际上不考虑参数名称，因为确定过程身份只需要参数的数据类型。

**`argtype`**

过程参数的数据类型（可带模式限定），如果有参数的话。

**`CASCADE`**

自动删除依赖此过程的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此过程，则拒绝删除。这是默认行为。

## 示例 {#examples}

此命令删除名为 `do_db_maintenance` 的过程：

```sql
DROP PROCEDURE do_db_maintenance();
```

## 兼容性 {#compatibility}

此命令符合 SQL 标准，但包含以下 Apache Cloudberry 扩展：

- 标准只允许每条命令删除一个过程。

- `IF EXISTS` 选项。

- 可以指定参数模式和名称。

## 另见 {#see-also}

[CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/), [ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/)
