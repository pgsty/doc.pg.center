---
title: "使用平台扩展框架（PXF）加载数据"
linkTitle: "使用 PXF 加载数据"
description: "Apache Cloudberry 平台扩展框架（PXF）是一个可扩展框架，使 Apache Cloudberry 能够查询元数据不由数据库管理的外部数据文件。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-pxf.md"
---

你可以使用其 `pxf://` 协议，访问对象存储系统（Azure、Google Cloud Storage、Minio、S3）、外部 Hadoop 系统（HDFS、Hive、HBase）和 SQL 数据库中的数据。

PXF 内置连接器，用于访问 HDFS 文件、Hive 表、HBase 表以及可通过 JDBC 访问的数据库中的数据。用户也可以自行创建连接器，连接其他数据存储或处理引擎。

Apache Cloudberry 使用的 PXF 版本派生自 Greenplum PXF 项目，并针对 Apache Cloudberry 做了专门适配。这个适配版本的源代码由 Apache 软件基金会托管在 [apache/cloudberry-pxf](https://github.com/apache/cloudberry-pxf)。

PXF 的 `pxf` 协议打包为 Apache Cloudberry 扩展，支持对外部数据存储进行读写。该框架包含一个 C 语言扩展和一个 Java 服务。配置并初始化 PXF 后，需要在每个 Apache Cloudberry Segment 主机上启动一个 PXF JVM 进程。这个长期运行的进程会并发处理多个查询请求。

使用 `pxf` 协议之前，必须显式初始化并启动 PXF 服务。还必须在每个需要使用 PXF 的数据库中启用 PXF，并向相关 Apache Cloudberry 用户授予 `pxf` 协议的权限。

## 安装和构建 PXF {#install-and-build-pxf}

PXF 是一个需要单独构建和安装的组件。官方 `apache/cloudberry-pxf` 仓库提供源代码以及构建、安装和开发 PXF 的详细说明。开始配置之前，请按照仓库中的开发指南设置 PXF。

**构建和安装指南**：[apache/cloudberry-pxf README](https://github.com/apache/cloudberry-pxf/blob/main/README.md)

## 配置 PXF {#configure-pxf}

使用 PXF 访问外部数据之前，必须配置并初始化该服务。

### 初始化和启动 PXF {#initialize-and-start-pxf}

要使用 PXF，必须先对其进行初始化。此过程会在每个 Apache Cloudberry Segment 主机上创建必要的配置目录结构和文件。初始化之后，需要启动 PXF 服务。

1.  将 PXF 可执行文件目录添加到 `PATH` 中。这一步确保你能在任何位置运行 `pxf` 命令。

    ```shell
    export PATH=/usr/local/pxf/bin:$PATH
    ```

    可以将这一行添加到 `.bashrc` 或 `.zshrc` 文件中，使其永久生效。

2.  初始化 PXF。`prepare` 命令用于设置 PXF 配置。此命令只需运行一次。

    ```shell
    pxf prepare
    ```

3.  启动 PXF 服务。此命令会在每个 Segment 主机上启动一个 Java 进程，负责协调外部数据访问。

    ```shell
    pxf start
    ```

### 在数据库中启用 PXF {#enable-pxf-in-a-database}

在每个需要通过 `pxf` 协议访问外部数据的数据库中，都必须启用 PXF。

要在数据库中启用 PXF，必须在该数据库中创建 PXF 扩展：

```sql
CREATE EXTENSION pxf;
```

`pxf` 协议随 Apache Cloudberry 一起作为扩展提供，必须在每个计划使用它的数据库中显式启用。

### 授予 PXF 访问权限 {#grant-access-to-pxf}

要允许非超级用户的 Apache Cloudberry 角色通过 `pxf` 协议创建外部表，必须向每个角色授予 `pxf` 协议的 `SELECT` 权限：

```sql
GRANT SELECT ON PROTOCOL pxf TO <role_name>;
```

要允许非超级用户的 Apache Cloudberry 角色通过 `pxf` 协议创建可写外部表，必须向每个角色授予 `pxf` 协议的 `INSERT` 权限：

```sql
GRANT INSERT ON PROTOCOL pxf TO <role_name>;
```

## PXF 配置概述 {#pxf-configuration-overview}

PXF 配置包括服务器配置和连接器配置。PXF *服务器*是一组具名配置，提供访问外部数据源所需的访问凭据和其他信息。PXF *连接器*是 PXF 与外部数据源之间的接口。

### 示例：配置 S3 连接器 {#example-configure-s3-connector}

创建用于访问 S3 数据的 PXF 配置：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>fs.s3a.access.key</name>
        <value>YOUR_ACCESS_KEY</value>
    </property>
    <property>
        <name>fs.s3a.secret.key</name>
        <value>YOUR_SECRET_KEY</value>
    </property>
    <property>
        <name>fs.s3a.endpoint</name>
        <value>s3.amazonaws.com</value>
    </property>
</configuration>
```

### 示例：配置 JDBC 连接器 {#example-configure-jdbc-connector}

用于访问 SQL 数据库：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>jdbc.driver</name>
        <value>org.postgresql.Driver</value>
    </property>
    <property>
        <name>jdbc.url</name>
        <value>jdbc:postgresql://hostname:5432/database</value>
    </property>
    <property>
        <name>jdbc.user</name>
        <value>username</value>
    </property>
    <property>
        <name>jdbc.password</name>
        <value>password</value>
    </property>
</configuration>
```

## 步骤 3：创建 PXF 外部表 {#step-3-create-pxf-external-tables}

PXF 外部表在 `LOCATION` 子句中使用 `pxf://` 协议。URL 格式因数据源和连接器而异。

### 从 HDFS 读取 {#read-from-hdfs}

访问存储在 HDFS 中的文本文件：

```sql
CREATE EXTERNAL TABLE sales_hdfs (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('pxf://hdfs-namenode:8020/data/sales/sales.txt?PROFILE=hdfs:text')
FORMAT 'TEXT' (DELIMITER '|');
```

### 从 Hive 表读取 {#read-from-hive-tables}

直接访问 Hive 表：

```sql
CREATE EXTERNAL TABLE hive_sales (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('pxf://hive-metastore:9083/sales_db.sales_table?PROFILE=hive')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

### 从 Parquet 文件读取 {#read-from-parquet-files}

访问对象存储中的 Parquet 文件：

```sql
CREATE EXTERNAL TABLE parquet_data (
    id bigint,
    name text,
    created_date date
)
LOCATION ('pxf://s3a://my-bucket/data/events.parquet?PROFILE=s3:parquet&SERVER=s3-server')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

### 从 SQL 数据库读取 {#read-from-sql-databases}

查询外部 SQL 数据库：

```sql
CREATE EXTERNAL TABLE external_customers (
    customer_id int,
    customer_name text,
    email text,
    registration_date date
)
LOCATION ('pxf://postgresql-server/customers?PROFILE=jdbc&SERVER=postgres-server')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

### 使用 PXF 写入数据 {#write-data-with-pxf}

创建可写外部表以导出数据：

```sql
CREATE WRITABLE EXTERNAL TABLE export_to_hdfs (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('pxf://hdfs-namenode:8020/exports/sales_export?PROFILE=hdfs:text')
FORMAT 'TEXT' (DELIMITER '|')
DISTRIBUTED BY (transaction_id);
```

## PXF URL 格式 {#pxf-url-format}

PXF 协议 URL 采用以下语法：

```
pxf://<host>[:<port>]/<path-to-data>?PROFILE=<profile_name>[&<custom-option>=<value>][&SERVER=<server_name>]
```

其中：
- `host:port`：外部数据源的位置
- `path-to-data`：具体数据的路径（文件、目录、表等）
- `PROFILE`：PXF 连接器配置类型（例如 `hdfs:text`、`hive`、`s3:parquet`、`jdbc`）
- `SERVER`：具名服务器配置（可选）
- `custom-option`：连接器特有的附加选项

## 常用 PXF 配置类型 {#common-pxf-profiles}

| 配置类型 | 数据源 | 格式 | 使用场景 |
|---------|-------------|--------|----------|
| `hdfs:text` | HDFS | 文本文件 | 分隔文本数据 |
| `hdfs:avro` | HDFS | Avro 文件 | 支持模式演进 |
| `hdfs:parquet` | HDFS | Parquet 文件 | 列式分析 |
| `hdfs:orc` | HDFS | ORC 文件 | 优化的行列式存储 |
| `hive` | Hive | 多种格式 | 访问 Hive 表 |
| `hbase` | HBase | HBase | 访问 NoSQL 数据 |
| `s3:text` | S3 | 文本文件 | 云对象存储 |
| `s3:parquet` | S3 | Parquet 文件 | 云端分析 |
| `jdbc` | SQL 数据库 | 多种格式 | 访问外部数据库 |

## 性能优化 {#performance-optimization}

### 分区剪枝 {#partition-pruning}

PXF 支持对 Hive 表进行分区剪枝：

```sql
SELECT * FROM hive_sales 
WHERE sale_date >= '2024-01-01' AND sale_date < '2024-02-01';
```

### 谓词下推 {#predicate-pushdown}

启用谓词下推以提高性能：

```sql
-- This filter can be pushed down to the external source
SELECT * FROM external_customers 
WHERE registration_date > '2024-01-01';
```

### 并行处理 {#parallel-processing}

使用多个文件以提高并行度：

```sql
CREATE EXTERNAL TABLE multi_file_data (
    id bigint,
    data text
)
LOCATION ('pxf://hdfs-namenode:8020/data/partitioned/*?PROFILE=hdfs:text')
FORMAT 'TEXT' (DELIMITER ',');
```

## 错误处理 {#error-handling}

启用错误日志记录，以监控数据质量：

```sql
CREATE EXTERNAL TABLE sales_with_errors (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('pxf://hdfs-namenode:8020/data/sales/?PROFILE=hdfs:text')
FORMAT 'TEXT' (DELIMITER '|')
LOG ERRORS SEGMENT REJECT LIMIT 50;
```

## 最佳实践 {#best-practices}

- 选择最贴合数据格式和存储系统的 PXF 配置类型，以确保最佳性能和功能支持。
- 创建可复用的具名服务器配置，集中管理连接参数和凭据，便于管理多个外部数据源。
- 将外部数据组织为大小在 100MB 到 1GB 之间的文件，以在各 Apache Cloudberry Segment 上实现最佳并行处理效果。
- 使用 Parquet 或 ORC 等压缩存储格式，减少 I/O 开销并提高查询性能。
- 在生产环境中实施全面的错误日志记录和监控，以快速发现并解决数据访问问题。
- 建立适当的认证机制，并对通往敏感外部数据源的所有连接启用加密。

## 限制 {#limitations}

- PXF 要求所有 Segment 主机都能访问外部数据源。
- 某些数据源可能有特定的版本兼容性要求。
- 写入操作取决于连接器的能力。
- 访问外部数据源的网络延迟可能影响性能。

## 故障排查 {#troubleshooting}

### 检查 PXF 服务状态 {#check-pxf-service-status}

```shell
pxf cluster status
```

### 查看 PXF 日志 {#view-pxf-logs}

```shell
pxf cluster logs
```

### 测试连通性 {#test-connectivity}

```sql
SELECT * FROM pxf_external_table LIMIT 5;
```

## 进一步了解 {#learn-more}

有关 Apache Cloudberry 平台扩展框架（PXF）的更多详细信息，请参阅官方 PXF 项目仓库，其中包含源代码、文档和贡献指南。

- [Apache Cloudberry PXF 项目](https://github.com/apache/cloudberry-pxf)
