---
title: "将多行文本文件读入单个表行"
description: "通过 PXF 将对象存储中的多行文本文件作为单个表行读取。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/objstore_fileasrow.md"
---

PXF 对象存储连接器支持将多行文本文件作为单个表行读取。本节介绍如何使用 PXF 读取对象存储中的多行文本和 JSON 数据文件，包括如何创建引用存储中多个文件的外部表。

PXF 仅支持以这种方式读取文本和 JSON 文件。

**注意**：从对象存储访问多行文件与在 HDFS 中访问多行文件非常相似。本主题指出读取这些文件时对象存储特有的信息。更多信息请参阅 [PXF HDFS 文档](/cloudberry/pxf/access-hadoop/hdfs_fileasrow/)。

## 前提条件 {#prerequisites}

在尝试读取对象存储中多个文件的数据之前，请确保已满足 PXF 对象存储的[前提条件](/cloudberry/pxf/access-objectstores/#prerequisites)。

## 创建外部表 {#creating-the-external-table}

使用 `<objstore>:text:multi` Profile 读取对象存储中的多个文件，每个文件读入单个表行。PXF 支持以下 `<objstore>` Profile 前缀：

| 对象存储  | Profile 前缀 |
|-------|-------------------------------------|
| Azure Blob Storage   | wasbs |
| Azure Data Lake Storage Gen2    | abfss |
| Google Cloud Storage    | gs |
| MinIO    | s3 |
| S3    | s3 |

以下语法创建引用对象存储中一个或多个文本文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> text|json | LIKE <other_table> )
  LOCATION ('pxf://<path-to-files>?PROFILE=<objstore>:text:multi&SERVER=<server_name>[&IGNORE_MISSING_PATH=<boolean>]&FILE_AS_ROW=true')
  FORMAT 'CSV');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和值如下表所述。

| 关键字  | 值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;files\>    | 对象存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;files\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;files\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE=\<objstore\>:text:multi    | `PROFILE` 关键字必须标明具体的对象存储。例如 `s3:text:multi`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定 \<path-to-files\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 会返回错误。值为 `true` 时，PXF 会忽略路径缺失错误并返回空分片。 |
| FILE\_AS\_ROW=true    | 必需选项，指示 PXF 将每个文件读入单个表行。 |
| FORMAT | `FORMAT` 必须指定为 `'CSV'`。  |

如果访问的是 S3 对象存储，可以按照[覆盖外部表的 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)中的说明，在 `CREATE EXTERNAL TABLE` 命令中通过自定义选项提供 S3 凭据。

## 示例 {#example}

示例请参阅 PXF HDFS 文档中的[示例：将 HDFS 文本文件读入单个表行](/cloudberry/pxf/access-hadoop/hdfs_fileasrow/#example-reading-an-hdfs-text-file-into-a-single-table-row)。要针对对象存储运行该示例，必须做出以下修改：

- 将文件复制到对象存储而不是 HDFS。例如，将文件复制到 S3：

    ```shell
    $ aws s3 cp /tmp/file1.txt s3://BUCKET/pxf_examples/tdir
    $ aws s3 cp /tmp/file2.txt s3://BUCKET/pxf_examples/tdir
    $ aws s3 cp /tmp/file3.txt s3://BUCKET/pxf_examples/tdir
    ```

- 使用上文所述的 `CREATE EXTERNAL TABLE` 语法以及 `LOCATION` 关键字和设置。例如，如果服务器名称为 `s3srvcfg`：

    ```sql
    CREATE EXTERNAL TABLE pxf_readfileasrow_s3( c1 text )
      LOCATION('pxf://BUCKET/pxf_examples/tdir?PROFILE=s3:text:multi&SERVER=s3srvcfg&FILE_AS_ROW=true')
    FORMAT 'CSV'
    ```
