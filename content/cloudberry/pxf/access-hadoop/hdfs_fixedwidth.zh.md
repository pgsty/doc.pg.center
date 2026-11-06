---
title: "读写定宽文本数据"
description: "通过 PXF 读取 HDFS 中的定宽文本数据。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_fixedwidth.md"
---

PXF HDFS Connector 支持使用 Apache Cloudberry 定宽自定义格式化器（fixed width custom formatter）读写定宽文本。本节介绍如何使用 PXF 访问定宽文本，包括如何创建引用 HDFS 数据存储中文件的外部表、对其进行查询以及向其中插入数据。

PXF 支持读取或写入使用 `default`、`bzip2` 和 `gzip` 编解码器压缩的定宽文本。

## 前提条件 {#prerequisites}

在尝试从 HDFS 读取定宽文本或向 HDFS 写入定宽文本之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## 读取定宽文本数据 {#reading-text-data-with-fixed-widths}

读取定宽文本且每一行被视为一条记录时，使用 `hdfs:fixedwidth` Profile。以下语法创建一个引用 HDFS 上此类文本文件的 Apache Cloudberry 可读外部表： 

```sql
CREATE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:fixedwidth[&SERVER=<server_name>][&NEWLINE=<bytecode>][&IGNORE_MISSING_PATH=<boolean>]')
FORMAT 'CUSTOM' (FORMATTER='fixedwidth_in', <field_name>='<width>' [, ...] [, line_delim[=|<space>][E]'<delim_value>']);
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | 当 \<path-to-hdfs-file\> 引用定宽文本数据时，使用 `PROFILE=hdfs:fixedwidth`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| NEWLINE=\<bytecode\>    | 当 `line_delim` 格式化器选项包含 `\r`、`\r\n` 或一组自定义转义字符时，必须分别将 `<bytecode>` 设置为 `CR`、`CRLF` 或该组字节码字符。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空数据集。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `FORMATTER='fixedwidth_in'`（读）配合使用。 |
| \&lt;field_name&gt;='\&lt;width&gt;'    | 字段的名称和宽度。例如：`first_name='15'` 指定 `first_name` 字段长度为 `15` 个字符。默认情况下，当字段值小于 `<width>` 大小时，Apache Cloudberry 期望该字段以空格右填充至该大小。 |
| line_delim    | 数据中的行分隔符字符。当 \<delim_value\> 为转义序列时，在其前面加上 `E`。示例：`line_delim=E'\n'`、`line_delim 'aaa'`。默认值为 `'\n'`。|

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。

## 关于指定 field_name 和 width {#about-specifying-field_name-and-width}

Apache Cloudberry 按物理顺序加载定宽数据行中的所有字段。您在 `FORMAT` 选项中指定的 `<field_name>` 必须与您在 `CREATE [WRITABLE] EXTERNAL TABLE` 命令中定义列的顺序一致。每个字段的大小通过 `<width>` 值指定。

有关格式化器选项的更多信息，请参阅 Apache Cloudberry 定宽自定义格式化器文档。

## 关于 line_delim 和 NEWLINE 格式化器选项 {#about-the-line_delim-and-newline-formatter-options}

默认情况下，Apache Cloudberry 使用 `\n`（LF）字符作为换行分隔符。当外部文件的行分隔符同样是 `\n` 时，无需指定 `line_delim` 选项。如果提供了 `line_delim` 格式化器选项，并且其值包含 `\r`（CR）、`\r\n`（CRLF）或一组自定义转义字符，则必须在外部表的 `LOCATION` 子句中指定 `NEWLINE` 选项，并分别将其值设置为 `CR`、`CRLF` 或该组字节码字符。

有关格式化器选项的更多信息，请参阅 Apache Cloudberry 定宽自定义格式化器文档。

## 示例：读取 HDFS 上的定宽文本数据 {#example-reading-fixed-width-text-data-on-hdfs}

按以下步骤创建示例文本文件，将文件复制到 HDFS，并使用 `hdfs:fixedwidth` Profile 和默认 PXF 服务器创建 PXF 外部表来查询这些数据：

1. 为 PXF 示例数据文件创建 HDFS 目录。例如：

    ```shell
    $ hdfs dfs -mkdir -p /data/pxf_examples
    ```

2. 创建名为 `pxf_hdfs_fixedwidth.txt` 的纯文本数据文件：

    ```shell
    $ echo 'Prague         Jan 101   4875.33   
    Rome           Mar 87    1557.39   
    Bangalore      May 317   8936.99   
    Beijing        Jul 411   11600.67  ' > /tmp/pxf_hdfs_fixedwidth.txt
    ```

    在此示例文件中，第一个字段长 15 个字符，第二个字段长 4 个字符，第三个字段长 6 个字符，最后一个字段长 10 个字符。

    > **注意** 请使用您选择的编辑器打开 `/tmp/pxf_hdfs_fixedwidth.txt` 文件，并确保最后一个字段以空格右填充至 10 个字符的大小。

4. 将数据文件复制到 HDFS：

    ```shell
    $ hdfs dfs -put /tmp/pxf_hdfs_fixedwidth.txt /data/pxf_examples/
    ```

5. 显示存储在 HDFS 中的 `pxf_hdfs_fixedwidth.txt` 文件的内容：

    ```shell
    $ hdfs dfs -cat /data/pxf_examples/pxf_hdfs_fixedwidth.txt
    ```

4. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

1. 使用 PXF `hdfs:fixedwidth` Profile 创建 Apache Cloudberry 外部表，该表引用您刚创建并添加到 HDFS 的 `pxf_hdfs_fixedwidth.txt` 文件：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_fixedwidth_r(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://data/pxf_examples/pxf_hdfs_fixedwidth.txt?PROFILE=hdfs:fixedwidth&NEWLINE=CRLF')
               FORMAT 'CUSTOM' (formatter='fixedwidth_in', location='15', month='4', num_orders='6', total_sales='10', line_delim=E'\r\n');
    ```
              
2. 查询外部表：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_fixedwidth_r;
    ```

    ```text
       location    | month | num_orders | total_sales 
    ---------------+-------+------------+-------------
     Prague        | Jan   |        101 |     4875.33
     Rome          | Mar   |         87 |     1557.39
     Bangalore     | May   |        317 |     8936.99
     Beijing       | Jul   |        411 |    11600.67
    (4 rows)
    ```

## 向 HDFS 写入定宽文本数据 {#writing-fixed-width-text-data-to-hdfs}

PXF HDFS 连接器的 `hdfs:fixedwidth` Profile 支持向 HDFS 写入定宽文本。使用 PXF HDFS 连接器创建可写外部表时，需要指定 HDFS 上某个目录的名称。向可写外部表插入记录时，所插入的数据块会被写入您所指定目录中的一个或多个文件。

**注意**：使用可写 Profile 创建的外部表只能用于 `INSERT` 操作。如果要查询已插入的数据，必须另外创建一个引用该 HDFS 目录的可读外部表。

使用以下语法创建引用 HDFS 目录的 Apache Cloudberry 可写外部表： 

```sql
CREATE WRITABLE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-dir>
    ?PROFILE=hdfs:fixedwidth[&SERVER=<server_name>][&NEWLINE=<bytecode>][&<write-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='fixedwidth_out' [, <field_name>='<width>'] [, ...] [, line_delim[=|<space>][E]'<delim_value>']);
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;dir\>    | HDFS 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | 使用 `PROFILE=hdfs:fixedwidth` 将定宽数据写入 \<path-to-hdfs-file\>。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| NEWLINE=\<bytecode\>    | 当 `line_delim` 格式化器选项包含 `\r`、`\r\n` 或一组自定义转义字符时，必须分别将 `<bytecode>` 设置为 `CR`、`CRLF` 或该组字节码字符。 |
| \<write&#8209;option\>=\<value\>  | 下文介绍 \<write-option\>。|
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `FORMATTER='fixedwidth_out'`（写）配合使用。 |
| \&lt;field_name&gt;='\&lt;width&gt;'    | 字段的名称和宽度。例如：`first_name='15'` 指定 `first_name` 字段长度为 `15` 个字符。默认情况下，向外部文件写入时，如果字段值小于 `<width>` 大小，Apache Cloudberry 会将该字段以空格右填充至 `<width>` 大小。 |
| line_delim    | 数据中的行分隔符字符。当 \<delim_value\> 为转义序列时，在其前面加上 `E`。示例：`line_delim=E'\n'`、`line_delim 'aaa'`。默认值为 `'\n'`。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间的额外数据移动。 |

使用 `hdfs:fixedwidth` Profile 创建的可写外部表可以选择使用记录压缩或块压缩。您可以通过 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中的选项指定压缩编解码器：

| 写选项  | 取值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入定宽文本数据时支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |

## 示例：向 HDFS 写入定宽文本数据 {#example-writing-fixed-width-text-data-to-hdfs}

此示例使用[示例：读取 HDFS 上的定宽文本数据](#example-reading-fixed-width-text-data-on-hdfs)中介绍的数据模式。 

| 列名  | 宽度 | 数据类型 |
|-------|-------|-------|
| location | 15 | text |
| month | 4 | text |
| number_of_orders | 6 | int |
| total_sales | 10 | float8 |

#### 步骤 {#procedure}

按以下步骤创建使用上述相同数据模式的 Apache Cloudberry 可写外部表。您将使用 PXF `hdfs:fixedwidth` Profile 和默认 PXF 服务器，将数据写入底层 HDFS 目录。您还将另外创建一个可读外部表，用于读取您写入 HDFS 目录的数据。

1. 使用上述数据模式创建 Apache Cloudberry 可写外部表。写入 HDFS 目录 `/data/pxf_examples/fixedwidth_write`。创建该表时指定 `\n` 作为行分隔符：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_hdfs_fixedwidth_w(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://data/pxf_examples/fixedwidth_write?PROFILE=hdfs:fixedwidth')
               FORMAT 'CUSTOM' (formatter='fixedwidth_out', location='15', month='4', num_orders='6', total_sales='10');
    ```
    
2. 对 `pxf_hdfs_fixedwidth_w` 表使用 `INSERT` 命令，向 HDFS 目录 `fixedwidth_write` 写入几条单独的记录：

    ```sql
    postgres=# INSERT INTO pxf_hdfs_fixedwidth_w VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    postgres=# INSERT INTO pxf_hdfs_fixedwidth_w VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

4. 在另一个终端窗口中，对 `fixedwidth_write` 目录使用 `cat` 命令，显示您刚添加到 HDFS 的数据：

    ```shell
    $ hdfs dfs -cat /data/pxf_examples/fixedwidth_write/*
    Frankfurt      Mar 777   3956.98   
    Cleveland      Oct 3812  96645.37  
    ```

5. Apache Cloudberry 不支持直接查询可写外部表。要查询刚添加到 HDFS 的数据，必须创建引用该 HDFS 目录的 Apache Cloudberry 可读外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_fixedwidth_r2(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://data/pxf_examples/fixedwidth_write?PROFILE=hdfs:fixedwidth')
               FORMAT 'CUSTOM' (formatter='fixedwidth_in', location='15', month='4', num_orders='6', total_sales='10');
    ```

6. 查询该可读外部表：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_fixedwidth_r2 ORDER BY total_sales;
    ```

    ```text
     location  | month | num_orders | total_sales 
    -----------+-------+------------+-------------
     Frankfurt | Mar   |        777 |     3956.98
     Cleveland | Oct   |       3812 |    96645.37
    (2 rows)
    ```
