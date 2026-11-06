---
title: "读写 HDFS Avro 数据"
description: "通过 PXF 读写 HDFS 中的 Avro 数据。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_avro.md"
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


使用 PXF HDFS Connector 读写 Avro 格式的数据。本节介绍如何使用 PXF 读写 HDFS 中的 Avro 数据，包括如何创建、查询引用 HDFS 数据存储中某个 Avro 文件的外部表，以及如何向其中插入数据。

PXF 支持读写使用以下编解码器压缩的 Avro 文件：`bzip2`、`xz`、`snappy`、`zstandard` 和 `deflate`。

## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## 处理 Avro 数据 {#working-with-avro-data}

Apache Avro 是一种数据序列化框架，数据以紧凑的二进制格式序列化。Avro 规定数据类型使用 JSON 定义。Avro 格式的数据拥有独立的模式，该模式同样使用 JSON 定义。Avro 模式连同其数据是完全自描述的。

### 数据类型映射 {#data-type-mapping}

Avro 规范定义了[基本](https://avro.apache.org/docs/current/spec.html#schema_primitive)类型、[复杂](https://avro.apache.org/docs/current/spec.html#schema_complex)类型和[逻辑](https://avro.apache.org/docs/current/spec.html#Logical+Types)类型。

要在 Apache Cloudberry 中表示 Avro 基本数据类型以及由基本类型构成的 Avro 数组，请将数据值映射到相同类型的 Apache Cloudberry 列。

Avro 还支持其他复杂数据类型，包括由非基本类型构成的数组、映射（map）、记录（record）、枚举（enumeration）和 fixed 类型。请将这些复杂数据类型的顶层字段映射到 Apache Cloudberry 的 `text` 类型。PXF 本身不支持读取这些类型的内部结构，但您可以创建 Apache Cloudberry 函数或应用程序代码，来提取这些复杂数据类型的子组件或对其做进一步处理。

Avro 支持的逻辑数据类型包括 date、decimal、duration、time、timestamp 和 uuid 类型。

### 读取映射 {#read-mapping}

<a id="a2g_type_mapping_table"></a>

读取 Avro 数据时，PXF 使用以下数据类型映射：

| Avro 数据类型     | PXF/Apache Cloudberry 数据类型    |
|--------------------|----------------------------|
| boolean | boolean |
| bytes | bytea |
| double | double |
| float | real |
| int | int |
| long | bigint |
| string | text |
| 复杂类型：由 boolean、bytes、double、float、int、long、string 类型构成的数组（任意维度） | 由 boolean、bytea、double、real、bigint、text 类型构成的数组（任意维度）   |
| 复杂类型：由其他类型构成的数组<br/>（*已提供 Avro 模式*） | text[]   |
| 复杂类型：Map、Record 或 Enum  | text，并在集合项、映射的键值对以及记录数据之间插入分隔符。   |
| 复杂类型：Fixed     | bytea（仅支持读操作）。   |
| Union      | 根据 union 的具体内容，遵循上述基本数据类型或复杂数据类型的约定；必须包含 2 个元素，其中一个必须为 null。  |
| 逻辑类型：Date | date |
| 逻辑类型：Decimal | decimal 或 numeric |
| 逻辑类型：duration | bytea |
| 逻辑类型：Time（毫秒精度） | time（不带时区的 time） |
| 逻辑类型：Time（微秒精度） | time（不带时区的 time） |
| 逻辑类型：Timestamp（毫秒精度） | timestamp（带或不带时区） |
| 逻辑类型：Timestamp（微秒精度） | timestamp（带或不带时区） |
| 逻辑类型：Local Timestamp（毫秒精度） | timestamp（带或不带时区） |
| 逻辑类型：Local Timestamp（微秒精度） | timestamp（带或不带时区） |
| 逻辑类型：UUID | UUID |

### 写入映射 {#write-mapping}

PXF 支持写入 Avro 基本类型以及由 Avro 基本类型构成的数组。PXF 支持将其他复杂类型以字符串（string）形式写入 Avro。

写入 Avro 数据时，PXF 使用以下数据类型映射：

<a id="g2_type_mapping_table"></a>

| PXF/Apache Cloudberry 数据类型 | Avro 数据类型 |
|-------------------|----------------------|
| bigint | long |
| boolean | boolean |
| bytea | bytes |
| double | double |
| char<sup>1</sup> | string |
| enum | string |
| int |  int |
| real | float |
| smallint<sup>2</sup> | int |
| text | string |
| varchar | string |
| numeric, date, time, timestamp, timestamptz<br/>（*未提供 Avro 模式*） | string |
| 由 bigint、boolean、bytea、double、int、real、text 类型构成的数组（任意维度） <br/>（*已提供 Avro 模式*） | 由 long、boolean、bytes、double、int、float、string 类型构成的 Array（任意维度） |
| bigint[], boolean[], bytea[], double[], int[], real[], text[] <br/>（*未提供 Avro 模式*） | long[], boolean[], bytes[], double[], int[], float[], string[]（一维数组） |
| numeric[], date[], time[], timestamp[], timestamptz[] <br/> （*已提供 Avro 模式*） | string[] |
| enum, record | string |

<br/><sup>1</sup>&nbsp;如有需要，PXF 会用空格将 <code>char[<i>n</i>]</code> 类型右填充至长度 <code><i>n</i></code>。
<br/><sup>2</sup>&nbsp;PXF 在写入 Avro 数据之前，会先将 Apache Cloudberry 的 `smallint` 类型转换为 `int`。请务必将该字段读取为 `int`。


### Avro 模式与数据 {#avro-schemas-and-data}

Avro 模式使用 JSON 定义，由上文数据类型映射部分所列的同样的基本类型和复杂类型组成。Avro 模式文件通常带有 `.avsc` 后缀。

Avro 模式文件中的字段通过一个对象数组来定义，其中每个对象由名称和类型指定。

Avro 数据文件包含模式以及数据的紧凑二进制表示。Avro 数据文件通常带有 `.avro` 后缀。

对 HDFS 进行读操作和写操作时，都可以指定 Avro 模式。模式文件既可以是二进制的 `*.avro` 文件，也可以是 JSON 格式的 `*.avsc` 文件：

| 外部表类型  | 是否指定模式 | 说明
|-------|--------------------------|-----------|
| 可读   | 是 | PXF 使用指定的模式；这会覆盖 Avro 数据文件中内嵌的模式。 |
| 可读   | 否 | PXF 使用 Avro 数据文件中内嵌的模式。 |
| 可写   | 是 | PXF 使用指定的模式。 |
| 可写   | 否 | PXF 根据外部表定义创建 Avro 模式。 |

向 PXF 提供 Avro 模式文件时，该文件必须位于每台 Apache Cloudberry 主机上的相同位置，**或者**位于 Hadoop 文件系统上。PXF 首先在 Apache Cloudberry 主机上按绝对文件路径查找。如果在那里没有找到模式文件，则相对于 PXF 类路径（classpath）查找该文件。如果 PXF 无法在本地找到模式文件，则会在 HDFS 上查找该文件。

`$PXF_BASE/conf` 目录位于 PXF 类路径中。PXF 可以找到您添加到每台 Apache Cloudberry 主机上该目录中的 Avro 模式文件。

有关向 HDFS 写入 Avro 数据时的其他模式注意事项，请参阅[写入 Avro 数据](#writing-avro-data)。

## 创建外部表 {#creating-the-external-table}

使用 `hdfs:avro` profile 读写 HDFS 中 Avro 格式的数据。以下语法创建引用此类文件的 Apache Cloudberry 可读外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:avro[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export');
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值，在下表中说明。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:avro`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的已命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>  | \<custom-option\> 将在下文讨论。|
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |
| DISTRIBUTED BY | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可避免加载操作中 Segment 之间产生额外的数据移动。使用 `EXPLAIN` 命令分析查询执行计划，验证该分布策略能否使 Segment 之间的数据移动最小化。 |

### 自定义选项 {#custom-options}

对于复杂类型，PXF `hdfs:avro` profile 会在显示之前，在集合项和值之间插入默认分隔符。您可以在 `CREATE EXTERNAL TABLE` 命令中为特定的 `hdfs:avro` 自定义选项指定值，从而使用非默认的分隔符字符。

`hdfs:avro` profile 支持以下 \<custom-option\>：

| 选项关键字   | 说明       
|---------------|--------------------|                                                                                        
| COLLECTION_DELIM | 当 PXF 将 Avro 复杂数据类型映射到 text 列时，放置在顶层数组、映射或记录字段的各项之间的分隔符字符。默认为逗号（`,`）字符。（读）|
| MAPKEY_DELIM | 当 PXF 将 Avro 复杂数据类型映射到 text 列时，放置在映射项的键与值之间的分隔符字符。默认为冒号 `:` 字符。（读）|
| RECORDKEY_DELIM | 当 PXF 将 Avro 复杂数据类型映射到 text 列时，放置在记录项的字段名与值之间的分隔符字符。默认为冒号 `:` 字符。（读）|
| SCHEMA | Avro 模式文件在 Apache Cloudberry 主机上或 HDFS 上的绝对路径，或模式文件在主机上的相对路径。（读和写）|
| IGNORE_MISSING_PATH | 布尔值，指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。当值为 `true` 时，PXF 忽略路径缺失错误并返回空分片（fragment）。（读） |

PXF `hdfs:avro` profile 支持与编码和压缩相关的写选项。您在 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中指定这些写选项。`hdfs:avro` profile 支持以下自定义写选项：

| 写选项  | 值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入 Avro 数据时支持的压缩编解码器包括：`bzip2`、`xz`、`snappy`、`deflate`、`zstandard` 和 `uncompressed`。如果未提供此选项，PXF 使用 `deflate` 压缩对数据进行压缩。 |
| CODEC_LEVEL    | 压缩级别（仅适用于 `deflate`、`zstandard` 和 `xz` 编解码器）。该级别控制速度与压缩率之间的权衡。有效值为 1（最快）到 9（压缩率最高）。默认压缩级别为 6。 |

## 创建外表 {#creating-the-foreign-table}

请将以下某个外部数据包装器与 `format 'avro'` 配合使用。

| 对象存储  | 外部数据包装器 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs_pxf_fdw |
| Azure Data Lake Storage Gen2    | abfss_pxf_fdw |
| Google Cloud Storage    | gs_pxf_fdw |
| MinIO    | s3_pxf_fdw |
| S3    | s3_pxf_fdw |

以下语法创建引用 Avro 格式文件的 Apache Cloudberry 外表：

```sql
CREATE SERVER <foreign_server> FOREIGN DATA WRAPPER <store>_pxf_fdw;
CREATE USER MAPPING FOR <user_name> SERVER <foreign_server>;

CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
  SERVER <foreign_server>
  OPTIONS ( resource '<path-to-file>', format 'avro' [, <custom-option> '<value>'[...]]);
```

| 关键字  | 值 |
|-------|-------------------------------------|
| \<foreign_server\>    | PXF 用于访问数据的已命名服务器配置。您可以在 `CREATE SERVER` 语句中覆盖凭据，具体方法参见[为外表覆盖 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-foreign-tables) |
| resource \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| format 'avro'  | 文件格式规范。 |
| \<custom&#8209;option\>=\<value\> | Avro 专用的自定义选项见[上文](/cloudberry/pxf/access-hadoop/hdfs_avro/#custom-options)。 |


## 示例：读取 Avro 数据 {#example-reading-avro-data}

本节中的示例将对具有以下字段名和数据类型的记录模式的 Avro 数据进行操作：

- id - long
- username - string
- followers - string 数组（string[]）
- fmap - long 类型的映射
- relationship - 枚举类型
- address - 由门牌号（int）、街道名（string）和城市（string）组成的记录

您将创建一个 Avro 模式和数据文件，然后创建一个可读外部表来读取这些数据。


### 创建模式 {#create-schema}

执行以下操作，创建表示上述示例模式的 Avro 模式。

1. 创建名为 `avro_schema.avsc` 的文件：

    ```shell
    $ vi /tmp/avro_schema.avsc
    ```

2. 将以下文本复制并粘贴到 `avro_schema.avsc` 中：

    ```json
    {
    "type" : "record",
      "name" : "example_schema",
      "namespace" : "com.example",
      "fields" : [ {
        "name" : "id",
        "type" : "long",
        "doc" : "Id of the user account"
      }, {
        "name" : "username",
        "type" : "string",
        "doc" : "Name of the user account"
      }, {
        "name" : "followers",
        "type" : {"type": "array", "items": "string"},
        "doc" : "Users followers"
      }, {
        "name": "fmap",
        "type": {"type": "map", "values": "long"}
      }, {
        "name": "relationship",
        "type": {
            "type": "enum",
            "name": "relationshipEnum",
            "symbols": ["MARRIED","LOVE","FRIEND","COLLEAGUE","STRANGER","ENEMY"]
        }
      }, {
        "name": "address",
        "type": {
            "type": "record",
            "name": "addressRecord",
            "fields": [
                {"name":"number", "type":"int"},
                {"name":"street", "type":"string"},
                {"name":"city", "type":"string"}]
        }
      } ],
      "doc:" : "A basic schema for storing messages"
    }
    ```

### 创建 Avro 数据文件（JSON） {#create-avro-data-file-json}

执行以下步骤，创建符合上述模式的示例 Avro 数据文件。

1.  创建名为 `pxf_avro.txt` 的文本文件：

    ```shell
    $ vi /tmp/pxf_avro.txt
    ```

2. 将以下数据输入到 `pxf_avro.txt` 中：

    ```text
    {"id":1, "username":"john","followers":["kate", "santosh"], "relationship": "FRIEND", "fmap": {"kate":10,"santosh":4}, "address":{"number":1, "street":"renaissance drive", "city":"san jose"}}
    
    {"id":2, "username":"jim","followers":["john", "pam"], "relationship": "COLLEAGUE", "fmap": {"john":3,"pam":3}, "address":{"number":9, "street":"deer creek", "city":"palo alto"}}
    ```

    示例数据使用逗号（`,`）分隔顶层记录，使用冒号 `:` 分隔映射的键/值以及记录的字段名/值。

3. 将文本文件转换为 Avro 格式。转换方式有多种，既可以通过编程方式，也可以通过命令行。在本示例中，我们使用 Java Avro 工具。

    1. 从 http://avro.apache.org/releases.html 将最新版本的 Avro 工具 jar 下载到当前工作目录。

    1. 转换文件：

        ```shell
        $ java -jar ./avro-tools-1.11.0.jar fromjson --schema-file /tmp/avro_schema.avsc /tmp/pxf_avro.txt > /tmp/pxf_avro.avro
        ```

        生成的 Avro 二进制数据文件写入 `/tmp/pxf_avro.avro`。 
    
4. 将生成的 Avro 文件复制到 HDFS：

    ```shell
    $ hdfs dfs -put /tmp/pxf_avro.avro /data/pxf_examples/
    ```
    
### 读取 Avro 数据 {#reading-avro-data}

执行以下操作，创建并查询引用上一节中添加到 HDFS 的 `pxf_avro.avro` 文件的外部表。创建该表时：

-  使用 PXF 默认服务器。
-  将顶层基本字段 `id`（long 类型）和 `username`（string 类型）映射到与之等价的 Apache Cloudberry 类型（bigint 和 text）。
-  将 `followers` 字段映射到 text 数组（text[]）。
-  将其余复杂字段映射到 text 类型。
-  使用 `hdfs:avro` profile 的自定义选项，显式设置记录、映射和集合的分隔符。


1. 使用 `hdfs:avro` profile，基于 `pxf_avro.avro` 文件创建可查询的外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_hdfs_avro(id bigint, username text, followers text[], fmap text, relationship text, address text)
                LOCATION ('pxf://data/pxf_examples/pxf_avro.avro?PROFILE=hdfs:avro&COLLECTION_DELIM=,&MAPKEY_DELIM=:&RECORDKEY_DELIM=:')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

2. 对 `pxf_hdfs_avro` 表执行一个简单查询：

    ```sql
    postgres=# SELECT * FROM pxf_hdfs_avro;
    ```

    ```text
     id | username |   followers    |        fmap         | relationship |                      address                      
    ----+----------+----------------+--------------------+--------------+---------------------------------------------------
      1 | john     | {kate,santosh} | {kate:10,santosh:4} | FRIEND       | {number:1,street:renaissance drive,city:san jose}
      2 | jim      | {john,pam}     | {pam:3,john:3}      | COLLEAGUE    | {number:9,street:deer creek,city:palo alto}
    (2 rows)
    ```

    对该外部表的简单查询显示，复杂类型数据的各组成部分以 `CREATE EXTERNAL TABLE` 调用中指定的分隔符分隔。


3. 查询该表，显示 `id` 和 `followers` text 数组的第一个元素：

    ```sql
    postgres=# SELECT id, followers[1] FROM pxf_hdfs_avro;
     id | followers 
    ----+-----------
      1 | kate
      2 | john
    ```


## 写入 Avro 数据 {#writing-avro-data}

PXF HDFS connector 的 `hdfs:avro` profile 支持向 HDFS 写入 Avro 数据。创建用于写入 Avro 数据的可写外部表时，您需要指定 HDFS 上某个目录的名称。向可写外部表插入记录时，所插入的数据块会被写入您所指定目录中的一个或多个文件。

创建用于向 Avro 文件写入数据的可写外部表时，每个表行是一条 Avro 记录，每个表列是一个 Avro 字段。

如果不指定 `SCHEMA` 文件，PXF 会根据 Apache Cloudberry 外部表定义为 Avro 文件生成模式。PXF 将外部表列的名称赋给 Avro 字段名。由于 Avro 有 `null` 类型，而 Apache Cloudberry 外部表不支持 `NOT NULL` 列限定符，因此 PXF 会把每种数据类型包装成由映射类型和 `null` 组成的 Avro `union`。例如，对于您以 Apache Cloudberry `text` 数据类型定义的可写外部表列，PXF 会生成以下模式元素：

```text
["string", "null"]
```

如果您提供的模式未包含字段数据类型与 `null` 的 `union`，而 PXF 又遇到 NULL 数据字段，则 PXF 会返回错误。

PXF 仅支持写入 Avro 基本数据类型，以及由[数据类型写入映射](#write-mapping)中所列类型构成的 Avro 数组。PXF 不支持向 Avro 写入复杂类型：

- 在 `LOCATION` 中指定 `SCHEMA` 文件时，模式只能包含基本数据类型。
- 当 PXF 生成模式时，您在可写外部表列定义中指定的任何复杂类型，都会作为单个 Avro `string` 类型写入 Avro 文件。例如，如果写入 Apache Cloudberry `numeric` 类型的数组，PXF 会将该数组转换为 `string`，而您必须使用 Apache Cloudberry `text` 类型的列来读取这些数据。


### 示例：写入 Avro 数据 {#example-writing-avro-data}

在本示例中，您将创建一个写入 HDFS 上 Avro 文件的外部表，由 PXF 生成 Avro 模式。向文件中插入一些数据之后，您再创建一个可读外部表来查询这些 Avro 数据。

本示例中创建和读取的 Avro 文件包含以下字段：

- id:  `int`
- username:  `text`
- followers:  `text[]`

示例步骤：

1. 创建可写外部表：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_avrowrite(id int, username text, followers text[])
                LOCATION ('pxf://data/pxf_examples/pxfwrite.avro?PROFILE=hdfs:avro')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');

2. 向 `pxf_avrowrite` 表中插入一些数据：

    ``` sql
    postgres=# INSERT INTO pxf_avrowrite VALUES (33, 'oliver', ARRAY['alex','frank']);
    postgres=# INSERT INTO pxf_avrowrite VALUES (77, 'lisa', ARRAY['tom','mary']);
    ```

    PXF 使用外部表定义来生成 Avro 模式。

3. 创建一个外部表，用于读取您刚刚插入表中的 Avro 数据：

    ```sql
    postgres=# CREATE EXTERNAL TABLE read_pxfwrite(id int, username text, followers text[])
                LOCATION ('pxf://data/pxf_examples/pxfwrite.avro?PROFILE=hdfs:avro')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

4. 通过查询 `read_pxfwrite` 表来读取 Avro 数据：

    ```sql
    postgres=# SELECT id, followers, followers[1], followers[2] FROM read_pxfwrite ORDER BY id;
    ```

    ```text
     id |  followers   | followers | followers 
    ----+--------------+-----------+-----------
     33 | {alex,frank} | alex      | frank
     77 | {tom,mary}   | tom       | mary
    (2 rows)
    ```
