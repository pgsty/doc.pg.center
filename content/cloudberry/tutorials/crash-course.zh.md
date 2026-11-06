---
title: "Apache Cloudberry 速成课程"
description: "如果想快速学习 Apache Cloudberry，请按照本速成课程操作。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/crash-course.md"
---

本速成课程全面介绍 Apache Cloudberry，这是一种开源的大规模并行处理（MPP）数据库。课程涵盖关键概念、功能、工具和实践练习，帮助你熟练掌握 Cloudberry。

主题包括：

- [第 0 课：前置条件](#lesson-0-prerequisite)
- [第 1 课：在哪里阅读官方文档](#lesson-1-where-to-read-the-official-documentation)
- [第 2 课：如何安装 Cloudberry](#lesson-2-how-to-install-cloudberry)
- [第 3 课：集群架构](#lesson-3-cluster-architecture)
- [第 4 课：管理工具](#lesson-4-management-utilities)
- [第 5 课：启动和停止集群](#lesson-5-start-and-stop-a-cluster)
- [第 6 课：检查集群状态](#lesson-6-check-cluster-state)
- [第 7 课：Cloudberry Segment 镜像的工作方式](#lesson-7-how-cloudberry-segment-mirroring-works)
- [第 8 课：Cloudberry 的容错与 Segment 恢复](#lesson-8-cloudberrys-fault-tolerance-and-segment-recovery)
- [第 9 课：设置并管理 Cloudberry 中的 Standby Coordinator 实例](#lesson-9-set-up-and-manage-the-standby-coordinator-instance-in-cloudberry)
- [第 10 课：扩容集群](#lesson-10-expand-a-cluster)
- [第 11 课：检查集群性能](#lesson-11-check-cluster-performance)
- [第 12 课：用户数据与表分布](#lesson-12-user-data-and-table-distribution)
- [第 13 课：数据库目录](#lesson-13-database-catalog)
- [第 14 课：Cloudberry 数据目录](#lesson-14-cloudberry-data-directories)
- [第 15 课：实例进程](#lesson-15-instance-processes)
    - [Coordinator 进程：](#coordinator-processes)
    - [主进程：](#primary-processes)
    - [镜像进程：](#mirror-processes)
- [第 16 课：数据库日志文件](#lesson-16-database-log-files)
- [第 17 课：Cloudberry 中的表类型：堆表、AO 表和 AOCO 表](#lesson-17-table-types-in-cloudberry-heap-ao-and-aoco)
- [第 18 课：外部表](#lesson-18-external-tables)
- [第 19 课：工作负载管理](#lesson-19-workload-management)

## 第 0 课：前置条件 {#lesson-0-prerequisite}

开始本速成课程前，请先阅读[基于单节点安装的 Apache Cloudberry 教程](https://github.com/apache/cloudberry-bootcamp/tree/main/000-cbdb-sandbox/configs)，熟悉 Apache Cloudberry 及其工作方式。

## 第 1 课：在哪里阅读官方文档 {#lesson-1-where-to-read-the-official-documentation}

快速浏览官方 [Cloudberry 文档](/cloudberry/introduction/cbdb-overview/)。如果不能全部理解，不必担心。

## 第 2 课：如何安装 Cloudberry {#lesson-2-how-to-install-cloudberry}

开始学习 Cloudberry 前，请先在偏好的环境中安装 Cloudberry。可以选择以下方式：

- 要在沙箱环境中测试或试用 Cloudberry，请参阅[在沙箱中安装 Cloudberry](https://github.com/apache/cloudberry-bootcamp/tree/main/000-cbdb-sandbox/configs)。
- 要在其他环境（包括生产环境）中部署 Cloudberry，并了解所需的软件和硬件配置，请参阅 [Cloudberry 部署指南](https://cloudberry.apache.org/docs/next/deployment/)。

## 第 3 课：集群架构 {#lesson-3-cluster-architecture}

Cloudberry 集群包含一个 Coordinator 主机（通常命名为 `cdw`）和多个 Segment 主机（通常命名为 `sdwXX`）。

> [!NOTE]
如果有人提到 `cdw`，指的是“Coordinator 主机”。同样，如果有人提到“sdw10”，指的是第 10 个 Segment 主机。

Coordinator 主机通常只包含一个实例，即 Coordinator 实例。Segment 主机可能包含许多工作实例。每个实例都有自己的一组进程、数据目录和监听端口。例如，Coordinator 实例（所有客户端都连接到这里）的监听端口通常是 `5432`。

每个 Segment 实例都有自己的监听端口，基准端口在集群配置文件中指定。

实例可以有两种角色：主实例和镜像实例。主实例提供数据库查询服务。镜像实例只跟踪并记录主实例中的数据变化，不提供数据库查询服务。如果主实例因故停机，相应的镜像实例会切换为主角色并开始提供查询服务（原主实例当前已停机，会被标记为镜像实例）。

集群信息存储在 `gp_segment_configuration` 系统表中，该表如下所示（使用“psql”命令连接数据库并执行查询）：

```shell
[gpadmin@cdw ~]$ psql

psql (14.4, server 14.4)
Type "help" for help.
```

```sql
gpadmin=# SELECT * FROM gp_segment_configuration;

 dbid | content | role | preferred_role | mode | status | port  | hostname | address |            datadir
------+---------+------+----------------+------+--------+-------+----------+---------+--------------------------------
    1 |      -1 | p    | p              | n    | u      |  5432 | cdw      | cdw     | /data0/database/coordinator/gpseg-1
    2 |       0 | p    | p              | n    | u      | 40000 | cdw      | cdw     | /data0/database/primary/gpseg0
    3 |       1 | p    | p              | n    | u      | 40001 | cdw      | cdw     | /data0/database/primary/gpseg1
(3 rows)
```

该系统表的列说明如下。

- `dbid`：唯一标识一个 Segment。
- `content`：唯一标识一对 Segment（主实例和镜像实例）。主实例及其对应的镜像实例具有相同的 `content` ID，但 `dbid` 值不同。Coordinator 的 `content` 值为 `-1`。工作实例的 content 值按递增顺序为 `0`、`1`、`2`、`3`……
- `role`：Segment 的当前角色。
- `preferred_role`：Segment 在原始配置中的角色。请注意，如果原始镜像实例已经接管并成为主实例，其 role 会发生变化；此列记录原始角色。
- `mode`：Segment 的模式。可选值为 `s`（同步）、`c`（变更跟踪）和 `r`（恢复）。
- `status`：Segment 的状态。可选值为 `u`（运行）和 `d`（停机）。
- `port`：Segment 的监听端口。对于客户端，只有 Coordinator 的监听端口重要；Segment 的监听端口用于 Coordinator 与它们通信。
- `hostname`：Segment 的主机名。
- `address`：每台主机可以有不同的网络控制器，并关联不同的 IP 地址和名称。
- `datadir`：存储每个 Segment 数据的数据目录。

**练习**

连接到你创建的 Cloudberry 集群，查看 `gp_segment_configuration` 表。尝试了解其中的行和列，并查看用于创建集群的集群配置文件。

## 第 4 课：管理工具 {#lesson-4-management-utilities}

Cloudberry 的管理工具是用于管理数据库集群的命令行工具。其主要作用包括：

- 执行启动、停止和配置数据库等任务。
- 帮助监控集群的健康状况和状态。
- 用于节点恢复、数据重平衡等维护工作。
- 通过增加节点扩容集群。
- 工具可以跨 Coordinator、Standby Coordinator 和多个 Segment 实例工作。

总之，管理工具是 DBA 用于管理、监控和维护 Cloudberry 集群的命令行程序和脚本。下面列出一些常用工具。

- `gpstop`：停止数据库集群。
- `gpstart`：启动数据库集群。
- `psql`：命令行客户端。
- `gpconfig`：显示或更改配置参数。
- `gpdeletesystem`：删除集群。
- `pg_dump`、`gpbackup`、`gprestore`：执行备份和恢复操作。
- `gpinitstanby`、`gpactivatestandby`：管理 Standby Coordinator 实例。
- `gprecoverseg`：恢复 Segment。
- `gpfdist`、`gpload`：操作外部表。
- `gpssh`、`gpscp`、`gpssh-exkeys`：用于集群导航。
- 日志：所有工具都将日志文件写入 `~/gpAdminLogs/`，每天一个文件。

**练习**

阅读这些工具的帮助信息（`<tool_name> --help`）。

## 第 5 课：启动和停止集群 {#lesson-5-start-and-stop-a-cluster}

- 使用 `gpstart` 启动 Cloudberry 集群：

    ```shell
    [gpadmin@cdw ~]$ gpstart -a
    ```

    ```shell
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Starting gpstart with args: -a
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Gathering information and validating the environment...
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Cloudberry Binary Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Cloudberry Catalog Version: '302206171'
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Starting Coordinator instance in admin mode
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-CoordinatorStart pg_ctl cmd is env GPSESSID=0000000000 GPERA=None $GPHOME/bin/pg_ctl -D /data0/database/coordinator/gpseg-1 -l /data0/database/coordinator/gpseg-1/log/startup.log -w -t 600 -o " -p 5432 -c gp_role=utility " start
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Obtaining Cloudberry Coordinator catalog information
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Setting new coordinator era
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Coordinator Started...
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Shutting down coordinator
    20230823:16:14:23:004256 gpstart:cdw:gpadmin-[INFO]:-Commencing parallel primary and mirror segment instance startup, please wait...
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Process results...
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-   Successful segment starts                                            = 4
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-   Failed segment starts                                                = 0
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-   Skipped segment starts (segments are marked down in configuration)   = 0
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Successfully started 4 of 4 segment instances
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Starting Coordinator instance cdw directory /data0/database/coordinator/gpseg-1
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-CoordinatorStart pg_ctl cmd is env GPSESSID=0000000000 GPERA=45b5ca734de32094_230823161423 $GPHOME/bin/pg_ctl -D /data0/database/coordinator/gpseg-1 -l /data0/database/coordinator/gpseg-1/log/startup.log -w -t 600 -o " -p 5432 -c gp_role=dispatch " start
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Command pg_ctl reports Coordinator cdw instance active
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Connecting to db template1 on host localhost
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-No standby coordinator configured.  skipping...
    20230823:16:14:24:004256 gpstart:cdw:gpadmin-[INFO]:-Database successfully started
    ```

- 使用 `gpstop` 停止 Cloudberry 集群：

    ```shell
    [gpadmin@cdw ~]$ gpstop -a
    ```

    ```shell
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Starting gpstop with args: -a
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Gathering information and validating the environment...
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Obtaining Cloudberry Coordinator catalog information
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Cloudberry Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Commencing Coordinator instance shutdown with mode='smart'
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Coordinator segment instance directory=/data0/database/coordinator/gpseg-1
    20230823:16:14:18:004143 gpstop:cdw:gpadmin-[INFO]:-Stopping coordinator segment and waiting for user connections to finish ...
    server shutting down
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-Attempting forceful termination of any leftover coordinator process
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-Terminating processes for segment /data0/database/coordinator/gpseg-1
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-No standby coordinator host configured
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-Targeting dbid [2, 4, 3, 5] for shutdown
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-Commencing parallel primary segment instance shutdown, please wait...
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-0.00% of jobs completed
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-100.00% of jobs completed
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-Commencing parallel mirror segment instance shutdown, please wait...
    20230823:16:14:19:004143 gpstop:cdw:gpadmin-[INFO]:-0.00% of jobs completed
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-100.00% of jobs completed
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-   Segments stopped successfully      = 4
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-   Segments with errors during stop   = 0
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-Successfully shutdown 4 of 4 segment instances
    20230823:16:14:20:004143 gpstop:cdw:gpadmin-[INFO]:-Database successfully shutdown with no errors reported
    ```

**练习**

阅读 `gpstop` 和 `gpstart` 的日志条目，尝试理解其含义。阅读并练习 `gpstart` 和 `gpstop` 的不同选项。

## 第 6 课：检查集群状态 {#lesson-6-check-cluster-state}

- 使用 `gpstate` 检查集群状态。

    `gpstate` 是用于提供集群状态信息的工具。可以添加不同选项来查看集群状态的不同方面。

    ```shell
    [gpadmin@cdw ~]$ gpstate
    ```

    ```shell
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-Starting gpstate with args:
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-local Cloudberry Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-coordinator Cloudberry Version: 'PostgreSQL 14.4 (Apache Cloudberry 1.0.0 build dev) on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 10.2.1 20210130 (Red Hat 10.2.1-11), 64-bit compiled on Aug  9 2023 14:45:43'
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-Gathering data from segments...
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-Cloudberry instance status summary
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Coordinator instance                                      = Active
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Coordinator standby                                       = No coordinator standby configured
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total segment instance count from metadata                = 4
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Primary Segment Status
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total primary segments                                    = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total primary segment valid (at coordinator)              = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total primary segment failures (at coordinator)           = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid files missing              = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid files found                = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs missing               = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs found                 = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of /tmp lock files missing                   = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of /tmp lock files found                     = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number postmaster processes missing                 = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number postmaster processes found                   = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Mirror Segment Status
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total mirror segments                                     = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total mirror segment valid (at coordinator)               = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total mirror segment failures (at coordinator)            = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid files missing              = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid files found                = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs missing               = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs found                 = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of /tmp lock files missing                   = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number of /tmp lock files found                     = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number postmaster processes missing                 = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number postmaster processes found                   = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number mirror segments acting as primary segments   = 0
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-   Total number mirror segments acting as mirror segments    = 2
    20230823:16:17:41:004530 gpstate:cdw:gpadmin-[INFO]:-----------------------------------------------------
    ```

- 查询 `gp_segment_configuration` 系统表检查集群状态。`gp_segment_configuration` 表显示有关集群状态的“Coordinator 实例”信息。

**练习**

检查集群状态，并尝试使用 `gpstate` 或 `gp_segment_configuration` 收集相关信息。

## 第 7 课：Cloudberry Segment 镜像的工作方式 {#lesson-7-how-cloudberry-segment-mirroring-works}

**Cloudberry 镜像概述：**

Apache Cloudberry 中的每个 Segment 实例都有两种可能的角色：主实例和镜像实例。

- 主角色：提供用户查询服务。
- 镜像角色：使用 WAL 复制跟踪并记录主实例的数据变化，但不提供用户查询服务。

如果主 Segment 实例遇到问题并停机，其对应的镜像 Segment 会接管主角色，确保查询服务连续。系统随后会将原主 Segment（当前已无法工作）标记为镜像。

**Segment 模式**

Segment 可以处于以下模式之一：

- `s`：同步。
- `c`：变更跟踪。
- `r`：恢复。

主 Segment 和镜像 Segment 的理想状态都是运行且同步（表示为 `P:u/s` 和 `M:u/s`）。

**Cloudberry 镜像场景**

- 场景 1：镜像实例停机时，会发生以下过程。

    1. 主 Segment 从同步模式切换到变更跟踪模式（`P:u/c` 和 `M:d/s`）。
    2. 记录并存储所有数据变化。
    3. DBA 注意到这一情况后进行调查，并使用 `gprecoverseg` 命令开始恢复镜像实例。
    4. 主 Segment 和镜像 Segment 都切换到恢复模式（`P:u/r`、`M:u/r`）。
    5. 恢复完成后，主 Segment 和镜像 Segment 都回到同步模式（`P:u/s`、`M:u/s`）。

    由于主 Segment 仍然正常工作，对用户而言该场景是透明的。因此，查询会继续运行，不会中断。

- 场景 2：主实例停机时，会发生以下过程。

    1. 终止主实例上的所有活动会话。
    2. 数据库系统将主实例标记为“down”，并将镜像实例提升为主角色，使其能够跟踪变化（`M:d/s`、`P:u/c`）。
    3. DBA 检测到这一情况后进行调查，并使用 `gprecoverseg` 命令开始恢复镜像。
    4. 开始恢复时，主 Segment 和镜像 Segment 都切换到恢复模式（`(M:u/r`、`P:u/r`）。
    5. 恢复完成后，两个 Segment 都切换到同步模式（`M:u/s`、`P:u/s`）。

    恢复后，实例的角色已经改变（原主实例现在是镜像实例）。要将 Segment 恢复为原始角色，需要对其进行重平衡。可以采用以下任一方式：

    - 使用 `gpstop` 和 `gpstart` 命令。
    - 使用 `gprecoverseg -r` 命令进行重平衡。

**向现有集群添加镜像**

如果 Cloudberry 集群最初创建时没有镜像，可以使用 `gpaddmirrors` 工具向现有集群添加镜像。示例如下：

```shell
[gpadmin@cdw ~]$ gpaddmirrors
```

> [!DETAILS] gpaddmirrors 示例输出
> ```shell
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Starting gpaddmirrors with args:
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-local Cloudberry Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-coordinator Cloudberry Version: 'PostgreSQL 14.4 (Apache Cloudberry 1.0.0 build dev) on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 10.2.1 20210130 (Red Hat 10.2.1-11), 64-bit compiled on Aug  9 2023 14:45:43'
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Successfully finished pg_controldata /data0/database/primary/gpseg0 for dbid 2:
> stdout: pg_control version number:            13000700
> Catalog version number:               302206171
> Database system identifier:           7270424369249924934
> Database cluster state:               in production
> pg_control last modified:             Wed 23 Aug 2023 03:59:52 PM CST
> Latest checkpoint location:           0/50EBA18
> Latest checkpoint's REDO location:    0/50EB9E0
> Latest checkpoint's REDO WAL file:    000000010000000000000001
> Latest checkpoint's TimeLineID:       1
> Latest checkpoint's PrevTimeLineID:   1
> Latest checkpoint's full_page_writes: on
> Latest checkpoint's NextXID:          0:762
> Latest checkpoint's NextGxid:         1
> Latest checkpoint's NextOID:          13266
> Latest checkpoint's NextRelfilenode:  12002
> Latest checkpoint's NextMultiXactId:  1
> Latest checkpoint's NextMultiOffset:  0
> Latest checkpoint's oldestXID:        752
> Latest checkpoint's oldestXID's DB:   1
> Latest checkpoint's oldestActiveXID:  761
> Latest checkpoint's oldestMultiXid:   1
> Latest checkpoint's oldestMulti's DB: 1
> Latest checkpoint's oldestCommitTsXid:0
> Latest checkpoint's newestCommitTsXid:0
> Time of latest checkpoint:            Wed 23 Aug 2023 03:59:52 PM CST
> Fake LSN counter for unlogged rels:   0/3E8
> Minimum recovery ending location:     0/0
> Min recovery ending loc's timeline:   0
> Backup start location:                0/0
> Backup end location:                  0/0
> End-of-backup record required:        no
> wal_level setting:                    replica
> wal_log_hints setting:                off
> max_connections setting:              60
> max_worker_processes setting:         13
> max_wal_senders setting:              10
> max_prepared_xacts setting:           250
> max_locks_per_xact setting:           128
> track_commit_timestamp setting:       off
> Maximum data alignment:               8
> Database block size:                  32768
> Blocks per segment of large relation: 32768
> WAL block size:                       32768
> Bytes per WAL segment:                67108864
> Maximum length of identifiers:        64
> Maximum columns in an index:          32
> Maximum size of a TOAST chunk:        8140
> Size of a large-object chunk:         8192
> Date/time type storage:               64-bit integers
> Float8 argument passing:              by value
> Data page checksum version:           1
> Mock authentication nonce:            94edd2a762753f7d12faff1737ffb338dec6e01a90eb3d509c6afc67e78bf58e
> File encryption method:
>
> stderr:
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Successfully finished pg_controldata /data0/database/primary/gpseg1 for dbid 3:
> stdout: pg_control version number:            13000700
> Catalog version number:               302206171
> Database system identifier:           7270424369087874885
> Database cluster state:               in production
> pg_control last modified:             Wed 23 Aug 2023 03:59:52 PM CST
> Latest checkpoint location:           0/50EBA18
> Latest checkpoint's REDO location:    0/50EB9E0
> Latest checkpoint's REDO WAL file:    000000010000000000000001
> Latest checkpoint's TimeLineID:       1
> Latest checkpoint's PrevTimeLineID:   1
> Latest checkpoint's full_page_writes: on
> Latest checkpoint's NextXID:          0:762
> Latest checkpoint's NextGxid:         1
> Latest checkpoint's NextOID:          13266
> Latest checkpoint's NextRelfilenode:  12002
> Latest checkpoint's NextMultiXactId:  1
> Latest checkpoint's NextMultiOffset:  0
> Latest checkpoint's oldestXID:        752
> Latest checkpoint's oldestXID's DB:   1
> Latest checkpoint's oldestActiveXID:  761
> Latest checkpoint's oldestMultiXid:   1
> Latest checkpoint's oldestMulti's DB: 1
> Latest checkpoint's oldestCommitTsXid:0
> Latest checkpoint's newestCommitTsXid:0
> Time of latest checkpoint:            Wed 23 Aug 2023 03:59:52 PM CST
> Fake LSN counter for unlogged rels:   0/3E8
> Minimum recovery ending location:     0/0
> Min recovery ending loc's timeline:   0
> Backup start location:                0/0
> Backup end location:                  0/0
> End-of-backup record required:        no
> wal_level setting:                    replica
> wal_log_hints setting:                off
> max_connections setting:              60
> max_worker_processes setting:         13
> max_wal_senders setting:              10
> max_prepared_xacts setting:           250
> max_locks_per_xact setting:           128
> track_commit_timestamp setting:       off
> Maximum data alignment:               8
> Database block size:                  32768
> Blocks per segment of large relation: 32768
> WAL block size:                       32768
> Bytes per WAL segment:                67108864
> Maximum length of identifiers:        64
> Maximum columns in an index:          32
> Maximum size of a TOAST chunk:        8140
> Size of a large-object chunk:         8192
> Date/time type storage:               64-bit integers
> Float8 argument passing:              by value
> Data page checksum version:           1
> Mock authentication nonce:            baf9fb0b44c5cc558357b266024336445d958e35f8896fcd94b5ef2143ad052d
> File encryption method:
>
> stderr:
> 20230823:16:02:50:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Heap checksum setting consistent across cluster
> Enter mirror segment data directory location 1 of 2 >
> /data0/database/mirror
> Enter mirror segment data directory location 2 of 2 >
> /data0/database/mirror
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Cloudberry Add Mirrors Parameters
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Cloudberry coordinator data directory    = /data0/database/coordinator/gpseg-1
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Cloudberry coordinator port              = 5432
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Batch size                              = 16
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Segment batch size                      = 64
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Mirror 1 of 2
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance host        = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance address     = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance directory   = /data0/database/primary/gpseg0
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance port        = 40000
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance host         = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance address      = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance directory    = /data0/database/mirror/gpseg0
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance port         = 41000
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Mirror 2 of 2
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance host        = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance address     = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance directory   = /data0/database/primary/gpseg1
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Primary instance port        = 40001
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance host         = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance address      = cdw
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance directory    = /data0/database/mirror/gpseg1
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-   Mirror instance port         = 41001
> 20230823:16:03:16:003517 gpaddmirrors:cdw:gpadmin-[INFO]:---------------------------------------------
>
> Continue with add mirrors procedure Yy|Nn (default=N):
> > y
> 20230823:16:03:30:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Starting to create new pg_hba.conf on primary segments
> 20230823:16:03:31:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Successfully modified pg_hba.conf on primary segments to allow replication connections
> 20230823:16:03:31:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-2 segment(s) to add
> 20230823:16:03:31:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Setting up the required segments for recovery
> 20230823:16:03:31:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Running recovery for the required segments
> cdw (dbid 4): pg_basebackup: base backup completed
> cdw (dbid 5): pg_basebackup: base backup completed
> 20230823:16:03:33:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Updating configuration with new mirrors
> 20230823:16:03:33:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Starting mirrors
> 20230823:16:03:33:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-era is 45b5ca734de32094_230823155950
> 20230823:16:03:33:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Commencing parallel segment instance startup, please wait...
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Process results...
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-******************************************************************
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Mirror segments have been added; data synchronization is in progress.
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Data synchronization will continue in the background.
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-Use  gpstate -s  to check the resynchronization progress.
> 20230823:16:03:34:003517 gpaddmirrors:cdw:gpadmin-[INFO]:-******************************************************************
> ```
> <br />

**练习**

向集群添加镜像。如果集群已经有镜像，请删除集群并重新创建一个没有镜像的集群（不支持删除镜像 Segment）。

## 第 8 课：Cloudberry 的容错与 Segment 恢复 {#lesson-8-cloudberrys-fault-tolerance-and-segment-recovery}

**Cloudberry 容错系统**

Cloudberry 的容错服务（FTS）持续监控集群，确保活动 Segment 能够不间断工作。如果某个 Segment 停机，系统会进行调整，确保每个 content 始终有一个可用的主实例。如果某个 content 的主实例和镜像实例都发生故障，这种情况称为“双重故障”，数据库将无法使用。

**FTS 服务的工作原理**

FTS 服务在 Coordinator 节点上通过“ftsprober”进程运行。该进程定期扫描 Segment。如果发现与上次保存的配置相比有任何变化，就会进行必要的调整。这些调整的详细信息存储在 Coordinator 日志文件和 `gp_configuration_history` 表中，同时每个实例的状态会更新到 `gp_segment_configuration` 表中。

下面是 `gp_configuration_history` 表的示例：

```sql
gpadmin=# SELECT * FROM gp_configuration_history;

             time              | dbid |                                      desc
-------------------------------+------+--------------------------------------------------------------------------------
 2023-08-23 16:03:33.917057+08 |    4 | gpaddmirrors: segment config for resync: inserted mirror segment configuration
 2023-08-23 16:03:33.917057+08 |    5 | gpaddmirrors: segment config for resync: inserted mirror segment configuration
 2023-08-23 16:03:52.784083+08 |    2 | FTS: update role, status, and mode for dbid 2 with contentid 0 to p, u, and s
 2023-08-23 16:03:52.78515+08  |    4 | FTS: update role, status, and mode for dbid 4 with contentid 0 to m, u, and s
 2023-08-23 16:03:52.794198+08 |    3 | FTS: update role, status, and mode for dbid 3 with contentid 1 to p, u, and s
 2023-08-23 16:03:52.794214+08 |    5 | FTS: update role, status, and mode for dbid 5 with contentid 1 to m, u, and s
(6 rows)
```

**恢复停机的 Segment**

如果 Segment 停机，可以使用 `gprecoverseg` 工具恢复它。该工具会读取 `gp_segment_configuration` 表，识别停机的 Segment，并尝试使用其关联的主 Segment 进行恢复。不过，要使恢复成功，主 Segment 必须处于活动状态。

**调查 Segment 故障**

1. 检查 `gp_segment_configuration` 表，查找停机的 Segment 及其镜像。
2. 阅读 Coordinator 日志文件，确定故障发生的时间。查找以“FTS:”开头的日志条目。
3. 阅读 `gp_configuration_history` 表，查看已记录事件的列表。
4. 检查主实例和镜像实例的日志文件，了解 Segment 故障的原因。
5. 确定故障原因后，使用 `gprecoverseg` 恢复 Segment。
6. 使用 `gpstate -e` 命令监控恢复过程。

**练习**

1. 找到与你的某个数据库实例相关的进程并停止它。
2. 观察 `gp_segment_configuration` 表是否发生变化。
3. 然后阅读 Coordinator 日志文件，再次检查 `gp_segment_configuration` 表。
4. 使用恢复工具修复故障 Segment。
5. 在 `gp_segment_configuration` 表中确认 Segment 已恢复。

## 第 9 课：设置并管理 Cloudberry 中的 Standby Coordinator 实例 {#lesson-9-set-up-and-manage-the-standby-coordinator-instance-in-cloudberry}

**了解 Standby Coordinator 的作用**

在 Cloudberry 架构中，Coordinator 实例可能成为单点故障。为避免这种情况，建议设置并维护一个“Standby Coordinator”实例。通常，该 Standby 实例设置在独立服务器上，这台服务器称为“Standby Coordinator 服务器”或“scdw”。

**管理 Standby Coordinator**

- 要创建 Standby Coordinator（在 Coordinator 服务器上执行），使用 `gpinitstandby -s scdw`。
- 如果 Standby Coordinator 失去同步，可以使用 `gpinitstandby -n` 重新同步。
- 要删除 Standby Coordinator，使用 `gpinitstandby -r`。

设置 Standby 实例后，可以查询 `gp_segment_configuration` 表。表输出中会显示新的 Standby 实例，其 `content` 值为 `-1`，`role` 值为 `'m'`。

**提升 Standby Coordinator**

如果 Coordinator 服务器或 Coordinator 实例不可用，Standby Coordinator 可以接替它。要将 Standby Coordinator 提升为 Coordinator 角色，请在 Standby 服务器上运行 `gpactivatestandby` 命令。

运行此命令后，角色会发生变化：Standby Coordinator 变为 Coordinator，而原 Coordinator 降级为 Standby 实例，尽管它仍处于离线状态。可以再次查询 `gp_segment_configuration` 表，观察这些变化。

**练习**

1. 创建 Standby Coordinator。
2. 删除 Standby Coordinator。
3. 再次创建 Standby Coordinator。
4. 激活该 Standby Coordinator，使其成为主 Coordinator。
5. 在原 Coordinator 服务器上创建另一个 Standby Coordinator。
6. 激活这个新的 Standby Coordinator。

在这些步骤中持续观察 `gp_segment_configuration` 表。这有助于理解角色以及各实例状态的变化。

## 第 10 课：扩容集群 {#lesson-10-expand-a-cluster}

如果需要扩容集群，可以使用 `gpexpand` 工具。你可以添加新主机，也可以向现有主机添加更多 Segment。

**扩容集群的步骤**

1. 运行 `gpexpand` 并回答问题。

    运行“gpexpand”。在此步骤中，系统会引导你回答要执行的操作。回答完所有问题后，工具会生成一个“配置文件”并停止。应当查看该文件，确认它执行的操作符合预期。

2. 运行 `gpexpand -i <config_file>` 为集群创建新实例。

    此步骤创建集群的新实例。这些新实例会显示在 `gp_segment_configuration` 表中。此时集群已经扩容，但新实例还没有用户数据。

    `gpexpand` 还会创建一个名为 `gpexpand` 模式的新区域。该区域列出下一步需要重分布的表。

3. 再次运行 `gpexpand`，重分布或扩散数据。

    此时，原先只位于旧实例中的数据会分布到扩容后的集群中。可以使用 `-d` 选项设置时间限制，多次执行此步骤。所有数据完成分布后，`gpexpand` 会停止。

4. 完成收尾。

    现在集群已经扩容，数据也已分布开。`gpexpand` 模式仍然存在，需要时可以查看它，不会造成问题。

    但是，如果要再次扩容集群，`gpexpand` 会要求先使用 `gpexpand -c` 删除该模式，然后才能继续。

**练习**

1. 运行 `gpexpand`，向当前服务器添加更多 Segment。
2. 再次运行 `gpexpand`，在新服务器上添加 Segment。
3. 查看 `gp_segment_configuration` 表，观察每次操作后它如何变化。

## 第 11 课：检查集群性能 {#lesson-11-check-cluster-performance}

可以使用 `gpcheckperf` 工具检查一组主机（集群）的性能。该工具可用于检查以下项目：

- 每台主机的 I/O 性能（使用 `-r -d` 选项）

    > 注意：gpcheckperf 将使用 `dd` 命令在每台主机上执行读测试和写测试。

- 网络性能（使用 `-r -n|N|M` 选项）

    > 注意：`-n` 表示串行；`-N` 表示在偶数台主机之间并行；`-M` 表示全矩阵模式。

- 每台主机的内存带宽测试（使用 `-r -s` 选项）

    > 注意：该工具使用 STREAM 基准测试程序测量可持续内存带宽（单位为 MB/s）。

**练习**

使用 `gpcheckcat` 的不同选项运行命令，并解释结果。

## 第 12 课：用户数据与表分布 {#lesson-12-user-data-and-table-distribution}

在 Cloudberry 中，Coordinator 实例不存储用户数据。用户数据存储在 Segment 上，Segment 之间不共享这些数据。

Cloudberry Database 的所有表都采用分布方式存储。创建或更改表时，可以选择指定 DISTRIBUTED BY（哈希分布）、DISTRIBUTED RANDOMLY（随机分布）或 DISTRIBUTED REPLICATED（完全复制），以确定表行的分布方式。

确定表分布策略时，请考虑以下几点。

- *数据均匀分布*——为了获得最佳性能，所有 Segment 都应包含相同份额的数据。如果数据不平衡或存在数据倾斜，数据量较大的 Segment 必须执行更多查询处理工作。应选择每条记录都唯一的分布键，例如主键。
- *本地操作与分布式操作*——本地操作比分布式操作快。如果在 Segment 层本地完成连接、排序或聚合操作，查询处理速度最快。在系统层完成工作需要在 Segment 之间分发元组，效率较低。如果表共享一个分布键，则可以在本地完成基于共享分布键列的连接或排序。采用随机分布策略时，无法执行本地连接操作。
- *查询处理均匀*——为了获得最佳性能，所有 Segment 都应承担相同份额的查询工作负载。如果表的数据分布策略与查询谓词不匹配，查询工作负载可能出现倾斜。例如，假设销售事务表按 customer ID 列（分布键）分布。如果查询谓词引用单个 customer ID，查询处理工作就会集中在一个 Segment 上。

复制表分布策略（DISTRIBUTED REPLICATED）只能用于小表。将数据复制到每个 Segment 会增加存储和维护成本，对大型事实表更是不可接受。复制表的主要使用场景是：

- 消除用户定义函数在 Segment 上可执行操作的限制；以及
- 通过无需将常用表广播到所有 Segment，提升查询性能。

在下面的示例中，如果表按哈希分布，可以看到 c1 列的值“1”始终位于同一个 Segment（gp_segment_id=1）上。

```
gpadmin=# create table t1 (c1 int) distributed by (c1);
CREATE TABLE

gpadmin=# insert into t1 values (1);
INSERT 0 1
gpadmin=# insert into t1 values (1);
INSERT 0 1
gpadmin=# insert into t1 values (1);
INSERT 0 1
gpadmin=# insert into t1 values (1);
INSERT 0 1

gpadmin=# select gp_segment_id, * from t1;
 gp_segment_id | c1
---------------+----
             1 |  1
             1 |  1
             1 |  1
             1 |  1
(4 rows)

```

在下面的示例中，如果表采用随机分布，可以看到 c1 列的值“1”随机分布在所有 Segment 上（gp_segment_id=0 和 gp_segment_id=1）。

```
gpadmin=# create table t2 (c1 int) distributed randomly;
CREATE TABLE

gpadmin=# insert into t2 values (1);
INSERT 0 1
gpadmin=# insert into t2 values (1);
INSERT 0 1
gpadmin=# insert into t2 values (1);
INSERT 0 1
gpadmin=# insert into t2 values (1);
INSERT 0 1

gpadmin=# select gp_segment_id, * from t2;
 gp_segment_id | c1
---------------+----
             0 |  1
             1 |  1
             1 |  1
             1 |  1
(4 rows)
```

练习：使用自己的表重现上述操作，并观察其效果。

## 第 13 课：数据库目录 {#lesson-13-database-catalog}

以 *gp_* 开头的系统表与 Cloudberry Database 的并行功能有关。以 *pg_* 开头的表，要么是 Cloudberry Database 支持的标准 PostgreSQL 系统目录表，要么与 Cloudberry 为增强 PostgreSQL 数据仓库工作负载而提供的功能有关。请注意，Cloudberry Database 的全局系统目录位于 Coordinator 实例上。

练习：运行以下查询，获取目录表名列表。

```
select tablename from pg_tables where schemaname='pg_catalog';
```

## 第 14 课：Cloudberry 数据目录 {#lesson-14-cloudberry-data-directories}

Coordinator 实例的数据目录位于 `/data0/database/coordinator/gpseg-1`。

以下是 Coordinator 实例数据目录中的内容：

```shell
[gpadmin@cdw gpseg-1]$ ls -tlr
```

```shell
total 156
-rw------- 1 gpadmin gpadmin     3 Aug 23 15:59 PG_VERSION
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_twophase
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_tblspc
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_snapshots
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_serial
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_replslot
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_notify
drwx------ 4 gpadmin gpadmin  4096 Aug 23 15:59 pg_multixact
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_dynshmem
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_cryptokeys
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_commit_ts
-rw------- 1 gpadmin gpadmin    88 Aug 23 15:59 postgresql.auto.conf
-rw------- 1 gpadmin gpadmin  1636 Aug 23 15:59 pg_ident.conf
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_xact
drwx------ 3 gpadmin gpadmin  4096 Aug 23 15:59 pg_wal
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_subtrans
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_distributedlog
-rw------- 1 gpadmin gpadmin 31760 Aug 23 15:59 postgresql.conf
-rw------- 1 gpadmin gpadmin    10 Aug 23 15:59 internal.auto.conf
-rw-rw-r-- 1 gpadmin gpadmin   860 Aug 23 15:59 gpssh.conf
drwx------ 6 gpadmin gpadmin  4096 Aug 23 15:59 base
-rw-rw-r-- 1 gpadmin gpadmin  4723 Aug 23 15:59 pg_hba.conf
-rw------- 1 gpadmin gpadmin    38 Aug 23 16:14 current_logfiles
-rw------- 1 gpadmin gpadmin   112 Aug 23 16:14 postmaster.opts
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:14 pg_stat
-rw------- 1 gpadmin gpadmin   130 Aug 23 16:14 gpsegconfig_dump
-rw------- 1 gpadmin gpadmin    88 Aug 23 16:14 postmaster.pid
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:14 log
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:14 global
drwx------ 4 gpadmin gpadmin  4096 Aug 23 16:39 pg_logical
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:44 pg_stat_tmp
```

Segment 实例的数据目录位于 `/data0/database/primary/gpseg0` 和 `/data0/database/primary/gpseg1`。以下是某个 Segment 实例数据目录中的内容：

```shell
[gpadmin@cdw gpseg-1]$ cd /data0/database/primary/gpseg0
[gpadmin@cdw gpseg0]$ ls -ltr
```

```shell
total 180
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_twophase
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_tblspc
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_snapshots
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_serial
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_notify
drwx------ 4 gpadmin gpadmin  4096 Aug 23 15:59 pg_multixact
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_dynshmem
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_cryptokeys
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_commit_ts
-rw------- 1 gpadmin gpadmin     3 Aug 23 15:59 PG_VERSION
-rw------- 1 gpadmin gpadmin  1636 Aug 23 15:59 pg_ident.conf
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_xact
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_subtrans
drwx------ 2 gpadmin gpadmin  4096 Aug 23 15:59 pg_distributedlog
-rw------- 1 gpadmin gpadmin 31637 Aug 23 15:59 postgresql.conf
-rw------- 1 gpadmin gpadmin    10 Aug 23 15:59 internal.auto.conf
-rw------- 1 gpadmin gpadmin  4915 Aug 23 16:03 pg_hba.conf
drwx------ 7 gpadmin gpadmin  4096 Aug 23 16:03 base
drwx------ 3 gpadmin gpadmin  4096 Aug 23 16:03 pg_replslot
drwx------ 3 gpadmin gpadmin  4096 Aug 23 16:03 pg_wal
-rw------- 1 gpadmin gpadmin   120 Aug 23 16:03 postgresql.auto.conf
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:14 log
-rw------- 1 gpadmin gpadmin    38 Aug 23 16:14 current_logfiles
-rw------- 1 gpadmin gpadmin   112 Aug 23 16:14 postmaster.opts
-rw------- 1 gpadmin gpadmin    89 Aug 23 16:14 postmaster.pid
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:14 pg_stat
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:29 global
drwx------ 4 gpadmin gpadmin  4096 Aug 23 16:44 pg_logical
-rw------- 1 gpadmin gpadmin 32768 Aug 23 16:44 fts_probe_file.bak
drwx------ 2 gpadmin gpadmin  4096 Aug 23 16:44 pg_stat_tmp
```

**练习**

查看数据目录及其子目录，并查看配置文件。

## 第 15 课：实例进程 {#lesson-15-instance-processes}

- postgres 进程：名称中包含数据目录（-D ...）的进程。该进程是所有其他数据库进程的父进程，负责处理到此实例的连接。

- logger 进程：将日志条目写入日志文件。

- stats collector 进程：统计信息收集器是支持收集和报告服务器活动信息的子系统。目前，该收集器可以按磁盘块和单行两种方式统计对表和索引的访问。

- background writer 进程：将“脏”（新建或已修改）缓冲区写入磁盘上的数据文件。

- sweeper 进程：与工作负载管理和优先级有关。

- checkpoint 进程：执行检查点。

- walwriter 进程：定期将 WAL 缓冲区刷写到磁盘。

- ftsprobe 进程：运行在 Coordinator 节点上，定期轮询 Segment 以维护每个 Segment 的状态。

- walsender 进程：运行在主 Segment 上，将 WAL 发送到镜像 Segment。

- walreceiver 进程：运行在镜像 Segment 上，从主 Segment 接收 WAL。

- conXXX：用户连接工作进程。

#### Coordinator 进程：{#coordinator-processes}

```
[gpadmin@cdw ~]$ ps aux|grep 5432
gpadmin   4409  0.0  0.4 209960 39776 ?        Ss   16:14   0:00 /usr/local/cloudberry/bin/postgres -D /data0/database/coordinator/gpseg-1 -p 5432 -c gp_role=dispatch
gpadmin   4410  0.0  0.0  45544  5160 ?        Ss   16:14   0:00 postgres:  5432, coordinator logger process
gpadmin   4412  0.0  0.1 210256  9484 ?        Ss   16:14   0:00 postgres:  5432, checkpointer
gpadmin   4413  0.0  0.0 210124  7440 ?        Ss   16:14   0:00 postgres:  5432, background writer
gpadmin   4414  0.0  0.1 210124 10304 ?        Ss   16:14   0:00 postgres:  5432, walwriter
gpadmin   4415  0.0  0.1 211544 12068 ?        Ss   16:14   0:00 postgres:  5432, autovacuum launcher
gpadmin   4416  0.0  0.0  45768  5672 ?        Ss   16:14   0:00 postgres:  5432, stats collector
gpadmin   4417  0.0  0.2 278596 22164 ?        Ssl  16:14   0:00 postgres:  5432, dtx recovery process
gpadmin   4418  0.0  0.2 278416 21624 ?        Ssl  16:14   0:00 postgres:  5432, ftsprobe process
gpadmin   4427  0.0  0.1 211492 11244 ?        Ss   16:14   0:00 postgres:  5432, logical replication launcher
gpadmin   4428  0.0  0.2 277792 17748 ?        Ssl  16:14   0:00 postgres:  5432, pg_cron launcher
gpadmin   4429  0.0  0.0 210124  5316 ?        Ss   16:14   0:00 postgres:  5432, sweeper process
gpadmin   4846  0.0  0.5 294692 48516 ?        Ssl  16:25   0:00 postgres:  5432, gpadmin gpadmin [local] con46 cmd172 idle
```

#### 主进程：{#primary-processes}

```
[gpadmin@cdw ~]$ ps aux|grep 40000
gpadmin   4373  0.0  0.5 212912 41404 ?        Ss   16:14   0:00 /usr/local/cloudberry/bin/postgres -D /data0/database/primary/gpseg0 -p 40000 -c gp_role=execute
gpadmin   4377  0.0  0.0  45540  5272 ?        Ss   16:14   0:00 postgres: 40000, logger process
gpadmin   4390  0.0  0.1 213212  9328 ?        Ss   16:14   0:00 postgres: 40000, checkpointer
gpadmin   4391  0.0  0.0 213076  7856 ?        Ss   16:14   0:00 postgres: 40000, background writer
gpadmin   4392  0.0  0.1 213076 10428 ?        Ss   16:14   0:00 postgres: 40000, walwriter
gpadmin   4393  0.0  0.1 213784  9948 ?        Ss   16:14   0:00 postgres: 40000, autovacuum launcher
gpadmin   4394  0.0  0.0  45768  5816 ?        Ss   16:14   0:00 postgres: 40000, stats collector
gpadmin   4395  0.0  0.0 213624  7984 ?        Ss   16:14   0:00 postgres: 40000, logical replication launcher
gpadmin   4396  0.0  0.0 212912  4480 ?        Ss   16:14   0:00 postgres: 40000, sweeper process
gpadmin   4400  0.0  0.1 214868 12432 ?        Ss   16:14   0:00 postgres: 40000, walsender gpadmin 172.17.0.2(37278) streaming 0/100F9088
```

#### 镜像进程：{#mirror-processes}

```
[gpadmin@cdw ~]$ ps aux|grep 41000
gpadmin   4375  0.0  0.5 212912 41196 ?        Ss   16:14   0:00 /usr/local/cloudberry/bin/postgres -D /data0/database/mirror/gpseg0 -p 41000 -c gp_role=execute
gpadmin   4379  0.0  0.0  45540  5160 ?        Ss   16:14   0:00 postgres: 41000, logger process
gpadmin   4383  0.0  0.1 213344 10908 ?        Ss   16:14   0:00 postgres: 41000, startup recovering 000000010000000000000004
gpadmin   4385  0.0  0.1 212912  8352 ?        Ss   16:14   0:00 postgres: 41000, checkpointer
gpadmin   4386  0.0  0.0 212912  6260 ?        Ss   16:14   0:00 postgres: 41000, background writer
gpadmin   4387  0.1  0.1 213788  9740 ?        Ss   16:14   0:04 postgres: 41000, walreceiver streaming 0/100F9088
```

练习：尝试识别集群中各实例的进程。

## 第 16 课：数据库日志文件 {#lesson-16-database-log-files}

每个实例都有自己的日志文件，位于 `<data_directory>/log` 目录中。

```shell
[gpadmin@cdw log]$ pwd

/data0/database/primary/gpseg0/log

[gpadmin@cdw log]$ ls -ltr

total 20
-rw------- 1 gpadmin gpadmin 8842 Aug 23 16:14 gpdb-2023-08-23_155951.csv
-rw------- 1 gpadmin gpadmin  468 Aug 23 16:14 startup.log
-rw------- 1 gpadmin gpadmin 3269 Aug 23 16:17 gpdb-2023-08-23_161424.csv
```

标准日志文件名为 `gpdb_<date>-<time>.csv`。

**练习**

查看日志文件，并在数据库中执行各种操作（创建表、运行查询等）。

## 第 17 课：Cloudberry 中的表类型：堆表、AO 表和 AOCO 表 {#lesson-17-table-types-in-cloudberry-heap-ao-and-aoco}

**堆表**

在 Cloudberry 中，标准表类型是“堆表”。这些表将行存储在页中，一个数据文件可以包含多个页。它们支持 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 和 `TRUNCATE` 等常见 SQL 操作。堆表中的每一行都有一个头部。不过，这些表不支持压缩。

**AO 表**

与堆表不同，AO 表没有行头部，但支持压缩。这一特性使 AO 表适合大型事实表。

**AOCO（列存）表**

对于只关注单列的任务（例如计算平均值（`AVG`）或总和），使用行存并不是理想选择。列存表按列存储数据，效率更高。这是因为查询一列时，不会受到其他列大小或数量的影响。

AOCO 表支持压缩，而且压缩效果甚至优于 AO 表。这是因为同一个文件中的数据类型一致，也就是说，单列中的所有数据类型相同。

**练习**

创建一个堆表、一个 AO 表和一个 AOCO 表。创建完成后，使用 `\d+ psql` 命令查看结果。

## 第 18 课：外部表 {#lesson-18-external-tables}

Cloudberry 支持外部表。这些表在数据库中定义，但链接到数据库外部的数据。表数据可以来自以下位置：

- 本地文件系统中的文件。
- 远程主机上的文件（需要为此使用 `gpfdist` 服务器）。
- HDFS，即 `gphdfs` 类型。
- 由命令即时生成的数据。

外部表的一个优点是可以轻松地将数据加载到 Cloudberry。当使用 `INSERT INTO table SELECT * FROM ext_table` 这样的命令时，数据会从不同部分一次性加载，而不是逐条加载。

**练习**

尝试创建不同类型的外部表并进行操作，以进一步了解它们。

## 第 19 课：工作负载管理 {#lesson-19-workload-management}

Cloudberry 中有一种称为资源队列（简称 RQ）的机制。可以将 RQ 看作一组需求相似且共享资源的会话。任何用户都可以加入 RQ。

此外还有一个名为 Priority 的功能。可以为整个 RQ 设置优先级，这意味着该 RQ 中的每个会话都具有这一优先级。如果需要，也可以使用 `gp_adjust_priority()` 函数只为一个会话设置优先级。

**练习**

创建一个用户，设置 RQ，将该用户加入 RQ，然后运行查询。观察 RQ 发生了什么。
