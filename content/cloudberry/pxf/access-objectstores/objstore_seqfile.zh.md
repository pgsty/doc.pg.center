---
title: "读写对象存储中的 SequenceFile 数据"
description: "通过 PXF 读写对象存储中的 SequenceFile 数据。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_seqfile.md"
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

PXF 对象存储连接器支持 SequenceFile 格式的二进制数据。本节介绍如何使用 PXF 读写 SequenceFile 数据，包括如何创建引用对象存储中文件的外部表、向其中插入数据并查询数据。

**注意**：从对象存储访问 SequenceFile 格式数据与在 HDFS 中访问 SequenceFile 格式数据非常相似。本主题指出读写 SequenceFile 数据时对象存储特有的信息，并在适当之处链接到 PXF HDFS SequenceFile 文档，以获取通用信息。


## 前提条件 {#prerequisites}

在尝试从对象存储读取数据或向对象存储写入数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 创建外部表 {#creating-the-external-table}

PXF `<objstore>:SequenceFile` Profile 支持读写 SequenceFile 格式的二进制数据。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

使用以下语法创建引用 HDFS 目录的 Apache Cloudberry 外部表。向可写外部表插入记录时，所插入的数据块将写入所指定目录中的一个或多个文件。

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-dir>
    ?PROFILE=<objstore>:SequenceFile&SERVER=<server_name>[&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;dir\>    | 对象存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:SequenceFile    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:SequenceFile`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| \<custom&#8209;option\>=\<value\> | SequenceFile 专用的自定义选项在 [PXF HDFS SequenceFile 文档](/cloudberry/pxf/access-hadoop/hdfs_seqfile/#custom-options)中说明。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间额外的数据移动。 |

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

## 示例 {#example}

写入/读取示例请参阅 PXF HDFS SequenceFile 文档中的[示例：向 HDFS 写入二进制数据](/cloudberry/pxf/access-hadoop/hdfs_seqfile/#example-writing-binary-data-to-hdfs)。要针对对象存储运行该示例，必须做出以下修改：

- 对可写外部表，使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE WRITABLE EXTERNAL TABLE pxf_tbl_seqfile_s3(location text, month text, number_of_orders integer, total_sales real)
      LOCATION ('pxf://BUCKET/pxf_examples/pxf_seqfile?PROFILE=s3:SequenceFile&DATA_SCHEMA=com.example.pxf.hdfs.writable.dataschema.PxfExample_CustomWritable&COMPRESSION_TYPE=BLOCK&COMPRESSION_CODEC=bzip2&SERVER=s3srvcfg')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```

- 对可读外部表，使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE read_pxf_tbl_seqfile_s3(location text, month text, number_of_orders integer, total_sales real)
      LOCATION ('pxf://BUCKET/pxf_examples/pxf_seqfile?PROFILE=s3:SequenceFile&DATA_SCHEMA=com.example.pxf.hdfs.writable.dataschema.PxfExample_CustomWritable&SERVER=s3srvcfg')
     FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```
