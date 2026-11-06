---
title: "PXF 操作系统升级注意事项"
description: "升级 PXF 主机上的操作系统。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/upgrade_os.md"
---

如果计划升级 Apache Cloudberry 集群主机上的操作系统，并且 Apache Cloudberry 安装中正在运行 PXF，则必须在升级操作系统之前和之后执行一些 PXF 特定的操作。

有关 Apache Cloudberry 版本所支持的操作系统版本，请参阅[支持的平台](/cloudberry/pxf/intro/#supported-platforms)。

以下过程假设在与当前运行的 Apache Cloudberry 集群不同的另一组主机上升级操作系统。

## 操作系统升级前操作 {#pre-os-upgrade-actions}

升级操作系统之前，请执行以下步骤：

1. 在开始操作系统升级**之前**，将当前集群中的 PXF 升级到最新版本，并验证 PXF 运行正常。

1. 保留以下 PXF 用户配置目录，它们通常位于 `/usr/local/cloudberry-pxf`：`conf/`、`keytabs/`、`lib/` 和 `servers/`。如果重新定位了 `$PXF_BASE`，请保留该目录中的配置。


## 操作系统升级后操作 {#post-os-upgrade-actions}

在新的一组主机上升级操作系统，并安装、配置和验证 Apache Cloudberry 之后，请执行以下过程：

1. 从 [Apache Cloudberry PXF 发布页](https://github.com/apache/cloudberry-pxf/releases) 下载适用于升级后操作系统的 PXF 软件包。*必须下载与原 Apache Cloudberry 集群上运行的 PXF 相同的版本。*

1. 在所有 Apache Cloudberry 主机上安装适用于升级后操作系统的 PXF。

1. 将原集群中的 PXF 配置文件复制到升级后操作系统的 Apache Cloudberry Coordinator 主机上的 `/usr/local/cloudberry-pxf`。如果选择[重新定位 $PXF_BASE](/cloudberry/pxf/administering/configuring/about_pxf_dir/#relocating-pxf_base)，则改为将配置复制到该目录。

1. 将 PXF 配置同步到 Apache Cloudberry 集群中的所有主机：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 在每台 Apache Cloudberry 主机上启动 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster start
    ```

1. 通过查询指定了各个 PXF 服务器配置的外部表，验证 PXF 能够访问每个外部数据源。
