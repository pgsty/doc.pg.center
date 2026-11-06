---
title: "Apache Cloudberry 端口与协议"
linkTitle: "端口与协议"
description: "列出 Cloudberry 集群内部使用的网络端口和协议。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/ports-and-protocols.md"
---

Apache Cloudberry 客户端通过 TCP 连接到 Cloudberry Coordinator 实例的客户端连接端口，默认端口为 `5432`。可以在 postgresql.conf 配置文件中重新配置监听端口。客户端连接使用 PostgreSQL libpq API。`psql` 命令行接口、若干 Cloudberry 工具以及各编程语言的 API，都会直接使用 libpq 库，或在内部实现 `libpq` 协议。

每个 Segment 实例也有一个客户端连接端口，仅供 Coordinator 实例用于协调各 Segment 的数据库操作。在 Cloudberry Coordinator 上运行 `gpstate -p` 命令，可列出 Cloudberry Coordinator、主 Segment 和镜像 Segment 的端口分配情况。例如：

```shell
[gpadmin@cdw ~]$ gpstate -p 
20250516:02:57:04:011030 gpstate:cdw:gpadmin-[INFO]:-Starting gpstate with args: -p
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-local Cloudberry Version: 'postgres (Apache Cloudberry) 14.4 build commit:fc9a9d4cad8dd4037b9bc07bf837c0b958726103'
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-coordinator Cloudberry Version: 'PostgreSQL 14.4 (Apache Cloudberry 2.0.0 build commit:fc9a9d4cad8dd4037b9bc07bf837c0b958726103) on x86_64-pc-linux-gnu, compiled by GCC gcc (GCC) 10, 64-bit compiled on May 16 2025 15:26:34'
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:--Coordinator segment instance  /data/coordinator/gpseg-1  port = 5432
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:--Segment instance port assignments
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-----------------------------------
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   Host   Datadir                Port
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/primary/gpseg0   20000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/mirror/gpseg0    21000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/primary/gpseg1   20001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/mirror/gpseg1    21001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/primary/gpseg2   20002
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/mirror/gpseg2    21002
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/primary/gpseg3   20000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/mirror/gpseg3    21000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/primary/gpseg4   20001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/mirror/gpseg4    21001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw2   /data/primary/gpseg5   20002
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/mirror/gpseg5    21002
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/primary/gpseg6   20000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/mirror/gpseg6    21000
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/primary/gpseg7   20001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/mirror/gpseg7    21001
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw3   /data/primary/gpseg8   20002
20250516:02:57:05:011030 gpstate:cdw:gpadmin-[INFO]:-   sdw1   /data/mirror/gpseg8    21002
```

备用复制、Segment 镜像、统计信息收集以及 Segment 之间的数据交换等功能还会创建其他 Apache Cloudberry 网络连接。一些持久连接在数据库启动时建立，其他临时连接则在查询执行等操作期间创建。查询执行进程、数据移动和统计信息收集所使用的临时连接，会通过 TCP 和 UDP 协议使用 `1025` 至 `65535` 范围内的可用端口。

> [!NOTE] 注意
> 为避免初始化 Apache Cloudberry 时与其他应用程序发生端口冲突，不要将 Apache Cloudberry 端口设置在操作系统参数 `net.ipv4.ip_local_port_range` 指定的范围内。例如，如果 `net.ipv4.ip_local_port_range = 10000 65535`，可以将 Apache Cloudberry 的基础端口号设为该范围之外的值：
>
> ```shell
> PORT_BASE = 6000
> MIRROR_PORT_BASE = 7000
> ```

一些与 Apache Cloudberry 配合使用的附加产品和服务有额外的网络要求。下表列出了 Cloudberry 集群内部使用的端口和协议，也包括与 Apache Cloudberry 集成的服务和应用程序。

|服务|协议/端口|说明|
|-------|-------------|-----------|
|Coordinator SQL 客户端连接|TCP 5432，libpq|Cloudberry Coordinator 主机上的 SQL 客户端连接端口。支持使用 PostgreSQL libpq API 的客户端。可配置。|
|Segment SQL 客户端连接|端口不固定，libpq|Segment 实例的 SQL 客户端连接端口。同一主机上的每个主 Segment 和镜像 Segment 都必须有唯一的端口。端口在 Cloudberry 系统初始化或扩容时分配。`gp_segment_configuration` 系统目录在 `port` 列中记录各主 Segment（p）或镜像 Segment（m）的端口号。运行 `gpstate -p` 可查看正在使用的端口。|
|Segment 镜像端口|端口不固定，libpq|Segment 用于接收其主 Segment 发来的镜像数据块的端口。此端口在设置镜像时分配。`gp_segment_configuration` 系统目录在 `port` 列中记录各主 Segment（p）或镜像 Segment（m）的端口号。运行 `gpstate -p` 可查看正在使用的端口。|
|Apache Cloudberry Interconnect|UDP 1025-65535，动态分配|Interconnect 在查询执行期间负责在 Cloudberry Segment 之间传输数据库元组。|
|Standby Coordinator 客户端监听器|TCP 5432，libpq|Standby Coordinator 主机上的 SQL 客户端连接端口。通常与 Coordinator 的客户端连接端口相同。使用 `gpinitstandby` 工具的 `-P` 选项配置。|
|Standby Coordinator 复制进程|TCP 1025-65535，gpsyncmaster|Coordinator 主机上的 `gpsyncmaster` 进程与辅助 Coordinator 主机建立连接，将 Coordinator 的日志复制到 Standby Coordinator。|
|Apache Cloudberry 文件加载和传输工具：gpfdist、gpload。|TCP 8080，HTTP<br/>TCP 9000，HTTPS|gpfdist 文件服务工具可以在 Cloudberry 主机或外部主机上运行。启动服务器时，使用 `-p` 选项指定连接端口。<br/><br/>gpload 工具会运行一个或多个 gpfdist 实例，使用配置文件中指定的端口或端口范围。|
|备份完成通知|TCP 25、TCP 587，SMTP|`gpbackup` 备份工具可以在备份完成后向指定的电子邮件地址列表发送邮件。必须在 Cloudberry Coordinator 主机上启用 SMTP 服务。|
|Apache Cloudberry 安全 Shell（SSH）：gpssh、gpsync、gpssh-exkeys、gppkg|TCP 22，SSH|许多 Cloudberry 工具使用 rsync 和 ssh 在主机之间传输文件，并管理集群内的 Cloudberry 系统。|
|GPText|TCP 2188（基础端口）|ZooKeeper 客户端端口。ZooKeeper 使用从基础端口号开始的一段端口范围。基础端口号和最大端口号在安装时通过 GPText 安装配置文件设置。默认基础端口号为 2188。|
|GPText|TCP 18983（基础端口）|GPText（Apache Solr）节点。GPText 节点使用从基础端口号开始的一段端口范围。基础端口号和最大端口号在安装时通过 GPText 安装配置文件设置。默认基础端口号为 18983。|
|EMC Data Domain 和 DD Boost|TCP/UDP 111，NFS portmapper|用于为 NFS 和 DD Boost 使用的 mountd 服务分配随机端口。可以在 Data Domain 服务器上为 mountd 服务静态分配端口。|
|EMC Data Domain 和 DD Boost|TCP 2052|NFS mountd 使用的主端口。可以在 Data Domain 系统上使用 `nfs set mountd-port` 命令设置此端口。|
|EMC Data Domain 和 DD Boost|TCP 2049，NFS|NFS 使用的主端口。可以在 Data Domain 服务器上使用 `nfs set server-port` 命令配置此端口。|
|EMC Data Domain 和 DD Boost|TCP 2051，复制|在 Data Domain 系统上配置复制时使用。可以在 Data Domain 服务器上使用 `replication modify` 命令配置此端口。|
|Pgbouncer 连接池|TCP，libpq|pgbouncer 连接池运行在 libpq 客户端与 Cloudberry（或 PostgreSQL）数据库之间。虽然可以在 Cloudberry Coordinator 主机上运行 pgbouncer，但建议将其部署在 Cloudberry 集群之外的主机上。在单独的主机上运行时，pgbouncer 可以作为 Cloudberry Coordinator 主机的温备机制，切换到 Cloudberry 备用主机而无需客户端重新配置。在 `pgbouncer.ini` 配置文件中设置客户端连接端口，以及 Cloudberry Coordinator 主机的地址和端口。|
