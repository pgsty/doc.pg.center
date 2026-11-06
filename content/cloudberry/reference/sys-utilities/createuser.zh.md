---
title: "createuser"
description: "创建新数据库角色。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/createuser.md"
---

## 概要 {#synopsis}

```shell
createuser [<connection-option> ...] [<role_attribute> ...] [-e] <role_name>

createuser -? | --help 

createuser -V | --version
```

## 说明 {#description}

`createuser` 创建新的 Apache Cloudberry 角色。创建新角色必须是超级用户或具有 `CREATEROLE` 权限。创建新的超级用户时，必须以超级用户身份连接数据库。

超级用户可以绕过数据库内的所有访问权限检查，因此不应轻易授予超级用户权限。

`createuser` 是 SQL 命令 `CREATE ROLE` 的封装。

## 选项 {#options}

**`role_name`**

要创建的角色名称。此名称必须与当前 Apache Cloudberry 安装中的所有现有角色不同。

**`-c number | --connection-limit=number`**

设置新角色的最大连接数。默认不限制。

**`-d | --createdb`**

允许新角色创建数据库。

**`-D | --no-createdb`**

不允许新角色创建数据库。这是默认行为。

**`-e | --echo`**

回显 `createuser` 生成并发送给服务器的命令。

**`-E | --encrypted`**

加密存储在数据库中的角色密码。如果未指定，将使用默认的密码处理方式。

**`-i | --inherit`**

新角色会自动继承其所属角色的权限。这是默认行为。

**`-I | --no-inherit`**

新角色不会自动继承其所属角色的权限。

**`--interactive`**

如果命令行中未指定用户名，则提示输入用户名；对于 `-d`/`-D`、`-r`/`-R`、`-s`/`-S` 这几组选项中未在命令行指定的选项，也会进行提示。

**`-l | --login`**

允许新角色登录 Apache Cloudberry。这是默认行为。

**`-L | --no-login`**

不允许新角色登录（组级角色）。

**`-N | --unencrypted`**

不加密存储在数据库中的角色密码。如果未指定，将使用默认的密码处理方式。

**`-P | --pwprompt`**

如果指定此选项，`createuser` 将提示输入新角色的密码。如果不打算使用密码认证，则无需指定此选项。

**`-r | --createrole`**

允许新角色创建其他角色（`CREATEROLE` 权限）。

**`-R | --no-createrole`**

不允许新角色创建其他角色。这是默认行为。

**`-s | --superuser`**

新角色将是超级用户。

**`-S | --no-superuser`**

新角色不是超级用户。这是默认行为。

**`-V | --version`**

打印 `createuser` 版本并退出。

**`--replication`**

新用户将具有 `REPLICATION` 权限。该权限的详细说明请参阅 [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/) 文档。

**`--no-replication`**

新用户不具有 `REPLICATION` 权限。该权限的详细说明请参阅 [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/) 文档。

**`-? | --help`**

显示 `createuser` 命令行参数的帮助并退出。

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

在默认数据库服务器上创建角色 `joe`：

```shell
$ createuser joe
```

在默认数据库服务器上创建角色 `joe`，并提示设置一些附加属性：

```shell
$ createuser --interactive joe
Shall the new role be a superuser? (y/n) **n**
Shall the new role be allowed to create databases? (y/n) **n**
Shall the new role be allowed to create more new roles? (y/n) **n**
CREATE ROLE
```

使用连接选项创建同一个角色 `joe`，显式指定其属性，并查看底层命令：

```shell
createuser -h coordinatorhost -p 54321 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT 
LOGIN;
CREATE ROLE
```

创建超级用户角色 `joe`，并立即设置密码为 `admin123`：

```shell
createuser -P -s -e joe
Enter password for new role: admin123
Enter it again: admin123
CREATE ROLE joe PASSWORD 'admin123' SUPERUSER CREATEDB 
CREATEROLE INHERIT LOGIN;
CREATE ROLE
```

在上述示例中，输入新密码时实际上不会回显；这里为了说明清楚，显示了输入的内容。不过，使用 `-e` 选项时，密码会出现在回显的命令中，如示例所示。

## 另请参阅 {#see-also}

[`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/), [dropuser](/cloudberry/reference/sys-utilities/dropuser/)
