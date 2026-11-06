---
title: "vacuumdb"
description: "对数据库进行垃圾回收和分析。"
weight: 400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/vacuumdb.md"
---

## 概要 {#synopsis}

```shell
vacuumdb [<connection-option>...] [--full | -f] [--freeze | -F] [--verbose | -v]
    [--analyze | -z] [--analyze-only | -Z] [--disable-page-skipping] [--skip-locked] [--table | -t <table> [( <column> [,...] )] ] [<dbname>]

vacuumdb [<connection-option>...] [--all | -a] [--full | -f] [-F] 
    [--verbose | -v] [--analyze | -z]
    [--analyze-only | -Z]
    [--disable-page-skipping]
    [--skip-locked]

vacuumdb -? | --help

vacuumdb -V | --version
```

## 说明 {#description}

`vacuumdb` 是用于清理 Apache Cloudberry 数据库的工具。`vacuumdb` 还会生成 Apache Cloudberry 查询优化器使用的内部统计信息。

`vacuumdb` 是 SQL 命令 `VACUUM` 的封装。通过此工具对数据库执行清理，与通过其他访问服务器的方式执行清理没有实质区别。

## 选项 {#options}

**`-a | --all`**

清理所有数据库。

**`[-d] dbname | [--dbname=]dbname`**

要清理的数据库名称。如果未指定，且未使用 `-a`（或 `--all`），则从环境变量 `PGDATABASE` 读取数据库名。如果该变量也未设置，则使用指定的连接用户名。

**`-e | --echo`**

回显 `reindexdb` 生成并发送给服务器的命令。

**`-f | --full`**

选择完整清理。这可能回收更多空间，但耗时长得多，而且会独占锁定表。

> **小心** 不建议在 Apache Cloudberry 中执行 `VACUUM FULL`。

**`-F | --freeze`**

冻结行的事务信息。

**`-q | --quiet`**

不显示响应。

**`-t table [(column)] | --table= table [(column)]`**

仅清理或分析此表。只有与 `--analyze` 或 `--analyze-all` 选项一起使用时，才能指定列名。可以指定多个 `-t` 开关来清理多个表。如果指定列，可能需要对括号进行转义，以免被 shell 解释。

**`-v | --verbose`**

在处理过程中打印详细信息。

**`-z | --analyze`**

收集供查询规划器使用的统计信息。

**`-Z | --analyze-only`**

仅计算供查询规划器使用的统计信息（不执行清理）。

**`--disable-page-skipping`**

禁用所有跳过页面的行为。

**`--skip-locked`**

跳过无法立即锁定的关系。

**`-V | --version`**

打印 `vacuumdb` 版本并退出。

**`-? | --help`**

显示 `vacuumdb` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

**`-h host | --host=host`**

指定运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p port | --port=port`**

指定 Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username | --username=username`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统用户名。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W | --password`**

强制提示输入密码。

**`--maintenance-db=dbname`**

指定连接哪个数据库，以查找还有哪些数据库需要清理。如果未指定，将使用 `postgres` 数据库；如果该数据库不存在，则使用 `template1`。

## 注意事项 {#notes}

`vacuumdb` 可能需要多次连接 Coordinator 服务器，每次都要求输入密码。此时使用 `~/.pgpass` 文件会更方便。

## 示例 {#examples}

清理数据库 `test`：

```shell
vacuumdb test
```

清理并分析名为 `bigdb` 的数据库：

```shell
vacuumdb --analyze bigdb
```

清理名为 `mydb` 的数据库中的单个表 `foo`，并分析该表的单个列 `bar`。注意，表名和列名外的引号用于避免括号被 shell 解释：

```shell
vacuumdb --analyze --verbose --table 'foo(bar)' mydb
```

## 另请参阅 {#see-also}

[`VACUUM`](/cloudberry/reference/sql-stmts/vacuum/), [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/)
