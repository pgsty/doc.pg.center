---
title: "ALTER USER MAPPING"
description: "更改外部服务器的用户映射的定义。"
weight: 400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-user-mapping.md"
---

## 概要 {#synopsis}

```sql
ALTER USER MAPPING FOR { <user_name> | USER | CURRENT_USER | SESSION_USER | PUBLIC }
    SERVER <server_name>
    OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ] )
```

## 描述 {#description}

`ALTER USER MAPPING` 用于更改外部服务器的用户映射的定义。

外部服务器的所有者可以为任意用户更改该服务器的用户映射。此外，被授予该服务器 `USAGE` 权限的用户可以更改与其自身用户名对应的用户映射。

## 参数 {#parameters}

**`user_name`**

映射的用户名。`CURRENT_USER` 和 `USER` 匹配当前用户的名称。`PUBLIC` 用于匹配系统中所有现有和将来的用户名。

**`server_name`**

用户映射的服务器名称。

**`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`**

更改用户映射的选项。新选项会覆盖先前指定的任何选项。`ADD`、`SET` 和 `DROP` 指定要执行的操作。如果没有显式指定操作，则默认操作为 `ADD`。选项名称必须唯一。Apache Cloudberry 使用服务器的外部数据包装器来验证名称和值。

## 示例 {#examples}

更改服务器 `foo` 上用户映射 `bob` 的密码：

```sql
ALTER USER MAPPING FOR bob SERVER foo OPTIONS (SET password 'public');
```

## 兼容性 {#compatibility}

`ALTER USER MAPPING` 符合 ISO/IEC 9075-9（SQL/MED）。这里存在一个细微的语法问题：标准省略了 `FOR` 关键字。由于 `CREATE USER MAPPING` 和 `DROP USER MAPPING` 在类似位置都使用 `FOR`，为了保持一致性和互操作性，Apache Cloudberry 在此处与标准有所不同。

## 另请参阅 {#see-also}

[CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/)、[DROP USER MAPPING](/cloudberry/reference/sql-stmts/drop-user-mapping/)
