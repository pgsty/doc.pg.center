---
title: "系统扩容概述"
description: "可以在停机时间很短的情况下扩容 Apache Cloudberry，添加 Segment 实例和 Segment 主机。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/system-expansion-overview.md"
---

通常，向 Cloudberry 集群添加节点可以使性能和存储容量线性扩展。

随着数据不断收集以及现有数据的保留期延长，数据仓库通常会持续增长。有时，为了将彼此分离的数据仓库整合到一个数据库中，需要增加数据库容量。为了容纳新增的分析项目，数据仓库也可能需要额外的计算能力（CPU）。系统初始规格设计时，为增长预留容量是明智的做法，但即使预期增长速度很高，通常也不宜在真正需要容量很久以前就投入资源。因此，应预期定期执行数据库扩容项目。

扩容数据库时，应预期具备以下特性：

- 可扩展的容量和性能。向 Apache Cloudberry 添加资源后，系统的容量和性能会达到如同最初就配置了这些资源时的水平。
- 扩容期间服务不中断（初始化阶段完成后）。定期和临时工作负载都不会中断。
- 事务一致性。
- 容错能力。扩容期间，标准容错机制（例如 Segment 镜像）仍保持活动、一致且有效。
- 复制和灾难恢复。现有的复制机制会在扩容期间继续运行。故障或灾难事件发生时所需的恢复机制仍然有效。
- 过程透明。扩容过程使用标准 Apache Cloudberry 机制，因此管理员可以诊断和排查问题。
- 过程可配置。扩容可能是一个长时间运行的过程，但可以安排在现有运维计划中。扩容模式中的表允许管理员确定表重分布的顺序，也可以暂停和恢复扩容活动。

扩容项目中，规划和物理实施所占的工作量比实际扩展数据库更大。项目需要多学科团队来规划和执行。对于本地部署，需要为新服务器取得并准备空间。服务器必须完成规格确定、采购、安装、布线、配置和测试。云部署也应制定类似计划。[规划新的硬件平台](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/#plan-new-hardware-platforms)介绍了部署新硬件时的一般注意事项。

准备好新的硬件平台并配置好网络后，配置操作系统，并使用 Cloudberry 工具运行性能测试。Apache Cloudberry 软件发行版包含一些实用工具，可在扩容软件阶段开始前测试新服务器并完成预热。准备新主机的步骤请参见[准备并添加主机](/cloudberry/sys-admin/expand-cluster/prepare-and-add-hosts/)。

新服务器安装并测试完成后，Apache Cloudberry 扩容过程的软件阶段开始。软件阶段的设计目标是尽量减少干扰、保持事务一致性、可靠且灵活。

- 扩容软件阶段的第一步是准备 Apache Cloudberry 系统：添加新的 Segment 主机并初始化新的 Segment 实例。可以安排在低活动时段执行此阶段，以免干扰正在进行的业务操作。初始化过程中会执行以下任务：

    - 安装 Apache Cloudberry 软件。
    - 在新 Segment 主机上的新 Segment 实例中创建数据库和数据库对象。
    - 在 postgres 数据库中创建 *gpexpand* 模式。可以使用该模式中的表和视图监控和控制扩容过程。
    系统更新后，新 Segment 主机上的新 Segment 实例即可使用。

    - 新 Segment 会立即可用，并参与新查询和数据加载。但是，现有数据会发生倾斜，集中在原有 Segment 上，必须在新的主 Segment 总数上重新分布。
    - 由于部分表数据发生倾斜，某些查询可能效率较低，因为可能需要更多数据移动操作。
- 软件阶段的最后一步是重新分布表数据。以 *gpexpand* 模式中的扩容控制表为依据重新分布表。对于每张表：

    - [`gpexand`](/cloudberry/reference/sys-utilities/gpexpand/) 工具根据分布策略，在所有服务器（包括新旧服务器）之间重新分布表数据。
    - 在扩容控制表中更新表的状态。
    - 数据重新分布后，当数据不再倾斜时，查询优化器会创建更高效的执行计划。
    所有表完成重分布后，扩容完成。

> [!NOTE]
> `gprestore` 工具无法恢复使用 `gpbackup` 工具在扩容前创建的备份，因此系统扩容完成后应立即备份数据库。

重新分布表数据是一个长时间运行的过程，会产生大量网络和磁盘活动。重新分布某些超大型数据库可能需要数天。为尽量减少活动增加对业务运行的影响，系统管理员可以临时暂停和恢复扩容活动，也可以按预定计划执行。可以设置数据集的优先级，让关键应用先受益于扩容。

在典型操作中，完整扩容过程会使用不同选项运行 `gpexpand` 工具四次。

1. [创建扩容输入文件](/cloudberry/sys-admin/expand-cluster/initialize-new-segments/)：

    ```shell
    gpexpand -f <hosts_file>
    ```

2. [初始化 Segment 并创建扩容模式](/cloudberry/sys-admin/expand-cluster/initialize-new-segments/)：

    ```shell
    gpexpand -i <input_file>
    ```

    `gpexpand` 会创建数据目录，将所有现有数据库中的用户表复制到新 Segment 上，并在扩容模式中记录每张表的元数据，以便跟踪状态。此过程完成后，扩容操作即提交，无法撤销。

3. [重新分布表数据](/cloudberry/sys-admin/expand-cluster/initialize-new-segments/)：

    ```shell
    gpexpand -d <duration>
    ```

    初始化期间，`gpexpand` 会添加并初始化新的 Segment 实例。要完成系统扩容，必须运行 `gpexpand`，在新增的 Segment 实例之间重新分布数据表。根据系统的大小和规模，可以在低使用时段通过一次会话完成重分布，也可以在较长时间内分批执行。重分布期间，每张表或分区都无法进行读写操作。随着每张表在新 Segment 之间完成重新分布，数据库性能应逐步改善，最终超过扩容前的性能水平。

    对于需要多次重分布会话的大型系统，可能需要多次运行 `gpexpand` 才能完成扩容。显式设置表的重分布排序可使 `gpexpand` 受益；请参见[规划表重分布](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)。

    用户可以在初始化期间访问 Apache Cloudberry，但对于严重依赖表哈希分布的系统，用户可能会遇到性能下降。ETL 作业、用户查询和报表等正常操作可以继续运行，但响应时间可能更长。

4. 删除扩容模式：

    ```shell
    gpexpand -c
    ```
