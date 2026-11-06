---
title: "平台要求"
description: "本节介绍将 Apache Cloudberry 部署到本地硬件，或 AWS、GCP、Azure 等公有云服务时的平台及操作系统软件要求。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/platform-requirements.md"
---

## 硬件要求 {#hardware-requirements}

### 支持的部署环境 {#supported-deployment-environments}

Apache Cloudberry 支持部署在物理机和虚拟机上。以下是各类环境的推荐配置。

#### 开发或测试环境 {#for-development-or-test-environments}

| 组件    | CPU  | 内存 | 磁盘类型 | 网络                 | 实例数量 |
| ------- | ---- | ---- | -------- | -------------------- | -------- |
| Coordinator  | 4 核 | 8 GB | SSD      | 10 Gbps 网卡（优先使用 2 块） | 1+       |
| Segment | 4 核 | 8 GB | SSD      | 10 Gbps 网卡（优先使用 2 块） | 1+       |

#### 生产环境 {#for-production-environments}

| 组件    | CPU    | 内存   | 磁盘类型 | 网络                 | 实例数量 |
| ------- | ------ | ------ | -------- | -------------------- | -------- |
| Coordinator  | 16 核及以上 | 32 GB 及以上 | SSD      | 10 Gbps 网卡（优先使用 2 块） | 2+       |
| Segment | 8 核及以上  | 32 GB 及以上 | SSD      | 10 Gbps 网卡（优先使用 2 块） | 2+       |

Apache Cloudberry 也可以部署在 AWS、Azure、GCP 等公有云平台上。云部署的硬件要求可能因所选实例类型而异。请参阅相应云提供商的文档，选择达到或超过推荐硬件规格的实例配置。

#### 最低硬件要求 {#minimum-hardware-requirements}

以下列出了在生产环境中使用 Linux 系统运行 Apache Cloudberry 的硬件服务器最低推荐规格。Apache Cloudberry 系统中的所有主机服务器必须具有相同的硬件和软件配置。Apache Cloudberry 还为其认证硬件平台提供硬件搭建指南。请与 Cloudberry 系统工程师一起评审计划采用的环境，确保硬件配置适合 Apache Cloudberry。

- 最低 CPU 要求：任何兼容 x86_64/AARCH64 的 CPU
- 最低内存要求：每台服务器 16 GB RAM
- 磁盘空间要求：
  - 每台主机安装 Cloudberry 需要 150MB
  - 每个 Segment 实例大约需要 300MB 来存放元数据
  - 将磁盘使用率限制在 70% 以内，为临时文件留出空间，并避免性能下降
- 网络要求：阵列内部使用万兆以太网；存在多个接口时，建议进行网卡绑定。Apache Cloudberry 可以使用 IPV4 或 IPV6 协议。

**超线程**

资源组是 Apache Cloudberry 的关键功能之一，可以控制事务并发度、CPU 和内存资源、负载隔离以及动态突发资源使用。

在基于 Intel 的系统上使用资源组控制资源分配时，可以考虑在服务器 BIOS 中关闭超线程（HT）（Intel 核心默认开启此功能）。关闭 HT 可能会导致吞吐量小幅下降（低于 15%），但可以增强资源组之间的隔离，并在低并发负载下提高查询性能。

### CPU 架构支持 {#cpu-architecture-support}

Apache Cloudberry 支持在 **x86_64** 和 **ARM（AARCH64）** CPU 架构上运行，适用于广泛的硬件平台，包括云实例和基于 ARM 的服务器。

| 架构 | 从源码构建 | 预编译二进制包 |
|---|---|---|
| x86_64 | 支持 | 已提供（2.1+） |
| ARM（AARCH64） | 支持 | 计划在 2.2 中提供 |

对于当前版本的 ARM 部署，可以[从源码构建 Apache Cloudberry](/cloudberry/build/source/)。

### 存储 {#storage}

- 为防止数据盘高负载影响操作系统正常的 I/O 响应，应将操作系统和数据分别放在不同的磁盘上。
- 如果主机配置允许，建议使用 2 块独立的 SAS 磁盘组成系统盘（RAID1），另外使用 10 块 SAS 磁盘组成数据盘（RAID5）。
- 建议使用 LVM 逻辑卷管理磁盘，以便更灵活地配置磁盘。

**系统盘**：系统盘应使用独立磁盘，避免数据盘高负载影响操作系统。建议将系统盘配置为双盘 RAID 1，并采用 XFS 文件系统。

**数据盘**：建议使用 LVM 管理数据盘。根据测试统计，为每个物理卷创建独立的逻辑卷可以获得最佳磁盘性能。例如：

```bash
pvcreate /dev/vdb
pvcreate /dev/vdc
pvcreate /dev/vdd
vgcreate data /dev/vdb /dev/vdc /dev/vdd
lvcreate --extents 100%pvs -n data0 data /dev/vdb
lvcreate --extents 100%pvs -n data1 data /dev/vdc
lvcreate --extents 100%pvs -n data2 data /dev/vdd 
```

挂载点名称必须连续，数据盘的挂载点应为 `/data0`、`/data1`、……、`/dataN`。数据盘应使用 XFS 文件系统。例如：

```bash
mkdir -p /data0 /data1 /data2
mkfs.xfs /dev/data/data0
mkfs.xfs /dev/data/data1
mkfs.xfs /dev/data/data2
mount /dev/data/data0 /data0/
mount /dev/data/data1 /data1/
mount /dev/data/data2 /data2/ 
```

## 数据交换网络 {#data-exchange-network}

- **网卡配置**

    数据交换网络用于传输业务数据，对网络性能和吞吐量要求较高。在生产环境中，通常需要两块 10 Gbps 网卡，绑定后使用。推荐的 bond 4 参数如下：

    ```bash
    BONDING_OPTS='mode=4 miimon=100 xmit_hash_policy=layer3+4'
    ```

- **连通性要求**

    - 在数据交换网络中连通管理控制台与数据库主机。如果管理控制台与数据库主机之间有防火墙设备，应确保 TCP 空闲连接能保持超过 12 小时。
    - 在数据交换网络中连通数据库主机与管理控制台主机，且不限制 TCP 空闲连接时间。
    - 在数据交换网络中，将数据库客户端和访问数据库的应用程序与数据库 Coordinator 节点连通。
    - 确保 TCP 空闲连接能保持超过 12 小时。

- **默认网关**

    如果主机配置了管理网络，应将数据交换网络的网卡（bond0）用作默认网关设备，否则可能导致主机网络流量监控异常、部署失败和性能问题。以下是查看默认网关的示例。

    ```bash
    netstat -rn | grep ^0.0.0.0
    ```

- **交换机**

    - 确保数据网络交换机从第一级到第二级的出口带宽，不低于单个机柜的最大磁盘 I/O 吞吐能力（按单块 RAID 卡 500 MBps 计算）。
    - 建议交换机收敛比为 4:1。收敛比达到 6:1 时，大多数链路会饱和。收敛比达到 8:1 时，会出现严重丢包。

## 软件要求 {#software-requirements}

### 支持的操作系统 {#supported-os}

Apache Cloudberry 支持以下操作系统：

- Rocky Linux 8/9/10（**从 Cloudberry 2.2 开始支持 Rocky Linux 10**）
- Ubuntu 22.04/24.04（**从 Cloudberry 2.2 开始支持 Ubuntu 24.04**）
- RHEL 8/9/10 及兼容发行版（Oracle Linux、AlmaLinux 等）

### 软件依赖 {#software-dependencies}

所有 Apache Cloudberry 主机都需要以下运行时软件包。通过 `dnf`（RPM）或 `apt`（DEB）安装时，会自动解析并安装这些依赖；此处列出供参考。

#### 通用依赖（所有平台） {#common-dependencies-all-platforms}

```
bash, openssh, rsync, perl, python3, less, hostname, iproute / iproute2, iputils / iputils-ping, which / debianutils
```

#### 适用于 Rocky Linux / RHEL 8 {#for-rocky-linux--rhel-8}

```
apr, audit, bash, bzip2, hostname, iproute, iputils, keyutils,
less, libcurl, libevent, libidn2, libselinux, libstdc++, libuuid,
libuv, libxml2, libyaml, libzstd, lz4, openldap, openssh,
openssh-clients, openssh-server, openssl, pam, perl, python3,
readline, rsync, which
```

#### 适用于 Rocky Linux / RHEL 9 {#for-rocky-linux--rhel-9}

```
apr, bash, bzip2, glibc, hostname, iproute, iputils, keyutils,
less, libcap, libcurl, libidn2, libpsl, libssh, libstdc++,
libxml2, libyaml, libzstd, lz4, openldap, openssh,
openssh-clients, openssh-server, openssl, pam, pcre2, perl,
python3, readline, rsync, which, xz
```

#### 适用于 Ubuntu 22.04 {#for-ubuntu-2204}

```
curl, cgroup-tools, debianutils, hostname, iputils-ping, iproute2,
keyutils, krb5-multidev, less, libapr1, libbz2-1.0, libcurl4,
libcurl3-gnutls, libevent-2.1-7, libreadline8, libxml2, libyaml-0-2,
libldap-2.5-0, libzstd1, libcgroup1, libssl3, libpam0g, libprotobuf23,
libpsl5, libuv1, liburing2, libxerces-c3.2, locales, lsof, lz4,
net-tools, openssh-client, openssh-server, openssl, python3, rsync,
wget, xz-utils, zlib1g
```

### Java {#java}

Apache Cloudberry 的 PL/Java 和 PXF 支持以下 Java 版本：

-   Open JDK 8 或 Open JDK 11、17，可从 [AdoptOpenJDK](https://adoptopenjdk.net) 获取
-   Oracle JDK 8 或 Oracle JDK 11、17

### 文件系统 {#file-system}

Apache Cloudberry 主机必须使用 XFS 文件系统存储数据。

如果共享存储以块设备形式提供给运行 Apache Cloudberry 的服务器，并在块设备上挂载 XFS 文件系统，Apache Cloudberry 就支持使用这种网络存储或共享存储。不支持网络文件系统。使用网络存储或共享存储时，必须与使用本地存储时一样启用 Apache Cloudberry 镜像，且不得修改 Segment 的镜像方案或恢复方案。

只有当存储以块设备形式提供，并挂载 XFS 文件系统来存放 Segment 目录时，才能在虚拟化系统上部署 Apache Cloudberry。

Apache Cloudberry 支持在 Amazon Web Services（AWS）服务器上使用 Amazon 实例存储（Amazon 使用的卷名为 ephemeral[0-23]）或 Amazon Elastic Block Store（Amazon EBS）存储。如果使用 Amazon EBS 存储，必须将 Amazon EBS 卷组成 RAID，并挂载 XFS 文件系统，才属于受支持的配置。

### SSH 配置 {#ssh-configuration}

SSH 服务端（`/etc/ssh/sshd_config`）的推荐配置如下。配置完成后，运行 `systemctl restart sshd.service` 使其生效。

| 参数                   | 值   | 说明             |
| ---------------------- | ---- | ---------------- |
| Port                   | 22   | 监听端口。         |
| PasswordAuthentication | yes  | 允许密码登录，集群初始化后可以更改。   |
| PermitEmptyPasswords   | no   | 不允许使用空密码登录。 |
| UseDNS                 | no   | 不使用 DNS。     |
