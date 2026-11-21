---
title: "从早期 PXF 版本升级"
description: "在 PXF 各版本之间升级。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/docs/upgrade/upgrade_pxf.md"
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

PXF 要求 **Java 17 或 21**。安装新版本 PXF 前，请在每台 Apache Cloudberry 主机上安装这两个 Java 版本之一，并将 `$PXF_BASE/conf/pxf-env.sh` 中的 `JAVA_HOME` 设为其安装目录。使用 `"$JAVA_HOME/bin/java" -version` 验证所配置的可执行文件。参见[为 PXF 安装 Java](/cloudberry/pxf/administering/configuring/install_java/)。

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

1. 如果从使用 Hadoop 2 的 PXF 版本升级，请检查每份复制的 `hdfs-site.xml` 中的 `dfs.datanode.socket.write.timeout`。在 Hadoop 3.3.6 中，值为 `0` 可能导致 HDFS 写入在等待 DataNode 确认时失败。请设置正的超时值，例如 `60000` 毫秒。

1. 将 PXF 配置从 Coordinator 主机同步到 Standby Coordinator 主机和每台 Apache Cloudberry Segment 主机。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 按照[启动 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#starting-pxf) 中的说明，在每台 Apache Cloudberry 主机上启动 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster start
    ```

## 不向后兼容的变更 {#backward-incompatible-changes}

### 迁移此前从本地路径读取的 Avro 模式 {#migrating-avro-schemas-previously-read-from-local-paths}

早期 PXF 版本先搜索 PXF 主机的本地文件系统，再搜索类路径和配置的文件系统。依赖此行为的表必须更新。例如，即使 PXF 主机上存在该文件，`SCHEMA=/opt/pxf/schemas/example.avsc` 也不再直接打开它。

请选择以下迁移方式之一：

- 将模式文件放入 `SERVER` 配置的文件系统，并将 `SCHEMA` 更新为相对于 `pxf.fs.basePath`（或文件系统根目录）的路径。例如，设置 `pxf.fs.basePath=/data` 时，将模式文件放在 `/data/schemas/example.avsc`，并使用 `SCHEMA=/schemas/example.avsc`。
- 将模式文件放入每台 PXF 主机的 `$PXF_BASE/conf`，并使用相对类路径名称。例如，将文件放在 `$PXF_BASE/conf/schemas/example.avsc`，并使用 `SCHEMA=schemas/example.avsc`。使用 `pxf cluster sync` 同步配置。

这些变更同时适用于 `.avsc` 和 `.avro` 模式文件的读写操作。使用 `file:avro` profile 时，模式路径与数据路径一样，相对于文件服务器必须设置的 `pxf.fs.basePath` 解析。
