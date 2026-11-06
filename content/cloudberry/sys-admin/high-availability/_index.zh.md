---
title: "高可用概述"
linkTitle: "高可用"
description: "通过提供容错硬件平台、启用 Apache Cloudberry 高可用特性，以及定期监控和维护以确保各系统组件健康运行，可以使 Apache Cloudberry 系统具备高可用性。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/high-availability-overview.md"
---

无论是正常磨损还是意外情况，硬件组件最终都会发生故障。断电可能导致组件暂时不可用。为可能发生故障的组件提供冗余备用组件，可以使系统具备高可用性，在故障发生时继续提供不中断的服务。有时，冗余成本超过了用户为避免服务中断所愿意付出的代价。此时，目标是确保能够在预期时间内恢复全部服务。

Apache Cloudberry 通过以下方式实现容错和数据可用性：

- [硬件级 RAID 存储保护](#hardware-level-raid)
- [数据存储校验和](#data-storage-checksums)
- [Cloudberry Segment 镜像](#segment-mirroring)
- [Coordinator 镜像](#coordinator-mirroring)
- [双集群](#dual-clusters)
- [数据库备份与恢复](#backup-and-restore)

## 硬件级 RAID {#hardware-level-raid}

Apache Cloudberry 部署的最佳实践是使用硬件级 RAID，在单块磁盘故障时提供高性能的冗余保护，无需启用数据库层的容错机制。这是在更底层的磁盘层提供冗余。

## 数据存储校验和 {#data-storage-checksums}

Apache Cloudberry 使用校验和验证从磁盘加载到内存的数据在文件系统中没有损坏。

Apache Cloudberry 为用户数据提供两种存储方式：堆存储和追加优化存储。两种存储模型都使用校验和验证从文件系统读取的数据，并在默认设置下以类似的方式处理校验和验证错误。

Apache Cloudberry 的 Coordinator 和 Segment 数据库进程会更新各自管理的内存中的数据页。内存页更新并刷写到磁盘时，系统会计算校验和并将其与页面一起保存。之后从磁盘读取页面时，会验证校验和；只有验证成功，页面才允许进入受管理的内存。校验和验证失败表明文件系统中的数据已损坏，Apache Cloudberry 会生成错误并取消事务。

默认校验和设置能最大限度地防止未被发现的磁盘损坏传播到数据库和镜像 Segment。

使用 `gpinitsystem` 管理工具初始化 Apache Cloudberry 集群时，默认启用堆存储校验和。虽然强烈不建议这样做，但仍可在 `gpinitsystem` 集群配置文件中将 `HEAP_CHECKSUM` 参数设为 off，以初始化不支持堆存储校验和的集群。参见 [`gpinitsystem`](/cloudberry/reference/sys-utilities/gpinitsystem/)。

初始化完成后，若不重新初始化系统并重新加载数据库，就无法更改集群的堆存储校验和支持设置。

可以查看只读服务器配置参数 `data_checksums`，确认集群是否启用了堆存储校验和：

```shell
$ gpconfig -s data_checksums
```

Apache Cloudberry 集群启动时，`gpstart` 工具会检查 Coordinator 和所有 Segment 上的堆存储校验和是否一致地启用或禁用。如果存在差异，集群将无法启动。参见 [`gpstart`](/cloudberry/reference/sys-utilities/gpstart/)。

如果必须忽略堆存储校验和验证错误才能恢复数据，可将系统配置参数 `ignore_checksum_failure` 设为 on。这样，在堆存储校验和验证失败时，Apache Cloudberry 会发出警告，但仍允许将该页加载到受管理的内存中。如果该页随后更新并保存到磁盘，损坏的数据可能被复制到镜像 Segment。由于这可能导致数据丢失，只有为了恢复数据时才应将 `ignore_checksum_failure` 设为 on。

对于追加优化存储，校验和支持是使用 `CREATE TABLE` 命令创建 AO 表时可设置的多个存储选项之一。默认存储选项由服务器配置参数 `gp_default_storage_options` 指定。`checksum` 存储选项默认启用，强烈不建议禁用。

如果决定禁用某个 AO 表的校验和，可以采用以下任一方式：

- 建表前修改 `gp_default_storage_options` 配置参数，加入 `checksum=false`；或者
- 在 `CREATE TABLE` 语句的 `WITH storage_options` 子句中加入 `checksum=false` 选项。

请注意，`CREATE TABLE` 语句允许为各个分区文件设置包括校验和在内的存储选项。

语法和示例见 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/) 命令参考及 `gp_default_storage_options` 配置参数参考。

## Segment 镜像 {#segment-mirroring}

Apache Cloudberry 将数据存储在多个 Segment 实例中，每个实例都是一个 Apache Cloudberry PostgreSQL 实例。每张表的数据按照建表时在 DDL 中定义的分布策略分散到各个 Segment。启用 Segment 镜像后，每个 Segment 实例都有一对*主实例*和*镜像实例*。镜像 Segment 通过基于预写式日志（WAL）的流复制，与主 Segment 保持同步。参见 [Segment 镜像概述](/cloudberry/sys-admin/high-availability/segment-mirroring-overview/)。

各 Segment 的镜像实例通常使用 `gpinitsystem` 或 `gpexpand` 工具初始化。最佳实践是将镜像与主实例部署在不同主机上，以防范单机故障。将镜像分配到主机有多种策略。选择主实例与镜像的布局时，应考虑故障场景，确保单机故障时尽量减少处理负载倾斜。

## Coordinator 镜像 {#coordinator-mirroring}

高可用集群包含两个 Coordinator 实例：一个*主实例*和一个*备用实例*。与 Segment 相同，Coordinator 和 Standby Coordinator 应部署在不同主机上，使集群能够容忍单台主机故障。客户端连接主 Coordinator，查询也只能在主 Coordinator 上运行。Standby Coordinator 通过基于预写式日志（WAL）的流复制，与主 Coordinator 保持同步。参见 [Coordinator 镜像概述](/cloudberry/sys-admin/high-availability/coordinator-mirroring-overview/)。

如果 Coordinator 发生故障，管理员运行 `gpactivatestandby` 工具，使 Standby Coordinator 接管并成为新的主 Coordinator。可以为 Coordinator 和 Standby Coordinator 配置虚拟 IP 地址，使当前 Coordinator 变化时，客户端程序无需改用其他网络地址。如果 Coordinator 主机故障，可将虚拟 IP 地址切换到实际承担 Coordinator 角色的主机。

## 双集群 {#dual-clusters}

维护两个存储相同数据的 Apache Cloudberry 集群，可以再增加一层冗余。

使双集群中的数据保持同步有两种方法：“双 ETL”和“备份/恢复”。

双 ETL 提供一个完整的备用集群，其数据与主集群相同。ETL（提取、转换和加载）指将传入数据清洗、转换、验证并加载到数据仓库的过程。采用双 ETL 时，该过程在两个集群上分别执行一次，并行运行，每次都进行验证。两个集群还都可以执行数据查询，使查询吞吐量翻倍。应用程序可以同时利用两个集群，并确保两个集群上的 ETL 均成功且通过验证。

采用备份/恢复方式维护双集群时，先备份主集群，再将备份恢复到第二个集群。与双 ETL 策略相比，这种方法需要更长时间才能同步第二个集群的数据，但需要开发的应用逻辑较少。使用备份填充第二个集群，适合每天执行数据修改和 ETL，或执行频率更低的场景。

## 备份与恢复 {#backup-and-restore}

除非可以很容易地从源数据重新生成数据库，否则建议定期备份数据库。备份用于防范操作、软件和硬件错误。

使用 [`gpbackup`](/cloudberry/reference/sys-utilities/gpbackup/) 工具备份 Apache Cloudberry。`gpbackup` 在各个 Segment 上并行备份，因此随着集群增加硬件，备份性能也会提升。

设计备份策略时，首要考虑之一是备份数据的存储位置。各 Segment 管理的数据可以备份到该 Segment 的本地存储，但不应长期保存在那里：备份会减少 Segment 的可用磁盘空间，更重要的是，硬件故障可能同时破坏 Segment 的在线数据和备份。完成备份后，应将备份文件从主集群移至独立、安全的存储。也可以直接备份到独立存储。

结合 Apache Cloudberry 存储插件使用 `gpbackup` 和 `gprestore` 工具，可以将备份发送到远程位置或存储设备，也可以从这些位置取回备份。Apache Cloudberry 存储插件支持连接 Amazon Simple Storage Service（Amazon S3）位置和 Dell EMC Data Domain 存储设备等目标。

使用备份/恢复存储插件 API，可以创建自定义插件，让 `gpbackup` 和 `gprestore` 工具将自定义备份存储系统与 Apache Cloudberry 集成。

有关 `gpbackup` 和 `gprestore` 的用法，参见 [Apache Cloudberry 备份与恢复文档](/cloudberry/sys-admin/backup-and-restore/)。
