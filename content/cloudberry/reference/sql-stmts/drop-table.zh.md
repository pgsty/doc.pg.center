---
title: "DROP TABLE"
description: "删除表。"
weight: 1320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-table.md"
---

## 概要 {#synopsis}

```sql
DROP TABLE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP TABLE` 从数据库中删除表。只有表所有者、模式所有者和超级用户才能删除表。要清空表中的行而保留表定义，请使用 [`DELETE`](/cloudberry/reference/sql-stmts/delete/) 或 [`TRUNCATE`](/cloudberry/reference/sql-stmts/truncate/)。

`DROP TABLE` 总会删除目标表上的所有索引、规则、触发器和约束。不过，要删除被视图引用的表，必须指定 `CASCADE`。`CASCADE` 会完整删除依赖该表的视图。

## 参数 {#parameters}

**`IF EXISTS`**

如果表不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的表名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此表的对象（例如视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此表，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除表 `mytable`：

```sql
DROP TABLE mytable;
```

删除 `films` 和 `distributors` 两个表：

```sql
DROP TABLE films, distributors;
```

## 兼容性 {#compatibility}

`DROP TABLE` 符合 SQL 标准，但标准只允许每条命令删除一个表。另外，`IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`ALTER TABLE`](/cloudberry/reference/sql-stmts/alter-table/), [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)
