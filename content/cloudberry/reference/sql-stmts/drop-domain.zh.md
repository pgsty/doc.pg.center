---
title: "DROP DOMAIN"
description: "删除域。"
weight: 1060
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-domain.md"
---

## 概要 {#synopsis}

```sql
DROP DOMAIN [IF EXISTS] <name> [, ...]  [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP DOMAIN` 删除先前定义的域。只有域的所有者才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果域不存在，不报错，而是发出一条提示。

**`name`**

现有域的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此域的对象（例如表列），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此域，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除名为 `us_postal_code` 的域：

```sql
DROP DOMAIN us_postal_code;
```

## 兼容性 {#compatibility}

此命令符合 SQL 标准，但 `IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER DOMAIN](/cloudberry/reference/sql-stmts/alter-domain/), [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/)
