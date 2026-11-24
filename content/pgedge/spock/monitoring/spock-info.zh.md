---
title: "查询集群信息"
description: "查阅 spock 模式的信息表和视图，验证节点、订阅及复制集中的表。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/spock_info.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



下表列出 `spock` 模式中的信息表和视图。

| 表名 | 说明 |
|---------------------|----------------------------|
| `channel_table_stats` | 按订阅和表统计插入、更新、删除、冲突及增量列应用次数。列为 `subid`、`relid`、`sub_name`、`table_name`、`n_tup_ins`、`n_tup_upd`、`n_tup_del`、`n_conflict`、`n_dca`。 |
| `channel_summary_stats` | 按订阅汇总 `channel_table_stats` 中各表的指标。列为 `subid`、`sub_name`、`n_tup_ins`、`n_tup_upd`、`n_tup_del`、`n_conflict`、`n_dca`。 |
| `events` | 列出共享内存中的近期事件，如启停订阅、工作进程启动／停止／失败、提供方连接和扩展升级。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。列为 `event_id`、`event_time`、`event_type`、`severity`、`subscription_id`、`subscription_name`、`pid`、`lsn`、`detail`。 |
| `depend` | 内部依赖表，跟踪加入复制的表及行过滤条件等对象。删除对象时，也会将其移出跟踪。列为 `classid`、`objid`、`objsubid`、`refclassid`、`refobjid`、`refobjsubid`、`deptype`。 |
| `exception_log` | 记录复制中无法恢复的错误或冲突。列为 `remote_origin`、`remote_commit_ts`、`command_counter`、`retry_errored_at`、`remote_xid`、`local_origin`、`local_commit_ts`、`table_schema`、`table_name`、`operation`（取 `BEGIN`、`COMMIT`、`INSERT`、`UPDATE`、`DELETE` 或 `DDL`）、`local_tup`、`remote_old_tup`、`remote_new_tup`、`ddl_statement`、`ddl_user`、`error_message`。 |
| `exception_status` | 供 ACE 跟踪状态详情，Spock 内部不使用此表。列为 `remote_origin`、`remote_commit_ts`、`retry_errored_at`、`remote_xid`、`status`、`resolved_at`、`resolution_details`。 |
| `exception_status_detail` | 列为 `remote_origin`、`remote_commit_ts`、`command_counter`、`retry_errored_at`、`remote_xid`、`status`、`resolved_at`、`resolution_details`。 |
| `local_node` | 只有一行，保存本地节点的 `node_id` 和 `node_local_interface`。与前两张表连接即可只显示本地节点的信息。 |
| `local_sync_status` | 显示已加入订阅的关系（表）的同步状态。请求全量同步时显示所有表，限定具体表时只显示这些表。列为 `sync_kind`、`sync_subid`、`sync_nspname`、`sync_relname`、`sync_status`、`sync_statuslsn`。 |
| `node` | 每个复制节点一行，包含 `node_id`、`node_name`，可选字段为 `location`、`country` 和 `info`。 |
| `node_interface` | 每个节点接口一行。`if_id`、`if_name`、`if_nodeid` 和 `if_dsn` 描述节点接口及其连接信息。 |
| `node_status` | 一行汇总节点的版本、工作进程与订阅数量、复制槽保留的 WAL、复制延迟及最近事件的时间。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `peer_status` | 列出本节点已知的所有节点、其接口及将其变更传入本地的订阅。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `pii` | 可选表，用于登记含有个人身份信息（PII）的列。可登记模式、表名和列名，以便添加表到复制集时定义列过滤。列为 `id`、`pii_schema`、`pii_table`、`pii_column`。 |
| `progress` | 内部使用，跟踪复制进度，包括源节点、提交 LSN、提交时间戳以及来源节点当前的 WAL 插入位置。列为 `node_id`、`remote_node_id`、`remote_commit_ts`、`remote_commit_lsn`、`remote_insert_lsn`、`last_updated_ts`、`updated_by_decode`。 |
| `queue` | 供 AutoDDL、订阅或表同步以及原生序列同步在内部使用。列为 `queued_at`、`role`、`replication_sets`、`message_type`、`message`。 |
| `replication_set` | 每个复制集一行，包含 `set_id`、`set_nodeid`、`set_name` 及四个布尔列 `replicate_insert`、`replicate_update`、`replicate_delete`、`replicate_truncate`。初始的三行对应 `default`、`default_insert_only` 和 `ddl_sql` 复制集。 |
| `replication_set_seq` | 复制集中的每个序列一行，包含 `set_id` 和 `set_seqoid`。 |
| `replication_set_table` | 每个表在其所属复制集中各有一行，包含 `set_id`、`set_reloid`（表标识）、`set_att_list` 和 `set_row_filter`。后两列分别描述复制使用的列清单和行过滤条件。 |
| `replication_set_status` | 列出本地节点的复制集、各类操作的复制标志、每个复制集包含的表和序列数，以及使用它的订阅数。 |
| `resolutions` | 本节点每次处理冲突各占一行。列为 `id`、`node_name`、`log_time`、`relname`、`idxname`、`conflict_type`（如 `update_update`）、`conflict_resolution`（如 `keep_local`）、`local_origin`、`local_tuple`、`local_xid, local_timestamp`、`remote_origin`、`remote_tuple`、`remote_xid`、`remote_timestamp`、`remote_lsn`。 |
| `settings` | 显示 Spock 参数及复制依赖的核心参数，包括单位、来源和是否需要重启。 |
| `slot_status` | 显示当前数据库的各个 Spock 复制槽、对应 walsender、保留的 WAL 量及反馈延迟。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `sequence_state` | 保存原生序列同步的内部状态。列为 `seqoid`、`cache_size`、`last_value`。 |
| `subscription` | 每个订阅一行。列为 `sub_id`、`sub_name`、`sub_origin`、`sub_target`、`sub_origin_if`、`sub_target_if`、`sub_enabled`、`sub_slot_name`、`sub_replication_sets`（订阅包含的复制集数组）、`sub_forward_origins`、`sub_apply_delay`、`sub_force_text_transfer`、`sub_skip_lsn`（由 `spock.sub_alter_skiplsn` 设置的 `pg_lsn`）、`sub_skip_schema`（应用时跳过的模式数组）和 `sub_created_at`（创建订阅的时间戳）。 |
| `subscription_stats` | 返回各订阅的活动计数，包括工作进程启动和失败、提供方连接、已接收的消息与事务、元组及冲突计数，以及最近错误。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `subscription_status` | 每个订阅返回一行，包括配置、状态、应用工作进程、复制位置、延迟和最近错误。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `system_status` | 一行汇总主机和实例的磁盘空间、负载、连接、长事务和空闲事务、距事务 ID 回卷的年龄、数据库统计信息及 WAL 归档状态。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
| `table_sync_status` | 显示 `local_sync_status`，将 `sync_kind` 和 `sync_status` 转换为便于阅读的值。 |
| `tables` | 列出数据库中的表。包含 `relid`、`nspname`（模式）、`relname`（表名）及 `set_name`；未加入复制集时为 `null`。 |
| `worker_status` | 列出节点上的监督进程、管理进程、应用和同步工作进程及其状态，以及各进程服务的订阅或表。详见[监控节点](/zh/pgedge/spock/monitoring/node-monitoring/)。 |
{.wide .expand}

## 示例 {#examples}

以下示例演示如何查询信息表，监控和验证 Spock 复制集群。

### 验证双节点集群的 Spock 配置 {#validating-spock-configuration-for-a-two-node-cluster}

通过 Spock 扩展可以确认节点是否已创建、复制是否正在进行。

查询 `spock.node` 检查节点创建情况。结果为空表示尚未运行创建命令；出现一行说明已有节点。

查询 `spock.subscription` 检查订阅创建情况。空结果表示本节点尚未创建订阅；出现一行说明已存在订阅。

连接数据库服务器并查询 `spock.node`，可查看已配置节点的信息。

```json
select * from spock.node;
-[ RECORD 1 ]--------
node_id   | 673694252
node_name | n1
location  |
country   |
info  	|
-[ RECORD 2 ]--------
node_id   | 560818415
node_name | n2
location  |
country   |
info  	|
```

### 确认订阅是否可用 {#confirming-that-a-functioning-subscription-exists}

连接数据库服务器并查询 `spock.subscription`，可查看订阅信息。

```sql
select * from spock.subscription;
-[ RECORD 1 ]-----------+--------------------------------------------------
sub_id              	| 3293941396
sub_name            	| sub_n1n2
sub_origin          	| 560818415
sub_target          	| 673694252
sub_origin_if       	| 4043145508
sub_target_if       	| 1437190346
sub_enabled         	| t
sub_slot_name       	| spk_demo_n2_sub_n1n2
sub_replication_sets	| {default,default_insert_only,ddl_sql,demo_repset}
sub_forward_origins 	|
sub_apply_delay     	| 00:00:00
sub_force_text_transfer | f
```
订阅正在复制时，`sub_enabled` 为 `t`。该值表明订阅已启用；要确认当前确有数据流，还应查看订阅运行状态。

### 列出参与复制的表 {#listing-tables-that-are-part-of-a-replication-scenario}

连接数据库服务器并查询 `spock.replication_set_table`，可查看已加入复制集的表。

```sql
select * from spock.replication_set_table;
-[ RECORD 1 ]--+-----------------
set_id     	| 2403235102
set_reloid 	| pgbench_accounts
set_att_list   |
set_row_filter |
-[ RECORD 2 ]--+-----------------
set_id     	| 2403235102
set_reloid 	| pgbench_branches
set_att_list   |
set_row_filter |
-[ RECORD 3 ]--+-----------------
set_id     	| 2403235102
set_reloid 	| pgbench_tellers
set_att_list   |
set_row_filter |
```

### 列出未参与复制的表 {#listing-tables-that-are-not-part-of-a-replication-cluster}

查询 `spock.tables` 可找出尚未加入复制集的表。复制集名称为 `null` 时，表示该表不属于任何复制集。

```sql
select * from spock.tables where set_name is null;
-[ RECORD 1 ]-------------
relid	| 24846
nspname  | public
relname  | pgbench_history
set_name |
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/spock_info.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
