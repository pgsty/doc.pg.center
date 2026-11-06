---
title: "升级 PXF 软件包"
description: "升级通过 rpm 或 deb 软件包安装的 PXF。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/upgrade_pxf_rpm.md"
---

如果通过 `rpm` 或 `deb` 软件包安装了 PXF，并且已在当前 Apache Cloudberry 安装中配置并正在使用 PXF，则在安装新版本的 PXF 时，必须执行一些升级操作。

PXF 升级过程分为两部分。在安装新版本之前执行一个过程，安装之后再执行另一个过程：

-   [第 1 步：完成 PXF 升级前操作](#step-1-complete-the-pxf-pre-upgrade-actions)
-   安装新版本的 PXF
-   [第 2 步：升级 PXF](#step-2-upgrade-pxf)


## 第 1 步：完成 PXF 升级前操作 {#step-1-complete-the-pxf-pre-upgrade-actions}

升级到新版本的 PXF 之前，请执行此过程：

1. 登录 Apache Cloudberry Coordinator 主机。例如：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 确认并记下 Apache Cloudberry 集群中当前运行的 PXF 版本：

    ```shell
    gpadmin@coordinator$ pxf version
    ```

1. 按照[停止 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#stopping-pxf) 中的说明，在每台主机上停止 PXF。

1. 安装新版本的 PXF，确认并记下新的 PXF 版本号，然后继续执行[第 2 步：升级 PXF](#step-2-upgrade-pxf)。


## 第 2 步：升级 PXF {#step-2-upgrade-pxf}

安装新版本的 PXF 之后，请执行以下过程：

1. 登录 Apache Cloudberry Coordinator 主机。例如：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 向 Apache Cloudberry 注册新版本的 `pxf` 扩展文件（参见 [pxf cluster register](/cloudberry/pxf/ref/pxf-cluster/)）。运行此命令时必须已设置 `$GPHOME`：

    ```shell
    gpadmin@coordinator$ pxf cluster register
    ```

1. 在每个使用 PXF 的 Apache Cloudberry 数据库中更新 `pxf` 扩展。数据库超级用户或数据库所有者必须在 `psql` 子系统或 SQL 脚本中运行以下 SQL 命令：

    ```sql
    ALTER EXTENSION pxf UPDATE;
    ```

1. 将 PXF 配置从 Coordinator 主机同步到 Standby Coordinator 主机和每台 Apache Cloudberry Segment 主机。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 按照[启动 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#starting-pxf) 中的说明，在每台主机上启动 PXF。
