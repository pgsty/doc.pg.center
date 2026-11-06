---
title: "gpload"
description: "运行 YAML 格式控制文件中定义的加载作业。"
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpload.md"
---

## 概要 {#synopsis}

```shell
gpload -f <control_file> [-l <log_file>] [-h <hostname>] [-p <port>] 
   [-U <username>] [-d <database>] [-W] [--gpfdist_timeout <seconds>] 
   [--no_auto_trans] [--max_retries <retry_times>] [[-v | -V] [-q]] [-D]

gpload -? 

gpload --version
```

## 要求 {#requirements}

运行 `gpload` 的客户端机器必须满足以下条件：

- 已安装 [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) 并行文件分发程序，且该程序位于 `$PATH` 中。此程序位于 Apache Cloudberry 服务器安装目录的 `$GPHOME/bin` 中。
- 能够与 Apache Cloudberry 阵列中的所有主机（Coordinator 和 Segment）双向进行网络通信。
- 能够与存放待加载数据的主机（ETL 服务器）双向进行网络通信。

## 说明 {#description}

`gpload` 是数据加载工具，为 Apache Cloudberry 外部表并行加载功能提供接口。`gpload` 使用 YAML 格式控制文件中定义的加载规范，调用 Apache Cloudberry 并行文件服务器（[gpfdist](/cloudberry/reference/sys-utilities/gpfdist/)），根据所定义的源数据创建外部表定义，然后运行 `INSERT`、`UPDATE` 或 `MERGE` 操作，将源数据加载到数据库中的目标表。

> **注意** 如果目标表的列名是保留关键字、包含大写字母，或含有必须用引号（" "）标识该列的字符，则不支持 `MERGE` 和 `UPDATE` 操作。

此操作（包括 YAML 控制文件 `SQL` 集合中指定的所有 SQL 命令，参阅[控制文件格式](#control-file-format)）作为单个事务执行，以防止对目标表同时执行多个加载操作时出现数据不一致。

## 选项 {#options}

**`-f control_file`**

必需。包含加载规范详细信息的 YAML 文件。参阅[控制文件格式](#control-file-format)。

**`--gpfdist_timeout seconds`**

设置 `gpfdist` 并行文件分发程序发送响应的超时时间。输入 `0` 到 `30` 秒之间的值（输入“`0`”禁用超时）。注意，在流量较大的网络中可能需要增大此值。

**`-l log_file`**

指定日志文件的写入位置。默认为 `~/gpAdminLogs/gpload_YYYYMMDD`。日志文件的更多信息请参阅[日志文件格式](#log-file-format)。

**`--no_auto_trans`**

如果对目标表只执行单个加载操作，可指定 `--no_auto_trans`，禁用将加载操作作为单个事务处理的行为。

默认情况下，`gpload` 将每次加载操作作为单个事务处理，以防止对目标表同时执行多个操作时出现数据不一致。

**`-q (no screen output)`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-D (debug mode)`**

检查错误条件，但不执行加载。

**`-v (verbose mode)`**

在加载步骤执行时显示详细输出。

**`-V (very verbose mode)`**

显示非常详细的输出。

**`-? (show help)`**

显示帮助并退出。

**`--version`**

显示此工具的版本并退出。

### 连接选项 {#connection-options}

**`-d database`**

要加载到的数据库。如果未指定，将从加载控制文件或环境变量 `$PGDATABASE` 读取，否则默认为当前系统用户名。

**`-h hostname`**

指定运行 Apache Cloudberry Coordinator 数据库服务器的主机名。如果未指定，将从加载控制文件或环境变量 `$PGHOST` 读取，否则默认为 `localhost`。

**`-p port`**

指定 Apache Cloudberry Coordinator 数据库服务器监听连接的 TCP 端口。如果未指定，将从加载控制文件或环境变量 `$PGPORT` 读取，否则默认为 5432。

**`--max_retries retry_times`**

指定连接超时后 `gpload` 尝试连接 Apache Cloudberry 的最大次数。默认值为 `0`，即超时后不再尝试连接。负整数（如 `-1`）表示不限尝试次数。

**`-U username`**

连接时使用的数据库角色名。如果未指定，将从加载控制文件或环境变量 `$PGUSER` 读取，否则默认为当前系统用户名。

**`-W (force password prompt)`**

强制提示输入密码。如果未指定，将从环境变量 `$PGPASSWORD`，或由 `$PGPASSFILE` 指定的密码文件，或 `~/.pgpass` 中读取密码。如果这些均未设置，即使未提供 `-W`，`gpload` 也会提示输入密码。

## 控制文件格式 {#control-file-format}

`gpload` 控制文件采用 [YAML 1.1](http://yaml.org/spec/1.1/) 文档格式，并定义了自身的模式，用于描述 Apache Cloudberry 加载操作的各个步骤。控制文件必须是有效的 YAML 文档。

`gpload` 程序按顺序处理控制文件文档，通过缩进（空格）确定文档层级及各部分之间的关系。空白字符具有实际意义，不应仅为排版而使用空白字符，也不得使用制表符。

加载控制文件的基本结构如下：

```yml
---
VERSION: 1.0.0.1
DATABASE: <db_name>
USER: <db_username>
HOST: <coordinator_hostname>
PORT: <coordinator_port>
GPLOAD:
   INPUT:
    - SOURCE:
         LOCAL_HOSTNAME:
           - <hostname_or_ip>
         PORT: <http_port>
       | PORT_RANGE: [<start_port_range>, <end_port_range>]
         FILE: 
           - </path/to/input_file>
         SSL: true | false
         CERTIFICATES_PATH: </path/to/certificates>
    - FULLY_QUALIFIED_DOMAIN_NAME: true | false
    - COLUMNS:
           - <field_name>: <data_type>
    - TRANSFORM: '<transformation>'
    - TRANSFORM_CONFIG: '<configuration-file-path>' 
    - MAX_LINE_LENGTH: <integer> 
    - FORMAT: text | csv
    - DELIMITER: '<delimiter_character>'
    - ESCAPE: '<escape_character>' | 'OFF'
    - NEWLINE: 'LF' | 'CR' | 'CRLF'
    - NULL_AS: '<null_string>'
    - FILL_MISSING_FIELDS: true | false
    - FORCE_NOT_NULL: true | false
    - QUOTE: '<csv_quote_character>'
    - HEADER: true | false
    - ENCODING: <database_encoding>
    - ERROR_LIMIT: <integer>
    - LOG_ERRORS: true | false
   EXTERNAL:
      - SCHEMA: <schema> | '%'
   OUTPUT:
    - TABLE: <schema.table_name>
    - MODE: insert | update | merge
    - MATCH_COLUMNS:
           - <target_column_name>
    - UPDATE_COLUMNS:
           - <target_column_name>
    - UPDATE_CONDITION: '<boolean_condition>'
    - MAPPING:
              <target_column_name>: <source_column_name> | '<expression>'
   PRELOAD:
    - TRUNCATE: true | false
    - REUSE_TABLES: true | false
    - STAGING_TABLE: <external_table_name>
    - FAST_MATCH: true | false
   SQL:
    - BEFORE: "<sql_command>"
    - AFTER: "<sql_command>"
```

**`VERSION`**

可选。`gpload` 控制文件模式的版本。当前版本为 1.0.0.1。

**`DATABASE`**

可选。指定连接 Apache Cloudberry 系统中的哪个数据库。如果未指定，则使用已设置的 `$PGDATABASE`，否则默认为当前系统用户名。也可以在命令行中使用 `-d` 选项指定数据库。

**`USER`**

可选。指定连接时使用的数据库角色。如果未指定，则使用已设置的 `$PGUSER`，否则默认为当前用户。也可以在命令行中使用 `-U` 选项指定数据库角色。

如果运行 `gpload` 的用户不是 Apache Cloudberry 超级用户，必须授予该用户适当权限，才能处理加载操作。

**`HOST`**

可选。指定 Apache Cloudberry Coordinator 主机名。如果未指定，则使用已设置的 `$PGHOST`，否则默认为 localhost。也可以在命令行中使用 `-h` 选项指定 Coordinator 主机名。

**`PORT`**

可选。指定 Apache Cloudberry Coordinator 端口。如果未指定，则使用已设置的 `$PGPORT`，否则默认为 5432。也可以在命令行中使用 `-p` 选项指定 Coordinator 端口。

**`GPLOAD`**

必需。开始加载规范部分。`GPLOAD` 规范必须定义 `INPUT` 和 `OUTPUT` 部分。

**`INPUT`**

必需。定义待加载输入数据的位置和格式。`gpload` 会在当前主机上启动一个或多个 [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) 文件分发程序实例，并在 Apache Cloudberry 中创建所需的外部表定义，指向源数据。注意，所有 Apache Cloudberry 主机（Coordinator 和 Segment）都必须能通过网络访问运行 `gpload` 的主机。

**`SOURCE`**

必需。`INPUT` 规范中的 `SOURCE` 块定义源文件的位置。一个 `INPUT` 部分可以定义多个 `SOURCE` 块。每个 `SOURCE` 块对应将在本地机器上启动的一个 [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) 文件分发程序实例。每个 `SOURCE` 块必须包含 `FILE` 规范。

有关 `gpfdist` 并行文件服务器以及单个和多个 `gpfdist` 实例的使用信息，请参阅[加载数据](/cloudberry/data-loading/files/load-data-using-gpfdist/)。

**`LOCAL_HOSTNAME`**

可选。指定运行 `gpload` 的本地机器的主机名或 IP 地址。如果该机器配置了多个网络接口卡（NIC），可以指定每个 NIC 的主机名或 IP，使网络流量同时使用所有 NIC。默认仅使用本地机器的主主机名或 IP。

**`PORT`**

可选。指定 [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) 文件分发程序使用的具体端口号。也可以提供 `PORT_RANGE`，从指定范围选择可用端口。如果同时定义 `PORT` 和 `PORT_RANGE`，则 `PORT` 优先。如果两者均未定义（`PORT` 或 `PORT_RANGE`），默认在 8000 到 9000 之间选择可用端口。

如果在 `LOCAL_HOSTNAME` 中声明了多个主机名，所有主机都使用此端口号。如果希望使用所有 NIC 加载指定目录位置中的同一个文件或一组文件，此配置很合适。

**`PORT_RANGE`**

可选。可代替 `PORT`，提供端口号范围，使 `gpload` 能从中为此 [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) 文件分发程序实例选择可用端口。

**`FILE`**

必需。指定本地文件系统中包含待加载数据的文件、命名管道或目录位置。只要所有指定文件的数据格式相同，就可以声明多个文件。

如果文件使用 `gzip` 或 `bzip2` 压缩（扩展名为 `.gz` 或 `.bz2`），会自动解压（前提是路径中包含 `gunzip` 或 `bunzip2`）。

指定待加载源文件时，可以使用通配符（`*`）或其他 C 风格的模式匹配来表示多个文件。指定文件被视为相对于运行 `gpload` 时的当前目录（也可以声明绝对路径）。

**`SSL`**

可选。指定是否使用 SSL 加密。如果 `SSL` 设为 true，`gpload` 将使用 `--ssl` 选项启动 `gpfdist` 服务器，并使用 `gpfdists://` 协议。

**`CERTIFICATES_PATH`**

SSL 为 `true` 时必需；SSL 为 `false` 或未指定时不能设置。`CERTIFICATES_PATH` 指定的位置必须包含以下文件：

- 服务器证书文件 `server.crt`
- 服务器私钥文件 `server.key`
- 受信任的证书颁发机构文件 `root.crt`

不能将根目录（`/`）指定为 `CERTIFICATES_PATH`。

**`FULLY_QUALIFIED_DOMAIN_NAME`**

可选。指定 `gpload` 将主机名解析为完全限定域名（FQDN）还是本地主机名。设为 `true` 时，解析为 FQDN；设为 `false` 时，解析为本地主机名。默认值为 `false`。

某些情况下可能需要完全限定域名，例如 Apache Cloudberry 系统与 `gpload` 访问的 ETL 应用程序位于不同域中。

**`COLUMNS`**

可选。以 `field_name:data_type` 格式指定源数据文件的结构。源文件中的 `DELIMITER` 字符分隔两个数据值字段（列）。行由换行字符（`0x0a`）确定。

如果未指定输入 `COLUMNS`，则隐式使用输出 `TABLE` 的结构，即源数据的列顺序、列数和数据格式必须与目标表相同。

默认的源到目标映射根据本节定义的列名与目标 `TABLE` 中列名的匹配关系确定。可通过 `MAPPING` 部分覆盖默认映射。

**`TRANSFORM`**

可选。指定传给 `gpload` 的输入转换名称。有关 XML 转换的信息，请参阅[加载和卸载数据](/cloudberry/data-loading/files/load-data-using-gpload/)。

**`TRANSFORM_CONFIG`**

指定 `TRANSFORM` 时必需。指定上述 `TRANSFORM` 参数所指定转换的配置文件位置。

**`MAX_LINE_LENGTH`**

可选。一个整数，指定传给 `gpload` 的 XML 转换数据中一行的最大长度。

**`FORMAT`**

可选。指定源数据文件的格式：纯文本（`TEXT`）或逗号分隔值（`CSV`）。如果未指定，默认为 `TEXT`。源数据格式的更多信息请参阅[加载数据](/cloudberry/data-loading/)。

**`DELIMITER`**

可选。指定分隔每行数据中各列的单个 ASCII 字符。TEXT 模式默认为制表符，CSV 模式默认为逗号。也可以指定不可打印的 ASCII 字符或 Unicode 字符，例如 `"\x1B"` 或 `"\u001B"`。不可打印字符也支持转义字符串语法 `E'<character-code>'`。ASCII 或 Unicode 字符必须用单引号括起。例如：`E'\x1B'` 或 `E'\u001B'`。

**`ESCAPE`**

指定用于 C 转义序列（如 `\n`、`\t`、`\100` 等），以及转义可能被视为行或列分隔符的数据字符的单个字符。请确保所选转义字符未出现在实际列数据中。文本格式文件的默认转义字符是 \（反斜线），CSV 格式文件的默认转义字符是 `"`（双引号），但也可以指定其他字符。还可以将转义值设为 `'OFF'`，禁用文本格式文件中的转义。这对于文本格式的 Web 日志等数据很有用，因为其中包含大量并非用于转义的反斜线。

**`NEWLINE`**

指定数据文件中的换行符类型，取以下值之一：

- LF（换行，0x0A）
- CR（回车，0x0D）
- CRLF（回车加换行，0x0D 0x0A）。

如果未指定，Apache Cloudberry 会检查接收到的第一行数据，检测换行符类型，并采用遇到的第一个类型。

**`NULL_AS`**

可选。指定表示空值的字符串。`TEXT` 模式默认为 `\N`（反斜线加 N），`CSV` 模式默认为不带引号的空值。如果不希望区分空值与空字符串，也可以在 `TEXT` 模式中使用空字符串。与此字符串匹配的任何源数据项都会被视为空值。

**`FILL_MISSING_FIELDS`**

可选。默认值为 `false`。读取末尾字段值缺失的数据行（行尾缺少数据字段）时，Apache Cloudberry 会返回错误。

如果值为 `true`，读取末尾字段值缺失的数据行时，会将这些值设为 `NULL`。空行、具有 `NOT NULL` 约束的字段，以及行尾分隔符仍会报错。

参阅 [`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/) 命令的 `FILL MISSING FIELDS` 子句。

**`FORCE_NOT_NULL`**

可选。在 CSV 模式下，将每个指定列按带引号的值处理，因此不视为 NULL 值。对于 CSV 模式的默认空值字符串（两个分隔符之间没有内容），此选项使缺失值被解释为零长度字符串。

**`QUOTE`**

`FORMAT` 为 `CSV` 时必需。指定 `CSV` 模式的引用字符。默认为双引号（`"`）。

**`HEADER`**

可选。指定数据文件第一行为标题行（包含列名），不应作为数据加载。如果使用多个数据源文件，所有文件都必须有标题行。默认假定输入文件没有标题行。

**`ENCODING`**

可选。源数据的字符集编码。可以指定字符串常量（如 `'SQL_ASCII'`）、整数编码编号，或指定 `'DEFAULT'` 以使用默认客户端编码。如果未指定，使用默认客户端编码。

> **注意** 如果*更改*现有 `gpload` 控制文件中的 `ENCODING` 值，必须手动删除使用先前 `ENCODING` 配置创建的所有外部表。如果 `REUSE_TABLES` 设为 `true`，`gpload` 不会删除并重建外部表以使用新的 `ENCODING`。

**`ERROR_LIMIT`**

可选。为本次加载启用单行错误隔离模式。启用后，只要输入处理期间任何 Apache Cloudberry Segment 实例都未达到错误数量上限，就会丢弃格式错误的输入行。如果未达到错误上限，所有正确行都会加载，错误行则被丢弃或作为错误日志信息捕获。默认在遇到第一个错误时取消加载操作。注意，单行错误隔离仅适用于格式错误的数据行，例如属性多余或缺失、属性数据类型错误，或客户端编码序列无效。主键冲突等约束错误仍会导致取消加载操作。处理加载错误的信息请参阅[加载数据](/cloudberry/data-loading/)。

**`LOG_ERRORS`**

声明 `ERROR_LIMIT` 时可选。值为 `true` 或 `false`，默认为 `false`。值为 `true` 时，在单行错误隔离模式下运行会在内部记录格式错误的行。可以使用 Apache Cloudberry 内置 SQL 函数 `gp_read_error_log('<table_name>')` 检查格式错误。如果加载数据时检测到格式错误，`gpload` 会生成包含错误信息所在表名的警告消息，类似于以下消息。

```shell
<timestamp>|WARN|1 bad row, please use GPDB built-in function gp_read_error_log('table-name') 
    to access the detailed error row
```

如果指定 `LOG_ERRORS: true`，还必须指定 `REUSE_TABLES: true`，才能在 Apache Cloudberry 错误日志中保留格式错误。如果未指定 `REUSE_TABLES: true`，错误信息会在 `gpload` 操作结束后删除，仅返回格式错误汇总信息。可以使用 Apache Cloudberry 函数 `gp_truncate_error_log()` 删除错误日志中的格式错误。

> **注意** `gpfdist` 读取数据时，如果遇到数据格式错误，错误消息会包含指示错误位置的行号。`gpfdist` 会尝试捕获出错行。但是，对于某些格式错误，`gpfdist` 可能无法捕获准确的行。

**`EXTERNAL`**

可选。定义 `gpload` 创建的外部表数据库对象所属的模式。

默认使用 Apache Cloudberry 的 `search_path`。

:SCHEMA

声明 `EXTERNAL` 时必需。外部表的模式名称。如果模式不存在，会返回错误。

如果指定 `%`（百分号），则使用 `OUTPUT` 部分中 `TABLE` 指定表名所属的模式。如果表名未指定模式，则使用默认模式。

**`OUTPUT`**

必需。定义目标表及要加载到数据库中的最终列值。

**`TABLE`**

必需。要加载到的目标表名称。

**`MODE`**

可选。如果未指定，默认为 `INSERT`。可使用三种加载模式：

INSERT - 使用以下方法将数据加载到目标表：

```sql
INSERT INTO <target_table> SELECT * FROM <input_data>;
```

UPDATE - 当目标表中某行的 `MATCH_COLUMNS` 属性值等于输入数据中的对应值，且可选的 `UPDATE_CONDITION` 为真时，更新该行的 `UPDATE_COLUMNS`。如果目标表列名是保留关键字、包含大写字母，或含有必须用引号（" "）标识该列的字符，则不支持 `UPDATE`。

MERGE - 插入新行，并在现有行的属性值等于输入数据中的对应值且可选的 `MATCH_COLUMNS` 为真时，更新现有行的 `UPDATE_COLUMNS`。当源数据中的 `MATCH_COLUMNS` 值在目标表现有数据中没有对应值时，该行被识别为新行。此时会插入源文件中的**整行**，而非仅插入 `MATCH` 和 `UPDATE` 列。如果有多个相同的新 `MATCH_COLUMNS` 值，只会为该值插入一个新行。使用 `UPDATE_CONDITION` 筛掉应丢弃的行。如果目标表列名是保留关键字、包含大写字母，或含有必须用引号（" "）标识该列的字符，则不支持 `MERGE`。

**`MATCH_COLUMNS`**

`MODE` 为 `UPDATE` 或 `MERGE` 时必需。指定更新时用作连接条件的列。只有指定目标列中的属性值等于对应源数据列中的值，目标表中的行才会被更新。

**`UPDATE_COLUMNS`**

`MODE` 为 `UPDATE` 或 `MERGE` 时必需。指定对于满足 `MATCH_COLUMNS` 条件及可选 `UPDATE_CONDITION` 的行，要更新哪些列。

**`UPDATE_CONDITION`**

可选。指定一个布尔条件（类似于在 `WHERE` 子句中声明的条件），只有满足该条件，目标表中的行才会被更新。

**`MAPPING`**

可选。如果指定映射，它会覆盖默认的源到目标列映射。默认映射根据源 `COLUMNS` 部分定义的列名与目标 `TABLE` 的列名是否匹配来确定。映射可采用以下任一方式：

`<target_column_name>: <source_column_name>`

或者

`<target_column_name>: '<expression>'`

其中，`<expression>` 是查询 `SELECT` 列表中可以指定的任意表达式，如常量值、列引用、运算符调用、函数调用等。

**`PRELOAD`**

可选。指定加载前要运行的操作。目前唯一的预加载操作是 `TRUNCATE`。

**`TRUNCATE`**

可选。如果设为 true，`gpload` 会在加载前删除目标表中的所有行。默认为 false。

**`REUSE_TABLES`**

可选。如果设为 true，`gpload` 不会删除其创建的外部表对象和暂存表对象。这些对象将在之后使用相同加载规范的加载操作中复用。这可以提高细流加载（持续向同一目标表执行小批量加载）的性能。

如果指定 `LOG_ERRORS: true`，还必须指定 `REUSE_TABLES: true`，才能在 Apache Cloudberry 错误日志中保留格式错误。如果未指定 `REUSE_TABLES: true`，格式错误信息会在 `gpload` 操作结束后删除。

如果 `<external_table_name>` 存在，工具会使用现有表。如果表结构与 `OUTPUT` 表结构不匹配，工具会返回错误。

**`STAGING_TABLE`**

可选。指定 `gpload` 操作期间创建的临时外部表名称。该外部表供 `gpfdist` 使用。还必须指定 `REUSE_TABLES: true`。如果 `REUSE_TABLES` 为 false 或未指定，将忽略 `STAGING_TABLE`。默认情况下，`gpload` 创建一个名称随机生成的临时外部表。

如果 external_table_name 包含句点（.），`gpload` 会返回错误。如果表已存在，工具会使用该表；如果现有表结构与 `OUTPUT` 表结构不匹配，则返回错误。

工具使用 `EXTERNAL` 部分中 `SCHEMA` 的值作为 `<external_table_name>` 所属的模式。如果 `SCHEMA` 值为 `%`，则 `<external_table_name>` 与目标表使用相同模式，即 `OUTPUT` 部分中 `TABLE` 所属的模式。

如果未设置 `SCHEMA`，工具会在数据库 `search_path` 中的模式里搜索该表。如果未找到，则在默认 `PUBLIC` 模式中创建 `external_table_name`。

`gpload` 创建暂存表时，采用目标表的分布键作为暂存表的分布键。如果目标表以 `DISTRIBUTED RANDOMLY` 方式创建，`gpload` 使用 `MATCH_COLUMNS` 作为暂存表的分布键。

**`FAST_MATCH`**

可选。如果设为 true，`gpload` 在复用外部表时，仅在数据库中搜索匹配的外部表对象，不检查目录表 `pg_attribute` 中外部表的列名和列类型是否可用于 `gpload` 操作。当复用外部表对象且数据库目录表 `pg_attribute` 包含大量行时，将此值设为 true 可提高 `gpload` 性能。如果列定义不兼容，工具会返回错误并退出。

默认值为 false，即检查外部表定义的列名和列类型。

还必须指定 `REUSE_TABLES: true`。如果 `REUSE_TABLES` 为 false 或未指定，却指定了 `FAST_MATCH: true`，`gpload` 会返回警告消息。

**`SQL`**

可选。定义加载前和／或加载后运行的 SQL 命令。可以指定多个 `BEFORE` 和／或 `AFTER` 命令，按所需执行顺序列出。

**`BEFORE`**

可选。加载操作开始前运行的 SQL 命令。请用引号括起命令。

**`AFTER`**

可选。加载操作完成后运行的 SQL 命令。请用引号括起命令。

## 日志文件格式 {#log-file-format}

`gpload` 输出的日志文件采用以下格式：

```shell
<timestamp>|<level>|<message>
```

其中，`<timestamp>` 的格式为 `YYYY-MM-DD HH:MM:SS`，level 为 `DEBUG`、`LOG`、`INFO` 或 `ERROR` 之一，message 为普通文本消息。

日志文件中一些可能有用的 `INFO` 消息如下（其中 \# 对应实际秒数、数据单位数或失败行数）：

```shell
INFO|running time: <#.##> seconds
INFO|transferred <#.#> kB of <#.#> kB.
INFO|gpload succeeded
INFO|gpload succeeded with warnings
INFO|gpload failed
INFO|1 bad row
INFO|<#> bad rows
```

## 注意事项 {#notes}

如果数据库对象名使用双引号标识符（定界标识符）创建，必须在 `gpload` 控制文件中用单引号括起该定界名称。例如，如果按以下方式创建表：

```sql
CREATE TABLE "MyTable" ("MyColumn" text);
```

YAML 格式的 `gpload` 控制文件应按以下方式引用上述表名和列名：

```shell
- COLUMNS:
   - '"MyColumn"': text
OUTPUT:
   - TABLE: public.'"MyTable"'
```

## 示例 {#examples}

运行 `my_load.yml` 中定义的加载作业：

```shell
gpload -f my_load.yml
```

加载控制文件示例：

```yml
---
VERSION: 1.0.0.1
DATABASE: ops
USER: gpadmin
HOST: cdw-1
PORT: 5432
GPLOAD:
   INPUT:
    - SOURCE:
         LOCAL_HOSTNAME:
           - etl1-1
           - etl1-2
           - etl1-3
           - etl1-4
         PORT: 8081
         FILE: 
           - /var/load/data/*
    - COLUMNS:
           - name: text
           - amount: float4
           - category: text
           - descr: text
           - date: date
    - FORMAT: text
    - DELIMITER: '|'
    - ERROR_LIMIT: 25
    - LOG_ERRORS: true
   OUTPUT:
    - TABLE: payables.expenses
    - MODE: INSERT
   PRELOAD:
    - REUSE_TABLES: true 
   SQL:
   - BEFORE: "INSERT INTO audit VALUES('start', current_timestamp)"
   - AFTER: "INSERT INTO audit VALUES('end', current_timestamp)"
```

## 另请参阅 {#see-also}

[gpfdist](/cloudberry/reference/sys-utilities/gpfdist/), [`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/)
