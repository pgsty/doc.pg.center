---
title: "访问 AWS S3 对象存储概述"
description: "关于使用 PXF 访问 S3 对象存储。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/access_s3.md"
---

PXF 安装时附带了 AWS S3 对象存储连接器。该连接器还支持以下运行时功能：

- 在 `CREATE EXTERNAL TABLE` 命令的 DDL 中提供 S3 凭据，以覆盖服务器配置中指定的 S3 凭据。
- 使用 Amazon S3 Select 服务读取 S3 中的某些 CSV 和 Parquet 数据。

## 覆盖外部表的 S3 服务器配置 {#overriding-the-s3-server-configuration-for-external-tables}

如果访问的是兼容 S3 的对象存储，可以在 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中通过以下自定义选项直接指定 S3 访问 ID 和密钥，从而覆盖 S3 服务器配置中的凭据：

| 自定义选项  | 值说明 |
|-------|-------------------------------------|
| accesskey    | AWS S3 账户的访问密钥 ID。 |
| secretkey    | 与 AWS S3 访问密钥 ID 关联的密钥。 |

例如：
<pre>CREATE EXTERNAL TABLE pxf_ext_tbl(name text, orders int)
  LOCATION ('pxf://S3_BUCKET/dir/file.txt?PROFILE=s3:text&SERVER=s3srvcfg<b>&accesskey=YOURKEY&secretkey=YOURSECRET</b>')
FORMAT 'TEXT' (delimiter=E',');</pre>

> <b>警告：</b>以这种方式提供的凭据会作为外部表定义的一部分而可见。请勿在生产环境中使用这种传递凭据的方式。

目前，PXF 不支持以这种方式覆盖 Azure、Google Cloud Storage 和 MinIO 的服务器凭据。

有关 PXF 为 Apache Cloudberry 用户获取配置属性设置时所遵循的优先级规则，详见[配置属性优先级](/cloudberry/pxf/administering/configuring/cfg_server/#about-configuration-property-precedence)。

## 覆盖外表的 S3 服务器配置 {#overriding-the-s3-server-configuration-for-foreign-tables}

PXF 支持通过外部数据包装器（Foreign Data Wrapper，FDW）框架访问 S3 数据，这是外部表框架之外的另一种方式。要使用外部数据包装器访问 S3，必须先创建一个定义 S3 连接参数的服务器。

以下命令创建名为 `s3srvcfg` 的服务器，使用 `s3_pxf_fdw` 外部数据包装器。该服务器将使用 PXF 服务器配置中的凭据。

<pre>CREATE SERVER s3srvcfg FOREIGN DATA WRAPPER s3_pxf_fdw;</pre>

不过，可以在 `CREATE SERVER` 命令中使用 `OPTIONS` 子句覆盖这些自定义选项。以下命令创建名为 `s3srvcfg` 的服务器，使用 `s3_pxf_fdw` 外部数据包装器，并指定 S3 访问凭据：

<pre>CREATE SERVER s3srvcfg FOREIGN DATA WRAPPER s3_pxf_fdw
  OPTIONS (accesskey 'YOURKEY', secretkey 'YOURSECRET');</pre>

请将 `YOURKEY` 替换为您的 AWS S3 访问密钥 ID，将 `YOURSECRET` 替换为您的 AWS S3 秘密访问密钥。


支持以下选项：
| 选项 | 说明 |
|-------|-------------------------------------|
| accesskey    | AWS S3 账户的访问密钥 ID。 |
| secretkey    | 与 AWS S3 访问密钥 ID 关联的密钥。 |

> <b>警告：</b>以这种方式提供的凭据会作为外部表定义的一部分而可见。请勿在生产环境中使用这种传递凭据的方式。

目前，PXF 不支持以这种方式覆盖 Azure、Google Cloud Storage 和 MinIO 的服务器凭据。

有关 PXF 为 Apache Cloudberry 用户获取配置属性设置时所遵循的优先级规则，详见[配置属性优先级](/cloudberry/pxf/administering/configuring/cfg_server/#about-configuration-property-precedence)。


> <b>警告：</b>在服务器配置或用户映射中提供的凭据存储在 Apache Cloudberry 系统目录中。请确保遵循您所在组织管理数据库凭据的安全策略。

## 使用 Amazon S3 Select 服务 {#using-the-amazon-s3-select-service}

有关 PXF 如何使用 Amazon S3 Select 服务读取存储在 S3 上的 CSV 和 Parquet 文件的具体信息，请参阅[使用 S3 Select 读取 S3 中的 CSV 和 Parquet 数据](/cloudberry/pxf/access-objectstores/read_s3_s3select/)。
