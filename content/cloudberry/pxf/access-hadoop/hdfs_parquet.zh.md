---
title: "读写 HDFS Parquet 数据"
description: "通过 PXF 读写 HDFS 中的 Parquet 数据。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_parquet.md"
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

使用 PXF HDFS 连接器读写 Parquet 格式的数据。本节介绍如何读写以 Parquet 格式存储的 HDFS 文件，包括如何创建引用 HDFS 数据存储中文件的外部表、对其进行查询以及向其中插入数据。

PXF 支持读取或写入使用以下编解码器压缩的 Parquet 文件：`snappy`、`gzip`、'lz4_raw' 和 `zstd`。

PXF 目前仅支持读写 Parquet 的基本数据类型。


## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据或向 HDFS 写入数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。


## 数据类型映射 {#data-type-mapping}

要在 Apache Cloudberry 中读写 Parquet 基本数据类型，请将 Parquet 数据值映射到相同类型的 Apache Cloudberry 列。

Parquet 支持一小组基本数据类型，并使用元数据注解来扩展其支持的数据类型。这些注解指定如何解释基本类型。例如，Parquet 将 `INTEGER` 和 `DATE` 类型都存储为 `INT32` 基本类型，并通过注解将原始类型标识为 `DATE`。

### 读映射 {#read-mapping}

<a id="p2g_type_mapping_table"></a>

读取 Parquet 数据时，PXF 使用以下数据类型映射：

| Parquet 物理类型 | Parquet 逻辑类型 | PXF/Cloudberry 数据类型 |
|-------------------|---------------|--------------------------|
| boolean | -- | Boolean |
| binary (byte\_array) | -- | Bytea |
| binary (byte\_array) | Date | Date |
| binary (byte\_array) | Timestamp_millis | Timestamp |
| binary (byte\_array) | UTF8 | Text |
| double | -- | Float8 |
| fixed\_len\_byte\_array | Decimal | Numeric |
| float | -- | Real |
| int32 | int_8 | Smallint |
| int32 | Date | Date |
| int32 | Decimal | Numeric |
| int32 | -- | Integer |
| int64 | Decimal | Numeric |
| int64 | -- | Bigint |
| int96 | -- | Timestamp |

**注意**：PXF 支持对上面列出的所有 parquet 数据类型进行过滤谓词下推，但 `fixed_len_byte_array` 和 `int96` 类型*除外*。

当 Parquet `LIST` 嵌套类型表示某些 Parquet 类型的一维数组时，PXF 可以读取该类型。支持的映射如下：

| Parquet 数据类型 | PXF/Cloudberry 数据类型 |
|-------------------|-------------------------|
| 元素类型为 \&lt;boolean&gt; 的列表 | Boolean[] |
| 元素类型为 \&lt;binary&gt; 的列表 | Bytea[] |
| 元素类型为 \&lt;binary&gt; (Date) 的列表 | Date[] |
| 元素类型为 \&lt;binary&gt; (Timestamp_millis) 的列表 | Timestamp[] |
| 元素类型为 \&lt;binary&gt; (UTF8) 的列表 | Text[] |
| 元素类型为 \&lt;double&gt; 的列表 | Float8[] |
| 元素类型为 \<fixed\_len\_byte\_array> (Decimal) 的列表 | Numeric[] |
| 元素类型为 \&lt;float&gt; 的列表 | Real[] |
| 元素类型为 \&lt;int32&gt; (int_8) 的列表 | Smallint[] |
| 元素类型为 \&lt;int32&gt; (Date) 的列表 | Date[] |
| 元素类型为 \&lt;int32&gt; (Decimal) 的列表 | Numeric[] |
| 元素类型为 \&lt;int32&gt; 的列表 | Integer[] |
| 元素类型为 \&lt;int64&gt; (Decimal) 的列表 | Numeric[] |
| 元素类型为 \&lt;int64&gt; 的列表 | Bigint[] |
| 元素类型为 \&lt;int96&gt; 的列表 | Timestamp[] |


### 写映射 {#write-mapping}

写入 Parquet 数据时，PXF 使用以下数据类型映射：

| PXF/Cloudberry 数据类型 | Parquet 物理类型 | Parquet 逻辑类型 |
|-------------------|---------------|--------------------------|
| Bigint | int64 | -- |
| Boolean | boolean | -- |
| Bpchar<sup>1</sup> |  binary (byte\_array) | UTF8 |
| Bytea | binary (byte\_array) | -- |
| Date |  int32 | Date |
| Float8 | double | -- |
| Integer | int32 | -- |
| Numeric/Decimal | fixed\_len\_byte\_array | Decimal |
| Real | float | -- |
| SmallInt | int32 | int\_8 |
| Text | binary (byte\_array) | UTF8 |
| Timestamp<sup>2</sup> | int96 | -- |
| Timestamptz<sup>3</sup> | int96 | -- |
| Varchar | binary (byte\_array) | UTF8 |
| 其他类型 | 不支持 | -- |

<br/><sup>1</sup>&nbsp;由于 Parquet 不保存字段长度，PXF 写入 Parquet 的 Bpchar 将成为长度未定义的 text。
<br/><sup>2</sup>&nbsp;PXF 会将 `Timestamp` 本地化为当前系统时区，并先转换为通用时间（UTC），最后再转换为 `int96`。
<br/><sup>3</sup>&nbsp;PXF 会将 `Timestamptz` 转换为 UTC `timestamp`，然后再转换为 `int96`。在此转换过程中，PXF 会丢失时区信息。

PXF 可以写入某些 Parquet 数据类型的一维 `LIST`。支持的映射如下：

| PXF/Cloudberry 数据类型 |  Parquet 数据类型 |
|-------------------|--------------------------|
| Bigint[] | 元素类型为 \&lt;int64&gt; 的列表 |
| Boolean[] | 元素类型为 \&lt;boolean&gt; 的列表 |
| Bpchar[]<sup>1</sup> |  元素类型为 \&lt;binary&gt; (UTF8) 的列表 |
| Bytea[] | 元素类型为 \&lt;binary&gt; 的列表 |
| Date[] | 元素类型为 \&lt;int32&gt; (Date) 的列表 |
| Float8[] | 元素类型为 \&lt;double&gt; 的列表 |
| Integer[] | 元素类型为 \&lt;int32&gt; 的列表 |
| Numeric[]/Decimal[] | 元素类型为 \<fixed\_len\_byte\_array> (Decimal) 的列表 |
| Real[] | 元素类型为 \&lt;float&gt; 的列表 |
| SmallInt[] | 元素类型为 \&lt;int32&gt; (int_8) 的列表 |
| Text[] |  元素类型为 \&lt;binary&gt; (UTF8) 的列表 |
| Timestamp[]<sup>2</sup> | 元素类型为 \&lt;int96&gt; 的列表 |
| Timestamptz[]<sup>3</sup> | 元素类型为 \&lt;int96&gt; 的列表 |
| Varchar[] | 元素类型为 \&lt;binary&gt; (UTF8) 的列表 |
| 其他类型 | 不支持 |

### 关于 Parquet 模式与数据 {#about-parquet-schemas-and-data}

Parquet 是一种列式存储格式。Parquet 数据文件包含数据的紧凑二进制表示。*模式*定义数据的结构，由上文数据类型映射一节中所列的同样的基本类型和复杂类型组成。

Parquet 数据文件包含内嵌的模式。您可以通过 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中的 `SCHEMA` 自定义选项（见下文），选择提供 PXF 向 HDFS 写入数据时所使用的模式：

| 外部表类型  | 是否指定 `SCHEMA`？ | 行为 |
|-------|--------------------------|-----------|
| 可写   | 是 | PXF 使用指定的模式。 |
| 可写   | 否 | PXF 根据外部表定义创建 Parquet 模式。 |

向 PXF 提供 Parquet 模式文件时，必须指定该文件的绝对路径，并且该文件必须位于 Hadoop 文件系统上。

## 创建外部表 {#creating-the-external-table}

PXF HDFS 连接器的 `hdfs:parquet` Profile 支持读写 Parquet 格式的 HDFS 数据。向可写外部表插入记录时，所插入的数据块会被写入您所指定目录中的一个或多个文件。

使用以下语法创建引用 HDFS 目录的 Apache Cloudberry 外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-dir>
    ?PROFILE=hdfs:parquet[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:parquet`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>  | 下文介绍 \<custom-option\>。|
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间的额外数据移动。 |


## 创建外表 {#creating-the-foreign-table}

PXF HDFS 的 `hdfs_pxf_fdw` 外部数据包装器支持读写 Parquet 格式的 HDFS 文件。向外表插入记录时，所插入的数据块会被写入 `resource` 子句中指定目录里的文件，每个 Segment 写入一个文件。

使用以下语法创建引用 HDFS 文件或目录的 Apache Cloudberry 外表：

```sql
CREATE SERVER <foreign_server> FOREIGN DATA WRAPPER hdfs_pxf_fdw;
CREATE USER MAPPING FOR <user_name> SERVER <foreign_server>;

CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
  SERVER <foreign_server>
  OPTIONS ( resource '<path-to-file>', format 'parquet' [, <custom-option> '<value>'[...]]);
```

Apache Cloudberry [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 命令中使用的具体关键字和取值说明如下。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<foreign_server\>    | PXF 用于访问数据的命名服务器配置。您可以按照[为外表覆盖 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-foreign-tables)中的说明，在 `CREATE SERVER` 语句中覆盖凭据。 |
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| format    | 文件格式；对于 Parquet 格式的数据，指定为 `'parquet'`。 |
| \<custom-option\>    | 下文介绍 \<custom-option\>。 |

### 自定义选项 {#custom-options}

PXF `hdfs:parquet` Profile 支持以下读选项：

| 读选项  | 取值说明 |
|-------|-------------------------------------|
| IGNORE_MISSING_PATH | 布尔值，指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |

PXF `hdfs:parquet` Profile 支持与编码和压缩相关的写选项。这些写选项在 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中指定。`hdfs:parquet` Profile 支持以下自定义写选项：

| 写选项  | 取值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入 Parquet 数据时支持的压缩编解码器包括：`snappy`、`gzip`、`lz4_raw`、`zstd` 和 `uncompressed`。如果未提供此选项，PXF 使用 `snappy` 压缩数据。 |
| ROWGROUP_SIZE | Parquet 文件由一个或多个行组组成，行组是将数据按行进行的逻辑划分。`ROWGROUP_SIZE` 标识行组的大小（以字节为单位）。默认的行组大小为 `8 * 1024 * 1024` 字节。 |
| PAGE_SIZE | 行组由列块组成，列块又被划分为页。`PAGE_SIZE` 是此类页的大小（以字节为单位）。默认的页大小为 `1 * 1024 * 1024` 字节。 |
| ENABLE\_DICTIONARY | 布尔值，指定是否启用字典编码。默认值为 `true`；PXF 写入 Parquet 文件时启用字典编码。 |
| DICTIONARY\_PAGE\_SIZE | 启用字典编码时，每个行组中的每一列有一个字典页。`DICTIONARY_PAGE_SIZE` 与 `PAGE_SIZE` 类似，但针对字典页。默认的字典页大小为 `1 * 1024 * 1024` 字节。 |
| PARQUET_VERSION | Parquet 版本；PXF 为此选项支持取值 `v1` 和 `v2`。默认的 Parquet 版本为 `v1`。 |
| SCHEMA | Parquet 模式文件在 Cloudberry PXF 主机上或 HDFS 上的绝对路径。 |

**注意**：如果不希望 PXF 压缩数据，必须显式指定 `uncompressed`。

使用 PXF 写入 HDFS 的 Parquet 文件采用以下命名格式：`<file>.<compress_extension>.parquet`，例如 `1547061635-0000004417_0.gz.parquet`。

## 示例 {#example}

此示例使用[示例：读取 HDFS 上的文本数据](/cloudberry/pxf/access-hadoop/hdfs_text/#example-reading-text-data-on-hdfs)中介绍的数据模式，并新增一列 `item_quantity_per_order`。该列是长度等于 `number_of_orders` 的数组，用于标识每个订单中的商品数量。

| 列名  | 数据类型 |
|-------|-------------------------------------|
| location | text |
| month | text |
| number\_of\_orders | int |
| item\_quantity\_per\_order | int[] |
| total\_sales | float8 |

在此示例中，您将创建一个 Parquet 格式的可写外部表，该表使用默认 PXF 服务器引用 HDFS 中 Parquet 格式的数据；向该表中插入一些数据，然后创建一个可读外部表来读取这些数据。

1. Apache Cloudberry 不支持对同一个外部表既读又写。请创建两个表——一个用于读，一个用于写，二者引用同一个 HDFS 目录：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_tbl_parquet (location text, month text, number_of_orders int, item_quantity_per_order int[], total_sales double precision)
        LOCATION ('pxf://data/pxf_examples/pxf_parquet?PROFILE=hdfs:parquet')
      FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');

    postgres=# CREATE EXTERNAL TABLE read_pxf_parquet(location text, month text, number_of_orders int, item_quantity_per_order int[], total_sales double precision)
        LOCATION ('pxf://data/pxf_examples/pxf_parquet?PROFILE=hdfs:parquet')
      FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    或者创建单个外表来同时进行读写操作：

    ```
        testdb=# CREATE SERVER example_parquet FOREIGN DATA WRAPPER hdfs_pxf_fdw;
        testdb=# CREATE USER MAPPING FOR CURRENT_USER SERVER example_parquet;
        testdb=# CREATE FOREIGN TABLE pxf_tbl_parquet(location text, month text, number_of_orders int, item_quantity_per_order int[], total_sales double precision)
                   SERVER example_parquet
                   OPTIONS (
                   	resource 'data/pxf_examples/pxf_parquet',
                   	format 'parquet'
                   );
    ```

2. 直接向 `pxf_tbl_parquet` 表插入数据，向 HDFS 目录 `pxf_parquet` 写入几条记录。例如：

    ```sql
    postgres=# INSERT INTO pxf_tbl_parquet VALUES ( 'Frankfurt', 'Mar', 3, '{1,11,111}', 3956.98 );
    postgres=# INSERT INTO pxf_tbl_parquet VALUES ( 'Cleveland', 'Oct', 2, '{3333,7777}', 96645.37 );
    ```

3. 查询可读外部表 `read_pxf_parquet`：

    ```sql
    postgres=# SELECT * FROM read_pxf_parquet ORDER BY total_sales;
    ```
    ```text
     location  | month | number_of_orders | item_quantity_per_order | total_sales
    -----------+-------+------------------+-------------------------+-------------
     Frankfurt | Mar   |              777 | {1,11,111}              |     3956.98
     Cleveland | Oct   |             3812 | {3333,7777}             |    96645.4
    (2 rows)
    ```

    或者查询同一个外表 `pxf_tbl_parquet`：

    ```sql
    postgres=# SELECT * FROM pxf_tbl_parquet ORDER BY total_sales;
    ```
    ```text
     location  | month | number_of_orders | item_quantity_per_order | total_sales
    -----------+-------+------------------+-------------------------+-------------
     Frankfurt | Mar   |              777 | {1,11,111}              |     3956.98
     Cleveland | Oct   |             3812 | {3333,7777}             |    96645.4
    (2 rows)
    ```

## 了解写入数值数据时的溢出情况 {#understanding-overflow-conditions-when-writing-numeric-data}

PXF 使用 `HiveDecimal` 类写入 Parquet 数值数据。`HiveDecimal` 将数值类型的精度（precision）和标度（scale）都限制为最大 38。

在外部表中定义 `NUMERIC` 列而不指定精度或标度时，PXF 在内部将该列映射为 `DECIMAL(38, 18)`。

PXF 处理以下精度溢出情况：

- 您在外部表中定义了 `NUMERIC` 列，并且某个值的整数位数超过了所支持的最大精度 38。例如 `1234567890123456789012345678901234567890.12345`，其整数位数为 45。
- 您定义了 `NUMERIC(<precision>)` 列，且 `<precision>` 大于 38。例如 `NUMERIC(55)`。
- 您在外部表中定义了 `NUMERIC` 列，并且某个值的整数位数大于 20（38-18）。例如 `123456789012345678901234567890.12345`，其整数位数为 30。

如果您定义了 `NUMERIC(<precision>, <scale>)` 列，并且某个值的整数位数大于 `<precision> - <scale>`，PXF 会返回错误。例如，您定义了 `NUMERIC(20,4)` 列，而值为 `12345678901234567.12`，其整数位数为 19，大于 20-4=16。

向 Parquet 文件写入数值数据时，PXF 在检测到溢出后可以采取三种操作之一：对值进行舍入（默认）、返回错误或忽略溢出。`pxf-site.xml` 服务器配置中的 `pxf.parquet.write.decimal.overflow` 属性控制 PXF 在这种情况下的操作；该属性的有效取值如下：

| 值  | PXF 操作 |
|-------|-------------------------------------|
| `round` | PXF 遇到溢出时，会尝试在写入前对值进行舍入，以同时满足精度和标度要求。如果舍入失败，PXF 报告错误。这可能会在外部系统中留下不完整的数据集。`round` 为默认值。 |
| `error` | PXF 遇到溢出时报告错误，事务失败。 |
| `ignore` | PXF 尝试对值进行舍入，以同时满足精度和标度要求；否则 PXF 写入 NULL 值。（这是 6.6.0 版本之前 PXF 的行为。） |

当 PXF 检测到溢出且 `pxf.parquet.write.decimal.overflow` 属性设置为 `ignore` 时，PXF 会记录一条警告。
