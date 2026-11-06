---
title: "读写对象存储中的 JSON 数据"
description: "通过 PXF 读取对象存储中的 JSON 数据。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_json.md"
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

PXF 对象存储连接器支持读写 JSON 格式的数据。本节介绍如何使用 PXF 和外部表访问并写入对象存储中的 JSON 数据。

**注意**：从对象存储访问 JSON 格式数据与在 HDFS 中访问 JSON 格式数据非常相似。本主题指出读写 JSON 数据时对象存储特有的信息，并在适当之处链接到 [PXF HDFS JSON 文档](/cloudberry/pxf/access-hadoop/hdfs_json/)，以获取通用信息。

## 前提条件 {#prerequisites}

在尝试从对象存储读取数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 处理 JSON 数据 {#working-with-json-data}

有关 JSON 这种基于文本的数据交换格式的说明，请参阅 PXF HDFS JSON 文档中的[处理 JSON 数据](/cloudberry/pxf/access-hadoop/hdfs_json/#working-with-json-data)。

## 数据类型映射 {#data-type-mapping}

有关 JSON 到 Apache Cloudberry 以及 Apache Cloudberry 到 JSON 的类型映射说明，请参阅 PXF HDFS JSON 文档中的[数据类型映射](/cloudberry/pxf/access-hadoop/hdfs_json/#data-type-mapping)。

## 创建外部表 {#creating-the-external-table}

使用 `<objstore>:json` Profile 读写对象存储中的 JSON 格式文件。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

以下语法创建引用 JSON 格式数据的 Apache Cloudberry 外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:json&SERVER=<server_name>[&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:json    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:json`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| \<custom&#8209;option\>=\<value\> | JSON 支持的自定义选项在 [PXF HDFS JSON 文档](/cloudberry/pxf/access-hadoop/hdfs_json/#custom-options)中说明。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` `'CUSTOM'` 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

## 读取示例 {#read-example}

JSON 读取示例请参阅 PXF HDFS JSON 文档中的[将示例 JSON 数据加载到 HDFS](/cloudberry/pxf/access-hadoop/hdfs_json/#loading-the-sample-json-data-to-hdfs)和[读取示例](/cloudberry/pxf/access-hadoop/hdfs_json/#example-single-object-per-row-read)。要针对对象存储运行该示例，必须做出以下修改：

- 将文件复制到对象存储而不是 HDFS。例如，将文件复制到 S3：

    ```shell
    $ aws s3 cp /tmp/objperrow.jsonl s3://BUCKET/pxf_examples/
    ```

- 使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE objperrow_json_s3(
      created_at TEXT,
      id_str TEXT,
      "user.id" INTEGER,
      "user.location" TEXT,
      "coordinates.values" INTEGER[]
    )
    LOCATION('pxf://BUCKET/pxf_examples/objperrow.jsonl?PROFILE=s3:json&SERVER=s3srvcfg')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

- 如果要访问 `coordinates.values` 数组的特定元素，可以在方括号中指定数组下标：

    ```sql
    SELECT "coordinates.values"[1], "coordinates.values"[2] FROM singleline_json_s3;
    ``` 

## 写入示例 {#write-example}

JSON 写入示例请参阅 PXF HDFS JSON 文档中的[写入 JSON 数据](/cloudberry/pxf/access-hadoop/hdfs_json/#writing-json-data)。要针对对象存储运行“每行一个对象”的写入示例，必须做出以下修改：

- 使用上文所述的 `CREATE WRITABLE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE WRITABLE EXTERNAL TABLE add_objperrow_json_s3(
      created_at TEXT,
      id_str TEXT,
      id INTEGER,
      location TEXT,
      coordinates INTEGER[]
    )
    LOCATION('pxf://BUCKET/pxf_examples/jsopr?PROFILE=s3:json&SERVER=s3srvcfg')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```

- 使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置回读数据。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE jsopr_tbl(
      created_at TEXT,
      id_str TEXT,
      id INTEGER,
      location TEXT,
      coordinates INTEGER[]
    )
    LOCATION('pxf://BUCKET/pxf_examples/jsopr?PROFILE=s3:json')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```
