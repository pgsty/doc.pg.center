---
title: "规划 Cloudberry 系统扩容"
description: "周密规划有助于确保 Cloudberry 扩容项目成功。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/plan-system-expansion.md"
---

本节内容有助于确保你已准备好执行系统扩容。

- [系统扩容清单](#system-expansion-checklist)可用于准备和执行系统扩容过程。
- [规划新的硬件平台](#plan-new-hardware-platforms)介绍采购和设置新硬件的规划工作。
- [规划新 Segment 初始化](#plan-new-segment-initialization)介绍使用 `gpexpand` 初始化新 Segment 主机时的规划工作。
- [规划表重分布](#plan-table-redistribution)介绍新 Segment 主机初始化后如何规划数据重分布。

> [!NOTE]
> 扩展 Apache Cloudberry 系统时，必须先停用 Cloudberry 互连代理，然后才能向系统添加新主机和 Segment 实例；重新启用互连代理前，必须使用新添加的 Segment 实例更新 `gp_interconnect_proxy_addresses` 参数。例如，以下命令通过将互连设置为默认值（`UDPIFC`）并重新加载 `postgresql.conf` 文件来停用 Cloudberry 互连代理，从而更新 Cloudberry 系统配置。

```shell
gpconfig -r gp_interconnect_type
gpstop -u
```

有关 Cloudberry 互连代理的信息，请参见[为 Cloudberry 互连配置代理](/cloudberry/sys-admin/configure-proxy/)。

## 系统扩容清单 {#system-expansion-checklist}

此清单概括了扩容 Apache Cloudberry 系统的主要任务，以及每个阶段的系统状态。

### 在线扩容前任务 {#online-pre-expansion-tasks}

系统已启动并可用。

- [ ] 规划新硬件平台的订购、构建和联网，或配置云资源。
- [ ] 制定数据库扩容计划。确定每台主机的 Segment 数量，安排用于测试性能和创建扩容模式的停机时段，并安排表重分布的时间间隔。
- [ ] 执行完整的模式转储。
- [ ] 在新主机上安装 Apache Cloudberry 二进制文件。
- [ ] 将 SSH 密钥复制到新主机（`gpssh-exkeys`）。
- [ ] 验证新硬件或云资源的磁盘 I/O 和内存带宽（`gpcheckperf`）。
- [ ] 验证 Coordinator 数据目录的 `log` 目录中没有超大文件。

### 离线扩容前任务 {#offline-pre-expansion-tasks}

在此过程中，系统对所有用户活动不可用。

- [ ] 验证不存在目录问题（`gpcheckcat`）。
- [ ] 验证现有硬件和新硬件或云资源组合后的磁盘 I/O 和内存带宽（`gpcheckperf`）。

### 在线 Segment 实例初始化 {#online-segment-instance-initialization}

系统已启动并可用。

- [ ] 准备扩容输入文件（`gpexpand`）。
- [ ] 将新 Segment 初始化到系统中并创建扩容模式（`gpexpand -i italic_input_file_`）。

### 在线扩容和表重分布 {#online-expansion-and-table-redistribution}

系统已启动并可用。

- [ ] 开始表重分布前，停止所有自动快照进程或其他占用磁盘空间的进程。
- [ ] 在扩容后的系统中重新分布表（`gpexpand`）。
- [ ] 删除扩容模式（`gpexpand -c`）。
- [ ] **重要：**运行 `analyze` 更新分布统计信息。扩容期间使用 `gpexpand -a`，扩容完成后使用 `analyze`。

### 备份数据库 {#back-up-databases}

系统已启动并可用。

- [ ] 使用 `gpbackup` 工具备份数据库。开始系统扩容前创建的备份无法恢复到新扩容的系统，因为 `gprestore` 只能将备份恢复到 Segment 数量相同的 Apache Cloudberry 系统。

## 规划新的硬件平台 {#plan-new-hardware-platforms}

以审慎、全面的方式部署兼容硬件，可以大幅降低扩容过程的风险。

新 Segment 主机的硬件资源和配置应与现有主机匹配。

规划和设置新硬件平台的步骤因部署方式而异。其中需要考虑：

- 为新硬件准备物理空间，包括散热、电源供应和其他物理因素。
- 确定连接新旧硬件所需的物理网络和布线。
- 记录现有 IP 地址空间，并为扩容后的系统制定网络计划。
- 获取现有硬件的系统配置（用户、配置文件、NIC 等），作为订购新硬件时的详细清单。
- 制定自定义构建计划，以便在特定站点和环境中按所需配置部署硬件。

选择新硬件并将其加入网络环境后，请确保执行[准备并添加主机](/cloudberry/sys-admin/expand-cluster/prepare-and-add-hosts/)中所述的任务。

## 规划新 Segment 初始化 {#plan-new-segment-initialization}

Apache Cloudberry 可以在系统已启动且可用时扩容。运行 `gpexpand`，将新的 Segment 实例初始化到系统中并创建扩容模式。

所需时间取决于 Cloudberry 系统中的模式对象数量以及其他与硬件性能有关的因素。在大多数环境中，初始化新 Segment 需要离线运行的时间少于三十分钟。

`gpexpand` 执行 Segment 初始化期间，不能运行以下工具：

- `gpbackup`
- `gpcheckcat`
- `gpconfig`
- `gppkg`
- `gprestore`

> [!NOTE]
> 开始初始化新 Segment 后，就不能再使用为扩容前系统创建的备份文件恢复系统。初始化成功完成后，扩容即提交，无法回滚。

### 规划镜像 Segment {#plan-mirror-segments}

如果现有系统具有镜像 Segment，则必须为新 Segment 配置镜像。如果现有 Segment 没有配置镜像，则不能使用 `gpexpand` 工具为新主机添加镜像。有关系统初始化期间可用的 Segment 镜像配置，请参见[关于 Segment 镜像配置](/cloudberry/sys-admin/high-availability/segment-mirroring-overview/#about-segment-mirroring-configurations)。

对于具有镜像 Segment 的 Apache Cloudberry 系统，请确保添加足够的新主机来容纳新的镜像 Segment。所需新主机数量取决于镜像策略：

- **组镜像**：至少添加两台新主机，使第一台主机的镜像可以放在第二台主机上，第二台主机的镜像可以放在第一台主机上。如果在系统初始化期间启用 Segment 镜像，这是默认的镜像类型。
- **分散镜像**：至少向系统添加一台多于每台主机 Segment 数量的新主机。独立主机数量必须大于每台主机的 Segment 实例数量，才能确保均匀分散。可以在系统初始化期间，或为现有系统启用 Segment 镜像时指定此镜像类型。
- **块镜像**：添加一个或多个主机系统块。例如，添加由四台或八台主机构成的一个块。块镜像是一种自定义镜像配置。有关块镜像的信息，请参见[Segment 镜像配置](/cloudberry/tutorials/best-practices/high-availability-best-practices/#configure-segment-mirroring)。

### 增加每台主机的 Segment 数量 {#increase-segments-per-host}

默认情况下，新主机初始化的主 Segment 数量与现有主机相同。可以增加每台主机的 Segment 数量，或向现有主机添加新的 Segment。

例如，如果现有主机当前每台有两个 Segment，可以使用 `gpexpand` 在现有主机上初始化两个额外 Segment，使每台主机总共有四个 Segment，并在新主机上初始化四个新 Segment。

创建扩容输入文件的交互过程会提示此选项；也可以在输入配置文件中手动指定新 Segment 目录。更多信息请参见[创建系统扩容输入文件](/cloudberry/sys-admin/expand-cluster/initialize-new-segments/)。

### 关于扩容模式 {#about-the-expansion-schema}

初始化时，`gpexpand` 工具会在 postgres 数据库中创建名为 *gpexpand* 的扩容模式。

扩容模式存储系统中每张表的元数据，以便在整个扩容过程中跟踪其状态。扩容模式由两个表和一个视图组成，用于跟踪扩容操作进度：

- *gpexpand.status*
- *gpexpand.status_detail*
- *gpexpand.expansion_progress*

通过修改 *gpexpand.status_detail* 控制扩容过程。例如，从该表中删除一条记录会阻止系统在新 Segment 之间扩展相应的表。更新记录的 `rank` 值可以控制表进行重分布时的处理顺序。更多信息请参见[为重分布排序表](/cloudberry/sys-admin/expand-cluster/redistribute-tables/)。

## 规划表重分布 {#plan-table-redistribution}

表重分布在系统在线时执行。对于许多 Cloudberry 系统，表重分布可以在低使用时段安排的一次 `gpexpand` 会话中完成。较大的系统可能需要多次会话，并需要设置表重分布顺序以尽量减少性能影响。如果可能，应在一次会话中完成表重分布。

> **重要** 要执行表重分布，Segment 主机必须有足够的磁盘空间，能够临时保存最大表的副本。重分布期间，所有表都无法进行读写操作。

表重分布对性能的影响取决于表的大小、存储类型和分区设计。对于任意给定的表，使用 `gpexpand` 重新分布所需的时间与执行 `CREATE TABLE AS SELECT` 操作所需的时间相当。重新分布 TB 级事实表时，扩容工具可能会使用大量可用系统资源，这可能影响查询性能或其他数据库工作负载。

### 表重分布方法 {#table-redistribution-method}

Apache Cloudberry 使用*重建*表分布方法在扩容期间重新分布数据。Cloudberry 会：

1. 创建新表。
2. 将旧表的全部数据复制到新表。
3. 替换旧表。

重建方法类似于使用 `CREATE TABLE AS SELECT` 命令创建新表。重新分布数据期间，Apache Cloudberry 会获取表上的 `ACCESS EXCLUSIVE` 锁。

### 管理大规模 Cloudberry 系统中的重分布 {#manage-redistribution-in-large-scale-cloudberry-systems}

规划重分布阶段时，请考虑对每张表获取 `ACCESS EXCLUSIVE` 锁的影响。表上的用户活动可能延迟其重分布，但表在重分布期间也无法供用户活动使用。

可以通过调整表的排序来管理表的重分布顺序。请参见[为重分布排序表](/cloudberry/sys-admin/expand-cluster/redistribute-tables/)。调整重分布顺序有助于应对磁盘空间有限的情况，并尽快恢复高优先级查询的最佳性能。

#### 空闲磁盘空间充足的系统 {#systems-with-abundant-free-disk-space}

对于空闲磁盘空间充足的系统（需要足够空间保存最大表的副本），可以首先重新分布查询大量使用的重要表，尽快恢复最佳查询性能。为这些表设置较高的排序值，并在系统使用率低的时段安排重分布操作。一次运行一个重分布进程，直到大型表或关键表完成重分布。

#### 空闲磁盘空间有限的系统 {#systems-with-limited-free-disk-space}

如果现有主机的磁盘空间有限，可以先重新分布较小的表（例如维度表），为保存最大表的副本腾出空间。随着每张表在扩容后的系统中完成重新分布，原有 Segment 上的可用磁盘空间会增加。当所有 Segment 都有足够的空闲空间来保存最大表的副本时，就可以重新分布大型表或关键表。大型表重分布需要排他锁；请在非高峰时段安排此过程。

还应考虑以下事项：

- 在非高峰时段运行多个并行重分布进程，以最大限度地利用可用系统资源。
- 运行多个进程时，应遵守 Cloudberry 系统的连接限制。有关限制并发连接的信息，请参见[限制并发连接](/cloudberry/security/client-auth/)。

### 重新分布追加优化表和压缩表 {#redistribute-append-optimized-and-compressed-tables}

`gpexpand` 重新分布追加优化表和压缩的追加优化表时，其速率与堆表不同。压缩和解压缩数据所需的 CPU 容量往往会增加对系统性能的影响。对于数据相似且大小相近的表，整体性能可能存在以下差异：

- 未压缩的追加优化表扩容速度比堆表快 10%。
- 定义为使用数据压缩的追加优化表，其扩容速度明显慢于未压缩的追加优化表，最慢可能达到 80%。
- 使用 ZFS/LZJB 等数据压缩的系统需要更长时间完成重分布。

> [!NOTE]
> 如果系统主机使用数据压缩，请在新主机上使用相同的压缩设置，以避免磁盘空间不足。

### 重新分布分区表 {#redistribute-partitioned-tables}

由于扩容工具可以处理大表中的每个独立分区，高效的分区设计可以降低表重分布的性能影响。只有分区表的子表会设置为随机分布策略。重分布的读写锁一次只作用于一个子表。

### 重新分布带索引的表 {#redistribute-indexed-tables}

由于 `gpexpand` 工具必须在重分布后为每个带索引的表重新创建索引，索引级别较高会对性能产生很大影响。索引密集型系统的表重分布速度会明显降低。
