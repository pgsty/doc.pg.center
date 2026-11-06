---
title: "PXF 列投影概述"
description: "PXF 在读取外部数据时如何执行列投影。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/intro/col_project.md"
---

PXF 支持列投影，且该功能始终处于启用状态。启用列投影后，只有外部表上的 `SELECT` 查询所需的列才会从外部数据源返回。这一过程可以提升查询性能，也可以减少传输到 Apache Cloudberry 的数据量。

> **注意：** 某些外部数据源不支持列投影。如果查询访问的数据源不支持列投影，则查询会在不使用列投影的情况下运行，数据在传输到 Apache Cloudberry 之后才会被过滤。

对于 `pxf` 外部表协议，列投影会自动启用。PXF 使用不同的连接器访问外部数据源，列投影的支持情况同样由具体的连接器实现决定。以下 PXF 连接器与 profile 的组合在读操作中支持列投影：

| 数据源 | 连接器 | Profile |
|-------------|---------------|---------|
| 外部 SQL 数据库 | JDBC 连接器 | jdbc |
| Hive | Hive 连接器 | hive（访问以 Text、Parquet、RCFile 和 ORC 存储的表）、hive:rc、hive:orc |
| Hadoop | HDFS 连接器 | hdfs:orc、hdfs:parquet |
| 网络文件系统 | 文件连接器 | file:orc、file:parquet |
| Amazon S3 | 兼容 S3 的对象存储连接器 | s3:orc、s3:parquet |
| 使用 S3 Select 的 Amazon S3 | 兼容 S3 的对象存储连接器 | s3:parquet、s3:text |
| Google Cloud Storage | GCS 对象存储连接器 | gs:orc、gs:parquet |
| Azure Blob Storage | Azure 对象存储连接器 | wasbs:orc、wasbs:parquet |
| Azure Data Lake Storage Gen2 | Azure 对象存储连接器 | abfss:orc、abfss:parquet |

> **注意：** 当 PXF 无法成功序列化查询过滤条件时（例如 `WHERE` 子句的结果为 `boolean` 类型），可能会停用列投影。

总之，必须同时满足以下所有条件，才会发生列投影：

* 您访问的外部数据源必须支持列投影。例如，Hive 对 ORC 格式的数据支持列投影，某些 SQL 数据库也支持列投影。
* 底层的 PXF 连接器和 profile 实现也必须支持列投影。例如，上面列出的 PXF Hive 和 JDBC 连接器 profile 支持列投影，支持读取 Parquet 数据的 PXF 连接器同样如此。
* PXF 必须能够序列化查询过滤条件。
