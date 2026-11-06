---
title: "配置 Hadoop 连接器（可选）"
linkTitle: "配置 PXF Hadoop 连接器（可选）"
description: "配置 PXF Hadoop 连接器（可选）。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/hadoop-connectors/client_instcfg.md"
---

PXF 兼容 Cloudera、Hortonworks Data Platform 以及通用的 Apache Hadoop 发行版。本主题介绍如何配置 PXF 的 Hadoop、Hive 和 HBase 连接器。

*如果不打算使用与 Hadoop 相关的 PXF 连接器，则无需执行此过程。*

## 前提条件 {#prerequisites}

配置 PXF Hadoop 连接器需要将 Hadoop 集群中的配置文件复制到 Apache Cloudberry 的 Coordinator 主机。在配置 PXF Hadoop 连接器之前，请确保可以将文件从 Hadoop 集群中的主机复制到 Apache Cloudberry Coordinator。


## 操作步骤 {#procedure}

请执行以下步骤，在 Apache Cloudberry Coordinator 主机上配置所需的、与 Hadoop 相关的 PXF 连接器。配置完连接器后，您将使用 `pxf cluster sync` 命令将 PXF 配置复制到 Apache Cloudberry 集群。

在此过程中，您可以使用 `default` 服务器配置，也可以创建新的 PXF 服务器配置。您需要将 Hadoop 配置文件复制到 Apache Cloudberry Coordinator 主机上的服务器配置目录，并确定访问所需的 Kerberos 和用户模拟设置（如适用）。然后，将 Coordinator 主机上的 PXF 配置同步到 Standby Coordinator 主机和 Segment 主机。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 确定 PXF Hadoop 服务器配置的名称。

3. 如果不使用 `default` PXF 服务器，请创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令创建名为 `hdp3` 的 Hadoop 服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/hdp3
    ````

4. 切换到服务器目录。例如：

    ```shell
    gpadmin@coordinator$ cd $PXF_BASE/servers/default
    ```

    或者：

    ```shell
    gpadmin@coordinator$ cd $PXF_BASE/servers/hdp3
    ```

2. PXF 需要 `core-site.xml` 和其他 Hadoop 配置文件中的信息。请使用您选择的工具，将 `core-site.xml`、`hdfs-site.xml`、`mapred-site.xml` 和 `yarn-site.xml` Hadoop 配置文件从 Hadoop 集群的 NameNode 主机复制到当前主机。文件路径可能因所用的 Hadoop 发行版而异。例如，以下命令使用 `scp` 复制这些文件：

    ```shell
    gpadmin@coordinator$ scp hdfsuser@namenode:/etc/hadoop/conf/core-site.xml .
    gpadmin@coordinator$ scp hdfsuser@namenode:/etc/hadoop/conf/hdfs-site.xml .
    gpadmin@coordinator$ scp hdfsuser@namenode:/etc/hadoop/conf/mapred-site.xml .
    gpadmin@coordinator$ scp hdfsuser@namenode:/etc/hadoop/conf/yarn-site.xml .
    ```
        
3. 如果计划使用 PXF Hive 连接器访问 Hive 表数据，请同样将 Hive 配置复制到 Apache Cloudberry Coordinator 主机。例如：

    ```shell
    gpadmin@coordinator$ scp hiveuser@hivehost:/etc/hive/conf/hive-site.xml .
    ```

4. 如果计划使用 PXF HBase 连接器访问 HBase 表数据，请同样将 HBase 配置复制到 Apache Cloudberry Coordinator 主机。例如：
    
    ```shell
    gpadmin@coordinator$ scp hbaseuser@hbasehost:/etc/hbase/conf/hbase-site.xml .
    ```

5. 将 PXF 配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

4. PXF 代表 Apache Cloudberry 最终用户访问 Hadoop 服务。默认情况下，PXF 会尝试使用登录 Apache Cloudberry 的用户账户的身份访问 HDFS、Hive 和 HBase。为支持此功能，必须为 Hadoop 配置代理设置；如果打算使用 Hive 和 HBase 的 PXF 连接器，也必须为 Hive 和 HBase 配置代理设置。请按照[配置用户模拟与代理](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxfuserimpers/)中的步骤，为 Hadoop 服务配置用户模拟和代理，或关闭 PXF 用户模拟。

5. 为将在 Apache Cloudberry 中作为外部表访问的 HDFS 文件和目录授予读取权限。如果启用了用户模拟（默认），则必须向每个会使用引用这些 HDFS 文件的外部表的 Apache Cloudberry 用户/角色名授予此权限。如果未启用用户模拟，则必须向 `gpadmin` 用户授予此权限。

6. 如果 Hadoop 集群使用 Kerberos 保护，则必须按照[为安全 HDFS 配置 PXF](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxf_kerbhdfs/)中的说明配置 PXF，并为每个 Apache Cloudberry 主机生成 Kerberos 主体和密钥表（keytab）。


## 关于更新 Hadoop 配置 {#about-updating-the-hadoop-configuration}

如果在 PXF 服务运行期间更新了 Hadoop、Hive 或 HBase 配置，则必须将更新后的配置复制到 `$PXF_BASE/servers/<server_name>` 目录，并将 PXF 配置重新同步到 Apache Cloudberry 集群。例如：

```shell
gpadmin@coordinator$ cd $PXF_BASE/servers/<server_name>
gpadmin@coordinator$ scp hiveuser@hivehost:/etc/hive/conf/hive-site.xml .
gpadmin@coordinator$ pxf cluster sync
```
