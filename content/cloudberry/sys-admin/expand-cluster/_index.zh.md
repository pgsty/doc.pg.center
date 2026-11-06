---
title: "扩容 Cloudberry 系统"
linkTitle: "集群扩容"
description: "通过向系统添加主机来扩展 Apache Cloudberry 系统，以提高性能和存储容量。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/expand-a-db-system.md"
---

通常，向 Cloudberry 集群添加节点可以使性能和存储容量线性扩展。

随着数据不断收集以及现有数据的保留期延长，数据仓库通常会逐渐增长。有时，为了将不同的数据仓库整合到一个数据库中，需要增加数据库容量。为适应新增加的分析项目，也可能需要额外的计算能力（CPU）。系统初始规格设计时，为增长预留容量是明智的做法，但通常不可能在资源真正需要很久以前就投入资源。因此，应预期定期执行数据库扩容项目。

由于 Cloudberry 采用 MPP 架构，向系统添加资源后，系统的容量和性能会达到如同最初就配置了这些资源时的水平。与需要长时间停机以转储和恢复数据的数据仓库系统不同，扩容 Apache Cloudberry 是一个分阶段进行、停机时间很短的过程。在重新分布数据期间，常规和临时工作负载可以继续运行，同时保持事务一致性。管理员可以根据正在进行的运维安排分布活动，并按需暂停和恢复。还可以为表排序，使数据集按优先顺序重新分布，从而让关键工作负载更早受益于扩容后的容量，或释放重新分布超大型表所需的磁盘空间。

扩容过程使用标准 Apache Cloudberry 操作，因此对管理员透明，也便于排查问题。Segment 镜像和现有的复制机制仍保持活动状态，因此容错能力不受损害，灾难恢复措施也继续有效。

- **[系统扩容概述](/cloudberry/sys-admin/expand-cluster/)**
可以在停机时间很短的情况下扩容 Apache Cloudberry，添加 Segment 实例和 Segment 主机。通常，向 Cloudberry 集群添加节点可以使性能和存储容量线性扩展。
- **[规划 Cloudberry 系统扩容](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)**
周密规划有助于确保 Cloudberry 扩容项目成功。
- **[准备并添加主机](/cloudberry/sys-admin/expand-cluster/prepare-and-add-hosts/)**
验证新主机系统已准备好集成到现有 Cloudberry 系统中。
- **[初始化新 Segment](/cloudberry/sys-admin/expand-cluster/initialize-new-segments/)**
使用 `gpexpand` 工具创建并初始化新的 Segment 实例，并创建扩容模式。
- **[重分布表](/cloudberry/sys-admin/expand-cluster/redistribute-tables/)**
重新分布表，使现有数据在扩容后的集群中保持平衡。
- **[扩容后任务](/cloudberry/sys-admin/expand-cluster/post-expansion-tasks/)**
扩容完成后，必须根据环境执行不同的任务。
