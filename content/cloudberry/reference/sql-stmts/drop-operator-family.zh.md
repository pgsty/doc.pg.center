---
title: "DROP OPERATOR FAMILY"
description: "移除一个操作符族。"
weight: 1170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-operator-family.md"
---

## 概要 {#synopsis}

```sql
DROP OPERATOR FAMILY [IF EXISTS] <name> USING <index_method> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP OPERATOR FAMILY` 删除一个现有的操作符族。要运行此命令，你必须是该操作符族的所有者。

`DROP OPERATOR FAMILY` 会一并删除该族中包含的所有操作符类，但不会删除该族所引用的任何操作符或函数。如果有任何索引依赖于该族内的操作符类，你需要指定 `CASCADE` 才能完成删除。

## 参数 {#parameters}

**`IF EXISTS`**

如果该操作符族不存在，则不抛出错误。这种情况下会发出一个提示。

**`name`**

一个现有操作符族的名称（可以是模式限定的）。

**`index_method`**

该操作符族所对应的索引访问方法的名称。

**`CASCADE`**

自动删除依赖于该操作符族的对象，并进而删除依赖于这些对象的所有对象。

**`RESTRICT`**

如果有任何对象依赖于该操作符族，则拒绝删除它。这是默认值。

## 示例 {#examples}

移除 B-树操作符族 `float_ops`：

```sql
DROP OPERATOR FAMILY float_ops USING btree;
```

如果存在任何使用该操作符族的索引，此命令将不会成功。添加 `CASCADE` 可以在删除该操作符族的同时删除这些索引。

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP OPERATOR FAMILY` 语句。

## 另见 {#see-also}

[ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/)、[CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/)、[ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/)、[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)、[DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/)
