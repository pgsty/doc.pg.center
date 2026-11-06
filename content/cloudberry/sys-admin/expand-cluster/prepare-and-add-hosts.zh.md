---
title: "准备并添加主机"
description: "验证新主机系统已准备好集成到现有 Cloudberry 系统中。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/prepare-and-add-hosts.md"
---

准备新主机系统以进行扩容时，需要安装 Apache Cloudberry 软件二进制文件、交换所需的 SSH 密钥并运行性能测试。

先在新主机上运行性能测试，再在所有主机上运行测试。在系统离线时对所有主机运行测试，避免用户活动影响结果。

通常，在管理员修改主机网络或系统中的其他特殊条件时，应运行性能测试。例如，如果扩容后的系统将运行在两个网络集群上，则应在每个集群上运行测试。

> [!NOTE]
> 准备用于 Apache Cloudberry 系统的主机，前提是新主机的操作系统已正确配置为与现有主机匹配，具体说明见[配置系统](/cloudberry/deployment/platform-requirements/#supported-os)。

## 将新主机添加到受信任主机环境 {#add-new-hosts-to-the-trusted-host-environment}

新主机必须与现有主机交换 SSH 密钥，使 Cloudberry 管理工具能够连接到所有 Segment，而无需输入密码。使用 [gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/) 工具执行两次密钥交换过程。

首先以 `root` 身份执行，便于管理；然后以 `gpadmin` 用户身份执行，供管理工具使用。按以下顺序执行任务：

1. [以 root 身份交换 SSH 密钥](#to-exchange-ssh-keys-as-root)
2. [创建 gpadmin 用户](#to-create-the-gpadmin-user)
3. [以 gpadmin 用户身份交换 SSH 密钥](#to-exchange-ssh-keys-as-the-gpadmin-user)

> [!NOTE]
> Apache Cloudberry Segment 主机的命名约定是 `sdwN`，其中 `sdw` 是前缀，`N` 是整数（`sdw1`、`sdw2` 等）。对于具有多个接口的主机，约定是在主机名后追加短横线（`-`）和编号。例如，`sdw1-1` 和 `sdw1-2` 是主机 `sdw1` 的两个接口名称。

### 以 root 身份交换 SSH 密钥 {#to-exchange-ssh-keys-as-root}

1. 创建一个包含现有阵列主机名的主机文件，再创建一个包含新增扩容主机名的独立主机文件。对于现有主机，可以使用为系统设置 SSH 密钥时使用的同一个主机文件。文件中列出所有主机（Coordinator、备用 Coordinator 和 Segment 主机），每行一个主机名，不能有多余行或空格。如果使用多网卡配置，请使用某台主机对应的已配置主机名来交换 SSH 密钥。本例中，`cdw` 配置了一个 NIC，`sdw1`、`sdw2` 和 `sdw3` 各配置了 4 个 NIC：

    ```
    cdw
    sdw1-1
    sdw1-2
    sdw1-3
    sdw1-4
    sdw2-1
    sdw2-2
    sdw2-3
    sdw2-4
    sdw3-1
    sdw3-2
    sdw3-3
    sdw3-4
    ```

2. 以 `root` 身份登录 Coordinator 主机，并从 Cloudberry 安装中加载 `cloudberry-env.sh` 文件。

    ```shell
    $ su - 
    # source /usr/local/cloudberry-db/cloudberry-env.sh
    ```

3. 通过主机列表文件运行 `gpssh-exkeys` 工具。例如：

    ```shell
    # gpssh-exkeys -e /home/gpadmin/<existing_hosts_file> -x 
    /home/gpadmin/<new_hosts_file>
    ```

4. `gpssh-exkeys` 会检查远程主机，并在所有主机之间执行密钥交换。出现提示时，输入 `root` 用户密码。例如：

    ```shell
    Enter password for root@<hostname>: <root_password>
    ```

### 创建 gpadmin 用户 {#to-create-the-gpadmin-user}

1. 使用 [gpssh](/cloudberry/reference/sys-utilities/gpssh/) 在所有新增 Segment 主机上创建 `gpadmin` 用户（如果该用户尚不存在）。使用为密钥交换创建的新主机列表。例如：

    ```shell
    # gpssh -f <new_hosts_file> '/usr/sbin/useradd gpadmin -d 
    /home/gpadmin -s /bin/bash'
    ```

2. 为新建的 `gpadmin` 用户设置密码。在 Linux 上，可以使用 `gpssh` 同时在所有 Segment 主机上执行此操作。例如：

    ```shell
    # gpssh -f <new_hosts_file> 'echo <gpadmin_password> | passwd 
    gpadmin --stdin'
    ```

3. 通过查找其主目录，验证已创建 `gpadmin` 用户：

    ```shell
    # gpssh -f <new_hosts_file> ls -l /home
    ```

### 以 gpadmin 用户身份交换 SSH 密钥 {#to-exchange-ssh-keys-as-the-gpadmin-user}

1. 以 `gpadmin` 身份登录，并通过主机列表文件运行 `gpssh-exkeys` 工具。例如：

    ```shell
    # gpssh-exkeys -e /home/gpadmin/<existing_hosts_file> -x 
    /home/gpadmin/<new_hosts_file>
    ```

2. `gpssh-exkeys` 会检查远程主机，并在所有主机之间执行密钥交换。出现提示时，输入 `gpadmin` 用户密码。例如：

    ```shell
    Enter password for gpadmin@<hostname>: <gpadmin_password>
    ```

## 验证磁盘 I/O 和内存带宽 {#validate-disk-io-and-memory-bandwidth}

使用 [gpcheckperf](/cloudberry/reference/sys-utilities/gpcheckperf/) 工具测试磁盘 I/O 和内存带宽。

### 运行 gpcheckperf {#to-run-gpcheckperf}

1. 使用新增主机的主机文件运行 `gpcheckperf` 工具。使用 `-d` 选项指定要在每台主机上测试的文件系统。必须对这些目录具有写入权限。例如：

    ```shell
    $ gpcheckperf -f <new_hosts_file> -d /data1 -d /data2 -v 
    ```

2. 由于工具会在主机之间复制超大文件，测试可能需要很长时间。完成后，会看到 Disk Write、Disk Read 和 Stream 测试的汇总结果。

对于划分为多个子网的网络，请为每个子网使用单独的主机文件重复此过程。

## 将新硬件集成到系统 {#integrate-new-hardware-into-the-system}

在使用新 Segment 初始化系统之前，使用 `gpstop` 关闭系统，防止用户活动导致性能测试结果出现偏差。然后，使用包含所有主机（现有主机和新增主机）的主机文件重新运行性能测试。
