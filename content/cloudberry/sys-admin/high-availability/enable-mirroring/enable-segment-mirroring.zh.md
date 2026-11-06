---
title: "启用 Segment 镜像"
description: "主 Segment 不可用时，镜像 Segment 允许数据库查询通过故障切换转到备用 Segment。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/enable-segment-mirroring.md"
---

默认情况下，镜像与主 Segment 配置在同一组主机上。也可以选择一组完全不同的主机部署镜像 Segment，使其不与任何主 Segment 共用机器。

> [!NOTE]
> 在线数据复制期间，Apache Cloudberry 应处于静止状态，不应运行工作负载或其他查询。

## 为现有系统添加 Segment 镜像（与主 Segment 使用相同主机） {#to-add-segment-mirrors-to-an-existing-system-same-hosts-as-primaries}

1. 在所有 Segment 主机上为镜像数据分配存储区域。该区域必须与主 Segment 在文件系统中的位置不同。
2. 使用 [`gpssh-exkeys`](/cloudberry/reference/sys-utilities/gpssh-exkeys/)，确保各 Segment 主机之间可以进行 SSH 连接和远程同步，且无需输入密码。
3. 运行 [`gpaddmirrors`](/cloudberry/reference/sys-utilities/gpaddmirrors/) 工具，为 Apache Cloudberry 系统启用镜像。例如，将主 Segment 端口号加 10000，得到镜像 Segment 的端口号：

    ```shell
    $ gpaddmirrors -p 10000
    ```

    其中，`-p` 指定在主 Segment 端口号上增加的数值。添加镜像时使用默认的组镜像配置。

## 为现有系统添加 Segment 镜像（与主 Segment 使用不同主机） {#to-add-segment-mirrors-to-an-existing-system-different-hosts-from-primaries}

1. 确保所有主机上都已安装 Apache Cloudberry 软件。详细安装说明见 [Apache Cloudberry 安装指南](/cloudberry/deployment/)。
2. 在所有 Segment 主机上为镜像数据分配存储区域，并按需分配表空间。
3. 使用 `gpssh-exkeys`，确保各 Segment 主机之间可以进行 SSH 连接和远程同步，且无需输入密码。
4. 创建配置文件，列出创建镜像所用的主机名、端口和数据目录。要生成一份可作为起点的示例配置文件，运行：

    ```shell
    $ gpaddmirrors -o <filename>          
    ```

    镜像配置文件的格式如下：

    ```
    <row_id>=<contentID>|<address>|<port>|<data_dir>
    ```

    其中，`row_id` 是文件中的行号，contentID 是 Segment 实例的内容 ID，address 是 Segment 主机的主机名或 IP 地址，port 是通信端口，`data_dir` 是 Segment 实例的数据目录。

    例如，以下镜像配置文件包含两台 Segment 主机，每台主机上有两个 Segment 实例：

    ```
    0=2|sdw1-1|41000|/data/mirror1/gp2
    1=3|sdw1-2|41001|/data/mirror2/gp3
    2=0|sdw2-1|41000|/data/mirror1/gp0
    3=1|sdw2-2|41001|/data/mirror2/gp1
    ```

5. 运行 `gpaddmirrors` 工具，为 Apache Cloudberry 系统启用镜像：

    ```shell
    $ gpaddmirrors -i <mirror_config_file>
    ```

    `-i` 选项指定刚创建的镜像配置文件。
