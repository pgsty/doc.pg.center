---
title: 大型数据库迁移
description: 介绍将大型 PostgreSQL 数据库迁移到 Microsoft Azure 上的 Citus 集群所需的步骤。
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-data-big?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

规模较大的环境可以使用 [Citus Warp](https://www.citusdata.com/blog/2017/12/08/citus-warp-pain-free-migrations/)、[Debezium](https://debezium.io/)、[Striim](https://www.striim.com/partners/striim-for-microsoft-azure/) 或 [Fivetran](https://www.fivetran.com) 等工具进行在线复制。这些工具可以将 PostgreSQL 源数据库中的变更流式传输到 Microsoft Azure 上的 `cloud_topic`。这就像应用自动写入两个数据库，而非一个数据库，同时具备完善的事务逻辑。

我们强烈建议在执行这一流程时，通过[提交支持请求](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest)联系我们。进行复制时，我们会通过虚拟私有云（VPC）对等互连或 IP 允许列表，将 Citus 集群的协调节点连接到现有数据库，然后开始复制。

开始复制前，需要完成以下步骤：

1. 在目标 Citus 集群上复制模式结构。
2. 在源数据库中启用逻辑复制。
3. 允许从 Citus 协调节点到源数据库的网络连接。
4. 联系我们开始复制。

## 复制模式 {#duplicate-schema}

将数据迁移到 Citus 的第一步是确保源端和目标端的模式完全匹配，至少所选迁移表必须如此。一种方法是在开发数据库（用于本地测试应用的 Citus 数据库）上运行 `pg_dump --schema-only`，然后在 Citus 协调节点上执行导出的内容。另一种方法是在目标数据库上运行应用的迁移脚本。

所有需要迁移的表都必须有主键，相应的目标表也必须有主键。唯一的区别是，如 `mt_schema_migration` 所述，目标表可以使用包含分布列的复合主键。

此外，务必在开始复制前将表分布到集群中，这样数据就不必全部容纳在协调节点上。

## 启用逻辑复制 {#enable-logical-replication}

Amazon RDS 等托管数据库需要通过修改服务器配置参数来启用复制。在 Amazon RDS 上，创建一个新的参数组，在其中设置 `rds.logical_replication = 1`，然后将其设为当前使用的参数组。这项变更需要重启数据库服务器才能生效，可以安排在下一个维护窗口执行。

如果自行管理 PostgreSQL，请将以下配置加入 postgresql.conf：

```shell
wal_level = logical
max_replication_slots = 5 # has to be > 0
max_wal_senders = 5       # has to be > 0
```

必须重启数据库，这些变更才会生效。

## 允许网络连接 {#open-access-for-network-connection}

确定目标协调节点的 IP 地址。使用 dig 查询主机名对应的 IP 地址：

```bash
dig +short <hostname> A
```

如果使用 Amazon RDS，请编辑数据库安全组的入站规则，添加一条自定义 TCP 规则：

协议<br> TCP

端口范围<br> 5432

来源<br> <citus ip>/32

这条规则将 Citus 协调节点的 IP 地址加入允许列表，使其能够建立入站连接。另一种方式是在双方的 VPC 之间建立对等互连。如有需要，我们可以协助配置。

## 开始复制 {#begin-replication}

在 Azure 门户中提交[支持工单](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest)联系我们。工程师会连接到数据库，执行初始数据库转储、创建复制槽并开始复制。迁移时可以按你的选择包含或排除特定表。

复制的第一阶段，如果数据库存在写入负载，PostgreSQL 的预写式日志（WAL）可能大幅增长。开始前，请确保源数据库有足够的磁盘空间。建议至少预留 100 GB 或磁盘总容量的 20%，以较大者为准。初始转储和恢复完成、复制开始后，数据库就能再次归档不再使用的 WAL 文件。

复制期间，**请密切关注源数据库的磁盘使用情况。** 如果源端和目标端的数据类型不匹配，或发生其他意外的模式变更，复制可能停滞。长时间停滞可能导致源端复制槽保留的数据无限增长，进而造成数据库崩溃。

考虑到复制可能停滞，我们强烈建议在复制期间尽量减少模式变更。如果必须进行影响较大的模式变更，就需要停止复制并重新开始。

进行影响较大的模式变更时，步骤如下：

1. 请支持工程师停止复制。
2. 修改源数据库的模式。
3. 修改目标数据库的模式。
4. 重新开始复制。

## 切换到 Citus，并停止与旧数据库的所有连接 {#switch-over-to-citus-and-stop-all-connections-to-old-database}

复制追上源数据库的当前状态后，还需要完成一件事。由于复制过程的特点，目标数据库上的序列值不会被正确更新。例如，为确保 `id` 列的序列值正确，需要在允许向目标数据库写入之前，手动调整序列值。

完成后，应用就可以连接新数据库了。我们不建议同时向源数据库和目标数据库写入。

应用切换到新数据库、源数据库不再发生任何变更后，请再次联系我们删除复制槽。至此，迁移完成。

## 相关内容 {#related-content}

- [数据迁移](/citus/migration/migration-data/)
- [使用 pg_dump 迁移小型数据库](/citus/migration/migration-data-small/)
- [迁移概述](/citus/migration/migration/)
