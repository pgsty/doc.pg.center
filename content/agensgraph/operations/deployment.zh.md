---
title: 部署
linkTitle: 部署
description: AgensGraph 服务端承载生产流量前需要决定什么。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/deployment.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


AgensGraph 服务端承载生产流量前需要决定什么。把软件装到机器上的步骤见[安装 AgensGraph](/zh/agensgraph/get-started/install/)；本页讨论围绕安装的选择。

## 平台 {#platforms}

AgensGraph 在 Linux 和 Windows 上构建并运行，在 macOS 上用于开发。大多数部署在 Linux 上。经过测试的发行版是 Rocky Linux、RHEL、Debian 和 Ubuntu 的当前版本。[容器镜像](/zh/agensgraph/get-started/install/#docker)基于 Debian trixie 和 bookworm、Rocky 9 和 10 以及 Alpine 构建。

AgensGraph 没有收窄 PostgreSQL 的平台支持，因此 [PostgreSQL 支持平台说明](https://www.postgresql.org/docs/18/installation-platform-notes.html)适用。

## 容量规划 {#sizing}

从数据出发，而不是从推荐表出发。

**内存是最重要的杠杆。** 图遍历按索引沿边进入分散页，因此是随机访问工作。缓存外的随机访问很慢。目标是让工作集放入操作系统缓存：查询走过的标签，加上它们的索引。按这个工作集为 `shared_buffers` 和 `effective_cache_size` 定容，方法见[配置](/zh/agensgraph/operations/configuration/#memory)。

查看你要处理的对象：

```sql
SELECT l.labname,
       pg_size_pretty(pg_total_relation_size(l.relid)) AS total
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
WHERE g.graphname = 'moviekb'
ORDER BY pg_total_relation_size(l.relid) DESC;
```

边标签通常是图中最大的对象，并带有三个自己的索引；为索引和行都预留空间。

**存储应是闪存。** 原因不是吞吐，而是随机读延迟。遍历的时间主要花在这里。它也会改变规划器配置——参见[配置](/zh/agensgraph/operations/configuration/#planner-settings-that-matter-for-traversal)中的 `random_page_cost`。

**对遍历来说，CPU 的重要性低于预期**，因为遍历大部分是串行的；**对面向整个标签的分析查询来说，重要性高于预期**，因为那些查询可以并行化。

任何真实负载的最低配置是 4 GB RAM。磁盘方面，要为数据、索引、WAL 和建索引所需空间预留容量。基础安装本身约需 2.5 GB。

## 首次启动前 {#before-the-first-start}

**用独立的非特权用户运行服务端。** 不用 root，也不用与应用共享的登录账户：

```shell
useradd --system --home /var/lib/agensgraph --shell /usr/sbin/nologin agens
```

**尽量把数据目录放在独立文件系统上**，这样它被填满时不会拖垮机器其余部分，也可以独立快照。

```shell
install -o agens -g agens -m 0700 -d /var/lib/agensgraph/18/data
sudo -u agens initdb -D /var/lib/agensgraph/18/data
```

`initdb` 要求数据目录模式为 0700 或 0750。在 PostgreSQL 18 上，它还默认启用数据页校验和——值得保留，也值得知道，因为以后升级进入这个集群时它会决定一个标志。参见[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/#step-2-initialize-the-new-cluster)。

**内核资源**很少需要调整。AgensGraph 像 PostgreSQL 9.3 以来一样，主共享内存使用匿名 mmap，只保留极小的 System V 段，因此旧的 `SHMMAX` 调优不再需要。仍可能造成问题的是内存受限主机上的 `vm.overcommit_memory` 和 OOM killer，以及连接很多的服务器上的打开文件限制。参考是 [PostgreSQL 内核资源章节](https://www.postgresql.org/docs/18/kernel-resources.html)。

## 用 systemd 运行 {#running-under-systemd}

单实例 unit：

```ini
[Unit]
Description=AgensGraph 2.18
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
User=agens
Group=agens
Environment=AGDATA=/var/lib/agensgraph/18/data
ExecStart=/usr/local/agensgraph/bin/postgres -D ${AGDATA}
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=120
OOMScoreAdjust=-900

[Install]
WantedBy=multi-user.target
```

直接启动 `postgres` 并使用 `Type=notify` 是 systemd 处理得最好的安排——它让 systemd 知道服务端何时真正接受连接，也让 `systemctl stop` 执行干净关闭。`OOMScoreAdjust` 让内核优先终止后端进程而不是 postmaster。

临时工作用 `ag_ctl`，服务用 systemd。混合使用——手动启动再用 systemd 停止——是产生过期 postmaster 的典型原因。

## 连接 {#connections}

`initdb` 后，**`listen_addresses`** 是 `localhost`。请有意识地扩大它，且必须与下面的认证规则一起调整。

**`max_connections`** 默认 100。每个连接都有内存代价，而图查询可能同时使用多个 `work_mem` 分配，因此调高它并非免费。如果应用打开大量短连接，请在它前面放连接池；AgensGraph 使用 PostgreSQL 协议，PgBouncer 和 Pgpool-II 无需修改即可工作。

**认证**由 `pg_hba.conf` 决定；本地连接默认的 `trust` 不应保留。参见[安全](/zh/agensgraph/operations/security/)。

## 复制与高可用 {#replication-and-high-availability}

流复制、逻辑复制和同步提交都能用于图，因为图就是表，WAL 不知道区别。因此备库无需额外配置即可携带图数据，只读图查询也可以在热备上运行。

有两个 AgensGraph 相关注意事项：

* 图写入不并行化，因此写密集图负载在主库上每条语句使用的核心不会超过一个。这影响写吞吐的规划，不影响复制行为。
* 提升备库后，或任何物理恢复后，检查 `ag_graph.graphmeta_valid`；如果为 false，运行 `regather_graphmeta()`——参见[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)。

Patroni 是自动故障转移的常用选择，与 AgensGraph 的配合方式和 PostgreSQL 相同。

## 生产前清单 {#a-pre-production-checklist}

* 已按[配置](/zh/agensgraph/operations/configuration/)检查 `postgresql.conf`，特别是 `shared_buffers`、`work_mem`、`effective_cache_size` 和 `random_page_cost`。
* `pg_hba.conf` 没有 `trust` 规则，`listen_addresses` 不超过必要范围。
* 备份已运行，并按[备份与恢复](/zh/agensgraph/operations/backup/#what-to-check)测试过恢复，包括图计数。
* 如果不能接受丢失最近写入，WAL 归档已开启。
* 已设置 `log_min_duration_statement` 并加载 `auto_explain`，慢查询会留下证据。
* 已监控连接数、复制延迟、缓存命中率 和磁盘余量。
* `autovacuum` 保持开启。边标签会频繁变更；关闭 autovacuum 会让图数据库得到一张两倍于数据的表。
* 有意识地决定 `auto_gather_graphmeta`：开启，每次写入付出少量代价换取规划器扫描裁剪；或关闭，按计划重新收集。
* 检查边标签的统计目标，特别是集群从 2.17 升级而来——参见[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/#step-6-post-upgrade-tasks)。
