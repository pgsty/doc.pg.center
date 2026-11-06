---
title: "gpstop"
description: "停止或重启 Apache Cloudberry 系统。"
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpstop.md"
---

## 概要 {#synopsis}

```shell
gpstop [-d <coordinator_data_directory>] [-B parallel_processes>] 
       [-M smart | fast | immediate] [-t <timeout_seconds>] [-r] [-y] [-a] 
       [-l <logfile_directory>] [-v | -q]

gpstop -m [-d <coordinator_data_directory>] [-y] [-l <logfile_directory>] [-v | -q]

gpstop -u [-d <coordinator_data_directory>] [-l <logfile_directory>] [-v | -q]
 
gpstop --host <host_namea> [-d <coordinator_data_directory>] [-l <logfile_directory>]
       [-t <timeout_seconds>] [-a] [-v | -q]

gpstop --version 

gpstop -? | -h | --help
```

## 说明 {#description}

`gpstop` 工具用于停止组成 Apache Cloudberry 系统的数据库服务器。停止 Apache Cloudberry 系统时，实际上是在同时停止多个 `postgres` 数据库服务器进程（Coordinator 和所有 Segment 实例）。`gpstop` 工具负责各实例的关闭，并行关闭各个实例。

默认关闭模式（`-M smart`）会等待当前客户端连接结束后再完成关闭。如果超时后仍有连接未关闭，或按 CTRL-C 中断，`gpstop` 会列出仍然打开的连接，并询问是继续等待连接结束，还是执行快速关闭或立即关闭。默认超时时间为 120 秒，可通过 `-t timeout_seconds` 选项更改。

指定 `-M fast` 关闭模式，会在关闭前回滚所有进行中的事务并终止所有连接。

使用 `-u` 选项，此工具会在不中断服务的情况下，加载对 Coordinator 的 `pg_hba.conf` 文件或 `postgresql.conf` 文件中*运行时*配置参数所做的更改。注意，所有活动会话只有重新连接数据库后才会采用这些更改。

## 选项 {#options}

**`-a`**

不提示用户确认。

**`-B parallel_processes`**

并行停止的 Segment 数量。需要在此选项后指定一个数字，例如 `gpstop -B 3`。

**`-d coordinator_data_directory`**

可选。Coordinator 主机的数据目录。需要在此选项后指定数据目录，例如 `gpstop -d /data/master/gpseg-1`。

**`--host host_name`**

此工具关闭指定主机上的 Apache Cloudberry Segment 实例，以便维护该主机。它会关闭该主机上的每个主 Segment 实例；如果相应的镜像 Segment 实例位于其他主机上，则将该镜像提升为主 Segment。该主机上的镜像 Segment 实例也会关闭。

在以下情况下，不会关闭 Segment 实例，且工具会返回错误：

- 系统未启用 Segment 镜像。
- Coordinator 或 Standby Coordinator 位于该主机上。
- 一个主 Segment 实例及其镜像均位于该主机上。

此选项不能与 `-m`、`-r`、`-u` 或 `-y` 选项同时指定。

> [!NOTE]
> `gprecoverseg` 工具用于恢复 Segment 实例。运行 `gprecoverseg` 命令，先将这些 Segment 作为镜像启动，再将它们恢复到首选角色（主 Segment）。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-m`**

可选。关闭以维护模式启动的 Apache Cloudberry Coordinator 实例。

**`-M fast`**

快速关闭。中断并回滚所有进行中的事务。

**`-M immediate`**

立即关闭。取消所有进行中的事务。

此模式会杀死所有 `postgres` 进程，不允许数据库服务器完成事务处理，也不清理任何临时工作文件或正在使用的工作文件。

**`-M smart`**

智能关闭。这是默认关闭模式。`gpstop` 等待活动用户连接断开后再执行关闭。如果超时后仍有用户连接未关闭（或按 CTRL-C 中断），`gpstop` 会列出仍然打开的用户连接，并询问是继续等待连接结束，还是执行快速关闭或立即关闭。

**`-q`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-r`**

关闭完成后重新启动。

**`-t timeout_seconds`**

指定等待 Segment 实例关闭的超时阈值，单位为秒。如果 Segment 实例未在指定秒数内关闭，`gpstop` 会显示消息，指出一个或多个 Segment 仍在关闭过程中，且在这些实例停止前无法重启 Apache Cloudberry。运行 `gpstop` 时，如果有需要回滚的超大事务，此选项很有用。这类大事务的回滚可能耗时超过一分钟，甚至超过默认的 120 秒超时时间。

**`-u`**

此选项重新加载 Coordinator 和 Segment 的 `pg_hba.conf` 文件，以及 `postgresql.conf` 文件中的运行时参数，但不关闭 Apache Cloudberry 阵列。编辑 `postgresql.conf` 或 `pg_hba.conf` 后，可使用此选项使新配置生效。注意，这仅适用于被指定为*运行时*参数的配置参数。

**`-v`**

显示此工具输出的详细状态、进度和错误消息。

**`-y`**

不停止 Standby Coordinator 进程。默认停止 Standby Coordinator。

**`-? | -h | --help`**

显示在线帮助。

**`--version`**

显示此工具的版本。

## 示例 {#examples}

以智能模式停止 Apache Cloudberry 系统：

```shell
gpstop
```

以快速模式停止 Apache Cloudberry 系统：

```shell
gpstop -M fast
```

停止所有 Segment 实例，然后重启系统：

```shell
gpstop -r
```

停止以维护模式启动的 Coordinator 实例：

```shell
gpstop -m
```

更改配置后重新加载 `postgresql.conf` 和 `pg_hba.conf` 文件，但不关闭 Apache Cloudberry 阵列：

```shell
gpstop -u
```

## 另请参阅 {#see-also}

[gpstart](/cloudberry/reference/sys-utilities/gpstart/)
