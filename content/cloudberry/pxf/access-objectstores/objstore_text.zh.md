---
title: "读写对象存储中的文本数据"
description: "通过 PXF 读写对象存储中的文本数据。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_text.md"
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

PXF 对象存储连接器支持普通分隔符文本和逗号分隔值（CSV）格式的文本数据。本节介绍如何使用 PXF 访问对象存储中的文本数据，包括如何创建、查询引用对象存储中文件的外部表，以及如何向其中插入数据。

**注意**：从对象存储访问文本数据与在 HDFS 中访问文本数据非常相似。

## 前提条件 {#prerequisites}

在尝试从对象存储读取数据或向对象存储写入数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 读取文本数据 {#reading-text-data}

从对象存储读取每行为一条记录的普通分隔符文本时，使用 `<objstore>:text` Profile；读取 .csv 数据时，使用 `<objstore>:csv`。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

以下语法创建引用对象存储中简单文本文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:text|csv&SERVER=<server_name>[&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>][&<custom-option>=<value>[...]]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:text<br/> PROFILE=\<objstore\>:csv    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:text`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片（fragment）。 |
| SKIP_HEADER_COUNT=\<numlines\> | 指定在读取数据之前，PXF 在每个 \<file\> 的第一个分片（split）中应跳过的标题行数。默认值为 0，即不跳过任何行。 |
| FORMAT | 当 \<path-to-file\> 引用普通分隔符文本数据时，使用 `FORMAT` `'TEXT'`。<br/> 当 \<path-to-file\> 引用逗号分隔值数据时，使用 `FORMAT` `'CSV'`。 |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当值为转义序列时，在 \<delim_value\> 前加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。如果文本文件包含标题行，请使用 `SKIP_HEADER_COUNT` 指定 PXF 应在每个文件第一个分片的开头跳过的行数。

如果访问的是 S3 对象存储：

- 可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

- 如果从 S3 读取 CSV 格式数据，可以指示 PXF 使用 Amazon S3 Select 服务检索数据。有关用于此目的的 PXF 自定义选项的更多信息，请参阅[使用 Amazon S3 Select 服务](/cloudberry/pxf/access-objectstores/access_s3/#using-the-amazon-s3-select-service)。

### 示例：从 S3 读取文本数据 {#example-reading-text-data-from-s3}

执行以下步骤创建示例文本文件，将该文件复制到 S3，并使用 `s3:text` 和 `s3:csv` Profile 创建两个 PXF 外部表来查询数据。

要运行此示例，必须：

- 在系统上安装 AWS CLI 工具
- 知道 AWS 访问 ID 和密钥
- 对某个 S3 存储桶具有写权限

1. 在 S3 中为 PXF 示例数据文件创建一个目录。例如，如果对名为 `BUCKET` 的 S3 存储桶具有写权限：

    ```shell
    $ aws s3 mb s3://BUCKET/pxf_examples
    ```

2. 在本地创建名为 `pxf_s3_simple.txt` 的分隔符纯文本数据文件：

    ```shell
    $ echo 'Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67' > /tmp/pxf_s3_simple.txt
    ```

    请注意，这里使用逗号（`,`）分隔四个数据字段。

4. 将数据文件复制到第 1 步中创建的 S3 目录：

    ```shell
    $ aws s3 cp /tmp/pxf_s3_simple.txt s3://BUCKET/pxf_examples/
    ```

5. 验证该文件现已位于 S3 中：

    ```shell
    $ aws s3 ls s3://BUCKET/pxf_examples/pxf_s3_simple.txt
    ```

4. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

1. 使用 PXF `s3:text` Profile 创建 Apache Cloudberry 外部表，引用刚刚创建并添加到 S3 的 `pxf_s3_simple.txt` 文件。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_textsimple(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://BUCKET/pxf_examples/pxf_s3_simple.txt?PROFILE=s3:text&SERVER=s3srvcfg')
              FORMAT 'TEXT' (delimiter=E',');
    ```
              
2. 查询该外部表：

    ```sql
    postgres=# SELECT * FROM pxf_s3_textsimple;          
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

2. 创建引用 `pxf_s3_simple.txt` 的第二个外部表，这次指定 `s3:csv` `PROFILE` 和 `CSV` `FORMAT`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_textsimple_csv(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://BUCKET/pxf_examples/pxf_s3_simple.txt?PROFILE=s3:csv&SERVER=s3srvcfg')
              FORMAT 'CSV';
    postgres=# SELECT * FROM pxf_s3_textsimple_csv;          
    ```

    对逗号分隔值数据指定 `FORMAT 'CSV'` 时，无需 `delimiter` 格式化器选项，因为逗号是默认的分隔符值。

## 读取含引号换行符的文本数据 {#reading-text-data-with-quoted-linefeeds}

使用 `<objstore>:text:multi` Profile 读取包含嵌入（带引号）换行符的、以分隔符分隔的单行或多行记录的普通文本数据。以下语法创建引用对象存储中此类文本文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:text:multi&SERVER=<server_name>[&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>][&<custom-option>=<value>[...]]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:text:multi    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:text:multi`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片（fragment）。 |
| SKIP_HEADER_COUNT=\<numlines\> | 指定在读取数据之前，PXF 在每个 \<file\> 的第一个分片（split）中应跳过的标题行数。默认值为 0，即不跳过任何行。 |
| FORMAT | 当 \<path-to-file\> 引用普通分隔符文本数据时，使用 `FORMAT` `'TEXT'`。<br/> 当 \<path-to-file\> 引用逗号分隔值数据时，使用 `FORMAT` `'CSV'`。 |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当值为转义序列时，在 \<delim_value\> 前加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。如果文本文件包含标题行，请使用 `SKIP_HEADER_COUNT` 指定 PXF 应在每个文件第一个分片的开头跳过的行数。

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

### 示例：从 S3 读取多行文本数据 {#example-reading-multi-line-text-data-from-s3}

执行以下步骤创建示例文本文件，将该文件复制到 S3，并使用 PXF `s3:text:multi` Profile 创建 Apache Cloudberry 可读外部表来查询数据。

要运行此示例，必须：

- 在系统上安装 AWS CLI 工具
- 知道 AWS 访问 ID 和密钥
- 对某个 S3 存储桶具有写权限

1. 创建第二个分隔符纯文本文件：

    ```shell
    $ vi /tmp/pxf_s3_multi.txt
    ```

2. 将以下数据复制/粘贴到 `pxf_s3_multi.txt` 中：

    ```text
    "4627 Star Rd.
    San Francisco, CA  94107":Sept:2017
    "113 Moon St.
    San Diego, CA  92093":Jan:2018
    "51 Belt Ct.
    Denver, CO  90123":Dec:2016
    "93114 Radial Rd.
    Chicago, IL  60605":Jul:2017
    "7301 Brookview Ave.
    Columbus, OH  43213":Dec:2018
    ```

    请注意，这里使用冒号 `:` 分隔三个字段。另请注意第一个（地址）字段两侧的引号。该字段包含一个嵌入的换行符，用于将街道地址与城市和州分隔开。

3. 将文本文件复制到 S3：

    ```shell
    $ aws s3 cp /tmp/pxf_s3_multi.txt s3://BUCKET/pxf_examples/
    ```

4. 使用 `s3:text:multi` Profile 创建引用 S3 文件 `pxf_s3_multi.txt` 的外部表，并确保将 `:`（冒号）标明为字段分隔符。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_textmulti(address text, month text, year int)
                LOCATION ('pxf://BUCKET/pxf_examples/pxf_s3_multi.txt?PROFILE=s3:text:multi&SERVER=s3srvcfg')
              FORMAT 'CSV' (delimiter ':');
    ```
    
    请注意指定 `delimiter` 的另一种语法。
    
2. 查询 `pxf_s3_textmulti` 表：

    ```sql
    postgres=# SELECT * FROM pxf_s3_textmulti;
    ```

    ```text
             address          | month | year 
    --------------------------+-------+------
     4627 Star Rd.            | Sept  | 2017
     San Francisco, CA  94107           
     113 Moon St.             | Jan   | 2018
     San Diego, CA  92093               
     51 Belt Ct.              | Dec   | 2016
     Denver, CO  90123                  
     93114 Radial Rd.         | Jul   | 2017
     Chicago, IL  60605                 
     7301 Brookview Ave.      | Dec   | 2018
     Columbus, OH  43213                
    (5 rows)
    ```

## 写入文本数据 {#writing-text-data}

`<objstore>:text|csv` Profile 支持将单行普通文本数据写入对象存储。使用 PXF 创建可写外部表时，需要指定一个目录的名称。向可写外部表插入记录时，所插入的数据块将写入所指定目录中的一个或多个文件。

**注意**：使用可写 Profile 创建的外部表只能用于 `INSERT` 操作。如果要查询所插入的数据，必须另外创建引用该目录的可读外部表。

使用以下语法创建引用对象存储目录的 Apache Cloudberry 可写外部表：

```sql
CREATE WRITABLE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-dir>
    ?PROFILE=<objstore>:text|csv&SERVER=<server_name>[&<custom-option>=<value>[...]]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;dir\>    | 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:text<br/> PROFILE=\<objstore\>:csv    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:text`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| \<custom&#8209;option\>=\<value\>  | \<custom-option\> 如下所述。|
| FORMAT | 使用 `FORMAT` `'TEXT'` 向 \<path-to-dir\> 写入以分隔符分隔的普通文本。<br/> 使用 `FORMAT` `'CSV'` 向 \<path-to-dir\> 写入逗号分隔值文本。 |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当值为转义序列时，在 \<delim_value\> 前加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间额外的数据移动。 |

使用 `<objstore>:text|csv` Profile 创建的可写外部表可以选择使用记录压缩或块压缩。压缩编解码器通过 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中的自定义选项指定。`<objstore>:text|csv` Profile 支持以下自定义写入选项：

| 选项  | 值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入文本数据时支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

### 示例：向 S3 写入文本数据 {#example-writing-text-data-to-s3}

此示例使用[示例：从 S3 读取文本数据](#example-reading-text-data-from-s3)中介绍的数据模式。

| 列名  | 数据类型 |
|-------|-------------------------------------|
| location | text |
| month | text |
| number\_of\_orders | int |
| total\_sales | float8 |

此示例还可以选择使用在该练习中创建的名为 `pxf_s3_textsimple` 的 Apache Cloudberry 外部表。

#### 步骤 {#procedure}

执行以下步骤，利用与上述相同的数据模式创建 Apache Cloudberry 可写外部表，其中一个将使用压缩。您将使用 PXF `s3:text` Profile 向 S3 写入数据，并另外创建一个可读外部表来读取写入 S3 的数据。

1. 利用上述数据模式创建 Apache Cloudberry 可写外部表，写入 S3 目录 `BUCKET/pxf_examples/pxfwrite_s3_textsimple1`。创建表时指定逗号（`,`）作为分隔符。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_s3_writetbl_1(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://BUCKET/pxf_examples/pxfwrite_s3_textsimple1?PROFILE=s3:text|csv&SERVER=s3srvcfg')
              FORMAT 'TEXT' (delimiter=',');
    ```
    
    将 `FORMAT` 子句的 `delimiter` 值指定为单个 ASCII 逗号字符 `,`。

2. 对 `pxf_s3_writetbl_1` 调用 SQL `INSERT` 命令，向 `pxfwrite_s3_textsimple1` S3 目录写入几条单独的记录：

    ```sql
    postgres=# INSERT INTO pxf_s3_writetbl_1 VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    postgres=# INSERT INTO pxf_s3_writetbl_1 VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

3. （可选）将在[示例：从 S3 读取文本数据](#example-reading-text-data-from-s3)中创建的 `pxf_s3_textsimple` 表中的数据插入 `pxf_s3_writetbl_1`：

    ```sql
    postgres=# INSERT INTO pxf_s3_writetbl_1 SELECT * FROM pxf_s3_textsimple;
    ```

5. Apache Cloudberry 不支持直接查询可写外部表。要查询刚刚添加到 S3 的数据，必须创建引用该 S3 目录的 Apache Cloudberry 可读外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_s3_textsimple_r1(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://BUCKET/pxf_examples/pxfwrite_s3_textsimple1?PROFILE=s3:text&SERVER=s3srvcfg')
			    FORMAT 'CSV';
    ```

    创建可读外部表时指定 `'CSV'` `FORMAT`，是因为创建可写表时使用了逗号（`,`）作为分隔符字符，而这正是 `'CSV'` `FORMAT` 的默认分隔符。

6. 查询该可读外部表：

    ```sql
    postgres=# SELECT * FROM pxf_s3_textsimple_r1 ORDER BY total_sales;
    ```

    ```text
     location  | month | num_orders | total_sales 
    -----------+-------+------------+-------------
     Rome      | Mar   |         87 |     1557.39
     Frankfurt | Mar   |        777 |     3956.98
     Prague    | Jan   |        101 |     4875.33
     Bangalore | May   |        317 |     8936.99
     Beijing   | Jul   |        411 |    11600.67
     Cleveland | Oct   |       3812 |    96645.37
    (6 rows)
    ```

    `pxf_s3_textsimple_r1` 表包含单独插入的记录；如果执行了可选步骤，还包含 `pxf_s3_textsimple` 表的全部内容。

7. 创建第二个 Apache Cloudberry 可写外部表，这次使用 Gzip 压缩，并采用冒号 `:` 作为分隔符：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_s3_writetbl_2 (location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://BUCKET/pxf_examples/pxfwrite_s3_textsimple2?PROFILE=s3:text&SERVER=s3srvcfg&COMPRESSION_CODEC=gzip')
              FORMAT 'TEXT' (delimiter=':');
    ```

8. 直接向 `pxf_s3_writetbl_2` 表插入数据，向 `pxfwrite_s3_textsimple2` S3 目录写入几条记录：

    ```sql
    gpadmin=# INSERT INTO pxf_s3_writetbl_2 VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    gpadmin=# INSERT INTO pxf_s3_writetbl_2 VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

9. 要查询新建的名为 `pxfwrite_s3_textsimple2` 的 S3 目录中的数据，可以按上文所述创建引用该 S3 目录的 Apache Cloudberry 可读外部表，并指定 `FORMAT 'CSV' (delimiter=':')`。


## 关于读取包含多字节或多字符分隔符的数据 {#about-reading-data-containing-multi-byte-or-multi-character-delimiters}

要从对象存储读取包含多字节分隔符或多字符分隔符的数据，只能使用 `*:csv` PXF Profile。为此类数据创建可读外部表的语法如下：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:csv[&SERVER=<server_name>][&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>][&NEWLINE=<bytecode>]')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import' <option>[=|<space>][E]'<value>');
```

请注意语法块中的 `FORMAT` 行。虽然语法与读取 CSV 的语法相似，但 PXF 需要自定义格式化器来读取包含多字节分隔符或多字符分隔符的数据。必须指定 `'CUSTOM'` 格式和 `pxfdelimited_import` 格式化器，还必须在格式化器选项中指定分隔符。

从对象存储读取包含多字节分隔符或多字符分隔符的数据时，PXF 识别以下格式化器选项：

| 选项名称  | 值说明 | 默认值 |
|-------|---------------|---------------|
| DELIMITER=\<delim_string\> | 分隔列的单字节或多字节分隔符字符串。该字符串长度最多为 32 字节，且不得包含引号或转义字符。**必需** | 无 |
| QUOTE=\<char\> | 适用于所有列的单个单字节 ASCII 引号字符。 | 无 |
| ESCAPE=\<char\> | 用于转义特殊字符（例如 `DELIM`、`QUOTE` 或 `NEWLINE` 的值，或 `ESCAPE` 值本身）的单个单字节 ASCII 字符。 | 无；如果设置了 `QUOTE`，则采用该值 |
| NEWLINE=\<bytecode\> | 指示一行结束的行尾标识符。有效值为 `LF`（换行）、`CR`（回车）或 `CRLF`（回车加换行）。 | `LF` |

以下各节提供有关指定分隔符、引号、转义和换行选项的更多信息和示例。

### 指定分隔符 {#specifying-the-delimiter}

必须直接指定分隔符，或提供其字节表示。例如，给定以下使用 `¤` 货币符号作为分隔符的示例数据：

```
133¤Austin¤USA
321¤Boston¤USA
987¤Paris¤France
```

要使用名为 `s3srvcfg` 的 PXF 服务器配置从 S3 读取这些数据，请按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE s3_mbyte_delim (id int, city text, country text)
  LOCATION ('pxf://multibyte_currency?PROFILE=s3:csv&SERVER=s3srvcfg')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤'); 
```

#### 关于指定分隔符的字节表示 {#about-specifying-the-byte-representation-of-the-delimiter}

可以直接指定分隔符，也可以提供其字节表示。如果选择指定分隔符的字节表示：

- 必须以 `E'<value>'` 格式指定分隔符的字节表示。
- 由于某些字符在不同编码中的字节表示不同，必须按*数据库编码*指定分隔符的字节表示。

例如，如果数据库编码为 `UTF8`，文件编码为 `LATIN1`，分隔符为 `¤` 货币符号，则必须指定 `¤` 的 `UTF8` 字节表示，即 `\xC2\xA4`：

```
CREATE READABLE EXTERNAL TABLE s3_byterep_delim (id int, city text, country text)
  LOCATION ('pxf://multibyte_example?PROFILE=s3:csv&SERVER=s3srvcfg')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER=E'\xC2\xA4') ENCODING 'LATIN1';
```

### 关于指定引号和转义字符 {#about-specifying-quote-and-escape-characters}

当 PXF 读取包含多字节分隔符或多字符分隔符的数据时，其行为取决于引号和转义字符的设置：

| 是否设置 QUOTE？ | 是否设置 ESCAPE？ | PXF 行为 |
|-------------|--------------|----------|
| 否<sup>1</sup> | 否 | PXF 按原样读取数据。 |
| 是<sup>2</sup> | 是 | PXF 按原样读取引号字符之间的数据，且仅对引号和转义字符进行反转义。 |
| 是<sup>2</sup> | 否（`ESCAPE 'OFF'`） | PXF 按原样读取引号字符之间的数据。 |
| 否<sup>1</sup> | 是 | PXF 按原样读取数据，且仅对分隔符、换行符和转义字符本身进行反转义。 |

<sup>1</sup> 未指定引号字符时，所有数据列都必须不带引号。

<sup>2</sup> 指定引号字符时，所有数据列都必须带引号。

> **注意** PXF 要求引号值与分隔符值之间、引号值与行尾值之间不存在多余字符。此外，分隔符与引号之间不得有空白。

### 关于 NEWLINE 选项 {#about-the-newline-options}

PXF 要求文件中的每一行都以相同的换行值结尾。

默认情况下，PXF 使用换行符（`LF`）作为换行分隔符。当外部文件的换行分隔符同样为换行符时，无需指定 `NEWLINE` 格式化器选项。

如果提供了 `NEWLINE` 格式化器选项且其值包含 `CR` 或 `CRLF`，则还必须在外部表的 `LOCATION` URI 中指定相同的 `NEWLINE` 选项。例如，如果换行分隔符为 `CRLF`，请按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE s3_mbyte_newline_crlf (id int, city text, country text)
  LOCATION ('pxf://multibyte_example_crlf?PROFILE=s3:csv&SERVER=s3srvcfg&NEWLINE=CRLF')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤', NEWLINE='CRLF');
```

### 示例 {#examples}

#### 带引号数据的分隔符 {#delimiter-with-quoted-data}

给定以下使用双引号（`"`）作为引号字符、`¤` 作为分隔符的示例数据：

```
"133"¤"Austin"¤"USA"
"321"¤"Boston"¤"USA"
"987"¤"Paris"¤"France"
```

请按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE s3_mbyte_delim_quoted (id int, city text, country text)
  LOCATION ('pxf://multibyte_q?PROFILE=s3:csv&SERVER=s3srvcfg')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤', QUOTE '"'); 
```

#### 带引号和转义数据的分隔符 {#delimiter-with-quoted-and-escaped-data}

给定以下使用引号字符 `"`、转义字符 `\` 和分隔符 `¤` 的示例数据：

```
"\"hello, my name is jane\" she said. let's escape something \\"¤"123"
```

请按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE s3_mybte_delim_quoted_escaped (sentence text, num int)
  LOCATION ('pxf://multibyte_qe?PROFILE=s3:csv&SERVER=s3srvcfg')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤', QUOTE '"', ESCAPE '\');
```

使用此外部表定义，PXF 将 `sentence` 文本字段读取为：

```
SELECT sentence FROM s3_mbyte_delim_quoted_escaped;

                          sentence 
-------------------------------------------------------------
 "hello, my name is jane" she said. let's escape something \
(1 row)
```
