---
title: "dropuser"
description: "删除数据库角色。"
weight: 420
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/dropuser.md"
---

## 概要 {#synopsis}

```shell
dropuser [<connection-option> ...] [-e] [-i] <role_name>

dropuser -? | --help 

dropuser -V | --version
```

## 说明 {#description}

`dropuser` 从 Apache Cloudberry 中删除现有角色。只有超级用户和具有 `CREATEROLE` 权限的用户才能删除角色。要删除超级用户角色，执行者自身也必须是超级用户。

`dropuser` 是 SQL 命令 `DROP ROLE` 的封装。

## 选项 {#options}

**`role_name`**

要删除的角色名称。如果命令行中未指定名称，且使用了 `-i`/`--interactive` 选项，则会提示输入名称。

**`-e | --echo`**

回显 `dropuser` 生成并发送给服务器的命令。

**`-i | --interactive`**

实际删除角色前提示确认；如果命令行中未指定角色名，还会提示输入角色名。

**`--if-exists`**

用户不存在时不报错，而是发出一条通知。

**`-V | --version`**

打印 `dropuser` 版本并退出。

**`-? | --help`**

显示 `dropuser` 命令行参数的帮助并退出。

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

## 示例 {#examples}

使用默认连接选项删除角色 `joe`：

```shell
dropuser joe
DROP ROLE
```

使用连接选项删除角色 joe，提示确认，并查看底层命令：

```shell
dropuser -p 54321 -h coordinatorhost -i -e joe
Role "joe" will be permanently removed.
Are you sure? (y/n) y
DROP ROLE "joe"
DROP ROLE
```

## 另请参阅 {#see-also}

[createuser](/cloudberry/reference/sys-utilities/createuser/), [`DROP ROLE`](/cloudberry/reference/sql-stmts/drop-role/)
