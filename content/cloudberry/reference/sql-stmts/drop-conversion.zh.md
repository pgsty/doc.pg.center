---
title: "DROP CONVERSION"
description: "删除编码转换。"
weight: 1040
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-conversion.md"
---

## 概要 {#synopsis}

```sql
DROP CONVERSION [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP CONVERSION` 删除先前定义的编码转换。必须拥有该编码转换才能删除它。

## 参数 {#parameters}

**`IF EXISTS`**

如果编码转换不存在，不报错，而是发出一条提示。

**`name`**

编码转换的名称，可以带模式限定。

CASCADE
**`RESTRICT`**

这些关键字没有效果，因为不存在对编码转换的依赖。

## 示例 {#examples}

删除名为 `myname` 的编码转换：

```sql
DROP CONVERSION myname;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP CONVERSION` 语句。标准中的 `CREATE TRANSLATION` 和 `DROP TRANSLATION` 语句类似于 Apache Cloudberry 的 `CREATE CONVERSION` 和 `DROP CONVERSION` 语句。

## 另见 {#see-also}

[ALTER CONVERSION](/cloudberry/reference/sql-stmts/alter-conversion/), [CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/)
