---
title: "CREATE USER MAPPING"
description: "定义用户到外部服务器的新映射。"
weight: 920
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-user-mapping.md"
---

## 概要 {#synopsis}

```sql
CREATE USER MAPPING [ IF NOT EXISTS ] FOR { <user_name> | USER | CURRENT_USER | PUBLIC }
    SERVER <server_name>
    [ OPTIONS ( <option> '<value>' [, ... ] ) ]
```

## 描述 {#description}

`CREATE USER MAPPING` 定义用户到外部服务器的映射。用户映射通常封装连接信息，外部数据包装器将这些信息与外部服务器封装的信息结合使用，以访问外部数据资源。

外部服务器所有者可以为该服务器上的任意用户创建用户映射。此外，如果用户已被授予服务器上的 `USAGE` 权限，也可以为自身用户名创建用户映射。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果给定用户到给定外部服务器的映射已经存在，不报错；Apache Cloudberry 会发出一条提示。注意，无法保证现有用户映射与原本要创建的映射有任何相似之处。

**`user_name`**

要映射到外部服务器的现有用户名。`CURRENT_USER` 和 `USER` 匹配当前用户名。指定 `PUBLIC` 时，Apache Cloudberry 创建所谓的公共映射，在没有适用的用户特定映射时使用。

**`server_name`**

要为其创建用户映射的现有服务器名称。

**`OPTIONS ( option 'value' [, ... ] )`**

新用户映射的选项。这些选项通常定义映射的实际用户名和密码。选项名称必须唯一。选项名称和值取决于服务器的外部数据包装器。

## 示例 {#examples}

为服务器 `foo` 上的用户 `bob` 创建用户映射：

```sql
CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

## 兼容性 {#compatibility}

`CREATE USER MAPPING` 符合 ISO/IEC 9075-9（SQL/MED）。

## 另见 {#see-also}

[ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/), [DROP USER MAPPING](/cloudberry/reference/sql-stmts/drop-user-mapping/), [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)
