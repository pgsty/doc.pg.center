---
title: "dropdb"
description: "删除数据库。"
weight: 410
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/dropdb.md"
---

## 概要 {#synopsis}

```shell
dropdb [<connection-option> ...] [-e] [-i] <dbname>

dropdb -? | --help

dropdb -V | --version
```

## 说明 {#description}

`dropdb` 删除现有数据库。运行此命令的用户必须是超级用户，或是要删除的数据库的所有者。

`dropdb` 是 SQL 命令 `DROP DATABASE` 的封装。

## 选项 {#options}

**`dbname`**

要删除的数据库名称。

**`-e | --echo`**

回显 `dropdb` 生成并发送给服务器的命令。

**`-i | --interactive`**

执行任何破坏性操作前提示确认。

**`-V | --version`**

打印 `dropdb` 版本并退出。

**`--if-exists`**

数据库不存在时不报错，而是发出一条通知。

**`-? | --help`**

显示 `dropdb` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

**`-h host | --host=host`**

运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p port | --port=port`**

Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username | --username=username`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W | --password`**

强制提示输入密码。

**`--maintenance-db=dbname`**

指定为删除目标数据库而连接的数据库名称。如果未指定，将使用 `postgres` 数据库；如果该数据库不存在（或恰好是要删除的数据库），则使用 `template1`。

## 示例 {#examples}

使用默认连接参数删除名为 `demo` 的数据库：

```shell
dropdb demo
```

使用连接选项删除名为 `demo` 的数据库，提示确认，并查看底层命令：

```shell
dropdb -p 54321 -h coordinatorhost -i -e demo
Database "demo" will be permanently deleted.
Are you sure? (y/n) y
DROP DATABASE "demo"
DROP DATABASE
```

## 另请参阅 {#see-also}

[createdb](/cloudberry/reference/sys-utilities/createdb/), [`DROP DATABASE`](/cloudberry/reference/sql-stmts/drop-database/)
