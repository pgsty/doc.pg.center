---
title: "DROP SEQUENCE"
description: "删除序列。"
weight: 1290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-sequence.md"
---

## 概要 {#synopsis}

```sql
DROP SEQUENCE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP SEQUENCE` 删除序列号生成器。必须拥有该序列（或是超级用户）才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果序列不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的序列名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此序列的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此序列，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除序列 `myserial`：

```sql
DROP SEQUENCE myserial;
```

## 兼容性 {#compatibility}

`DROP SEQUENCE` 符合 SQL 标准，但标准只允许每条命令删除一个序列。另外，`IF EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/), [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/)
