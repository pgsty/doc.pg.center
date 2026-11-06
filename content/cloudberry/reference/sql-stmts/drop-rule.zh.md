---
title: "DROP RULE"
description: "删除重写规则。"
weight: 1270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-rule.md"
---

## 概要 {#synopsis}

```sql
DROP RULE [IF EXISTS] <name> ON <table_name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP RULE` 从表或视图中删除重写规则。

## 参数 {#parameters}

**`IF EXISTS`**

如果规则不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的规则名称。

**`table_name`**

规则应用于的表或视图名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此规则的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此规则，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除表 `sales` 上的重写规则 `sales_2006`：

```sql
DROP RULE sales_2006 ON sales;
```

## 兼容性 {#compatibility}

`DROP RULE` 和整个查询重写系统一样，都是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`ALTER RULE`](/cloudberry/reference/sql-stmts/alter-rule/), [`CREATE RULE`](/cloudberry/reference/sql-stmts/create-rule/)
