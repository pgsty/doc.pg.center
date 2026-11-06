---
title: "reindexdb"
description: "重建数据库中的索引。"
weight: 390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/reindexdb.md"
---

## 概要 {#synopsis}

```shell
reindexdb [<connection-option> ...] [<option> ...] [-S | --schema <schema>] ...
        [-t | --table <table>] 
        [-i | --index <index>] ... [<dbname>]

reindexdb [<connection-option> ...] [<option> ...] -a | --all

reindexdb [<connection-option> ...] [<option> ...] -s | --system [<dbname>]

reindexdb -? | --help

reindexdb -V | --version
```

## 说明 {#description}

`reindexdb` 是用于重建 Apache Cloudberry 索引的工具。

`reindexdb` 是 SQL 命令 [`REINDEX`](/cloudberry/reference/sql-stmts/reindex/) 的封装。通过此工具重建数据库索引，与通过其他访问服务器的方式执行索引重建没有实质区别。

## 选项 {#options}

`reindexdb` 接受以下命令行参数：

**`-a`**<br />
**`--all`**

重建所有数据库的索引。

**`[-d] dbname`**<br />
**`[--dbname=]dbname`**

未使用 `-a` 或 `--all` 时，指定要重建索引的数据库名称。如果未指定，Apache Cloudberry 将从环境变量 `PGDATABASE` 读取数据库名。如果该变量也未设置，则使用指定的连接用户名。dbname 可以是[连接字符串](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)。此时，连接字符串参数将覆盖任何与之冲突的命令行选项。

**`-e`**<br />
**`--echo`**

回显 `reindexdb` 生成并发送给服务器的命令。

**`-i index`**<br />
**`--index=index`**

仅重建指定索引。可以指定多个 `-i` 开关，以重建多个索引。

**`-q`**<br />
**`--quiet`**

不显示进度消息。

**`-s`**<br />
**`--system`**

仅重建系统目录的索引。

**`-S schema`**<br />
**`--schema=schema`**

仅重建指定模式的索引。可以指定多个 `-S` 开关，以重建多个模式的索引。

**`-t table`**<br />
**`--table=table`**

仅重建指定表的索引。可以指定多个 `-t` 开关，以重建多个表的索引。

**`-v`**<br />
**`--verbose`**

在处理过程中打印详细信息。

**`-V`**<br />
**`--version`**

打印 `reindexdb` 版本并退出。

**`-?`**<br />
**`--help`**

显示 `reindexdb` 命令行参数的帮助并退出。

**连接选项**

`reindexdb` 还接受以下用于指定连接参数的命令行参数：

**`-h host`**<br />
**`--host=host`**

指定运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p port`**<br />
**`--port=port`**

指定 Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username`**<br />
**`--username=username`**

连接时使用的数据库用户名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统用户名。

**`-w`**<br />
**`--no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W`**<br />
**`--password`**

强制 `reindexdb` 在连接数据库前提示输入密码。
此选项并非必需，因为服务器要求密码认证时，`reindexdb` 会自动提示输入密码。不过，`reindexdb` 会为确认服务器需要密码而浪费一次连接尝试。在某些情况下，指定 `-W` 可以避免这次额外的连接尝试。

**`--maintenance-db=dbname`**

使用 `-a` 或 `--all` 时，指定连接哪个数据库，以查找还有哪些数据库需要重建索引。如果未指定，将使用 `postgres` 数据库；如果该数据库不存在，则使用 `template1`。这可以是一个[连接](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)。此时，连接字符串参数将覆盖任何与之冲突的命令行选项。此外，连接其他数据库时还会复用除数据库名本身以外的连接字符串参数。

## 注意事项 {#notes}

`reindexdb` 会锁定系统目录表，可能影响正在运行的查询。为避免干扰正在进行的业务操作，应安排在活动较少的时段执行 `reindexb` 操作。

`reindexdb` 可能需要多次连接 Coordinator 服务器，每次都要求输入密码。此时使用 `~/.pgpass` 文件会更方便。

## 环境变量 {#environment}

**`PGDATABASE`**<br />
**`PGHOST`**<br />
**`PGPORT`**<br />
**`PGUSER`**

默认连接参数。

**`PG_COLOR`**

指定是否在诊断消息中使用颜色。可选值为 `always`、`auto` 和 `never`。

与大多数其他 Apache Cloudberry 工具一样，此工具也使用 `libpq` 支持的环境变量。

## 诊断 {#diagnostics}

如果遇到问题，请参阅 [REINDEX](/cloudberry/reference/sql-stmts/reindex/) 和 [psql](/cloudberry/reference/sys-utilities/psql/) 中有关潜在问题和错误消息的讨论。数据库服务器必须在目标主机上运行。此外，`libpq` 前端库使用的所有默认连接设置和环境变量也都适用。

## 注意事项 {#notes-1}

`reindexdb` 可能需要多次连接 Apache Cloudberry 服务器，每次都要求输入密码。此时使用 `~/.pgpass` 文件会更方便。

## 示例 {#examples}

重建名为 `mydb` 的数据库的索引：

```shell
reindexdb mydb
```

在名为 `abcd` 的数据库中，重建表 `foo` 和索引 `bar`：

```shell
reindexdb --table=foo --index=bar abcd
```

## 另请参阅 {#see-also}

[REINDEX](/cloudberry/reference/sql-stmts/reindex/)
