---
title: "DROP FOREIGN DATA WRAPPER"
description: "删除外部数据包装器。"
weight: 1090
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-foreign-data-wrapper.md"
---

## 概要 {#synopsis}

```sql
DROP FOREIGN DATA WRAPPER [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP FOREIGN DATA WRAPPER` 从当前数据库中删除现有的外部数据包装器。只有外部数据包装器的所有者才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果外部数据包装器不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有外部数据包装器的名称。

**`CASCADE`**

自动删除依赖此外部数据包装器的对象（例如外表和服务器），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此外部数据包装器，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除名为 `dbi` 的外部数据包装器：

```sql
DROP FOREIGN DATA WRAPPER dbi;
```

## 兼容性 {#compatibility}

`DROP FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED）。`IF EXISTS` 子句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/)
