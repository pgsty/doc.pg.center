---
title: "ALTER STATISTICS"
description: "修改扩展统计信息对象的定义。"
weight: 310
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-statistics.md"
---

## 概要 {#synopsis}

```sql
ALTER STATISTICS <name> RENAME TO <new_name>

ALTER STATISTICS <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER STATISTICS <name> SET SCHEMA <new_schema>
```

## 说明 {#description}

`ALTER STATISTICS` 用于修改现有扩展统计信息对象的参数。`ALTER STATISTICS` 命令中未明确设置的任何参数都保持其先前的设置。

你必须是统计信息对象的所有者才能使用 `ALTER STATISTICS`。要修改统计信息对象的模式，你还必须拥有新模式上的 `CREATE` 权限。要修改所有者，你还必须是新所属角色的直接或间接成员，并且该角色必须拥有统计信息对象所在模式上的 `CREATE` 权限。（这些限制确保修改所有者不会做出你通过删除并重新创建统计信息对象所做不到的事情。不过，超级用户无论如何都可以修改任何统计信息对象的所有权。）

## 参数 {#parameters}

**`name`**

要修改的统计信息对象的名称（可以带模式限定）。

**`new_owner`**

统计信息对象新所有者的用户名。

**`new_name`**

统计信息对象的新名称。

**`new_schema`**

统计信息对象的新模式。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER STATISTICS` 语句。

## 另请参阅 {#see-also}

[CREATE STATISTICS](/cloudberry/reference/sql-stmts/create-statistics/)、[DROP STATISTICS](/cloudberry/reference/sql-stmts/drop-statistics/)
