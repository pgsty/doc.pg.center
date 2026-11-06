---
title: "CREATE USER"
description: "定义新的数据库角色。"
weight: 930
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-user.md"
---

## 概要 {#synopsis}

```sql
CREATE USER <name> [[WITH] <option> [ ... ]]

where option can be:
      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | CREATEEXTTABLE | NOCREATEEXTTABLE 
      [ ( <attribute>='<value>'[, ...] ) ]
           where <attributes> and <value> are:
           type='readable'|'writable'
           protocol='gpfdist'|'http'
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT <connlimit>
    | [ ENCRYPTED ] PASSWORD '<password>' | PASSWORD NULL
    | VALID UNTIL '<timestamp>'
    | IN ROLE <role_name> [, ...]
    | IN GROUP <role_name>
    | ROLE <role_name> [, ...]
    | ADMIN <role_name> [, ...]
    | USER <role_name> [, ...]
    | SYSID <uid>
    | RESOURCE QUEUE <queue_name>
    | RESOURCE GROUP <group_name>
    | [ DENY <deny_point> ]
    | [ DENY BETWEEN <deny_point> AND <deny_point>]
```

## 描述 {#description}

`CREATE USER` 是 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 的别名。唯一区别在于：调用 `CREATE USER` 命令时默认采用 `LOGIN`，而调用 `CREATE ROLE` 时默认采用 `NOLOGIN`。

## 兼容性 {#compatibility}

`CREATE USER` 语句是 Apache Cloudberry 的扩展。SQL 标准将用户定义留给实现自行规定。

## 另见 {#see-also}

[CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/)
