---
title: "创建数据存储区域"
description: "为 Coordinator、Standby Coordinator、主 Segment 和镜像 Segment 创建数据存储目录。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/create_data_dirs.md"
---

## 在 Coordinator 和 Standby Coordinator 主机上创建数据存储区域 {#creating-data-storage-areas-on-the-coordinator-and-standby-coordinator-hosts}

Apache Cloudberry 的 Coordinator 和 Standby Coordinator 主机都需要数据存储区域，用于存放系统目录数据及其他系统元数据等 Apache Cloudberry 系统数据。

### 在 Coordinator 上创建数据目录 {#to-create-the-data-directory-location-on-the-coordinator}

Coordinator 上的数据目录位置与 Segment 上的不同。Coordinator 不存储任何用户数据，其实例上只存储系统目录表和系统元数据，因此无需为其分配与 Segment 同样多的存储空间。

1.  创建或选择一个目录，作为 Coordinator 的数据存储区域。该目录应有足够的磁盘空间来存放数据，且所有者和所属组都应为 `gpadmin`。例如，以 `root` 身份运行以下命令：

    ```
    # mkdir -p /data/coordinator
    ```

2.  将该目录的所有者更改为 `gpadmin` 用户。例如：

    ```
    # chown gpadmin:gpadmin /data/coordinator
    ```

3.  使用 [gpssh](/cloudberry/reference/sys-utilities/gpssh/)，在 Standby Coordinator 上也创建 Coordinator 数据目录。例如：

    ```
    # source /usr/local/cloudberry-db/cloudberry-env.sh 
    # gpssh -h scdw -e 'sudo mkdir -p /data/coordinator'
    # gpssh -h scdw -e 'sudo chown gpadmin:gpadmin /data/coordinator'
    ```

## 在 Segment 主机上创建数据存储区域 {#creating-data-storage-areas-on-segment-hosts}

Apache Cloudberry 的 Segment 主机上需要为主 Segment 创建数据存储区域。镜像 Segment 需要独立的存储区域。

### 在所有 Segment 主机上创建数据目录 {#to-create-the-data-directory-locations-on-all-segment-hosts}

1.  在 Coordinator 主机上，以 `root` 身份登录：

    ```
    # su
    ```

2.  创建名为 `hostfile_gpssh_segonly` 的文件。对于每台 Segment 主机，该文件中只应包含一个在该机器上配置的主机名。例如，有三台 Segment 主机时：

    ```
    sdw1
    sdw2
    sdw3
    ```

3.  使用 [gpssh](/cloudberry/reference/sys-utilities/gpssh/) 和刚创建的 `hostfile_gpssh_segonly` 文件，一次性在所有 Segment 主机上创建主实例和镜像实例的数据目录。例如：

    ```
    # source /usr/local/cloudberry-db/cloudberry-env.sh 
    # gpssh -f hostfile_gpssh_segonly -e 'sudo mkdir -p /data/primary'
    # gpssh -f hostfile_gpssh_segonly -e 'sudo mkdir -p /data/mirror'
    # gpssh -f hostfile_gpssh_segonly -e 'sudo chown -R gpadmin /data/*'
    ```
