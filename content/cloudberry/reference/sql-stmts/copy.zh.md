---
title: "COPY"
description: "在文件和表之间复制数据。"
weight: 510
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/copy.md"
---

## 概要 {#synopsis}

```sql
COPY <table_name> [(<column_name> [, ...])] 
     FROM {'<filename>' | PROGRAM '<command>' | STDIN}
     [ [ WITH ] ( <option> [, ...] ) ]
     [ ON SEGMENT ]

COPY { <table_name> [(<column_name> [, ...])] | (<query>)} 
     TO {'<filename>' | PROGRAM '<command>' | STDOUT}
     [ [ WITH ] ( <option> [, ...] ) ]
     [ ON SEGMENT ]

-- where option can be one of:

FORMAT <format_name>
OIDS [ <boolean> ]
FREEZE [ <boolean> ]
DELIMITER '<delimiter_character>'
NULL '<null string>'
HEADER [ <boolean> ]
QUOTE '<quote_character>'
ESCAPE '<escape_character>'
FORCE_QUOTE { ( <column_name> [, ...] ) | * }
FORCE_NOT_NULL ( <column_name> [, ...] ) 
FORCE_NULL ( <column_name> [, ...] )
ENCODING '<encoding_name>'       
FILL MISSING FIELDS
LOG ERRORS [ SEGMENT REJECT LIMIT <count> [ ROWS | PERCENT ] ]
IGNORE EXTERNAL PARTITIONS
```

## 描述 {#description}

`COPY` 在 Apache Cloudberry 表与标准文件系统文件之间移动数据。`COPY TO` 将表的内容复制到一个文件（如果使用 `ON SEGMENT` 进行复制，则按 Segment ID 复制到多个文件），而 `COPY FROM` 将文件中的数据复制到表中（把数据追加到表中已有内容之后）。`COPY TO` 还可以复制 `SELECT` 查询的结果。

如果指定了列列表，`COPY` 只会在文件与指定列之间复制这些列的数据。如果表中有未出现在列列表中的列，`COPY FROM` 会为这些列插入默认值。

带文件名的 `COPY` 会指示 Apache Cloudberry Coordinator 主机直接读取或写入文件。该文件必须可由 Coordinator 主机访问，并且文件名必须从 Coordinator 主机的角度指定。

当 `COPY` 与 `ON SEGMENT` 子句一起使用时，`COPY TO` 会使各 Segment 创建各自的、面向 Segment 的文件，这些文件保留在 Segment 主机上。`ON SEGMENT` 的文件名参数接受字符串字面量 `<SEGID>`（必需），并使用绝对路径或字符串字面量 `<SEG_DATA_DIR>`。运行 `COPY` 操作时，Segment ID 和 Segment 数据目录的路径会替换这些字符串字面量值。

以复制表（`DISTRIBUTED REPLICATED`）作为源执行 `COPY TO` 时，会创建一个包含来自单个 Segment 的行的文件，因此目标文件不包含重复行。以复制表作为源并使用 `ON SEGMENT` 子句执行 `COPY TO` 时，会在 Segment 主机上创建包含该表所有行的目标文件。

`ON SEGMENT` 子句允许你把表数据复制到 Segment 主机上的文件中，用于在集群之间迁移数据或执行备份等操作。由 `ON SEGMENT` 子句创建的 Segment 数据可以通过 `gpfdist` 等工具恢复，这对高速数据加载很有用。

> **注意** 仅建议专家用户使用 `ON SEGMENT` 子句。

指定 `PROGRAM` 时，服务器会运行给定的命令，并从该程序的标准输出读取数据，或向该程序的标准输入写入数据。命令必须从服务器的角度指定，并且可由 `gpadmin` 用户执行。

指定 `STDIN` 或 `STDOUT` 时，数据通过客户端与 Coordinator 之间的连接传输。`STDIN` 和 `STDOUT` 不能与 `ON SEGMENT` 子句一起使用。

如果使用 `SEGMENT REJECT LIMIT`，则 `COPY FROM` 操作将以单行错误隔离模式运行。在此版本中，单行错误隔离模式仅适用于输入文件中存在格式错误的行——例如，多出或缺少属性、属性的数据类型错误，或客户端编码序列无效。违反 `NOT NULL`、`CHECK` 或 `UNIQUE` 约束等约束错误仍按“全有或全无”的输入模式处理。用户可以指定可接受的错误行数（按每个 Segment 计算），超过该数量后，整个 `COPY FROM` 操作将被取消，不会加载任何行。错误行计数是按 Segment 计算的，而不是针对整个加载操作。如果未达到每个 Segment 的拒绝限制，则所有不含错误的行都会被加载，任何错误行都会被丢弃。若要保留错误行以便进一步检查，请指定 `LOG ERRORS` 子句来捕获错误日志信息。错误信息和对应的行在 Apache Cloudberry 内部存储。

**输出**

成功完成时，`COPY` 命令返回如下形式的命令标签，其中 count 是复制的行数：

```sql
COPY <count>
```

如果在单行错误隔离模式下运行 `COPY FROM` 命令，并且有任何行因格式错误而未被加载，则会返回以下提示消息，其中 count 是被拒绝的行数：

```sql
NOTICE: Rejected <count> badly formatted rows.
```

## 参数 {#parameters}

**`table_name`**

现有表的名称（可以带模式限定）。

**`column_name`**

要复制的列的可选列表。如果未指定列列表，则复制表的所有列。

以默认的文本格式复制时，`bytea` 类型列中的一行数据最大可达 256MB。

**`query`**

要复制其结果的 `SELECT` 或 `VALUES` 命令。请注意，查询两侧必须加括号。

**`filename`**

输入或输出文件的路径名。输入文件名可以是绝对路径或相对路径，但输出文件名必须是绝对路径。Windows 用户可能需要使用 `E''` 字符串，并将路径名中使用的每个反斜杠写成两个。

**`PROGRAM 'command'`**

指定要运行的命令。在 `COPY FROM` 中，输入从该命令的标准输出读取；在 `COPY TO` 中，输出写入该命令的标准输入。命令必须从 Apache Cloudberry Coordinator 主机系统的角度指定，并且必须可由 Apache Cloudberry 管理员用户（`gpadmin`）执行。

命令由 shell 调用。向 shell 传递参数时，请去除或转义对 shell 有特殊含义的任何特殊字符。出于安全原因，最好使用固定的命令字符串，或者至少避免在字符串中传入任何用户输入。

指定 `ON SEGMENT` 时，该命令必须可由 Apache Cloudberry 管理员用户（`gpadmin`）在所有 Apache Cloudberry 主 Segment 主机上执行。该命令由每个 Cloudberry Segment 实例运行。命令中必须包含 `<SEGID>`。

有关命令语法要求以及指定该子句时所复制的数据，请参见 `ON SEGMENT` 子句。

**`STDIN`**

指定输入来自客户端应用程序。`STDIN` 不支持 `ON SEGMENT` 子句。

**`STDOUT`**

指定输出发往客户端应用程序。`STDOUT` 不支持 `ON SEGMENT` 子句。

**`boolean`**

指定是否启用或关闭所选选项。可以写 `TRUE`、`ON` 或 `1` 来启用该选项，写 `FALSE`、`OFF` 或 `0` 来停用它。布尔值也可以省略，此时假定为 `TRUE`。

**`FORMAT`**

选择要读取或写入的数据格式：`text`、`csv`（逗号分隔值）或 `binary`。默认值为 `text`。

**`OIDS`**

指定复制每一行的 OID。（如果对没有 OID 的表指定 OIDS，或在复制查询结果时指定，则会引发错误。）

**`FREEZE`**

请求复制数据时使行处于已冻结状态，就像运行 `VACUUM FREEZE` 命令之后那样。这是用于初始数据加载的性能选项。只有当被加载的表是在当前子事务中创建或截断的、没有打开的游标，并且此事务没有持有更旧的快照时，行才会被冻结。

请注意，数据一旦成功加载，所有其他会话就能立即看到这些数据。这违反了 MVCC 可见性的正常规则，指定此选项的用户应了解它可能引起的潜在问题。

**`DELIMITER`**

指定文件每一行中分隔各列的字符。在 `text` 格式中默认为制表符，在 `CSV` 格式中默认为逗号。它必须是单个单字节字符。使用 `binary` 格式时不允许此选项。

**`NULL`**

指定表示空值的字符串。在 `text` 格式中默认为 `\N`（反斜杠-N），在 `CSV` 格式中默认为不带引号的空字符串。如果你不想区分空值和空字符串，即使在 `text` 格式中也可能更倾向于使用空字符串。使用 `binary` 格式时不允许此选项。

> **注意** 使用 `COPY FROM` 时，任何与此字符串匹配的数据项都将作为空值存储，因此应确保使用与 `COPY TO` 时相同的字符串。

**`HEADER`**

指定文件包含一个标题行，其中给出文件中各列的名称。在输出时，第一行包含表中的列名；在输入时，第一行会被忽略。仅在使用 `CSV` 格式时允许此选项。

**`QUOTE`**

指定数据值被引用时使用的引号字符。默认为双引号。它必须是单个单字节字符。仅在使用 `CSV` 格式时允许此选项。

**`ESCAPE`**

指定应出现在与 `QUOTE` 值相匹配的数据字符之前的字符。默认与 `QUOTE` 值相同（因此如果引号字符出现在数据中，它会被重复一次）。它必须是单个单字节字符。仅在使用 `CSV` 格式时允许此选项。

**`FORCE_QUOTE`**

强制对每个指定列中所有非 `NULL` 值使用引号。`NULL` 输出从不加引号。如果指定 `*`，则所有列中的非 `NULL` 值都会加引号。此选项仅允许用于 `COPY TO`，并且仅在使用 `CSV` 格式时可用。

**`FORCE_NOT_NULL`**

不将指定列的值与 NULL 字符串进行匹配。在 NULL 字符串为空的默认情况下，这意味着空值会被读取为零长度字符串而不是 NULL，即使它们没有加引号也是如此。此选项仅允许用于 `COPY FROM`，并且仅在使用 `CSV` 格式时可用。

**`FORCE_NULL`**

将指定列的值与 NULL 字符串进行匹配，即使该值已加引号也是如此；如果匹配，则把该值设置为 `NULL`。在 NULL 字符串为空的默认情况下，这会把加引号的空字符串转换为 `NULL`。此选项仅允许用于 `COPY FROM`，并且仅在使用 `CSV` 格式时可用。

**`ENCODING`**

指定文件使用 encoding_name 编码。如果省略此选项，则使用当前客户端编码。更多细节请参见下面的“注解”。

**`ON SEGMENT`**

指定 Segment 主机上各个独立的 Segment 数据文件。每个文件包含由主 Segment 实例管理的表数据。例如，使用 `COPY TO...ON SEGMENT` 命令把表数据复制到文件时，该命令会在 Segment 主机上为该主机上的每个 Segment 实例创建一个文件。每个文件包含由该 Segment 实例管理的表数据。

`COPY` 命令不会从镜像 Segment 实例和 Segment 数据文件复制数据，也不会向它们复制数据。

`ON SEGMENT` 不支持关键字 `STDIN` 和 `STDOUT`。

字符串字面量 `<SEG_DATA_DIR>` 和 `<SEGID>` 用于指定绝对路径和文件名，语法如下：

```sql
COPY <table> [TO|FROM] '<SEG_DATA_DIR>/<gpdumpname><SEGID>_<suffix>' ON SEGMENT;
```

**`<SEG_DATA_DIR\>`**

表示 `ON SEGMENT` 复制所用 Segment 实例数据目录绝对路径的字符串字面量。尖括号（`<` 和 `>`）是用于指定路径的字符串字面量的一部分。运行 `COPY` 时，`COPY` 会用 Segment 路径替换该字符串字面量。可以使用绝对路径代替 `<SEG_DATA_DIR>` 字符串字面量。

**`<SEGID\>`**

表示进行 `ON SEGMENT` 复制时要复制的 Segment 实例的 content ID 编号的字符串字面量。指定 `ON SEGMENT` 时，`<SEGID>` 是文件名中必需的部分。尖括号是用于指定文件名的字符串字面量的一部分。

使用 `COPY TO` 时，运行 `COPY` 命令时该字符串字面量会被替换为 Segment 实例的 content ID。

使用 `COPY FROM` 时，请在文件名中指定 Segment 实例的 content ID，并将该文件放在该 Segment 实例所在的主机上。每台主机上的每个主 Segment 实例都必须有一个对应的文件。运行 `COPY FROM` 命令时，数据会从该文件复制到 Segment 实例。

指定 `PROGRAM command` 子句时，命令中必须包含 `<SEGID>` 字符串字面量，`<SEG_DATA_DIR>` 字符串字面量则是可选的。请参见[示例](#examples)。

对于 `COPY FROM...ON SEGMENT` 命令，数据复制到表中时会检查表的分布策略。默认情况下，如果某数据行违反了表的分布策略，则返回错误。你可以通过服务器配置参数 `gp_enable_segment_copy_checking` 停用分布策略检查。请参见[注解](#notes)。

**`NEWLINE`**

指定数据文件中使用的换行符——`LF`（换行，0x0A）、`CR`（回车，0x0D）或 `CRLF`（回车加换行，0x0D 0x0A）。如果未指定，Apache Cloudberry Segment 将通过检查它收到的第一行数据来检测换行符类型，并使用遇到的第一种换行符类型。

**`CSV`**

选择逗号分隔值（CSV）模式。请参见 [CSV 格式](#file-formats)。

**`FILL MISSING FIELDS`**

在 `TEXT` 和 `CSV` 两种格式的 `COPY FROM` 中，当某行数据在行尾缺少数据字段时，指定 `FILL MISSING FIELDS` 会把缺失的尾部字段值设置为 `NULL`（而不是报告错误）。空行、带有 `NOT NULL` 约束的字段，以及行尾的尾部分隔符仍会报告错误。

**`LOG ERRORS`**

这是一个可选子句，可以放在 `SEGMENT REJECT LIMIT` 子句之前，用于捕获有关存在格式错误的行的错误日志信息。

错误日志信息在内部存储，并通过 Apache Cloudberry 内置 SQL 函数 `gp_read_error_log()` 访问。

有关错误日志信息以及用于查看和管理错误日志信息的内置函数，请参见[注解](#notes)。

**`SEGMENT REJECT LIMIT count [ROWS | PERCENT]`**

以单行错误隔离模式运行 `COPY FROM` 操作。如果输入行存在格式错误，只要在加载操作期间没有任何一个 Apache Cloudberry Segment 实例达到拒绝限制数，这些行就会被丢弃。拒绝限制数可以指定为行数（默认）或占总行数的百分比（1-100）。如果使用 `PERCENT`，则每个 Segment 只有在处理完参数 `gp_reject_percent_threshold` 所指定的行数之后，才开始计算错误行百分比。`gp_reject_percent_threshold` 的默认值为 300 行。违反 `NOT NULL`、`CHECK` 或 `UNIQUE` 约束等约束错误仍按“全有或全无”的输入模式处理。如果未达到限制，则所有正确的行都会被加载，任何错误行都会被丢弃。

> **注意** 如果没有先触发 `SEGMENT REJECT LIMIT` 或未指定该子句，Apache Cloudberry 会限制最初可以包含格式错误的行数。如果前 1000 行被拒绝，`COPY` 操作会停止并回滚。

最初被拒绝行数的限制可以通过 Apache Cloudberry 服务器配置参数 `gp_initial_bad_row_limit` 更改。有关该参数的信息，请参见服务器配置参数。

**`IGNORE EXTERNAL PARTITIONS`**

从分区表复制数据时，不会从属于外部表的叶子分区复制数据。未复制数据时，日志文件中会添加一条消息。

如果未指定此子句，并且 Apache Cloudberry 尝试从属于外部表的叶子分区复制数据，则会返回错误。

有关指定 SQL 查询以从属于外部表的叶子分区复制数据的信息，请参见下一节“注解”。

## 注解 {#notes}

`COPY` 只能用于表，不能用于外部表或视图。不过，你可以写成 `COPY (SELECT * FROM viewname) TO ...`

`COPY` 只处理所指定的表本身；它不会向子表复制数据，也不会从子表复制数据。因此，例如 `COPY table TO` 显示的数据与 `SELECT * FROM ONLY `table`` 相同。但可以使用 `COPY (SELECT * FROM table) TO ...` 转储继承层次结构中的所有数据。

类似地，若要从包含属于外部表的叶子分区的分区表中复制数据，请使用 SQL 查询来选择要复制的数据。例如，如果表 `my_sales` 包含一个属于外部表的叶子分区，则命令 `COPY my_sales TO stdout` 会返回错误。下面的命令则会把数据发送到 `stdout`：

```sql
COPY (SELECT * from my_sales ) TO stdout
```

`BINARY` 关键字会使所有数据以二进制格式而不是文本格式存储或读取。它比普通文本模式稍快，但二进制格式文件在不同机器架构和 Apache Cloudberry 版本之间的可移植性较差。此外，如果数据为二进制格式，则不能在单行错误隔离模式下运行 `COPY FROM`。

你必须对 `COPY TO` 所读取值的表拥有 `SELECT` 权限，对 `COPY FROM` 所插入值的表拥有 `INSERT` 权限。拥有命令中所列各列的列权限即可。

`COPY` 命令中指定的文件由数据库服务器直接读取或写入，而不是由客户端应用程序读取或写入。因此，这些文件必须位于 Apache Cloudberry Coordinator 主机上或可由其访问，而不是位于客户端。这些文件必须可被 Apache Cloudberry 系统用户（运行服务器的用户 ID）访问并读取或写入，而不是可被客户端访问。只允许数据库超级用户在 `COPY` 中指定文件名，因为这样可以读取或写入服务器有权限访问的任何文件。

`COPY FROM` 会调用目标表上的任何触发器并检查约束。但是，它不会调用重写规则。请注意，在此版本中，单行错误隔离模式不会对违反约束的情况进行评估。

`COPY` 的输入和输出受 `DateStyle` 影响。为了确保可移植到可能使用非默认 `DateStyle` 设置的其他 Apache Cloudberry 安装，在使用 `COPY TO` 之前应将 `DateStyle` 设置为 ISO。同样，最好避免在 IntervalStyle 设置为 `sql_standard` 时转储数据，因为负的间隔值可能被 IntervalStyle 设置不同的服务器误解。

输入数据按 `ENCODING` 选项或当前客户端编码进行解释，输出数据按 `ENCODING` 或当前客户端编码进行编码，即使数据并不经过客户端，而是由服务器直接从文件读取或写入文件，也是如此。

以文本模式从文件复制 XML 数据时，服务器配置参数 xmloption 会影响所复制 XML 数据的验证。如果该值为 `content`（默认值），则 XML 数据按 XML 内容片段进行验证。如果参数值为 `document`，则 XML 数据按 XML 文档进行验证。如果 XML 数据无效，`COPY` 会返回错误。

默认情况下，`COPY` 在遇到第一个错误时停止操作。对于 `COPY TO`，这应该不会引起问题，但对于 `COPY FROM`，目标表已经收到了之前的行。这些行将不可见也无法访问，但仍然占用磁盘空间。如果故障发生在一个大型 `COPY FROM` 操作的较后阶段，这可能浪费大量磁盘空间。你可能希望调用 `VACUUM` 来回收浪费的空间。另一种选择是使用单行错误隔离模式过滤掉错误行，同时仍然加载正确的行。

`FORCE_NULL` 和 `FORCE_NOT_NULL` 可以同时用于同一列。其结果是把带引号的 NULL 字符串转换为空值，并把不带引号的 NULL 字符串转换为空字符串。

运行 `COPY FROM...ON SEGMENT` 命令时，服务器配置参数 `gp_enable_segment_copy_checking` 控制数据复制到表中时是否检查表的分布策略（来自表的 `DISTRIBUTED` 子句）。默认检查分布策略。如果数据行违反了该 Segment 实例的分布策略，则返回错误。有关该参数的信息，请参见服务器配置参数。

由 `COPY TO...ON SEGMENT` 命令生成的表数据可用于通过 `COPY FROM...ON SEGMENT` 恢复表数据。但是，恢复到各 Segment 的数据是按用 `COPY TO` 命令生成这些文件时的表分布策略分布的。如果你尝试恢复表数据，而表的分布策略在运行 `COPY FROM...ON SEGMENT` 之前已被更改，则 `COPY` 命令可能返回表分布策略错误。

> **注意** 如果运行 `COPY FROM...ON SEGMENT` 且服务器配置参数 `gp_enable_segment_copy_checking` 为 `false`，则可能需要手动重分布表数据。请参见 `ALTER TABLE` 子句 `WITH REORGANIZE`。

指定 `LOG ERRORS` 子句时，Apache Cloudberry 会捕获读取外部表数据时发生的错误。你可以查看和管理所捕获的错误日志数据。

- 使用内置 SQL 函数 `gp_read_error_log('table_name')`。它要求对 table_name 拥有 `SELECT` 权限。此示例显示通过 `COPY` 命令加载到表 `ext_expenses` 的数据的错误日志信息：

    ```sql
    SELECT * from gp_read_error_log('ext_expenses');
    ```

    如果 table_name 不存在，该函数返回 `FALSE`。

- 如果指定表已存在错误日志数据，则新的错误日志数据会追加到现有错误日志数据之后。错误日志信息不会复制到镜像 Segment。
- 使用内置 SQL 函数 `gp_truncate_error_log('table_name')` 删除 table_name 的错误日志数据。它要求具有表所有者权限。此示例删除将数据移入表 `ext_expenses` 时捕获的错误日志信息：

    ```sql
    SELECT gp_truncate_error_log('ext_expenses'); 
    ```

    如果 table_name 不存在，该函数返回 `FALSE`。

    指定 `*` 通配符可删除当前数据库中现有表的错误日志信息。指定字符串 `*.*` 可删除所有数据库的错误日志信息，包括因先前数据库问题而未被删除的错误日志信息。如果指定 \*，则需要数据库所有者权限。如果指定 `*.*`，则需要操作系统超级用户权限。

当不是超级用户的 Apache Cloudberry 用户运行 `COPY` 命令时，该命令可以由资源队列控制。资源队列必须配置 `ACTIVE_STATEMENTS` 参数，该参数指定分配给该队列的角色可运行的查询数量上限。Apache Cloudberry 不会对 `COPY` 命令应用代价值或内存值，因此仅设置了代价或内存限制的资源队列不会影响 `COPY` 命令的运行。

非超级用户只能运行以下类型的 `COPY` 命令：

- 源为 `stdin` 的 `COPY FROM` 命令
- 目标为 `stdout` 的 `COPY TO` 命令

## 文件格式 {#file-formats}

`COPY` 支持的文件格式。

**文本格式**

使用 `text` 格式时，读取或写入的数据是一个文本文件，每个表行占一行。行中的各列由 delimiter_character（默认为制表符）分隔。列值本身是由各属性数据类型的输出函数生成的字符串，或各属性数据类型的输入函数可接受的字符串。对于为空值的列，使用指定的 NULL 字符串代替。如果输入文件的任何一行所包含的列数多于或少于预期，`COPY FROM` 都会引发错误。如果指定了 `OIDS`，则 OID 会作为第一列读取或写入，位于用户数据列之前。

数据文件有两个对 `COPY` 具有特殊含义的保留字符：

- 指定的分隔符（默认为制表符），用于分隔数据文件中的字段。
- UNIX 风格的换行符（`\n` 或 `0x0a`），用于标示数据文件中的新行。强烈建议生成 `COPY` 数据的应用程序把数据换行符转换为 UNIX 风格的换行符，而不是 Microsoft Windows 风格的回车换行符（`\r\n` 或 `0x0a 0x0d`）。

如果你的数据包含这两个字符中的任何一个，则必须对该字符进行转义，使 `COPY` 将其视为数据，而不是字段分隔符或新行。

默认情况下，文本格式文件的转义字符是 \\（反斜杠），csv 格式文件的转义字符是 `"`（双引号）。如果你想使用不同的转义字符，可以使用 `ESCAPE AS` 子句。请确保选择的转义字符不会在数据文件中作为实际数据值出现。你还可以使用 `ESCAPE 'OFF'` 在文本格式文件中停用转义。

例如，假设你有一个包含三列的表，并且想使用 `COPY` 加载以下三个字段。

- 百分号 = %
- 竖线 = |
- 反斜杠 = \\

你指定的 delimiter_character 是 `|`（竖线字符），指定的转义字符是 `*`（星号）。数据文件中格式化后的行如下所示：

```sql
percentage sign = % | vertical bar = *| | backslash = \
```

请注意，属于数据一部分的竖线字符已使用星号字符（\*）转义。还请注意，由于我们使用了另一个转义字符，因此不需要对反斜杠进行转义。

如果下列字符作为列值的一部分出现，则必须在其前面加上转义字符：转义字符本身、换行符、回车符和当前分隔符。你可以使用 `ESCAPE AS` 子句指定不同的转义字符。

**CSV 格式**

此格式选项用于导入和导出许多其他程序（例如电子表格）使用的逗号分隔值（CSV）文件格式。它不使用 Apache Cloudberry 标准文本格式的转义规则，而是生成并识别通用的 CSV 转义机制。

每条记录中的值由 `DELIMITER` 字符分隔。如果值包含分隔符、`QUOTE` 字符、`ESCAPE` 字符（默认为双引号）、`NULL` 字符串、回车符或换行符，则整个值的前后都会加上 `QUOTE` 字符。你还可以使用 `FORCE_QUOTE` 在输出特定列中的非 `NULL` 值时强制加引号。

CSV 格式没有区分 `NULL` 值与空字符串的标准方法。Apache Cloudberry 的 `COPY` 通过引号来处理这一点。`NULL` 以 `NULL` 参数字符串输出并且不加引号，而与 `NULL` 字符串匹配的非 `NULL` 值则会加引号。例如，在默认设置下，`NULL` 写成不带引号的空字符串，而空字符串数据值则写成带双引号的形式（`""`）。读取值时遵循类似的规则。你可以使用 `FORCE_NOT_NULL` 阻止对特定列进行 `NULL` 输入比较。你还可以使用 `FORCE_NULL` 把带引号的 NULL 字符串数据值转换为 `NULL`。

由于反斜杠在 `CSV` 格式中不是特殊字符，因此数据结束标记 `\.` 也可能作为数据值出现。为避免任何误解，单独出现在一行上的 `\.` 数据值在输出时会自动加引号，而在输入时，如果加了引号，则不会被解释为数据结束标记。如果你加载的是由另一个应用程序创建的文件，该文件只有一个不带引号的列，并且其值可能是 `\.`，则可能需要在输入文件中为该值加上引号。

> **注意** 在 `CSV` 格式中，所有字符都是有意义的。被空白字符或 `DELIMITER` 以外的任何字符包围的带引号的值，将包含这些字符。如果你从一个把 CSV 行用空白字符填充到某个固定宽度的系统导入数据，这可能导致错误。如果出现这种情况，你可能需要先预处理 CSV 文件以去除尾部空白，然后再将数据导入 Apache Cloudberry。

`CSV` 格式既能识别也能生成包含内嵌回车符和换行符的带引号值的 CSV 文件。因此，这些文件并不像文本格式文件那样严格地每个表行占一行。

> **注意** 许多程序会生成奇怪的、有时甚至是反常的 CSV 文件，因此该文件格式更像是一种惯例而不是标准。所以你可能会遇到一些无法用这种机制导入的文件，而 `COPY` 也可能生成其他程序无法处理的文件。

**二进制格式**

`binary` 格式选项会使所有数据以二进制格式而不是文本格式存储或读取。它比文本格式和 `CSV` 格式稍快，但二进制格式文件在不同机器架构和 Apache Cloudberry 版本之间的可移植性较差。此外，二进制格式与数据类型高度相关；例如，从 `smallint` 列输出二进制数据再读入 `integer` 列是行不通的，尽管这在文本格式中完全可行。

二进制文件格式由文件头、零个或多个包含行数据的元组以及文件尾组成。头部和数据采用网络字节序。

- **文件头** — 文件头由 15 字节的固定字段组成，后跟可变长度的头部扩展区。固定字段如下：
    - **签名** — 11 字节序列 PGCOPY\\n\\377\\r\\n\\0 — 请注意，零字节是签名中必需的一部分。（该签名的设计目的是便于识别那些经过非 8 位透明传输而遭到破坏的文件。行尾转换过滤器、丢失的零字节、丢失的高位或奇偶校验变化都会改变此签名。）
    - **标志字段** — 32 位整数位掩码，用于表示文件格式的重要方面。位从 0（LSB）到 31（MSB）编号。请注意，此字段与文件格式中使用的所有整数字段一样，以网络字节序（最高有效字节在前）存储。第 16-31 位保留用于表示关键的文件格式问题；如果读取器发现此范围内设置了意外的位，应取消操作。第 0-15 位保留用于标示向后兼容的格式问题；读取器应直接忽略此范围内设置的任何意外位。当前只定义了一个标志，其余位必须为零（第 16 位：如果数据带有 OID 则为 1，否则为 0）。
    - **头部扩展区长度** — 32 位整数，表示头部剩余部分的字节长度，不包括其自身。当前该值为零，第一个元组紧随其后。将来对格式的更改可能允许头部中存在额外数据。读取器应静默跳过其不知道如何处理的任何头部扩展数据。设想头部扩展区将包含一系列自标识的块。标志字段并不用于告知读取器扩展区中有什么内容。头部扩展内容的具体设计留待以后的版本。
- **元组** — 每个元组以一个 16 位整数开始，表示元组中的字段数。（目前，表中所有元组的字段数都相同，但将来不一定总是如此。）然后，对元组中的每个字段重复如下内容：一个 32 位长度字，后跟相应字节数的字段数据。（长度字不包括其自身，并且可以为零。）作为特例，-1 表示 NULL 字段值。在 NULL 的情况下，后面没有值字节。

    字段之间没有对齐填充或任何其他额外数据。

    目前，假定二进制格式文件中的所有数据值都是二进制格式（格式代码一）。预计将来的扩展可能会增加一个头部字段，允许为各列分别指定格式代码。

    如果文件中包含 OID，则 OID 字段紧跟在字段数字之后。它是一个普通字段，只是不计入字段数。特别地，它有一个长度字——这样可以不太费力地处理 4 字节与 8 字节的 OID，并且如果将来证明有此需要，还可以将 OID 显示为空值。

- **文件尾** — 文件尾由一个包含 `-1` 的 16 位整数字组成。这很容易与元组的字段数字区分开。如果字段数字既不是 `-1` 也不是预期的列数，读取器应报告错误。这为防止与数据以某种方式失去同步提供了额外的检查。

## 示例 {#examples}

使用竖线（|）作为字段分隔符，将表复制到客户端：

```sql
COPY country TO STDOUT (DELIMITER '|');
```

将文件中的数据复制到 `country` 表中：

```sql
COPY country FROM '/home/usr1/sql/country_data';
```

只把名称以 'A' 开头的国家复制到文件中：

```sql
COPY (SELECT * FROM country WHERE country_name LIKE 'A%') TO 
'/home/usr1/sql/a_list_countries.copy';
```

使用单行错误隔离模式并记录错误，将文件中的数据复制到 `sales` 表中：

```sql
COPY sales FROM '/home/usr1/sql/sales_data' LOG ERRORS 
   SEGMENT REJECT LIMIT 10 ROWS;
```

若要复制 Segment 数据供以后使用，请使用 `ON SEGMENT` 子句。`COPY TO ON SEGMENT` 命令的使用形式如下：

```sql
COPY <table> TO '<SEG_DATA_DIR>/<gpdumpname><SEGID>_<suffix>' ON SEGMENT; 
```

`<SEGID>` 是必需的。但是，你可以用绝对路径替换路径中的 `<SEG_DATA_DIR>` 字符串字面量。

当你把字符串字面量 `<SEG_DATA_DIR>` 和 `<SEGID>` 传递给 `COPY` 时，`COPY` 会在运行操作时填入相应的值。

例如，如果你有一个 `mytable`，其 Segment 和镜像 Segment 如下所示：

```sql
contentid | dbid | file segment location 
    0     |  1   | /home/usr1/data1/gpsegdir0
    0     |  3   | /home/usr1/data_mirror1/gpsegdir0 
    1     |  4   | /home/usr1/data2/gpsegdir1
    1     |  2   | /home/usr1/data_mirror2/gpsegdir1 
```

运行命令：

```sql
COPY mytable TO '<SEG_DATA_DIR>/gpbackup<SEGID>.txt' ON SEGMENT;
```

将产生以下文件：

```sql
/home/usr1/data1/gpsegdir0/gpbackup0.txt
/home/usr1/data2/gpsegdir1/gpbackup1.txt
```

第一列中的 content ID 是插入到文件路径中的标识符（例如上面的 `gpsegdir0/gpbackup0.txt`）。文件是在 Segment 主机上创建的，而不是像标准 `COPY` 操作那样在 Coordinator 上创建。使用 `ON SEGMENT` 复制时，不会为镜像 Segment 创建数据文件。

如果指定的是绝对路径而不是 `<SEG_DATA_DIR>`，例如在以下语句中

```sql
COPY mytable TO '/tmp/gpdir/gpbackup_<SEGID>.txt' ON SEGMENT;
```

文件将被放置在每个 Segment 上的 `/tmp/gpdir` 中。如果需要重分布，也可以使用 `gpfdist` 工具来恢复通过带 `ON SEGMENT` 选项的 `COPY TO` 生成的数据文件。

> **注意** 可以使用 `gpfdist` 等工具恢复数据。备份/恢复工具不适用于通过 `COPY TO ON SEGMENT` 手动生成的文件。

此示例使用 `SELECT` 语句将数据复制到每个 Segment 上的文件中：

```sql
COPY (SELECT * FROM testtbl) TO '/tmp/mytst<SEGID>' ON SEGMENT;
```

此示例复制 `lineitem` 表中的数据，并使用 `PROGRAM` 子句通过 `cat` 工具将数据添加到 `/tmp/lineitem_program.csv` 文件中。该文件位于 Apache Cloudberry Coordinator 上。

```sql
COPY LINEITEM TO PROGRAM 'cat > /tmp/lineitem.csv' CSV; 
```

此示例使用 `PROGRAM` 和 `ON SEGMENT` 子句将数据复制到 Segment 主机上的文件中。在 Segment 主机上，`COPY` 命令会用 Segment content ID 替换 `<SEGID>`，为该 Segment 主机上的每个 Segment 实例创建一个文件。

```sql
COPY LINEITEM TO PROGRAM 'cat > /tmp/lineitem_program<SEGID>.csv' ON SEGMENT CSV; 
```

此示例使用 `PROGRAM` 和 `ON SEGMENT` 子句从 Segment 主机上的文件复制数据。从文件复制数据时，`COPY` 命令会用 Segment content ID 替换 `<SEGID>`。在 Segment 主机上，每个 Segment 实例都必须有一个对应的文件，且文件名包含该 Segment 主机上的 Segment content ID。

```sql
COPY LINEITEM_4 FROM PROGRAM 'cat /tmp/lineitem_program<SEGID>.csv' ON SEGMENT CSV;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `COPY` 语句。

Apache Cloudberry 早期版本中使用的以下语法仍然受支持：

```sql
COPY <table_name> [(<column_name> [, ...])] FROM {'<filename>' | PROGRAM '<command>' | STDIN}
     [ [WITH]  
       [ON SEGMENT]
       [BINARY]
       [OIDS]
       [HEADER]
       [DELIMITER [ AS ] '<delimiter_character>']
       [NULL [ AS ] '<null string>']
       [ESCAPE [ AS ] '<escape>' | 'OFF']
       [NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF']
       [CSV [QUOTE [ AS ] '<quote>'] 
            [FORCE NOT NULL <column_name> [, ...]]
       [FILL MISSING FIELDS]
       [[LOG ERRORS]  
       SEGMENT REJECT LIMIT <count> [ROWS | PERCENT] ]

COPY { <table_name> [(<column_name> [, ...])] | (<query>)} TO {'<filename>' | PROGRAM '<command>' | STDOUT}
      [ [WITH] 
        [ON SEGMENT]
        [BINARY]
        [OIDS]
        [HEADER]
        [DELIMITER [ AS ] 'delimiter_character']
        [NULL [ AS ] 'null string']
        [ESCAPE [ AS ] '<escape>' | 'OFF']
        [CSV [QUOTE [ AS ] 'quote'] 
             [FORCE QUOTE <column_name> [, ...]] | * ]
      [IGNORE EXTERNAL PARTITIONS ]
```

请注意，在此语法中，`BINARY` 和 `CSV` 被视为独立的关键字，而不是 FORMAT 选项的参数。

## 另见 {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/)
