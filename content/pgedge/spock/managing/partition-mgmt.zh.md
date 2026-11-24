---
title: 复制分区表
description: 说明 Spock 如何复制分区表，以及如何把新增分区加入复制集。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/partition_mgmt.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



默认情况下，把分区表加入 Spock 复制集时，Spock 会包含该分区表当前的所有分区。如果之后再对表分区，或向分区表添加分区，需要使用 [`spock.repset_add_partition`](/zh/pgedge/spock/reference/functions/spock-repset-add-partition/) 函数把它们加入复制集。与非分区表一样，订阅方必须已有对应分区表及各分区的定义。

从复制集移除分区表时，默认也会移除该表的分区。应使用 [`spock.repset_remove_partition`](/zh/pgedge/spock/reference/functions/spock-repset-remove-partition/) 更新集群元数据。

分区表复制与普通表略有不同。初始同步期间，我们查询分区表（父表）获取所有需要同步的行，而不单独同步各个分区。数据完成初始同步后，恢复正常操作，分区开始像普通表一样复制。

如果把各分区单独加入复制集，它们会像普通表一样复制到每个订阅方的同名表。提供方与订阅方的分区定义相同时，这种方式无须在每次同步时执行分区路由，性能更好。


> [!NOTE]
>
> 初始集群设置和同步期间，表分区不会直接同步。父表会从源同步所有分区的数据；目标端在保留表结构的同时正确填充各个分区。在初始同步期间，这一分区行为等同于为单个分区设置 `synchronize_data = false`。
>
> 设置完成（初始同步结束）后，父表和分区都会受到修改监控，变更会在发生时复制。
>

通过分区表复制分区时，`TRUNCATE` 命令总是会复制到所有受影响的表或分区。


> [!NOTE]
>
> 可以对分区表以及单个分区使用 `row_filter` 子句。


---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/partition_mgmt.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
