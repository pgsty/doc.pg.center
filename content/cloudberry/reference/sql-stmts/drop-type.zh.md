---
title: "DROP TYPE"
description: "删除数据类型。"
weight: 1400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-type.md"
---

## 概要 {#synopsis}

```sql
DROP TYPE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP TYPE` 删除用户定义的数据类型。只有类型所有者才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果类型不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的数据类型名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此类型的对象（例如表列、函数和操作符），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此类型，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除数据类型 `box`：

```sql
DROP TYPE box;
```

## 兼容性 {#compatibility}

此命令类似于 SQL 标准中的对应命令，但 `IF EXISTS` 选项是 Apache Cloudberry 的扩展。不过，Apache Cloudberry 的 `CREATE TYPE` 命令和数据类型扩展机制有许多部分与 SQL 标准不同。

## 另见 {#see-also}

[`ALTER TYPE`](/cloudberry/reference/sql-stmts/alter-type/), [`CREATE TYPE`](/cloudberry/reference/sql-stmts/create-type/)
