---
title: "访问 Azure、Google Cloud Storage 和兼容 S3 的对象存储"
linkTitle: "使用 PXF 访问对象存储"
description: "使用 PXF 访问 Azure、Google Cloud Storage、MinIO 和 S3 对象存储。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/access_objstore.md"
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

PXF 安装时附带了连接器，可连接 Azure Blob Storage、Azure Data Lake Storage Gen2、Google Cloud Storage、AWS、MinIO 以及 Dell ECS 等兼容 S3 的对象存储。

## 前提条件 {#prerequisites}

在使用 PXF 处理对象存储数据之前，请确保：

- 已配置 PXF，并且 PXF 正在每台 Apache Cloudberry 主机上运行。详见[配置 PXF](/cloudberry/pxf/administering/configuring/)。
- 已配置计划使用的 PXF 对象存储连接器。配置方法请参阅[配置 Azure 和 Google Cloud Storage 对象存储连接器](/cloudberry/pxf/administering/configuring/objstore_cfg/)以及[配置 MinIO、AWS S3 和 Dell ECS 对象存储连接器](/cloudberry/pxf/administering/configuring/s3_objstore_cfg/)。
- Apache Cloudberry 主机与外部对象存储系统之间的时间已同步。


## 连接器、数据格式和 Profile {#connectors-data-formats-and-profiles}

PXF 对象存储连接器提供内置 Profile，支持以下数据格式：

- Text
- CSV
- Avro
- JSON
- ORC
- Parquet
- AvroSequenceFile
- SequenceFile

PXF 的 Azure 连接器提供以下 Profile，用于读取（多数情况下也可写入）这些受支持的数据格式。

>**注意**：
>ADL 支持已弃用，请改用 ABFSS Profile。

| 数据格式 | Azure Blob Storage | Azure Data Lake Storage Gen2 | 支持的操作 |
|-----|------|---------| ---------|
| 以分隔符分隔的单行[纯文本](/cloudberry/pxf/access-objectstores/objstore_text/) | wasbs:text | abfss:text | 读、写 |
| 以逗号分隔的单行[纯文本](/cloudberry/pxf/access-objectstores/objstore_text/)值 | wasbs:csv | abfss:csv | 读、写 |
| 以多字节或多字符分隔符分隔的单行 [csv](/cloudberry/pxf/access-objectstores/objstore_text/#about-reading-data-containing-multi-byte-or-multi-character-delimiters) | wasbs:csv | abfss:csv | 读 |
| 以分隔符分隔且[含带引号换行符的文本](/cloudberry/pxf/access-objectstores/objstore_text/) | wasbs:text:multi | abfss:text:multi | 读 |
| 定宽单行[文本](/cloudberry/pxf/access-objectstores/objstore_fixedwidth/) | wasbs:fixedwidth | abfss:fixedwidth | 读、写 |
| [Avro](/cloudberry/pxf/access-objectstores/objstore_avro/) | wasbs:avro | abfss:avro | 读、写 |
| [JSON](/cloudberry/pxf/access-objectstores/objstore_json/) | wasbs:json | abfss:json | 读、写 |
| [ORC](/cloudberry/pxf/access-objectstores/objstore_orc/) | wasbs:orc | abfss:orc | 读、写 |
| [Parquet](/cloudberry/pxf/access-objectstores/objstore_parquet/) | wasbs:parquet | abfss:parquet | 读、写 |
| AvroSequenceFile | wasbs:AvroSequenceFile | abfss:AvroSequenceFile | 读、写 |
| [SequenceFile](/cloudberry/pxf/access-objectstores/objstore_seqfile/) | wasbs:SequenceFile | abfss:SequenceFile | 读、写 |

类似地，PXF 的 Google Cloud Storage 连接器和兼容 S3 的对象存储连接器提供以下 Profile：

| 数据格式 | Google Cloud Storage | AWS S3、MinIO 或 Dell ECS | 支持的操作 |
|-----|------|---------| ---------|
| 以分隔符分隔的单行[纯文本](/cloudberry/pxf/access-objectstores/objstore_text/) | gs:text | s3:text | 读、写 |
| 以逗号分隔的单行[纯文本](/cloudberry/pxf/access-objectstores/objstore_text/)值 | gs:csv | s3:csv | 读、写 |
| 以多字节或多字符分隔符分隔的单行逗号分隔值 [csv](/cloudberry/pxf/access-objectstores/objstore_text/#about-reading-data-containing-multi-byte-or-multi-character-delimiters) | gs:csv | s3:csv | 读 |
| 以分隔符分隔且[含带引号换行符的文本](/cloudberry/pxf/access-objectstores/objstore_text/) | gs:text:multi | s3:text:multi | 读 |
| 定宽单行[文本](/cloudberry/pxf/access-objectstores/objstore_fixedwidth/) | gs:fixedwidth | s3:fixedwidth | 读、写 |
| [Avro](/cloudberry/pxf/access-objectstores/objstore_avro/) | gs:avro | s3:avro | 读、写 |
| [JSON](/cloudberry/pxf/access-objectstores/objstore_json/) | gs:json | s3:json | 读 |
| [ORC](/cloudberry/pxf/access-objectstores/objstore_orc/) | gs:orc | s3:orc | 读、写 |
| [Parquet](/cloudberry/pxf/access-objectstores/objstore_parquet/) | gs:parquet | s3:parquet | 读、写 |
| AvroSequenceFile | gs:AvroSequenceFile | s3:AvroSequenceFile | 读、写 |
| [SequenceFile](/cloudberry/pxf/access-objectstores/objstore_seqfile/) | gs:SequenceFile | s3:SequenceFile | 读、写 |

在 `CREATE EXTERNAL TABLE` 命令中指定 `pxf` 协议时，需要提供 Profile 名称，以创建引用特定对象存储中文件或目录的 Apache Cloudberry 外部表。

## CREATE EXTERNAL TABLE 命令示例 {#sample-create-external-table-commands}

> <b>注意：</b>创建引用对象存储中文件或目录的外部表时，必须在 `LOCATION` URI 中指定 `SERVER`。

以下命令创建一个引用 S3 上文本文件的外部表，指定名为 `s3:text` 的 Profile 和名为 `s3srvcfg` 的服务器配置：

<pre>
CREATE EXTERNAL TABLE pxf_s3_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://S3_BUCKET/pxf_examples/pxf_s3_simple.txt?<b>PROFILE=s3:text&SERVER=s3srvcfg</b>')
FORMAT 'TEXT' (delimiter=E',');
</pre>

以下命令创建一个引用 Azure Blob Storage 上文本文件的外部表，指定名为 `wasbs:text` 的 Profile 和名为 `wasbssrvcfg` 的服务器配置。您需要提供 Azure Blob Storage 容器标识符和 Azure Blob Storage 账户名称。

<pre>
CREATE EXTERNAL TABLE pxf_wasbs_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://<b>AZURE_CONTAINER@YOUR_AZURE_BLOB_STORAGE_ACCOUNT_NAME</b>.blob.core.windows.net/path/to/blob/file?<b>PROFILE=wasbs:text&SERVER=wasbssrvcfg</b>')
FORMAT 'TEXT';
</pre>

以下命令创建一个引用 Azure Data Lake Storage Gen2 上文本文件的外部表，指定名为 `abfss:text` 的 Profile 和名为 `abfsssrvcfg` 的服务器配置。您需要提供 Azure Data Lake Storage Gen2 账户名称。

<pre>
CREATE EXTERNAL TABLE pxf_abfss_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://<b>YOUR_ABFSS_ACCOUNT_NAME</b>.dfs.core.windows.net/path/to/file?<b>PROFILE=abfss:text&SERVER=abfsssrvcfg</b>')
FORMAT 'TEXT';
</pre>

以下命令创建一个引用 Google Cloud Storage 上 JSON 文件的外部表，指定名为 `gs:json` 的 Profile 和名为 `gcssrvcfg` 的服务器配置：

<pre>
CREATE EXTERNAL TABLE pxf_gsc_json(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://dir/subdir/file.json?<b>PROFILE=gs:json&SERVER=gcssrvcfg</b>')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
</pre>
