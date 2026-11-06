---
title: "连接 Apache Cloudberry"
linkTitle: "连接数据库"
description: "本文介绍如何连接 Apache Cloudberry。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/database-basic/connect-to-cbdb.md"
---

## 连接参数 {#connection-parameters}

用户可以使用兼容 PostgreSQL 的客户端程序（如 `psql`）连接 Apache Cloudberry。用户和管理员始终通过 *Coordinator* 连接 Apache Cloudberry。Segment 不接受客户端连接。

要与 Apache Cloudberry Coordinator 建立连接，需要了解以下连接信息，并据此配置客户端程序。

|连接参数|说明|环境变量|
|--------------------|-----------|--------------------|
|应用程序名称|连接数据库的应用程序名称。该名称保存在 `application_name` 连接参数中，默认值为 *psql*。|`$PGAPPNAME`|
|数据库名称|要连接的数据库名称。对于刚完成初始化的系统，首次连接时使用 `postgres` 数据库。|`$PGDATABASE`|
|主机名|Apache Cloudberry Coordinator 的主机名。默认主机为本地主机。|`$PGHOST`|
|端口|Apache Cloudberry Coordinator 实例运行时使用的端口号。默认值为 5432。|`$PGPORT`|
|用户名|连接时使用的数据库用户（角色）名称，不一定与操作系统用户名相同。如果不确定自己的数据库用户名，请向 Apache Cloudberry 管理员确认。请注意，每个 Apache Cloudberry 系统在初始化时都会自动创建一个超级用户账号。该账号与初始化 Apache Cloudberry 系统的操作系统用户同名（通常为 `gpadmin`）。|`$PGUSER`|

[使用 psql 连接](#connect-with-psql)提供了连接 Apache Cloudberry 的命令示例。

## 支持的客户端应用程序 {#supported-client-applications}

用户可以使用多种客户端应用程序连接 Apache Cloudberry：

- Apache Cloudberry 安装中包含多个 [Apache Cloudberry 客户端应用程序](#client-utility-applications)。`psql` 客户端应用程序提供了 Apache Cloudberry 的交互式命令行界面。
- 用户可以通过 ODBC、JDBC 等标准[数据库应用程序接口](#connect-with-application-interfaces)，自行开发与 Apache Cloudberry 交互的客户端应用程序。
- 大多数使用 ODBC、JDBC 等标准数据库接口的客户端工具，都可以通过配置来连接 Apache Cloudberry。

### 客户端实用程序 {#client-utility-applications}

Apache Cloudberry 附带多个客户端实用程序，安装在 Apache Cloudberry Coordinator 主机的 `$GPHOME/bin` 目录中。以下是最常用的客户端实用程序：

|名称|用途|
|----|-----|
|`createdb`|创建新数据库|
|`createuser`|定义新的数据库角色|
|`dropdb`|删除数据库|
|`dropuser`|删除角色|
|`psql`|PostgreSQL 交互式终端|
|`reindexdb`|重建数据库的索引|
|`vacuumdb`|对数据库进行垃圾回收和分析|

使用这些客户端应用程序时，必须通过 Apache Cloudberry Coordinator 实例连接数据库。你需要知道目标数据库名称、Coordinator 的主机名和端口号，以及连接时使用的数据库用户名。可以分别通过命令行选项 `-d`、`-h`、`-p` 和 `-U` 提供这些信息。如果某个参数不属于任何选项，则优先将其解释为数据库名称。

所有这些选项都有默认值，未指定选项时就会使用相应的默认值。默认主机为本地主机，默认端口号为 5432。默认用户名和默认数据库名称都与你的操作系统用户名相同。请注意，操作系统用户名和 Apache Cloudberry 用户名不一定相同。

如果默认值不合适，可以将环境变量 `PGDATABASE`、`PGHOST`、`PGPORT` 和 `PGUSER` 设置为适当的值，或使用 `psql` 的 `~/.pgpass` 文件保存常用密码。

### 使用 psql 连接 {#connect-with-psql}

根据所用的默认值或已设置的环境变量，可以按以下示例通过 `psql` 访问数据库：

```shell
$ psql -d mydatabase -h coordinator_host -p 5432 -U `gpadmin`
```

```shell
$ psql mydatabase
```

```shell
$ psql
```

如果尚未创建用户定义的数据库，可以连接 `postgres` 数据库来访问系统。例如：

```shell
$ psql postgres
```

连接数据库后，`psql` 会提供提示符，其中包含 `psql` 当前连接的数据库名称，后接字符串 `=>`（如果你是数据库超级用户，则为 `=#`）。例如：

```shell
mydatabase=>
```

可以在提示符后输入 SQL 命令。SQL 命令必须以 `;`（分号）结尾，才会发送到服务器执行。例如：

```sql
=> SELECT * FROM mytable;
```

## 通过应用程序接口连接 {#connect-with-application-interfaces}

你可能希望自行开发与 Apache Cloudberry 交互的客户端应用程序。PostgreSQL 为最常用的数据库应用程序编程接口（API）提供了多种数据库驱动，这些驱动也可以用于 Apache Cloudberry。驱动需要单独下载。除随 PostgreSQL 提供的 libpq 外，每种驱动都是独立的 PostgreSQL 开发项目，必须下载、安装并配置后才能连接 Apache Cloudberry。可用的驱动如下：

|API|PostgreSQL 驱动|下载链接|
|---|-----------------|-------------|
|ODBC|psqlODBC|[https://odbc.postgresql.org/](https://odbc.postgresql.org/)|
|JDBC|pgjdbc|[https://jdbc.postgresql.org/](https://jdbc.postgresql.org/)|
|Perl DBI|pgperl|[https://metacpan.org/release/DBD-Pg](https://metacpan.org/release/DBD-Pg)|
|Python DBI|pygresql|[http://www.pygresql.org/](http://www.pygresql.org/)|
|Python DBI|psycopg2|[https://www.psycopg.org/](https://www.psycopg.org/)|
|libpq C 库|libpq|[https://www.postgresql.org/docs/14/libpq.html](https://www.postgresql.org/docs/14/libpq.html)|

通过 API 访问 Apache Cloudberry 的一般步骤如下：

1. 从相应的来源下载所用编程语言的平台及对应的 API。例如，可以从 Oracle 获取 Java 开发工具包（JDK）和 JDBC API。
2. 按照 API 规范编写客户端应用程序。编程时，应了解 Apache Cloudberry 对 SQL 的支持情况，避免使用不受支持的 SQL 语法。

下载适当的驱动，并配置到 Apache Cloudberry Coordinator 实例的连接。

## 排查连接问题 {#troubleshoot-connection-problems}

多种原因可能导致客户端应用程序无法成功连接 Apache Cloudberry。本节介绍连接问题的一些常见原因及解决方法。

| 问题 | 解决方法 |
| ------- | -------- |
| `pg_hba.conf` 中没有对应主机或用户的条目 | 要使 Apache Cloudberry 接受远程客户端连接，必须配置 Apache Cloudberry Coordinator 实例，允许将要连接 Apache Cloudberry 的客户端主机和数据库用户建立连接。为此，需要在 `pg_hba.conf` 配置文件（位于 Coordinator 实例的数据目录中）中添加相应条目。 |
| Apache Cloudberry 未运行 | 如果 Apache Cloudberry Coordinator 实例已停止，用户将无法连接。可以在 Apache Cloudberry Coordinator 主机上运行 `gpstate` 实用程序，确认 Apache Cloudberry 系统是否处于运行状态。 |
| 网络问题：Interconnect 超时 | 如果用户从远程客户端连接 Apache Cloudberry Coordinator 主机，网络问题可能导致无法连接（例如 DNS 主机名解析问题、主机系统宕机等）。要排除网络问题，可以从远程客户端主机连接 Apache Cloudberry Coordinator 主机。例如：`ping hostname`<br/><br/>如果系统无法解析 Apache Cloudberry 所涉及主机的主机名和 IP 地址，查询和连接就会失败。有些操作通过 `localhost` 连接 Apache Cloudberry Coordinator，另一些则使用实际主机名，因此两者都必须能解析。如果遇到此错误，首先应确保能够从 Coordinator 主机通过网络连接 Apache Cloudberry 集群中的每台主机。在 Coordinator 和所有 Segment 的 `/etc/hosts` 文件中，确保正确配置 Apache Cloudberry 集群中所有主机的主机名和 IP 地址。IP 地址 `127.0.0.1` 必须解析为 `localhost`。 |
