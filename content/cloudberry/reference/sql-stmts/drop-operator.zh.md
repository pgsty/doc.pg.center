---
title: "DROP OPERATOR"
description: "删除操作符。"
weight: 1180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-operator.md"
---

## 概要 {#synopsis}

```sql
DROP OPERATOR [IF EXISTS] <name> ( {<left_type> | NONE} , 
    {<right_type> | NONE} ) [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP OPERATOR` 从数据库系统中删除现有操作符。必须是操作符的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果操作符不存在，不报错，而是发出一条提示。

**`name`**

现有操作符的名称（可带模式限定）。

**`left_type`**

操作符左操作数的数据类型；如果没有左操作数，写为 `NONE`。

**`right_type`**

操作符右操作数的数据类型；如果没有右操作数，写为 `NONE`。

**`CASCADE`**

自动删除依赖此操作符的对象（例如使用它的视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此操作符，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除用于 `integer` 类型的幂操作符 `a^b`：

```sql
DROP OPERATOR ^ (integer, integer);
```

删除用于 `bit` 类型的左一元按位取反操作符 `~b`：

```sql
DROP OPERATOR ~ (none, bit);
```

删除用于 `bigint` 类型的右一元阶乘操作符 `x!`：

```sql
DROP OPERATOR ! (bigint, none);
```

在一条命令中删除多个操作符：

```sql
DROP OPERATOR ~ (none, bit), ! (bigint, none);
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP OPERATOR` 语句。

## 另见 {#see-also}

[ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/), [CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/)
