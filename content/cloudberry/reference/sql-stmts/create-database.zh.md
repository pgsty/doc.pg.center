---
title: "CREATE DATABASE"
description: "创建一个新数据库。"
weight: 570
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-database.md"
---

## 概要 {#synopsis}

```sql
CREATE DATABASE name
    [ [WITH] [OWNER [=] <user_name>]
          [TEMPLATE [=] <template>]
          [TABLESPACE [=] <tablespace_name>]
          [ALLOW_CONNECTIONS [=] <allowconn>]
          [CONNECTION LIMIT [=] <connlimit> ]
          [IS_TEMPLATE [=] <istemplate> ] ]
```

## 描述 {#description}

`CREATE DATABASE` 创建一个新数据库。

要创建数据库，你必须是超级用户，或者拥有特殊的 `CREATEDB` 权限。参见 [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/)。

默认情况下，创建者会成为新数据库的所有者。超级用户可以使用 `OWNER` 子句创建由其他用户拥有的数据库，甚至可以创建由不具备任何特殊权限的用户拥有的数据库。具有 `CREATEDB` 权限的非超级用户只能创建由自己拥有的数据库。

默认情况下，新数据库通过克隆标准系统数据库 `template1` 来创建。可以通过写成 `TEMPLATE name` 指定其他模板。特别是，写成 `TEMPLATE template0` 时，可以创建一个纯净的数据库，其中只包含 Apache Cloudberry 预定义的标准对象。如果你希望避免复制任何可能已添加到 `template1` 中、仅属于本安装的本地对象，这会很有用。

## 参数 {#parameters}

**`name`**

要创建的数据库的名称。

**`user_name`**

将拥有新数据库的数据库用户的名称，或者指定 `DEFAULT` 以使用默认所有者（即运行该命令的用户）。要创建由其他角色拥有的数据库，你必须是该角色的直接或间接成员，或者是超级用户。

**`template`**

用于创建新数据库的模板名称，或者指定 `DEFAULT` 以使用默认模板（template1）。

**`tablespace_name`**

将与新数据库关联的表空间名称，或者指定 `DEFAULT` 以使用模板数据库的表空间。该表空间将成为在此数据库中创建的对象所使用的默认表空间。更多信息参见 [`CREATE TABLESPACE`](/cloudberry/reference/sql-stmts/create-tablespace/)。

**`allowconn`**

如果为 `false`，则任何人都不能连接到该数据库。默认值为 `true`，即允许连接（但仍受其他机制限制，例如 `GRANT/REVOKE CONNECT`）。

**`connlimit`**

在 Coordinator 上该数据库允许的最大并发连接数。默认值为 `-1`，表示不受限制。Apache Cloudberry 超级用户不受此限制。

**`istemplate`**

如果为 `true`，则任何具有 `CREATEDB` 权限的用户都可以克隆该数据库；如果为 `false`（默认值），则只有超级用户或该数据库的所有者可以克隆它。注意，模板数据库不能被删除。

可选参数可以按任意顺序书写，不必按照上面所示的顺序。

## 注解 {#notes}

`CREATE DATABASE` 不能在事务块内运行。

形如“could not initialize database directory”的错误，很可能与数据目录权限不足、磁盘已满或其他文件系统问题有关。

使用 [`DROP DATABASE`](/cloudberry/reference/sql-stmts/drop-database/) 移除数据库。

程序 createdb 是此命令的包装程序，为方便使用而提供。

数据库级配置参数（通过 [`ALTER DATABASE`](/cloudberry/reference/sql-stmts/alter-database/) 设置）以及数据库级权限（通过 [GRANT](/cloudberry/reference/sql-stmts/grant/) 设置）都不会从模板数据库中复制。

尽管可以通过把 `template1` 以外的某个数据库的名称指定为模板来复制该数据库，但这（目前还）不打算作为一种通用的 `"COPY DATABASE"` 功能。主要限制是，在复制模板数据库期间，不能有任何其他会话连接到该数据库。如果 `CREATE DATABASE` 启动时存在任何其他连接，该命令就会失败；否则，在 `CREATE DATABASE` 完成之前，到模板数据库的新连接都会被阻止。

`CONNECTION LIMIT` 选项只是近似地强制执行；如果该数据库只剩下一个连接“槽”时，有两个新会话几乎同时启动，则两者都可能失败。此外，该限制不对超级用户或后台工作进程强制执行。

## 示例 {#examples}

要创建一个新数据库：

```sql
CREATE DATABASE mydatabase;
```

要创建一个由用户 `salesapp` 拥有、默认表空间为 `salesspace` 的数据库 `sales`：

```sql
CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE DATABASE` 语句。数据库相当于目录（catalog），而目录的创建方式由实现定义。

## 另见 {#see-also}

[`ALTER DATABASE`](/cloudberry/reference/sql-stmts/alter-database/)、[`DROP DATABASE`](/cloudberry/reference/sql-stmts/drop-database/)
