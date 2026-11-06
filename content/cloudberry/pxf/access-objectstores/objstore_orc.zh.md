---
title: "读写对象存储中的 ORC 数据"
description: "通过 PXF 读写对象存储中的 ORC 数据。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_orc.md"
---

PXF 对象存储连接器支持读写 ORC 格式的数据。本节介绍如何使用 PXF 访问对象存储中的 ORC 数据，包括如何创建并查询引用存储中文件的外部表。

**注意**：从对象存储访问 ORC 格式数据与在 HDFS 中访问 ORC 格式数据非常相似。本主题指出读写 ORC 数据时对象存储特有的信息，并在适当之处链接到 [PXF Hadoop ORC 文档](/cloudberry/pxf/access-hadoop/hdfs_orc/)，以获取通用信息。


## 前提条件 {#prerequisites}

在尝试从对象存储读取数据或向对象存储写入数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。


## 数据类型映射 {#data-type-mapping}

有关 Apache Cloudberry 与 ORC 数据类型之间映射的说明，请参阅 PXF Hadoop ORC 文档中的[数据类型映射](/cloudberry/pxf/access-hadoop/hdfs_orc/#data-type-mapping)。


## 创建外部表 {#creating-the-external-table}

PXF `<objstore>:orc` Profile 支持读写 ORC 格式的数据。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

使用以下语法创建引用对象存储文件的 Apache Cloudberry 外部表。向可写外部表插入记录时，所插入的数据块将写入所指定目录中的一个或多个文件。

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>?PROFILE=<objstore>:orc&SERVER=<server_name>[&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:orc    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:orc`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| \<custom&#8209;option\>=\<value\> | ORC 支持的自定义选项在 [PXF Hadoop ORC 文档](/cloudberry/pxf/access-hadoop/hdfs_orc/#custom-options)中说明。 |
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间额外的数据移动。 |

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

## 创建外表 {#creating-the-foreign-table}

请使用以下外部数据包装器之一，并指定 `format 'orc'`。

| 对象存储  | 外部数据包装器 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs_pxf_fdw |
| Azure Data Lake Storage Gen2    | abfss_pxf_fdw |
| Google Cloud Storage    | gs_pxf_fdw |
| MinIO    | s3_pxf_fdw |
| S3    | s3_pxf_fdw |

以下语法创建引用 ORC 格式文件的 Apache Cloudberry 外表：

```sql
CREATE SERVER <foreign_server> FOREIGN DATA WRAPPER <store>_pxf_fdw;
CREATE USER MAPPING FOR <user_name> SERVER <foreign_server>;

CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
  SERVER <foreign_server>
  OPTIONS ( resource '<path-to-file>', format 'orc' [, <custom-option> '<value>' [, ...] ]);
```

| 关键字  | 值 |
|-------|-------------------------------------|
| \<foreign_server\>    | PXF 用于访问数据的命名服务器配置。可以按照[覆盖外表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-foreign-tables)中的说明，在 `CREATE SERVER` 语句中覆盖凭据。 |
| resource \<path&#8209;to&#8209;file\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| format 'orc'  | 文件格式；对 ORC 格式的数据，指定 `'orc'`。 |
| \<custom&#8209;option\>=\<value\> | ORC 专用的自定义选项在 [PXF HDFS ORC 文档](/cloudberry/pxf/access-hadoop/hdfs_orc/#custom-options)中说明。 |


## 示例 {#example}

示例请参阅 PXF Hadoop ORC 文档中的[示例：读取 HDFS 上的 ORC 文件](/cloudberry/pxf/access-hadoop/hdfs_orc/#example-reading-an-orc-file-on-hdfs)。要针对对象存储运行该示例，必须做出以下修改：

- 将 ORC 文件复制到对象存储而不是 HDFS。例如，将文件复制到 S3：

    ```shell
    $ aws s3 cp /tmp/sampledata.orc s3://BUCKET/pxf_examples/orc_example/
    ```

- 使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE sample_orc( location TEXT, month TEXT, num_orders INTEGER, total_sales NUMERIC(10,2), items_sold TEXT[] )
      LOCATION('pxf://BUCKET/pxf_examples/orc_example?PROFILE=s3:orc&SERVER=s3srvcfg')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

- 对可写外部表，使用上文所述的 `CREATE WRITABLE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE WRITABLE EXTERNAL TABLE write_to_sample_orc (location TEXT, month TEXT, num_orders INT, total_sales NUMERIC(10,2), items_sold TEXT[])
      LOCATION ('pxf://BUCKET/pxf_examples/orc_example?PROFILE=s3:orc&SERVER=s3srvcfg')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```

- 或者使用 `CREATE FOREIGN TABLE` 语法创建一个同时用于读写操作的外表。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE SERVER s3srvcfg FOREIGN DATA WRAPPER s3_pxf_fdw;
    CREATE USER MAPPING FOR CURRENT_USER SERVER s3srvcfg;

    CREATE FOREIGN TABLE sample_orc (location TEXT, month TEXT, num_orders INT, total_sales NUMERIC(10,2), items_sold TEXT[])
    SERVER s3srvcfg
    OPTIONS (
    	resource 'BUCKET/pxf_examples/orc_example',
    	format 'orc'
    )
    ```
