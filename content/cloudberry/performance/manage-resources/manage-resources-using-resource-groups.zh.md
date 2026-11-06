---
title: "使用资源组管理资源"
linkTitle: "资源组"
description: "可以使用资源组管理和保障 Apache Cloudberry 中 CPU、内存、并发事务限制和磁盘 I/O 的资源分配。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/manage-resources-using-resource-groups.md"
---

定义资源组后，可将其分配给一个或多个 Apache Cloudberry 角色，或者 PL/Container 等外部组件，以控制其资源使用。

将资源组分配给角色后，该组定义的资源限制对所有归属于它的角色共同生效。例如，资源组的内存限制表示：分配到该组的所有角色中，Apache Cloudberry 用户提交的全部运行中事务的最大内存用量。

Apache Cloudberry 使用基于 Linux 的控制组管理 CPU 资源，使用失控检测器（Runaway Detector）统计、跟踪和管理内存。

## 角色资源组与组件资源组 {#role-and-component-resource-groups}

Apache Cloudberry 支持两类资源组：用于管理角色资源的组，以及用于管理 PL/Container 等外部组件资源的组。

资源组最常见的用途，是管理不同角色在 Apache Cloudberry 集群中可以并发运行的活动查询数。还可以管理 Apache Cloudberry 为每个查询分配的 CPU、内存资源和磁盘 I/O。

用户执行查询时，Apache Cloudberry 会根据资源组定义的一组限制评估该查询。如果尚未达到组的资源限制，而且查询不会使组超出并发事务限制，Apache Cloudberry 就会立即运行查询。否则，查询将排队等待。例如，如果资源组已达到最大并发事务数，后续查询就必须排队，等待其他查询完成后才能运行。如果将资源组的并发和内存限制调高到足够大的值，Apache Cloudberry 也可能启动等待中的查询。

在角色资源组内部，事务按先进先出的顺序处理。Apache Cloudberry 定期评估系统的活动工作负载，并根据需要重新分配资源、启动作业或将作业排队。

还可以使用资源组管理 PL/Container 等外部组件的 CPU 和内存资源。外部组件资源组使用 Linux cgroups 管理组件的 CPU 资源总量。

## 资源组属性与限制 {#resource-group-attributes-and-limits}

创建资源组时，需要提供一组限制，确定该组可用的 CPU 和内存资源量。下表列出资源组可用的限制：

| 限制类型 | 说明 | 取值范围 | 默认值 |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|--------------------------------------------------------------------------|
| `CONCURRENCY` | 资源组允许的最大并发事务数，包括活动和空闲事务。 | [0, max_connections] | 20 |
| `CPU_MAX_PERCENT` | 该组可使用的 CPU 资源百分比上限。 | [1, 100] | -1（未设置） |
| `CPU_WEIGHT` | 资源组的调度优先级。 | [1, 500] | 100 |
| `CPUSET` | 为资源组预留的具体 CPU 逻辑核（启用超线程时为逻辑线程）。 | 取决于系统 CPU 核配置 | -1 |
| `IO_LIMIT` | 最大磁盘读写 I/O 吞吐量和每秒最大读写 I/O 操作数的限制。按表空间设置。 | [2, 4294967295 or max] | -1 |
| `MEMORY_QUOTA` | 为资源组指定的内存限制值。 | 整数（MB） | -1（未设置，使用 `statement_mem` 作为单个查询的内存限制） |
| `MIN_COST` | 纳入资源组的查询计划的最低代价。 | 整数 | 0 |

> [!NOTE]
> 资源限制不适用于 `SET`、`RESET` 和 `SHOW` 命令。

### 事务并发限制 {#transaction-concurrency-limit}

`CONCURRENCY` 限制控制资源组允许的最大并发事务数。

每个资源组在逻辑上划分为固定数量的槽位，其数量等于 `CONCURRENCY` 限制。Apache Cloudberry 为这些槽位分配相等、固定比例的内存资源。

角色资源组的 `CONCURRENCY` 默认值为 20。值为 0 表示不允许该资源组运行任何查询。

资源组达到 `CONCURRENCY` 限制后，Apache Cloudberry 会将后续提交的事务排队。运行中的事务完成后，如果内存资源充足，就会取出最早排队的事务并运行。注意，如果事务处于 `idle in transaction` 状态，即使没有语句正在执行，仍会占用并发槽位。

可以设置服务器配置参数 `gp_resource_group_queuing_timeout`，指定事务在队列中等待多久后会被 Apache Cloudberry 取消。默认超时值为零，表示事务可以无限期排队。

### 绕过限制并脱离资源组 {#bypass-limits-and-unassign-from-resource-groups}

设置服务器配置参数 `gp_resource_group_bypass` 可以使查询绕过资源组的并发限制。该参数启用或禁用资源组的并发事务限制，使查询能够立即运行。默认值为 false，表示执行 `CONCURRENCY` 限制。只能为单个会话设置该参数，不能在事务或函数内部设置。如果将 `gp_resource_group_bypass` 设为 true，查询将不再受所属资源组的 CPU 或内存限制；其内存限制改为每个查询使用 `statement_mem`。如果内存不足以满足分配请求，查询会失败。

可以让只使用系统目录表的查询绕过限制，例如数据库图形用户界面（GUI）客户端为获取元数据而执行的目录查询。如果服务器配置参数 `gp_resource_group_bypass_catalog_query` 为 true（默认值），Apache Cloudberry 资源组调度器会让所有仅读取系统目录、或查询文本中只包含 `pg_catalog` 模式表的查询绕过限制。这些查询自动脱离当前资源组，不受该组限制，也不计入该组的资源用量。查询资源在资源组之外分配，查询立即运行，其内存限制为每个查询使用 `statement_mem`。

可以使用服务器配置参数 `gp_resource_group_bypass_direct_dispatch`，让直接分发查询绕过限制。直接分发查询是一类只需要单个 Segment 参与执行的特殊查询。为提高效率，Apache Cloudberry 对其采用直接分发优化，只将计划发送给需要执行它的 Segment，而不发送给所有 Segment。如果将 `gp_resource_group_bypass_direct_dispatch` 设为 true，查询将不再受所属资源组的 CPU 或内存限制，因此可以立即运行。其内存限制改为每个查询使用 `statement_mem`；如果内存不足以满足分配请求，查询会失败。只能为单个会话设置此参数，不能在事务或函数内部设置。

计划代价低于 `MIN_COST` 限制的查询会自动脱离资源组，不受该组的任何限制。查询使用的资源不计入资源组用量，其内存限制为 `statement_mem`。`MIN_COST` 默认值为 0。

### CPU 限制 {#cpu-limits}

Apache Cloudberry 使用 Linux 控制组实现 CPU 资源管理，有两种 CPU 资源分配方式：

- 将一定百分比的 CPU 资源分配给资源组
- 将特定 CPU 核分配给资源组

为资源组设置一种分配模式时，Apache Cloudberry 会禁用另一种模式。同一 Apache Cloudberry 集群中的不同资源组可以同时采用这两种 CPU 资源分配模式。也可以在运行时更改某个资源组的 CPU 资源分配模式。

Apache Cloudberry 使用服务器配置参数 `gp_resource_group_cpu_limit`，指定每个 Segment 节点上最多可分配给资源组的系统 CPU 资源百分比。其余未预留的 CPU 资源供操作系统内核和 Apache Cloudberry 守护进程使用。随后，每台主机上可供 Apache Cloudberry 查询使用的 CPU 资源，会平均分配给该节点上的各个 Segment。

> [!NOTE]
> 如果 Apache Cloudberry 集群节点上还运行其他工作负载，`gp_resource_group_cpu_limit` 的默认值可能无法为其留下足够的 CPU 资源，因此务必相应调整此服务器配置参数。

> [!WARNING]
> 避免将 `gp_resource_group_cpu_limit` 设为高于 `.9` 的值。否则，高负载查询可能占用几乎全部 CPU 资源，使 Apache Cloudberry 辅助进程缺乏运行所需的资源。

#### 按 CPU 核分配资源 {#assign-cpu-resources-by-core}

通过 `CPUSET` 属性指定要为资源组预留的 CPU 核。这些核必须在系统中可用，且不能与为其他资源组预留的核重叠。Apache Cloudberry 会将分配给某个资源组的核专供该组使用，但系统中的非 Apache Cloudberry 进程仍可能使用这些核。为资源组配置 `CPUSET` 后，Apache Cloudberry 会禁用该组的 `CPU_MAX_PERCENT` 和 `CPU_WEIGHT`，并将其值设为 -1。

分别指定 Coordinator 主机与 Segment 主机使用的 CPU 核，两部分用分号分隔。配置 `CPUSET` 时，可以使用逗号分隔的单个核编号或编号区间，且必须用单引号括起这些编号或区间。例如，`'1;1,3-4'` 表示 Coordinator 主机使用核 1，Segment 主机使用核 1、3、4。

为 `CPUSET` 组分配 CPU 核时，请考虑以下事项：

- 使用 `CPUSET` 创建的资源组独占指定核。如果组中没有运行中的查询，这些预留核就会空闲，其他资源组的查询也不能使用。应考虑尽量减少 `CPUSET` 组的数量，避免浪费系统 CPU 资源。
- 可以考虑不分配 CPU 核 0。以下情况下，核 0 会作为回退机制使用：
    - `admin_group` 和 `default_group` 至少需要一个 CPU 核。所有核都已预留时，Apache Cloudberry 会将 CPU 核 0 分配给这两个默认组。此时，原先分配了 CPU 核 0 的资源组，会与 `admin_group` 和 `default_group` 共享该核。
    - 更换一个节点后重启 Apache Cloudberry 集群时，如果该节点的核数不足以服务所有 `CPUSET` 资源组，系统会自动将这些组分配到 CPU 核 0，避免启动失败。
- 为资源组分配核时，尽量使用较小的核编号。如果替换 Apache Cloudberry 节点后的新节点核数更少，或者要将数据库备份恢复到节点核数更少的集群，操作可能失败。例如，集群有 16 个核时，分配核 1-7 较为合适；如果给资源组分配 CPU 核 9，将数据库恢复到 8 核节点就会失败。

配置了 `CPUSET` 的资源组具有更高的 CPU 资源优先级。Segment 主机上所有 `CPUSET` 资源组的最大 CPU 资源使用百分比，为预留核数除以总核数，再乘以 100。

> [!NOTE]
> 必须先通过服务器配置参数 `gp_resource_manager` 为 Apache Cloudberry 集群启用基于资源组的资源管理，*之后*才能为资源组配置 `CPUSET`。

#### 按百分比分配 CPU 资源 {#assign-cpu-resources-by-percentage}

使用 `CPU_MAX_PERCENT` 配置资源组，即可按百分比分配 CPU 资源。配置 `CPU_MAX_PERCENT` 时，Apache Cloudberry 会禁用该组的 `CPUSET`。

参数 `CPU_MAX_PERCENT` 为资源管理设置 Segment CPU 使用百分比的硬上限。单个资源组的 `CPU_MAX_PERCENT` 最小值为 1，最大值为 100；集群中所有资源组的 `CPU_MAX_PERCENT` 之和可以超过 100。它指定了在一个 CPU 时间周期内，资源组中全部任务可运行的总时间比例。组内任务用完限制所允许的时间后，在该周期的剩余时间内会被限流，直到下一周期才允许继续运行。

资源组中的任务空闲、不消耗 CPU 时间时，剩余时间会汇入全局未使用 CPU 周期池。其他资源组可以从该池借用 CPU 周期。某个资源组实际可用的 CPU 时间可能随系统中的资源组数量变化。

`CPU_MAX_PERCENT` 对 CPU 使用量施加硬上限。例如，设为 40% 时，虽然资源组可以暂时使用其他组的部分空闲 CPU 资源，但最多仍只能使用 Apache Cloudberry 可用 CPU 资源的 40%。

通过参数 `CPU_WEIGHT` 设置当前组的调度优先级。默认值为 100，取值范围为 1 到 500，表示组内任务可获得的相对 CPU 时间份额。例如，一个组的相对份额为 100，另外两个组各为 50，当所有组的进程都尝试使用全部 CPU（即所有组的 `CPU_MAX_PERCENT` 都为 100）时，第一个组获得总 CPU 时间的 50%，另外两个组各得 25%。如果再增加一个相对份额为 100 的组，第一个组就只能使用 33% 的 CPU，其余三个组分别获得 16.5%、16.5% 和 33%。

例如，考虑以下资源组：

| 组名 | CONCURRENCY | CPU_MAX_PERCENT | CPU_WEIGHT |
|---------------|-------------|-----------------|------------|
| default_group | 20          | 50              | 10         |
| admin_group   | 10          | 70              | 30         |
| system_group  | 10          | 30              | 10         |
| test          | 10          | 10              | 10         |

`default_group` 中的角色可用 CPU 比例（由 `CPU_WEIGHT` 决定）为 10/(10+30+10+10)=16%。这意味着系统负载较高时，它们至少可以使用 16% 的 CPU。系统存在空闲 CPU 资源时，可以使用更多资源，因为 `CPU_MAX_PERCENT` 设置的硬上限为 50%。

系统负载较高时，`admin_group` 中的角色可用 CPU 比例为 30/(10+30+10+10)=50%。系统存在空闲 CPU 资源时，最多可使用硬上限规定的 70%。

`test` 中的角色 CPU 比例为 10/(10+30+10+10)=16%。但由于 `CPU_MAX_PERCENT` 规定的硬上限为 10%，即使系统空闲，它们也最多只能使用 10% 的资源。

### 内存限制 {#memory-limits}

启用资源组后，内存在 Apache Cloudberry Segment 级和资源组级管理，也可以在事务级管理。

为查询分配的内存量由以下参数决定：

资源组参数 `MEMORY_QUOTA` 设置在某个 Segment 上为该组预留的最大内存量。这决定了查询执行期间，其所有工作进程在 Segment 主机上能够消耗的总内存量。查询可分配的内存量为组内存限制除以组并发限制：`MEMORY_QUOTA` / `CONCURRENCY`。

如果查询需要大量内存，可以在会话级使用服务器配置参数 `gp_resgroup_memory_query_fixed_mem` 为其设置固定内存量。此参数覆盖资源组的内存分配，且可以超出其分配量。

Apache Cloudberry 为新查询分配内存时，如果设置了 `gp_resgroup_memory_query_fixed_mem`，就使用该值并绕过资源组设置；否则使用 `MEMORY_QUOTA` / `CONCURRENCY`。如果没有设置 `MEMORY_QUOTA`，查询内存分配量默认使用 `statement_mem`。

对于所有查询，如果系统内存不足，就会溢出到磁盘。达到 `gp_workfile_limit_files_per_query` 限制时，Apache Cloudberry 会产生内存不足（OOM）错误。

例如，资源组 `adhoc` 的 `MEMORY_QUOTA` 为 1.5 GB，`CONCURRENCY` 为 `3`，默认情况下提交到该组的每条语句会分配 500 MB 内存。考虑以下事件序列：

1. 用户 `ADHOC_1` 提交查询 `Q1`，将 `gp_resgroup_memory_query_fixed_mem` 覆盖为 800MB。系统允许 `Q1` 语句开始执行。

2. 用户 `ADHOC_2` 提交查询 `Q2`，使用默认的 500MB。

3. `Q1` 和 `Q2` 仍在运行时，用户 `ADHOC3` 提交查询 `Q3`，使用默认的 500MB。

    查询 `Q1` 和 `Q2` 已使用组内 1500MB 中的 1300MB。但如果此时 Segment 中仍有足够的系统内存供 `Q3` 使用，它仍可正常运行。

4. 用户 `ADHOC4` 提交查询 `Q4`，将 `gp_resgroup_memory_query_fixed_mem` 设为 700 MB。

    由于绕过了资源组限制，`Q4` 会立即运行。

内存限制还有以下特殊注意事项：

- 如果启用配置参数 `gp_resource_group_bypass` 或 `gp_resource_group_bypass_catalog_query` 来绕过资源组限制，查询的内存分配量由 `statement_mem` 决定。
- 当（`MEMORY_QUOTA` / `CONCURRENCY`）小于 `statement_mem` 时，系统使用 `statement_mem` 作为查询的固定内存分配量。
- `statement_mem` 的最大值受 `max_statement_mem` 限制。
- 如果查询计划代价低于配置的 `MIN_COST`，也会按 `statement_mem` 分配内存。

### 磁盘 I/O 限制 {#disk-io-limits}

Apache Cloudberry 使用 Linux 控制组实现磁盘 I/O 限制。参数 `IO_LIMIT` 限制分配给特定资源组的查询的最大磁盘读写 I/O 吞吐量，以及每秒最大读写 I/O 操作数。它用于分配带宽、保障高优先级资源组使用资源，并避免过度使用磁盘带宽。该参数按表空间设置。

> [!NOTE]
> 磁盘 I/O 限制仅在使用 Linux 控制组 v2 时可用。

限制磁盘 I/O 时，需要指定：

- 要设置限制的表空间名称或表空间对象 ID（OID）。使用 `*` 可为所有表空间设置限制。
- `rbps` 和 `wbps`：限制资源组的最大磁盘读写 I/O 吞吐量，单位为 MB/sec。默认值为 `max`，表示不限制。
- `riops` 和 `wiops`：限制资源组每秒最大的读写 I/O 操作数。默认值为 `max`，表示不限制。

如果未设置 `IO_LIMIT`，`rbps`、`wpbs`、`riops` 和 `wiops` 默认均为 `max`，表示不限制磁盘 I/O。此时，`gp_toolkit.gp_resgroup_config` 系统视图将其值显示为 `-1`。如果只设置了 `IO_LIMIT` 的部分值（例如 `rbps`），其余未设置项默认使用 `max`（本例中为 `wbps`、`riops`、`wiops`）。

## 配置和使用资源组 {#configure-and-use-resource-groups}

### 前提条件 {#prerequisites}

Apache Cloudberry 资源组使用 Linux 控制组（cgroups）管理 CPU 资源和磁盘 I/O。cgroups 有 v1 和 v2 两个版本，Apache Cloudberry 均支持，但 `IO_LIMIT` 参数仅支持 cgroup v2。Linux 发行版默认提供的控制组版本取决于操作系统版本：Enterprise Linux 8 及更早版本默认使用 v1，Enterprise Linux 9 及更高版本默认使用 v2。

检查系统启动时默认挂载的文件系统，可以确认当前环境配置了哪个 cgroup 版本：

```bash
stat -fc %T /sys/fs/cgroup/
```

cgroup v1 的输出为 `tmpfs`，cgroup v2 的输出为 `cgroup2fs`。

无需更改 cgroup 版本，可以直接跳到 `optimize-performance/manage-resources-using-resource-groups:configure cgroup v1` 或 `optimize-performance/manage-resources-using-resource-groups:configure cgroup v2`，完成所需的前置配置。

如果希望从 cgroup v1 切换到 v2，请以 root 身份运行以下命令：

> [!NOTE]
> - 如果使用较早的 CentOS 版本，例如 Centos 7.x 或更早版本，只能使用默认的 `cgroup v1` 控制组。如果使用 Centos 8.x，可以按以下步骤将控制组从 v1 切换到 v2。
> - 自 v2.0.0 起，对于 `cpu.pressure`，即使 `gp_resource_manager` 设为 `group-v2`，Apache Cloudberry 也不再检查 `/proc/pressure/cpu` 接口的权限或存在性。因此，只要内核版本兼容，即使没有启用 PSI（压力停顿信息），`group-v2` 模式仍可正常工作。

- Red Hat 8/Rocky 8/Oracle 8 系统：

  ```bash
  grubby --update-kernel=/boot/vmlinuz-$(uname -r) --args="systemd.unified_cgroup_hierarchy=1"
  ```

- Ubuntu 系统：

  ```bash
  vim /etc/default/grub     # add or modify: GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=1"     
  update-grub
  ```

如果希望从 cgroup v2 切换到 v1，请以 root 身份运行以下命令：

- Red Hat 8/Rocky 8/Oracle 8 系统：

  ```bash
  grubby --update-kernel=/boot/vmlinuz-$(uname -r) --args="systemd.unified_cgroup_hierarchy=0 systemd.legacy_systemd_cgroup_controller"
  ```

- Ubuntu 系统：

  ```bash
  vim /etc/default/grub     
  # add or modify: GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"     
  update-grub
  ```

之后重启主机，使修改生效。

#### 配置 cgroup v1 {#configure-cgroup-v1}

在 Apache Cloudberry 集群的每个节点上完成以下任务，配置供资源组使用的 cgroups v1：

1. 安装 `libcgroup` 和 `libcgroup-tools`：

    ```bash
    sudo yum install libcgroup
    sudo yum install libcgroup-tools      
    ```

2. 找到 cgroups 配置文件 `/etc/cgconfig.conf`。必须是超级用户或具有 `sudo` 权限，才能编辑此文件：

    ```bash
    vi /etc/cgconfig.conf
    ```

3. 向文件添加以下配置信息：

    ```
    group gpdb {
         perm {
             task {
                 uid = gpadmin;
                 gid = gpadmin;
             }
             admin {
                 uid = gpadmin;
                 gid = gpadmin;
             }
         }
         cpu {
         }
         cpuacct {
         }
         cpuset {
         }
         memory {
         }
    } 
    ```

    这些内容配置了由 `gpadmin` 用户管理的 CPU、CPU 记账、CPU 核集合和内存控制组。Apache Cloudberry 仅使用内存控制组监控内存用量。

4. 在每个 Apache Cloudberry 节点启动 cgroups 服务。对于 Redhat/Oracle/Rocky 8.x 及更早版本，以 root 身份运行：

    ```bash
    cgconfigparser -l /etc/cgconfig.conf 
    ```

5. 为了在系统重启时自动重建 Apache Cloudberry 所需的 cgroup 层次结构和参数，请配置系统在节点启动时启用 Linux cgroup 服务守护进程 `cgconfig.service`。要确保配置在重启后保留，请以 root 用户运行以下命令。对于 Redhat/Oracle/Rocky 8.x 及更早版本：

    ```bash
    systemctl enable cgconfig.service
    ```

    要立即启动服务而不重启系统，请输入：

    ```bash
    systemctl start cgconfig.service
    ```

6. 确定节点的 `cgroup` 目录挂载点。对于 Redhat/Oracle/Rocky 8.x 及更早版本，以 root 身份运行：

    ```bash
    grep cgroup /proc/mounts
    ```

    输出的第一行标明 `cgroup` 挂载点。

7. 运行以下命令，验证 Apache Cloudberry cgroups 配置是否正确。将 `<cgroup_mount_point>` 替换为上一步确定的挂载点：

    ```bash
    ls -l <cgroup_mount_point>/cpu/gpdb
    ls -l <cgroup_mount_point>/cpuset/gpdb
    ls -l <cgroup_mount_point>/memory/gpdb
    ```

    如果这些目录存在且归 `gpadmin:gpadmin` 所有，就说明已经成功为 Apache Cloudberry 资源管理配置 cgroups。

#### 配置 cgroup v2 {#configure-cgroup-v2}

1. 以 root 用户身份配置系统，使其在启动时通过系统和服务管理器 `systemd` 默认挂载 `cgroups-v2`。

    ```bash
    grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
    ```

2. 重启系统，使修改生效：`reboot now`

3. 创建目录 `/sys/fs/cgroup/gpdb`，添加所有必需的控制器，并确保 `gpadmin` 用户具有该目录的读写权限。

    ```shell
    mkdir -p /sys/fs/cgroup/gpdb
    echo "+cpuset +io +cpu +memory" | tee -a /sys/fs/cgroup/cgroup.subtree_control
    chown -R gpadmin:gpadmin /sys/fs/cgroup/gpdb
    ```

运行上述命令后，可能会遇到 `Invalid argument` 错误。这是因为 cgroups v2 不支持控制实时进程，只有全部实时进程都位于根 cgroup 中时，才能启用 `cpu` 控制器。此时，应先找到所有实时进程并将其移到根 cgroup，再重新启用控制器。

1. 确保 `gpadmin` 对 `/sys/fs/cgroup/cgroup.procs` 具有写权限。集群启动后，需要将 Apache Cloudberry 进程从用户切片移到 `/sys/fs/cgroup/gpdb/`，以管理 postmaster 服务及其所有辅助进程，因此必须具备此权限。

    ```bash
    chmod a+w /sys/fs/cgroup/cgroup.procs
    ```

    由于资源组手动管理 cgroup 文件，上述设置在系统重启后会失效。为 systemd 添加以下 bash 脚本，使其在系统启动时自动运行。以 root 用户执行以下步骤：

2. 创建 `gpdb.service`。

    ```bash
    vim /etc/systemd/system/gpdb.service 
    ```

3. 将以下内容写入 `gpdb.service`。如果用户不是 `gpadmin`，请替换为相应用户。

    ```bash
    [Unit]
    Description=Apache Cloudberry Cgroup v2 Configuration Service
    [Service]
    Type=simple
    WorkingDirectory=/sys/fs/cgroup/gpdb.service
    Delegate=yes
    Slice=-.slice

    # set hierarchies only if cgroup v2 mounted
    ExecCondition=bash -c '[ xcgroup2fs = x$(stat -fc "%%T" /sys/fs/cgroup) ] || exit 1'
    ExecStartPre=bash -ec " \
    chown -R gpadmin:gpadmin .; \
    chmod a+w ../cgroup.procs; \
    mkdir -p helper.scope"
    ExecStart=sleep infinity
    ExecStartPost=bash -ec "echo $MAINPID > ./helper.scope/cgroup.procs;"
    [Install]
    WantedBy=basic.target
    ```

4. 重新加载 systemd 守护进程并启用服务：

    ```bash
    systemctl daemon-reload
    systemctl enable gpdb.service
    ```

## 启用资源组 {#enable-resource-groups}

安装 Apache Cloudberry 时，默认未启用任何资源管理策略。要使用资源组，请设置服务器配置参数 `gp_resource_manager`。

1. 根据 Linux 发行版配置的 cgroup 版本，将服务器配置参数 `gp_resource_manager` 设为 `"group"` 或 `"group-v2"`。例如：

    ```bash
    gpconfig -c gp_resource_manager -v "group"
    gpconfig -c gp_resource_manager -v "group-v2"
    ```

2. 重启 Apache Cloudberry：

    ```bash
    gpstop
    gpstart
    ```

启用后，角色提交的任何事务都会进入分配给该角色的资源组，并受该组的并发、内存、CPU 和磁盘 I/O 限制。

Apache Cloudberry 创建三个默认资源组：`admin_group`、`default_group` 和 `system_group`。启用资源组后，未被显式分配资源组的角色，会按其能力分配到默认组。`SUPERUSER` 角色分配到 `admin_group`，非管理员角色分配到 `default_group`。Apache Cloudberry 系统进程的资源归属 `system_group`，不能手动将任何角色分配到 `system_group`。

使用以下命令查看全部资源组的详细信息，包括默认的 `admin_group`、`default_group` 和 `system_group`：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_config;
```

## 创建资源组 {#create-resource-groups}

为角色创建资源组时，需要提供名称和 CPU 资源分配模式（按核或按百分比）。还可以选择提供并发事务限制、内存限制、CPU 软优先级、磁盘 I/O 限制和最低代价。使用 `CREATE RESOURCE GROUP` 命令创建新资源组。

为角色创建资源组时，必须提供 `CPU_MAX_PERCENT` 或 `CPUSET` 限制值。这些限制指定要分配给该组的 Apache Cloudberry CPU 资源百分比。可以指定 `MEMORY_QUOTA`，为资源组预留固定数量的内存。

例如，创建名为 *rgroup1* 的资源组，CPU 限制为 20，内存限制为 25，CPU 软优先级为 500，最低代价为 50，并为 `pg_default` 表空间设置磁盘 I/O 限制：

```sql
CREATE RESOURCE GROUP rgroup1 WITH (CONCURRENCY=20, CPU_MAX_PERCENT=20, MEMORY_QUOTA=250, CPU_WEIGHT=500, MIN_COST=50, 
IO_LIMIT='pg_default: wbps=1000, rbps=1000, wiops=100, riops=100');
```

> [!NOTE]
> 如果使用 `cgroup v1` 却指定了 IO_LIMIT，资源组仍会创建，但会产生以下警告："resource group io limit only can be used in cgroup v2"。

CPU 限制 20 由分配到 `rgroup1` 的所有角色共享；内存限制 25 同样由分配到 `rgroup1` 的所有角色共享。`rgroup1` 使用默认的 `CONCURRENCY` 设置 20。

`ALTER RESOURCE GROUP` 命令更新资源组的限制。要修改限制，请指定该组的新值。例如：

```sql
ALTER RESOURCE GROUP rg_role_light SET CONCURRENCY 7;
ALTER RESOURCE GROUP exec SET MEMORY_QUOTA 30;
ALTER RESOURCE GROUP rgroup1 SET CPUSET '1;2,4';
ALTER RESOURCE GROUP sales SET IO_LIMIT 'tablespace1:wbps=2000,wiops=2000;tablespace2:rbps=2024,riops=2024'; 
```

> [!NOTE]
> 不能将 `admin_group` 的 `CONCURRENCY` 设置或修改为零（0）。

`DROP RESOURCE GROUP` 命令删除资源组。删除角色资源组时，该组不能仍被分配给任何角色，组内也不能有活动或等待中的事务。

删除资源组：

```sql
DROP RESOURCE GROUP exec; 
```

## 根据内存用量配置自动终止查询 {#configure-automatic-query-termination-based-on-memory-usage}

Apache Cloudberry 支持失控检测器（Runaway detector），根据查询使用的内存量自动终止查询。对于资源组管理的查询，Apache Cloudberry 根据其内存用量终止运行中的查询。相关配置参数如下：

- `gp_vmem_protect_limit` 设置活动 Segment 实例的全部 `postgres` 进程可消耗的内存量。如果查询导致超出该限制，将不再分配内存，查询会失败。
- `runaway_detector_activation_percent`：启用资源组后，如果已使用的内存超过 `gp_vmem_protect_limit` \* `runaway_detector_activation_percent`，Apache Cloudberry 会根据内存用量终止查询。候选查询来自用户资源组，不包括 `system_group`。系统从内存消耗最大的查询开始终止，直到内存使用比例降到指定比例以下。

## 将资源组分配给角色 {#assign-a-resource-group-to-a-role}

通过 `CREATE ROLE` 或 `ALTER ROLE` 命令的 `RESOURCE GROUP` 子句，将资源组分配给数据库角色。如果未为角色指定资源组，就会按角色能力分配默认组：`SUPERUSER` 角色分配到 `admin_group`，非管理员角色分配到 `default_group`。

使用 `ALTER ROLE` 或 `CREATE ROLE` 命令为角色分配资源组。例如：

```sql
ALTER ROLE bill RESOURCE GROUP rg_light;
CREATE ROLE mary RESOURCE GROUP exec;
```

一个资源组可以分配给一个或多个角色。如果定义了角色层次结构，为父角色分配资源组不会向下传播到该角色组的成员。

如果希望移除角色的资源组分配并改用默认组，请将角色的组名设置为 `NONE`。例如：

```sql
ALTER ROLE mary RESOURCE GROUP NONE;
```

## 监控资源组状态 {#monitor-resource-group-status}

监控资源组和查询的状态可能涉及以下任务。

### 查看资源组限制 {#view-resource-group-limits}

`gp_toolkit.gp_resgroup_config` 系统视图显示资源组的当前限制。查看所有资源组的限制：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_config;
```

### 查看资源组查询状态 {#view-resource-group-query-status}

`gp_toolkit.gp_resgroup_status` 系统视图用于查看资源组的状态和活动，包括运行中和排队中的事务数。查看这些信息：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_status;
```

### 按主机查看资源组内存用量 {#view-resource-group-memory-usage-per-host}

`gp_toolkit.gp_resgroup_status_per_host` 系统视图用于按主机查看资源组的实时内存用量。查看这些信息：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_status_per_host;
```

### 查看分配给角色的资源组 {#view-the-resource-group-assigned-to-a-role}

要查看资源组与角色的分配关系，请对系统目录表 `pg_roles` 和 `pg_resgroup` 执行以下查询：

```sql
SELECT rolname, rsgname FROM pg_roles, pg_resgroup
WHERE pg_roles.rolresgroup=pg_resgroup.oid;
```

### 按主机查看资源组磁盘 I/O 用量 {#view-resource-group-disk-io-usage-per-host}

`gp_toolkit.gp_resgroup_iostats_per_host` 系统视图用于按主机查看资源组的实时磁盘 I/O 用量。查看这些信息：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_iostats_per_host;
```

### 查看资源组中运行和等待的查询 {#view-a-resource-groups-running-and-pending-queries}

要查看资源组中运行和等待的查询，以及等待中的查询已排队多久，请查询 `pg_stat_activity` 系统目录表：

```sql
SELECT query, rsgname,wait_event_type, wait_event 
FROM pg_stat_activity;
```

`pg_stat_activity` 显示发起查询的用户或角色信息。使用 PL/Container 等外部组件的查询由两部分组成：在 Apache Cloudberry 中运行的查询算子，以及在 PL/Container 实例中运行的 UDF。Apache Cloudberry 在分配给查询发起角色的资源组下处理查询算子。PL/Container 实例中的 UDF 则在分配给 PL/Container 运行时的资源组下执行。后者不会显示在 `pg_stat_activity` 视图中；Apache Cloudberry 无法了解 PL/Container 等外部组件如何管理运行实例中的内存。

### 取消资源组中运行或排队的事务 {#cancel-a-running-or-queued-transaction-in-a-resource-group}

某些情况下，可能需要取消资源组中运行或排队的事务。例如，移除仍在资源组队列中等待、尚未执行的查询；或者停止耗时过长的查询，以及在事务中空闲、却占用了其他用户所需事务槽位的查询。

默认情况下，事务可以在资源组中无限期排队。如果希望 Apache Cloudberry 在指定时间后取消排队事务，请设置服务器配置参数 `gp_resource_group_queuing_timeout`。该参数设为大于 0 的值（单位毫秒）时，Apache Cloudberry 会取消等待时间超过所配置超时的排队事务。

要手动取消运行或排队的事务，首先必须确定该事务关联的进程 ID（pid）。获取进程 ID 后，可以调用 `pg_cancel_backend()` 结束该进程，如下所示。

例如，要查看所有资源组中当前活动或等待的全部语句所关联的进程信息，请运行以下查询。如果没有返回结果，说明所有资源组中都没有运行或排队的事务。

```sql
SELECT rolname, g.rsgname, pid, waiting, state, query, datname 
FROM pg_roles, gp_toolkit.gp_resgroup_status g, pg_stat_activity 
WHERE pg_roles.rolresgroup=g.groupid
AND pg_stat_activity.usename=pg_roles.rolname;
```

部分查询输出示例：

```sql
rolname | rsgname  | pid     | waiting | state  |          query           | datname 
---------+----------+---------+---------+--------+------------------------ -+---------
 sammy  | rg_light |  31861  |    f    | idle   | SELECT * FROM mytesttbl; | testdb
 billy  | rg_light |  31905  |    t    | active | SELECT * FROM topten;    | testdb
```

使用此输出确定要取消的事务的进程 ID（`pid`），然后取消该进程。例如，取消上述示例输出中的等待查询：

```sql
SELECT pg_cancel_backend(31905);
```

可以在 `pg_cancel_backend()` 的第二个参数中提供可选消息，向用户说明取消进程的原因。

> [!NOTE]
> 不要使用操作系统的 `KILL` 命令取消任何 Apache Cloudberry 进程。

## 将查询移到其他资源组 {#move-a-query-to-a-different-resource-group}

具有 Apache Cloudberry 超级用户权限的用户，可以运行 `gp_toolkit.pg_resgroup_move_query()` 函数，将运行中的查询从一个资源组移到另一个组，无需停止查询。可以将长时间运行的查询移到资源配额更高或可用资源更多的组，以加快其执行。

> [!NOTE]
> 只能将活动或运行中的查询移到新资源组。由于并发或内存限制而处于空闲状态的排队或等待查询，不能移动。

`pg_resgroup_move_query()` 需要运行中查询的进程 ID（pid），以及目标资源组名称。函数签名如下：

```sql
pg_resgroup_move_query( pid int4, group_name text );
```

可以按 `optimize-performance/manage-resources-using-resource-groups:cancel a running or queued transaction in a resource group` 所述，从 `pg_stat_activity` 系统视图获取运行中查询的 pid。使用 `gp_toolkit.gp_resgroup_status` 视图可列出各资源组的名称、ID 和状态。

调用 `pg_resgroup_move_query()` 时，查询会受到目标资源组所配置限制的约束：

- 如果该组已达到并发任务限制，Apache Cloudberry 会将查询排队，直到有槽位可用；如果设置了 `gp_resource_group_queuing_timeout`，则最多等待相应的毫秒数。
- 如果该组有空闲槽位，`pg_resgroup_move_query()` 会尝试将槽位控制权交给目标进程，最长等待 `gp_resource_group_move_timeout` 毫秒。如果目标进程在 `gp_resource_group_queuing_timeout` 超时之前仍无法处理移动请求，Apache Cloudberry 会返回错误：`target process failed to move to a new group`。
- 如果 `pg_resgroup_move_query()` 被取消，但目标进程已经获得全部槽位控制权，Segment 进程将不会移到新组，目标进程仍持有槽位。这种不一致状态会在事务结束时，或目标进程在同一事务中分发下一条命令时修复。
- 如果目标资源组没有足够的可用内存满足查询当前的内存需求，Apache Cloudberry 会返回错误：`group <group_name> doesn't have enough memory ...`。此时可以增加分配给目标资源组的组共享内存，或等待一段时间，让运行中的查询完成后再调用该函数。

Apache Cloudberry 移动查询后，无法保证目标资源组中当前运行的查询不会超出组内存限制。此时，目标组中一个或多个运行中的查询可能失败，包括被移动的查询。应预留足够的资源组全局共享内存，尽量降低这种情况发生的可能性。

`pg_resgroup_move_query()` 只将指定查询移到目标资源组。此会话中后续提交的查询，仍会由 Apache Cloudberry 分配到原资源组。

## 常见问题 {#frequently-asked-questions}

**为什么 CPU 使用率低于资源组配置的 `CPU_MAX_PERCENT`？**

资源组中运行的查询和切片较少、相关进程没有利用系统全部 CPU 核时，可能出现这种情况。

我的资源组的 `CPU_WEIGHT` 相当于 40%，为什么 CPU 使用率始终达不到这个比例？

`CPU_MAX_PERCENT` 可能低于 40，因此即使有空闲资源，也会限制 CPU 使用率。

**为什么运行中的事务数低于资源组配置的 `CONCURRENCY` 限制？**

Apache Cloudberry 在运行事务前会考虑内存是否充足，内存不足时会将事务排队。如果通过 `ALTER RESOURCE GROUP` 增大了 `CONCURRENCY` 限制，却没有相应调整内存限制，当前运行中的事务可能已耗尽该组的全部内存配额。此时，Apache Cloudberry 会将该资源组的后续事务排队。

**为什么资源组中运行的事务数超过配置的 `CONCURRENCY` 限制？**

这是预期行为，可能由以下原因导致：

- 资源组不对 `SET`、`RESET` 和 `SHOW` 命令施加资源限制。
- 服务器配置参数 `gp_resource_group_bypass` 禁用资源组的并发事务限制，使查询可以立即运行。
- 如果服务器配置参数 `gp_resource_group_bypass_catalog_query` 为 true（默认值），所有仅读取系统目录、或查询文本中只包含 `pg_catalog` 模式表的查询，都不受资源组限制。
- 计划代价低于 `MIN_COST` 的查询会自动脱离资源组，不受该组任何限制。

**为什么查询返回“memory limit reached”错误？**

通过 `ALTER RESOURCE GROUP` 修改资源组的内存或并发限制时，Apache Cloudberry 会自动按新设置调整事务和组的内存。如果最近修改了资源组属性，导致当前运行的查询可用内存不足，就可能出现“out of memory”错误。

**查询因内存不足无法运行，出现内存泄漏导致的 Out of Memory（OOM）。**

首先，通过调整 `CONCURRENCY`、`MEMORY_QUOTA` 等资源组参数，确保资源组分配了查询所需的足够内存。分析查询类型，判断是否会产生大量占用内存的中间结果。如果会，可以设置合理的 `gp_resgroup_memory_query_fixed_mem`，在会话级为该查询分配更多内存。

**内存泄漏 OOM 之后，系统并发负载很高。**

系统开始清理内存泄漏遗留的会话时，并发负载会很高，OOM 错误消息可能再次出现。受当前设计限制，无法加快失控会话（Runaway Session）的清理过程。解决方法是将 `runaway_detector_activation_percent` 调整为 0.85、0.8，甚至更低，以增加 Segment 主机的可用内存。

**某些事务请求只在特定时段运行，其他时间不运行。**

可以按固定时间间隔动态修改资源组配置，匹配工作负载要求，并为不同时段定制资源分配，以提高效率。例如，修改组内资源配置，或添加、删除资源组。
