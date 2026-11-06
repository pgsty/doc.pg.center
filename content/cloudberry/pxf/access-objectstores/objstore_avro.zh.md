---
title: "读写对象存储中的 Avro 数据"
description: "通过 PXF 读写对象存储中的 Avro 数据。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_avro.md"
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

PXF 对象存储连接器支持读取 Avro 格式的数据。本节介绍如何使用 PXF 读写对象存储中的 Avro 数据，包括如何创建、查询引用存储中 Avro 文件的外部表，以及如何向其中插入数据。

**注意**：从对象存储访问 Avro 格式数据与在 HDFS 中访问 Avro 格式数据非常相似。本主题指出读取 Avro 数据时对象存储特有的信息，并在适当之处链接到 [PXF HDFS Avro 文档](/cloudberry/pxf/access-hadoop/hdfs_avro/)，以获取通用信息。


## 前提条件 {#prerequisites}

在尝试从对象存储读取数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 处理 Avro 数据 {#working-with-avro-data}

有关 Apache Avro 数据序列化框架的说明，请参阅 PXF HDFS Avro 文档中的[处理 Avro 数据](/cloudberry/pxf/access-hadoop/hdfs_avro/#working-with-avro-data)。

读取或写入对象存储中的 Avro 数据时：

- 如果 Avro 模式文件位于对象存储中：

    - 必须在模式文件路径中包含存储桶（bucket）。该存储桶不必与 Avro 数据文件所在的存储桶相同。
    - 在 `SERVER` 配置中指定的密钥必须能够同时访问数据文件和模式文件所在的存储桶。
- 模式文件路径中不得包含空格。

## 创建外部表 {#creating-the-external-table}

使用 `<objstore>:avro` Profile 读写对象存储中的 Avro 格式文件。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

以下语法创建引用 Avro 格式文件的 Apache Cloudberry 外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:avro&SERVER=<server_name>[&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:avro    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:avro`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| \<custom&#8209;option\>=\<value\> | Avro 专用的自定义选项在 [PXF HDFS Avro 文档](/cloudberry/pxf/access-hadoop/hdfs_avro/#custom-options)中说明。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。|

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。


## 创建外表 {#creating-the-foreign-table}

请使用以下外部数据包装器之一，并指定 `format 'avro'`。

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
| \<foreign_server\>    | PXF 用于访问数据的命名服务器配置。可以按照[覆盖外表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-foreign-tables)中的说明，在 `CREATE SERVER` 语句中覆盖凭据。 |
| resource \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| format 'avro'  | 文件格式说明。 |
| \<custom&#8209;option\>=\<value\> | Avro 专用的自定义选项在 [PXF HDFS Avro 文档](/cloudberry/pxf/access-hadoop/hdfs_avro/#custom-options)中说明。 |

## 示例 {#example}

Avro 示例请参阅 PXF HDFS Avro 文档中的[示例：读取 Avro 数据](/cloudberry/pxf/access-hadoop/hdfs_avro/#example-reading-avro-data)。要针对对象存储运行该示例，必须做出以下修改：

- 将文件复制到对象存储而不是 HDFS。例如，将文件复制到 S3：

    ```shell
    $ aws s3 cp /tmp/pxf_avro.avro s3://BUCKET/pxf_examples/
    ```

- 使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE pxf_s3_avro(id bigint, username text, followers text[], fmap text, relationship text, address text)
      LOCATION ('pxf://BUCKET/pxf_examples/pxf_avro.avro?PROFILE=s3:avro&SERVER=s3srvcfg&COLLECTION_DELIM=,&MAPKEY_DELIM=:&RECORDKEY_DELIM=:')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

按照[写入 Avro 数据](/cloudberry/pxf/access-hadoop/hdfs_avro/#writing-avro-data)中的步骤操作时，也需要做类似的修改。
