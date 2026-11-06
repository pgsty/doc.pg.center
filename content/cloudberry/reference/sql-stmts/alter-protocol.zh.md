---
title: "ALTER PROTOCOL"
description: "更改协议的定义。"
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-protocol.md"
---

## 概要 {#synopsis}

```sql
ALTER PROTOCOL <name> RENAME TO <newname>

ALTER PROTOCOL <name> OWNER TO <newowner>
```

## 描述 {#description}

`ALTER PROTOCOL` 更改协议的定义。只能更改协议的名称或所有者。

要使用 `ALTER PROTOCOL`，你必须拥有该协议。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该协议所在的模式上具有 `CREATE` 权限。

设置这些限制是为了确保更改所有者只做出那些通过删除并重新创建该协议也能做到的更改。请注意，超级用户可以更改任何协议的所有权。

## 参数 {#parameters}

**`name`**

一个现有协议的名称（可以是模式限定的）。

**`newname`**

协议的新名称。

**`newowner`**

协议的新所有者。

## 示例 {#examples}

将协议 `GPDBauth` 重命名为 `GPDB_authentication`：

```sql
ALTER PROTOCOL GPDBauth RENAME TO GPDB_authentication;
```

将协议 `GPDB_authentication` 的所有者更改为 `joe`：

```sql
ALTER PROTOCOL GPDB_authentication OWNER TO joe;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER PROTOCOL` 语句。

## 另见 {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/)、[CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/)、[DROP PROTOCOL](/cloudberry/reference/sql-stmts/drop-protocol/)
