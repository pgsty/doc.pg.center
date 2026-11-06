---
title: "快速部署指南"
description: "本指南为有经验的管理员提供简明的操作流程，便于直接复制粘贴执行。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/quick-deploy.md"
---

本指南介绍如何部署一个包含 5 个节点的 Apache Cloudberry 集群：

- 1 个 Coordinator（`cdw`）
- 1 个 Standby Coordinator（`scdw`）
- 3 个 Segment（`sdw1`、`sdw2`、`sdw3`），每个节点包含 2 个主实例和 2 个镜像实例

> [!NOTE] 说明
> 有关每个步骤的详细说明，请参阅完整部署指南：
> [配置系统](/cloudberry/deployment/prepare-to-deploy/)、[使用 RPM/DEB 软件包安装](/cloudberry/deployment/install_cloudberry/)、[创建数据存储区域](/cloudberry/deployment/create_data_dirs/)和[初始化 Apache Cloudberry](/cloudberry/deployment/init_cloudberry/)。

## 集群布局 {#cluster-layout}

| 主机 | 角色 | IP（示例） |
|------|------|--------------|
| cdw | Coordinator | 192.168.1.1 |
| scdw | Standby Coordinator | 192.168.1.2 |
| sdw1 | Segment 1 | 192.168.1.3 |
| sdw2 | Segment 2 | 192.168.1.4 |
| sdw3 | Segment 3 | 192.168.1.5 |

使用的数据目录：

- Coordinator/Standby Coordinator：`/data/coordinator`
- 主 Segment：`/data/primary`（每台主机 2 个实例）
- 镜像 Segment：`/data/mirror`（每台主机 2 个实例）

---

## 1. 配置系统（在所有主机上以 root 身份执行） {#1-configuring-your-systems-as-root-on-all-hosts}

### 1.1 停用 SELinux {#11-deactivate-selinux}

> [!NOTE] 说明
> 此步骤仅适用于 RHEL/Oracle/Rocky Linux。Ubuntu 默认不安装 SELinux，可以跳过此步骤。

```bash
# Check current status
sestatus

# If not disabled, deactivate it
sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config

# Reboot is required to take effect
```

### 1.2 停用防火墙 {#12-deactivate-firewall}

**适用于 RHEL/Rocky Linux（firewalld）：**

```bash
# Check current status
systemctl status firewalld

# If not disabled, deactivate it
systemctl stop firewalld.service
systemctl disable firewalld.service
```

**适用于 Ubuntu（ufw）：**

```bash
# Check current status (disabled by default)
ufw status

# If active, disable it
ufw disable
```

### 1.3 设置 hosts 文件 {#13-set-the-hosts-file}

设置每台主机的主机名（立即生效，无需重启）：

```bash
# Run on each host respectively
hostnamectl set-hostname cdw    # on coordinator
hostnamectl set-hostname scdw   # on standby coordinator
hostnamectl set-hostname sdw1   # on segment 1
hostnamectl set-hostname sdw2   # on segment 2
hostnamectl set-hostname sdw3   # on segment 3

# Verify
hostname

# Refresh the shell prompt to show the new hostname
exec bash
```

编辑所有主机上的 `/etc/hosts`：

```bash
cat >> /etc/hosts <<EOF
192.168.1.1  cdw
192.168.1.2  scdw
192.168.1.3  sdw1
192.168.1.4  sdw2
192.168.1.5  sdw3
EOF
```

### 1.4 设置 sysctl.conf 参数 {#14-set-sysctlconf-parameters}

```bash
cat >> /etc/sysctl.conf <<EOF
kernel.shmall = 197951838
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
kernel.core_pattern=/var/core/core.%h.%t
EOF

mkdir -p /var/core
sysctl -p
```

> [!NOTE] 说明
> 上述 `kernel.shmall` 和 `kernel.shmmax` 值是针对内存约为 1583 GB 的主机给出的示例。请为实际系统计算正确的值：
>
> ```bash
> echo $(expr $(getconf _PHYS_PAGES) / 2)              # kernel.shmall
> echo $(expr $(getconf _PHYS_PAGES) / 2 \* $(getconf PAGE_SIZE))  # kernel.shmmax
> ```

### 1.5 设置系统资源限制 {#15-set-system-resource-limits}

```bash
cat >> /etc/security/limits.conf <<EOF
* soft nofile 524288
* hard nofile 524288
* soft nproc 131072
* hard nproc 131072
* soft core unlimited
EOF
```

- `nofile` — 打开的文件描述符数量上限
- `nproc` — 进程数上限
- `core` — 核心转储文件大小（unlimited 表示启用核心转储，用于调试）

### 1.6 XFS 挂载选项 {#16-xfs-mount-options}

> [!NOTE] 说明
> 如果使用只有一块系统盘、没有额外数据盘的云虚拟机，可以跳过以下磁盘格式化和挂载步骤，直接在现有文件系统上创建数据目录：
>
> ```bash
> mkdir -p /data
> ```
>
> 以下 XFS 格式化步骤适用于具有专用数据盘的情况。

```bash
mkdir -p /data
mkfs.xfs -f /dev/sdb   # adjust device name as needed

# Use device name directly
echo "/dev/sdb /data xfs rw,nodev,noatime,inode64 0 0" >> /etc/fstab
# Or use UUID for stable identification across reboots (recommended for cloud/VM environments)
# echo "UUID=$(blkid -s UUID -o value /dev/vdb1) /data xfs rw,nodev,noatime,inode64 0 0" >> /etc/fstab

mount /data
```

### 1.7 磁盘 I/O 设置 {#17-disk-io-settings}

```bash
# Set read-ahead value
/sbin/blockdev --setra 16384 /dev/sdb

# Persist read-ahead across reboots
echo '/sbin/blockdev --setra 16384 /dev/sdb' >> /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local

# Set I/O scheduler permanently (for non-NVMe/SSD disks)
# For RHEL/Rocky Linux:
grubby --update-kernel=ALL --args="elevator=mq-deadline"
# For Ubuntu:
sed -i 's/GRUB_CMDLINE_LINUX="\(.*\)"/GRUB_CMDLINE_LINUX="\1 elevator=mq-deadline"/' /etc/default/grub && update-grub
```

### 1.8 禁用透明大页 {#18-disable-transparent-huge-pages}

```bash
# Check current THP status
cat /sys/kernel/mm/*transparent_hugepage/enabled

# If not [never], disable it permanently
# For RHEL/Rocky Linux:
grubby --update-kernel=ALL --args="transparent_hugepage=never"
# For Ubuntu:
sed -i 's/GRUB_CMDLINE_LINUX="\(.*\)"/GRUB_CMDLINE_LINUX="\1 transparent_hugepage=never"/' /etc/default/grub && update-grub

# Reboot is required to take effect
```

### 1.9 禁用 IPC 对象移除 {#19-disable-ipc-object-removal}

```bash
sed -i 's/^#RemoveIPC=.*/RemoveIPC=no/' /etc/systemd/logind.conf
service systemd-logind restart
```

### 1.10 SSH 连接阈值 {#110-ssh-connection-threshold}

```bash
sed -i 's/^#MaxStartups.*/MaxStartups 10:30:200/' /etc/ssh/sshd_config
sed -i 's/^#MaxSessions.*/MaxSessions 200/' /etc/ssh/sshd_config
service sshd restart
```

### 1.11 同步系统时钟 {#111-synchronize-system-clocks}

```bash
# For RHEL/Rocky Linux
systemctl enable chronyd
systemctl restart chronyd
chronyc tracking

# For Ubuntu (enable must use 'chrony', restart works with either name)
systemctl enable chrony
systemctl restart chronyd
chronyc tracking
```

### 1.12 创建 gpadmin 管理用户 {#112-create-the-gpadmin-administrative-user}

```bash
groupadd gpadmin
useradd gpadmin -r -m -g gpadmin
passwd gpadmin

# Grant passwordless sudo
# For RHEL/Rocky Linux: uncomment the %wheel NOPASSWD line in sudoers
# Or use visudo to uncomment: %wheel ALL=(ALL) NOPASSWD: ALL
sed -i 's/^# %wheel\tALL=(ALL)\tNOPASSWD: ALL/%wheel\tALL=(ALL)\tNOPASSWD: ALL/' /etc/sudoers
usermod -aG wheel gpadmin

# For Ubuntu: add gpadmin to sudo group and create a sudoers drop-in file
usermod -aG sudo gpadmin
echo "gpadmin ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/gpadmin
chmod 440 /etc/sudoers.d/gpadmin

# Set data directory ownership to gpadmin
chown -R gpadmin:gpadmin /data
```

> [!NOTE] 说明
> 确保 `gpadmin` 用户在所有主机上的 UID/GID 相同。使用 `id gpadmin` 验证，或向 `groupadd` 传入 `-g <gid>`、向 `useradd` 传入 `-u <uid>`，以设置固定值。

---

## 2. 安装 Apache Cloudberry 软件包（在每台主机上以 root 身份执行） {#2-install-the-apache-cloudberry-package-as-root-on-each-host}

从 [Apache Cloudberry 发布页面](https://cloudberry.apache.org/releases)将软件包下载到每台主机的 `/home/gpadmin/` 目录，然后安装：

```bash
# For RPM (Rocky Linux, RHEL, etc.)
dnf install /home/gpadmin/apache-cloudberry-db-incubating-*.rpm

# For DEB (Ubuntu)
# apt install --fix-broken /home/gpadmin/apache-cloudberry-db-incubating-*.deb

# Set ownership
chown -R gpadmin:gpadmin /usr/local/cloudberry*
```

---

## 3. 启用免密 SSH（在 cdw 上以 gpadmin 身份执行） {#3-enable-passwordless-ssh-as-gpadmin-on-cdw}

```bash
su - gpadmin
source /usr/local/cloudberry-db/cloudberry-env.sh

# Generate SSH key (press Enter at passphrase prompts)
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa

# Enable 1-n passwordless SSH (will prompt for gpadmin password)
ssh-copy-id cdw
ssh-copy-id scdw
ssh-copy-id sdw1
ssh-copy-id sdw2
ssh-copy-id sdw3

# Create the host file for gpssh-exkeys
cat > ~/hostfile_exkeys <<EOF
cdw
scdw
sdw1
sdw2
sdw3
EOF

# Enable n-n passwordless SSH
gpssh-exkeys -f ~/hostfile_exkeys

# Verify
gpssh -f ~/hostfile_exkeys -e 'hostname'
```

### 确认安装 {#confirm-the-installation}

```bash
gpssh -f ~/hostfile_exkeys -e 'ls -l /usr/local/cloudberry-db-*'
```

---

## 4. 创建数据存储区域（在 cdw 上以 gpadmin 身份执行） {#4-create-data-storage-areas-as-gpadmin-on-cdw}

```bash
source /usr/local/cloudberry-db/cloudberry-env.sh

# Coordinator data directory
sudo mkdir -p /data/coordinator
sudo chown gpadmin:gpadmin /data/coordinator

# Standby coordinator data directory
gpssh -h scdw -e 'sudo mkdir -p /data/coordinator'
gpssh -h scdw -e 'sudo chown gpadmin:gpadmin /data/coordinator'

# Segment host file
cat > ~/hostfile_gpinitsystem <<EOF
sdw1
sdw2
sdw3
EOF

# Segment primary and mirror directories
gpssh -f ~/hostfile_gpinitsystem -e 'sudo mkdir -p /data/primary'
gpssh -f ~/hostfile_gpinitsystem -e 'sudo mkdir -p /data/mirror'
gpssh -f ~/hostfile_gpinitsystem -e 'sudo chown -R gpadmin:gpadmin /data'
```

---

## 5. 初始化集群（在 cdw 上以 gpadmin 身份执行） {#5-initialize-the-cluster-as-gpadmin-on-cdw}

### 5.1 创建初始化主机文件 {#51-create-the-initialization-host-file}

```bash
# Already created in step 4 as ~/hostfile_gpinitsystem
cat ~/hostfile_gpinitsystem
```

### 5.2 创建配置文件 {#52-create-the-configuration-file}

```bash
mkdir -p ~/gpconfigs

cat > ~/gpconfigs/gpinitsystem_config <<EOF
SEG_PREFIX=gpseg
PORT_BASE=6000
declare -a DATA_DIRECTORY=(/data/primary /data/primary)
COORDINATOR_HOSTNAME=cdw
COORDINATOR_DIRECTORY=/data/coordinator
COORDINATOR_PORT=5432
TRUSTED_SHELL=ssh
CHECK_POINT_SEGMENTS=8
ENCODING=UNICODE
MIRROR_PORT_BASE=7000
declare -a MIRROR_DATA_DIRECTORY=(/data/mirror /data/mirror)
DATABASE_NAME=warehouse
EOF
```

### 5.3 运行初始化工具 {#53-run-the-initialization-utility}

```bash
gpinitsystem -c ~/gpconfigs/gpinitsystem_config -h ~/hostfile_gpinitsystem \
    -s scdw --mirror-mode=spread
```

出现提示时，输入 `y` 继续。成功后应看到：

```
=> Apache Cloudberry instance successfully created.
```

> [!TIP] 提示
> `-s scdw` 选项会在创建集群时初始化 Standby Coordinator。如果运行 `gpinitsystem` 时省略了 `-s`，可以在之后单独初始化 Standby Coordinator：
>
> ```bash
> gpinitstandby -s scdw
> ```
>
> 验证 Standby Coordinator 已同步：
>
> ```bash
> gpstate -f
> ```

### 5.4 设置时区（可选） {#54-set-the-timezone-optional}

```bash
gpconfig -c TimeZone -v 'US/Pacific'
gpstop -ra
```

### 5.5 设置环境变量 {#55-set-environment-variables}

```bash
cat >> ~/.bashrc <<EOF
source /usr/local/cloudberry-db/cloudberry-env.sh
export COORDINATOR_DATA_DIRECTORY=/data/coordinator/gpseg-1
export PGPORT=5432
export PGUSER=gpadmin
export PGDATABASE=warehouse
# (Optional) RHEL/Rocky Linux: ensure ps works under cloudberry-env.sh
export LD_PRELOAD=/lib64/libz.so.1 ps
EOF

source ~/.bashrc

# Copy to standby
scp ~/.bashrc scdw:~/
```

---

## 6. 登录 Apache Cloudberry {#6-log-into-apache-cloudberry}

```bash
psql -d warehouse
```

检查集群状态：

```sql
warehouse=# SELECT * FROM gp_segment_configuration ORDER BY content, role;
```

---

## 集群操作速查 {#quick-reference-cluster-operations}

```bash
# Check cluster status
gpstate -s

# Stop the cluster
gpstop -a

# Start the cluster
gpstart -a

# Restart the cluster
gpstop -ra
```
