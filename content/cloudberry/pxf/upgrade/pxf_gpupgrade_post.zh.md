---
title: "PXF 升级后操作（cbupgrade）"
description: "Apache Cloudberry 原地大版本升级之后需要为 PXF 执行的任务。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/pxf_gpupgrade_post.md"
---

> [!WARNING] 前瞻性参考
> `cbupgrade` 是 Apache Cloudberry 的原地大版本升级工具
> （例如，从 Apache Cloudberry 2.x 升级到 3.x）。它**仍在积极开发中，
> 目前尚不受支持**。本页仅作为前瞻性参考，说明 PXF 预计将如何参与
> `cbupgrade` 工作流；在 `cbupgrade` 发布之前，具体命令和软件包布局
> 可能会发生变化。
> 请勿在生产集群上使用此过程。

如果正在运行 PXF，并计划使用 `cbupgrade` 将 Apache Cloudberry 原地升级到
新的大版本，则需要在运行 `cbupgrade` 之后执行以下步骤。

在下面的步骤中，`<old-version>` 指面向原 Apache Cloudberry 大版本的
PXF 安装，`<new-version>` 指面向新大版本的 PXF 安装。


## 升级后操作 {#post-upgrade-actions}

运行 `cbupgrade` 之后，请执行以下步骤：

1. 确定 `cbupgrade` 过程成功还是失败。

1. **如果 `cbupgrade` 过程失败**：

    1. 运行以下命令，将 PXF 安装回滚到之前的状态（即运行升级前脚本之前的状态）：

        ```shell
        gpadmin@coordinator$ export GPHOME=<old-cloudberry-install-dir>
        gpadmin@coordinator$ /usr/local/cloudberry-pxf-<old-version>/bin/pxf-post-gpupgrade
        ```

        **注意：** 升级后脚本必须连接到正在运行的 Apache Cloudberry 集群。默认情况下，它会尝试以 `gpadmin` 用户（无密码）连接到 `localhost` 上端口 `5432` 的 `gpadmin` 数据库。如果需要自定义这些设置，请参阅[自定义 Apache Cloudberry 连接参数](#customizing-the-apache-cloudberry-connection-parameters)，了解如何为此设置环境变量。

    1. 重启原 Apache Cloudberry 安装中运行的 PXF。

        ```shell
        gpadmin@coordinator$ /usr/local/cloudberry-pxf-<old-version>/bin/pxf cluster start
        ```

    1. 可以选择卸载面向新 Apache Cloudberry 大版本的 PXF 软件包。

    1. **退出此过程。**

1. **如果 `cbupgrade` 过程成功，请执行此过程中的其余步骤。**

1. 将 PXF 配置为新 Apache Cloudberry 大版本中的全新安装：

    ```shell
    gpadmin@coordinator$ export GPHOME=<new-cloudberry-install-dir>
    gpadmin@coordinator$ /usr/local/cloudberry-pxf-<new-version>/bin/pxf-post-gpupgrade
    ```

    **注意：** 升级后脚本必须连接到正在运行的 Apache Cloudberry 集群。默认情况下，它会尝试以 `gpadmin` 用户（无密码）连接到 `localhost` 上端口 `5432` 的 `gpadmin` 数据库。如果需要自定义这些设置，请参阅[自定义 Apache Cloudberry 连接参数](#customizing-the-apache-cloudberry-connection-parameters)，了解如何为此设置环境变量。

1. 如果没有重新定位 `$PXF_BASE`，则必须将 PXF 配置从原 PXF 安装位置复制到新的 PXF 安装位置。例如：

    ```bash
    gpadmin@coordinator$ for dir in conf lib servers keytabs; do
        cp -aiv /usr/local/cloudberry-pxf-<old-version>/$dir/. /usr/local/cloudberry-pxf-<new-version>/$dir/
    done
    ```

1. 将 PXF 配置从 Apache Cloudberry Coordinator 主机同步到 Standby Coordinator 和 Segment 主机：

    ```shell
    gpadmin@coordinator$ /usr/local/cloudberry-pxf-<new-version>/bin/pxf cluster sync
    ```

1. 启动为新 Apache Cloudberry 大版本安装的 PXF。

    ```shell
    gpadmin@coordinator$ /usr/local/cloudberry-pxf-<new-version>/bin/pxf cluster start
    ```

1. 更新 `.bashrc` 或 `.bash_profile` shell 初始化脚本中的 `$PATH`，将所有出现的 `/usr/local/cloudberry-pxf-<old-version>` 替换为 `/usr/local/cloudberry-pxf-<new-version>`。

1. 通过查询指定了各个 PXF 服务器配置的外部表，验证 PXF 能够访问每个外部数据源。

1. （_可选_）在集群中的每台 Segment 主机上卸载原 PXF 软件包；此操作需要 `sudo` 权限。例如：

    ```shell
    $ yum remove cloudberry-pxf-<old-version>
    ```

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
