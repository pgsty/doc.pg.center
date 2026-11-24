---
title: "pglogical 与 Spock 函数名对照"
description: "从 pglogical 2 移植到 Spock 时，用本表核对函数名称及对应功能。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/pgl-cheat-sheet.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



Spock 的函数名通常比 pglogical 的短。从 pglogical 2 移植集群或脚本时，几乎每个函数调用都要改名。下表列出相应的 Spock 函数。

对照版本为 pglogical 2.4.8 和 Spock 6.0.0。已有参考页的 Spock 函数均附链接。

## 节点 {#nodes}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_node()` | [`spock.node_create()`](/zh/pgedge/spock/reference/functions/spock-node-create/) |
| `pglogical.drop_node()` | [`spock.node_drop()`](/zh/pgedge/spock/reference/functions/spock-node-drop/) |
| `pglogical.alter_node_add_interface()` | [`spock.node_add_interface()`](/zh/pgedge/spock/reference/functions/spock-node-add-interface/) |
| `pglogical.alter_node_drop_interface()` | [`spock.node_drop_interface()`](/zh/pgedge/spock/reference/functions/spock-node-drop-interface/) |
| `pglogical.pglogical_node_info()` | [`spock.node_info()`](/zh/pgedge/spock/reference/functions/spock-node-info/) |
{.wide .expand}

## 订阅 {#subscriptions}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_subscription()` | [`spock.sub_create()`](/zh/pgedge/spock/reference/functions/spock-sub-create/) |
| `pglogical.drop_subscription()` | [`spock.sub_drop()`](/zh/pgedge/spock/reference/functions/spock-sub-drop/) |
| `pglogical.alter_subscription_interface()` | [`spock.sub_alter_interface()`](/zh/pgedge/spock/reference/functions/spock-sub-alter-interface/) |
| `pglogical.alter_subscription_disable()` | [`spock.sub_disable()`](/zh/pgedge/spock/reference/functions/spock-sub-disable/) |
| `pglogical.alter_subscription_enable()` | [`spock.sub_enable()`](/zh/pgedge/spock/reference/functions/spock-sub-enable/) |
| `pglogical.alter_subscription_add_replication_set()` | [`spock.sub_add_repset()`](/zh/pgedge/spock/reference/functions/spock-sub-add-repset/) |
| `pglogical.alter_subscription_remove_replication_set()` | [`spock.sub_remove_repset()`](/zh/pgedge/spock/reference/functions/spock-sub-remove-repset/) |
| `pglogical.show_subscription_status()` | [`spock.sub_show_status()`](/zh/pgedge/spock/reference/functions/spock-sub-show-status/) |
| `pglogical.show_subscription_table()` | [`spock.sub_show_table()`](/zh/pgedge/spock/reference/functions/spock-sub-show-table/) |
{.wide .expand}

## 复制集 {#replication-sets}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_replication_set()` | [`spock.repset_create()`](/zh/pgedge/spock/reference/functions/spock-repset-create/) |
| `pglogical.alter_replication_set()` | [`spock.repset_alter()`](/zh/pgedge/spock/reference/functions/spock-repset-alter/) |
| `pglogical.drop_replication_set()` | [`spock.repset_drop()`](/zh/pgedge/spock/reference/functions/spock-repset-drop/) |
| `pglogical.replication_set_add_table()` | [`spock.repset_add_table()`](/zh/pgedge/spock/reference/functions/spock-repset-add-table/) |
| `pglogical.replication_set_add_all_tables()` | [`spock.repset_add_all_tables()`](/zh/pgedge/spock/reference/functions/spock-repset-add-all-tables/) |
| `pglogical.replication_set_remove_table()` | [`spock.repset_remove_table()`](/zh/pgedge/spock/reference/functions/spock-repset-remove-table/) |
| `pglogical.replication_set_add_sequence()` | [`spock.repset_add_seq()`](/zh/pgedge/spock/reference/functions/spock-repset-add-seq/) |
| `pglogical.replication_set_add_all_sequences()` | [`spock.repset_add_all_seqs()`](/zh/pgedge/spock/reference/functions/spock-repset-add-all-seqs/) |
| `pglogical.replication_set_remove_sequence()` | [`spock.repset_remove_seq()`](/zh/pgedge/spock/reference/functions/spock-repset-remove-seq/) |
| `pglogical.show_repset_table_info()` | [`spock.repset_show_table()`](/zh/pgedge/spock/reference/functions/spock-repset-show-table/) |
{.wide .expand}

## 同步 {#synchronisation}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.alter_subscription_synchronize()` | [`spock.sub_alter_sync()`](/zh/pgedge/spock/reference/functions/spock-sub-alter-sync/) |
| `pglogical.alter_subscription_resynchronize_table()` | [`spock.sub_resync_table()`](/zh/pgedge/spock/reference/functions/spock-sub-resync-table/) |
| `pglogical.synchronize_sequence()` | [`spock.sync_seq()`](/zh/pgedge/spock/reference/functions/spock-sync-seq/) |
| `pglogical.wait_for_subscription_sync_complete()` | [`spock.sub_wait_for_sync()`](/zh/pgedge/spock/reference/functions/spock-sub-wait-for-sync/) |
| `pglogical.wait_for_table_sync_complete()` | [`spock.table_wait_for_sync()`](/zh/pgedge/spock/reference/functions/spock-table-wait-for-sync/) |
| `pglogical.wait_slot_confirm_lsn()` | [`spock.wait_slot_confirm_lsn()`](/zh/pgedge/spock/reference/functions/spock-wait-slot-confirm-lsn/) |
{.wide .expand}

## DDL、工具函数与版本信息 {#ddl-utilities-and-version-information}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.replicate_ddl_command()` | [`spock.replicate_ddl()`](/zh/pgedge/spock/reference/functions/spock-replicate-ddl/) |
| `pglogical.table_data_filtered()` | `spock.table_data_filtered()` |
| `pglogical.xact_commit_timestamp_origin()` | [`spock.xact_commit_timestamp_origin()`](/zh/pgedge/spock/reference/functions/spock-xact-commit-timestamp-origin/) |
| `pglogical.pglogical_gen_slot_name()` | [`spock.spock_gen_slot_name()`](/zh/pgedge/spock/reference/functions/spock-gen-slot-name/) |
| `pglogical_version()` | [`spock.spock_version()`](/zh/pgedge/spock/reference/functions/spock-version/) |
| `pglogical_version_num()` | [`spock.spock_version_num()`](/zh/pgedge/spock/reference/functions/spock-version-num/) |
| `pglogical_max_proto_version()` | [`spock.spock_max_proto_version()`](/zh/pgedge/spock/reference/functions/spock-max-proto-version/) |
| `pglogical_min_proto_version()` | [`spock.spock_min_proto_version()`](/zh/pgedge/spock/reference/functions/spock-min-proto-version/) |
{.wide .expand}

## 在 Spock 中没有对应项的函数 {#functions-with-no-spock-equivalent}

`pglogical.queue_truncate()` 没有对应函数。Spock 通过复制集的 `replicate_truncate` 选项控制是否复制 `TRUNCATE`，使用 [`spock.repset_create()`](/zh/pgedge/spock/reference/functions/spock-repset-create/) 或 [`spock.repset_alter()`](/zh/pgedge/spock/reference/functions/spock-repset-alter/) 设置。

## pglogical 中没有的 Spock 函数 {#spock-functions-with-no-pglogical-ancestor}

Spock 还提供 pglogical 中没有的函数，因此移植工作可能涉及改名之外的调整。完整列表见[函数参考](/zh/pgedge/spock/reference/)，包括 `spock.sync_event()`、`spock.wait_for_sync_event()`、`spock.repset_add_partition()`、`spock.sub_alter_options()` 和 `spock.sub_alter_skiplsn()`。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/pgl-cheat-sheet.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
