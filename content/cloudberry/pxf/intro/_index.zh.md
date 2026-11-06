---
title: "PXF 简介"
description: "PXF 的概念、支持的平台、架构以及外部表语法。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/intro/intro_pxf.md"
---

Apache Cloudberry 平台扩展框架（PXF）提供*连接器*，使您能够访问存储在 Apache Cloudberry 部署之外的数据源中的数据。这些连接器将外部数据源映射到 Apache Cloudberry *外部表*定义。创建 Apache Cloudberry 外部表时，您需要通过在命令中提供的*服务器*名称和 *profile* 名称来指定外部数据存储及数据格式。

您可以通过 Apache Cloudberry 查询外部表，被引用的数据仍保留在原处；也可以使用外部表将数据加载到 Apache Cloudberry 中，以获得更高的性能。

## 支持的平台 {#supported-platforms}

### 操作系统 {#operating-systems}

PXF 与以下操作系统平台和 Apache Cloudberry 版本兼容：

| 操作系统版本 | Apache Cloudberry 版本 |
|--------------|-----------------|
| Rocky Linux 8、Rocky Linux 9、Ubuntu 22.04 | 2.0、2.1 |
| Rocky Linux 8、Rocky Linux 9、Ubuntu 22.04、**Rocky Linux 10**、**Ubuntu 24.04** | 2.2+（计划中） |

### Java {#java}

PXF 支持 Java 8 和 Java 11。


### Hadoop {#hadoop}

PXF 内置了其依赖的所有 Hadoop JAR 文件，并支持以下 Hadoop 组件版本：

| Hadoop 版本 | Hive Server 版本 | HBase Server 版本 |
|----------------|---------------------|-------------|
| 2.x、3.1+ | 1.x、2.x、3.1+ | 2.3.7 |

## 架构概览 {#architectural-overview}

您的 Apache Cloudberry 部署由一台 Coordinator 主机、一台备用 Coordinator 主机和多台 Segment 主机组成。每台 Apache Cloudberry 主机上运行一个 PXF 服务进程。运行在 Segment 主机上的 PXF 服务进程会为该主机上每个参与外部表查询的 Segment 实例分配一个工作线程。多台 Segment 主机上的 PXF 服务并行地与外部数据存储通信。运行在 Coordinator 和备用 Coordinator 主机上的 PXF 服务进程目前不参与数据传输；这些进程将来可能会用于其他用途。


## 关于连接器、服务器和 Profile {#about-connectors-servers-and-profiles}

*连接器*是一个通用术语，用于概括读取或写入外部数据存储所需的实现细节。PXF 提供了面向 Hadoop（HDFS、Hive、HBase）、对象存储（Azure、Google Cloud Storage、MinIO、AWS S3 和 Dell ECS）以及 SQL 数据库（通过 JDBC）的内置连接器。

PXF *服务器（Server）*是连接器的一份命名配置。服务器定义提供 PXF 访问外部数据源所需的信息。这些配置信息因数据存储而异，可能包括服务器位置、访问凭据及其他相关属性。

Apache Cloudberry 管理员会为每个允许 Apache Cloudberry 用户访问的外部数据存储至少配置一个服务器定义，并酌情发布可用的服务器名称。

创建外部表时，您需要指定 `SERVER=<server_name>` 设置，以标识用于获取访问外部数据存储所需的配置和凭据的服务器配置。

默认的 PXF 服务器名为 `default`（保留名称）；在已配置的情况下，当没有 `SERVER=<server_name>` 设置时，它会提供外部数据源的位置和访问信息。

最后，PXF *profile* 是一个命名映射，用于标识特定外部数据存储所支持的特定数据格式或协议。PXF 支持文本、Avro、JSON、RCFile、Parquet、SequenceFile 和 ORC 数据格式以及 JDBC 协议，并提供了若干内置 profile，将在下一节讨论。

## 创建外部表 {#creating-an-external-table}

PXF 实现了一个名为 `pxf` 的 Apache Cloudberry 协议，您可以使用它创建引用外部数据存储中数据的外部表。指定 `pxf` 协议的 [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令语法如下：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
        ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION('pxf://<path-to-data>?PROFILE=<profile_name>[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT '[TEXT|CSV|CUSTOM]' (<formatting-properties>);
```

指定 `pxf` 协议的 `CREATE EXTERNAL TABLE` 语句中的 `LOCATION` 子句是一个 URI。该 URI 标识外部数据的路径，或描述外部数据位置的其他信息。例如，如果外部数据存储是 HDFS，则 `<path-to-data>` 标识某个 HDFS 文件的绝对路径；如果外部数据存储是 Hive，则 `<path-to-data>` 标识带模式限定的 Hive 表名。

您使用 URI 中以问号（?）开头的查询部分来标识 PXF 服务器和 profile 名称。

读取或写入某些数据格式时，PXF 可能需要额外的信息。您可以通过 `LOCATION` 字符串中可选的 `<custom-option>=<value>` 部分提供特定于 profile 的信息，并通过字符串中的 `<formatting-properties>` 部分提供格式信息。不同 profile 支持的自定义选项和格式属性各不相同，具体请参见该 profile 的使用文档。

表 1. CREATE EXTERNAL TABLE 参数取值及说明

<a id="creatinganexternaltable__table_pfy_htz_4p"></a>

| 关键字               | 取值及说明                                                                                                                                                                                                                                                          |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| \<path&#8209;to&#8209;data\>        | 目录、文件名、通配符模式、表名等。\<path-to-data\> 的语法取决于外部数据源。                                                                                                                                                                                                                    |
| PROFILE=\<profile_name\>  | PXF 用于访问数据的 profile。PXF 支持的 profile 可访问 [Hadoop 服务](/cloudberry/pxf/access-hadoop/)、[对象存储](/cloudberry/pxf/access-objectstores/)、[网络文件系统](/cloudberry/pxf/access-nfs/)和[其他 SQL 数据库](/cloudberry/pxf/access-jdbc/)中的文本、Avro、JSON、RCFile、Parquet、SequenceFile 和 ORC 数据。  |
| SERVER=\<server_name\>   | PXF 用于访问数据的命名服务器配置。未指定时，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>=\<value\> | profile 或服务器支持的其他选项及其取值。 |
| FORMAT&nbsp;\<value\>| PXF profile 支持 `TEXT`、`CSV` 和 `CUSTOM` 格式。  |
| \<formatting&#8209;properties\> | profile 支持的格式属性；例如 `FORMATTER` 或 `delimiter`。                                                                   |

**注意：** 创建 PXF 外部表时，不能在格式化器规范中使用 `HEADER` 选项。

## 其他 PXF 特性 {#other-pxf-features}

某些 PXF 连接器和 profile 支持过滤条件下推和列投影。有关这些支持的详细信息，请参阅以下主题：

- [PXF 过滤条件下推概述](/cloudberry/pxf/intro/filter_push/)
- [PXF 列投影概述](/cloudberry/pxf/intro/col_project/)
