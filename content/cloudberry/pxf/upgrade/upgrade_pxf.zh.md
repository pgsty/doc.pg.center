---
title: "从早期 PXF 版本升级"
description: "在 PXF 各版本之间升级。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/upgrade_pxf.md"
---

如果已安装 PXF 的 `rpm` 或 `deb` 软件包，并且已在当前 Apache Cloudberry 安装中配置并正在使用 PXF，则在安装新版本的 PXF 时，必须执行一些升级操作。

PXF 升级过程分为三步。依次执行一个安装前过程、安装本身，以及一个安装后过程：

-   [第 1 步：执行 PXF 升级前操作](#step-1-perform-the-pxf-pre-upgrade-actions)
-   [第 2 步：安装新版 PXF](#step-2-install-the-new-pxf)
-   [第 3 步：完成 PXF 升级](#step-3-complete-the-pxf-upgrade)


## 第 1 步：执行 PXF 升级前操作 {#step-1-perform-the-pxf-pre-upgrade-actions}

升级到新版本的 PXF 之前，请执行此过程：

1. 登录 Apache Cloudberry Coordinator 主机。例如：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 确认并记下 Apache Cloudberry 集群中当前运行的 PXF 版本：

    ```shell
    gpadmin@coordinator$ pxf version
    ```

1. 按照[停止 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#stopping-pxf) 中的说明，在每台 Apache Cloudberry 主机上停止 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster stop
    ```

1. （可选，建议）备份 `$PXF_BASE` 中的 PXF 用户配置文件。例如，如果 `PXF_BASE=/usr/local/cloudberry-pxf`：

    ```shell
    gpadmin@coordinator$ cp -avi /usr/local/cloudberry-pxf pxf_base.bak
    ```


## 第 2 步：安装新版 PXF {#step-2-install-the-new-pxf}

安装新版本的 PXF，并确认并记下新的 PXF 版本号。


## 第 3 步：完成 PXF 升级 {#step-3-complete-the-pxf-upgrade}

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

1. 查阅所要升级到的版本的 [CHANGELOG](https://cloudberry.apache.org/releases)。如果某个版本引入了新的配置属性或更改了默认行为，请相应更新 `$PXF_BASE` 中受影响的 `pxf-site.xml`、`pxf-application.properties` 或相关文件。

1. 将 PXF 配置从 Coordinator 主机同步到 Standby Coordinator 主机和每台 Apache Cloudberry Segment 主机。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 按照[启动 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#starting-pxf) 中的说明，在每台 Apache Cloudberry 主机上启动 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster start
    ```
