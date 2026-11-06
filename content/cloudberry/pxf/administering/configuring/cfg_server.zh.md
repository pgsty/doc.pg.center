---
title: "配置 PXF 服务器"
description: "配置具名 PXF 服务器。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/cfg_server.md"
---

本主题概述 PXF 服务器配置。要配置某个服务器，请参阅与要配置的连接器对应的主题。

你通过 PXF 连接器从外部数据存储读取数据或向其写入数据。要访问外部数据存储，必须提供服务器位置。你还可能需要提供客户端访问凭据以及其他特定于该外部数据存储的属性。PXF 通过以下方式简化外部数据存储访问的配置：

- 支持基于文件的连接器和用户配置
- 提供特定于连接器的模板配置文件

PXF *服务器（Server）* 定义就是一份提供特定外部数据存储访问能力的具名配置。PXF 服务器名称就是位于 `$PXF_BASE/servers/` 中的某个目录的名称。你在服务器配置中提供的信息特定于连接器。例如，PXF JDBC 连接器的服务器定义可以包含 JDBC 驱动类名、URL、用户名和密码等设置。你还可以在 JDBC 服务器定义中配置特定于连接和特定于会话的属性。

PXF 为每个连接器提供了一个服务器模板文件；该模板列出了使用该连接器时通常必须配置的一组属性。

你需要为 Apache Cloudberry 用户需要访问的每个外部数据存储配置一个服务器定义。例如，如果需要访问两个 Hadoop 集群，则要为每个集群创建一个 PXF Hadoop 服务器配置。如果需要访问一个 Oracle 数据库和一个 MySQL 数据库，则要为每个数据库创建一个或多个 PXF JDBC 服务器配置。

服务器配置可以包含用户访问凭据以及外部数据存储其他属性的默认设置。你可以允许 Apache Cloudberry 用户使用默认设置访问外部数据存储，也可以按用户配置访问凭据和其他属性。这样，你就可以在单个 PXF 服务器定义中，为不同的 Apache Cloudberry 用户配置不同的外部数据存储访问凭据。


## 关于服务器模板文件 {#about-server-template-files}

PXF 服务器的配置信息位于 `$PXF_BASE/servers/<server_name>/` 中的一个或多个 `<connector>-site.xml` 文件内。

PXF 为每个连接器提供了一个模板配置文件。安装 PXF 之后，这些服务器模板配置文件位于 `<PXF_INSTALL_DIR>/templates/` 目录：

```
gpadmin@coordinator$ ls <PXF_INSTALL_DIR>/templates
abfss-site.xml   hbase-site.xml  jdbc-site.xml    pxf-site.xml    yarn-site.xml
core-site.xml  hdfs-site.xml   mapred-site.xml  s3-site.xml
gs-site.xml    hive-site.xml   minio-site.xml   wasbs-site.xml
```

例如，`s3-site.xml` 模板文件的内容如下：

```text
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>fs.s3a.access.key</name>
        <value>YOUR_AWS_ACCESS_KEY_ID</value>
    </property>
    <property>
        <name>fs.s3a.secret.key</name>
        <value>YOUR_AWS_SECRET_ACCESS_KEY</value>
    </property>
    <property>
        <name>fs.s3a.fast.upload</name>
        <value>true</value>
    </property>
</configuration>
```

<b>注意：</b>你在配置文件中以明文形式向 PXF 指定凭据。

**注意**：Hadoop 连接器的模板文件不应直接修改并用于配置，因为它们仅提供所需信息的示例。你不需要修改 Hadoop 模板，而是要将 Hadoop 集群中的若干 Hadoop `*-site.xml` 文件复制到 PXF Hadoop 服务器配置中。


## 关于默认服务器 {#about-the-default-server}

PXF 定义了一个名为 `default` 的特殊服务器。PXF 安装会创建 `$PXF_BASE/servers/default/` 目录。该目录最初为空，用于标识默认的 PXF 服务器配置。你可以配置默认 PXF 服务器，并将其指派给任何外部数据源。例如，你可以将 PXF 默认服务器指派给某个 Hadoop 集群，或用户经常访问的某个 MySQL 数据库。

如果在 `CREATE EXTERNAL TABLE` 命令的 `LOCATION` 子句中省略 `SERVER=<server_name>` 设置，PXF 会自动使用 `default` 服务器配置。


## 配置服务器 {#configuring-a-server}

为连接外部数据存储而配置 PXF 连接器时，需要为该连接器添加一个具名 PXF 服务器配置。你要执行的任务可能包括：

1. 确定是配置 `default` PXF 服务器，还是为服务器配置选择新名称。
2. 创建目录 `$PXF_BASE/servers/<server_name>`。
3. 将模板或其他配置文件复制到新的服务器目录。
4. 为模板文件中的属性填入适当的默认值。
5. 添加你的环境所需的任何其他配置属性和值。
6. 按照[关于配置 PXF 用户](#configuring-a-pxf-user)中的说明，为该服务器配置一个或多个用户。
7. 将服务器和用户配置同步到 Apache Cloudberry 集群。

**注意**：添加或更新 PXF 服务器配置后，必须将 PXF 配置重新同步到 Apache Cloudberry 集群。

配置 PXF 服务器后，将服务器名称发布给需要访问该数据存储的 Apache Cloudberry 用户。用户创建访问外部数据存储的外部表时，只需提供服务器名称。PXF 会从由该服务器名称标识的服务器配置目录下的服务器配置文件和用户配置文件中获取外部数据源位置和访问凭据。

要配置 PXF 服务器，请参阅连接器配置主题：

- 要为 Hadoop 配置 PXF 服务器，请参阅[配置 PXF Hadoop 连接器](/cloudberry/pxf/administering/configuring/hadoop-connectors/)。
- 要为对象存储配置 PXF 服务器，请参阅[配置 MinIO、AWS S3 和 Dell ECS 对象存储连接器](/cloudberry/pxf/administering/configuring/s3_objstore_cfg/)以及[配置 Azure 和 Google Cloud Storage 对象存储连接器](/cloudberry/pxf/administering/configuring/objstore_cfg/)。
- 要配置 PXF JDBC 服务器，请参阅[配置 JDBC 连接器](/cloudberry/pxf/administering/configuring/jdbc-connector/)。
- [配置 PXF 网络文件系统服务器](/cloudberry/pxf/access-nfs/#configuring-a-pxf-network-file-system-server)介绍了为网络文件系统访问配置 PXF 服务器的过程。

## 关于 pxf-site.xml 配置文件 {#about-the-pxf-sitexml-configuration-file}

PXF 包含一个名为 `pxf-site.xml` 的模板文件，用于 PXF 特有的配置参数。你可以使用 `pxf-site.xml` 模板文件配置：

- 服务器配置的 Kerberos 和/或用户模拟设置
- 文件访问的基础目录
- PXF 在写入数值型 ORC 或 Parquet 数据时检测到溢出状况后的处理动作

<b>注意：</b>此文件中的 Kerberos 和用户模拟设置可能仅适用于 Hadoop 和 JDBC 服务器配置；它们不适用于文件系统或对象存储服务器配置。

当以下一个或多个条件成立时，需要为 PXF 服务器在 `pxf-site.xml` 文件中配置属性：

- 远程 Hadoop 系统使用 Kerberos 认证。
- 你想在远程 Hadoop 或外部数据库系统上启用/停用用户模拟。
- 你想为 Hadoop PXF 服务器启用/停用 Kerberos 约束委派。
- 你将使用该服务器配置访问网络文件系统。
- 你将使用该服务器配置访问远程 Hadoop 或对象存储文件系统，并且希望只允许用户访问特定目录及其子目录。

`pxf-site.xml` 包含以下属性：

| 属性 | 说明 | 默认值 |
|----------------|--------------------------------------------|---------------|
| pxf.service.kerberos.principal | Kerberos 主体名称。 | gpadmin/\_HOST@EXAMPLE.COM |
| pxf.service.kerberos.keytab | Kerberos keytab 文件的文件系统路径。 | $PXF_BASE/keytabs/pxf.service.keytab |
| pxf.service.kerberos.constrained-delegation | 启用/停用 [Kerberos 约束委派](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxf_kerbhdfs/#about-kerberos-constrained-delegation)。**注意：** 此属性仅适用于 Hadoop PXF 服务器配置，不适用于 JDBC PXF 服务器。 | false |
| pxf.service.kerberos.ticket-renew-window| PXF 尝试续期/刷新 Kerberos 票据所需经过的最短生命周期（以百分比表示）。取值范围为 0（PXF 为所有请求生成新票据）到 1（PXF 在票据完整生命周期结束后续期）。 | 0.8 (80%) |
| pxf.service.user.impersonation | 启用/停用连接远程系统时的用户模拟。 | 如果 `pxf-site.xml` 中缺少 `pxf.service.user.impersonation` 属性，则对 PXF Hadoop 服务器默认为 `true`（启用），对 JDBC 服务器默认为 `false`（停用）。 |
| pxf.service.user.name | 远程系统的登录用户。 | 此属性默认被注释掉。属性未设置时，默认值为启动 pxf 进程的操作系统用户，通常是 `gpadmin`。属性已设置时，默认值取决于用户模拟设置，以及（访问 Hadoop 时）是否访问受 Kerberos 保护的集群；请参阅*配置 Hadoop 用户、用户模拟和代理*主题中的[用例和配置场景](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxfuserimpers/#use-cases-and-configuration-scenarios)一节。 |
| pxf.fs.basePath | 标识远程文件系统上的基础路径或共享点。当服务器配置与访问文件的 Profile 一起使用时，此属性适用。 | 无；此属性默认被注释掉。 |
| pxf.ppd.hive<sup>1</sup> | 指定对指定了 `hive`、`hive:rc` 或 `hive:orc` Profile 的外部表执行查询时，是否启用谓词下推。 | True；启用谓词下推。 |
| pxf.sasl.connection.retries | 指定在连接被拒绝并返回 `GSS initiate failed` 错误后，PXF 重试 SASL 连接请求的最大次数。 | 5 |
| pxf.orc.write.decimal.overflow | 指定向 ORC 文件写入时，PXF 如何处理超过最大精度 38 而[溢出](/cloudberry/pxf/access-hadoop/hdfs_orc/#understanding-overflow-conditions-when-writing-numeric-data)的数值数据。有效值为：round、error 或 ignore | round |
| pxf.parquet.write.decimal.overflow | 指定向 Parquet 文件写入时，PXF 如何处理超过最大精度 38 而[溢出](/cloudberry/pxf/access-hadoop/hdfs_parquet/#understanding-overflow-conditions-when-writing-numeric-data)的数值数据。有效值为：round、error 或 ignore | round |

<br/><sup>1</sup>&nbsp;如有需要，可以在创建外部表时，通过在 `LOCATION` 子句中指定 `&PPD=<boolean>` 选项，按表覆盖此设置。

有关 Hadoop 和 JDBC 服务器配置中相关的 `pxf-site.xml` 属性设置，请分别参阅[配置 PXF Hadoop 连接器](/cloudberry/pxf/administering/configuring/hadoop-connectors/)和[配置 JDBC 连接器](/cloudberry/pxf/administering/configuring/jdbc-connector/)。有关配置 PXF 服务器以访问网络文件系统时相关的 `pxf-site.xml` 属性设置，请参阅[配置 PXF 网络文件系统服务器](/cloudberry/pxf/access-nfs/#configuring-a-pxf-network-file-system-server)。

### 关于 pxf.fs.basePath 属性 {#about-the-pxffsbasepath-property}

你可以使用 `pxf.fs.basePath` 属性，将用户对文件的访问限制在特定的远程目录内。设置后，此属性适用于任何访问文件的 Profile，包括 `*:text`、`*:parquet`、`*:json` 等。

为服务器配置 `pxf.fs.basePath` 属性后，PXF 会将 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中指定的文件路径视为相对于此基础路径设置，并据此构造远程路径。

> <b>注意：</b>当你配置 PXF 服务器以通过 `file:*` Profile 访问网络文件系统时，必须设置 `pxf.fs.basePath`。对于访问 Hadoop 或对象存储中文件的 PXF 服务器，此属性是可选的。


## 配置 PXF 用户 {#configuring-a-pxf-user}

你可以按服务器、按 Apache Cloudberry 用户配置对外部数据存储的访问。

> <b>注意：</b>PXF 按服务器、按用户的配置对 JDBC 服务器最有价值。

你通过在 PXF 服务器配置目录 `$PXF_BASE/servers/<server_name>/` 中提供 `<cloudberry_user_name>-user.xml` 用户配置文件，为特定的 Apache Cloudberry 用户配置外部数据存储的用户访问凭据和属性。例如，你在文件 `$PXF_BASE/servers/<server_name>/bill-user.xml` 中指定名为 `bill` 的 Apache Cloudberry 用户的属性。一个 PXF 服务器配置中可以配置零个、一个或多个用户。


你在用户配置文件中指定的属性特定于连接器。你可以在 `<cloudberry_user_name>-user.xml` 配置文件中指定 PXF 连接器服务器支持的任何配置属性。

例如，假设你已在名为 `pgsrv1` 的 PXF JDBC 服务器配置中配置了对某个 PostgreSQL 数据库的访问。要允许名为 `bill` 的 Apache Cloudberry 用户以名为 `pguser1`、密码为 `changeme` 的 PostgreSQL 用户身份访问该数据库，需要创建用户配置文件 `$PXF_BASE/servers/pgsrv1/bill-user.xml`，其中包含以下属性：

```xml
<configuration>
    <property>
        <name>jdbc.user</name>
        <value>pguser1</value>
    </property>
    <property>
        <name>jdbc.password</name>
        <value>changeme</value>
    </property>
</configuration>
```

如果要为 `bill` 配置特定的搜索路径和更大的读取获取大小，还需要将以下属性添加到 `bill-user.xml` 用户配置文件中：

```xml
    <property>
        <name>jdbc.session.property.search_path</name>
        <value>bill_schema</value>
    </property>
    <property>
        <name>jdbc.statement.fetchSize</name>
        <value>2000</value>
    </property>
```

### 步骤 {#procedure}

对于要配置的每个 PXF 用户，你需要：

1. 确定 Apache Cloudberry 用户的名称。
2. 确定要为其配置用户访问的 PXF 服务器定义。
3. 确定要为该用户配置的每个属性的名称和值。
4. 创建/编辑文件 `$PXF_BASE/servers/<server_name>/<cloudberry_user_name>-user.xml`，并添加外层 configuration 块：

    ```xml
    <configuration>
    </configuration>
    ```
5. 将第 3 步中确定的每个属性/值对添加到 `<cloudberry_user_name>-user.xml` 文件的 configuration 块内。
6. 如果是将 PXF 用户配置添加到先前已配置的 PXF 服务器定义中，请将用户配置同步到 Apache Cloudberry 集群。


## 关于配置属性优先级 {#about-configuration-property-precedence}

PXF 服务器配置可以包含用户访问凭据以及访问外部数据存储所需的其他属性的默认设置。某些 PXF 连接器（例如 S3 和 JDBC 连接器）允许你通过 `CREATE EXTERNAL TABLE` 命令 `LOCATION` 子句中的自定义选项直接指定某些服务器属性。`<cloudberry_user_name>-user.xml` 文件则指定特定于某个 Apache Cloudberry 用户的外部数据存储属性设置。

对于给定的 Apache Cloudberry 用户，PXF 使用以下优先级规则（从高到低）获取该用户的配置属性设置：

1. 在 `<server_name>/<cloudberry_user_name>-user.xml` 中配置的属性会覆盖其他任何位置对该属性的设置。
2. 通过 `CREATE EXTERNAL TABLE` 命令 `LOCATION` 子句中的自定义选项指定的属性，会覆盖 PXF 服务器配置中对该属性的任何设置。
3. 在 `<server_name>` PXF 服务器定义中配置的属性标识默认属性值。

借助这些优先级规则，你可以创建一个可供多个 Apache Cloudberry 用户访问的外部表，每个用户使用各自独有的外部数据存储用户凭据。


## 使用服务器配置 {#using-a-server-configuration}

要访问外部数据存储，Apache Cloudberry 用户需在 `CREATE EXTERNAL TABLE` 命令 `LOCATION` 子句的 `SERVER=<server_name>` 选项中指定服务器名称。用户提供的 `<server_name>` 标识服务器配置目录，PXF 从该目录获取访问外部数据存储所需的配置和凭据。

例如，以下命令使用 `$PXF_BASE/servers/s3srvcfg/s3-site.xml` 文件中定义的服务器配置访问 S3 对象存储：

```text
CREATE EXTERNAL TABLE pxf_ext_tbl(name text, orders int)
  LOCATION ('pxf://BUCKET/dir/file.txt?PROFILE=s3:text&SERVER=s3srvcfg')
FORMAT 'TEXT' (delimiter=E',');
```

未提供 `SERVER=<server_name>` 设置时，PXF 会自动使用 `default` 服务器配置。

例如，如果 `default` 服务器配置标识的是一个 Hadoop 集群，则以下示例命令引用位于 `/path/to/file.txt` 的 HDFS 文件：

```text
CREATE EXTERNAL TABLE pxf_ext_hdfs(location text, miles int)
  LOCATION ('pxf://path/to/file.txt?PROFILE=hdfs:text')
FORMAT 'TEXT' (delimiter=E',');
```

> <b>注意：</b>查询外部表或向其写入数据的 Apache Cloudberry 用户，使用为 <code>&lt;server_name></code> 用户配置的凭据访问外部数据存储。如果没有为 <code>&lt;server_name></code> 配置特定于用户的凭据，则该 Apache Cloudberry 用户使用为 <code>&lt;server_name></code> 配置的默认凭据访问外部数据存储。
