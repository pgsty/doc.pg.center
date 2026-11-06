---
title: "读写对象存储中的定宽文本数据"
description: "通过 PXF 读取对象存储中的定宽文本数据。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_fixedwidth.md"
---

PXF 对象存储连接器通过 Apache Cloudberry 定宽自定义格式化器（fixed width custom formatter）支持读写定宽文本。本节介绍如何使用 PXF 访问定宽文本，包括如何创建、查询引用对象存储中文件的外部表，以及如何向其中插入数据。

**注意**：从对象存储访问定宽文本数据与在 HDFS 中访问此类数据非常相似。

## 前提条件 {#prerequisites}

在尝试从对象存储读取数据或向对象存储写入数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 读取定宽文本数据 {#reading-text-data-with-fixed-widths}

当从对象存储读取定宽文本且每行为一条记录时，使用 `<objstore>:fixedwidth` Profile。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| AWS S3    | s3 |

以下语法创建引用对象存储中此类文本文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:fixedwidth[&SERVER=<server_name>][&NEWLINE=<bytecode>][&IGNORE_MISSING_PATH=<boolean>]')
FORMAT 'CUSTOM' (FORMATTER='fixedwidth_in', <field_name>='<width>' [, ...] [, line_delim[=|<space>][E]'<delim_value>']);
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:fixedwidth | `PROFILE` 必须标明具体的对象存储。例如 `s3:fixedwidth`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。未指定时，PXF 使用 `default` 服务器。 |
| NEWLINE=\<bytecode\>    | 当 `line_delim` 格式化器选项包含 `\r`、`\r\n` 或一组自定义转义字符时，必须将 `<bytecode>` 分别设置为 `CR`、`CRLF` 或对应的字节码字符集。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片（fragment）。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `FORMATTER='fixedwidth_in'`（读）配合使用。 |
| \&lt;field_name&gt;='\&lt;width&gt;'    | 字段的名称和宽度。例如：`first_name='15'` 指定 `first_name` 字段长度为 `15` 个字符。默认情况下，当字段值小于 `<width>` 大小时，Apache Cloudberry 期望该字段在右侧以空格填充至该大小。 |
| line_delim    | 数据中的行分隔符字符。当值为转义序列时，在 \<delim_value\> 前加上 `E`。示例：`line_delim=E'\n'`、`line_delim 'aaa'`。默认值为 `'\n'`。|

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

## 关于指定 field_name 和 width {#about-specifying-field_name-and-width}

Apache Cloudberry 按物理顺序加载一行定宽数据中的所有字段。在 `FORMAT` 选项中指定的 `<field_name>` 必须与在 `CREATE [WRITABLE] EXTERNAL TABLE` 命令中定义列的顺序一致。每个字段的大小通过 `<width>` 值指定。

有关格式化器选项的更多信息，请参阅 Apache Cloudberry 定宽自定义格式化器文档。


## 关于 line_delim 和 NEWLINE 格式化器选项 {#about-the-line_delim-and-newline-formatter-options}

默认情况下，Apache Cloudberry 使用 `\n`（LF）字符作为换行分隔符。当外部文件的行分隔符同样为 `\n` 时，无需指定 `line_delim` 选项。如果提供了 `line_delim` 格式化器选项且其值包含 `\r`（CR）、`\r\n`（CRLF）或一组自定义转义字符，则必须在外部表的 `LOCATION` 子句中指定 `NEWLINE` 选项，并将其值分别设置为 `CR`、`CRLF` 或对应的字节码字符集。

有关格式化器选项的更多信息，请参阅 Apache Cloudberry 定宽自定义格式化器文档。

## 示例：读取 S3 上的定宽文本数据 {#example-reading-fixed-width-text-data-on-s3}

执行以下步骤创建示例文本文件，将该文件复制到 S3，并使用 `s3:fixedwidth` Profile 创建 PXF 外部表来查询数据。

要运行此示例，必须：

- 在系统上安装 AWS CLI 工具
- 知道 AWS 访问 ID 和密钥
- 对某个 S3 存储桶具有写权限

步骤：

1. 在 S3 中为 PXF 示例数据文件创建一个目录。例如，如果对名为 `BUCKET` 的 S3 存储桶具有写权限：

    ```shell
    $ aws s3 mb s3://BUCKET/pxf_examples
    ```
1. 在本地创建名为 `pxf_s3_fixedwidth.txt` 的纯文本数据文件：

    ```shell
    $ echo 'Prague         Jan 101   4875.33   
    Rome           Mar 87    1557.39   
    Bangalore      May 317   8936.99   
    Beijing        Jul 411   11600.67  ' > /tmp/pxf_s3_fixedwidth.txt
    ```

    在此示例文件中，第一个字段长 15 个字符，第二个字段长 4 个字符，第三个字段长 6 个字符，最后一个字段长 10 个字符。

    > **注意** 请在所选的编辑器中打开 `/tmp/pxf_s3_fixedwidth.txt` 文件，并确保最后一个字段在右侧以空格填充至 10 个字符的大小。

1. 将数据文件复制到第 1 步中创建的 S3 目录：

    ```shell
    $ aws s3 cp /tmp/pxf_s3_fixedwidth.txt s3://BUCKET/pxf_examples/
    ```

1. 验证该文件现已位于 S3 中：

    ```shell
    $ aws s3 ls s3://BUCKET/pxf_examples/pxf_s3s_fixedwidth.txt
    ```

1. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

1. 使用 PXF `s3:fixedwidth` Profile 创建 Apache Cloudberry 外部表，引用刚刚创建并添加到 S3 的 `pxf_s3_fixedwidth.txt` 文件。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_fixedwidth_r(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://data/pxf_examples/pxf_s3_fixedwidth.txt?PROFILE=s3:fixedwidth&SERVER=s3srvcfg&NEWLINE=CRLF')
               FORMAT 'CUSTOM' (formatter='fixedwidth_in', location='15', month='4', num_orders='6', total_sales='10', line_delim=E'\r\n');
    ```
              
2. 查询该外部表：

    ```sql
    postgres=# SELECT * FROM pxf_s3_fixedwidth_r;
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

## 写入定宽文本数据 {#writing-fixed-width-text-data}

`<objstore>:fixedwidth` Profile 支持将定宽文本写入对象存储。使用 PXF 创建可写外部表时，需要指定一个目录的名称。向可写外部表插入记录时，所插入的数据块将写入所指定目录中的一个或多个文件。

**注意**：使用可写 Profile 创建的外部表只能用于 `INSERT` 操作。如果要查询所插入的数据，必须另外创建引用该目录的可读外部表。

使用以下语法创建引用对象存储目录的 Apache Cloudberry 可写外部表：

```sql
CREATE WRITABLE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-dir>
    ?PROFILE=<objstore>:fixedwidth[&SERVER=<server_name>][&NEWLINE=<bytecode>][&<write-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='fixedwidth_out' [, <field_name>='<width>'] [, ...] [, line_delim[=|<space>][E]'<delim_value>']);
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;dir\>    | 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:fixedwidth | `PROFILE` 必须标明具体的对象存储。例如 `s3:fixedwidth`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。未指定时，PXF 使用 `default` 服务器。 |
| NEWLINE=\<bytecode\>    | 当 `line_delim` 格式化器选项包含 `\r`、`\r\n` 或一组自定义转义字符时，必须将 `<bytecode>` 分别设置为 `CR`、`CRLF` 或对应的字节码字符集。 |
| \<write&#8209;option\>=\<value\>  | \<write-option\> 如下所述。|
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `FORMATTER='fixedwidth_out'`（写）配合使用。 |
| \&lt;field_name&gt;='\&lt;width&gt;'    | 字段的名称和宽度。例如：`first_name='15'` 指定 `first_name` 字段长度为 `15` 个字符。默认情况下，写入外部文件时，如果字段值小于 `<width>` 大小，Apache Cloudberry 会在字段右侧以空格填充至 `<width>` 大小。 |
| line_delim    | 数据中的行分隔符字符。当值为转义序列时，在 \<delim_value\> 前加上 `E`。示例：`line_delim=E'\n'`、`line_delim 'aaa'`。默认值为 `'\n'`。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间额外的数据移动。 |

使用 `<objstore>:fixedwidth` Profile 创建的可写外部表可以选择使用记录压缩或块压缩。压缩编解码器通过 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中的选项指定：

| 写入选项  | 值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入定宽文本数据时支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |

## 示例：向 S3 写入定宽文本数据 {#example-writing-fixed-width-text-data-to-s3}

此示例使用[示例：读取 S3 上的定宽文本数据](#example-reading-fixed-width-text-data-on-s3)中介绍的数据模式。

| 列名  | 宽度 | 数据类型 |
|-------|-------|-------|
| location | 15 | text |
| month | 4 | text |
| number_of_orders | 6 | int |
| total_sales | 10 | float8 |

#### 步骤 {#procedure}

执行以下步骤，利用与上述相同的数据模式创建 Apache Cloudberry 可写外部表。您将使用 PXF `s3:fixedwidth` Profile 向 S3 写入数据，并另外创建一个可读外部表来读取写入 #3 的数据。

1. 利用上述数据模式创建 Apache Cloudberry 可写外部表，写入 S3 目录 `BUCKET/pxf_examples/fixedwidth_write`。创建表时指定 `\n` 作为行分隔符。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_s3_fixedwidth_w(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://BUCKET/pxf_examples/fixedwidth_write?PROFILE=s3:fixedwidth&SERVER=s3srvcfg')
               FORMAT 'CUSTOM' (formatter='fixedwidth_out', location='15', month='4', num_orders='6', total_sales='10');
    ```
    
2. 对 `pxf_s3_fixedwidth_w` 表使用 `INSERT` 命令，向 `fixedwidth_write` S3 目录写入几条单独的记录：

    ```sql
    postgres=# INSERT INTO pxf_s3_fixedwidth_w VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    postgres=# INSERT INTO pxf_s3_fixedwidth_w VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

5. Apache Cloudberry 不支持直接查询可写外部表。要查询刚刚添加到 S3 的数据，必须创建引用该 S3 目录的 Apache Cloudberry 可读外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_fixedwidth_r2(location text, month text, num_orders int, total_sales float8)
                 LOCATION ('pxf://BUCKET/pxf_examples/fixedwidth_write?PROFILE=s3:fixedwidth&SERVER=s3srvcfg')
               FORMAT 'CUSTOM' (formatter='fixedwidth_in', location='15', month='4', num_orders='6', total_sales='10');
    ```

6. 查询该可读外部表：

    ```sql
    postgres=# SELECT * FROM pxf_s3_fixedwidth_r2 ORDER BY total_sales;
    ```

    ```text
     location  | month | num_orders | total_sales 
    -----------+-------+------------+-------------
     Frankfurt | Mar   |        777 |     3956.98
     Cleveland | Oct   |       3812 |    96645.37
    (2 rows)
    ```
