---
title: "DROP USER MAPPING"
description: "删除外部服务器的用户映射。"
weight: 1410
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-user-mapping.md"
---

## 概要 {#synopsis}

```sql
DROP USER MAPPING [ IF EXISTS ] { <user_name> | USER | CURRENT_USER | PUBLIC } 
    SERVER <server_name>
```

## 描述 {#description}

`DROP USER MAPPING` 从外部服务器中删除现有用户映射。

外部服务器所有者可以删除该服务器上任意用户的用户映射。此外，如果用户已被授予服务器上的 `USAGE` 权限，也可以删除其自身用户名对应的用户映射。

## 参数 {#parameters}

**`IF EXISTS`**

如果用户映射不存在，不报错；Apache Cloudberry 会发出一条提示。

**`user_name`**

映射的用户名。`CURRENT_USER` 和 `USER` 匹配当前用户名。`PUBLIC` 用于匹配系统中所有现有和未来的用户名。

**`server_name`**

用户映射的服务器名称。

## 示例 {#examples}

删除服务器 `foo` 上名为 `bob` 的用户映射（如果存在）：

```sql
DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

## 兼容性 {#compatibility}

`DROP SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。`IF EXISTS` 子句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/), [ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/)
