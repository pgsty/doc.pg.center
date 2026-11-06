---
title: "DROP AGGREGATE"
description: "删除聚合函数。"
weight: 1010
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-aggregate.md"
---

## 概要 {#synopsis}

```sql
DROP AGGREGATE [IF EXISTS] <name> ( <aggregate_signature> ) [, ...] [CASCADE | RESTRICT]

-- where <aggregate_signature> is:

* |
[ <argmode> ] [ <argname> ] <argtype> [ , ... ] |
[ [ <argmode> ] [ <argname> ] <argtype> [ , ... ] ] ORDER BY [ <argmode> ] [ <argname> ] <argtype> [ , ... ]
```

## 描述 {#description}

`DROP AGGREGATE` 删除现有聚合函数。当前用户必须是该聚合函数的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果聚合函数不存在，不报错，而是发出一条提示。

**`name`**

现有聚合函数的名称（可带模式限定）。

**`argmode`**

参数模式：`IN` 或 `VARIADIC`。省略时默认为 `IN`。

**`argname`**

参数名称。注意，`DROP AGGREGATE` 实际上不考虑参数名称，因为确定聚合函数的身份只需要参数的数据类型。

**`argtype`**

聚合函数所处理的输入数据类型。引用零参数聚合函数时，用 `*` 代替参数说明列表。引用有序集聚合函数时，在直接参数与聚合参数的说明之间写上 `ORDER BY`。

**`CASCADE`**

自动删除依赖此聚合函数的对象（例如使用它的视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此聚合函数，则拒绝删除。这是默认行为。

## 注意事项 {#notes}

引用有序集聚合函数的其他语法见 [ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/)。

## 示例 {#examples}

删除用于 `integer` 类型的聚合函数 `myavg`：

```sql
DROP AGGREGATE myavg(integer);
```

删除假想集聚合函数 `myrank`，它接受任意排序列列表及与之对应的直接参数列表：

```sql
DROP AGGREGATE myrank(VARIADIC "any" ORDER BY VARIADIC "any");
```

在一条命令中删除多个聚合函数：

```sql
DROP AGGREGATE myavg(integer), myavg(bigint);
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP AGGREGATE` 语句。

## 另见 {#see-also}

[ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/), [CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/)
