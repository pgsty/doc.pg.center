---
title: "为 PXF 安装 Java"
description: "为 PXF 服务安装 Java。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/docs/administering/configuring/install_java.md"
---

PXF 是一个 Java 服务。它要求每台 Apache Cloudberry 主机上安装 Java 17 或 21。


## 前提条件 {#prerequisites}

确保你有权访问每台 Apache Cloudberry 主机上的 Java，或拥有在其上安装 Java 的超级用户权限。

## 步骤 {#procedure}

请执行以下步骤，在 Apache Cloudberry 集群的 Coordinator 主机、Standby Coordinator 主机和每台 Segment 主机上安装 Java。只要可能，你将使用 `gpssh` 实用程序在多台主机上运行命令。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 确定系统上已安装的 Java 版本：

    ```text
    gpadmin@coordinator$ rpm -qa | grep java
    ```

3. 如果系统上没有安装 Java，请在 Coordinator 主机、Standby Coordinator 主机和每台 Apache Cloudberry Segment 主机上安装 Java。

    1. 创建一个文本文件，列出 Apache Cloudberry Standby Coordinator 主机和 Segment 主机，每行一个主机名。例如，名为 `gphostfile` 的文件可以包含：

        ```text
        coordinator
        mstandby
        seghost1
        seghost2
        seghost3
        ```
    2. 在每台主机上安装 Java 软件包。例如：

        ```shell
        gpadmin@coordinator$ gpssh -e -v -f gphostfile sudo yum -y install java-17-openjdk
        ```

4. 确定 PXF 使用的 Java `$JAVA_HOME` 设置。例如：

    ```shell
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk
    ```

    如果超级用户已将新安装的 Java 替代项配置为系统默认：

    ```shell
    JAVA_HOME=/usr/lib/jvm/jre
    ```

5. 记下 `$JAVA_HOME` 设置；配置 PXF 时将需要此值。
