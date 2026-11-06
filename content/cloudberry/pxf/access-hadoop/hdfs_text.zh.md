---
title: "读写 HDFS 文本数据"
description: "通过 PXF 读写 HDFS 中的文本数据。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_text.md"
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

PXF HDFS Connector 支持以普通分隔符分隔和逗号分隔值形式存储的文本数据。本节介绍如何使用 PXF 访问 HDFS 文本数据，包括如何创建引用 HDFS 数据存储中文件的外部表、对其进行查询以及向其中插入数据。

PXF 支持读取或写入使用 `default`、`bzip2` 和 `gzip` 编解码器压缩的文本文件。

## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据或向 HDFS 写入数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## 读取文本数据 {#reading-text-data}

读取以普通文本分隔的数据时使用 `hdfs:text` Profile；读取每行为一条记录的 .csv 数据时使用 `hdfs:csv`。以下语法创建一个引用 HDFS 上此类文本文件的 Apache Cloudberry 可读外部表： 

```sql
CREATE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:text|csv[&SERVER=<server_name>][&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | 当 \<path-to-hdfs-file\> 引用以普通文本分隔的数据时，使用 `PROFILE` `hdfs:text`。<br/> 当 \<path-to-hdfs-file\> 引用逗号分隔值数据时，使用 `PROFILE` `hdfs:csv`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |
| SKIP_HEADER_COUNT=\<numlines\> | 指定 PXF 在读取数据之前，应在每个 \<hdfs-file\> 的第一个分片中跳过的标题行数。默认值为 0，即不跳过任何行。 |
| FORMAT | 当 \<path-to-hdfs-file\> 引用以普通文本分隔的数据时，使用 `FORMAT` `'TEXT'`。<br/> 当 \<path-to-hdfs-file\> 引用逗号分隔值数据时，使用 `FORMAT` `'CSV'`。  |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当 \<delim_value\> 为转义序列时，在其前面加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。如果文本文件包含标题行，请使用 `SKIP_HEADER_COUNT` 指定 PXF 应在每个文件第一个分片开头跳过的行数。

### 示例：读取 HDFS 上的文本数据 {#example-reading-text-data-on-hdfs}

按以下步骤创建示例文本文件，将文件复制到 HDFS，并使用 `hdfs:text` 和 `hdfs:csv` Profile 以及默认 PXF 服务器创建两个 PXF 外部表来查询这些数据：

1. 为 PXF 示例数据文件创建 HDFS 目录。例如：

    ```shell
    $ hdfs dfs -mkdir -p /data/pxf_examples
    ```

2. 创建名为 `pxf_hdfs_simple.txt` 的以分隔符分隔的纯文本数据文件：

    ```shell
    $ echo 'Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67' > /tmp/pxf_hdfs_simple.txt
    ```

    请注意，这里使用逗号（`,`）分隔四个数据字段。

4. 将数据文件添加到 HDFS：

    ```shell
    $ hdfs dfs -put /tmp/pxf_hdfs_simple.txt /data/pxf_examples/
    ```

5. 显示存储在 HDFS 中的 `pxf_hdfs_simple.txt` 文件的内容：

    ```shell
    $ hdfs dfs -cat /data/pxf_examples/pxf_hdfs_simple.txt
    ```

4. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

1. 使用 PXF `hdfs:text` Profile 创建 Apache Cloudberry 外部表，该表引用您刚创建并添加到 HDFS 的 `pxf_hdfs_simple.txt` 文件：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_textsimple(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:text')
              FORMAT 'TEXT' (delimiter=E',');
    ```
              
2. 查询外部表：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_textsimple;          
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

2. 创建第二个引用 `pxf_hdfs_simple.txt` 的外部表，这次指定 `hdfs:csv` `PROFILE` 和 `CSV` `FORMAT`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_textsimple_csv(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:csv')
              FORMAT 'CSV';
    postgres=# SELECT * FROM pxf_hdfs_textsimple_csv;          
    ```

    为逗号分隔值数据指定 `FORMAT 'CSV'` 时，无需 `delimiter` 格式化器选项，因为逗号是默认的分隔符值。

## 读取含带引号换行符的文本数据 {#reading-text-data-with-quoted-linefeeds}

使用 `hdfs:text:multi` Profile 读取以分隔符分隔、记录为单行或多行且包含内嵌（带引号的）换行符的普通文本数据。以下语法创建一个引用 HDFS 上此类文本文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:text:multi[&SERVER=<server_name>][&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:text:multi`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |
| SKIP_HEADER_COUNT=\<numlines\> | 指定 PXF 在读取数据之前，应在每个 \<hdfs-file\> 的第一个分片中跳过的标题行数。默认值为 0，即不跳过任何行。 |
| FORMAT | 当 \<path-to-hdfs-file\> 引用以普通文本分隔的数据时，使用 `FORMAT` `'TEXT'`。<br/> 当 \<path-to-hdfs-file\> 引用逗号分隔值数据时，使用 `FORMAT` `'CSV'`。  |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当 \<delim_value\> 为转义序列时，在其前面加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |

**注意**：PXF 不支持 `CREATE EXTERNAL TABLE` 命令中的 `(HEADER)` 格式化器选项。如果文本文件包含标题行，请使用 `SKIP_HEADER_COUNT` 指定 PXF 应在每个文件第一个分片开头跳过的行数。

### 示例：读取 HDFS 上的多行文本数据 {#example-reading-multi-line-text-data-on-hdfs}

按以下步骤创建示例文本文件，将文件复制到 HDFS，并使用 PXF `hdfs:text:multi` Profile 和默认 PXF 服务器创建 Apache Cloudberry 可读外部表来查询这些数据：

1. 创建第二个以分隔符分隔的纯文本文件：

    ```shell
    $ vi /tmp/pxf_hdfs_multi.txt
    ```

2. 将以下数据复制／粘贴到 `pxf_hdfs_multi.txt` 中：

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

    请注意，这里使用冒号 `:` 分隔三个字段。还请注意第一个（地址）字段两侧的引号。该字段包含一个内嵌换行符，用于将街道地址与城市和州分隔开。

3. 将文本文件复制到 HDFS：

    ```shell
    $ hdfs dfs -put /tmp/pxf_hdfs_multi.txt /data/pxf_examples/
    ```

4. 使用 `hdfs:text:multi` Profile 创建引用 HDFS 文件 `pxf_hdfs_multi.txt` 的外部表，注意要将 `:`（冒号）标识为字段分隔符：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_textmulti(address text, month text, year int)
                LOCATION ('pxf://data/pxf_examples/pxf_hdfs_multi.txt?PROFILE=hdfs:text:multi')
              FORMAT 'CSV' (delimiter ':');
    ```
    
    请注意指定 `delimiter` 的另一种语法。
    
2. 查询 `pxf_hdfs_textmulti` 表：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_textmulti;
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

## 向 HDFS 写入文本数据 {#writing-text-data-to-hdfs}

PXF HDFS 连接器的 `hdfs:text` 和 `hdfs:csv` Profile 支持向 HDFS 写入单行普通文本数据。使用 PXF HDFS 连接器创建可写外部表时，需要指定 HDFS 上某个目录的名称。向可写外部表插入记录时，所插入的数据块会被写入您所指定目录中的一个或多个文件。

**注意**：使用可写 Profile 创建的外部表只能用于 `INSERT` 操作。如果要查询已插入的数据，必须另外创建一个引用该 HDFS 目录的可读外部表。

使用以下语法创建引用 HDFS 目录的 Apache Cloudberry 可写外部表： 

```sql
CREATE WRITABLE EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-dir>
    ?PROFILE=hdfs:text|csv[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT '[TEXT|CSV]' (delimiter[=|<space>][E]'<delim_value>');
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;dir\>    | HDFS 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | 使用 `PROFILE` `hdfs:text` 将以分隔符分隔的普通文本写入 \<path-to-hdfs-file\>。<br/> 使用 `PROFILE` `hdfs:csv` 将逗号分隔值文本写入 \<path-to-hdfs-dir\>。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>  | 下文介绍 \<custom-option\>。|
| FORMAT | 使用 `FORMAT` `'TEXT'` 将以分隔符分隔的普通文本写入 \<path-to-hdfs-dir\>。<br/> 使用 `FORMAT` `'CSV'` 将逗号分隔值文本写入 \<path-to-hdfs-dir\>。 |
| delimiter    | 数据中的分隔符字符。对于 `FORMAT` `'CSV'`，默认的 \<delim_value\> 为逗号（`,`）。当 \<delim_value\> 为转义序列时，在其前面加上 `E`。示例：`(delimiter=E'\t')`、`(delimiter ':')`。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间的额外数据移动。 |

使用 `hdfs:text` 或 `hdfs:csv` Profile 创建的可写外部表可以选择使用记录压缩或块压缩。您可以通过 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中的自定义选项指定压缩编解码器。`hdfs:text` 和 `hdfs:csv` Profile 支持以下自定义写选项：

| 选项  | 取值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入文本数据时支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |

### 示例：向 HDFS 写入文本数据 {#example-writing-text-data-to-hdfs}

此示例使用[示例：读取 HDFS 上的文本数据](#example-reading-text-data-on-hdfs)中介绍的数据模式。 

| 列名  | 数据类型 |
|-------|-------------------------------------|
| location | text |
| month | text |
| number\_of\_orders | int |
| total\_sales | float8 |

此示例还可选地使用您在该练习中创建的名为 `pxf_hdfs_textsimple` 的 Apache Cloudberry 外部表。

#### 步骤 {#procedure}

按以下步骤创建使用上述相同数据模式的 Apache Cloudberry 可写外部表，其中一个表将使用压缩。您将使用 PXF `hdfs:text` Profile 和默认 PXF 服务器，将数据写入底层 HDFS 目录。您还将另外创建一个可读外部表，用于读取您写入 HDFS 目录的数据。

1. 使用上述数据模式创建 Apache Cloudberry 可写外部表。写入 HDFS 目录 `/data/pxf_examples/pxfwritable_hdfs_textsimple1`。创建该表时指定逗号（`,`）作为分隔符：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_hdfs_writabletbl_1(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://data/pxf_examples/pxfwritable_hdfs_textsimple1?PROFILE=hdfs:text')
              FORMAT 'TEXT' (delimiter=',');
    ```
    
    将 `FORMAT` 子句的 `delimiter` 值指定为单个 ASCII 逗号字符 `,`。

2. 通过对 `pxf_hdfs_writabletbl_1` 调用 SQL `INSERT` 命令，向 HDFS 目录 `pxfwritable_hdfs_textsimple1` 写入几条单独的记录：

    ```sql
    postgres=# INSERT INTO pxf_hdfs_writabletbl_1 VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    postgres=# INSERT INTO pxf_hdfs_writabletbl_1 VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

3. （可选）将您在[示例：读取 HDFS 上的文本数据] (#example-reading-text-data-on-hdfs)中创建的 `pxf_hdfs_textsimple` 表中的数据插入 `pxf_hdfs_writabletbl_1`：

    ```sql
    postgres=# INSERT INTO pxf_hdfs_writabletbl_1 SELECT * FROM pxf_hdfs_textsimple;
    ```

4. 在另一个终端窗口中，显示您刚添加到 HDFS 的数据：

    ```shell
    $ hdfs dfs -cat /data/pxf_examples/pxfwritable_hdfs_textsimple1/*
    Frankfurt,Mar,777,3956.98
    Cleveland,Oct,3812,96645.37
    Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67
    ```

    由于您在创建可写外部表时指定逗号（`,`）作为分隔符，因此该字符就是 HDFS 数据每条记录中使用的字段分隔符。

5. Apache Cloudberry 不支持直接查询可写外部表。要查询刚添加到 HDFS 的数据，必须创建引用该 HDFS 目录的 Apache Cloudberry 可读外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_textsimple_r1(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://data/pxf_examples/pxfwritable_hdfs_textsimple1?PROFILE=hdfs:text')
			    FORMAT 'CSV';
    ```

    创建可读外部表时指定 `'CSV'` `FORMAT`，是因为您创建可写表时使用了逗号（`,`）作为分隔符字符，而逗号正是 `'CSV'` `FORMAT` 的默认分隔符。

6. 查询可读外部表：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_textsimple_r1 ORDER BY total_sales;
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

    `pxf_hdfs_textsimple_r1` 表包含您单独插入的记录；如果执行了可选步骤，还包含 `pxf_hdfs_textsimple` 表的全部内容。

7. 创建第二个 Apache Cloudberry 可写外部表，这次使用 Gzip 压缩，并使用冒号 `:` 作为分隔符：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_hdfs_writabletbl_2 (location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://data/pxf_examples/pxfwritable_hdfs_textsimple2?PROFILE=hdfs:text&COMPRESSION_CODEC=gzip')
              FORMAT 'TEXT' (delimiter=':');
    ```

8. 直接向 `pxf_hdfs_writabletbl_2` 表插入数据，向 HDFS 目录 `pxfwritable_hdfs_textsimple2` 写入几条记录：

    ```sql
    gpadmin=# INSERT INTO pxf_hdfs_writabletbl_2 VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    gpadmin=# INSERT INTO pxf_hdfs_writabletbl_2 VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

9. 在另一个终端窗口中，显示您添加到 HDFS 的数据内容；对 `hdfs dfs` 使用 `-text` 选项，以文本形式查看压缩数据：

    ```shell
    $ hdfs dfs -text /data/pxf_examples/pxfwritable_hdfs_textsimple2/*
    Frankfurt:Mar:777:3956.98
    Cleveland:Oct:3812:96645.3
    ```

    请注意，冒号 `:` 是此 HDFS 数据中的字段分隔符。

    要查询新创建的名为 `pxfwritable_hdfs_textsimple2` 的 HDFS 目录中的数据，可以按上述方式创建引用该 HDFS 目录的 Apache Cloudberry 可读外部表，并指定 `FORMAT 'CSV' (delimiter=':')`。

## 关于设置外部表编码 {#about-setting-the-external-table-encoding}

当外部文件的编码与数据库编码不同时，必须将外部表的 `ENCODING` 设置为与数据文件的编码一致。例如，如果数据库编码为 `UTF8`，文件编码为 `LATIN1`，请按如下方式创建外部表：

```
CREATE EXTERNAL TABLE pxf_csv_latin1(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:csv')
FORMAT 'CSV' ENCODING 'LATIN1';
```

## 关于读取包含多字节或多字符分隔符的数据 {#about-reading-data-containing-multi-byte-or-multi-character-delimiters}

读取包含多字节分隔符或多个分隔符字符的数据时，只能使用 `*:csv` PXF Profile。为此类数据创建可读外部表的语法如下：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:csv[&SERVER=<server_name>][&IGNORE_MISSING_PATH=<boolean>][&SKIP_HEADER_COUNT=<numlines>][&NEWLINE=<bytecode>]')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import' <option>[=|<space>][E]'<value>');
```

请注意语法块中的 `FORMAT` 行。虽然该语法与读取 CSV 的语法类似，但 PXF 需要使用自定义格式化器来读取包含多字节或多字符分隔符的数据。您必须指定 `'CUSTOM'` 格式和 `pxfdelimited_import` 格式化器。还必须在格式化器选项中指定分隔符。

读取包含多字节或多字符分隔符的数据时，PXF 识别以下格式化器选项：

| 选项名称  | 取值说明 | 默认值 |
|-------|---------------|---------------|
| DELIMITER=\<delim_string\> | 分隔各列的单字节或多字节分隔符字符串。该字符串的长度最多为 32 字节，且不得包含引号或转义字符。**必需** | 无 |
| QUOTE=\<char\> | 用于所有列的单个单字节 ASCII 引号字符。 | 无 |
| ESCAPE=\<char\> | 用于转义特殊字符（例如 `DELIM`、`QUOTE` 或 `NEWLINE` 的值，或 `ESCAPE` 值本身）的单个单字节 ASCII 字符。 | 无；如果设置了 `QUOTE`，则采用该值 |
| NEWLINE=\<bytecode\> | 标识一行结束的行尾指示符。有效值为 `LF`（换行）、`CR`（回车）或 `CRLF`（回车加换行）。 | `LF` |

以下各节提供有关指定分隔符、引号、转义和换行选项的更多信息和示例。

### 指定分隔符 {#specifying-the-delimiter}

必须直接指定分隔符，或提供其字节表示。例如，给定以下使用 `¤` 货币符号作为分隔符的示例数据：

```
133¤Austin¤USA
321¤Boston¤USA
987¤Paris¤France
```

按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE mbyte_delim (id int, city text, country text)
  LOCATION ('pxf://multibyte_currency?PROFILE=hdfs:csv')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤'); 
```

#### 关于指定分隔符的字节表示 {#about-specifying-the-byte-representation-of-the-delimiter}

您可以直接指定分隔符，也可以提供其字节表示。如果选择指定分隔符的字节表示：

- 必须以 `E'<value>'` 格式指定分隔符的字节表示。
- 由于某些字符在不同编码中具有不同的字节表示，因此必须以*数据库编码*指定分隔符的字节表示。

例如，如果数据库编码为 `UTF8`，文件编码为 `LATIN1`，分隔符为 `¤` 货币符号，则必须指定 `¤` 的 `UTF8` 字节表示，即 `\xC2\xA4`：

```
CREATE READABLE EXTERNAL TABLE byterep_delim (id int, city text, country text)
  LOCATION ('pxf://multibyte_example?PROFILE=hdfs:csv')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER=E'\xC2\xA4') ENCODING 'LATIN1';
```

### 关于指定引号和转义字符 {#about-specifying-quote-and-escape-characters}

PXF 读取包含多字节或多字符分隔符的数据时，其行为取决于引号和转义字符的设置：

| 是否设置 QUOTE？ | 是否设置 ESCAPE？ | PXF 行为 |
|-------------|--------------|----------|
| 否<sup>1</sup> | 否 | PXF 按原样读取数据。 |
| 是<sup>2</sup> | 是 | PXF 按原样读取引号字符之间的数据，且仅对引号和转义字符取消转义。 |
| 是<sup>2</sup> | 否（`ESCAPE 'OFF'`） | PXF 按原样读取引号字符之间的数据。 |
| 否<sup>1</sup> | 是 | PXF 按原样读取数据，且仅对分隔符、换行符和转义字符本身取消转义。 |

<sup>1</sup> 未指定引号字符时，所有数据列都必须不带引号。

<sup>2</sup> 指定引号字符时，所有数据列都必须带引号。

> **注意** PXF 要求引号值与分隔符值之间、引号值与行尾值之间都没有多余字符。此外，分隔符与引号之间不得有空白字符。

### 关于 NEWLINE 选项 {#about-the-newline-options}

PXF 要求文件中的每一行都以相同的换行值结尾。

默认情况下，PXF 使用换行符（`LF`）作为换行分隔符。当外部文件的换行分隔符同样是换行符时，无需指定 `NEWLINE` 格式化器选项。

如果提供了 `NEWLINE` 格式化器选项，并且其值包含 `CR` 或 `CRLF`，则还必须在外部表的 `LOCATION` URI 中指定相同的 `NEWLINE` 选项。例如，如果换行分隔符为 `CRLF`，请按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE mbyte_newline_crlf (id int, city text, country text)
  LOCATION ('pxf://multibyte_example_crlf?PROFILE=hdfs:csv&NEWLINE=CRLF')
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

按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE mbyte_delim_quoted (id int, city text, country text)
  LOCATION ('pxf://multibyte_q?PROFILE=hdfs:csv')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤', QUOTE '"'); 
```

#### 带引号和转义数据的分隔符 {#delimiter-with-quoted-and-escaped-data}

给定以下使用引号字符 `"`、转义字符 `\` 和分隔符 `¤` 的示例数据：

```
"\"hello, my name is jane\" she said. let's escape something \\"¤"123"
```

按如下方式创建外部表：

```
CREATE READABLE EXTERNAL TABLE mybte_delim_quoted_escaped (sentence text, num int)
  LOCATION ('pxf://multibyte_qe?PROFILE=hdfs:csv')
FORMAT 'CUSTOM' (FORMATTER='pxfdelimited_import', DELIMITER='¤', QUOTE '"', ESCAPE '\');
```

使用此外部表定义时，PXF 将 `sentence` 文本字段读取为：

```
SELECT sentence FROM mbyte_delim_quoted_escaped;

                          sentence 
-------------------------------------------------------------
 "hello, my name is jane" she said. let's escape something \
(1 row)
```
