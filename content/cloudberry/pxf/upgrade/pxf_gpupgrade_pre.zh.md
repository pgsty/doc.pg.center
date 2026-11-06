---
title: "PXF 升级前操作（cbupgrade）"
description: "在 Apache Cloudberry 原地大版本升级之前准备 PXF。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/pxf_gpupgrade_pre.md"
---

> [!WARNING] 前瞻性参考
> `cbupgrade` 是 Apache Cloudberry 的原地大版本升级工具
> （例如，从 Apache Cloudberry 2.x 升级到 3.x）。它**仍在积极开发中，
> 目前尚不受支持**。本页仅作为前瞻性参考，说明 PXF 预计将如何参与
> `cbupgrade` 工作流；在 `cbupgrade` 发布之前，具体命令和软件包布局
> 可能会发生变化。
> 请勿在生产集群上使用此过程。

如果正在运行 PXF，并计划使用 `cbupgrade` 将 Apache Cloudberry 原地升级到
新的大版本，则需要在运行 `cbupgrade` 之前执行以下步骤。


## 升级前操作 {#pre-upgrade-actions}

运行 `cbupgrade` 之前，请执行以下步骤：

1. 将当前集群中的 PXF 升级到最新版本；有关说明，请参阅[升级 PXF](/cloudberry/pxf/upgrade/) 文档。

1. 记下 PXF 版本。

1. 在集群中的每台 Segment 主机上安装面向新 Apache Cloudberry 大版本的 PXF 软件包。只需安装 PXF 软件包；无需运行 `pxf cluster prepare` 或 `pxf cluster register` 命令。

1. 登录当前 Apache Cloudberry 集群的 Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    gpadmin@coordinator$ 
    ```

1. 针对当前安装运行 PXF 升级前脚本；请替换为当前 Apache Cloudberry 安装目录的文件系统路径：

    ```shell
    gpadmin@coordinator$ export GPHOME=<current-cloudberry-install-dir>
    gpadmin@coordinator$ /usr/local/cloudberry-pxf-<current-version>/bin/pxf-pre-cbupgrade
    ```

    **注意：** 升级前脚本必须连接到正在运行的 Apache Cloudberry 集群。默认情况下，它会尝试以 `gpadmin` 用户（无密码）连接到 `localhost` 上端口 `5432` 的 `gpadmin` 数据库。如果需要自定义这些设置，请参阅[自定义 Apache Cloudberry 连接参数](#customizing-the-apache-cloudberry-connection-parameters)，了解如何为此设置环境变量。

1. 停止 PXF；请注意，在 Apache Cloudberry 升级过程中，PXF 外部表将无法访问。

    ```shell
    gpadmin@coordinator$ /usr/local/cloudberry-pxf-<current-version>/bin/pxf cluster stop
    ```

1. PXF 已准备就绪，可由 `cbupgrade` 升级；请返回 `cbupgrade` 文档，完成大版本升级。


## 自定义 Apache Cloudberry 连接参数 {#customizing-the-apache-cloudberry-connection-parameters}

在 `cbupgrade` 之前和之后运行的 PXF 脚本必须连接到正在运行的 Apache Cloudberry 集群。默认情况下，这些脚本会尝试以 `gpadmin` 用户（无密码）连接到 `localhost` 上端口 `5432` 的 `gpadmin` 数据库。如果需要自定义这些设置，可以通过指定以下环境变量来实现：

| 环境变量 | 默认值 | 说明 |
|----------------------|---------------|-------------------------------------------------------|
| `$PGHOST`            | localhost     | Apache Cloudberry Coordinator 主机的主机名或 IP 地址。 |
| `$PGPORT`            | 5432          | 连接 Coordinator 主机所用的端口号。     |
| `$PGDATABASE`        | gpadmin       | 数据库名称。 |
| `$PGUSER`            | gpadmin       | Apache Cloudberry 用户名。     |
| `$PGPASSWORD`        | _无_        | 该用户的密码。 |

更多详细信息，请参阅 PostgreSQL 文档中的[环境变量](https://www.postgresql.org/docs/9.4/libpq-envars.html)主题。
