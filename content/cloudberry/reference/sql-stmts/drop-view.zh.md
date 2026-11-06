---
title: "DROP VIEW"
description: "删除视图。"
weight: 1430
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-view.md"
---

## 概要 {#synopsis}

```sql
DROP VIEW [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP VIEW` 删除现有视图。只有视图所有者才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果视图不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的视图名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此视图的对象（例如其他视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此视图，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除视图 `topten`：

```sql
DROP VIEW topten;
```

## 兼容性 {#compatibility}

`DROP VIEW` 完全符合 SQL 标准，但标准只允许每条命令删除一个视图。另外，`IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE VIEW`](/cloudberry/reference/sql-stmts/create-view/), [`ALTER VIEW`](/cloudberry/reference/sql-stmts/alter-view/)
