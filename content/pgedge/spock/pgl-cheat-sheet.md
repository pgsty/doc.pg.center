---
title: pglogical to Spock function names
description: Spock's function names are shorter than pglogical's, so a cluster or a script being ported from pglogical
  2 needs almost every call renamed.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/pgl-cheat-sheet.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



Spock's function names are shorter than pglogical's, so a cluster or a
script being ported from pglogical 2 needs almost every call renamed. This
page maps each pglogical function to its Spock equivalent.

Verified against pglogical 2.4.8 and Spock 6.0.0. Where a Spock function has
a reference page, its name links to it.

## Nodes {#nodes}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_node()` | [`spock.node_create()`](/pgedge/spock/reference/functions/spock-node-create/) |
| `pglogical.drop_node()` | [`spock.node_drop()`](/pgedge/spock/reference/functions/spock-node-drop/) |
| `pglogical.alter_node_add_interface()` | [`spock.node_add_interface()`](/pgedge/spock/reference/functions/spock-node-add-interface/) |
| `pglogical.alter_node_drop_interface()` | [`spock.node_drop_interface()`](/pgedge/spock/reference/functions/spock-node-drop-interface/) |
| `pglogical.pglogical_node_info()` | [`spock.node_info()`](/pgedge/spock/reference/functions/spock-node-info/) |
{.wide .expand}

## Subscriptions {#subscriptions}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_subscription()` | [`spock.sub_create()`](/pgedge/spock/reference/functions/spock-sub-create/) |
| `pglogical.drop_subscription()` | [`spock.sub_drop()`](/pgedge/spock/reference/functions/spock-sub-drop/) |
| `pglogical.alter_subscription_interface()` | [`spock.sub_alter_interface()`](/pgedge/spock/reference/functions/spock-sub-alter-interface/) |
| `pglogical.alter_subscription_disable()` | [`spock.sub_disable()`](/pgedge/spock/reference/functions/spock-sub-disable/) |
| `pglogical.alter_subscription_enable()` | [`spock.sub_enable()`](/pgedge/spock/reference/functions/spock-sub-enable/) |
| `pglogical.alter_subscription_add_replication_set()` | [`spock.sub_add_repset()`](/pgedge/spock/reference/functions/spock-sub-add-repset/) |
| `pglogical.alter_subscription_remove_replication_set()` | [`spock.sub_remove_repset()`](/pgedge/spock/reference/functions/spock-sub-remove-repset/) |
| `pglogical.show_subscription_status()` | [`spock.sub_show_status()`](/pgedge/spock/reference/functions/spock-sub-show-status/) |
| `pglogical.show_subscription_table()` | [`spock.sub_show_table()`](/pgedge/spock/reference/functions/spock-sub-show-table/) |
{.wide .expand}

## Replication sets {#replication-sets}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.create_replication_set()` | [`spock.repset_create()`](/pgedge/spock/reference/functions/spock-repset-create/) |
| `pglogical.alter_replication_set()` | [`spock.repset_alter()`](/pgedge/spock/reference/functions/spock-repset-alter/) |
| `pglogical.drop_replication_set()` | [`spock.repset_drop()`](/pgedge/spock/reference/functions/spock-repset-drop/) |
| `pglogical.replication_set_add_table()` | [`spock.repset_add_table()`](/pgedge/spock/reference/functions/spock-repset-add-table/) |
| `pglogical.replication_set_add_all_tables()` | [`spock.repset_add_all_tables()`](/pgedge/spock/reference/functions/spock-repset-add-all-tables/) |
| `pglogical.replication_set_remove_table()` | [`spock.repset_remove_table()`](/pgedge/spock/reference/functions/spock-repset-remove-table/) |
| `pglogical.replication_set_add_sequence()` | [`spock.repset_add_seq()`](/pgedge/spock/reference/functions/spock-repset-add-seq/) |
| `pglogical.replication_set_add_all_sequences()` | [`spock.repset_add_all_seqs()`](/pgedge/spock/reference/functions/spock-repset-add-all-seqs/) |
| `pglogical.replication_set_remove_sequence()` | [`spock.repset_remove_seq()`](/pgedge/spock/reference/functions/spock-repset-remove-seq/) |
| `pglogical.show_repset_table_info()` | [`spock.repset_show_table()`](/pgedge/spock/reference/functions/spock-repset-show-table/) |
{.wide .expand}

## Synchronisation {#synchronisation}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.alter_subscription_synchronize()` | [`spock.sub_alter_sync()`](/pgedge/spock/reference/functions/spock-sub-alter-sync/) |
| `pglogical.alter_subscription_resynchronize_table()` | [`spock.sub_resync_table()`](/pgedge/spock/reference/functions/spock-sub-resync-table/) |
| `pglogical.synchronize_sequence()` | [`spock.sync_seq()`](/pgedge/spock/reference/functions/spock-sync-seq/) |
| `pglogical.wait_for_subscription_sync_complete()` | [`spock.sub_wait_for_sync()`](/pgedge/spock/reference/functions/spock-sub-wait-for-sync/) |
| `pglogical.wait_for_table_sync_complete()` | [`spock.table_wait_for_sync()`](/pgedge/spock/reference/functions/spock-table-wait-for-sync/) |
| `pglogical.wait_slot_confirm_lsn()` | [`spock.wait_slot_confirm_lsn()`](/pgedge/spock/reference/functions/spock-wait-slot-confirm-lsn/) |
{.wide .expand}

## DDL, utilities and version information {#ddl-utilities-and-version-information}

| pglogical 2.4 | Spock 6.0 |
| --- | --- |
| `pglogical.replicate_ddl_command()` | [`spock.replicate_ddl()`](/pgedge/spock/reference/functions/spock-replicate-ddl/) |
| `pglogical.table_data_filtered()` | `spock.table_data_filtered()` |
| `pglogical.xact_commit_timestamp_origin()` | [`spock.xact_commit_timestamp_origin()`](/pgedge/spock/reference/functions/spock-xact-commit-timestamp-origin/) |
| `pglogical.pglogical_gen_slot_name()` | [`spock.spock_gen_slot_name()`](/pgedge/spock/reference/functions/spock-gen-slot-name/) |
| `pglogical_version()` | [`spock.spock_version()`](/pgedge/spock/reference/functions/spock-version/) |
| `pglogical_version_num()` | [`spock.spock_version_num()`](/pgedge/spock/reference/functions/spock-version-num/) |
| `pglogical_max_proto_version()` | [`spock.spock_max_proto_version()`](/pgedge/spock/reference/functions/spock-max-proto-version/) |
| `pglogical_min_proto_version()` | [`spock.spock_min_proto_version()`](/pgedge/spock/reference/functions/spock-min-proto-version/) |
{.wide .expand}

## Functions with no Spock equivalent {#functions-with-no-spock-equivalent}

`pglogical.queue_truncate()` has no counterpart. Spock controls whether
`TRUNCATE` replicates with the replication set's `replicate_truncate`
option, set with [`spock.repset_create()`](/pgedge/spock/reference/functions/spock-repset-create/)
or [`spock.repset_alter()`](/pgedge/spock/reference/functions/spock-repset-alter/),
rather than with a function call.

## Spock functions with no pglogical ancestor {#spock-functions-with-no-pglogical-ancestor}

Spock adds functions that pglogical never had, so a port is not finished when
the last name in the table above has been changed. See the
[function list](/pgedge/spock/reference/) for the full set; the additions
include `spock.sync_event()`, `spock.wait_for_sync_event()`,
`spock.repset_add_partition()`, `spock.sub_alter_options()` and
`spock.sub_alter_skiplsn()`.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/pgl-cheat-sheet.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
