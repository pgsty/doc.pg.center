---
title: "gpexpand"
description: "将现有 Apache Cloudberry 扩容到系统中的新主机上。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpexpand.md"
---

## 概要 {#synopsis}

```shell
gpexpand [{-f|--hosts-file} <hosts_file>]
        | {-i|--input} <input_file> [-B <batch_size>]
        | [{-d | --duration} <hh:mm:ss> | {-e|--end} '<YYYY-MM-DD hh:mm:ss>'] 
          [-a|-analyze] 
          [-n  <parallel_processes>]
        | {-r|--rollback}
        | {-c|--clean}
        [-v|--verbose] [-s|--silent]
        [{-t|--tardir} <directory> ]
        [-S|--simple-progress ]

gpexpand -? | -h | --help 

gpexpand --version
```

## 前提条件 {#prerequisites}

- 已以 Apache Cloudberry 超级用户（`gpadmin`）身份登录。
- 已按现有 Segment 主机的方式安装和配置新的 Segment 主机。这包括：
    - 配置硬件和操作系统
    - 安装 Cloudberry 软件
    - 创建 `gpadmin` 用户账户
    - 交换 SSH 密钥。
- Segment 主机上有足够的磁盘空间，能够临时保存最大表的一份副本。
- 重分布数据时，Apache Cloudberry 必须以生产模式运行，不能处于受限模式或 Coordinator 模式。启动 Apache Cloudberry 时不能指定 `gpstart` 的 `-R` 或 `-m` 选项。

> **注意** `gpexpand` 执行 Segment 初始化时，不能运行以下工具。
>
> - `gpbackup`
> - `gpcheckcat`
> - `gpconfig`
> - `gppkg`
> - `gprestore`

> **重要** 扩容 Apache Cloudberry 系统时，在向系统添加新主机和 Segment 实例前，必须禁用 Cloudberry Interconnect 代理；重新启用 Interconnect 代理前，必须更新 `gp_interconnect_proxy_addresses` 参数，加入新添加的 Segment 实例。

## 说明 {#description}

`gpexpand` 工具分两个阶段执行系统扩容：先初始化 Segment 实例，再重分布表数据。

初始化阶段，`gpexpand` 使用输入文件运行，该文件指定新 Segment 实例的数据目录、dbid 值及其他属性。可以手动创建输入文件，也可以按交互式问答中的提示创建。

如果选择通过交互式问答创建输入文件，还可以指定一个包含扩容系统主机列表的文件。如果平台或命令 shell 限制了交互提示中可输入的主机名列表长度，就可能必须使用 `-f` 指定主机。

除初始化 Segment 实例外，初始化阶段还会执行以下操作：

- 在 postgres 数据库中创建名为 *gpexpand* 的扩容模式，用于保存扩容操作的状态，包括表的详细状态。

表数据重分布阶段，`gpexpand` 会重分布表数据，使数据在新旧 Segment 实例之间重新均衡分布。

> **注意** 数据重分布应在使用量较低的时段进行。可以将重分布分为多个批次，在较长时间内完成。

要开始重分布阶段，请运行不带选项的 `gpexpand`，或使用 `-d`（持续时间）、`-e`（结束时间）或 `-i` 选项。如果指定结束时间或持续时间，此工具将重分布扩容模式中的表，直到到达指定时间或持续时长。如果指定 `-i` 或未指定选项，重分布阶段会持续到扩容模式中的所有表都完成重组。每个表都使用 `ALTER TABLE` 命令重组，以在新增 Segment 之间重新均衡分布，并恢复表原有的分布策略。如果 `gpexpand` 完成所有表的重组，会显示成功消息并结束。

> **注意** 此工具通过系统之间的安全 shell（SSH）连接执行任务。在大型 Apache Cloudberry 部署、云部署，或每台主机包含大量 Segment 的部署中，此工具可能超过主机对未认证连接设置的最大阈值。可以考虑更新 SSH 的 `MaxStartups` 和 `MaxSessions` 配置参数以提高此阈值。有关 SSH 配置选项的更多信息，请参阅 Linux 发行版的 SSH 文档。

## 选项 {#options}

**`-a | --analyze`**

扩容后运行 `ANALYZE` 更新表统计信息。默认不运行 `ANALYZE`。

**`-B batch_size`**

向指定主机发送一批远程命令后暂停一秒，此处指定批次大小。默认值为 `16`。有效值为 1–128。

`gpexpand` 工具会发出多条设置命令，可能超过 SSH 守护进程配置中由 `MaxStartups` 定义的未认证连接最大阈值。暂停一秒可以让认证在 `gpexpand` 继续发出命令前完成。

通常无需更改默认值。但是，如果 `gpexpand` 因连接错误（如 `'ssh_exchange_identification: Connection closed by remote host.'`）失败，可能需要减少最大命令数。

**`-c | --clean`**

删除扩容模式。

**`-d | --duration hh:mm:ss`**

扩容会话从开始到结束的持续时间。

**`-e | --end 'YYYY-MM-DD hh:mm:ss'`**

扩容会话结束的日期和时间。

**`-f | --hosts-file filename`**

指定包含系统扩容所用新主机列表的文件名。文件每行必须只包含一个主机名。

此文件可以包含指定了网络接口的主机名，也可以包含未指定网络接口的主机名。`gpexpand` 工具可处理这两种情况；如果原有节点配置了多个网络接口，会在主机名末尾添加接口编号。

> **注意** Apache Cloudberry Segment 主机的命名约定为 `sdwN`，其中 `sdw` 是前缀，`N` 是整数。例如 `sdw1`、`sdw2` 等。对于具有多个接口的主机，约定在主机名后添加连字符（`-`）和数字。例如，`sdw1-1` 和 `sdw1-2` 是主机 `sdw1` 的两个接口名。

有关使用主机名或 IP 地址的信息，请参阅[使用主机名或 IP 地址指定主机](#specify-hosts-using-hostnames-or-ip-addresses)。另请参阅[使用具有多个 NIC 的主机系统](#use-host-systems-with-multiple-nics)。

**`-i | --input input_file`**

指定扩容配置文件名，每个待添加 Segment 占一行，格式如下：

hostname|address|port|datadir|dbid|content|preferred_role

**`-n parallel_processes`**

同时重分布的表数量。有效值为 1–96。

每个表重分布进程需要两个数据库连接：一个用于更改表，另一个用于更新扩容模式中该表的状态。增大 `-n` 前，请检查服务器配置参数 `max_connections` 的当前值，确保不会超出最大连接数限制。

**`-r | --rollback`**

回滚失败的扩容设置操作。

**`-s | --silent`**

以静默模式运行。遇到警告时，不提示确认是否继续。

**`-S | --simple-progress`**

如果指定此选项，`gpexpand` 工具仅在 Apache Cloudberry 表 *gpexpand.expansion_progress* 中记录最少的进度信息，不在表 *gpexpand.status_detail* 中记录关系大小和状态信息。

指定此选项可减少写入 *gpexpand* 表的进度信息量，从而提高性能。

**`[-t | --tardir] directory`**

Segment 主机上某个目录的完全限定路径，`gpexpand` 工具会将临时 tar 文件复制到此目录。该文件包含用于创建 Segment 实例的 Apache Cloudberry 文件。默认目录为用户主目录。

**`-v | --verbose`**

详细调试输出。使用此选项时，此工具会输出用于扩容数据库的所有 DDL 和 DML。

**`--version`**

显示工具版本号并退出。

**`-? | -h | --help`**

显示在线帮助。

## 使用主机名或 IP 地址指定主机 {#specify-hosts-using-hostnames-or-ip-addresses}

扩容 Apache Cloudberry 系统时，可以指定主机名或 IP 地址作为该值。

- 如果指定主机名，为安全起见，应在本地完成主机名到 IP 地址的解析。例如，应使用本地 `/etc/hosts` 文件中的条目将主机名映射到 IP 地址。不应通过公共 DNS 服务器等外部服务解析主机名。更改主机名到不同 IP 地址的映射前，必须停止 Cloudberry 系统。
- 如果指定 IP 地址，初始配置后不应更改该地址。启用 Segment 镜像后，如果 IP 地址与配置值不同，主 Segment 到镜像 Segment 的复制将失败。因此，除非有特定要求使用 IP 地址，否则扩容 Apache Cloudberry 系统时应使用主机名。

扩容 Cloudberry 系统时，`gpexpand` 会将新 Segment 实例信息填入 `gp_segment_configuration` 目录表。Apache Cloudberry 使用 `gp_segment_configuration` 目录表的 `address` 值查找主机系统，以进行 Coordinator 与 Segment 实例之间、以及 Segment 实例之间的 Cloudberry Interconnect（内部）通信和其他内部通信。

## 使用具有多个 NIC 的主机系统 {#use-host-systems-with-multiple-nics}

如果主机系统配置了多个 NIC，可以扩容 Apache Cloudberry 系统，让每个 NIC 都作为 Cloudberry 主机系统使用。必须确保主机系统配置了足够的资源，以支持要添加到主机上的所有 Segment 实例。此外，如果启用 Segment 镜像，必须确保扩容后的 Cloudberry 系统配置支持主机系统发生故障时的故障切换。

例如，以下是简单 Cloudberry 系统的 `gpexpand` 配置文件。Segment 主机 `gp7s1` 和 `gp7s2` 都配置了两个 NIC：`-s1` 和 `-s2`，Apache Cloudberry 系统将每个 NIC 作为一个主机系统使用。

```shell
gp7s1-s2|gp7s1-s2|40001|/data/data1/gpseg2|6|2|p
gp7s2-s1|gp7s2-s1|50000|/data/mirror1/gpseg2|9|2|m
gp7s2-s1|gp7s2-s1|40000|/data/data1/gpseg3|7|3|p
gp7s1-s2|gp7s1-s2|50001|/data/mirror1/gpseg3|8|3|m
```

## 示例 {#examples}

使用输入文件运行 `gpexpand`，初始化新 Segment，并在 postgres 数据库中创建扩容模式：

```shell
$ gpexpand -i input_file
```

运行 `gpexpand`，最多持续六十小时，将表重分布到新的 Segment：

```shell
$ gpexpand -d 60:00:00
```

## 另请参阅 {#see-also}

[gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/)
<!-- [Expanding a Cloudberry System](/cloudberry/sys-admin/expand-cluster/) -->
