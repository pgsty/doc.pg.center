---
title: "gpactivatestandby"
description: "激活 Standby Coordinator 主机，使其成为 Apache Cloudberry 系统的活动 Coordinator。"
weight: 430
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpactivatestandby.md"
---

## 概要 {#synopsis}

```shell
gpactivatestandby [-d <standby_coordinator_datadir>] [-f] [-a] [-q] 
    [-l <logfile_directory>]

gpactivatestandby -v 

gpactivatestandby -? | -h | --help
```

## 说明 {#description}

`gpactivatestandby` 工具激活作为备份的 Standby Coordinator 主机，使其作为 Apache Cloudberry 系统的活动 Coordinator 实例运行。激活后的 Standby Coordinator 实际上成为 Apache Cloudberry 的 Coordinator，在 Coordinator 端口上接受客户端连接。

>**注意**
>运行 `gpactivatestandby` 前，务必运行 `gpstate -f`，确认 Standby Coordinator 已与当前 Coordinator 节点同步。如果已同步，`gpstate -f` 输出的最后一行将类似于：`20230607:06:50:06:004205 gpstate:test1-m:gpadmin-[INFO]:--Sync state: sync`

初始化 Standby Coordinator 时，默认使用与活动 Coordinator 相同的端口。有关 Standby Coordinator 的 Coordinator 端口信息，请参阅 [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/)。

必须在即将激活的 Coordinator 主机上运行此工具，而不是在即将停用的故障 Coordinator 主机上运行。此工具假定系统已配置 Standby Coordinator 主机（参阅 [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/)）。

此工具执行以下步骤：

- 停止 Standby Coordinator 上的同步进程（`walreceiver`）
- 使用日志更新 Standby Coordinator 的系统目录表
- 激活 Standby Coordinator，使其成为系统新的活动 Coordinator
- 使用新的 Coordinator 主机重启 Apache Cloudberry 系统

作为备份的 Cloudberry Standby Coordinator 主机在主 Coordinator 主机无法运行时充当“温备”。事务日志复制进程（`walsender` 和 `walreceiver`）分别运行在主 Coordinator 和 Standby Coordinator 主机上，使两台主机之间的数据保持同步，从而让 Standby Coordinator 持续保持最新状态。

如果主 Coordinator 发生故障，日志复制进程将关闭，此时可以使用 `gpactivatestandby` 工具激活 Standby Coordinator 来接替它。激活 Standby Coordinator 时，会使用已复制的日志重建最后一次成功提交事务时 Cloudberry Coordinator 主机的状态。

使用 `gpactivatestandby` 激活新的主 Coordinator 主机时，原先承担主 Coordinator 角色的主机必须已停止运行。此工具会检查已停用 Coordinator 主机的数据目录中是否存在 `postmaster.pid` 文件；如果找到该文件，就会认为原 Coordinator 主机仍处于活动状态。在某些情况下，运行 `gpactivatestandby` 前可能需要从已停用 Coordinator 主机的数据目录中删除 `postmaster.pid` 文件（例如，该主机的进程意外终止时）。

激活 Standby Coordinator 后，运行 `ANALYZE` 更新数据库查询统计信息。例如：

```shell
psql <dbname> -c 'ANALYZE;'
```

将 Standby Coordinator 激活为主 Coordinator 后，Apache Cloudberry 系统便不再配置有 Standby Coordinator。你可能希望使用 [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/) 工具指定另一台主机作为新的 Standby Coordinator。

## 选项 {#options}

**`-a (do not prompt)`**

不提示用户确认。

**`-d standby_coordinator_datadir`**

即将激活的 Coordinator 主机的数据目录绝对路径。

如果未指定此选项，`gpactivatestandby` 将使用即将激活的 Coordinator 主机上 `COORDINATOR_DATA_DIRECTORY` 环境变量的值。如果指定了此选项，它将覆盖 `COORDINATOR_DATA_DIRECTORY` 的任何设置。

如果无法确定目录，此工具将返回错误。

**`-f (force activation)`**

使用此选项强制激活备用 Coordinator 主机。仅在确定 Standby Coordinator 与主 Coordinator 主机一致时使用此选项。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-q (no screen output)`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-v (show utility version)`**

显示此工具的版本、状态、最后更新日期和校验和。

**`-? | -h | --help (help)`**

显示在线帮助。

## 示例 {#example}

激活 Standby Coordinator 主机，使其成为 Apache Cloudberry 系统的活动 Coordinator 实例（在即将激活的备用 Coordinator 主机上运行）：

```shell
gpactivatestandby -d /gpdata
```

## 另请参阅 {#see-also}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/), [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/)
