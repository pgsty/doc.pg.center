---
title: "createdb"
description: "创建新数据库。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/createdb.md"
---

## 概要 {#synopsis}

```shell
createdb [<connection-option> ...] [<option> ...] [<dbname> ['<description>']]

createdb -? | --help

createdb -V | --version
```

## 说明 {#description}

`createdb` 在 Apache Cloudberry 系统中创建新数据库。

通常，运行此命令的数据库用户会成为新数据库的所有者。不过，只要执行用户具有适当权限，也可以通过 `-O` 选项指定其他所有者。

`createdb` 是 SQL 命令 [`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/) 的封装。

## 选项 {#options}

**`dbname`**

要创建的数据库名称。该名称必须与 Apache Cloudberry 系统中的所有其他数据库名称不同。如果未指定，依次读取环境变量 `PGDATABASE`、`PGUSER` 的值，否则默认为当前系统用户。

**`description`**

与新建数据库关联的注释。包含空白字符的描述必须用引号括起。

**`-D tablespace | --tablespace=TABLESPACE`**

指定数据库的默认表空间。（此名称按双引号标识符处理。）

**`-e | --echo`**

回显 `createdb` 生成并发送给服务器的命令。

**`-E encoding | --encoding=ENCODING`**

新数据库使用的字符集编码。可以指定字符串常量（如 `'UTF8'`）、整数编码编号，或指定 `DEFAULT` 以使用默认编码。

**`-l locale | --locale=LOCALE`**

指定此数据库使用的区域设置。这等同于同时指定 `--lc-collate` 和 `--lc-ctype`。

**`--lc-collate=LOCALE`**

指定此数据库使用的 `LC_COLLATE` 设置。

**`--lc-ctype=LOCALE`**

指定此数据库使用的 `LC_CTYPE` 设置。

**`-O owner | --owner=OWNER`**

将拥有新数据库的数据库用户名。默认为运行此命令的用户。（此名称按双引号标识符处理。）

**`-T template | --template=TEMPLATE`**

用于创建新数据库的模板名称。默认为 `template1`。（此名称按双引号标识符处理。）

**`-V | --version`**

打印 `createdb` 版本并退出。

**`-? | --help`**

显示 `createdb` 命令行参数的帮助并退出。

选项 `-D`、`-l`、`-E`、`-O` 和 `-T` 对应于底层 SQL 命令 `CREATE DATABASE` 的选项；详情请参阅 [`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/)。

### 连接选项 {#connection-options}

**`-h host | --host=HOSTNAME`**

运行 Apache Cloudberry Coordinator 服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p port | --port=PORT`**

Apache Cloudberry Coordinator 服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username | --username=USERNAME`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W | --password`**

强制提示输入密码。

**`--maintenance-db=DBNAME`**

指定创建新数据库时连接的数据库名称。如果未指定，将使用 `postgres` 数据库；如果该数据库不存在（或恰好是正在创建的新数据库的名称），则使用 `template1`。

## 示例 {#examples}

使用默认选项创建数据库 `test`：

```shell
createdb test
```

创建数据库 `demo`，使用主机 `gpcoord` 上端口为 `54321` 的 Apache Cloudberry Coordinator，并采用 `LATIN1` 编码：

```shell
createdb -p 54321 -h gpcoord -E LATIN1 demo
```

## 另请参阅 {#see-also}

[`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/), [dropdb](/cloudberry/reference/sys-utilities/dropdb/)
