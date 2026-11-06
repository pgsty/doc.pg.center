---
title: "DROP TRIGGER"
description: "删除触发器。"
weight: 1390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-trigger.md"
---

## 概要 {#synopsis}

```sql
DROP TRIGGER [IF EXISTS] <name> ON <table> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP TRIGGER` 删除现有触发器定义。当前用户必须是定义该触发器的表的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果触发器不存在，不报错，而是发出一条提示。

**`name`**

要删除的触发器名称。

**`table`**

定义该触发器的表名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此触发器的对象。

**`RESTRICT`**

如果有对象依赖此触发器，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除表 `expenses` 上的触发器 `sendmail`：

```sql
DROP TRIGGER sendmail ON expenses;
```

## 兼容性 {#compatibility}

Apache Cloudberry 的 `DROP TRIGGER` 语句与 SQL 标准不兼容。在 SQL 标准中，触发器名称并非表的局部名称，因此命令只需写为 `DROP TRIGGER name`。

## 另见 {#see-also}

[ALTER TRIGGER](/cloudberry/reference/sql-stmts/alter-trigger/), [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/)
