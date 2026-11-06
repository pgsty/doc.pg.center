---
title: "系统配置最佳实践"
linkTitle: "系统配置"
description: "为配置 Apache Cloudberry 集群主机的系统管理员提供的要求和最佳实践。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/system-configuration-best-practices.md"
---

Apache Cloudberry 集群通常以 root 身份配置。

## 配置时区 {#configure-the-timezone}

Apache Cloudberry 从内部存储的一组 PostgreSQL 时区中选择要使用的时区。可用的 PostgreSQL 时区取自互联网号码分配机构（IANA）的时区数据库；PostgreSQL 使用的 IANA 数据库发生变化时，Apache Cloudberry 会根据需要更新其可用时区列表。

Cloudberry 会将 PostgreSQL 时区与用户指定的时区进行匹配；如果没有配置时区，则与主机系统时区匹配。例如，选择默认时区时，Cloudberry 会根据主机系统时区文件，使用算法选择一个 PostgreSQL 时区。如果系统时区包含闰秒信息，Apache Cloudberry 无法将系统时区与 PostgreSQL 时区匹配。在这种情况下，Apache Cloudberry 会根据主机系统信息计算与 PostgreSQL 时区的“最佳匹配”。

最佳实践是将 Apache Cloudberry 和主机系统配置为使用已知且受支持的时区。这样会为 Apache Cloudberry 的 Coordinator 和 Segment 实例设置时区，并防止 Apache Cloudberry 在每次集群重启时，使用当前系统时区和 Cloudberry 时区文件（这些文件可能自上次重启以来已根据 IANA 数据库更新）重新计算“最佳匹配”时区。使用 `gpconfig` 工具查看和设置 Apache Cloudberry 时区。例如，以下命令查看 Apache Cloudberry 时区，并将时区设置为 `US/Pacific`。

```shell
gpconfig -s TimeZone
gpconfig -c TimeZone -v 'US/Pacific'
```

更改时区后必须重启 Apache Cloudberry。命令 `gpstop -ra` 会重启 Apache Cloudberry。目录视图 `pg_timezone_names` 提供 Apache Cloudberry 时区信息。

## 配置文件系统 {#configure-the-file-system}

XFS 是 Apache Cloudberry 数据目录使用的文件系统。使用[配置系统](/cloudberry/deployment/prepare-to-deploy/)中介绍的挂载选项。

## 配置端口 {#configure-ports}

更多信息请参见[推荐的操作系统参数设置](/cloudberry/deployment/prepare-to-deploy/#the-sysctlconf-file)。

设置 `ip_local_port_range`，使其不与 Apache Cloudberry 端口范围冲突。例如，在 `/etc/sysctl.conf` 中设置以下范围：

```conf
net.ipv4.ip_local_port_range = 10000  65535
```

可以将 Apache Cloudberry 基础端口号设置为以下值。

```conf
PORT_BASE = 6000
MIRROR_PORT_BASE = 7000
```

更多信息请参见[推荐的操作系统参数设置](/cloudberry/deployment/prepare-to-deploy/#the-sysctlconf-file)。

## 配置 I/O {#configure-io}

在包含数据目录的设备上，将 blockdev 预读大小设为 16384。以下命令设置 `/dev/sdb` 的预读大小。

```shell
/sbin/blockdev --setra 16384 /dev/sdb
```

以下命令返回 `/dev/sdb` 的预读大小。

```shell
# /sbin/blockdev --getra /dev/sdb
16384
```

应为所有数据目录设备设置 deadline I/O 调度器。

```shell
# cat /sys/block/sdb/queue/scheduler
noop anticipatory [deadline] cfq 
```

应在 `/etc/security/limits.conf` 文件中提高操作系统文件和进程的最大数量。

```conf
* soft  nofile 524288
* hard  nofile 524288
* soft  nproc 131072
* hard  nproc 131072
```

## 配置操作系统内存 {#configure-os-memory}

Linux sysctl 的 `vm.overcommit_memory` 和 `vm.overcommit_ratio` 变量会影响操作系统管理内存分配的方式。

`vm.overcommit_memory` 决定操作系统判断可以向进程分配多少内存的方法。该参数应始终设为 2，这是数据库唯一安全的设置。

> **注意** 有关配置内存过量分配的信息，请参见：

- [https://en.wikipedia.org/wiki/Memory_overcommitment](https://www.google.com/url?q=https://en.wikipedia.org/wiki/Memory_overcommitment&sa=D&ust=1499719618717000&usg=AFQjCNErcHO7vErv4pn9fIhCxrR0XRiknA)
- [https://www.kernel.org/doc/Documentation/vm/overcommit-accounting](https://www.google.com/url?q=https://www.kernel.org/doc/Documentation/vm/overcommit-accounting&sa=D&ust=1499719618717000&usg=AFQjCNEmu5tZutAaN1KCSlIwz4hwqihkOQ)

`vm.overcommit_ratio` 是用于应用进程的 RAM 百分比。在 Red Hat Enterprise Linux 中，默认值为 50。

不要在操作系统中启用大页。

## 配置共享内存 {#configure-shared-memory}

Apache Cloudberry 使用共享内存在属于同一 `postgres` 实例的 `postgres` 进程之间通信。应在 `sysctl` 中设置以下共享内存参数，这些参数很少需要修改。

```conf
kernel.shmmax = 810810728448
kernel.shmmni = 4096
kernel.shmall = 197951838
```

## 确定每台主机的 Segment 数量 {#determine-the-number-of-segments-per-host}

确定每台 Segment 主机上运行的 Segment 数量，会极大影响系统整体性能。Segment 会彼此共享主机的 CPU 核、内存和 NIC，也会与主机上运行的其他进程共享这些资源。高估服务器能够承载的 Segment 数量，是性能不佳的常见原因。

选择每台主机运行多少个 Segment 时，必须考虑以下因素：

- 核心数
- 服务器中安装的物理 RAM 数量
- NIC 数量
- 连接到服务器的存储容量
- 主 Segment 和镜像 Segment 的组合
- 将在主机上运行的 ETL 进程
- 主机上运行的非 Cloudberry 进程

## 配置资源队列 Segment 内存 {#configure-resource-queue-segment-memory}

服务器配置参数 `gp_vmem_protect_limit` 指定单个 Segment 的所有活动 postgres 进程在任意时刻可以消耗的内存量。超过此值的查询会失败。使用以下计算估算 `gp_vmem_protect_limit` 的安全值。

1. 计算 `gp_vmem`，即 Apache Cloudberry 可用的主机内存。
    - 如果系统总内存小于 256 GB，使用以下公式：

        ```shell
        gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.7
        ```

    - 如果系统总内存大于或等于 256 GB，使用以下公式：

        ```shell
        gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.17
        ```

    其中，`SWAP` 是主机的交换空间，单位为 GB；`RAM` 是主机安装的 RAM，单位为 GB。

2. 计算 `max_acting_primary_segments`。这是由于集群中另一台主机发生 Segment 或主机故障、镜像 Segment 被激活时，一台主机上可以运行的主 Segment 最大数量。例如，在一个由 4 台主机构成的块中，每台主机有 8 个主 Segment；如果一台 Segment 主机发生故障，则故障主机所在块中的每台剩余主机上会激活 2 或 3 个镜像 Segment。此配置的 `max_acting_primary_segments` 值为 11（8 个主 Segment 加上故障时激活的 3 个镜像）。
3. 用 Apache Cloudberry 总内存除以活动主 Segment 最大数量，计算 `gp_vmem_protect_limit`：

    ```shell
    gp_vmem_protect_limit = gp_vmem / max_acting_primary_segments
    ```

    转换为 MB 后，即可得到系统配置参数 `gp_vmem_protect_limit` 的设置值。

对于生成大量工作文件的场景，应调整 `gp_vmem` 计算公式，将工作文件计入其中。

- 如果系统总内存小于 256 GB：

    ```shell
    gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM - (300KB * total_#_workfiles))) / 1.7
    ```

- 如果系统总内存大于或等于 256 GB：

    ```shell
    gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM - (300KB * total_#_workfiles))) / 1.17
    ```

可以根据 `gp_vmem` 的值计算操作系统参数 `vm.overcommit_ratio`：

```shell
vm.overcommit_ratio = (RAM - 0.026 * gp_vmem) / RAM
```

有关 `vm.overcommit_ratio` 的更多信息，请参见[操作系统内存配置](#configure-os-memory)。

## 配置资源队列语句内存 {#configure-resource-queue-statement-memory}

服务器配置参数 `statement_mem` 是为 Segment 数据库中的单个查询分配的内存量。如果语句需要额外内存，就会溢出到磁盘。使用以下公式计算 `statement_mem` 的值：

`(gp_vmem_protect_limit * .9) / max_expected_concurrent_queries`

例如，如果有 40 个并发查询，且 `gp_vmem_protect_limit` 设为 8GB（8192MB），则 `statement_mem` 的计算方式为：

`(8192MB * .9) / 40 = 184MB`

每个查询在必须溢出到磁盘前，可以使用 184MB 内存。

要安全地提高 `statement_mem`，必须提高 `gp_vmem_protect_limit` 或减少并发查询数。要提高 `gp_vmem_protect_limit`，必须增加物理 RAM 和/或交换空间，或者减少每台主机的 Segment 数量。

注意，向集群添加 Segment 主机并不能解决内存不足错误，除非利用新增主机减少每台主机的 Segment 数量。

当没有足够内存容纳所有映射器输出时（通常是缓冲区空间占用达到 80% 时），会创建溢出文件。

## 配置资源队列溢出文件 {#configure-resource-queue-spill-files}

如果为查询分配的内存不足以在内存中运行，Apache Cloudberry 会在磁盘上创建*溢出文件*（也称为*工作文件*）。默认情况下，单个查询最多可以创建 100,000 个溢出文件，这足以满足大多数查询。

可以使用配置参数 `gp_workfile_limit_files_per_query` 控制每个查询、每个 Segment 创建的最大溢出文件数。将该参数设为 0，允许查询创建无限数量的溢出文件。限制允许的溢出文件数量，可以防止失控查询干扰系统。

如果分配的内存不足，或查询数据存在数据倾斜，查询可能生成大量溢出文件。如果查询创建的溢出文件超过指定数量，Apache Cloudberry 会返回以下错误：

`ERROR: number of workfiles per query limit exceeded`

在提高 `gp_workfile_limit_files_per_query` 之前，应尝试通过修改查询、修改数据分布或修改内存配置来减少溢出文件数量。

`gp_toolkit` 模式包含多个视图，可以查看当前使用溢出文件的所有查询的信息。这些信息可用于排查问题和调整查询：

- `gp_workfile_entries` 视图为当前每个 Segment 上使用工作文件磁盘空间的每个算子提供一行记录。有关算子的信息，请参见[如何阅读 EXPLAIN 计划](/cloudberry/performance/optimize-queries/analyze-query-performance/#read-explain-output)。
- `gp_workfile_usage_per_query` 视图为当前每个 Segment 上使用工作文件磁盘空间的每个查询提供一行记录。
- `gp_workfile_usage_per_segment` 视图为每个 Segment 提供一行记录。每行显示当前该 Segment 上工作文件使用的磁盘空间总量。

配置参数 `gp_workfile_compression` 指定是否压缩溢出文件。默认值为 `off`。启用压缩可以改善使用溢出文件时的性能。
