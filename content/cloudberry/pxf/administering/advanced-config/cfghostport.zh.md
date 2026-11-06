---
title: "服务监听地址、主机与端口"
description: "配置 PXF 服务的主机和端口。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/advanced-config/cfghostport.md"
---

在默认部署拓扑中，自 PXF 6.7.0 起，PXF Service 在 Apache Cloudberry 主机上启动，并监听 `localhost:5888`。在此配置下，PXF Service 监听 Apache Cloudberry 主机上的本地流量。您可以将 PXF 配置为监听其他监听地址，也可以将其配置为监听其他端口号，或运行在其他主机上。要更改默认配置，请设置下面列出的一个或多个属性：

|   属性 |  类型 | 描述      | 默认值 |
|-------------------------|-------------------|-----|----|
|   server.address  | `pxf-application.properties` 属性 | PXF 服务器的监听地址。 | `localhost`  |
|   PXF_HOST  | 环境变量 | 运行 PXF Service 的（非 Greenpum）主机的名称或 IP 地址。 | `localhost`  |
|   PXF_PORT  | 环境变量 | PXF 服务器在该主机上监听请求的端口号。 | `5888`  |


## 配置监听地址 {#configuring-the-listen-address}

`server.address` 属性用于指定 PXF 服务监听的网络接口的 IP 地址或主机名。PXF 服务默认的监听地址为 `localhost`。您可以更改监听地址，使其他主机能够向 PXF 发送请求（例如，当您选择了[备用部署拓扑](/cloudberry/pxf/administering/deployment_topos/#alternate-deployment-topology)，或需要获取 PXF 监控数据时）。

请执行以下步骤更改 PXF 监听地址：

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 在 PXF 安装目录中找到 `pxf-application.properties` 文件。如果您没有迁移 `$PXF_BASE`，该文件位于：

    ```text
    /usr/local/cloudberry-pxf/conf/pxf-application.properties
    ```

1. 使用您选择的编辑器打开该文件，取消注释并设置以下行：

    ```text
    server.address=<new_listen_addr>
    ```

    将监听地址更改为 `0.0.0.0` 后，PXF 会监听来自所有主机的请求。

1. 保存文件并退出编辑器。

1. 同步 PXF 配置，然后重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster restart
    ```

## 配置端口号 {#configuring-the-port-number}

> <b>注意：</b>以这种方式配置服务端口号时，必须同时重启 Apache Cloudberry 和 PXF。请考虑在计划停机期间进行此项配置。

请执行以下步骤，在一台或多台 Apache Cloudberry 主机上配置 PXF 服务器的端口号：

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 对每台 Apache Cloudberry 主机执行以下操作：

    1. 确定希望 PXF Service 监听的端口号。
    1. 登录该 Apache Cloudberry 主机：

        ```shell
        $ ssh gpadmin@<seghost>
        ```
    1. 使用您选择的编辑器打开 `~/.bashrc` 文件。
    1. 设置 `PXF_PORT` 环境变量。例如，要将 PXF Service 的端口号设置为 5998，请在 `.bashrc` 文件中添加以下内容：

        ```shell
        export PXF_PORT=5998
        ```
    1. 保存文件并退出编辑器。

1. 执行刚刚更新的 `.bashrc` 文件：

    ```shell
    gpadmin@coordinator$ source ~/.bashrc
    ```

3. 按照 Apache Cloudberry 文档中[重启 Apache Cloudberry](/cloudberry/database-basic/start-and-stop-cbdb-database/) 的说明重启 Apache Cloudberry。

4. 在每台 Apache Cloudberry 主机上重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```

5. 按照[关于 PXF 服务运行时监控](/cloudberry/pxf/administering/monitor_pxf/#about-pxf-service-runtime-monitoring)中的说明，通过访问 `http://<PXF_HOST>:<PXF_PORT>/actuator/health` 查看 PXF 监控信息，验证 PXF 正运行在重新配置的端口上。


## 配置主机 {#configuring-the-host}

如果您为 PXF 选择了[备用部署拓扑](/cloudberry/pxf/administering/deployment_topos/#alternate-deployment-topology)，则必须在每台 Apache Cloudberry Segment 主机上设置 `PXF_HOST` 环境变量，以告知 Apache Cloudberry PXF 服务的位置。您还必须按照[配置监听地址](#configuring-the-listen-address)中的说明设置监听地址。

请执行以下步骤，在每台 Apache Cloudberry Segment 主机上配置 PXF 主机：

> <b>注意：</b>以这种方式配置主机时，必须重启 Apache Cloudberry。请考虑在计划停机期间进行此项配置。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 对每台 Apache Cloudberry Segment 主机执行以下操作：

    1. 确定 PXF 服务器的主机名或 IP 地址。
    3. 登录该 Apache Cloudberry Segment 主机：

        ```shell
        $ ssh gpadmin@<seghost>
        ```
    4. 使用您选择的编辑器打开 `~/.bashrc` 文件。
    5. 设置 `PXF_HOST` 环境变量。例如，要将 PXF 主机设置为 `pxfalthost1`，请在 `.bashrc` 文件中添加以下内容：

        ```shell
        export PXF_HOST=pxfalthost1
        ```
    4. 保存文件并退出编辑器。

1. 执行刚刚更新的 `.bashrc` 文件：

    ```shell
    gpadmin@coordinator$ source ~/.bashrc
    ```

1. 按照[配置监听地址](#configuring-the-listen-address)中的说明，配置 PXF Service 的监听地址。

3. 按照 Apache Cloudberry 文档中[重启 Apache Cloudberry](/cloudberry/database-basic/start-and-stop-cbdb-database/) 的说明重启 Apache Cloudberry。

5. 按照[关于 PXF 服务运行时监控](/cloudberry/pxf/administering/monitor_pxf/#about-pxf-service-runtime-monitoring)中的说明，通过访问 `http://<PXF_HOST>:<PXF_PORT>/actuator/health` 查看 PXF 监控信息，验证 PXF 正运行在重新配置的主机上。
