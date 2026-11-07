---
title: Spock Functions
description: 'The following user functions are available via the Spock extension:'
weight: 90
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Functions
icon: fa-solid fa-book-open
type: docs
---



The following user functions are available via the Spock extension:

| Command  | Description |
|----------|-------------|
| **Node Management Functions** | You can add and remove nodes dynamically using Spock interfaces.|
| spock.node_info | Returns information about the node on which the function is invoked. |
| [spock.node_create](/pgedge/spock/reference/functions/spock-node-create/) | Define a node for spock. |
| [spock.node_drop](/pgedge/spock/reference/functions/spock-node-drop/) | Remove a spock node. |
| [node_add_interface](/pgedge/spock/reference/functions/spock-node-add-interface/) | Add a new node interface. |
| [spock.node_drop_interface](/pgedge/spock/reference/functions/spock-node-drop-interface/) | Delete a node interface. |
| [spock.node_alter](/pgedge/spock/reference/functions/spock-node-alter/) | Change this node's own location, country, and/or info (merging info), validating a tiebreaker if one is set. |
| [spock.node_refresh_info](/pgedge/spock/reference/functions/spock-node-refresh-info/) | Refresh this node's cached copy of a peer's (or every peer's) location, country, and info. |
| **Replication Set Management Functions** | Replication sets provide a mechanism to control which tables in the database will be replicated and which actions on those tables will be replicated.  Each replicated set can specify individually if `INSERTs`, `UPDATEs`, `DELETEs` and `TRUNCATEs` on the set are replicated. Each table can be in multiple replication sets, and each subscriber can subscribe to multiple replication sets. The resulting set of tables and actions replicated is the union of the sets the table is in. Spock installation creates three replication sets: `default`, `default_insert_only` and `ddl_sql`. The `default` replication set is defined to replicate all changes to tables in it. The `default_insert_only` replication set only replicates `INSERT` statements, and is meant for use by tables that don't have primary key. The `ddl_sql` replication set is defined to replicate schema changes specified by `spock.replicate_ddl`. |
| [spock.repset_create](/pgedge/spock/reference/functions/spock-repset-create/) | Define a replication set. |
| [spock.repset_alter](/pgedge/spock/reference/functions/spock-repset-alter/) | Modify a replication set. |
| [repset_drop](/pgedge/spock/reference/functions/spock-repset-drop/) | Remove a replication set. |
| [spock.repset_add_partition](/pgedge/spock/reference/functions/spock-repset-add-partition/) | Add a partition to a replication set. |
| [spock.repset_remove_partition](/pgedge/spock/reference/functions/spock-repset-remove-partition/) | Remove a partition from the replication set that the parent table is a part of. |
| [spock.repset_add_table](/pgedge/spock/reference/functions/spock-repset-add-table/) | Add table(s) to replication set. |
| [spock.repset_add_all_tables](/pgedge/spock/reference/functions/spock-repset-add-all-tables/) | Add all existing table(s) to the replication set. |
| [spock.repset_remove_table](/pgedge/spock/reference/functions/spock-repset-remove-table/) | Remove table from replication set. |
| spock.repset_show_table | |
| [spock.repset_add_seq](/pgedge/spock/reference/functions/spock-repset-add-seq/) | Adds a sequence to a replication set. |
| [spock.repset_add_all_seqs](/pgedge/spock/reference/functions/spock-repset-add-all-seqs/) | Adds all sequences from the specified schemas to a replication set. |
| [spock.repset_remove_seq](/pgedge/spock/reference/functions/spock-repset-remove-seq/) | Remove a sequence from a replication set. |
| spock.sync_seq | Synchronize the specified sequence. |
| **Subscription Management Functions** | |
| [spock.sub_create](/pgedge/spock/reference/functions/spock-sub-create/) | Create a subscription. |
| [spock.sub_drop](/pgedge/spock/reference/functions/spock-sub-drop/) | Delete a subscription. |
| [spock.sub_disable](/pgedge/spock/reference/functions/spock-sub-disable/) | Put a subscription on hold, and disconnect from the provider. |
| [spock.sub_enable](/pgedge/spock/reference/functions/spock-sub-enable/) | Make a subscription live. |
| [spock.sub_add_repset](/pgedge/spock/reference/functions/spock-sub-add-repset/) | Add a replication set to a subscription. |
| [spock.sub_remove_repset](/pgedge/spock/reference/functions/spock-sub-remove-repset/) | Drop a replication set from a subscription. |
| [spock.sub_show_status](/pgedge/spock/reference/functions/spock-sub-show-status/) | Display the status of the subcription. |
| [spock.sub_show_table](/pgedge/spock/reference/functions/spock-sub-show-table/) | Show subscription tables. |
| [spock.sub_alter_interface](/pgedge/spock/reference/functions/spock-sub-alter-interface/) | Modify an interface to a subscription. |
| [spock.sub_wait_for_sync](/pgedge/spock/reference/functions/spock-sub-wait-for-sync/) | Pause until the subscription is synchronized. |
| spock.sub_alter_skiplsn | Skip transactions until the specified lsn. |
| spock.sub_alter_sync | Synchronize all missing tables. |
| [spock.sub_alter_options](/pgedge/spock/reference/functions/spock-sub-alter-options/) | Change one or more subscription options in a single atomic operation. |
| spock.sub_resync_table | Synchronize a specific table. |
| **Miscellaneous Management Functions** | |
| [spock.table_wait_for_sync](/pgedge/spock/reference/functions/spock-table-wait-for-sync/) | Pause until a table finishes synchronizing. |
| [spock.replicate_ddl](/pgedge/spock/reference/functions/spock-replicate-ddl/) | Enable DDL replication. |
| spock_version | Returns the Spock version in a major/minor version form: `4.0.10`. Defined in the public schema so invoked without the `spock.` prefix. |
| spock_version_num | Returns the Spock version in a single numeric form: `40010`. Defined in the public schema so invoked without the `spock.` prefix. |
| spock.get_channel_stats | Returns tuple traffic statistics. |
| spock.get_apply_stats | Returns the activity counters of every subscription; the source of the `spock.subscription_stats` view. |
| spock.get_events | Returns the recent events of the node; the source of the `spock.events` view. |
| spock.get_monitor_summary | Returns capacity and usage of the spock shared memory structures. |
| spock.get_pending_exceptions | Returns the transactions apply workers are retrying under exception handling. |
| spock.get_system_info | Returns host, operating system and version information of the node. |
| spock.get_slot_groups | Returns the slot groups with attached walsenders. |
| spock.get_subscription_stats | Returns the conflict counters of a subscription (PostgreSQL 18 and later). |
| spock.get_worker_status | Returns every spock worker slot; the source of the `spock.worker_status` view. |
| spock.get_country | Returns the country code if explicitly set; returns `??` if not set. |
| spock.lag_tracker | Returns a list of slots, with commit_lsn and commit_timestamp for each. |
| spock.repair_mode | Used to manage the state of replication - If set to `true`, stops replicating statements, including DDL; when `false`, resumes replication. |
| spock.replicate_ddl | Replicate a specific statement. |
| spock.redact_dsn | Returns a connection string with its password hidden. |
| spock.reset_channel_stats | Reset the channel statistics. |
| spock.reset_events | Clears the event history shown by `spock.events`. |
| spock.reset_subscription_stats | Resets the activity and conflict counters of one subscription, or of all subscriptions. |
| spock.report_section | Renders the rows of a query as an aligned text table or as one block per row. |
| spock.node_report | Returns the whole node as a text report: versions, settings and every monitoring view. |
| spock_max_proto_version | The highest Spock native protocol supported by the current binary/build. Defined in the public schema so invoked without the `spock.` prefix. |
| spock_min_proto_version | The lowest build for which this Spock binary is backward compatible. Defined in the public schema so invoked without the `spock.` prefix. |
| spock.table_data_filtered | Scans the specified table and returns rows that match the row filter from the specified replication set(s).  Row filters are added to a replication set when adding a table with `repset_add_table`. |
| spock.terminate_active_transactions | Terminates all active transactions. |
| spock.wait_slot_confirm_lsn | Wait for the `confirmed_flush_lsn` of the specified slot, or all logical slots if none given. |
| spock.xact_commit_timestamp_origin | Returns the commit timestamp and origin of the specified transaction. |
{.wide .expand}

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
