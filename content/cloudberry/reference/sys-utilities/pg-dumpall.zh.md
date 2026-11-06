---
title: "pg_dumpall"
description: "将 Apache Cloudberry 系统中的所有数据库导出到单个脚本文件或其他归档文件。"
weight: 350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-dumpall.md"
---

## 概要 {#synopsis}

```shell
pg_dumpall [<connection-option> ...] [<dump_option> ...]

pg_dumpall -? | --help

pg_dumpall -V | --version
```

## 说明 {#description}

`pg_dumpall` 是标准 PostgreSQL 工具，用于备份 Apache Cloudberry（或 PostgreSQL）实例中的所有数据库，Apache Cloudberry 也支持此工具。它创建单个（非并行）转储文件。对于 Apache Cloudberry 的常规备份，最好使用 Apache Cloudberry 备份工具 gpbackup，以获得最佳性能。

`pg_dumpall` 创建单个脚本文件，其中包含可输入 [psql](/cloudberry/reference/sys-utilities/psql/) 以恢复数据库的 SQL 命令。它通过对每个数据库调用 [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) 完成此工作。`pg_dumpall` 还转储所有数据库共用的全局对象。（`pg_dump` 不保存这些对象。）目前包括数据库用户和组的信息，以及应用于整个数据库的访问权限。

由于 `pg_dumpall` 会读取所有数据库的表，要生成完整转储，很可能需要以数据库超级用户身份连接。运行保存的脚本时也需要超级用户权限，以便添加用户和组，以及创建数据库。

SQL 脚本将写入标准输出。使用 `[-f | --file]` 选项或 shell 运算符可将其重定向到文件。

`pg_dumpall` 需要多次连接 Apache Cloudberry Coordinator 服务器（每个数据库一次）。使用密码认证时，可能每次都要求输入密码。此时使用 `~/.pgpass` 文件会更方便。

## 选项 {#options}

### 转储选项 {#dump-options}

**`-a | --data-only`**

仅转储数据，不转储模式（数据定义）。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-c | --clean`**
输出在创建数据库对象的命令之前清理（删除）这些对象的命令。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-f filename | --file=filename`**

将输出发送到指定文件。

**`-g | --globals-only`**

仅转储全局对象（角色和表空间），不转储数据库。

**`-o | --oids`**

将对象标识符（OID）作为各表数据的一部分转储。不建议对准备恢复到 Apache Cloudberry 的文件使用此选项。

**`-O | --no-owner`**

不输出用于将对象所有权设为与原数据库一致的命令。默认情况下，[pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) 发出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 语句，设置创建的数据库对象的所有权。除非以超级用户（或脚本中所有对象的共同所有者）身份运行脚本，否则这些语句会失败。要生成任何用户都可恢复、并让该用户拥有所有对象的脚本，请指定 `-O`。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-r | --roles-only`**

仅转储角色，不转储数据库或表空间。

**`-s | --schema-only`**

仅转储对象定义（模式），不转储数据。

**`-S username | --superuser=username`**

指定禁用触发器时使用的超级用户名。仅在使用 `--disable-triggers` 时有效。最好省略此选项，直接以超级用户身份运行生成的脚本。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`-t | --tablespaces-only`**

仅转储表空间，不转储数据库或角色。

**`-v | --verbose`**

指定详细模式，使 [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) 将详细的对象注释及开始／结束时间输出到转储文件，并将进度消息输出到标准错误。

**`-V | --version`**

打印 `pg_dumpall` 版本并退出。

**`-x | --no-privileges | --no-acl`**

不转储访问权限（`GRANT/REVOKE` 命令）。

**`--binary-upgrade`**

此选项供就地升级工具使用。不建议也不支持将其用于其他用途。此选项的行为可能在未来版本中更改，恕不另行通知。

**`--column-inserts | --attribute-inserts`**

使用包含显式列名的 `INSERT` 命令（`INSERT INTO <table> (<column>, ...) VALUES ...`）转储数据。这会使恢复非常缓慢，主要用于生成可加载到非 PostgreSQL 系数据库的转储。此外，因为每行生成独立命令，重新加载某行时出错只会丢失该行，而非整个表的内容。

**`--disable-dollar-quoting`**

禁用函数体的美元引用，强制采用 SQL 标准字符串语法引用函数体。

**`--disable-triggers`**

此选项仅在创建纯数据转储时有效。它指示 `pg_dumpall` 加入命令，在重新加载数据期间临时禁用目标表上的触发器。如果表上有不希望在重新加载数据时调用的触发器，可使用此选项。`--disable-triggers` 输出的命令必须以超级用户身份执行。因此，还应使用 `-S` 指定超级用户名，或最好确保以超级用户身份运行生成的脚本。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`--inserts`**

使用 `INSERT` 命令（而非 `COPY`）转储数据。这会使恢复非常缓慢，主要用于生成可加载到非 PostgreSQL 系数据库的转储。此外，因为每行生成独立命令，重新加载某行时出错只会丢失该行，而非整个表的内容。注意，如果重新排列过列顺序，恢复可能完全失败。`--column-inserts` 选项能适应列顺序变化，但速度更慢。

**`--lock-wait-timeout=timeout`**

转储开始时，不无限等待获取表上的共享锁。如果无法在指定超时时间内锁定某个表，则失败。超时时间可以使用 `SET statement_timeout` 接受的任何格式。允许的值因待转储服务器的版本而异，但所有 Apache Cloudberry 版本都接受以毫秒表示的整数。

**`--no-security-labels`**

不转储安全标签。

**`--no-tablespaces`**

不输出选择表空间的命令。使用此选项后，所有对象都将在恢复时的默认表空间中创建。

**`--no-unlogged-table-data`**

不转储不记录 WAL 的表的内容。此选项不影响是否转储表定义（模式），仅阻止转储表数据。

**`--quote-all-identifiers`**

强制为所有标识符添加引号。默认情况下，`pg_dumpall` 仅对其自身主版本中的保留字标识符添加引号。其他版本服务器的保留字集合可能略有不同，这有时会导致兼容性问题。使用 `--quote-all-identifiers` 可避免此类问题，但生成的转储脚本更难阅读。

**`--resource-queues`**

转储资源队列定义。

**`--resource-groups`**

转储资源组定义。

**`--use-set-session-authorization`**

输出 SQL 标准的 `SET SESSION AUTHORIZATION` 命令，代替 `ALTER OWNER` 命令来确定对象所有权。这使转储更符合标准，但根据转储中对象的历史，可能无法正确恢复。使用 `SET SESSION AUTHORIZATION` 的转储需要超级用户权限才能正确恢复，而 `ALTER OWNER` 所需的权限较低。

**`--gp-syntax`**

在 `CREATE TABLE` 语句中输出 Apache Cloudberry 语法。这允许转储 Apache Cloudberry 表的分布策略（`DISTRIBUTED BY` 或 `DISTRIBUTED RANDOMLY` 子句），便于恢复到其他 Apache Cloudberry 系统。

**`--no-gp-syntax`**

不在 `CREATE TABLE` 语句中输出表分布子句。

**`-? | --help`**

显示 `pg_dumpall` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

**`-d connstr | --dbname=connstr`**

以连接字符串形式指定连接服务器的参数。更多信息请参阅 PostgreSQL 文档中的[连接字符串](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)。

为与其他客户端应用程序保持一致，此选项名为 `--dbname`。但由于 `pg_dumpall` 需要连接多个数据库，连接字符串中的数据库名会被忽略。使用 `-l` 选项可指定用于转储全局对象和查找其他待转储数据库的数据库名称。

**`-h host | --host=host`**

运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 `localhost`。

**`-l dbname | --database=dbname`**

指定转储全局对象时连接的数据库名称。如果未指定，使用 `postgres` 数据库。如果 `postgres` 数据库不存在，则使用 `template1` 数据库。

**`-p port | --port=port`**

Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 `5432`。

**`-U username | --username= username`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W | --password`**

强制提示输入密码。

**`--role=rolename`**

指定创建转储时使用的角色名。此选项使 `pg_dumpall` 在连接数据库后发出 `SET ROLE <rolename>` 命令。当认证用户（由 `-U` 指定）缺少 `pg_dumpall` 所需的权限，但可以切换到具有所需权限的角色时，此选项很有用。有些安装环境禁止直接以超级用户身份登录，使用此选项可以在不违反该策略的情况下创建转储。

## 注意事项 {#notes}

由于 `pg_dumpall` 内部会调用 [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/)，某些诊断消息会提到 `pg_dump`。

恢复后，建议对每个数据库运行 `ANALYZE`，使查询规划器获得有用的统计信息。也可以运行 `vacuumdb -a -z` 清理并分析所有数据库。

`pg_dumpall` 要求在恢复前创建所有必需的表空间目录，否则位于非默认位置的数据库将创建失败。

## 示例 {#examples}

转储所有数据库：

```shell
pg_dumpall > db.out
```

可使用以下命令从此文件重新加载数据库：

```shell
psql template1 -f db.out
```

仅转储全局对象（包括资源队列）：

```shell
pg_dumpall -g --resource-queues
```

## 另请参阅 {#see-also}

[pg_dump](/cloudberry/reference/sys-utilities/pg-dump/)
