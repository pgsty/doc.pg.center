---
title: "DROP EXTERNAL TABLE"
description: "删除外部表定义。"
weight: 1080
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-external-table.md"
---

## 概要 {#synopsis}

```sql
DROP EXTERNAL [WEB] TABLE [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP EXTERNAL TABLE` 从数据库系统中删除现有外部表的定义，不删除外部数据源或文件。必须是外部表的所有者才能运行此命令。

## 参数 {#parameters}

**`WEB`**

删除外部 Web 表时使用的可选关键字。

**`IF EXISTS`**

如果外部表不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有外部表的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此外部表的对象（例如视图）。

**`RESTRICT`**

如果有对象依赖此外部表，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除名为 `staging` 的外部表（如果存在）：

```sql
DROP EXTERNAL TABLE IF EXISTS staging;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP EXTERNAL TABLE` 语句。

## 另见 {#see-also}

[`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/), [`ALTER EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/alter-external-table/)
