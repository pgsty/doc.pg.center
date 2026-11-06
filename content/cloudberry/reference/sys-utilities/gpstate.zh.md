---
title: "gpstate"
description: "显示正在运行的 Apache Cloudberry 系统的状态。"
weight: 290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpstate.md"
---

## 概要 {#synopsis}

```shell
gpstate [-d <coordinator_data_directory>] [-B <parallel_processes>] 
          [-s | -b | -Q | -e] [-m | -c] [-p] [-i] [-f] [-v | -q] | -x 
          [-l <log_directory>]

gpstate -? | -h | --help
```

## 说明 {#description}

`gpstate` 工具显示正在运行的 Apache Cloudberry 实例的信息。Apache Cloudberry 系统由跨多台机器的多个 PostgreSQL 数据库实例（Segment）组成，因此可能需要了解一些额外信息。`gpstate` 工具提供系统的其他状态信息，例如：

- 哪些 Segment 已停机。
- Coordinator 和 Segment 的配置信息（主机、数据目录等）。
- 系统使用的端口。
- 主 Segment 与其对应镜像 Segment 的映射。

## 选项 {#options}

**`-b (brief status)`**

可选。显示 Apache Cloudberry 系统状态的简要汇总。这是默认选项。

**`-B parallel_processes`**

并行检查的 Segment 数量。需要在此选项后指定一个数字，例如 `gpstate -B 3`。

**`-c (show primary to mirror mappings)`**

可选。显示主 Segment 与其对应镜像 Segment 的映射。

**`-d coordinator_data_directory`**

可选。Coordinator 数据目录。需要在此选项后指定数据目录，例如 `gpstate -d /data/master/gpseg-1`。

**`-e (show segments with mirror status issues)`**

显示可能存在问题的主／镜像 Segment 对的详细信息。这些问题包括：

- 是否有 Segment 已停机。
- 是否有主／镜像 Segment 对未同步，包括还需同步多少字节的信息（显示在 `WAL sync remaining bytes` 输出字段中）。

> [!NOTE]
> `gpstate -e` 不显示已同步的 Segment 对。

- 是否有主／镜像 Segment 对未处于其首选角色。

**`-f (show standby coordinator details)`**
如果配置了 Standby Coordinator 主机，显示其详细信息。

**`-i (show Apache Cloudberry version)`**

显示每个实例的 Apache Cloudberry 软件版本信息。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-m (list mirrors)`**

可选。列出系统中的镜像 Segment 实例及其当前角色。

**`-p (show ports)`**

列出整个 Apache Cloudberry 系统使用的端口号。

**`-q (no screen output)`**

可选。以静默模式运行。除警告消息外，命令输出不显示在屏幕上，但仍会写入日志文件。

**`-Q (quick status)`**

可选。检查 Coordinator 主机系统目录中的 Segment 状态，不轮询 Segment 获取状态。

**`-s (detailed status)`**

可选。显示 Apache Cloudberry 系统的详细状态信息。

**`-v (verbose output)`**

可选。显示错误消息，并输出详细的状态和进度信息。

**`-x (expand)`**

可选。显示 Apache Cloudberry 系统扩容进度和状态的详细信息。

**`-? | -h | --help (help)`**

显示在线帮助。

## 输出字段定义 {#output-field-definitions}

`gpstate -s` 为 Coordinator 报告以下输出字段：

|输出数据|说明|
|-----------|-----------|
|Coordinator host|Coordinator 的主机名|
|Coordinator postgres process ID|Coordinator 数据库监听进程的 PID|
|Coordinator data directory|Coordinator 数据目录在文件系统中的位置|
|Coordinator port|Coordinator 的 `postgres` 数据库监听进程端口|
|Coordinator current role|dispatch = 常规运行模式<br/><br/>utility = 维护模式|
|Cloudberry array configuration type|Standard = 每台主机一个 NIC<br/><br/>Multi-Home = 每台主机多个 NIC|
|Cloudberry initsystem version|系统首次初始化时的 Apache Cloudberry 版本|
|Cloudberry current version|Apache Cloudberry 当前版本|
|Postgres version|Apache Cloudberry 所基于的 PostgreSQL 版本|
|Cloudberry mirroring status|物理镜像或无镜像|
|Coordinator standby|Standby Coordinator 的主机名|
|Standby coordinator state|Standby Coordinator 的状态：active 或 passive|

`gpstate -s` 为每个主 Segment 报告以下输出字段：

|输出数据|说明|
|-----------|-----------|
|Hostname|系统配置的主机名|
|Address|网络地址主机名（NIC 名称）|
|Datadir|Segment 数据目录在文件系统中的位置|
|Port|Segment 的 `postgres` 数据库监听进程端口号|
|Current Role|Segment 当前角色：Mirror 或 Primary|
|Preferred Role|系统初始化时的角色：Mirror 或 Primary|
|Mirror Status|主／镜像 Segment 对的状态：<br/><br/>Synchronized = 两者的数据都是最新的<br/><br/>Not in Sync = 镜像 Segment 尚未追上主 Segment|
|Current write location|主 Segment 写入新到达日志的位置|
|Bytes remaining to send to mirror|主实例尚需发送给镜像的字节数|
|Active PID|Segment 的活动进程 ID|
|Configuration reports status as|系统目录报告的 Segment 状态：Up 或 Down|
|Database status|Apache Cloudberry 处理传入请求的状态：Up、Down 或 Suspended。Suspended 状态表示 Segment 从一种状态切换到另一种状态时，数据库活动暂时暂停。|

`gpstate -s` 为每个镜像 Segment 报告以下输出字段：

|输出数据|说明|
|-----------|-----------|
|Hostname|系统配置的主机名|
|Address|网络地址主机名（NIC 名称）|
|Datadir|Segment 数据目录在文件系统中的位置|
|Port|Segment 的 `postgres` 数据库监听进程端口号|
|Current Role|Segment 当前角色：Mirror 或 Primary|
|Preferred Role|系统初始化时的角色：Mirror 或 Primary|
|Mirror Status|主／镜像 Segment 对的状态：<br/><br/>Synchronized = 两者的数据都是最新的<br/><br/>Not in Sync = 镜像 Segment 尚未追上主 Segment|
|WAL Sent Location|主 Segment 已向镜像发送日志数据的位置|
|WAL Flush Location|镜像 Segment 已将日志数据刷入磁盘的位置|
|WAL Replay Location|镜像 Segment 已在本地重放日志的位置|
|Bytes received but remain to flush|日志刷盘位置与发送位置之间的差值|
|Bytes received but remain to replay|日志重放位置与发送位置之间的差值|
|Active PID|Segment 的活动进程 ID|
|Configuration reports status as|系统目录报告的 Segment 状态：Up 或 Down|
|Database status|Apache Cloudberry 处理传入请求的状态：Up、Down 或 Suspended。Suspended 状态表示 Segment 从一种状态切换到另一种状态时，数据库活动暂时暂停。|

> [!NOTE]
> 主 Segment 与其镜像之间没有连接时，`gpstate -s` 会在以下字段中显示 `Unknown`：
>
> - `Bytes remaining to send to mirror`
> - `WAL Sent Location`
> - `WAL Flush Location`
> - `WAL Replay Location`
> - `Bytes received but remain to flush`
> - `Bytes received but remain to replay`

`gpstate -f` 为 Standby Coordinator 复制状态报告以下输出字段：

|输出数据|说明|
|-----------|-----------|
|Standby address|Standby Coordinator 的主机名|
|Standby data dir|Standby Coordinator 数据目录在文件系统中的位置|
|Standby port|Standby Coordinator 的 `postgres` 数据库监听进程端口|
|Standby PID|Standby Coordinator 的进程 ID|
|Standby status|Standby Coordinator 的状态：Standby host passive|
|WAL Sender State|预写式日志（WAL）流传输状态：streaming、startup、backup、catchup|
|Sync state|WAL 发送进程的同步状态：sync|
|Sent Location|WAL 发送进程已发送事务日志（xlog）记录的位置|
|Flush Location|WAL 接收进程已刷盘的 xlog 记录位置|
|Replay Location|备用实例已重放的 xlog 记录位置|

## 示例 {#examples}

显示 Apache Cloudberry 系统的详细状态信息：

```shell
gpstate -s
```

快速检查 Coordinator 主机系统目录中是否有停机的 Segment：

```shell
gpstate -Q
```

显示镜像 Segment 实例的信息：

```shell
gpstate -m
```

显示 Standby Coordinator 配置的信息：

```shell
gpstate -f
```

显示 Apache Cloudberry 软件版本信息：

```shell
gpstate -i
```

## 另请参阅 {#see-also}

[gpstart](/cloudberry/reference/sys-utilities/gpstart/), [gpexpand](/cloudberry/reference/sys-utilities/gpinitsystem/), [gplogfilter](/cloudberry/reference/sys-utilities/gplogfilter/)
