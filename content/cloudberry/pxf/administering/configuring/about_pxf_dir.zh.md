---
title: "安装目录与配置目录"
description: "PXF 安装目录与配置目录的布局。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/about_pxf_dir.md"
---

本文档使用 `<PXF_INSTALL_DIR>` 指代 PXF 安装目录。其取值取决于 PXF 的安装方式：

 - 如果 PXF 作为 Apache Cloudberry 的一部分安装，其值为 `$GPHOME/pxf`。
 - 如果安装的是 PXF 的 `rpm` 或 `deb` 软件包，其值为 `/usr/local/cloudberry-pxf` 或 `/usr/local/cloudberry-pxf-<version>`，或者是您自行选择的目录（仅限 Rocky Linux/RHEL）。

`<PXF_INSTALL_DIR>` 既包含 PXF 可执行文件，也包含 PXF 运行时配置文件和目录。PXF 不需要初始化步骤：`$PXF_BASE` 标识运行时配置目录，默认的 `$PXF_BASE` 即 `<PXF_INSTALL_DIR>`。

如果希望将配置文件和运行时文件存放在其他位置，请参阅[迁移 $PXF_BASE](#relocating-pxf_base)。

> <b>注意：</b>本文档使用 <code>&lt;PXF_INSTALL_DIR></code> 指代 PXF 安装目录，使用 `$PXF_BASE` 环境变量指代 PXF 运行时配置目录。PXF 在内部使用该变量。只有在显式迁移该目录时，才需要在 shell 环境中设置它。

## PXF 安装目录 {#pxf-installation-directories}

安装 Apache Cloudberry 或 PXF 的 `rpm` 或 `deb` 软件包时，以下 PXF 文件和目录会安装到 `<PXF_INSTALL_DIR>`：

| 目录 | 说明                                                                                                   |
|--------------------------------|------------------------------------------------------------------------------------------|
| application/                | PXF Server 应用程序 JAR 文件。   |
| bin/                | PXF 命令行可执行文件目录。   |
| commit.sha          | 此 PXF 发行版的提交标识符。   |
| gpextable/           | PXF 扩展文件。在单个主机上运行 `pxf register` 命令时，或在 Apache Cloudberry Coordinator 主机上运行 `pxf [cluster] register` 命令时（作用于集群中的所有主机），PXF 会将此目录中的 `pxf.control` 文件复制到 Apache Cloudberry 安装目录（`$GPHOME`）。   |
| share/                | 共享 PXF 文件目录，是否需要其中的文件取决于所访问的外部数据存储。`share/` 最初只包含 PXF HBase JAR 文件。 |
| templates/  | PXF 服务器配置文件模板目录。 |
| version              | PXF 版本。             |

安装 Apache Cloudberry 或 PXF 的 `rpm` 或 `deb` 软件包时，以下 PXF 目录会安装到 `$PXF_BASE`：

| 目录 | 说明                                                                                                                                                                                                                                |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| conf/                | 用于 PXF 运行时和日志配置的[用户可自定义 PXF 配置文件](/cloudberry/pxf/administering/configuring/config_files/)所在位置。该目录包含 `pxf-application.properties`、`pxf-env.sh`、`pxf-log4j2.xml` 和 `pxf-profiles.xml` 文件。 |
| keytabs/  | PXF 服务 Kerberos 主体密钥表（keytab）文件的默认位置。`keytabs/` 目录及其中的文件仅 Apache Cloudberry 安装用户（通常为 `gpadmin`）可读。 |
| lib/     | [用户添加的运行时依赖](/cloudberry/pxf/administering/reg_jar_depend/)所在位置。其中的 `native/` 子目录是 PXF 本地库的默认运行时目录。 |
| logs/                | PXF 运行时[日志文件](/cloudberry/pxf/administering/advanced-config/cfg_logging/)目录。`logs/` 目录及日志文件仅 Apache Cloudberry 安装用户（通常为 `gpadmin`）可读。 |
| run/         | PXF 默认运行目录。启动 PXF 后，该目录包含 PXF 进程 ID 文件 `pxf-app.pid`。`run/` 及其中的文件和目录仅 Apache Cloudberry 安装用户（通常为 `gpadmin`）可读。 |
| servers/  | [PXF 服务器](/cloudberry/pxf/administering/configuring/cfg_server/)的配置目录；每个子目录包含一个服务器定义，子目录名称即服务器名称。默认服务器名为 `default`。Apache Cloudberry 管理员可以配置其他服务器。 |

有关 PXF 配置和启动命令及步骤的详细信息，请参阅[配置 PXF](/cloudberry/pxf/administering/configuring/) 和[启动 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#starting-pxf)。

## 迁移 $PXF_BASE {#relocating-pxf_base}

如果需要让 `$PXF_BASE` 位于与 `<PXF_INSTALL_DIR>` 不同的目录，可以在安装 PXF 之后，将其从默认位置更改为您选择的位置。

PXF 提供 [pxf [cluster] prepare](/cloudberry/pxf/ref/pxf-cluster/) 命令来准备新的 `$PXF_BASE` 位置。该命令会将上述运行时目录和配置目录复制到 `PXF_BASE` 环境变量所指定的文件系统位置。

例如，要在所有 Apache Cloudberry 主机上将 `$PXF_BASE` 迁移到 `/path/to/dir` 目录，请按如下方式运行命令：

```shell
gpadmin@coordinator$ PXF_BASE=/path/to/dir pxf cluster prepare
```

当 `$PXF_BASE` 与 `<PXF_INSTALL_DIR>` 不同时，请在运行 `pxf` 命令时设置 `PXF_BASE` 环境变量，以通知 PXF：

```text
gpadmin@coordinator$ PXF_BASE=/path/to/dir pxf cluster start
```

请在 PXF 安装所有者（通常为 `gpadmin` 用户）的 `.bashrc` shell 初始化脚本中按如下方式设置该环境变量：

```text
export PXF_BASE=/path/to/dir
```
