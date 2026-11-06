---
title: "pg_restore"
description: "从 `pg_dump` 创建的归档文件中恢复数据库。"
weight: 370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-restore.md"
---

## 概要 {#synopsis}

```shell
pg_restore [<connection-option> ...] [<restore_option> ...] <filename>

pg_restore -? | --help

pg_restore -V | --version
```

## 说明 {#description}

`pg_restore` 工具从 [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) 创建的某种非纯文本格式归档中恢复数据库。它发出必要的命令，将数据库重建到保存时的状态。归档文件还允许 `pg_restore` 有选择地恢复内容，甚至在恢复前重新排列各项的顺序。

`pg_restore` 可以按两种模式运行。如果指定数据库名，则将归档直接恢复到该数据库；否则，会生成一个包含重建数据库所需 SQL 命令的脚本，并写入文件或标准输出。脚本输出等同于 `pg_dump` 的纯文本输出格式，因此部分控制输出的选项与 `pg_dump` 选项类似。

`pg_restore` 无法恢复归档文件中不存在的信息。例如，如果归档采用“将数据转储为 `INSERT` 命令”选项创建，`pg_restore` 就无法使用 `COPY` 语句加载数据。

## 选项 {#options}

**`filename`**

指定待恢复归档文件的位置（对于目录格式归档，则为目录位置）。如果未指定，使用标准输入。

### 恢复选项 {#restore-options}

**`-a | --data-only`**

仅恢复数据，不恢复模式（数据定义）。如果归档包含表数据和序列值，则恢复这些内容。

此选项类似于指定 `--section=data`，但由于历史原因，两者并不完全相同。

**`-c | --clean`**

重新创建数据库对象前，先清理（删除）它们。（如果目标数据库中不存在某些对象，可能会产生一些无害的错误消息。）

**`-C | --create`**

先创建数据库，再恢复到其中。如果还指定了 `--clean`，则在连接目标数据库前先删除并重新创建它。

使用此选项时，`-d` 指定的数据库仅用于发出最初的 `DROP DATABASE` 和 `CREATE DATABASE` 命令。所有数据都恢复到归档中所指名的数据库。

**`-d dbname | --dbname=dbname`**

连接此数据库并直接恢复到其中。与大多数其他 Apache Cloudberry 工具一样，此工具也使用 `libpq` 支持的环境变量。但未提供数据库名时，它不会读取 `PGDATABASE`。

**`-e | --exit-on-error`**

向数据库发送 SQL 命令时如果遇到错误，则退出。默认继续执行，并在恢复结束时显示错误数量。

**`-f outfilename | --file=outfilename`**

指定生成脚本的输出文件；与 `-l` 一起使用时，则指定列表的输出文件。默认为标准输出。

**`-F c|d|t | --format={custom | directory | tar}`**

由 [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) 生成的归档格式。无需指定，因为 `pg_restore` 会自动确定格式。格式可以是 `custom`、`directory` 或 `tar`。

**`-I index | --index=index`**

仅恢复指定索引的定义。

**`-j | --number-of-jobs | --jobs=number-of-jobs`**

使用多个并发作业执行 `pg_restore` 中最耗时的部分，即加载数据、创建索引或创建约束。对于运行在多处理器机器上的服务器，此选项可以显著缩短大型数据库的恢复时间。

根据操作系统不同，每个作业是一个进程或线程，并使用一个独立的服务器连接。

此选项的最佳值取决于服务器、客户端和网络的硬件配置，包括 CPU 核数和磁盘配置等因素。可以从服务器的 CPU 核数开始尝试，但在很多情况下，更大的值也能缩短恢复时间。当然，过大的值会因资源抖动而降低性能。

此选项仅支持自定义归档格式。输入文件必须是普通文件，不能是管道等。输出脚本而非直接连接数据库服务器时，会忽略此选项。此外，多作业不能与 `--single-transaction` 选项一起使用。

**`-l | --list`**

列出归档内容。此操作的输出可配合 `-L` 选项，限制待恢复项并重新排序。

**`-L list-file | --use-list=list-file`**

仅恢复 list-file 中列出的项，并按文件中的顺序恢复。注意，如果将 `-n` 或 `-t` 等筛选开关与 `-L` 一起使用，会进一步限制恢复的项。

list-file 通常通过编辑先前 `-l` 操作的输出创建。可以移动或删除行，也可以在行首加分号（;）将其注释掉。示例见下文。

**`-n schema | --schema=schema`**

仅恢复指定模式中的对象。可与 `-t` 选项组合，仅恢复特定表。

**`-O | --no-owner`**

不输出用于将对象所有权设为与原数据库一致的命令。默认情况下，`pg_restore` 发出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 语句，设置创建的模式元素的所有权。除非最初以超级用户（或脚本中所有对象的共同所有者）身份连接数据库，否则这些语句会失败。使用 `-O` 后，可用任意用户名建立初始连接，该用户将拥有所有创建的对象。

**`-P 'function-name(argtype [, ...])' | --function='function-name(argtype [, ...])'`**

仅恢复指定函数。函数名必须用引号括起。函数名和参数的拼写必须与转储文件的内容目录中完全一致（通过 `--list` 选项显示）。

**`-s | --schema-only`**

仅恢复归档中包含的模式（数据定义）条目，不恢复数据。

此选项与 `--data-only` 相反。它类似于指定 `--section=pre-data --section=post-data`，但由于历史原因，两者并不完全相同。

（不要将它与 `--schema` 选项混淆，后者使用“模式”一词的另一种含义。）

**`-S username | --superuser=username`**

指定禁用触发器时使用的超级用户名。仅在使用 `--disable-triggers` 时有效。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`-t table | --table=table`**

仅恢复指定表的定义和／或数据。可以使用多个 `-t` 开关指定多个表。可与 `-n` 选项组合以指定模式。

**`-T trigger | --trigger=trigger`**

仅恢复指定触发器。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`-v | --verbose`**

指定详细模式。

**`-V | --version`**

打印 `pg_restore` 版本并退出。

**`-x | --no-privileges | --no-acl`**

不恢复访问权限（`GRANT/REVOKE` 命令）。

**`-1 | --single-transaction`**

将恢复作为单个事务执行。这确保所有命令要么全部成功完成，要么不应用任何更改。

**`--disable-triggers`**

此选项仅在执行纯数据恢复时有效。它指示 `pg_restore` 执行命令，在重新加载数据期间临时禁用目标表上的触发器。如果表上有不希望在重新加载数据时调用的触发器，可使用此选项。`--disable-triggers` 输出的命令必须以超级用户身份执行。因此，还应使用 `-S` 指定超级用户名，或最好以超级用户身份运行 `pg_restore`。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`--no-data-for-failed-tables`**

默认情况下，即使创建某个表的命令失败（例如，因为表已存在），仍会恢复该表的数据。使用此选项后，会跳过此类表的数据。如果目标数据库可能已包含所需表内容，此行为很有用，可以防止加载重复或过时数据。此选项仅在直接恢复到数据库时有效，生成 SQL 脚本输出时无效。

**`--no-security-labels`**

不输出恢复安全标签的命令，即使归档中包含这些标签。

**`--no-tablespaces`**

不输出选择表空间的命令。使用此选项后，所有对象都将在恢复时的默认表空间中创建。

**`--section=sectionname`**

仅恢复指定部分。部分名称可以是 `pre-data`、`data` 或 `post-data`。可以多次指定此选项，选择多个部分。

默认恢复所有部分。

**`--use-set-session-authorization`**

输出 SQL 标准的 `SET SESSION AUTHORIZATION` 命令，代替 `ALTER OWNER` 命令来确定对象所有权。这使转储更符合标准，但根据转储中对象的历史，可能无法正确恢复。

**`-? | --help`**

显示 `pg_restore` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

**`-h host | --host host`**

运行 Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p port | --port port`**

Apache Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U username | --username username`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`-W | --password`**

强制提示输入密码。

**`--role=rolename`**

指定执行恢复时使用的角色名。此选项使 `pg_restore` 在连接数据库后发出 `SET ROLE rolename` 命令。当认证用户（由 `-U` 指定）缺少 `pg_restore` 所需的权限，但可以切换到具有所需权限的角色时，此选项很有用。有些安装环境禁止直接以超级用户身份登录，使用此选项可以在不违反该策略的情况下执行恢复。

## 注意事项 {#notes}

如果安装环境向 `template1` 数据库添加了本地对象，应确保将 `pg_restore` 的输出加载到真正为空的数据库，否则可能因重复定义这些新增对象而报错。要创建不包含任何本地新增对象的空数据库，应从 `template0` 而非 `template1` 复制，例如：

```sql
CREATE DATABASE foo WITH TEMPLATE template0;
```

向已有表恢复数据且使用 `--disable-triggers` 选项时，`pg_restore` 会在插入数据前发出命令禁用用户表上的触发器，并在数据插入后发出命令重新启用它们。如果恢复中途停止，系统目录可能处于错误状态。

有关 `pg_dump` 限制的详细信息，另请参阅 `pg_dump` 文档。

恢复后，建议对每个已恢复表运行 `ANALYZE`，使查询规划器获得有用的统计信息。

## 示例 {#examples}

假设已将名为 `mydb` 的数据库转储到自定义格式的转储文件：

```shell
pg_dump -Fc mydb > db.dump
```

删除数据库并从转储中重新创建它：

```shell
dropdb mydb
pg_restore -C -d template1 db.dump
```

将转储重新加载到名为 `newdb` 的新数据库中。注意，这里没有使用 `-C`，而是直接连接待恢复的数据库。此外，新数据库从 `template0` 而非 `template1` 克隆，以确保初始为空：

```shell
createdb -T template0 newdb
pg_restore -d newdb db.dump
```

要重新排列数据库项，首先需要转储归档的内容目录：

```shell
pg_restore -l db.dump > db.list
```

列表文件由文件头及每项对应的一行组成，例如：

```shell
; Archive created at Mon Sep 14 13:55:39 2009
;     dbname: DBDEMOS
;     TOC Entries: 81
;     Compression: 9
;     Dump Version: 1.10-0
;     Format: CUSTOM
;     Integer: 4 bytes
;     Offset: 8 bytes
;     Dumped from database version: 9.4.24
;     Dumped by pg_dump version: 9.4.24
;
; Selected TOC Entries:
;
3; 2615 2200 SCHEMA - public pasha
1861; 0 0 COMMENT - SCHEMA public pasha
1862; 0 0 ACL - public pasha
317; 1247 17715 TYPE public composite pasha
319; 1247 25899 DOMAIN public domain0 pasha2
```

分号表示注释的开始，行首数字是分配给各项的内部归档 ID。文件中的行可以注释掉、删除或重新排序。例如：

```shell
10; 145433 TABLE map_resolutions postgres
;2; 145344 TABLE species postgres
;4; 145359 TABLE nt_header postgres
6; 145402 TABLE species_records postgres
;8; 145416 TABLE ss_old postgres
```

可将其作为 `pg_restore` 的输入，仅按顺序恢复第 10 项和第 6 项：

```shell
pg_restore -L db.list db.dump
```

## 另请参阅 {#see-also}

[pg_dump](/cloudberry/reference/sys-utilities/pg-dump/)
