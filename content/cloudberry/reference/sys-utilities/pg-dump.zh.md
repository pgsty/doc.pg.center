---
title: "pg_dump"
description: "将数据库导出为单个脚本文件或其他归档文件。"
weight: 340
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-dump.md"
---

## 概要 {#synopsis}

```shell
pg_dump [<connection-option> ...] [<dump_option> ...] [<dbname>]

pg_dump -? | --help

pg_dump -V | --version
```

## 说明 {#description}

`pg_dump` 是标准 PostgreSQL 工具，用于备份数据库，Apache Cloudberry 也支持此工具。它创建单个（非并行）转储文件。对于 Apache Cloudberry 的常规备份，最好使用 Apache Cloudberry 备份工具 gpbackup，以获得最佳性能。

将数据迁移到其他数据库厂商的系统，或迁移到 Segment 配置不同的其他 Apache Cloudberry 系统（例如，目标系统的 Segment 实例更多或更少）时，应使用 `pg_dump`。恢复时，如果转储文件为归档格式，必须使用对应的 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 工具；如果转储文件为纯文本格式，则可以使用 [psql](/cloudberry/reference/sys-utilities/psql/) 等客户端程序。

由于 `pg_dump` 与标准 PostgreSQL 兼容，可以用它将数据迁移到 Apache Cloudberry。Apache Cloudberry 中的 `pg_dump` 工具与 PostgreSQL 的 `pg_dump` 工具非常相似，但有以下例外和限制：

- 使用 `pg_dump` 备份 Apache Cloudberry 数据库时，请注意，对于超大型数据库，转储操作可能耗时很长（数小时）。还必须确保有足够的磁盘空间创建转储文件。
- 将数据从一个 Apache Cloudberry 系统迁移到另一个系统时，请使用 `--gp-syntax` 命令行选项，在 `CREATE TABLE` 语句中包含 `DISTRIBUTED BY` 子句。这样可以确保恢复时 Apache Cloudberry 表数据按正确的分布键列分布。

即使数据库正在被并发使用，`pg_dump` 也会创建一致的备份。`pg_dump` 不会阻塞其他访问数据库的用户（读者或写入者）。

与某种归档文件格式结合并配合 `pg_restore` 使用时，`pg_dump` 提供灵活的归档和传输机制。可以使用 `pg_dump` 备份整个数据库，然后使用 `pg_restore` 检查归档，和／或选择要恢复的数据库部分。最灵活的输出文件格式是自定义格式（`-Fc`）和目录格式（`-Fd`）。它们允许选择并重新排列所有归档项，支持并行恢复，并且默认进行压缩。目录格式是唯一支持并行转储的格式。

## 选项 {#options}

**`<dbname>`**

指定要转储的数据库名称。如果未指定，将使用环境变量 `PGDATABASE`。如果该变量也未设置，则使用指定的连接用户名。

### 转储选项 {#dump-options}

-a | --data-only
仅转储数据，不转储模式（数据定义）。将转储表数据和序列值。

此选项类似于指定 `--section=data`，但由于历史原因，两者并不完全相同。

**`-b | --blobs`**

将大对象包含在转储中。除非指定了 `--schema`、`--table` 或 `--schema-only`，否则默认执行此操作。只有在请求特定模式或表的转储时，`-b` 开关才有用于添加大对象的意义。注意，大对象被视为数据，因此使用 `--data-only` 时会包含大对象，使用 `--schema-only` 时则不会。

> **注意** Apache Cloudberry 不支持 PostgreSQL 的[大对象功能](https://www.postgresql.org/docs/12/largeobjects.html)，无法通过该功能流式传输存储在大对象结构中的用户数据。

**`-c | --clean`**

在文本输出文件中加入命令，以便在输出创建数据库对象的命令前清理（删除）这些对象。（如果目标数据库中不存在某些对象，恢复时可能产生一些无害的错误消息。）注意，转储操作开始前不会删除对象，而是将 `DROP` 命令加入 DDL 转储输出文件，以便使用这些文件恢复时，在 `CREATE` 命令前运行 `DROP` 命令。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-C | --create`**

以创建数据库本身并重新连接到所创建数据库的命令开始输出。（使用这种形式的脚本时，在运行脚本前连接目标安装中的哪个数据库都无关紧要。）如果同时指定 `--clean`，脚本会先删除并重新创建目标数据库，再重新连接。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-E <encoding> | --encoding=<encoding>`**

使用指定的字符集编码创建转储。默认情况下，转储使用数据库编码创建。（另一种获得相同结果的方法是将 `PGCLIENTENCODING` 环境变量设为所需的转储编码。）

**`-f <file> | --file=<file>`**

将输出发送到指定文件。对于基于文件的输出格式，可以省略此参数，此时使用标准输出。但对于目录输出格式必须提供此参数，此时它指定目标目录而非文件。在这种情况下，目录由 `pg_dump` 创建，且事先不得存在。

**`-F p|c|d|t | --format=plain|custom|directory|tar`**

选择输出格式。format 可以是以下格式之一：

- p | plain — 输出纯文本 SQL 脚本文件（默认）。
- c | custom — 输出适合输入 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 的自定义归档。与目录输出格式一起，这是最灵活的输出格式，因为它允许在恢复期间手动选择并重新排列归档项。此格式默认压缩，也支持并行转储。
- d | directory — 输出适合输入 `pg_restore` 的目录格式归档。此操作会创建一个目录，其中每个被转储的表和大对象各有一个文件，另外还有一个所谓的内容目录文件，以机器可读的格式描述被转储的对象，`pg_restore` 可以读取该文件。目录格式归档可以使用标准 Unix 工具处理；例如，可以使用 `gzip` 压缩未压缩归档中的文件。此格式默认压缩。
- t | tar — 输出适合输入 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 的 tar 格式归档。tar 格式与目录格式兼容；提取 tar 格式归档会生成有效的目录格式归档。但是，tar 格式不支持压缩。此外，使用 tar 格式时，恢复期间不能更改表数据项的相对顺序。

**`-j <njobs> | --jobs=<njobs>`**

通过同时转储 `<njobs>` 个表来并行执行转储。此选项会缩短转储时间，但也会增加数据库服务器负载。只能将此选项与目录输出格式一起使用，因为只有该输出格式允许多个进程同时写入数据。

> **注意** 使用 `pg_dump` 的并行转储只在查询分发器（Coordinator）节点上并行，而不像使用 `gpbackup` 时那样跨查询执行器（Segment）节点并行。

`pg_dump` 会打开 `<njobs> + 1` 个数据库连接，因此请确保 `max_connections` 设置足以容纳所有连接。

并行转储期间请求数据库对象上的排他锁，可能导致转储失败。原因是，`pg_dump` Coordinator 进程会请求工作进程稍后要转储的对象上的共享锁，以确保转储运行期间没有人删除这些对象。如果另一个客户端随后请求表上的排他锁，该锁不会立即授予，而会排队等待 Coordinator 进程释放共享锁。因此，对该表的任何其他访问也不会获准，并会排在排他锁请求之后，其中包括尝试转储该表的工作进程。若不采取预防措施，这将形成典型的死锁。为检测此冲突，`pg_dump` 工作进程使用 `NOWAIT` 选项再次请求共享锁。如果工作进程未获授此共享锁，说明此期间其他人请求了排他锁，转储无法继续，`pg_dump` 只能取消转储。

要创建一致的备份，数据库服务器必须支持同步快照。借助此功能，数据库客户端即使使用不同连接，也能确保看到同一数据集。`pg_dump -j` 使用多个数据库连接：Coordinator 进程连接数据库一次，每个工作作业再连接一次。如果没有同步快照功能，就无法保证不同工作作业在各自连接中看到相同数据，可能导致备份不一致。

如果要对 6.0 以前版本的服务器执行并行转储，必须确保从 Coordinator 连接数据库到最后一个工作作业连接数据库期间，数据库内容不发生变化。最简单的做法是在开始备份前，停止访问该数据库的所有数据修改进程（DDL 和 DML）。

**`-n <schema> | --schema=<schema>`**

仅转储匹配模式的模式；这会选择该模式本身及其包含的所有对象。如果未指定此选项，将转储目标数据库中的所有非系统模式。可以通过多次写入 `-n` 开关来选择多个模式。此外，模式参数会按照与 `psql` 的 `\d` 命令相同的规则解释为模式，因此也可以在模式中写入通配符来选择多个模式。使用通配符时，如有需要请注意给模式加引号，防止 shell 扩展通配符。

注意：指定 -n 时，`pg_dump` 不会尝试转储所选模式可能依赖的任何其他数据库对象。因此，无法保证特定模式转储的结果能够单独成功恢复到干净数据库中。

> **注意** 指定 `-n` 时，不会转储大对象等非模式对象。可以使用 `--blobs` 开关将大对象加回转储。

**`-N <schema> | --exclude-schema=<schema>`**

不转储匹配模式的任何模式。模式按与 `-n` 相同的规则解释。可以多次提供 `-N`，排除匹配多个模式的模式。同时给出 `-n` 和 `-N` 时，只转储至少匹配一个 `-n` 开关且不匹配任何 `-N` 开关的模式。如果未提供 `-n` 而提供了 `-N`，则从原本的常规转储中排除匹配 `-N` 的模式。

**`-o | --oids`**

将对象标识符（OID）作为各表数据的一部分转储。不建议对准备恢复到 Apache Cloudberry 的文件使用此选项。

**`-O | --no-owner`**

不输出用于将对象所有权设为与原数据库一致的命令。默认情况下，`pg_dump` 发出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 语句，设置创建的数据库对象的所有权。除非以超级用户（或脚本中所有对象的共同所有者）身份运行脚本，否则这些语句会失败。要生成任何用户都可恢复、并让该用户拥有所有对象的脚本，请指定 `-O`。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

**`-s | --schema-only`**

仅转储对象定义（模式），不转储数据。

此选项与 `--data-only` 相反。它类似于指定 `--section=pre-data --section=post-data`，但由于历史原因，两者并不完全相同。

（不要将它与 `--schema` 选项混淆，后者使用“模式”一词的另一种含义。）

如需仅排除数据库中一部分表的数据，请参阅 `--exclude-table-data`。

**`-S <username> | --superuser=<username>`**

指定禁用触发器时使用的超级用户名。仅在使用 `--disable-triggers` 时有效。最好省略此选项，直接以超级用户身份运行生成的脚本。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`-t <table> | --table=<table>`**

仅转储匹配表模式的表（或视图、序列或外表）。以 `schema.table` 格式指定表。

可以通过多次写入 `-t` 开关来选择多个表。此外，表参数会按照与 `psql` 的 `\d` 命令相同的规则解释为模式，因此也可以在模式中写入通配符来选择多个表。使用通配符时，如有需要请注意给模式加引号，防止 shell 扩展通配符。使用 `-t` 时，`-n` 和 `-N` 开关不起作用，因为无论这些开关如何，`-t` 选择的表都会被转储，且不会转储非表对象。

> **注意** 指定 `-t` 时，`pg_dump` 不会尝试转储所选表可能依赖的任何其他数据库对象。因此，无法保证特定表转储的结果能够单独成功恢复到干净数据库中。

此外，不能使用 `-t` 指定分区表的子表。要转储分区表，必须指定根分区表名。

**`-T <table> | --exclude-table=<table>`**

不转储匹配表模式的任何表。模式按与 `-t` 相同的规则解释。可以多次提供 `-T`，排除匹配多个模式的表。同时给出 `-t` 和 `-T` 时，只转储至少匹配一个 `-t` 开关且不匹配任何 `-T` 开关的表。如果未提供 `-t` 而提供了 `-T`，则从原本的常规转储中排除匹配 `-T` 的表。

**`-v | --verbose`**

指定详细模式，使 `pg_dump` 将详细的对象注释及开始／结束时间输出到转储文件，并将进度消息输出到标准错误。

**`-V | --version`**

打印 `pg_dump` 版本并退出。

**`-x | --no-privileges | --no-acl`**

不转储访问权限（`GRANT/REVOKE` 命令）。

**`-Z 0..9 | --compress=0..9`**

指定要使用的压缩级别。零表示不压缩。对于自定义归档格式，此选项指定各表数据段的压缩级别，默认以中等级别压缩。

对于纯文本输出，将压缩级别设为非零值会使整个输出文件被压缩，就像将其通过 `gzip` 处理一样；但默认不压缩。tar 归档格式目前完全不支持压缩。

**`--binary-upgrade`**

此选项供就地升级工具使用。不建议也不支持将其用于其他用途。此选项的行为可能在未来版本中更改，恕不另行通知。

**`--column-inserts | --attribute-inserts`**

使用 `INSERT` 命令转储带有显式列名的数据（`(INSERT INTO`table`(`column`, ...) VALUES ...)`）。这会使恢复非常缓慢，主要用于生成可加载到非 PostgreSQL 系数据库的转储。不过，因为此选项为每行生成独立命令，重新加载某行时出错只会丢失该行，而非整个表的内容。

**`--disable-dollar-quoting`**

此选项禁用函数体的美元引用，强制采用 SQL 标准字符串语法引用函数体。

**`--disable-triggers`**

此选项仅在创建纯数据转储时有效。它指示 `pg_dump` 加入命令，在重新加载数据期间临时禁用目标表上的触发器。如果表上有不希望在重新加载数据时调用的触发器，可使用此选项。`--disable-triggers` 输出的命令必须以超级用户身份执行。因此，还应使用 `-S` 指定超级用户名，或最好确保以超级用户身份运行生成的脚本。此选项仅对纯文本格式有意义。对于归档格式，可以在调用 [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) 时指定该选项。

> **注意** Apache Cloudberry 不支持用户定义的触发器。

**`--exclude-table-and-children=<table>`**

此选项等同于 `-T` 或 `--exclude-table`，但还会排除继承自匹配 `<table>` 名称的表的子表分区。

**`--exclude-table-data=<table>`**

不转储匹配表模式的任何表的数据。模式按与 `-t` 相同的规则解释。可以多次提供 `--exclude-table-data`，排除匹配多个模式的表。需要某个表的定义但不需要其中数据时，此选项很有用。

如需排除数据库中所有表的数据，请参阅 `--schema-only`。

**`--exclude-table-data-and-children=<table>`**

此选项等同于 `--exclude-table-data`，但还会排除继承自匹配 `<table>` 名称的表的子表分区。

**`--if-exists`**

清理数据库对象时使用条件命令（即加入 `IF EXISTS` 子句）。只有同时指定 `--clean` 时，此选项才有效。

**`--inserts`**

使用 `INSERT` 命令（而非 `COPY`）转储数据。这会使恢复非常缓慢，主要用于生成可加载到非 PostgreSQL 系数据库的转储。不过，因为此选项为每行生成独立命令，重新加载某行时出错只会丢失该行，而非整个表的内容。注意，如果重新排列过列顺序，恢复可能完全失败。`--column-inserts` 选项能适应列顺序变化，但速度更慢。

**`--lock-wait-timeout=<timeout>`**

转储开始时，不无限等待获取表上的共享锁。如果无法在指定超时时间内锁定某个表，则失败。超时时间以毫秒数指定。

**`--no-security-labels`**

不转储安全标签。

**`--no-tablespaces`**

不输出选择表空间的命令。使用此选项后，所有对象都将在恢复时的默认表空间中创建。

此选项仅对纯文本格式有意义。对于归档格式，可以在调用 `pg_restore` 时指定该选项。

**`--no-unlogged-table-data`**

不转储不记录 WAL 的表的内容。此选项不影响是否转储表定义（模式），仅阻止转储表数据。从备用服务器转储时，始终排除不记录 WAL 的表中的数据。

**`--quote-all-identifiers`**

强制为所有标识符添加引号。从 Apache Cloudberry 主版本与 `pg_dump` 不同的服务器转储数据库，或要将输出加载到不同主版本的服务器时，建议使用此选项。默认情况下，`pg_dump` 仅对其自身主版本中的保留字标识符添加引号。其他版本服务器的保留字集合可能略有不同，这有时会导致兼容性问题。使用 `--quote-all-identifiers` 可避免此类问题，但生成的转储脚本更难阅读。

**`--section=<sectionname>`**

仅转储指定部分。部分名称可以是 `pre-data`、`data` 或 `post-data`。可以多次指定此选项，选择多个部分。默认转储所有部分。

`data` 部分包含实际表数据和序列值。`post-data` 项包括索引、触发器、规则以及已验证检查约束以外的约束定义。`pre-data` 项包括所有其他数据定义项。

**`--serializable-deferrable`**

使用可串行化事务执行转储，确保所用快照与之后的数据库状态一致；但要等待事务流中不会出现异常的时点，从而避免转储失败或导致其他事务因 serialization_failure 回滚。

此选项不适用于仅用于灾难恢复的转储。如果要用转储加载数据库副本，以便在原数据库继续更新时进行报告或其他只读负载分担，此选项可能有用。不使用它时，转储可能反映出一个与最终提交事务的任何串行执行都不一致的状态。例如，如果采用批处理技术，某个批次可能在转储中显示为已关闭，但该批次中的所有项目并未出现。

如果启动 `pg_dump` 时没有活动的读写事务，此选项不会产生影响。如果存在读写事务，转储开始时间可能无限期延迟。开始运行后，使用或不使用此开关的性能相同。

> **注意** 由于 Apache Cloudberry 不支持可串行化事务，`--serializable-deferrable` 选项在 Apache Cloudberry 中无效。

**`--table-and-children=<table>`**

此选项等同于 `-t` 或 `--table`，但还会包含继承自匹配 `<table>` 名称的表的所有子表分区。

**`--use-set-session-authorization`**

输出 SQL 标准的 `SET SESSION AUTHORIZATION` 命令，代替 `ALTER OWNER` 命令来确定对象所有权。这使转储更符合标准，但根据转储中对象的历史，可能无法正确恢复。使用 `SET SESSION AUTHORIZATION` 的转储需要超级用户权限才能正确恢复，而 `ALTER OWNER` 所需的权限较低。

**`--gp-syntax | --no-gp-syntax`**

使用 `--gp-syntax` 在 `CREATE TABLE` 语句中转储 Apache Cloudberry 语法。这允许转储 Apache Cloudberry 表的分布策略（`DISTRIBUTED BY` 或 `DISTRIBUTED RANDOMLY` 子句），便于恢复到其他 Apache Cloudberry 系统。连接 Apache Cloudberry 系统时，默认包含 Apache Cloudberry 语法；连接标准 PostgreSQL 系统时，默认排除该语法。

**`--function-oids <oids>`**

转储对象标识符列表中指定的函数。

> **注意** 此选项仅供其他管理工具使用，不建议也不支持用于任何其他用途。此选项的行为可能在未来版本中更改，恕不另行通知。

**`--relation-oids <oids>`**

转储对象标识符列表中指定的关系。

> **注意** 此选项仅供其他管理工具使用，不建议也不支持用于任何其他用途。此选项的行为可能在未来版本中更改，恕不另行通知。

**`-? | --help`**

显示 `pg_dump` 命令行参数的帮助并退出。

### 连接选项 {#connection-options}

**`-d <dbname> | --dbname=<dbname>`**

指定要连接的数据库名称。这等同于在命令行中将 dbname 作为第一个非选项参数指定。

如果此参数包含 `=` 号，或以有效 URI 前缀（`postgresql://` 或 `postgres://`）开头，则将其视为 conninfo 字符串。更多信息请参阅 PostgreSQL 文档中的[连接字符串](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)。

**`-h <host> | --host=<host>`**

运行 Apache Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将读取环境变量 `PGHOST` 的值，否则默认为 localhost。

**`-p <port> | --port=<port>`**

Apache Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将读取环境变量 `PGPORT` 的值，否则默认为 5432。

**`-U <username> | --username=<username>`**

连接时使用的数据库角色名。如果未指定，将读取环境变量 `PGUSER` 的值，否则默认为当前系统角色名。

**`-W | --password`**

强制提示输入密码。

**`-w | --no-password`**

从不提示输入密码。如果服务器要求密码认证，而又无法通过 `.pgpass` 文件等其他方式获取密码，连接尝试将失败。此选项适用于无人输入密码的批处理作业和脚本。

**`--role=<rolename>`**

指定创建转储时使用的角色名。此选项使 `pg_dump` 在连接数据库后发出 `SET ROLE rolename` 命令。当认证用户（由 `-U` 指定）缺少 `pg_dump` 所需的权限，但可以切换到具有所需权限的角色时，此选项很有用。有些安装环境禁止直接以超级用户身份登录，使用此选项可以在不违反该策略的情况下创建转储。

## 注意事项 {#notes}

选择纯数据转储并使用 `--disable-triggers` 选项时，`pg_dump` 会发出命令，在插入数据前禁用用户表上的触发器，并在数据插入后发出命令重新启用它们。如果恢复中途停止，系统目录可能处于错误状态。

`pg_dump` 生成的转储文件不包含优化器用于制定查询规划决策的统计信息。因此，建议从转储文件恢复后运行 `ANALYZE`，以确保最佳性能。

`pg_dump` 的数据库活动通常由统计信息收集器收集。如果不希望这样，可以通过 `PGOPTIONS` 或 `ALTER USER` 命令将参数 `track_counts` 设为 false。

由于 `pg_dump` 可能用于向 Apache Cloudberry 的较新版本传输数据，因此可以预期 `pg_dump` 的输出能够加载到比 `pg_dump` 的版本更新的 Apache Cloudberry 版本中。`pg_dump` 也可以从比自身版本更旧的 Apache Cloudberry 版本转储。但是，`pg_dump` 不能从比自身主版本更新的 Apache Cloudberry 版本转储；它会拒绝尝试，以免生成无效转储。此外，不能保证 `pg_dump` 的输出能够加载到更旧主版本的服务器中，即使转储来自该版本的服务器也不例外。将转储文件加载到更旧服务器可能需要手动编辑转储文件，删除旧服务器不理解的语法。跨版本场景建议使用 `--quote-all-identifiers` 选项，因为它可以防止不同 Apache Cloudberry 版本保留字列表不同带来的问题。

## 示例 {#examples}

将名为 `mydb` 的数据库转储到 SQL 脚本文件：

```shell
pg_dump mydb > db.sql
```

将此类脚本重新加载到名为 `newdb` 的（新创建的）数据库中：

```shell
psql -d newdb -f db.sql
```

以 tar 文件格式转储 Apache Cloudberry，并包含分布策略信息：

```shell
pg_dump -Ft --gp-syntax mydb > db.tar
```

将数据库转储为自定义格式归档文件：

```shell
pg_dump -Fc mydb > db.dump
```

将数据库转储为目录格式归档：

```shell
pg_dump -Fd mydb -f dumpdir
```

使用 5 个工作作业并行将数据库转储为目录格式归档：

```shell
pg_dump -Fd mydb -j 5 -f dumpdir
```

将归档文件重新加载到名为 `newdb` 的（新创建的）数据库中：

```shell
pg_restore -d newdb db.dump
```

转储名为 `mytab` 的单个表：

```shell
pg_dump -t mytab mydb > db.sql
```

要在 `-t` 及相关开关中指定大写或大小写混合的名称，必须用双引号括起名称，否则名称会折叠为小写。但双引号对 shell 有特殊含义，因此还必须对其进行引用。因此，要转储一个大小写混合的表，命令应类似于：

```shell
pg_dump -t '"MixedCaseName"' mydb > mytab.sql
```

## 另请参阅 {#see-also}

[pg_dumpall](/cloudberry/reference/sys-utilities/pg-dumpall/)、[pg_restore](/cloudberry/reference/sys-utilities/pg-restore/)、[psql](/cloudberry/reference/sys-utilities/psql/)
