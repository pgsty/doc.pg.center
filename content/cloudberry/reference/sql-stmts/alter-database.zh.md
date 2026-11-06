---
title: "ALTER DATABASE"
description: "更改一个数据库的属性。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-database.md"
---

## 概要 {#synopsis}

```sql
ALTER DATABASE <name> [ [WITH] <option> [ ... ]  ]

-- where <option> can be:

    ALLOW_CONNECTIONS <allowconn>
    CONNECTION LIMIT <connlimit>
    IS_TEMPLATE <istemplate>

ALTER DATABASE <name> RENAME TO <new_name>

ALTER DATABASE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER DATABASE <name> SET TABLESPACE <new_tablespace>

ALTER DATABASE <name> SET <configuration_parameter> { TO | = } { <value> | DEFAULT }
ALTER DATABASE <name> SET <configuration_parameter> FROM CURRENT
ALTER DATABASE <name> RESET <configuration_parameter>
ALTER DATABASE <name> RESET ALL
```

## 描述 {#description}

`ALTER DATABASE` 更改一个数据库的属性。

第一种形式更改数据库级别的设置。（详见下文。）只有数据库所有者或超级用户才能更改这些设置。

第二种形式更改数据库的名称。只有数据库所有者或超级用户才能重命名数据库；非超级用户的所有者还必须具有 `CREATEDB` 权限。你不能重命名当前数据库，请先连接到另一个数据库。

第三种形式更改数据库的所有者。要更改所有者，你必须拥有该数据库，同时还必须是新所有者角色的直接或间接成员，并且必须具有 `CREATEDB` 权限。（请注意，超级用户自动拥有所有这些权限。）

第四种形式更改数据库的默认表空间。只有数据库所有者或超级用户才能执行此操作；你还必须对新表空间具有创建权限。此命令会把该数据库旧默认表空间中的所有表和索引物理移动到新表空间。新的默认表空间对该数据库而言必须为空，并且任何人都不能连接到该数据库。请注意，位于非默认表空间中的表和索引不受影响。

其余各种形式更改 Apache Cloudberry 中某个配置参数的会话默认值。此后每当在该数据库中启动新会话时，所指定的值就成为会话默认值。数据库级别的默认值会覆盖服务器配置文件（`postgresql.conf`）中的任何设置。只有数据库所有者或超级用户才能更改数据库的会话默认值。某些参数不能以这种方式设置，或者只能由超级用户设置。

## 参数 {#parameters}

**`name`**

要更改其属性的数据库名称。

**`allowconn`**

如果为 `false`，则任何人都不能连接到该数据库。

**`connlimit`**

在 Coordinator 上允许连接到该数据库的最大并发连接数。默认值为 `-1`，表示没有限制。Apache Cloudberry 超级用户不受此限制约束。

**`istemplate`**

如果为 `true`，则任何具有 `CREATEDB` 权限的用户都可以克隆该数据库；如果为 `false`，则只有超级用户或该数据库的所有者才能克隆它。请注意，模板数据库不能被删除。

**`new_name`**

数据库的新名称。

**`new_owner`**

数据库的新所有者。

**`new_tablespace`**

数据库的新默认表空间。

此形式的命令不能在事务块内执行。

**`configuration_parameter` value**

将该数据库中指定配置参数的会话默认值设置为给定值。如果 value 为 `DEFAULT`，或者等价地使用了 `RESET`，则会移除数据库级别的设置，因此新会话将继承系统范围的默认设置。使用 `RESET ALL` 可清除所有数据库级别的设置。`SET FROM CURRENT` 会把会话中该参数的当前值保存为数据库级别的值。

有关允许的参数名称和取值的更多信息，请参见 [`SET`](/cloudberry/reference/sql-stmts/set/) 和服务器配置参数。

## 注解 {#notes}

也可以把会话默认值绑定到特定角色而不是数据库；参见 [`ALTER ROLE`](/cloudberry/reference/sql-stmts/alter-role/)。如果发生冲突，角色级别的设置会覆盖数据库级别的设置。

## 示例 {#examples}

在 `test` 数据库中默认禁用索引扫描：

```sql
ALTER DATABASE test SET enable_indexscan TO off;
```

为 `mydatabase` 数据库设置默认的模式搜索路径：

```sql
ALTER DATABASE mydatabase SET search_path TO myschema, public, pg_catalog;
```

## 兼容性 {#compatibility}

`ALTER DATABASE` 语句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/)、[`DROP DATABASE`](/cloudberry/reference/sql-stmts/drop-database/)、[SET](/cloudberry/reference/sql-stmts/set/)、[`CREATE TABLESPACE`](/cloudberry/reference/sql-stmts/create-tablespace/)
