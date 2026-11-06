---
title: "配置系统"
description: "介绍如何为安装 Apache Cloudberry 软件准备操作系统环境。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/prepare-to-deploy.md"
---

在物理机或虚拟机上部署 Apache Cloudberry 之前，需要完成一些准备工作。开始部署前，请阅读本文和[平台要求](/cloudberry/deployment/platform-requirements/)。

按顺序执行以下任务：

1. 确保主机系统满足[平台要求](/cloudberry/deployment/platform-requirements/)中描述的要求。
2. [停用或配置 SELinux。](#deactivate-or-configure-selinux)
3. [停用或配置防火墙软件。](#deactivate-or-configure-firewall-software)
4. [设置必需的操作系统参数。](#recommended-os-parameters-settings)
5. [同步系统时钟。](#synchronizing-system-clocks)
6. [创建 gpadmin 账户。](#creating-the-cloudberry-administrative-user)

除非另有说明，这些任务应在 Apache Cloudberry 阵列中的*所有*主机上执行，包括 Coordinator、Standby Coordinator 和 Segment 主机。

Apache Cloudberry 的主机命名约定是：Coordinator 主机使用 `cdw`，Standby Coordinator 主机使用 `scdw`。

Segment 主机的命名约定为 `sdwN`，其中 `sdw` 是前缀，`N` 是整数。例如，Segment 主机名可以是 `sdw1`、`sdw2` 等。对于具有多个接口的主机，建议进行网卡绑定；如果接口未绑定，惯例是在主机名后追加连字符（`-`）和数字。例如，`sdw1-1` 和 `sdw1-2` 是主机 `sdw1` 的两个接口名。

> [!IMPORTANT] 重要
> 如果 Apache Cloudberry 集群不能接受数据丢失，建议为 Coordinator 和 Segment 配置镜像。如果未启用镜像，Apache Cloudberry 只存储一份数据，因此在发生硬件故障时，数据可用性和正确性只能依靠底层存储介质来保障。

## 停用或配置 SELinux {#deactivate-or-configure-selinux}

> [!NOTE] 说明
> 本节仅适用于 RHEL/Oracle/Rocky Linux。Ubuntu 默认不安装 SELinux，而是使用 AppArmor；Apache Cloudberry 不需要对 AppArmor 做任何配置。Ubuntu 用户可以跳过本节。

对于所有运行 RHEL/Oracle/Rocky Linux 的 Apache Cloudberry 主机系统，必须将 SELinux 设为 `Disabled`，或者调整配置，解除对 Apache Cloudberry 进程、目录和 `gpadmin` 用户的访问限制。

如果选择停用 SELinux：

1. 以 root 用户身份检查 SELinux 状态：

    ```bash
    # sestatus

    SELinuxstatus: disabled
    ```

2. 如果 SELinux 尚未停用，编辑 `/etc/selinux/config` 文件将其停用。以 root 身份，将 `config` 文件中的 `SELINUX` 参数值更改为：

    ```bash
    SELINUX=disabled
    ```

3. 如果系统安装了系统安全服务守护进程（SSSD），即使已停用 SELinux，仍可能因 SELinux 导致 SSH 身份验证被拒绝。为避免此问题，请编辑 SSSD 配置文件，将 `selinux_provider` 参数设为 `none`。以 root 身份编辑 `/etc/sssd/sssd.conf`，添加以下参数：

    ```
    selinux_provider=none
    ```

4. 重启系统以应用所做的更改，并验证 SELinux 已停用。

如果选择以 `Enforcing` 模式启用 SELinux，Apache Cloudberry 进程和用户可以在默认的 `Unconfined` 上下文中正常运行。如果需要对 Apache Cloudberry 进程和用户施加更严格的 SELinux 限制，必须测试配置，确保不会影响 Apache Cloudberry 的功能或性能。

## 停用或配置防火墙软件 {#deactivate-or-configure-firewall-software}

还应停用防火墙软件，例如 RHEL 系统上的 `firewalld` 或 Ubuntu 系统上的 `ufw`（默认已停用）。如果不停用防火墙软件，就必须配置软件，允许 Apache Cloudberry 主机之间进行必要的通信。

- 适用于 RHEL/Rocky Linux（firewalld）

    检查 `firewalld` 状态：

    ```bash
    systemctl status firewalld
    ```

    如果 `firewalld` 已停用，命令输出为：

    ```
    * firewalld.service - firewalld - dynamic firewall daemon
    Loaded: loaded (/usr/lib/systemd/system/firewalld.service; disabled; vendor preset: enabled)
    Active: inactive (dead)
    ```

    如有必要，以 root 身份运行以下命令，停用 `firewalld`：

    ```bash
    systemctl stop firewalld.service
    systemctl disable firewalld.service
    ```

- 适用于 Ubuntu（ufw）

    Ubuntu 默认禁用 `ufw`。使用以下命令验证状态：

    ```bash
    ufw status
    ```

    如果输出为 `Status: inactive`，则无需操作。如果处于活动状态，请将其禁用：

    ```bash
    ufw disable
    ```

更多信息请参阅防火墙或操作系统文档。

## 推荐的操作系统参数设置 {#recommended-os-parameters-settings}

Apache Cloudberry 要求在系统的所有主机上设置特定的 Linux 操作系统（OS）参数，包括 Coordinator 和 Segment 主机。

一般来说，需要调整以下几类系统参数：

- **共享内存** — 只有将内核共享内存段的大小设置得当，Apache Cloudberry 实例才能工作。大多数操作系统的默认安装所设置的共享内存值，对 Apache Cloudberry 来说都过低。在 Linux 系统上，还必须停用 OOM（内存不足）终止器。
- **网络** — 在处理大量数据的 Apache Cloudberry 系统上，必须设置特定的网络调优参数，以优化 Cloudberry Interconnect 建立的网络连接。
- **用户限制** — 用户限制控制由用户 shell 启动的进程可用的资源。Apache Cloudberry 要求提高单个进程允许同时打开的文件描述符数量上限。默认设置可能导致部分 Apache Cloudberry 查询耗尽处理查询所需的文件描述符，从而使查询失败。

具体而言，需要编辑以下 Linux 配置：

- [hosts 文件](#the-hosts-file)
- [sysctl.conf 文件](#the-sysctlconf-file)
- [系统资源限制](#system-resources-limits)
- [核心转储](#core-dump)
- [XFS 挂载选项](#xfs-mount-options)
- [磁盘 I/O 设置](#disk-io-settings)
- [网络](#networking)
- [透明大页（THP）](#transparent-huge-pages-thp)
- [IPC 对象移除](#ipc-object-removal)
- [SSH 连接阈值](#ssh-connection-threshold)

### hosts 文件 {#the-hosts-file}

编辑 `/etc/hosts` 文件，确保其中包含参与 Apache Cloudberry 系统的每台机器的主机名及所有接口地址名。

首先，使用 `hostnamectl` 命令设置每台主机的主机名。主机名只能包含字母、数字和连字符（`-`），建议字母全部使用小写。每个主机名必须在所有主机中全局唯一。例如：

```bash
# Run on each host respectively
hostnamectl set-hostname cdw    # on coordinator
hostnamectl set-hostname scdw   # on standby coordinator
hostnamectl set-hostname sdw1   # on segment 1
hostnamectl set-hostname sdw2   # on segment 2
hostnamectl set-hostname sdw3   # on segment 3

# Verify (takes effect immediately)
hostname

# Refresh the shell prompt to show the new hostname
exec bash
```

然后，编辑所有主机上的 `/etc/hosts` 文件，添加所有主机名到其 IP 地址的映射。例如：

```
192.168.1.1  cdw
192.168.1.2  scdw
192.168.1.3  sdw1
192.168.1.4  sdw2
192.168.1.5  sdw3
```

### sysctl.conf 文件 {#the-sysctlconf-file}

本节列出的 `sysctl.conf` 参数，旨在改善多种环境下的性能、优化效果和一致性。请根据具体情况和配置调整这些设置。

在 `/etc/sysctl.conf` 文件中设置参数，然后使用 `sysctl -p` 重新加载：

```conf
# kernel.shmall = _PHYS_PAGES / 2 # See Shared Memory Pages
kernel.shmall = 197951838
# kernel.shmmax = kernel.shmall * PAGE_SIZE
kernel.shmmax = 810810728448
kernel.shmmni = 4096
vm.overcommit_memory = 2 # See Segment Host Memory
vm.overcommit_ratio = 95 # See Segment Host Memory

net.ipv4.ip_local_port_range = 10000 65535 # See Port Settings
kernel.sem = 250 2048000 200 8192
kernel.sysrq = 1
kernel.core_uses_pid = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.msgmni = 2048
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.conf.all.arp_filter = 1
net.ipv4.ipfrag_high_thresh = 41943040
net.ipv4.ipfrag_low_thresh = 31457280
net.ipv4.ipfrag_time = 60
net.core.netdev_max_backlog = 10000
net.core.rmem_max = 2097152
net.core.wmem_max = 2097152
vm.swappiness = 10
vm.zone_reclaim_mode = 0
vm.dirty_expire_centisecs = 500
vm.dirty_writeback_centisecs = 100
vm.dirty_background_ratio = 0 # See System Memory
vm.dirty_ratio = 0
vm.dirty_background_bytes = 1610612736
vm.dirty_bytes = 4294967296
```

#### 共享内存页 {#shared-memory-pages}

Apache Cloudberry 使用共享内存，在属于同一 `postgres` 实例的 `postgres` 进程之间通信。`kernel.shmall` 设置整个系统可使用的共享内存总量，单位为页。`kernel.shmmax` 设置单个共享内存段的大小上限，单位为字节。

根据系统的物理内存和页面大小，设置 `kernel.shmall` 和 `kernel.shmmax` 的值。一般而言，这两个参数表示的容量都应为系统物理内存的一半。

使用操作系统变量 `_PHYS_PAGES` 和 `PAGE_SIZE` 来设置这些参数。

```
kernel.shmall = ( _PHYS_PAGES / 2)
kernel.shmmax = ( _PHYS_PAGES / 2) * PAGE_SIZE
```

要计算 `kernel.shmall` 和 `kernel.shmmax` 的值，请运行以下命令。其中使用的 `getconf` 命令会返回操作系统变量的值。

```bash
$ echo $(expr $(getconf _PHYS_PAGES) / 2)
$ echo $(expr $(getconf _PHYS_PAGES) / 2 \* $(getconf PAGE_SIZE))
```

作为最佳实践，建议将计算所得的值写入 `/etc/sysctl.conf` 文件。例如，某主机系统安装了 1583 GB 内存，返回的值为 `_PHYS_PAGES = 395903676` 和 `PAGE_SIZE = 4096`。对应的 `kernel.shmall` 和 `kernel.shmmax` 值如下：

```
kernel.shmall = 197951838
kernel.shmmax = 810810728448
```

如果 Apache Cloudberry Coordinator 的共享内存配置与 Segment 主机不同，`_PHYS_PAGES` 和 `PAGE_SIZE` 的值可能不同，Coordinator 主机上的 `kernel.shmall` 和 `kernel.shmmax` 值也会与 Segment 主机上的值不同。

#### Segment 主机内存 {#segment-host-memory}

操作系统使用 Linux 内核参数 `vm.overcommit_memory`，确定可以为进程分配多少内存。对于 Apache Cloudberry，此参数应始终设为 2。

`vm.overcommit_ratio` 是用于应用进程的 RAM 百分比，其余部分留给操作系统。在 Red Hat Enterprise Linux 上，默认值为 50。

`vm.overcommit_ratio` 的计算公式如下：

```
vm.overcommit_ratio = (RAM - 0.026 * gp_vmem) / RAM
```

`gp_vmem` 的计算方法如下：

```
# If the system memory is less than 256 GB, use the following formula to calculate:
gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.7

# If the system memory is greater than or equal to 256 GB, use the following formula to calculate:
gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.17

# In the above formulas, SWAP is the swap space on the host, in GB.
# RAM is the size of the memory installed on the host, in GB.
```

#### 端口设置 {#port-settings}

为避免初始化时 Apache Cloudberry 与其他应用程序发生端口冲突，请记下操作系统参数 `net.ipv4.ip_local_port_range` 指定的端口范围。使用 `gpinitsystem` 集群配置文件初始化 Apache Cloudberry 时，不要将 Apache Cloudberry 端口设在该范围内。

例如，如果 `net.ipv4.ip_local_port_range = 10000 65535`，请将 Apache Cloudberry 的基础端口号设为以下值。

```
PORT_BASE = 6000
MIRROR_PORT_BASE = 7000
```

#### IP 分片设置 {#ip-fragmentation-settings}

当 Apache Cloudberry Interconnect 使用 UDP（默认值）时，网卡负责控制 IP 数据包的分片和重组。

如果 UDP 消息大小超过网络的最大传输单元（MTU），IP 层就会对消息进行分片。（有关 Apache Cloudberry MTU 大小的更多信息，请参阅本节后面的[网络](#networking)。）接收方必须先将分片存储在缓冲区中，才能重新整理并组装消息。

以下 `sysctl.conf` 操作系统参数控制重组过程：

| 操作系统参数 | 说明 |
|---|---|
| `net.ipv4.ipfrag_high_thresh` | 为 IP 分片重组分配的内存上限阈值，单位为字节。一旦达到此阈值，后续分片就会被丢弃，直到内存使用量降至下限阈值。增大此值可以让系统处理更多重组请求，避免因内存不足而丢弃分片。默认值为 4194304 字节（4MB）。 |
| `net.ipv4.ipfrag_low_thresh` | 为 IP 分片重组分配的内存下限阈值，单位为字节。增大此值有助于确保即使内存使用量相对较低，也有足够空间接收和重组新的 IP 分片。默认值为 3145728 字节（3MB）。（在内核版本 4.17 之后弃用。） |
| `net.ipv4.ipfrag_time` | IP 分片保留在内存中的最长时间，单位为秒。默认值为 30。 |

Apache Cloudberry 推荐采用以下参数设置：

```conf
net.ipv4.ipfrag_high_thresh = 41943040
net.ipv4.ipfrag_low_thresh = 31457280
net.ipv4.ipfrag_time = 60
```

> [!TIP] 提示
> 如果在 Segment 日志中看到消息 `interconnect may have encountered a network error, please check your network`，或 Segment 因相同错误发生故障，很可能是 IP 分片重组缓冲区相对于当前负载过小。这种情况常见于内存较大、UDP Interconnect 流量较高的主机。
>
> 对于内存超过 16GB 的主机，可以尝试将阈值提高到以下初始值，并使用 `sysctl -p` 重新加载：
>
> ```conf
> net.ipv4.ipfrag_high_thresh = 536870912
> net.ipv4.ipfrag_low_thresh = 429496730
> net.ipv4.ipfrag_time = 60
> ```
>
> 调整这些值时：
>
> - 先将 `net.ipv4.ipfrag_high_thresh = 536870912`（512MB）作为起点。如果 Interconnect 错误仍然存在，请继续增大此值。此参数最高可提高到可用物理内存的 5%。
> - 将 `net.ipv4.ipfrag_low_thresh` 设为 `net.ipv4.ipfrag_high_thresh` 的约 80%。上限阈值为 512MB 时，此值约为 `429496730`。

#### 系统内存 {#system-memory}

对于内存超过 64GB 的主机系统，推荐以下设置：

```conf
vm.dirty_background_ratio = 0
vm.dirty_ratio = 0
vm.dirty_background_bytes = 1610612736 # 1.5GB
vm.dirty_bytes = 4294967296 # 4GB
```

对于内存不超过 64GB 的主机系统，请移除 `vm.dirty_background_bytes` 和 `vm.dirty_bytes`，并将两个 `ratio` 参数设为以下值：

```conf
vm.dirty_background_ratio = 3
vm.dirty_ratio = 10
```

增大 `vm.min_free_kbytes`，以确保能轻松满足网络和存储驱动程序的 `PF_MEMALLOC` 请求。这对系统内存较大的机器尤为重要，因为其默认值往往过低。使用以下 awk 命令，将 `vm.min_free_kbytes` 设为推荐的系统物理内存的 3%：

```bash
awk 'BEGIN {OFMT = "%.0f";} /MemTotal/ {print "vm.min_free_kbytes =", $2 * .03;}' /proc/meminfo >> /etc/sysctl.conf
```

不要将 `vm.min_free_kbytes` 设为超过系统内存的 5%，否则可能导致内存不足。

### 系统资源限制 {#system-resources-limits}

在 `/etc/security/limits.conf` 文件中设置以下参数：

```
* soft nofile 524288
* hard nofile 524288
* soft nproc 131072
* hard nproc 131072
```

对于 Red Hat Enterprise Linux（RHEL）系统，`/etc/security/limits.d/20-nproc.conf` 文件中的参数值会覆盖 `limits.conf` 文件中的值。请确保覆盖文件中的所有参数均设为所需值。Linux 模块 `pam_limits` 先读取 `limits.conf` 文件中的值，再读取覆盖文件中的值，以设置用户限制。有关 PAM 和用户限制的信息，请参阅 PAM 和 `pam_limits` 的文档。

在每台 Segment 主机上运行 `ulimit -u` 命令，显示每个用户可用的最大进程数。验证返回值为 131072。

### 核心转储 {#core-dump}

将以下行添加到 `/etc/sysctl.conf`，启用核心文件生成，并将其保存到已知位置：

```conf
kernel.core_pattern=/var/core/core.%h.%t
```

将以下行添加到 `/etc/security/limits.conf`：

```
* soft core unlimited
```

要将更改应用到当前运行的内核，请运行以下命令：

```bash
# sysctl -p
```

### XFS 挂载选项 {#xfs-mount-options}

在 Linux 平台上，XFS 是 Apache Cloudberry 数据目录的首选数据存储文件系统。使用 `mount` 命令，并指定以下推荐的 XFS 挂载选项：

```
rw,nodev,noatime,inode64
```

> [!NOTE] 说明
> RHEL 8/9 和 Ubuntu 系统不支持 `nobarrier` 选项。只使用 `rw,nodev,noatime,inode64` 这些选项。

> [!TIP] 提示
> 如果使用只有一块系统盘、没有额外数据盘的云虚拟机，可以跳过以下磁盘格式化和挂载步骤，直接在现有文件系统上创建数据目录：
>
> ```bash
> mkdir -p /data
> chown -R gpadmin:gpadmin /data
> ```

如果有专用数据盘，请在 `/etc/fstab` 文件中设置 XFS 文件系统挂载。根据实际情况调整设备路径：

```bash
mkdir -p /data
mkfs.xfs -f /dev/sdb

# Use device name directly
echo "/dev/sdb /data xfs rw,nodev,noatime,inode64 0 0" >> /etc/fstab
# Or use UUID for stable identification across reboots (recommended for cloud/VM environments)
# echo "UUID=$(blkid -s UUID -o value /dev/vdb1) /data xfs rw,nodev,noatime,inode64 0 0" >> /etc/fstab

mount /data
chown -R gpadmin:gpadmin /data
```

运行以下命令，检查挂载是否成功：

```bash
df -h
```

### 磁盘 I/O 设置 {#disk-io-settings}

#### 预读值 {#read-ahead-value}

每个磁盘设备文件的预读（`blockdev`）值都应为 16384。要验证磁盘设备的预读值，请运行：

```bash
# sudo /sbin/blockdev --getra <devname>
```

例如：

```bash
# sudo /sbin/blockdev --getra /dev/sdb
```

要设置设备的 blockdev（预读）值，请运行：

```bash
# sudo /sbin/blockdev --setra <bytes> <devname>
```

例如：

```bash
# sudo /sbin/blockdev --setra 16384 /dev/sdb
```

> [!NOTE] 说明
> `blockdev --setra` 命令的设置不会持久保存。必须确保每次系统重启时都设置预读值。具体设置方法因系统而异。

在系统启动时设置 `blockdev` 值的一种方法，是在 `rc.local` 文件中添加 `/sbin/blockdev --setra` 命令。例如，将以下行添加到 `rc.local` 文件中，设置磁盘 `sdb` 的预读值。

```
/sbin/blockdev --setra 16384 /dev/sdb
```

在使用 systemd 的系统上，还必须为 `rc.local` 文件设置执行权限，使其能在启动时运行。例如，在 RHEL 系统上，以下命令为该文件设置执行权限。

```bash
# chmod +x /etc/rc.d/rc.local
```

重启系统，使设置生效。

#### 磁盘 I/O 调度器 {#disk-io-scheduler}

Linux 磁盘调度器对提交给存储设备的 I/O 请求进行排序，控制内核向磁盘提交读写操作的方式。

典型的 Linux 磁盘 I/O 调度器支持多种访问策略。最佳策略取决于底层存储基础设施。针对不同操作系统和存储设备类型，Apache Cloudberry 系统推荐采用以下调度器策略设置：

| 存储设备类型 | 操作系统 | 推荐的调度器策略 |
|---|---|---|
| 非易失性存储器高速接口（NVMe） | RHEL 8/9、Ubuntu | `none` |
| 固态硬盘（SSD） | RHEL 8/9、Ubuntu | `none` |
| 其他 | RHEL 8/9、Ubuntu | `mq-deadline` |

要指定调度器并使其持续生效到下次系统重启，请运行：

```bash
# echo schedulername > /sys/block/<devname>/queue/scheduler
```

例如：

```bash
# echo mq-deadline > /sys/block/sdb/queue/scheduler
```

> [!NOTE] 说明
> 使用 `echo` 命令设置磁盘 I/O 调度器策略不会持久保存；必须确保每次系统重启时都运行该命令。具体运行方式因系统而异。

在使用 `grub2` 的系统上，要在启动时指定 I/O 调度器，可以在 RHEL 上使用系统工具 `grubby`，或在 Ubuntu 上直接编辑 Grub 配置文件。

要永久设置启动时使用的 I/O 调度器：

- 对于 RHEL/Rocky Linux，使用 `grubby`。以 `root` 身份运行以下命令来添加参数：

    ```bash
    # grubby --update-kernel=ALL --args="elevator=mq-deadline"
    ```

    以下 `grubby` 命令用于显示内核参数设置：

    ```bash
    # grubby --info=ALL
    ```

- 对于 Ubuntu，编辑 `/etc/default/grub` 并运行 `update-grub`：

    ```bash
    # sed -i 's/GRUB_CMDLINE_LINUX="\(.*\)"/GRUB_CMDLINE_LINUX="\1 elevator=mq-deadline"/' /etc/default/grub

    # update-grub
    ```

添加参数后，重启系统。

### 网络 {#networking}

网络的最大传输单元（MTU）指定联网设备能够接受的最大数据包或帧的大小，单位为字节。巨型帧是指超过标准 MTU 1500 字节的帧。

Apache Cloudberry 使用三项不同的 MTU 设置：

- Apache Cloudberry 服务器配置参数 `gp_max_packet_size`。默认最大数据包大小为 8192，此默认值假定使用巨型帧 MTU。
- 操作系统的 MTU 设置。
- 机架交换机的 MTU 设置。

这些设置相互关联：其值应始终相同或接近；否则，MTU 大小应满足 Apache Cloudberry < 操作系统 < 交换机的顺序。

9000 是交换机常见的受支持设置，也是推荐用于 Apache Cloudberry 主机操作系统和机架交换机的 MTU 值。

### 透明大页（THP） {#transparent-huge-pages-thp}

应停用透明大页（THP），因为它会降低 Apache Cloudberry 的性能。

首先，检查当前 THP 状态：

```bash
cat /sys/kernel/mm/*transparent_hugepage/enabled
```

如果输出显示 `[never]`，说明 THP 已禁用。否则，请将其永久禁用：

- 对于 RHEL/Rocky Linux，使用 `grubby`。以 root 身份运行以下命令来添加参数：

    ```bash
    # grubby --update-kernel=ALL --args="transparent_hugepage=never"
    ```

- 对于 Ubuntu，编辑 `/etc/default/grub` 并运行 `update-grub`：

    ```bash
    # sed -i 's/GRUB_CMDLINE_LINUX="\(.*\)"/GRUB_CMDLINE_LINUX="\1 transparent_hugepage=never"/' /etc/default/grub

    # update-grub
    ```

添加参数后，重启系统。

以下 cat 命令用于检查 THP 状态。输出表示 THP 已停用：

```bash
cat /sys/kernel/mm/*transparent_hugepage/enabled
# Expected output: always madvise [never]
```

### IPC 对象移除 {#ipc-object-removal}

停用 IPC 对象移除功能。默认的 `systemd` 设置 `RemoveIPC=yes` 会在非系统用户账户退出登录时移除 IPC 连接。这会导致 Apache Cloudberry 工具 `gpinitsystem` 因信号量错误而失败。执行以下任一操作，可以避免此问题。

- 按照[创建 Cloudberry 管理用户](#creating-the-cloudberry-administrative-user)一节在 Coordinator 节点上添加 `gpadmin` 操作系统用户账户时，将其创建为系统账户。
- 停用 `RemoveIPC`。在 Apache Cloudberry 主机系统上的 `/etc/systemd/logind.conf` 中设置以下参数。

    ```
    RemoveIPC=no
    ```

    重启 `systemd-login` 服务或重启系统后，设置即会生效。要重启服务，请以 root 用户身份运行以下命令。

    ```bash
    service systemd-logind restart
    ```

### SSH 连接阈值 {#ssh-connection-threshold}

某些 Apache Cloudberry 管理工具，包括 `gpexpand`、`gpinitsystem` 和 `gpaddmirrors`，使用系统之间的安全 shell（SSH）连接来执行任务。在大型 Apache Cloudberry 部署、云部署或每台主机具有大量 Segment 的部署中，这些工具可能超过主机对未完成身份验证连接数的最大阈值。此时，会收到类似以下的错误：`ssh_exchange_identification: Connection closed by remote host`。

要提高 Apache Cloudberry 系统的连接阈值，请更新 SSH 守护进程配置文件 `/etc/ssh/sshd_config` 中的 SSH 配置参数 `MaxStartups` 和 `MaxSessions`。

> [!NOTE] 说明
> 必须具有 root 权限才能编辑这两个文件。

如果为 `MaxStartups` 和 `MaxSessions` 指定单个整数值，则分别表示最大并发未完成身份验证连接数（`MaxStartups`），以及每个网络连接允许打开的 shell、登录或子系统会话的最大数量（`MaxSessions`）。例如：

```
MaxStartups 200
MaxSessions 200
```

如果使用“start:rate:full”语法指定 `MaxStartups`，就会启用 SSH 守护进程的随机早期连接丢弃机制。`start` 表示允许的未完成身份验证 SSH 连接尝试数上限。当未完成身份验证的连接尝试数达到 `start` 时，SSH 守护进程会按 `rate` 指定的百分比拒绝后续连接尝试。`full` 表示未完成身份验证连接尝试数的上限，达到该值后会拒绝所有连接尝试。例如：

```
MaxStartups 10:30:200
MaxSessions 200
```

更新 `MaxStartups` 和 `MaxSessions` 后，重启 SSH 守护进程：

```bash
# service sshd restart
```

## 同步系统时钟 {#synchronizing-system-clocks}

必须使用 NTP（网络时间协议），同步组成 Apache Cloudberry 系统的所有主机的系统时钟。准确计时对于确保数据库运行可靠和数据完整性至关重要。

实现 NTP 有多种架构可选。建议采用以下一种：

- 将 Coordinator 配置为 NTP 主时间源，集群中的其他主机连接到它。
- 配置外部 NTP 主时间源，集群中的所有主机连接到它。

根据操作系统版本，NTP 协议可能由 `ntpd` 守护进程、`chronyd` 守护进程或其他程序实现。更多信息请参阅所选 NTP 实现的文档。

### 方案 1：以 Coordinator 为主时间源配置系统时钟 {#option-1-configure-system-clocks-with-the-coordinator-as-the-primary-source}

1. 在 Coordinator 主机上，以 root 身份登录并编辑 NTP 守护进程配置文件。将 `server` 参数指向数据中心的 NTP 时间服务器。例如，假设 `10.6.220.20` 是数据中心 NTP 服务器的 IP 地址：

    ```
    server 10.6.220.20
    ```

2. 在每台 Segment 主机上，以 root 身份登录并编辑 NTP 守护进程配置文件。将第一个 `server` 参数指向 Coordinator 主机，第二个 server 参数指向 Standby Coordinator 主机。例如：

    ```
    server cdw prefer
    server scdw
    ```

3. 在 Standby Coordinator 主机上，以 root 身份登录并编辑 NTP 守护进程配置文件。将第一个 `server` 参数指向主 Coordinator 主机，第二个 server 参数指向数据中心的 NTP 时间服务器。例如：

    ```
    server cdw prefer
    server 10.6.220.20
    ```

4. 以 root 身份同步所有 Apache Cloudberry 主机上的系统时钟。

    如果使用 `ntpd` 守护进程：

    ```bash
    systemctl restart ntpd
    ```

    如果使用 `chronyd` 守护进程：

    ```bash
    # For RHEL/Rocky Linux
    systemctl restart chronyd

    # For Ubuntu (restart works with either name, but enable requires 'chrony')
    systemctl restart chronyd
    ```

### 方案 2：以外部主时间源配置系统时钟 {#option-2-configure-system-clocks-with-an-external-primary-source}

1. 在所有主机上，包括 Coordinator、Standby Coordinator 和 Segment，以 root 身份登录并编辑 NTP 守护进程配置文件。将第一个 `server` 参数指向数据中心的 NTP 时间服务器。例如，假设 `10.6.220.20` 是数据中心 NTP 服务器的 IP 地址：

    ```
    server 10.6.220.20
    ```

2. 在 Coordinator 主机上，使用 NTP 守护进程同步所有 Apache Cloudberry 主机上的系统时钟。例如，使用 `gpssh`：

    如果使用 `ntpd` 守护进程：

    ```bash
    gpssh -f hostfile_gpssh_allhosts -v -e 'systemctl restart ntpd'
    ```

    如果使用 `chronyd` 守护进程：

    ```bash
    gpssh -f hostfile_gpssh_allhosts -v -e 'systemctl restart chronyd'
    ```

## 创建 Cloudberry 管理用户 {#creating-the-cloudberry-administrative-user}

在每个节点上创建专用的操作系统用户账户，用于运行和管理 Apache Cloudberry。按惯例，此用户账户名为 `gpadmin`。

> [!IMPORTANT] 重要
> 不能以 `root` 身份运行 Apache Cloudberry 服务器。

`gpadmin` 用户必须具有访问安装和运行 Apache Cloudberry 所需服务及目录的权限。

每台 Apache Cloudberry 主机上的 `gpadmin` 用户都必须安装 SSH 密钥对，并能够从集群中的任意主机通过 SSH 连接到其他任意主机，而无需输入密码或密钥口令（称为“免密 SSH”）。如果已启用从 Coordinator 主机到集群中其他所有主机的免密 SSH（“1-*n* 免密 SSH”），之后可以使用 Apache Cloudberry 的 `gpssh-exkeys` 命令行工具，启用任意主机到其他任意主机的免密 SSH（“*n*-*n* 免密 SSH”）。

也可以授予 `gpadmin` 用户 sudo 权限，以便以 `gpadmin` 身份，使用 `sudo`、`ssh/rsync` 和 `gpssh/gpsync` 命令轻松管理 Apache Cloudberry 集群中的所有主机。

以下步骤说明如何在主机上设置 `gpadmin` 用户、设置密码、创建 SSH 密钥对，以及可选地启用 sudo 功能。必须在每台 Apache Cloudberry 集群主机上以 root 身份执行这些步骤。（对于大型 Apache Cloudberry 集群，应使用系统部署工具自动执行这些步骤。）

1. 创建 `gpadmin` 用户组和用户。

    > [!NOTE] 说明
    > 确保 `gpadmin` 用户在每台主机上的用户 ID（uid）和组 ID（gid）数值相同，避免依赖这些值判断身份或权限的脚本或服务出现问题。例如，如果 `gpadmin` 用户在不同 Segment 主机上的 uid 或 gid 不同，将 Apache Cloudberry 数据库备份到某些网络文件系统或存储设备时可能失败。创建 `gpadmin` 用户组和用户时，可以使用 `groupadd -g` 选项指定 gid，使用 `useradd -u` 选项指定 uid。使用 `id gpadmin` 命令，可以查看当前主机上 `gpadmin` 用户的 uid 和 gid。

    本例创建 `gpadmin` 用户组，将 `gpadmin` 用户创建为具有主目录的系统账户并加入 `gpadmin` 组，然后为该用户设置密码。

    ```bash
    # groupadd gpadmin
    # useradd gpadmin -r -m -g gpadmin
    # passwd gpadmin
    New password: <changeme>
    Retype new password: <changeme>
    ```

2. 切换到 `gpadmin` 用户，并为 `gpadmin` 用户生成 SSH 密钥对。

    ```bash
    $ su - gpadmin
    $ ssh-keygen -t rsa -b 4096
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/gpadmin/.ssh/id_rsa):
    Created directory '/home/gpadmin/.ssh'.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    ```

    出现密钥口令提示时，按 Enter，这样 SSH 连接就无需输入密钥口令。

3. 授予 `gpadmin` 用户 sudo 访问权限。

    **对于 RHEL/Rocky Linux** — 运行 `visudo`，取消 `%wheel` 组条目的注释：

    ```
    %wheel        ALL=(ALL)       NOPASSWD: ALL
    ```

    确保取消的是包含 `NOPASSWD` 关键字那一行的注释。然后将 `gpadmin` 加入 `wheel` 组：

    ```bash
    # usermod -aG wheel gpadmin
    ```

    **对于 Ubuntu** — 将 `gpadmin` 加入 `sudo` 组，并创建 sudoers 配置片段文件，启用免密 sudo：

    ```bash
    usermod -aG sudo gpadmin
    echo "gpadmin ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/gpadmin
    chmod 440 /etc/sudoers.d/gpadmin
    ```
