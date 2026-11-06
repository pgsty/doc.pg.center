---
title: "使用 RPM/DEB 软件包安装"
description: "本文介绍如何使用 RPM 或 DEB 软件包，在物理机或虚拟机上手动部署 Apache Cloudberry。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/install_cloudberry.md"
---

阅读本文前，建议先阅读[平台要求](/cloudberry/deployment/platform-requirements/)和[配置系统](/cloudberry/deployment/prepare-to-deploy/)。

必须在 Apache Cloudberry 系统中的每台主机上安装 Apache Cloudberry。

> [!NOTE] 说明
> 从 Apache Cloudberry 2.1 开始，官方提供 RPM 和 DEB 软件包下载。RPM 软件包支持 Rocky Linux 8/9、RHEL 8/9 及兼容发行版。DEB 软件包支持 Ubuntu 22.04。
>
> 下载后，请验证文件的签名和校验和。

## 安装软件包 {#install-the-package}

准备工作完成后，即可安装 Apache Cloudberry。需要从 [Apache Cloudberry 发布页面](https://cloudberry.apache.org/releases)下载相应的软件包，然后使用安装包在每个节点上安装数据库。

1. 下载安装包，并复制到 Coordinator、Standby Coordinator 以及每台 Segment 主机上的 `gpadmin` 主目录。

2. 使用 sudo（或以 `root` 身份），通过系统的包管理器在每台主机上安装 Apache Cloudberry 软件包：

    ```bash    
    # For RPM (Rocky Linux, RHEL, etc.)
    sudo dnf install <RPM package path>
    # Or for older systems: sudo yum install <RPM package path>
    
    # For DEB (Ubuntu)
    sudo apt install --fix-broken <DEB package path>
    # Or alternatively: sudo dpkg -i <DEB package path> && apt-get install -f
    ```

    `yum`、`dnf` 和 `apt` 命令会自动安装软件依赖，将 Apache Cloudberry 软件文件复制到 `/usr/local` 下带有版本号的目录 `/usr/local/cloudberry-db-<version>`，并创建指向安装目录的符号链接 `/usr/local/cloudberry-db`。

3. 授予 `gpadmin` 用户访问 `/usr/local/cloudberry-db/` 目录的权限。

    ```bash
    sudo chown -R gpadmin:gpadmin /usr/local/cloudberry*
    ```

## （可选）安装到非默认目录 {#optional-installing-to-a-non-default-directory}

> [!WARNING] 警告
> Apache Cloudberry 2.1 不支持自定义安装目录。此功能计划在 Apache Cloudberry 2.2 中提供。以下说明仅供今后参考。

### 适用于基于 RPM 的系统（Rocky Linux、RHEL 等） {#for-rpm-based-systems-rocky-linux-rhel-etc}

在基于 RHEL 的系统上，可以使用 `rpm` 命令的 `--prefix` 选项，将 Apache Cloudberry 安装到非默认目录（而不是 `/usr/local` 下）。注意，直接使用 `rpm` 不会自动安装依赖，必须在每台主机上手动安装。

1. 下载 Apache Cloudberry 软件包，并复制到 Coordinator、Standby Coordinator 以及每台 Segment 主机上 `gpadmin` 用户的主目录。

2. 在每台主机系统上手动安装依赖：

    ```bash
    $ sudo dnf install openssh-server openssh-clients sudo shadow-utils \
    bash procps-ng ca-certificates python3 apr bzip2 krb5-libs libevent \
    libicu liburing libuuid libxml2 libyaml libzstd lz4 ncurses openldap \
    openssl pam pcre2 perl protobuf readline zlib libuv iproute \
    net-tools which rsync keyutils libssh libpsl xz
    ```

3. 使用 `rpm` 的 `--prefix` 选项，将 Apache Cloudberry 软件包安装到每台主机上选定的安装目录：

    ```bash
    $ sudo rpm --install ./<RPM package filename> --prefix=<directory>
    ```

    `rpm` 命令会将 Apache Cloudberry 软件文件复制到所选 `<directory>` 下带有版本号的目录中，并创建指向该版本目录的符号链接 `<directory>/cloudberry-db`。

4. 将已安装文件的所有者和所属组更改为 `gpadmin`：

    ```bash
    $ sudo chown -R gpadmin:gpadmin <directory>/cloudberry*
    ```

如果使用 `rpm` 安装到非默认目录，之后进行小版本升级时，仍需使用 `rpm`（而不是 `dnf`）。

## 启用免密 SSH {#enabling-passwordless-ssh}

每台 Cloudberry 主机上的 `gpadmin` 用户都必须能够从集群中的任意主机通过 SSH 连接到其他任意主机，而无需输入密码或密钥口令（称为“免密 SSH”）。如果已启用从 Coordinator 主机到集群中其他所有主机的免密 SSH（“1-*n* 免密 SSH”），可以使用 `gpssh-exkeys` 命令行工具，启用任意主机到其他任意主机的免密 SSH（“*n*-*n* 免密 SSH”）。

1. 以 `gpadmin` 用户身份登录 Coordinator 主机，后续操作也使用 `gpadmin` 用户。
2.  使用 source 加载 Apache Cloudberry 安装目录中的 `path` 文件。

    ```
    $ source /usr/local/cloudberry-db-<version>/cloudberry-env.sh
    ```

    > [!WARNING] 警告
    > 从 Cloudberry 2.1 开始，路径文件名已从 `greenplum_path.sh` 改为 `cloudberry-env.sh`，详情请参阅这篇[博客文章](https://cloudberry.apache.org/blog/from-greenplum-path.sh-to-cloudberry-env.sh/)。

    > [!NOTE] 说明
    > 将上述 `source` 命令添加到 `gpadmin` 用户的 `.bashrc` 或其他 shell 启动文件中，以便每次以 `gpadmin` 身份登录时都设置好 Apache Cloudberry 的路径和环境变量。

3.  使用 `ssh-copy-id` 命令，将 `gpadmin` 用户的公钥添加到集群中其他每台主机的 SSH 文件 `authorized_hosts` 中。

    ```
    $ ssh-copy-id scdw
    $ ssh-copy-id sdw1
    $ ssh-copy-id sdw2
    $ ssh-copy-id sdw3
    . . .
    ```

    这样就启用了 1-*n* 免密 SSH。系统会提示输入每台主机上 `gpadmin` 用户的密码。如果系统上安装了 `sshpass` 命令，可以使用类似以下的命令来避免交互式提示。

    ```
    $ SSHPASS=<password> sshpass -e ssh-copy-id scdw
    ```

4.  在 `gpadmin` 主目录中创建名为 `hostfile_exkeys` 的文件，列出 Cloudberry 系统中每台主机（Coordinator、Standby Coordinator 和 Segment 主机）在机器上配置的主机名及主机地址（接口名）。确保没有空行或多余空格。请检查各系统的 `/etc/hosts` 文件，以确定当前环境应使用的正确主机名。

    例如，假设有一台 Coordinator、一台 Standby Coordinator 和三台 Segment 主机，且每台主机都有两个未绑定的网络接口，文件内容将类似于：

    ```
    cdw
    cdw-1
    cdw-2
    scdw
    scdw-1
    scdw-2
    sdw1
    sdw1-1
    sdw1-2
    sdw2
    sdw2-1
    sdw2-2
    sdw3
    sdw3-1
    sdw3-2
    ```

5.  使用 `hostfile_exkeys` 文件运行 `gpssh-exkeys` 工具，为 `gpadmin` 用户启用 *n*-*n* 免密 SSH。

    ```
    $ gpssh-exkeys -f hostfile_exkeys
    ```

## 确认安装 {#confirm-the-installation}

为确保 Apache Cloudberry 软件已正确安装和配置，请在 Apache Cloudberry 的 Coordinator 主机上执行以下确认步骤。如有问题，请先修正，再继续下一项任务。

1. 以 `gpadmin` 身份登录 Coordinator 主机：

    ```bash
    $ su - gpadmin
    ```

2. 使用 `gpssh` 工具，检查能否在没有密码提示的情况下登录所有主机，并确认所有主机都已安装 Apache Cloudberry 软件。使用前面创建的 `hostfile_exkeys` 文件。例如：

    ```bash
    $ gpssh -f hostfile_exkeys -e 'ls -l /usr/local/cloudberry-db-*'
    ```

    如果安装成功，应能在没有密码提示的情况下登录所有主机。所有主机的安装目录内容应相同，且目录所有者都应为 `gpadmin` 用户。

    如果出现密码提示，请运行以下命令，重新交换 SSH 密钥：

    ```bash
    $ gpssh-exkeys -f hostfile_exkeys
    ```

## Apache Cloudberry 安装内容说明 {#about-your-apache-cloudberry-installation}

-   **`cloudberry-env.sh`** — 此文件包含 Apache Cloudberry 的环境变量。
-   **bin** — 此目录包含 Apache Cloudberry 管理工具，还包含 PostgreSQL 客户端和服务器程序，其中大部分程序也用于 Apache Cloudberry。
-   **docs/cli_help** — 此目录包含 Apache Cloudberry 命令行工具的帮助文件。
-   **docs/cli_help/gpconfigs** — 此目录包含 `gpinitsystem` 配置文件和主机文件的示例，可在安装和初始化 Apache Cloudberry 系统时修改并使用。
-   **ext** — 某些 Apache Cloudberry 工具使用的随附程序（例如 Python）。
-   **include** — Apache Cloudberry 的 C 头文件。
-   **lib** — Apache Cloudberry 和 PostgreSQL 的库文件。
-   **sbin** — 辅助脚本、内部脚本及程序。
-   **share** — Apache Cloudberry 的共享文件。
