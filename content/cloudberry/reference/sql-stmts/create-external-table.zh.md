---
title: "CREATE EXTERNAL TABLE"
description: "定义新的外部表。"
weight: 600
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-external-table.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [READABLE] EXTERNAL [TEMPORARY | TEMP] TABLE <table_name>     
    ( <column_name> <data_type> [, ...] | LIKE <other_table >)
     LOCATION ('file://<seghost>[:<port>]/<path>/<file>' [, ...])
       | ('gpfdist://<filehost>[:<port>]/<file_pattern>[#transform=<trans_name>]'
           [, ...]
       | ('gpfdists://<filehost>[:<port>]/<file_pattern>[#transform=<trans_name>]'
           [, ...])
       | ('pxf://<path-to-data>?PROFILE=<profile_name>[&SERVER=<server_name>][&<custom-option>=<value>[...]]'))
       | ('s3://<S3_endpoint>[:<port>]/<bucket_name>/[<S3_prefix>] [region=<S3-region>] [config=<config_file> | config_server=<url>]')
     [ON COORDINATOR]
     FORMAT 'TEXT' 
           [( [HEADER]
              [DELIMITER [AS] '<delimiter>' | 'OFF']
              [NULL [AS] '<null string>']
              [ESCAPE [AS] '<escape>' | 'OFF']
              [NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF']
              [FILL MISSING FIELDS] )]
          | 'CSV'
           [( [HEADER]
              [QUOTE [AS] '<quote>'] 
              [DELIMITER [AS] '<delimiter>']
              [NULL [AS] '<null string>']
              [FORCE NOT NULL <column> [, ...]]
              [ESCAPE [AS] '<escape>']
              [NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF']
              [FILL MISSING FIELDS] )]
          | 'CUSTOM' (Formatter=<<formatter_specifications>>)
    [ OPTIONS ( <key> '<value>' [, ...] ) ]
    [ ENCODING '<encoding>' ]
      [ [LOG ERRORS [PERSISTENTLY]] SEGMENT REJECT LIMIT <count>
      [ROWS | PERCENT] ]

CREATE [READABLE] EXTERNAL WEB [TEMPORARY | TEMP] TABLE <table_name>     
   ( <column_name> <data_type> [, ...] | LIKE <other_table >)
      LOCATION ('http://<webhost>[:<port>]/<path>/<file>' [, ...])
    | EXECUTE '<command>' [ON ALL 
                          | COORDINATOR
                          | <number_of_segments>
                          | HOST ['<segment_hostname>'] 
                          | SEGMENT <segment_id> ]
      FORMAT 'TEXT' 
            [( [HEADER]
               [DELIMITER [AS] '<delimiter>' | 'OFF']
               [NULL [AS] '<null string>']
               [ESCAPE [AS] '<escape>' | 'OFF']
               [NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF']
               [FILL MISSING FIELDS] )]
           | 'CSV'
            [( [HEADER]
               [QUOTE [AS] '<quote>'] 
               [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [FORCE NOT NULL <column> [, ...]]
               [ESCAPE [AS] '<escape>']
               [NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF']
               [FILL MISSING FIELDS] )]
           | 'CUSTOM' (Formatter=<<formatter specifications>>)
     [ OPTIONS ( <key> '<value>' [, ...] ) ]
     [ ENCODING '<encoding>' ]
     [ [LOG ERRORS [PERSISTENTLY]] SEGMENT REJECT LIMIT <count>
       [ROWS | PERCENT] ]

CREATE WRITABLE EXTERNAL [TEMPORARY | TEMP] TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table >)
     LOCATION('gpfdist://<outputhost>[:<port>]/<filename>[#transform=<trans_name>]'
          [, ...])
      | ('gpfdists://<outputhost>[:<port>]/<file_pattern>[#transform=<trans_name>]'
          [, ...])
      FORMAT 'TEXT' 
               [( [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [ESCAPE [AS] '<escape>' | 'OFF'] )]
          | 'CSV'
               [([QUOTE [AS] '<quote>'] 
               [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [FORCE QUOTE <column> [, ...]] | * ]
               [ESCAPE [AS] '<escape>'] )]

           | 'CUSTOM' (Formatter=<<formatter specifications>>)
    [ OPTIONS ( <key> '<value>' [, ...] ) ]
    [ ENCODING '<write_encoding>' ]
    [ DISTRIBUTED BY ({<column> [<opclass>]}, [ ... ] ) | DISTRIBUTED RANDOMLY ]

CREATE WRITABLE EXTERNAL [TEMPORARY | TEMP] TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table >)
     LOCATION('s3://<S3_endpoint>[:<port>]/<bucket_name>/[<S3_prefix>] [region=<S3-region>] [config=<config_file> | config_server=<url>]')
      [ON COORDINATOR]
      FORMAT 'TEXT' 
               [( [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [ESCAPE [AS] '<escape>' | 'OFF'] )]
          | 'CSV'
               [([QUOTE [AS] '<quote>'] 
               [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [FORCE QUOTE <column> [, ...]] | * ]
               [ESCAPE [AS] '<escape>'] )]

CREATE WRITABLE EXTERNAL WEB [TEMPORARY | TEMP] TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
    EXECUTE '<command>' [ON ALL]
    FORMAT 'TEXT' 
               [( [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [ESCAPE [AS] '<escape>' | 'OFF'] )]
          | 'CSV'
               [([QUOTE [AS] '<quote>'] 
               [DELIMITER [AS] '<delimiter>']
               [NULL [AS] '<null string>']
               [FORCE QUOTE <column> [, ...]] | * ]
               [ESCAPE [AS] '<escape>'] )]
           | 'CUSTOM' (Formatter=<<formatter specifications>>)
    [ OPTIONS ( <key> '<value>' [, ...] ) ]
    [ ENCODING '<write_encoding>' ]
    [ DISTRIBUTED BY ({<column> [<opclass>]}, [ ... ] ) | DISTRIBUTED RANDOMLY ]
```

## 说明 {#description}

`CREATE EXTERNAL TABLE` 或 `CREATE EXTERNAL WEB TABLE` 在 Apache Cloudberry 中创建新的可读外部表定义。可读外部表通常用于快速并行加载数据。定义外部表后，可以使用 SQL 命令直接（并行）查询其中的数据。例如，可以选择、连接或排序外部表数据，也可以为外部表创建视图。可读外部表不允许 DML 操作（`UPDATE`、`INSERT`、`DELETE` 或 `TRUNCATE`），也不能在可读外部表上创建索引。

`CREATE WRITABLE EXTERNAL TABLE` 或 `CREATE WRITABLE EXTERNAL WEB TABLE` 在 Apache Cloudberry 中创建新的可写外部表定义。可写外部表通常用于将数据库中的数据卸载到一组文件或命名管道中。可写外部 Web 表还可以将数据输出到可执行程序。定义可写外部表后，可以从数据库表中选择数据并将其插入可写外部表。可写外部表只允许 `INSERT` 操作，不允许 `SELECT`、`UPDATE`、`DELETE` 或 `TRUNCATE`。

普通外部表与外部 Web 表的主要区别在于数据源。普通可读外部表访问静态平面文件，而外部 Web 表访问动态数据源，即 Web 服务器上的数据，或通过运行操作系统命令或脚本产生的数据。

## 参数 {#parameters}

**`READABLE | WRITABLE`**

指定外部表的类型，默认是可读。可读外部表用于将数据加载到 Apache Cloudberry；可写外部表用于卸载数据。

**`WEB`**

在 Apache Cloudberry 中创建可读或可写外部 Web 表定义。可读外部 Web 表有两种形式：通过 `http://` 协议访问文件，或通过运行操作系统命令访问数据。可写外部 Web 表将数据输出到可以接受数据输入流的可执行程序。查询执行期间不会重新扫描外部 Web 表。

`s3` 协议不支持外部 Web 表。不过，可以创建一个运行第三方工具、直接从 S3 读取数据或向 S3 写入数据的外部 Web 表。

**`TEMPORARY | TEMP`**

如果指定，则在 Apache Cloudberry 中创建临时可读或可写外部表定义。临时外部表位于特殊模式中；创建表时不能指定模式名。会话结束时会自动删除临时外部表。

临时表存在期间，同名的永久表对当前会话不可见，除非使用模式限定名称引用永久表。

**`table_name`**

新外部表的名称。

**`column_name`**

要在外部表定义中创建的列名称。与普通表不同，外部表没有列约束或默认值，因此不要指定这些内容。

LIKE other_table
`LIKE` 子句指定一个表，新外部表会自动从该表复制所有列名、数据类型和 Cloudberry 分布策略。如果原表指定了列约束或默认列值，这些内容不会复制到新的外部表定义中。

**`data_type`**

列的数据类型。

**`LOCATION ('protocol://[host[:port]]/path/file' [, ...])`**

如果使用 `pxf` 协议访问外部数据源，请参见 pxf:// 协议 了解 `pxf` 协议。

对于可读外部表，指定用于填充外部表或 Web 表的外部数据源 URI。普通可读外部表允许使用 `gpfdist` 或 `file` 协议；外部 Web 表允许使用 `http` 协议。如果省略 `port`，则 `http` 和 `gpfdist` 协议默认使用端口 `8080`。使用 `gpfdist` 协议时，`path` 相对于 `gpfdist` 提供文件服务的目录（即启动 `gpfdist` 程序时指定的目录）。此外，`gpfdist` 可以使用通配符或其他 C 风格的模式匹配（例如，用 `[[:space:]]` 表示空白字符）表示目录中的多个文件。例如：

```
'gpfdist://filehost:8081/*'
'gpfdist://coordinatorhost/my_load_file'
'file://seghost1/dbfast1/external/myfile.txt'
'http://intranet.example.com/finance/expenses.csv'
```

对于可写外部表，指定收集 Cloudberry Segment 输出数据并将其写入一个或多个命名文件的 `gpfdist` 进程或 S3 协议的位置 URI。对 `gpfdist` 而言，`path` 相对于 `gpfdist` 提供文件服务的目录（即启动 `gpfdist` 程序时指定的目录）。如果列出多个 `gpfdist` 位置，发送数据的 Segment 会在可用输出位置之间平均分配。例如：

```
'gpfdist://outputhost:8081/data1.out',
'gpfdist://outputhost:8081/data2.out'
```

如上例列出两个 `gpfdist` 位置时，一半 Segment 会将输出数据发送到 `data1.out` 文件，另一半发送到 `data2.out` 文件。

使用 `#transform=trans_name` 选项，可以指定加载或提取数据时要应用的转换。trans_name 是 YAML 配置文件中转换的名称，该文件由运行 `gpfdist` 工具时指定。

**`ON COORDINATOR`**

将所有与表有关的操作限制在 Apache Cloudberry Coordinator Segment 上。只允许对使用 `s3` 或自定义协议创建的可读和可写外部表使用。`gpfdist`、`gpfdists`、`pxf` 和 `file` 协议不支持 `ON COORDINATOR`。

> **注意** 请注意，使用 `ON COORDINATOR` 子句读取或写入外部表可能产生资源影响。如果将表操作完全限制在 Apache Cloudberry Coordinator Segment 上，可能会遇到性能问题。

**`EXECUTE 'command' [ON ...]`**

仅适用于可读外部 Web 表或可写外部表。对于可读外部 Web 表，指定由 Segment 实例运行的操作系统命令。命令可以是单个操作系统命令或脚本。`ON` 子句用于指定运行该命令的 Segment 实例。

- `ON ALL` 是默认值。Apache Cloudberry 系统中所有 Segment 主机上的每个活动（主）Segment 实例都会运行该命令。如果命令运行脚本，该脚本必须位于所有 Segment 主机上的相同位置，并且可由 Cloudberry 超级用户（`gpadmin`）执行。
- `ON COORDINATOR` 只在 Coordinator 主机上运行命令。

    > **注意** 指定 `ON COORDINATOR` 子句时，外部 Web 表不支持日志记录。

- `ON number` 表示由指定数量的 Segment 运行命令。具体 Segment 由 Apache Cloudberry 系统在运行时随机选择。如果命令运行脚本，该脚本必须位于所有 Segment 主机上的相同位置，并且可由 Cloudberry 超级用户（`gpadmin`）执行。
- `HOST` 表示每台 Segment 主机上由一个 Segment 运行命令（每台主机运行一次），与每台主机上的活动 Segment 实例数量无关。
- `HOST segment_hostname` 表示由指定 Segment 主机上的所有活动（主）Segment 实例运行命令。
- `SEGMENT segment_id` 表示只由指定 Segment 运行一次命令。可以查看系统目录表 gp_segment_configuration 中的 content number 来确定 Segment 实例的 ID。Apache Cloudberry Coordinator 的 content ID 始终为 `-1`。

对于可写外部表，`EXECUTE` 子句中指定的命令必须准备好接收通过管道传入的数据。由于所有有数据要发送的 Segment 都会将输出写入指定命令或程序，因此 `ON` 子句唯一可用的选项是 `ON ALL`。

**`FORMAT 'TEXT | CSV' (options)`**

当 `FORMAT` 子句指定分隔文本（`TEXT`）或逗号分隔值（`CSV`）格式时，格式化选项与 PostgreSQL [COPY](/cloudberry/reference/sql-stmts/copy/) 命令提供的选项类似。如果文件中的数据没有使用默认列分隔符、转义字符、空值字符串等，就必须指定额外的格式化选项，以便 Apache Cloudberry 正确读取外部文件中的数据。

如果使用 `pxf` 协议访问外部数据源，请参见 “使用 PXF 访问外部数据” 了解 PXF 的用法。

**`FORMAT 'CUSTOM' (formatter=formatter_specification)`**

指定自定义数据格式。formatter_specification 指定用于格式化数据的函数，后面跟着传给该格式化函数的逗号分隔参数。格式化程序说明的长度（包括 `Formatter=` 的字符串）最多约为 50K 字节。

如果使用 `pxf` 协议访问外部数据源，请参见 “使用 PXF 访问外部数据” 了解 PXF 的用法。

**`DELIMITER`**

指定用于分隔每行（记录）数据中各列的单个 ASCII 字符。默认值在 `TEXT` 模式下是制表符，在 `CSV` 模式下是逗号。对可读外部表使用 `TEXT` 模式时，可以将分隔符设为 `OFF`，用于将非结构化数据加载到单列表等特殊场景。

对 `s3` 协议，分隔符不能是换行字符（`\n`）或回车字符（`\r`）。

**`NULL`**

指定表示 `NULL` 值的字符串。在 `TEXT` 模式下默认是 `\N`（反斜杠-N），在 `CSV` 模式下默认是没有引号的空值。即使在 `TEXT` 模式下，也可以选择空字符串，以便不区分 `NULL` 值和空字符串。使用外部表和 Web 表时，任何与该字符串匹配的数据项都会被视为 `NULL` 值。

以 `text` 格式为例，可以使用此 `FORMAT` 子句指定两个单引号组成的字符串（`''`）为 `NULL` 值。

```sql
FORMAT 'text' (delimiter ',' null '\'\'\'\'' )
```

**`ESCAPE`**

指定用于 C 转义序列（例如 `\n`、`\t`、`\100` 等）以及转义原本可能被视为行或列分隔符的数据字符的单个字符。应选择实际列数据中不会出现的转义字符。文本格式文件的默认转义字符是 `\`（反斜杠），csv 格式文件的默认转义字符是 `"`（双引号），但也可以指定其他字符作为转义字符。还可以在文本格式文件中将转义值指定为 `'OFF'` 来停用转义。这对文本格式的 Web 日志数据很有用，因为其中包含许多并非转义用途的反斜杠。

**`NEWLINE`**

指定数据文件中使用的换行符：`LF`（换行，0x0A）、`CR`（回车，0x0D）或 `CRLF`（回车加换行，0x0D 0x0A）。如果未指定，Apache Cloudberry Segment 会查看接收到的数据第一行，使用遇到的第一种换行类型来检测换行符类型。

**`HEADER`**

对于可读外部表，指定数据文件的第一行是标题行（包含表列名称），不应作为表数据包含。如果使用多个数据源文件，所有文件都必须有标题行。

对于 `s3` 协议，标题行中的列名不能包含换行字符（`\n`）或回车字符（`\r`）。

`pxf` 协议不支持 `HEADER` 格式化选项。

**`QUOTE`**

指定 `CSV` 模式的引用字符。默认值是双引号（`"`）。

**`FORCE NOT NULL`**

在 `CSV` 模式下，将每个指定列按带引号处理，因此不视为 `NULL` 值。对于 `CSV` 模式的默认空值字符串（两个分隔符之间没有内容），这会使缺失值按零长度字符串处理。

**`FORCE QUOTE`**

在可写外部表的 `CSV` 模式下，强制为每个指定列的所有非 `NULL` 值加引号。如果指定 `*`，则所有列的非 `NULL` 值都会加引号。`NULL` 输出从不加引号。

**`FILL MISSING FIELDS`**

对于可读外部表的 `TEXT` 和 `CSV` 模式，指定 `FILL MISSING FIELDS` 后，如果一行数据在行末缺少数据字段，就会将缺失的尾部字段值设为 `NULL`（而不是报告错误）。空行、带 `NOT NULL` 约束的字段以及行尾分隔符仍会报告错误。

**`OPTIONS key 'value'[, key' value' ...]`**

可选。以键值对形式指定参数和值；将协议作为外部表的外部表协议使用时，这些键值对会传给自定义数据访问协议。自定义数据访问协议负责处理和验证键值对。

**`ENCODING 'encoding'`**

外部表使用的字符集编码。指定字符串常量（例如 `'SQL_ASCII'`）、整数编码编号，或指定 `DEFAULT` 使用服务器默认编码。参见 “字符集支持”。

**`LOG ERRORS [PERSISTENTLY]`**

可选子句，可以放在 `SEGMENT REJECT LIMIT` 子句之前，用于记录格式错误行的信息。错误日志数据在内部存储。如果指定外部表已有错误日志数据，新数据会追加到现有错误日志数据中。错误日志数据不会复制到镜像 Segment。

除非指定关键字 `PERSISTENTLY`，否则删除外部表时会删除错误日志数据。如果指定该关键字，删除外部表后日志数据仍会保留。

使用 Apache Cloudberry 内置 SQL 函数 `gp_read_error_log()` 访问错误日志数据；如果指定了 `PERSISTENTLY` 关键字，则使用 SQL 函数 `gp_read_persistent_error_log()`。

如果使用 `PERSISTENTLY` 关键字，必须安装管理持久错误日志信息的函数。

有关错误日志信息及用于查看和管理错误日志信息的内置函数，参见[注意事项](#notes)。

**`SEGMENT REJECT LIMIT count [ROWS | PERCENT]`**

以单行错误隔离模式运行 `COPY FROM` 操作。如果输入行存在格式错误，只要加载期间任何 Cloudberry Segment 实例都没有达到拒绝限制 count，就会丢弃这些行。拒绝限制 count 可以指定为行数（默认）或总行数的百分比（1-100）。如果使用 `PERCENT`，每个 Segment 只有在处理完参数 `gp_reject_percent_threshold` 指定的行数后才开始计算坏行百分比。`gp_reject_percent_threshold` 的默认值为 300 行。违反 `NOT NULL`、`CHECK` 或 `UNIQUE` 约束等约束错误仍会按“全有或全无”输入模式处理。如果未达到限制，所有正确行都会加载，错误行会被丢弃。

> **注意** 读取外部表时，如果没有先触发 `SEGMENT REJECT LIMIT` 或未指定该限制，Apache Cloudberry 会限制最初可包含格式错误的行数。如果前 1000 行都被拒绝，`COPY` 操作会停止并回滚。

可以使用 Apache Cloudberry 服务器配置参数 `gp_initial_bad_row_limit` 更改最初被拒绝行数的限制。

**`DISTRIBUTED BY ({column [opclass]}, [ ... ] )`**

**`DISTRIBUTED RANDOMLY`**

用于声明可写外部表的 Apache Cloudberry 分布策略。默认情况下，可写外部表采用随机分布。如果导出数据的源表使用哈希分布策略，为可写外部表定义相同的分布键列和操作符类 `oplcass`，就可以避免通过 Interconnect 移动行，从而提高卸载性能。当发出 `INSERT INTO wex_table SELECT * FROM source_table` 等卸载命令时，如果两个表具有相同的哈希分布策略，要卸载的行就可以直接从 Segment 发送到输出位置。

## 示例 {#examples}

在后台以端口 `8081` 启动 `gpfdist` 文件服务器程序，为目录 `/var/data/staging` 提供文件服务：

```sql
gpfdist -p 8081 -d /var/data/staging -l /home/<gpadmin>/log &
```

使用 `gpfdist` 协议和 `gpfdist` 目录中找到的任意文本格式文件（`*.txt`）创建名为 `ext_customer` 的可读外部表。文件使用竖线（`|`）作为列分隔符，使用空格作为 `NULL`。同时以单行错误隔离模式访问外部表：

```sql
CREATE EXTERNAL TABLE ext_customer
   (id int, name text, sponsor text) 
   LOCATION ( 'gpfdist://filehost:8081/*.txt' ) 
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ')
   LOG ERRORS SEGMENT REJECT LIMIT 5;
```

创建与上面相同的可读外部表定义，但使用 CSV 格式文件：

```sql
CREATE EXTERNAL TABLE ext_customer 
   (id int, name text, sponsor text) 
   LOCATION ( 'gpfdist://filehost:8081/*.csv' ) 
   FORMAT 'CSV' ( DELIMITER ',' );
```

使用 `file` 协议和多个带标题行的 CSV 格式文件，创建名为 `ext_expenses` 的可读外部表：

```sql
CREATE EXTERNAL TABLE ext_expenses (name text, date date, 
amount float4, category text, description text) 
LOCATION ( 
'file://seghost1/dbfast/external/expenses1.csv',
'file://seghost1/dbfast/external/expenses2.csv',
'file://seghost2/dbfast/external/expenses3.csv',
'file://seghost2/dbfast/external/expenses4.csv',
'file://seghost3/dbfast/external/expenses5.csv',
'file://seghost3/dbfast/external/expenses6.csv' 
)
FORMAT 'CSV' ( HEADER );
```

创建一个可读外部 Web 表，使其在每台 Segment 主机上运行一次脚本：

```sql
CREATE EXTERNAL WEB TABLE log_output (linenum int, message 
text)  EXECUTE '/var/load_scripts/get_log_data.sh' ON HOST 
 FORMAT 'TEXT' (DELIMITER '|');
```

创建名为 `sales_out` 的可写外部表，使用 `gpfdist` 将输出数据写入名为 `sales.out` 的文件。文件使用竖线（`|`）作为列分隔符，使用空格作为 `NULL`。

```sql
CREATE WRITABLE EXTERNAL TABLE sales_out (LIKE sales) 
   LOCATION ('gpfdist://etl1:8081/sales.out')
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ')
   DISTRIBUTED BY (txn_id);
```

创建一个可写外部 Web 表，将 Segment 接收的输出数据通过管道传给名为 `to_adreport_etl.sh` 的可执行脚本：

```sql
CREATE WRITABLE EXTERNAL WEB TABLE campaign_out 
(LIKE campaign) 
 EXECUTE '/var/unload_scripts/to_adreport_etl.sh'
 FORMAT 'TEXT' (DELIMITER '|');
```

使用上面定义的可写外部表卸载选定数据：

```sql
INSERT INTO campaign_out SELECT * FROM campaign WHERE customer_id=123;
```

## 注意事项 {#notes}

指定 `LOG ERRORS` 子句时，Apache Cloudberry 会捕获读取外部表数据时发生的错误。

可以查看和管理捕获的错误日志数据。管理日志数据所用的函数取决于数据是否持久化（即 `LOG ERRORS` 子句是否使用 `PERSISTENTLY` 关键字）。

- 管理未使用 `PERSISTENTLY` 关键字定义的外部表中的非持久错误日志数据的函数。
- 内置 SQL 函数 `gp_read_error_log('table_name')` 显示外部表的错误日志信息。本例显示外部表 `ext_expenses` 的错误日志数据。

    ```sql
    SELECT * from gp_read_error_log('ext_expenses');
    ```

    如果使用 `LOG ERRORS PERSISTENTLY` 子句创建外部表，或外部表不存在，该函数不会返回数据。

- 内置 SQL 函数 `gp_truncate_error_log('table_name')` 删除 table_name 的错误日志数据。本例删除从外部表 `ext_expenses` 捕获的错误日志数据：

    ```sql
    SELECT gp_truncate_error_log('ext_expenses'); 
    ```

    删除表也会删除表的日志数据。如果外部表使用 `LOG ERRORS PERSISTENTLY` 子句定义，该函数不会截断日志数据。

    如果表不存在，该函数返回 `FALSE`。

- 管理使用 `PERSISTENTLY` 关键字定义的外部表中的持久错误日志数据的函数。
- SQL 函数 `gp_read_persistent_error_log('table_name')` 显示外部表的持久日志数据。

    如果使用未包含 `PERSISTENTLY` 关键字的方式创建外部表，该函数不会返回数据。即使外部表已删除，该函数也会返回其持久日志数据。

- SQL 函数 `gp_truncate_persistent_error_log('table_name')` 截断表的持久日志数据。

    对于持久日志数据，必须手动删除数据。删除外部表不会删除持久日志数据。

- 以下事项适用于非持久和持久错误日志数据及相关函数。
- `gp_read_*` 函数要求对表具有 `SELECT` 权限。
- `gp_truncate_*` 函数要求拥有表的所有者权限。
- 可以使用通配符 `*` 删除当前数据库中现有表的错误日志信息。指定字符串 `*.*` 可删除所有数据库错误日志信息，包括因先前数据库问题而未删除的错误日志信息。指定 `*` 时需要数据库所有者权限。指定 `*.*` 时需要操作系统超级用户权限。非持久和持久错误日志数据必须分别使用对应的 `gp_truncate_*` 函数删除。

当多个 Apache Cloudberry 外部表使用 `gpfdist`、`gpfdists` 或 `file` 协议并访问 Linux 系统中的同一个命名管道时，Apache Cloudberry 会将命名管道的访问限制为单个读取者。如果第二个读取者尝试访问该命名管道，就会返回错误。

## 兼容性 {#compatibility}

`CREATE EXTERNAL TABLE` 是 Apache Cloudberry 的扩展。SQL 标准没有关于外部表的规定。

## 另请参阅 {#see-also}

[CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/), [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/), [COPY](/cloudberry/reference/sql-stmts/copy/), [SELECT INTO](/cloudberry/reference/sql-stmts/select-into/), [INSERT](/cloudberry/reference/sql-stmts/insert/)
