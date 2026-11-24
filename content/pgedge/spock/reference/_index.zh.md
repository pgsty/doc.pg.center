---
title: "Spock 函数参考"
description: "按用途查阅节点、复制集、订阅和监控函数。"
weight: 90
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/index.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: "函数参考"
icon: fa-solid fa-book-open
type: docs
translation_status: translated
translation_notice: en
---

Spock 扩展提供以下用户函数。

| 命令 | 说明 |
| --- | --- |
| **节点管理函数** | 可通过 Spock 接口动态添加或移除节点。 |
| spock.node_info | 返回调用此函数的节点信息。 |
| [spock.node_create](/zh/pgedge/spock/reference/functions/spock-node-create/) | 定义一个 Spock 节点。 |
| [spock.node_drop](/zh/pgedge/spock/reference/functions/spock-node-drop/) | 删除一个 Spock 节点。 |
| [node_add_interface](/zh/pgedge/spock/reference/functions/spock-node-add-interface/) | 为节点添加接口。 |
| [spock.node_drop_interface](/zh/pgedge/spock/reference/functions/spock-node-drop-interface/) | 删除节点接口。 |
| [spock.node_alter](/zh/pgedge/spock/reference/functions/spock-node-alter/) | 修改本节点的位置、国家或地区及其他信息。合并 `info`，并校验其中的 `tiebreaker` 值。 |
| [spock.node_refresh_info](/zh/pgedge/spock/reference/functions/spock-node-refresh-info/) | 刷新本地缓存中一个或所有对等节点的位置、国家或地区及其他信息。 |
| **复制集管理函数** | 复制集决定复制哪些表，以及各表的哪些操作。每个复制集可分别选择复制 `INSERT`、`UPDATE`、`DELETE` 和 `TRUNCATE`。一个表可以属于多个复制集，订阅方也可以订阅多个复制集。实际复制的表及操作取各集合的并集。安装时会创建三个复制集。`default` 复制表的所有变更。`default_insert_only` 只复制插入，适用于没有主键的表。`ddl_sql` 复制通过 `spock.replicate_ddl` 指定的模式变更。 |
| [spock.repset_create](/zh/pgedge/spock/reference/functions/spock-repset-create/) | 定义复制集。 |
| [spock.repset_alter](/zh/pgedge/spock/reference/functions/spock-repset-alter/) | 修改复制集。 |
| [repset_drop](/zh/pgedge/spock/reference/functions/spock-repset-drop/) | 删除复制集。 |
| [spock.repset_add_partition](/zh/pgedge/spock/reference/functions/spock-repset-add-partition/) | 将分区加入复制集。 |
| [spock.repset_remove_partition](/zh/pgedge/spock/reference/functions/spock-repset-remove-partition/) | 将分区从父表所在的复制集中移除。 |
| [spock.repset_add_table](/zh/pgedge/spock/reference/functions/spock-repset-add-table/) | 将表加入复制集。 |
| [spock.repset_add_all_tables](/zh/pgedge/spock/reference/functions/spock-repset-add-all-tables/) | 将已有的表全部加入复制集。 |
| [spock.repset_remove_table](/zh/pgedge/spock/reference/functions/spock-repset-remove-table/) | 从复制集中移除表。 |
| spock.repset_show_table |  |
| [spock.repset_add_seq](/zh/pgedge/spock/reference/functions/spock-repset-add-seq/) | 将序列加入复制集。 |
| [spock.repset_add_all_seqs](/zh/pgedge/spock/reference/functions/spock-repset-add-all-seqs/) | 将指定模式下的所有序列加入复制集。 |
| [spock.repset_remove_seq](/zh/pgedge/spock/reference/functions/spock-repset-remove-seq/) | 从复制集中移除序列。 |
| spock.sync_seq | 同步指定序列。 |
| **订阅管理函数** |  |
| [spock.sub_create](/zh/pgedge/spock/reference/functions/spock-sub-create/) | 创建订阅。 |
| [spock.sub_drop](/zh/pgedge/spock/reference/functions/spock-sub-drop/) | 删除订阅。 |
| [spock.sub_disable](/zh/pgedge/spock/reference/functions/spock-sub-disable/) | 暂停订阅并断开与提供方的连接。 |
| [spock.sub_enable](/zh/pgedge/spock/reference/functions/spock-sub-enable/) | 启用订阅。 |
| [spock.sub_add_repset](/zh/pgedge/spock/reference/functions/spock-sub-add-repset/) | 为订阅添加复制集。 |
| [spock.sub_remove_repset](/zh/pgedge/spock/reference/functions/spock-sub-remove-repset/) | 从订阅中移除复制集。 |
| [spock.sub_show_status](/zh/pgedge/spock/reference/functions/spock-sub-show-status/) | 显示订阅状态。 |
| [spock.sub_show_table](/zh/pgedge/spock/reference/functions/spock-sub-show-table/) | 显示订阅中的表。 |
| [spock.sub_alter_interface](/zh/pgedge/spock/reference/functions/spock-sub-alter-interface/) | 更改订阅使用的接口。 |
| [spock.sub_wait_for_sync](/zh/pgedge/spock/reference/functions/spock-sub-wait-for-sync/) | 等待订阅同步完成。 |
| spock.sub_alter_skiplsn | 跳过事务，直至指定 LSN。 |
| spock.sub_alter_sync | 同步所有缺失的表。 |
| [spock.sub_alter_options](/zh/pgedge/spock/reference/functions/spock-sub-alter-options/) | 在同一原子操作中更改一个或多个订阅选项。 |
| spock.sub_resync_table | 重新同步指定表。 |
| **其他管理函数** |  |
| [spock.table_wait_for_sync](/zh/pgedge/spock/reference/functions/spock-table-wait-for-sync/) | 等待指定表完成同步。 |
| [spock.replicate_ddl](/zh/pgedge/spock/reference/functions/spock-replicate-ddl/) | 复制指定的 DDL 语句。 |
| spock_version | 返回点分格式的 Spock 版本，例如 `4.0.10`。函数定义在 public 模式中，调用时省略 `spock.` 前缀。 |
| spock_version_num | 返回数值形式的 Spock 版本，例如 `40010`。函数定义在 public 模式中，调用时省略 `spock.` 前缀。 |
| spock.get_channel_stats | 返回元组传输统计。 |
| spock.get_apply_stats | 返回各订阅的活动计数，供 `spock.subscription_stats` 视图使用。 |
| spock.get_events | 返回节点近期事件，供 `spock.events` 视图使用。 |
| spock.get_monitor_summary | 返回 Spock 共享内存结构的容量和使用量。 |
| spock.get_pending_exceptions | 返回应用工作进程正按异常处理策略重试的事务。 |
| spock.get_system_info | 返回节点的主机、操作系统及版本信息。 |
| spock.get_slot_groups | 返回有关联 WAL 发送进程的复制槽组。 |
| spock.get_subscription_stats | 返回订阅的冲突计数（PostgreSQL 18 及更高版本）。 |
| spock.get_worker_status | 返回每个 Spock 工作进程槽的状态，供 `spock.worker_status` 视图使用。 |
| spock.get_country | 返回显式设置的国家或地区代码。未设置时返回 `??`。 |
| spock.lag_tracker | 列出复制槽及各槽的 commit_lsn 和 commit_timestamp。 |
| spock.repair_mode | 控制当前会话的出站复制。设为 `true` 时暂停复制语句（含 DDL），设为 `false` 时恢复。 |
| spock.replicate_ddl | 复制指定语句。 |
| spock.redact_dsn | 返回隐藏了密码的连接字符串。 |
| spock.reset_channel_stats | 重置通道统计。 |
| spock.reset_events | 清除 `spock.events` 中的事件历史。 |
| spock.reset_subscription_stats | 重置一个或全部订阅的活动计数及冲突计数。 |
| spock.report_section | 将查询结果排成对齐的文本表格，或每行显示为一个文本块。 |
| spock.node_report | 生成整份节点报告，含版本、配置及各监控视图。 |
| spock_max_proto_version | 返回当前构建支持的最高 Spock 原生协议版本。函数位于 public 模式，调用时省略 `spock.` 前缀。 |
| spock_min_proto_version | 返回当前构建向后兼容的最低协议版本。函数位于 public 模式，调用时省略 `spock.` 前缀。 |
| spock.table_data_filtered | 扫描指定表，返回符合指定复制集行过滤条件的行。用 `repset_add_table` 将表加入复制集时设置过滤条件。 |
| spock.terminate_active_transactions | 终止所有活动事务。 |
| spock.wait_slot_confirm_lsn | 等待指定复制槽的 `confirmed_flush_lsn` 达到目标位置。省略槽名时等待所有逻辑槽。 |
| spock.xact_commit_timestamp_origin | 返回指定事务的提交时间戳和复制源。 |
{.wide .expand}


- [管理函数](/zh/pgedge/spock/reference/gen-mgmt/)
- [节点管理](/zh/pgedge/spock/reference/node-mgmt/)
- [复制集管理](/zh/pgedge/spock/reference/repset-mgmt/)
- [订阅管理函数](/zh/pgedge/spock/reference/sub-mgmt/)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/index.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/).
