---
title: "SHOW"
description: "显示运行时系统配置参数的值。"
weight: 1740
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/show.md"
---

## 概要 {#synopsis}

```sql
SHOW <name>

SHOW ALL
```

## 描述 {#description}

`SHOW` 显示 Apache Cloudberry 运行时系统配置参数的当前设置。可以通过 `SET` 语句、编辑 Apache Cloudberry Coordinator 的 `postgresql.conf` 配置文件、设置 `PGOPTIONS` 环境变量（使用 libpq 或基于 libpq 的应用程序时），或在启动 Apache Cloudberry 服务器时提供命令行标志来设置这些参数。

## 参数 {#parameters}

**`name`**

运行时系统配置参数的名称。

某些可通过 `SHOW` 查看参数是只读的：可以查看其值，但不能设置：

**`SERVER_VERSION`**

显示 Apache Cloudberry 服务器的版本号。

**`SERVER_ENCODING`**

显示服务器端的字符集编码。此参数可以查看但不能设置，因为编码是在创建数据库时确定的。

**`LC_COLLATE`**

显示数据库用于排序规则（文本排序）的区域设置。此参数可以查看但不能设置，因为该设置是在创建数据库时确定的。

**`LC_CTYPE`**

显示数据库用于字符分类的区域设置。此参数可以查看但不能设置，因为该设置是在创建数据库时确定的。

**`IS_SUPERUSER`**

如果当前角色拥有超级用户权限，则为真。

**`ALL`**

显示所有配置参数的当前值及其描述。

## 注意事项 {#notes}

`current_setting()` 函数产生等效输出；见 PostgreSQL 文档中的[系统管理函数](https://www.postgresql.org/docs/12/functions-admin.html)。另外，[pg_settings](https://www.postgresql.org/docs/12/view-pg-settings.html) 系统视图也提供相同信息。

## 示例 {#examples}

显示参数 `DateStyle` 的当前设置：

```sql
SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

显示参数 `row_security` 的当前设置：

```sql
SHOW row_security;
 row_security
--------------
 on
(1 row)
```

显示所有参数的当前设置：

```sql
SHOW ALL;
       name       | setting |                  description
-----------------+---------+----------------------------------------------------
 application_name | psql    | Sets the application name to be reported in sta...

 ...

 xmlbinary        | base64  | Sets how binary values are to be encoded in XML.
 xmloption        | content | Sets whether XML data in implicit parsing and s...
(473 rows)
```

## 兼容性 {#compatibility}

`SHOW` 命令是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[SET](/cloudberry/reference/sql-stmts/set/), [RESET](/cloudberry/reference/sql-stmts/reset/)
