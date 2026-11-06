---
title: "gpinitstandby"
description: "为 Apache Cloudberry 系统添加和／或初始化 Standby Coordinator 主机。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpinitstandby.md"
---

## 概要 {#synopsis}

```shell
gpinitstandby { -s <standby_hostname> [-P port] | -r | -n } [-a] [-q] 
    [-D] [-S <standby_data_directory>] [-l <logfile_directory>] 
    [--hba-hostnames <boolean>] 

gpinitstandby -v 

gpinitstandby -?
```

## 说明 {#description}

`gpinitstandby` 工具为 Apache Cloudberry 系统添加作为备份的 Standby Coordinator 实例。如果系统已配置 Standby Coordinator 实例，应先用 `-r` 选项移除它，再添加新的 Standby Coordinator 实例。

运行此工具前，确保 Standby Coordinator 主机已安装 Apache Cloudberry 软件，且主机之间已交换 SSH 密钥。建议将 Coordinator 主机与 Standby Coordinator 主机上的 Coordinator 端口设为相同端口号。

应在当前活动的*主* Coordinator 主机上运行此工具。

此工具执行以下步骤：

- 更新 Apache Cloudberry 系统目录，移除现有 Standby Coordinator 信息（如果提供了 `-r` 选项）
- 更新 Apache Cloudberry 系统目录，添加新的 Standby Coordinator 实例信息
- 编辑 Apache Cloudberry Coordinator 的 `pg_hba.conf` 文件，允许新添加的 Standby Coordinator 访问
- 在备用 Coordinator 主机上设置 Standby Coordinator 实例
- 启动同步进程

作为备份的 Standby Coordinator 实例在主 Coordinator 无法运行时充当“温备”。事务日志复制进程（`walsender` 和 `walreceiver`）分别运行在主 Coordinator 和 Standby Coordinator 主机上，使两个实例之间的数据保持同步，从而让 Standby Coordinator 持续保持最新状态。如果主 Coordinator 发生故障，日志复制进程将关闭，此时可以使用 `gpactivatestandby` 工具激活 Standby Coordinator 来接替它。激活 Standby Coordinator 时，会使用已复制的日志重建最后一次成功提交事务时 Coordinator 实例的状态。

激活后的 Standby Coordinator 实际上成为 Apache Cloudberry Coordinator，在 Coordinator 端口上接受客户端连接，并执行 SQL 命令处理、资源管理等常规 Coordinator 操作。

> **重要** 如果 `gpinitstandby` 工具先前未能成功初始化 Standby Coordinator，再次运行 `gpinitstandby` 前，必须删除 Standby Coordinator 数据目录中的文件。初始化失败后不会自动清理此数据目录，因为其中的日志文件有助于确定失败原因。

如果初始化失败，会在备用主机的 `/tmp` 目录中生成汇总报告文件，列出需要清理的目录。

## 选项 {#options}

**`-a (do not prompt)`**

不提示用户确认。

**`-D (debug)`**

将日志级别设为 debug。

**`--hba-hostnames boolean`**

可选。控制此工具更新 `pg_hba.conf` 文件中可连接 Apache Cloudberry 的地址时使用 IP 地址还是主机名。设为 0（默认值）时，使用 IP 地址更新文件；设为 1 时，使用主机名更新文件。为保持一致，应使用初始化 Apache Cloudberry 系统时为 `HBA_HOSTNAMES` 指定的相同值。 <!-- For information about how Apache Cloudberry resolves host names in the `pg_hba.conf` file, see [Configuring Client Authentication](/cloudberry/security/client-auth/). -->

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-n (restart standby coordinator)`**

指定此选项，可启动已配置但因某种原因停止的 Apache Cloudberry Standby Coordinator。

**`-P port`**

此选项指定 Apache Cloudberry Standby Coordinator 使用的端口。默认与活动 Apache Cloudberry Coordinator 使用的端口相同。

如果 Apache Cloudberry Standby Coordinator 与活动 Coordinator 位于同一主机上，端口必须不同。如果两者位于同一主机且端口相同，此工具会返回错误。

**`-q (no screen output)`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-r (remove standby coordinator)`**

从 Apache Cloudberry 系统中移除当前配置的 Standby Coordinator 实例。

**`-s standby_hostname`**

Standby Coordinator 主机的主机名。

**`-S standby_data_directory`**

新 Standby Coordinator 使用的数据目录。默认与活动 Coordinator 使用的目录相同。

如果 Standby Coordinator 与活动 Coordinator 位于同一主机上，必须使用此选项指定不同的目录。

**`-v (show utility version)`**

显示此工具的版本、状态、最后更新日期和校验和。

**`-? (help)`**

显示在线帮助。

## 示例 {#examples}

为 Apache Cloudberry 系统添加 Standby Coordinator 实例并启动同步进程：

```shell
gpinitstandby -s host09
```

启动现有 Standby Coordinator 实例，并与当前主 Coordinator 实例同步数据：

```shell
gpinitstandby -n
```

> **注意** 不要在同一命令中指定 -n 和 -s 选项。

为 Apache Cloudberry 系统添加 Standby Coordinator 实例，并指定不同的端口：

```shell
gpinitstandby -s myhost -P 2222
```

如果指定的主机名与活动 Apache Cloudberry Coordinator 相同，还必须通过 `-P` 选项指定不同的端口号，并通过 `-S` 选项指定备用数据目录。

从 Cloudberry 系统配置中移除现有 Standby Coordinator：

```shell
gpinitstandby -r
```

## 另请参阅 {#see-also}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/), [gpaddmirrors](/cloudberry/reference/sys-utilities/gpaddmirrors/), [gpactivatestandby](/cloudberry/reference/sys-utilities/gpactivatestandby/)
