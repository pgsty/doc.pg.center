---
title: "gpmovemirrors"
description: "将镜像 Segment 实例移动到新位置。"
weight: 200
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpmovemirrors.md"
---

## 概要 {#synopsis}

```shell
gpmovemirrors -i <move_config_file> [-d <coordinator_data_directory>] 
          [-l <logfile_directory>] [-b <segment_batch_size>]
          [-B <batch_size>] [-v] [--hba-hostnames <boolean>] 

gpmovemirrors -? 

gpmovemirrors --version
```

## 说明 {#description}

`gpmovemirrors` 工具将镜像 Segment 实例移动到新位置。可以通过移动镜像来优化分布或数据存储。

默认情况下，此工具会提示输入镜像 Segment 数据目录要移至的文件系统位置。

必须确保运行 `gpmovemirrors` 的用户（`gpadmin` 用户）具有写入指定数据目录位置的权限。运行 `gpmovemirrors` 前，可以在 Segment 主机上创建这些目录，并将其 `chown` 给适当的用户。

## 选项 {#options}

**`-b segment_batch_size`**

每台主机并行操作的最大 Segment 数量。有效值为 `1` 到 `128`。如果未指定，此工具会在每台主机上并行恢复最多 64 个 Segment。

**`-B batch_size`**

并行处理的主机数。如果未指定，此工具会并行处理最多 16 台主机。有效值为 `1` 到 `64`。

**`-d coordinator_data_directory`**

Coordinator 数据目录。如果未指定，将使用 `$COORDINATOR_DATA_DIRECTORY` 的值。

**`--hba-hostnames boolean`**

可选。控制此工具更新 `pg_hba.conf` 文件中可连接 Apache Cloudberry 的地址时使用 IP 地址还是主机名。设为 0（默认值）时，使用 IP 地址更新文件；设为 1 时，使用主机名更新文件。为保持一致，应使用初始化 Apache Cloudberry 系统时为 `HBA_HOSTNAMES` 指定的相同值。
<!-- For information about how Apache Cloudberry resolves host names in the `pg_hba.conf` file, see [Configuring Client Authentication](/cloudberry/security/client-auth/). -->

**`-i move_config_file`**

配置文件，包含要移动哪些镜像 Segment 以及要将它们移至何处的信息。

系统中的每个主 Segment 都必须对应列出一个镜像 Segment。配置文件中每行采用以下格式（与 `gp_segment_configuration` 目录表中的属性一致）：

```shell
<old_address>|<port>|<data_dir> <new_address>|<port>|<data_dir>
```

其中，`<old_address>` 和 `<new_address>` 是 Segment 主机的主机名或 IP 地址，`<port>` 是通信端口，`<data_dir>` 是 Segment 实例数据目录。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-v (verbose)`**

将日志输出级别设为 verbose。

**`--version (show utility version)`**

显示此工具的版本。

**`-? (help)`**

显示在线帮助。

## 示例 {#examples}

将现有 Apache Cloudberry 系统中的镜像移至另一组主机：

```shell
$ gpmovemirrors -i move_config_file
```

其中，`move_config_file` 内容大致如下：

```shell
sdw2|50000|/data2/mirror/gpseg0 sdw3|50000|/data/mirror/gpseg0
sdw2|50001|/data2/mirror/gpseg1 sdw4|50001|/data/mirror/gpseg1
sdw3|50002|/data2/mirror/gpseg2 sdw1|50002|/data/mirror/gpseg2
```
