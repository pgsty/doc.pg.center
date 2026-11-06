---
title: "故障排查"
linkTitle: "PXF 故障排查"
description: "PXF 故障排查：日志、常见错误和内存问题。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/troubleshooting/troubleshooting_pxf.md"
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


## PXF 错误 {#pxf-errors}
下表描述了使用 PXF 时可能遇到的一些错误：

| 错误消息                 | 说明                     |
|-------------------------------|---------------------------------|
| Protocol "pxf" does not exist | **原因**：未注册 `pxf` 扩展。<br/>**解决方法**：按照 PXF [启用步骤](/cloudberry/pxf/administering/using_pxf/#enabling-pxf-in-a-database)中的说明，为数据库创建（启用）PXF 扩展。|
| Invalid URI pxf://\<path-to-data\>: missing options section | **原因**：`LOCATION` URI 未包含 Profile 或其他必需选项。<br/>**解决方法**：提交 `CREATE EXTERNAL TABLE` 命令时，在 URI 中提供 Profile 和必需选项。 |
| PXF server error : Input path does not exist: hdfs://\<namenode\>:8020/\<path-to-file\> | **原因**：您在 \<path-to-file\> 中指定的 HDFS 文件不存在。 <br/>**解决方法**：提供现有 HDFS 文件的路径。 |
| PXF server error : NoSuchObjectException(message:\<schema\>.\<hivetable\> table not found) | **原因**：您通过 \<schema\>.\<hivetable\> 指定的 Hive 表不存在。 <br/>**解决方法**：提供现有 Hive 表的名称。 |
| PXF server error : Failed connect to localhost:5888; Connection refused (\<segment-id\> slice\<N\> \<segment-host\>:\<port\> pid=\<process-id\>)<br/> ... |**原因**：PXF 服务未在 \<segment-host\> 上运行。<br/>**解决方法**：在 \<segment-host\> 上重启 PXF。 |
| PXF server error: Permission denied: user=\<user\>, access=READ, inode=&quot;\<filepath\>&quot;:-rw------- | **原因**：运行 PXF 操作的 Apache Cloudberry 用户没有访问底层 Hadoop 服务（HDFS 或 Hive）的权限。请参见[配置 Hadoop 用户、用户模拟和代理](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxfuserimpers/)。 |
| PXF server error: PXF service could not be reached. PXF is not running in the tomcat container | **原因**：`pxf` 扩展已更新到新版本，但 PXF 服务器尚未更新到兼容版本。 <br/>**解决方法**：确保已在所有主机上更新并重启 PXF 服务器。 |
| ERROR: could not load library "/usr/local/cloudberry-db-x.x.x/lib/postgresql/pxf.so" | **原因**：Apache Cloudberry 升级或迁移后，某些步骤（例如 `pxf cluster register`）尚未完成。 <br/>**解决方法**：请确保遵循 [PXF 升级与迁移](/cloudberry/pxf/upgrade/)中概述的步骤。 | 

大多数 PXF 错误消息都包含 `HINT`，可用于解决错误，或收集更多信息以定位错误。

## PXF 日志 {#pxf-logging}

有关日志级别、配置以及 `pxf-app.out` 和 `pxf-service.log` 日志文件的更多信息，请参阅[日志](/cloudberry/pxf/administering/advanced-config/cfg_logging/)主题。


## 解决 PXF JDBC 连接器时区错误 {#addressing-pxf-jdbc-connector-time-zone-errors}

您使用 PXF JDBC 连接器访问存储在外部 SQL 数据库中的数据。取决于 JDBC 驱动程序，如果 PXF 服务的默认时区与外部 SQL 数据库设置的时区不一致，驱动程序可能会返回错误。

例如，如果您使用 PXF JDBC 连接器访问时区冲突的 Oracle 数据库，PXF 会记录类似如下的错误：

```text
java.io.IOException: ORA-00604: error occurred at recursive SQL level 1
ORA-01882: timezone region not found
```

遇到此错误时，可以在 `$PXF_BASE/conf/pxf-env.sh` 配置文件的 `PXF_JVM_OPTS` 属性设置中，为 PXF 服务设置默认时区选项。例如，设置时区：

```text
export PXF_JVM_OPTS="<current_settings> -Duser.timezone=America/Chicago"
```

您也可以使用 `PXF_JVM_OPTS` 属性设置其他 Java 选项。

如前面各节所述，您必须将更新后的 PXF 配置同步到 Apache Cloudberry 集群，并在每台主机上重启 PXF 服务。


## 关于 PXF 外部表子分区 {#about-pxf-external-table-child-partitions}

Apache Cloudberry 支持分区表，并允许将叶子子分区与 PXF 外部表交换。

当您从分区的 Apache Cloudberry 表读取，且其中一个或多个分区是 PXF 外部表，而该外部表路径下没有支撑数据时，PXF 会返回错误，查询随之失败。在分区表场景下，PXF 的这一默认行为并不理想；空的子分区是有效的，不应导致对父表的查询失败。

`IGNORE_MISSING_PATH` PXF 自定义选项是一个布尔值，用于指定外部表路径缺失或无效时采取的操作。默认值为 `false`，即 PXF 遇到缺失路径时返回错误。如果外部表是 Apache Cloudberry 表的子分区，您希望 PXF 忽略缺失路径错误，则应将此选项设置为 `true`。

例如，PXF 会忽略下面这个外部表产生的缺失路径错误：

```sql
CREATE EXTERNAL TABLE ext_part_87 (id int, some_date date)
  LOCATION ('pxf://bucket/path/?PROFILE=s3:parquet&SERVER=s3&IGNORE_MISSING_PATH=true')
FORMAT 'CUSTOM' (formatter = 'pxfwritable_import');
```

`IGNORE_MISSING_PATH` 自定义选项仅适用于基于文件的 Profile，包括 `*:text`、`*:csv`、`*:fixedwidth`、`*:parquet`、`*:avro`、`*:json`、`*:AvroSequenceFile` 和 `*:SequenceFile`。当外部表指定 `hbase`、`hive[:*]` 或 `jdbc` Profile，或使用 S3-Select 从 S3 读取时，该选项*不可用*。


## 解决 Hive MetaStore 连接错误 {#addressing-hive-metastore-connection-errors}

PXF Hive 连接器使用 Hive MetaStore 来确定 Hive 表的 HDFS 位置。从 PXF 6.2.1 版本开始，PXF 会对失败的 Hive MetaStore 连接重试一次。如果通过 PXF 外部表访问 Hive 时遇到以下任一错误消息或异常，请考虑增加重试次数：

- `Failed to connect to the MetaStore Server.`
- `Could not connect to meta store ...`
- `org.apache.thrift.transport.TTransportException: null`

PXF 使用 `hive-site.xml` 的 `hive.metastore.failure.retries` 属性设置来确定重试失败的 Hive MetaStore 连接的最大次数。`hive-site.xml` 文件位于您用来访问 Hive 的 PXF 服务器的配置目录中。

执行以下步骤配置 PXF 尝试的 Hive MetaStore 连接重试次数；您可能需要将 `hive.metastore.failure.retries` 属性添加到 `hive-site.xml` 文件中：

1. 登录 Apache Cloudberry Coordinator 主机。

1. 确定您的 Hive PXF 服务器的名称。

1. 在您选择的编辑器中打开 `$PXF_BASE/servers/<hive-server-name>/hive-site.xml` 文件，如果文件中尚不存在 `hive.metastore.failure.retries` 属性，则添加该属性，并设置其值。例如，配置 5 次重试： 

    ```xml
    <property>
        <name>hive.metastore.failure.retries</name>
        <value>5</value>
    </property>
    ```

1. 保存文件并退出编辑器。

1. 将 PXF 配置同步到 Apache Cloudberry 集群中的所有主机：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 重新运行失败的 SQL 外部表命令。

## 解决缺少压缩编解码器的错误 {#addressing-a-missing-compression-codec-error}

默认情况下，PXF 不打包 LZO 压缩库。如果 Hadoop 集群配置为使用 LZO 压缩，PXF 会在首次访问 Hadoop 时返回错误消息 `Compression codec com.hadoop.compression.lzo.LzoCodec not found`。要解决此问题，您必须按如下所述向 PXF 注册 LZO 压缩库（更多信息请参阅[注册 JAR 依赖](/cloudberry/pxf/administering/reg_jar_depend/#registering-a-jar-dependency)）：

1. 在 Hadoop NameNode 的 Hadoop 安装目录中找到 LZO 库。例如，该库在文件系统中的位置可能是 `/usr/lib/hadoop-lzo/lib/hadoop-lzo.jar`。

1. 登录 Apache Cloudberry Coordinator 主机。

1. 将 `hadoop-lzo.jar` 从 Hadoop NameNode 复制到 Apache Cloudberry Coordinator 主机上的 PXF 配置目录。例如，如果 `$PXF_BASE` 为 `/usr/local/cloudberry-pxf`：

    ```shell
    gpadmin@coordinator$ scp <hadoop-user>@<namenode-host>:/usr/lib/hadoop-lzo/lib/hadoop-lzo.jar /usr/local/cloudberry-pxf/lib/
    ```

1. 同步 PXF 配置并重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster restart
    ```

1. 重新运行查询。

## 解决 Snappy 压缩初始化错误 {#addressing-a-snappy-compression-initialization-error}

Snappy 压缩需要一个可执行的临时目录来加载其本地库。如果您使用 PXF 读取或写入经 Snappy 压缩的 Avro、ORC 或 Parquet 文件，并遇到错误 `java.lang.NoClassDefFoundError: Could not initialize class org.xerial.snappy.Snappy`，则 Snappy 使用的临时目录（默认为 `/tmp`）可能不可执行。

要解决此问题，请为 Snappy 的 `tempdir` 指定一个可执行目录。此过程包括停止 PXF、更新 PXF 配置、同步配置更改，然后重启 PXF，步骤如下：

1. 确定 `/tmp` 目录是否可执行：

    ```shell
    $ mount | grep '/tmp'
    tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,seclabel)
    ```

    `mount` 输出中出现 `noexec` 选项表示该目录不可执行。

    请在每台 Apache Cloudberry 主机上执行此检查。

1. 如果 `/tmp` 的 `mount` 命令输出中不包含 `noexec`，则该目录是可执行的。请退出此过程，该解决方法无法解决您的问题。

    如果 `/tmp` 的 `mount` 命令输出中包含 `noexec`，请继续。

1. 登录 Apache Cloudberry Coordinator 主机。

1. 在 Apache Cloudberry 集群上停止 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster stop
    ```

1.  在 PXF 安装中找到 `pxf-env.sh` 文件。如果您没有迁移 `$PXF_BASE`，该文件位于：

    ```text
    /usr/local/cloudberry-pxf/conf/pxf-env.sh
    ```

1.  在您选择的编辑器中打开 `pxf-env.sh`，找到设置 `PXF_JVM_OPTS` 的行，如果该行尚未取消注释则取消注释，并在该设置中添加 `-Dorg.xerial.snappy.tempdir=${PXF_BASE}/run`。例如：

    ```shell
    # Memory
    export PXF_JVM_OPTS="-Xmx2g -Xms1g -Dorg.xerial.snappy.tempdir=${PXF_BASE}/run"
    ```

    此选项将 Snappy 临时目录设置为 `${PXF_BASE}/run`，这是 PXF 可访问的可执行目录。

1.  同步 PXF 配置，然后重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster start
    ```

## 从 STORED AS ORC 的 Hive 表读取返回 NULL {#reading-from-a-hive-table-stored-as-orc-returns-nulls}

如果您使用 PXF 读取 `STORED AS ORC` 的 Hive 表，并且一个或多个有值的列返回 NULL，则可能是 Hive 表定义中指定的列名与 ORC 内嵌模式定义中指定的列名之间存在大小写敏感问题。如果该表由 Spark 等其他系统创建并填充，就可能出现这种情况。

本节所述的解决方法适用于以下所有条件均成立的情况：

- 您创建的 Apache Cloudberry PXF 外部表指定了 `hive:orc` Profile。
- 您创建的 Apache Cloudberry PXF 外部表指定了 `VECTORIZE=false`（默认）设置。
- Hive 表模式中指定的列名与 ORC 内嵌模式中指定的列名大小写不一致。
- 您通过执行以下任务，确认 ORC 内嵌模式中的字段名并非全部为小写：
    1. 在 `hive` 子系统中运行 `DESC FORMATTED <table-name>`，并记下返回的 `location`；例如 `location:hdfs://namenode/hive/warehouse/<table-name>`。
    1. 运行以下命令，列出构成该表的 ORC 文件：

        ```shell
        $ hdfs dfs -ls <location>
        ```
    1. 使用以下命令转储每个 ORC 文件。例如，如果第一步返回 `hdfs://namenode/hive/warehouse/hive_orc_tbl1, run:`，则运行：

        ```shell
        $ hive --orcfiledump /hive/warehouse/hive_orc_tbl1/<orc-file> > dump.out
        ```
    1. 检查输出，特别是 `Type` 的值（示例输出：`Type: struct<COL0:int,COL1:string>`）。如果字段名并非全部为小写，请继续执行下面的解决方法。

*要解决此问题，请执行以下步骤*：

1. 登录 Apache Cloudberry Coordinator 主机。

1. 确定您的 Hadoop PXF 服务器配置的名称。

1. 在服务器配置目录中找到 `hive-site.xml` 配置文件。例如，如果 `$PXF_BASE` 为 `/usr/local/cloudberry-pxf`，服务器名称为 `<server_name>`，则该文件位于：

    ```text
    /usr/local/cloudberry-pxf/servers/<server_name>/hive-site.xml
    ```

1. 在 `hive-site.xml` 文件中添加或更新以下属性定义，然后保存并退出编辑器：

    ```xml
    <property>
        <name>orc.schema.evolution.case.sensitive</name>
        <value>false</value>
        <description>A boolean flag to determine if the comparision of field names in schema evolution is case sensitive.</description>
    </property>
    ```

1. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ````

1. 再次尝试该查询。
