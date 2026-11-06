---
title: "ALTER SCHEMA"
description: "修改模式的定义。"
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-schema.md"
---

## 概要 {#synopsis}

```sql
ALTER SCHEMA <name> RENAME TO <new_name>

ALTER SCHEMA <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## 说明 {#description}

`ALTER SCHEMA` 用于修改模式的定义。

你必须是模式的所有者才能使用 `ALTER SCHEMA`。要重命名模式，你还必须拥有该数据库的 `CREATE` 权限。要修改所有者，你还必须是新所属角色的直接或间接成员，并且必须拥有该数据库的 `CREATE` 权限。请注意，超级用户自动拥有所有这些权限。

## 参数 {#parameters}

**`name`**

现有模式的名称。

**`new_name`**

模式的新名称。新名称不能以 `pg_` 开头，因为此类名称保留给系统模式。

**`new_owner`**

模式的新所有者。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER SCHEMA` 语句。

## 另请参阅 {#see-also}

[CREATE SCHEMA](/cloudberry/reference/sql-stmts/create-schema/)、[DROP SCHEMA](/cloudberry/reference/sql-stmts/drop-schema/)
