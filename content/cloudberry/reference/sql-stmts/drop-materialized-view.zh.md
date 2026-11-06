---
title: "DROP MATERIALIZED VIEW"
description: "删除物化视图。"
weight: 1150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-materialized-view.md"
---

## 概要 {#synopsis}

```sql
DROP MATERIALIZED VIEW [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP MATERIALIZED VIEW` 删除现有物化视图。必须是物化视图的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果物化视图不存在，不报错，而是发出一条提示。

**`name`**

要删除的物化视图名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此物化视图的对象（例如其他物化视图或普通视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此物化视图，则拒绝删除。这是默认行为。

## 示例 {#examples}

此命令删除名为 `order_summary` 的物化视图。

```sql
DROP MATERIALIZED VIEW order_summary;
```

## 兼容性 {#compatibility}

`DROP MATERIALIZED VIEW` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[`ALTER MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/alter-materialized-view/), [`CREATE MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/create-materialized-view/), [`REFRESH MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/refresh-materialized-view/)
