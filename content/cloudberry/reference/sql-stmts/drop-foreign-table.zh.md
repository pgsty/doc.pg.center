---
title: "DROP FOREIGN TABLE"
description: "删除外表。"
weight: 1100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-foreign-table.md"
---

## 概要 {#synopsis}

```sql
DROP FOREIGN TABLE [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP FOREIGN TABLE` 删除现有外表。只有外表的所有者才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果外表不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的外表名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此外表的对象（例如视图），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此外表，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除 `films` 和 `distributors` 两个外表：

```sql
DROP FOREIGN TABLE films, distributors;
```

## 兼容性 {#compatibility}

`DROP FOREIGN TABLE` 符合 ISO/IEC 9075-9（SQL/MED），但标准只允许每条命令删除一个外表。`IF EXISTS` 子句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER FOREIGN TABLE](/cloudberry/reference/sql-stmts/alter-foreign-table/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/)
