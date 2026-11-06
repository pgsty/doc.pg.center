---
title: "配置 PXF"
description: "安装后配置 PXF。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/instcfg_pxf.md"
---

Apache Cloudberry 部署由一台 Coordinator 主机、一台 Standby Coordinator 主机和多台 Segment 主机组成。配置 Apache Cloudberry Platform Extension Framework (PXF) 之后，你需要在每台 Apache Cloudberry 主机上启动一个 PXF JVM 进程（PXF Service）。

PXF 提供了连接 Hadoop、Hive、HBase、对象存储、网络文件系统和外部 SQL 数据存储的连接器。你必须配置 PXF，以支持计划使用的连接器。

要配置 PXF，必须：

1. 按照[为 PXF 安装 Java](/cloudberry/pxf/administering/configuring/install_java/)中的说明，在每台 Apache Cloudberry 主机上安装 Java 8 或 11。如果 `JAVA_HOME` 不是 `/usr/java/default`，则必须在 `pxf-env.sh` [配置文件](/cloudberry/pxf/administering/configuring/config_files/)中指定其值，以告知 PXF `$JAVA_HOME` 的设置。
    - 在 Apache Cloudberry Coordinator 主机上编辑 `$PXF_BASE/conf/pxf-env.sh` 文件。

        ```shell
        gpadmin@coordinator$ vi /usr/local/cloudberry-pxf/conf/pxf-env.sh
        ```
    - 在 `pxf-env.sh` 文件中找到 `JAVA_HOME` 设置，必要时取消注释，并将其设置为你的 `$JAVA_HOME` 值。例如：

        ```
        export JAVA_HOME=/usr/lib/jvm/jre
        ```

1. 向 Apache Cloudberry 注册 PXF 扩展（参见 [pxf cluster register](/cloudberry/pxf/ref/pxf-cluster/)）。首次安装 PXF 2.1+ 版本之后，和/或升级 Apache Cloudberry 安装之后，请运行此命令：

    ```shell
    gpadmin@coordinator$ pxf cluster register
    ```

1. 如果计划使用 Hadoop、Hive 或 HBase PXF 连接器，必须执行[配置 PXF Hadoop 连接器](/cloudberry/pxf/administering/configuring/hadoop-connectors/)中描述的配置步骤。

1. 如果计划使用 PXF 连接器访问 Azure、Google Cloud Storage、MinIO 或 S3 对象存储，必须执行[配置 Azure、Google Cloud Storage、MinIO 和 S3 对象存储连接器](/cloudberry/pxf/administering/configuring/objstore_cfg/)中描述的配置步骤。

1. 如果计划使用 PXF JDBC 连接器访问外部 SQL 数据库，请执行[配置 JDBC 连接器](/cloudberry/pxf/administering/configuring/jdbc-connector/)中描述的配置步骤。

1. 如果计划使用 PXF 访问网络文件系统，请执行[配置 PXF 网络文件系统服务器](/cloudberry/pxf/access-nfs/#configuring-a-pxf-network-file-system-server)中描述的配置步骤。

1. 进行任何配置更改后，将 PXF 配置同步到集群中的所有主机。

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 同步 PXF 配置更改后，[启动 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/)。

2. 启用 [PXF 扩展](/cloudberry/pxf/administering/using_pxf/#enabling-pxf-in-a-database)并[向用户授予访问权限](/cloudberry/pxf/administering/using_pxf/#granting-a-role-access-to-pxf)。
