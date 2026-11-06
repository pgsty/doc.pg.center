---
title: "DROP SCHEMA"
description: "删除模式。"
weight: 1280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-schema.md"
---

## 概要 {#synopsis}

```sql
DROP SCHEMA [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP SCHEMA` 从数据库中删除模式。

只有模式所有者或超级用户才能删除模式。注意，即使模式所有者并不拥有模式中的某些对象，也可以删除模式（从而删除其中的全部对象）。

## 参数 {#parameters}

**`IF EXISTS`**

如果模式不存在，不报错，而是发出一条提示。

**`name`**

要删除的模式名称。

**`CASCADE`**

自动删除模式中包含的对象（表、函数等），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果模式包含任何对象，则拒绝删除。这是默认行为。

## 注意事项 {#notes}

使用 `CASCADE` 选项可能导致此命令删除指定模式以外的其他模式中的对象。

## 示例 {#examples}

从数据库中删除模式 `mystuff` 及其包含的全部内容：

```sql
DROP SCHEMA mystuff CASCADE;
```

## 兼容性 {#compatibility}

`DROP SCHEMA` 完全符合 SQL 标准，但标准只允许每条命令删除一个模式。另外，`IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE SCHEMA`](/cloudberry/reference/sql-stmts/create-schema/), [`ALTER SCHEMA`](/cloudberry/reference/sql-stmts/alter-schema/)
