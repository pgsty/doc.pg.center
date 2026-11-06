---
title: "以单计算节点部署 Apache Cloudberry"
linkTitle: "（可选）以单计算节点部署"
description: "Apache Cloudberry 并不完全兼容 PostgreSQL，部分功能和语法为 Apache Cloudberry 专有。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/single-node.md"
---

如果业务已经依赖 Apache Cloudberry，并希望在单个节点上使用其专有语法和功能，以避免与 PostgreSQL 的兼容性问题，可以考虑部署不包含 Segment 的 Apache Cloudberry。

Apache Cloudberry 提供单计算节点部署模式。此模式在 gp_role 为 `utility` 时运行，仅包含一个 Coordinator（QD）节点和一个 Standby Coordinator 节点，不包含 Segment 节点，也不进行数据分布。可以直接连接 Coordinator 并运行查询，就像连接普通的多节点集群一样。注意，由于不存在数据分布，部分 SQL 语句在此模式下不生效，另有部分 SQL 语句不受支持。详情请参阅[使用行为变化](#user-behavior-changes)。

## 部署方法 {#how-to-deploy}

### 步骤 1：部署准备 {#step-1-prepare-to-deploy}

以 root 用户身份登录每台主机，按以下各节的顺序修改每个节点服务器的设置。

#### 添加 `gpadmin` 管理用户 {#add-gpadmin-admin-user}

按照以下示例创建名为 `gpadmin` 的用户组和用户，将组 ID 和用户 ID 都设为 `520`。创建并指定 `gpadmin` 的主目录为 `/home/gpadmin`。

```bash
groupadd -g 520 gpadmin  # Adds user group gpadmin.
useradd -g 520 -u 520 -m -d /home/gpadmin/ -s /bin/bash gpadmin  # Adds username gpadmin and creates the home directory of gpadmin.
passwd gpadmin  # Sets a password for gpadmin; after executing, follow the prompts to input the password.
```

#### 禁用 SELinux 和防火墙软件 {#disable-selinux-and-firewall-software}

运行 `systemctl status firewalld` 查看防火墙状态。如果防火墙已开启，需要将 `/etc/selinux/config` 文件中的 `SELINUX` 参数设为 `disabled`，将其关闭。

```bash
SELINUX=disabled
```

也可以使用以下命令禁用防火墙：

```bash
systemctl stop firewalld.service
systemctl disable firewalld.service
```

#### 设置系统参数 {#set-system-parameters}

在 `/etc/sysctl.conf` 配置文件中添加相关系统参数，并运行 `sysctl -p` 命令使配置生效。

设置配置参数时，可以参考以下示例，并根据实际需求调整。下文介绍了其中部分参数的详细说明和推荐设置。

```bash
kernel.shmall = _PHYS_PAGES / 2
kernel.shmall = 197951838
kernel.shmmax = kernel.shmall * PAGE_SIZE
kernel.shmmax = 810810728448
kernel.shmmni = 4096
vm.overcommit_memory = 2
vm.overcommit_ratio = 95
net.ipv4.ip_local_port_range = 10000 65535
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
vm.dirty_background_ratio = 0
vm.dirty_ratio = 0
vm.dirty_background_bytes = 1610612736
vm.dirty_bytes = 4294967296
```

##### 共享内存设置 {#shared-memory-settings}

在 `/etc/sysctl.conf` 配置文件中，`kernel.shmall` 表示可用共享内存总量，单位为页。`kernel.shmmax` 表示单个共享内存段的大小上限，单位为字节。

可以使用操作系统的 `_PHYS_PAGES` 和 `PAGE_SIZE` 参数定义这两个值：

```
kernel.shmall = ( _PHYS_PAGES / 2)
kernel.shmmax = ( _PHYS_PAGES / 2) * PAGE_SIZE
```

要获取这两个操作系统参数的值，可以使用 `getconf`，例如：

```bash
$echo $(expr $(getconf _PHYS_PAGES)/2) 
$echo $(expr $(getconf _PHYS_PAGES)/2 \*$(getconf PAGE_SIZE))
```

- `vm.overcommit_memory` 表示内存过量分配的处理模式。可选值包括：

    - `0`：启发式处理过量分配
    - `1`：始终允许过量分配
    - `2`：不允许过量分配

    将此参数值设为 `2`，以拒绝过量分配。

- `vm.overcommit_ratio` 是一个内核参数，表示应用进程占用的 RAM 百分比。在 CentOS 上，默认值为 `50`。`vm.overcommit_ratio` 的计算公式如下：

    ```
    vm.overcommit_ratio = (RAM - 0.026 * gp_vmem) / RAM
    ```

- `gp_vmem` 的计算方法如下：

    ```
    # If the system memory is less than 256 GB, use the following formula to calculate:
    gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.7

    # If the system memory is greater than or equal to 256 GB, use the following formula to calculate:
    gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.17

    # In the above formulas, SWAP is the swap space on the host, in GB.
    # RAM is the size of the memory installed on the host, in GB.
    ```

##### IP 分片设置 {#ip-segmentation-settings}

Apache Cloudberry 使用 UDP 协议进行内部连接时，网卡控制 IP 数据包的分片和重组。如果 UDP 消息大小超过网络最大传输单元（MTU），IP 层就会对消息进行分片。

- `net.ipv4.ipfrag_high_thresh`：当 IP 分片的总大小超过此阈值时，内核会尝试重组 IP 分片。如果分片总大小超过此阈值，但未能在指定时间内收齐所有分片，内核就不会重组分片。此阈值通常用于控制是否重组较大的分片。默认值为 `4194304` 字节（4 MB）。
- `net.ipv4.ipfrag_low_thresh`：当 IP 分片的总大小低于此阈值时，内核会尽可能等待更多分片到达，以便完成更大的重组。此阈值用于尽量减少未完成的重组操作，并提高系统性能。默认值为 `3145728` 字节（3 MB）。
- `net.ipv4.ipfrag_time` 是控制 IP 分片重组超时的内核参数。默认值为 `30`。

建议将上述参数设为以下值：

```
net.ipv4.ipfrag_high_thresh = 41943040
net.ipv4.ipfrag_low_thresh = 31457280
net.ipv4.ipfrag_time = 60
```

##### 系统内存 {#system-memory}

- 如果服务器内存超过 64 GB，建议在 `/etc/sysctl.conf ` 配置文件中设置以下参数：

    ```
    vm.dirty_background_ratio = 0
    vm.dirty_ratio = 0
    vm.dirty_background_bytes = 1610612736 # 1.5GB
    vm.dirty_bytes = 4294967296 # 4GB
    ```

- 如果服务器内存少于 64 GB，无需设置 `vm.dirty_background_bytes ` 或 `vm.dirty_bytes`。建议在 `/etc/sysctl.conf ` 配置文件中设置以下参数：

    ```
    vm.dirty_background_ratio = 3 
    vm.dirty_ratio = 10
    ```

- 为应对系统内存紧张时的紧急情况，建议在 `/etc/sysctl.conf` 配置文件中添加 `vm.min_free_kbytes` 参数，控制系统预留的可用内存量。建议使用以下命令，将 `vm.min_free_kbytes` 设为系统物理内存的 3%：

    ```bash
    awk 'BEGIN {OFMT = "%.0f";} /MemTotal/ {print "vm.min_free_kbytes =", $2 * .03;}' /proc/meminfo  /etc/sysctl.conf
    ```

- 不建议将 `vm.min_free_kbytes` 设为超过系统物理内存的 5%。

##### 资源限制 {#resource-limit}

编辑 `/etc/security/limits.conf` 文件，添加以下内容，以限制硬件和软件资源的用量。

```
*soft nofile 524288
*hard nofile 524288
*soft nproc 131072
*hard nproc 131072
```

##### 核心转储 {#core-dump}

1. 将以下参数添加到 `/etc/sysctl.conf` 配置文件：

    ```
    kernel.core_pattern=/var/core/core.%h.%t
    ```

2. 运行以下命令使配置生效：

    ```bash
    sysctl -p
    ```

3. 将以下参数添加到 `/etc/security/limits.conf`：

    ```
    * soft core unlimited
    ```

##### 设置 XFS 文件系统挂载选项 {#set-mount-options-for-the-xfs-file-system}

XFS 是 Apache Cloudberry 数据目录使用的文件系统。XFS 支持以下挂载选项：

```
rw,nodev,noatime,inode64
```

可以在 `/etc/fstab` 文件中设置 XFS 文件系统挂载。请参考以下命令，并根据实际情况选择文件路径：

```bash
mkdir -p /data0/
mkfs.xfs -f /dev/vdc
echo "/dev/vdc /data0 xfs rw,nodev,noatime,inode64 0 0"  /etc/fstab
mount /data0
chown -R gpadmin:gpadmin /data0/
```

> [!NOTE] 说明
> RHEL 8/9 和 Ubuntu 系统不支持 `nobarrier` 选项。只使用 `rw,nodev,noatime,inode64` 这些选项。

运行以下命令，检查挂载是否成功：

```bash
df -h
```

##### blockdev 值 {#blockdev-value}

每个磁盘文件的 blockdev 值都应为 `16384`。要验证磁盘设备的 blockdev 值，请使用以下命令：

```bash
sudo/sbin/blockdev --getra<devname>
```

例如，要验证示例服务器磁盘的 blockdev 值：

```bash
sudo/sbin/blockdev --getra /dev/vdc
```

要修改设备文件的 blockdev 值，请使用以下命令：

```bash
sudo/sbin/blockdev --setra<bytes> <devname>
```

例如，要修改示例服务器硬盘设备文件的 blockdev 值：

```bash
sudo/sbin/blockdev --setra16384/dev/vdc
```

##### 磁盘 I/O 调度策略设置 {#io-scheduling-policy-settings-for-disks}

Apache Cloudberry 对应的磁盘类型、操作系统和调度策略如下：

<table>
<thead>
  <tr>
    <th>存储设备类型</th>
    <th>操作系统</th>
    <th>推荐的调度策略</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">NVMe</td>
  </tr>
  <tr>
    <td>RHEL 8</td>
    <td>none</td>
  </tr>
  <tr>
    <td>Ubuntu</td>
    <td>none</td>
  </tr>
  <tr>
    <td rowspan="3">SSD</td>
  </tr>
  <tr>
    <td>RHEL 8</td>
    <td>none</td>
  </tr>
  <tr>
    <td>Ubuntu</td>
    <td>none</td>
  </tr>
  <tr>
    <td rowspan="3">其他</td>
  </tr>
  <tr>
    <td>RHEL 8</td>
    <td>mq-deadline</td>
  </tr>
  <tr>
    <td>Ubuntu</td>
    <td>mq-deadline</td>
  </tr>
</tbody>
</table>

可参考以下命令修改调度策略。注意，此命令只进行临时修改，服务器重启后即失效。

```bash
echo schedulername>/sys/block/<devname>/queue/scheduler
```

例如，临时修改示例服务器的磁盘 I/O 调度策略：

```bash
echo deadline>/sys/block/vdc/queue/scheduler
```

要永久修改调度策略，请使用系统工具 `grubby`。使用 `grubby` 后，重启服务器即可使修改生效。示例命令如下：

```bash
grubby --update-kernel=ALL --args="elevator=deadline"
```

要查看内核参数设置，请使用以下命令：

```bash
grubby --info=ALL
```

##### 禁用透明大页（THP） {#disable-transparent-huge-pages-thp}

需要禁用透明大页（THP），因为它会降低数据库性能。命令如下：

```bash
grubby --update-kernel=ALL --args="transparent_hugepage=never"
```

检查 THP 状态：

```bash
cat /sys/kernel/mm/*transparent_hugepage/enabled
```

##### 禁用 IPC 对象移除 {#disable-ipc-object-deletion}

将 `RemoveIPC` 的值设为 `no`，以禁用 IPC 对象移除。可以在 Apache Cloudberry 的 `/etc/systemd/logind.conf` 文件中设置此参数。

```
RemoveIPC=no
```

禁用后，运行以下命令重启服务器，使禁用设置生效：

```bash
service systemd-logind restart
```

##### SSH 连接阈值 {#ssh-connection-threshold}

要设置 SSH 连接阈值，需要修改 `/etc/ssh/sshd_config` 配置文件中的 `MaxStartups` 和 `MaxSessions` 参数。以下两种写法均可。

```
MaxStartups 200
MaxSessions 200
```

```
MaxStartups 10:30:200
MaxSessions 200
```

运行以下命令重启服务器，使设置生效：

```bash
service sshd restart
```

##### 时钟同步 {#clock-synchronization}

Apache Cloudberry 要求为所有主机配置时钟同步，并且时钟同步服务应随主机启动。可以选择以下一种同步方法：

- 以 Coordinator 节点的时间为时间源，其他主机与 Coordinator 节点主机的时钟同步。
- 使用外部时钟源同步时钟。

本文示例使用外部时钟源同步，即将以下配置添加到 `/etc/chrony.conf` 配置文件中：

```
# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
server 0.centos.pool.ntp.org iburst
```

设置后，可以运行以下命令检查时钟同步状态：

```bash
systemctl status chronyd
```

### 步骤 2：安装 Apache Cloudberry {#step-2-install-apache-cloudberry}

> [!NOTE] 说明
> 从 Apache Cloudberry 2.1 开始，官方提供 RPM 和 DEB 软件包。RPM 软件包支持 Rocky Linux 8/9、RHEL 8/9 及兼容发行版。DEB 软件包支持 Ubuntu 22.04。

1. 将软件包下载到 `gpadmin` 的主目录。

2. 在 `/home/gpadmin` 目录中安装软件包。

    以 `root` 用户身份运行以下命令，并将 `<package path>` 替换为实际的软件包路径。安装期间会自动创建 `/usr/local/cloudberry-db/` 目录。

    ```bash
    cd /home/gpadmin
    
   # For RPM (Rocky Linux, RHEL, etc.)
    dnf install <RPM package path>
    # Or for older systems: yum install <RPM package path>
    
    # For DEB (Ubuntu)
    apt install <DEB package path>
    # Or alternatively: dpkg -i <DEB package path> && apt-get install -f
    ```

3. 授予 `gpadmin` 用户访问 `/usr/local/cloudberry-db/` 目录的权限。

    ```bash
    chown -R gpadmin:gpadmin /usr/local/cloudberry*
    ```

4. 为节点配置本地 SSH 连接。以 `gpadmin` 用户身份执行以下操作：

    ```bash
    ssh-keygen
    ssh-copy-id localhost
    ssh `hostname` # Makes sure that the local SSH connection works well.
    ```

### 步骤 3：以单计算节点部署 Apache Cloudberry {#step-3-deploy-apache-cloudberry-with-a-single-computing-node}

使用脚本工具 [`gpdemo`](/cloudberry/reference/sys-utilities/gpdemo/) 快速部署 Apache Cloudberry。`gpdemo` 包含在 RPM 软件包中，会与配置脚本（gpinitsystem、gpstart 和 gpstop）一起安装到 `GPHOME/bin` 目录。`gpdemo` 支持快速部署单计算节点的 Apache Cloudberry。

在前面的[设置 XFS 文件系统挂载选项](#set-mount-options-for-the-xfs-file-system)一节中，XFS 文件系统的数据目录挂载于 `/data0`。以下命令在此数据目录中部署单计算节点集群：

```bash
cd /data0
NUM_PRIMARY_MIRROR_PAIRS=0 gpdemo  # Uses gpdemo
```

运行 `gpdemo` 时，会输出警告 `[WARNING]: -SinglenodeMode has been enabled, no segment will be created.`，表示当前正在以单计算节点模式部署 Apache Cloudberry。

## 常见问题 {#common-issues}

### 如何检查集群的部署模式 {#how-to-check-the-deployment-mode-of-a-cluster}

执行以下步骤，确认当前 Apache Cloudberry 集群的部署模式：

1. 连接 Coordinator 节点。
2. 执行 `SHOW gp_role;`，查看集群的运行模式。

    - 如果返回 `utility`，表示集群处于 utility 模式（维护模式），只有 Coordinator 节点可用。

        继续运行 `SHOW gp_internal_is_singlenode;` 命令，查看集群是否处于单计算节点模式。

        - 如果返回 `on`，当前集群处于单计算节点模式。
        - 如果返回 `off`，当前集群处于 utility 维护模式。

    - 如果返回 `dispatch`，表示当前集群是包含 Segment 节点的普通集群。可以运行 `SELECT * FROM n;`，进一步查看集群的 Segment 数量、状态、端口、数据目录等信息。

### 数据目录在哪里 {#where-is-the-data-directory}

`gpdemo` 会在当前路径（`$PWD`）下自动创建数据目录。对于单计算节点部署：

- Coordinator 的默认目录为 `./datadirs/singlenodedir`。
- Standby Coordinator 节点的默认目录为 `./datadirs/standby`。

## 工作原理 {#how-it-works}

以单计算节点模式部署 Apache Cloudberry 时，部署脚本 `gpdemo` 会将 `gp_internal_is_singlenode = true` 写入配置文件 `postgresql.conf`，并以 `gp_role = utility` 参数设置启动一个 Coordinator 和一个 Standby Coordinator 节点。所有数据都写入本地，不使用 Segment，也不进行数据分布。

## 使用行为变化 {#user-behavior-changes}

在单计算节点模式下，Apache Cloudberry 的产品行为有以下变化。执行相关操作前，应留意这些变化：

- 执行 `CREATE TABLE` 创建表时，`DISTRIBUTED BY` 子句不再生效，并输出警告：`WARNING: DISTRIBUTED BY clause has no effect in singlenode mode`。
- `SELECT` 语句的 `SCATTER BY` 子句不再生效，并输出警告：`WARNING: SCATTER BY clause has no effect in singlenode mode`。
- 其他不受支持的语句（例如 `ALTER TABLE SET DISTRIBUTED BY`）会被拒绝，并返回错误。
- 由于只有单个节点，不存在全局事务或全局死锁，`UPDATE` 和 `DELETE` 语句的锁级别会从 `ExclusiveLock` 降低为 `RowExclusiveLock`，以提供更好的并发性能。此行为与 PostgreSQL 一致。
