---
title: "DROP FUNCTION"
description: "删除函数。"
weight: 1110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-function.md"
---

## 概要 {#synopsis}

```sql
DROP FUNCTION [IF EXISTS] name ( [ [argmode] [argname] argtype [, ...] ] )
    [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP FUNCTION` 删除现有函数的定义。用户必须是该函数的所有者才能运行此命令。必须指定函数的参数类型，因为可能存在多个名称相同但参数列表不同的函数。

## 参数 {#parameters}

**`IF EXISTS`**

如果函数不存在，不报错，而是发出一条提示。

**`name`**

现有函数的名称（可带模式限定）。

**`argmode`**

参数模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。省略时默认为 `IN`。注意，`DROP FUNCTION` 实际上不考虑 `OUT` 参数，因为确定函数身份只需要输入参数。因此，只需列出 `IN`、`INOUT` 和 `VARIADIC` 参数。

**`argname`**

参数名称。注意，`DROP FUNCTION` 实际上不考虑参数名称，因为确定函数身份只需要参数的数据类型。

**`argtype`**

函数参数的数据类型（可带模式限定），如果有参数的话。

**`CASCADE`**

自动删除依赖此函数的对象（例如操作符）。

**`RESTRICT`**

如果有对象依赖此函数，则拒绝删除。这是默认行为。

## 示例 {#examples}

此命令删除平方根函数：

```sql
DROP FUNCTION sqrt(integer);
```

## 兼容性 {#compatibility}

SQL 标准定义了 `DROP FUNCTION` 语句，但与此命令不兼容。

## 另见 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/)
