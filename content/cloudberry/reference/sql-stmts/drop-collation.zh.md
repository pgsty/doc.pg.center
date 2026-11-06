---
title: "DROP COLLATION"
description: "删除先前定义的排序规则。"
weight: 1030
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-collation.md"
---

## 概要 {#synopsis}

```sql
DROP COLLATION [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP COLLATION` 删除先前定义的排序规则。必须拥有该排序规则才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果排序规则不存在，不报错，而是发出一条提示。

**`name`**

排序规则的名称，可以带模式限定。

**`CASCADE`**

自动删除依赖此排序规则的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此排序规则，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除名为 `german` 的排序规则：

```sql
DROP COLLATION german;
```

## 兼容性 {#compatibility}

`DROP COLLATION` 命令符合 SQL 标准，但 `IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/), [CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/)
