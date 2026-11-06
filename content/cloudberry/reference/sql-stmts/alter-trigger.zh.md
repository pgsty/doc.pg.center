---
title: "ALTER TRIGGER"
description: "更改触发器的定义。"
weight: 380
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-trigger.md"
---

## 概要 {#synopsis}

```sql
ALTER TRIGGER <name> ON <table> RENAME TO <newname>
```

## 描述 {#description}

`ALTER TRIGGER` 用于更改现有触发器的属性。`RENAME` 子句更改给定触发器的名称，而不改变触发器定义的其他部分。必须拥有触发器所作用的表，才能更改其属性。

## 参数 {#parameters}

**`name`**

要更改的现有触发器的名称。

**`table`**

该触发器所作用的表的名称。

**`newname`**

触发器的新名称。

## 注意事项 {#notes}

临时启用或停用触发器的功能由 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 提供，而不是由 `ALTER TRIGGER` 提供，因为 `ALTER TRIGGER` 没有便捷的方式来表达一次性启用或停用某个表的所有触发器这一选项。

请注意，在此版本中，Apache Cloudberry 对触发器的支持有限。更多信息请参见 [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/)。

## 示例 {#examples}

重命名现有触发器：

```sql
ALTER TRIGGER emp_stamp ON emp RENAME TO emp_track_chgs;
```

## 兼容性 {#compatibility}

`ALTER TRIGGER` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另请参阅 {#see-also}

[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)、[CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/)、[DROP TRIGGER](/cloudberry/reference/sql-stmts/drop-trigger/)
