---
title: "DROP OPERATOR CLASS"
description: "移除一个操作符类。"
weight: 1160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-operator-class.md"
---

## 概要 {#synopsis}

```sql
DROP OPERATOR CLASS [IF EXISTS] <name> USING <index_method> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP OPERATOR` 删除一个现有的操作符类。要运行此命令，你必须是该操作符类的所有者。

`DROP OPERATOR CLASS` 不会删除该类所引用的任何操作符或函数。如果有任何索引依赖于该操作符类，你需要指定 `CASCADE` 才能完成删除。

## 参数 {#parameters}

**`IF EXISTS`**

如果该操作符类不存在，则不抛出错误。这种情况下会发出一个提示。

**`name`**

一个现有操作符类的名称（可以是模式限定的）。

**`index_method`**

该操作符类所对应的索引访问方法的名称。

**`CASCADE`**

自动删除依赖于该操作符类的对象（例如索引），并进而删除依赖于这些对象的所有对象。

**`RESTRICT`**

如果有任何对象依赖于该操作符类，则拒绝删除它。这是默认值。

## 注解 {#notes}

`DROP OPERATOR CLASS` 不会删除包含该类的操作符族，即使该族中已经没有任何其他成员（尤其是在该族由 `CREATE OPERATOR CLASS` 隐式创建的情况下）。空的操作符族并无害处，但为了整洁起见，你也许会希望用 `DROP OPERATOR FAMILY` 移除该族；或者更好的做法是，一开始就使用 `DROP OPERATOR FAMILY`。

## 示例 {#examples}

移除 B-树操作符类 `widget_ops`：

```sql
DROP OPERATOR CLASS widget_ops USING btree;
```

如果存在任何使用该操作符类的索引，此命令将不会成功。添加 `CASCADE` 可以在删除该操作符类的同时删除这些索引。

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP OPERATOR CLASS` 语句。

## 另见 {#see-also}

[ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/)、[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)、[DROP OPERATOR FAMILY](/cloudberry/reference/sql-stmts/drop-operator-family/)
