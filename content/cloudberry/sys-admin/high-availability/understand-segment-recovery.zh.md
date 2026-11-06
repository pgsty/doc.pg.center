---
title: "理解 Segment 恢复"
description: "本节介绍 Segment 恢复的相关概念和原理。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/understand-segment-recovery.md"
---

如果已有 Segment 停止运行，需要立即恢复，请参见[从 Segment 故障中恢复](/cloudberry/sys-admin/high-availability/recover-from-segment-failures/)中的操作说明。关于 Apache Cloudberry 如何检测 Segment 停止运行，以及用于跟踪故障 Segment 的容错服务器（FTS），参见 [Apache Cloudberry 如何检测 Segment 故障](/cloudberry/sys-admin/high-availability/detect-a-failed-segment/)。

本节分为以下部分：

- [Segment 恢复基础](#segment-recovery-basics)
- [Segment 恢复过程](#segment-recovery-flow-of-events)
- [简单的故障切换与恢复示例](#simple-failover-and-recovery-example)
- [三种 Segment 恢复方式](#the-three-types-of-segment-recovery)

## Segment 恢复基础 {#segment-recovery-basics}

如果 Coordinator 无法连接某个 Segment 实例，就会在 Apache Cloudberry 的 `gp_segment_configuration` 表中将其标记为 down。该实例会保持离线，直到管理员采取措施使其重新上线。恢复故障 Segment 实例或主机的过程，取决于故障原因以及是否启用了镜像。Segment 实例可能因多种原因被标记为 down：

- Segment 主机不可用，例如发生网络或硬件故障。
- Segment 实例未运行，例如没有 `postgres` 数据库监听进程。
- Segment 实例的数据目录损坏或缺失，例如数据无法访问、文件系统损坏或磁盘故障。

要使故障 Segment 实例恢复运行，必须先纠正最初导致故障的问题。如果已启用镜像，随后可以尝试使用 `gprecoverseg` 工具从其镜像恢复 Segment 实例。关于恢复故障 Segment 数据的三种方式，参见下文[三种 Segment 恢复方式](#the-three-types-of-segment-recovery)。

## Segment 恢复过程 {#segment-recovery-flow-of-events}

**主 Segment 停止运行时**

**主** Segment 停止运行后，处理过程如下：

1. 主 Segment 停止运行。
2. 容错服务器（FTS）检测到故障，在 `gp_segment_configuration` 表中将该 Segment 标记为 down。
3. 镜像 Segment 提升为主 Segment，开始承担主实例角色。原主实例降为镜像。
4. 用户修复根本原因。
5. 用户运行 `gprecoverseg`，恢复该镜像 Segment（此前的主实例）。
6. WAL 同步过程确保镜像 Segment 的数据与主 Segment 同步。用户可以通过 `gpstate -e` 检查同步状态。
7. Apache Cloudberry 在 `gp_segment_configuration` 表中将这些 Segment 标记为正常运行（`u`）。
8. 如果 Segment 未处于首选角色，用户运行 `gprecoverseg -r`，使它们恢复首选角色。

**镜像 Segment 停止运行时**

**镜像** Segment 停止运行后，处理过程如下：

1. 镜像 Segment 停止运行。
2. 容错服务器（FTS）检测到故障，在 `gp_segment_configuration` 表中将该 Segment 标记为 down。
3. 用户修复根本原因。
4. 用户运行 `gprecoverseg`，恢复该镜像 Segment（此前也是镜像）。
5. 执行同步过程：镜像通过 WAL 同步与其主实例保持一致。可以使用 `gpstate -e` 检查同步状态。

## 恢复后重新平衡 {#rebalance-after-recovery}

Segment 实例恢复后，可能未处于首选角色，导致处理负载倾斜。`gp_segment_configuration` 表包含 `role`（当前角色）和 `preferred_role`（最初的角色）列。当 Segment 的 `role` 与 `preferred_role` 不一致时，系统可能不均衡。要重新平衡集群，使所有 Segment 回到首选角色，请运行 `gprecoverseg -r` 命令。

## 简单的故障切换与恢复示例 {#simple-failover-and-recovery-example}

以一对主 Segment 和镜像 Segment 为例，假设主实例已发生故障切换，由镜像接管。下表列出开始恢复故障主 Segment 之前，`gp_segment_configuration` 表中的首选角色、当前角色、模式和状态。

还可以运行 `gpstate -e`，显示主 Segment 或镜像 Segment 实例存在的问题。

| Segment 类型 |`preferred_role`|`role`|`mode`|`status`|
|--------------|----------------|------|------|--------|
|主实例|`p`（主）|`m`（镜像）|`n`（未同步）|`d`（不可用）|
|镜像实例|`m`（镜像）|`p`（主）|`n`（未同步）|`u`（正常运行）|

主 Segment 已停止运行，两个 Segment 实例均未处于首选角色。镜像 Segment 正常运行，当前角色是主实例。但由于其镜像（原主 Segment）已停止运行，它尚未与该镜像同步。你可能需要修复故障 Segment 所在主机的问题、Segment 实例自身的问题，或同时修复两者。随后使用 `gprecoverseg` 为故障 Segment 实例的恢复做好准备，并启动主实例与镜像实例之间的同步。

`gprecoverseg` 完成后，Segment 处于下表所示状态：主实例和镜像实例均正常运行，但角色与首选角色相反。

> [!NOTE]
> `gprecoverseg` 完成后，到 Segment 状态被设为 `u`（正常运行）之间，可能存在延迟。

| Segment 类型 |`preferred_role`|`role`|`mode`|`status`|
|--------------|----------------|------|------|--------|
|主实例|`p`（主）|`m`（镜像）|`s`（已同步）|`u`（正常运行）|
|镜像实例|`m`（镜像）|`p`（主）|`s`（已同步）|`u`（正常运行）|

`gprecoverseg -r` 命令通过将 Segment 恢复为首选角色来重新平衡系统。

| Segment 类型 |`preferred_role`|`role`|`mode`|`status`|
|--------------|----------------|------|------|--------|
|主实例|`p`（主）|`p`（主）|`s`（已同步）|`u`（正常运行）|
|镜像实例|`m`（镜像）|`m`（镜像）|`s`（已同步）|`u`（正常运行）|

## 三种 Segment 恢复方式 {#the-three-types-of-segment-recovery}

Apache Cloudberry 可以执行三种 Segment 恢复：全量恢复、差异恢复和增量恢复（默认）。

全量恢复
:  全量恢复会恢复全部 Segment。具体而言，它会清除当前镜像 Segment 上的全部数据文件和目录，再将当前主 Segment 的完整内容复制到镜像 Segment。全量恢复使用 `pg_basebackup` 工具复制文件。

   全量恢复支持以下目标：

   - 当前主机，即“原地恢复”
   - 当前集群内的另一台主机
   - 当前集群外的新主机

差异恢复
:   差异恢复会在主 Segment 与镜像 Segment 之间进行文件系统级比较，仅将主实例上发生变化的文件复制到镜像。差异恢复只支持原地恢复，使用 `rsync` 命令复制文件。

增量恢复（默认）
:   增量恢复借助预写式日志文件（WAL 文件），使镜像 Segment 内容与主 Segment 同步。增量恢复只支持原地恢复，使用 `pg_rewind` 工具复制文件。

    默认情况下，`gprecoverseg` 执行增量恢复，将镜像置于*同步中*模式，开始在镜像上重放从主实例记录下来的变更。如果增量恢复无法完成，恢复就会失败；此时应再次运行带 `-F` 选项的 `gprecoverseg`，执行全量恢复，使主实例将全部数据复制到镜像。

    > [!NOTE]
    > 增量恢复尝试失败后，必须执行全量恢复。

    应尽可能使用增量恢复，因为其速度明显快于全量恢复。如果**确实**需要原地全量恢复，可以使用 `gprecoverseg` 的 `--differential` 选项加速：这会使 `gprecoverseg` 跳过所有未发生变化的文件和目录。
