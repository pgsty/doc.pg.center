---
title: "gpstart"
description: "启动 Apache Cloudberry 系统。"
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpstart.md"
---

## 概要 {#synopsis}

```shell
gpstart [-d <coordinator_data_directory>] [-B <parallel_processes>] [-R]
        [-m] [-y] [-a] [-t <timeout_seconds>] [-l <logfile_directory>] 
        [--skip-heap-checksum-validation]
        [-v | -q]

gpstart -? | -h | --help 

gpstart --version
```

## 说明 {#description}

`gpstart` 工具用于启动 Apache Cloudberry 服务器进程。启动 Apache Cloudberry 系统时，实际上是在同时启动多个 `postgres` 数据库服务器监听进程（Coordinator 和所有 Segment 实例）。`gpstart` 工具负责各实例的启动，并行启动各个实例。

启动过程中，此工具会检查 Apache Cloudberry Coordinator 和 Segment 实例的堆校验和设置是否一致，即所有实例都启用或都禁用。如果各实例的堆校验和设置不同，将返回错误，Apache Cloudberry 不会启动。可指定 `--skip-heap-checksum-validation` 选项禁用此验证。

<!-- For more information about heap checksums, see [Enabling High Availability and Data Consistency Features](/cloudberry/sys-admin/high-availability/). -->

> **注意** 启动 Apache Cloudberry 系统前，必须已使用 `gpinitsystem` 初始化系统。是否启用堆校验和在初始化系统时设置，初始化后无法更改。

如果 Apache Cloudberry 系统配置了 Standby Coordinator，而 `gpstart` 在启动时未检测到它，`gpstart` 会显示警告，并允许取消启动操作。

- 如果未指定 `-a` 选项（禁用交互模式提示），`gpstart` 将显示并记录以下消息：

    ```
    Standby host is unreachable, cannot determine whether the standby is currently acting as the coordinator. Received error: <error>
    Continue only if you are certain that the standby is not acting as the coordinator.
    ```

    它还会显示以下提示，询问是否继续启动：

    ```
    Continue with startup Yy|Nn (default=N):
    ```

- 如果指定了 `-a` 选项，此工具不会启动系统。上述消息仅写入日志，`gpstart` 还会添加以下日志消息：

    ```
    Non interactive mode detected. Not starting the cluster. Start the cluster in interactive mode.
    ```

如果无法访问 Standby Coordinator，可以先启动系统，在系统可用的情况下排查 Standby Coordinator 的问题。

## 选项 {#options}

**`-a`**

不提示用户确认。禁用交互模式。

**`-B parallel_processes`**

并行启动的 Segment 数量。如果未指定，此工具将根据需要启动的 Segment 实例数启动最多 64 个并行进程。

**`-d coordinator_data_directory`**

可选。Coordinator 主机的数据目录。如果未指定，将使用 `$COORDINATOR_DATA_DIRECTORY` 的值。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-m`**

可选。仅启动 Coordinator 实例，适用于维护任务。此模式只允许以工具模式连接 Coordinator。例如：

`PGOPTIONS='-c gp_role=utility' psql`

不检查 Coordinator 与 Segment 实例的堆校验和设置是否一致。

**`-q`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-R`**

以受限模式启动 Apache Cloudberry（仅允许数据库超级用户连接）。

**`--skip-heap-checksum-validation`**

启动时，此工具不验证 Apache Cloudberry Coordinator 与 Segment 实例的堆校验和设置是否一致。默认行为是确保所有实例的堆校验和设置相同，即都启用或都禁用。

> **小心** 未经此验证就启动 Apache Cloudberry 可能导致数据丢失。只有在必须忽略堆校验和验证错误以恢复数据或排查错误时，才应使用此选项启动 Apache Cloudberry。

**`-t timeout_seconds`**

指定等待 Segment 实例启动的超时时间，单位为秒。如果 Segment 实例曾异常关闭（例如由于断电或其 `postgres` 数据库监听进程被杀死），则数据库恢复和验证过程可能使启动耗时更长。如果未指定，默认超时时间为 600 秒。

**`-v`**

显示此工具输出的详细状态、进度和错误消息。

**`-y`**

可选。不启动 Standby Coordinator 主机。默认启动 Standby Coordinator 主机及同步进程。

**`-? | -h | --help`**

显示在线帮助。

**`--version`**

显示此工具的版本。

## 示例 {#examples}

启动 Apache Cloudberry 系统：

```shell
gpstart
```

以受限模式启动 Apache Cloudberry 系统（仅允许超级用户连接）：

```shell
gpstart -R
```

仅启动 Cloudberry Coordinator 实例，并以工具模式连接：

```shell
gpstart -m 
PGOPTIONS='-c gp_role=utility' psql
```

## 另请参阅 {#see-also}

[gpstop](/cloudberry/reference/sys-utilities/gpstop/), [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/)
