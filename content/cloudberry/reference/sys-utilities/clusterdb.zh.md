---
title: "clusterdb"
description: "对先前使用 `CLUSTER` 聚簇过的表重新进行聚簇。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/clusterdb.md"
---

## 概要 {#synopsis}

```shell
clusterdb [<connection-option> ...] [--verbose | -v] [--table | -t <table>] [[--dbname | -d] <dbname]

clusterdb [<connection-option> ...] [--verbose | -v] --all | -a

clusterdb -? | --help

clusterdb -V | --version
```

## 说明 {#description}

对表进行聚簇，是指按某个索引对磁盘上的表进行物理重排。聚簇有助于提高使用该索引的查询的索引查找性能。聚簇是一次性操作：后续更新表时，不会对变更进行聚簇。也就是说，不会尝试按索引顺序存放新行或更新后的行。

`clusterdb` 工具查找数据库中所有曾使用 `CLUSTER` SQL 命令聚簇过的表，并按上次使用的同一个索引重新进行聚簇。从未聚簇过的表不受影响。

`clusterdb` 是 SQL 命令 [`CLUSTER`](/cloudberry/reference/sql-stmts/cluster/) 的封装。通过此工具对数据库进行聚簇，与通过其他访问服务器的方式执行聚簇没有实质区别。

## 选项 {#options}

`clusterdb` 接受以下命令行参数：

**`-a`**<br />
**`--all`**

对所有数据库进行聚簇。

**`[-d] dbname`**<br />
**`[--dbname=]dbname`**

未使用 `-a/--all` 时，指定要聚簇的数据库名称。如果未指定，将从环境变量 `PGDATABASE` 读取数据库名。如果该变量也未设置，则使用指定的连接用户名。dbname 可以是[连接字符串](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)。此时，连接字符串参数将覆盖任何与之冲突的命令行选项。

**`-e`**<br />
**`--echo`**

回显 `clusterdb` 生成并发送给服务器的命令。

**`-q`**<br />
**`--quiet`**

不显示进度消息。

**`-t table`**<br />
**`--table=table`**

仅对指定的表进行聚簇。可以指定多个 `-t` 开关，以聚簇多个表。

**`-v`**<br />
**`--verbose`**

在处理过程中打印详细信息。

**`-V`**<br />
**`--version`**

打印 `clusterdb` 版本并退出。

**`-?`**<br />
**`--help`**

显示 `clusterdb` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

`clusterdb` 还接受以下用于指定连接参数的命令行参数：

**`-h host`**<br />
**`--host=host`**

指定运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 `localhost`。

**`-p port`**<br />
**`--port=port`**

指定 Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username`**<br />
**`--username=username`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-w`**<br />
**`--no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W`**<br />
**`--password`**

强制 `clusterdb` 在连接数据库前提示输入密码。

此选项并非必需，因为服务器要求密码认证时，`clusterdb` 会自动提示输入密码。不过，`clusterdb` 会为确认服务器需要密码而浪费一次连接尝试。在某些情况下，指定 `-W` 可以避免这次额外的连接尝试。

**`--maintenance-db=dbname`**

指定连接哪个数据库，以查找还有哪些数据库需要聚簇。如果未指定，将使用 `postgres` 数据库；如果该数据库不存在，则使用 `template1`。这可以是[连接](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)字符串。此时，连接字符串参数将覆盖任何与之冲突的命令行选项。此外，连接其他数据库时还会复用除数据库名本身以外的连接字符串参数。

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

如果遇到问题，请参阅 [`CLUSTER`](/cloudberry/reference/sql-stmts/cluster/) 和 [psql](/cloudberry/reference/sys-utilities/psql/) 中有关潜在问题和错误消息的讨论。数据库服务器必须在目标主机上运行。此外，`libpq` 前端库使用的所有默认连接设置和环境变量也都适用。

## 示例 {#examples}

对名为 `test` 的数据库进行聚簇：

```shell
clusterdb test
```

对名为 `xyzzy` 的数据库中的单个表 `foo` 进行聚簇：

```shell
clusterdb --table=foo xyzzy
```

## 另请参阅 {#see-also}

[`CLUSTER`](/cloudberry/reference/sql-stmts/cluster/)
