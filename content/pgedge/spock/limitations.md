---
title: Limitations and Restrictions
description: Spock has several limitations and restrictions that users should be aware of when designing and implementing
  replication scenarios.
weight: 110
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/limitations.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Limitations
type: docs
---



Spock has several limitations and restrictions that users should be aware of
when designing and implementing replication scenarios.

## Superuser Privileges Are Required {#superuser-privileges-are-required}

Currently, the Spock extension requires superuser privileges to configure
replication and administration.

## `UNLOGGED` and `TEMPORARY` Tables Are Not Replicated {#unlogged-and-temporary-tables-are-not-replicated}

`UNLOGGED` and `TEMPORARY` tables will not and cannot be replicated, much
like with physical streaming replication.

## One Database at a Time {#one-database-at-a-time}

To replicate multiple databases you must set up individual provider or
subscriber relationships for each. There is no way to configure replication
for all databases in a PostgreSQL install at once.

## PRIMARY KEY or REPLICA IDENTITY Required {#primary-key-or-replica-identity-required}

`UPDATE`s and `DELETE`s cannot be replicated for tables that lack a `PRIMARY
KEY` or other valid replica identity such as using an index, which must be
unique, not partial, not deferrable, and include only columns marked NOT
NULL. Replication has no way to find the tuple that should be updated or
deleted since there is no unique identifier.

`REPLICA IDENTITY FULL` is not supported as a standalone replication identity
for UPDATE or DELETE operations. However, it is supported when used in
conjunction with Delta-Apply columns on tables that have a primary key. For
tables without a primary key or Delta-Apply configuration, UPDATE and DELETE
operations require a PRIMARY KEY or explicit REPLICA IDENTITY USING INDEX.

## Only One Unique Index or Constraint or PK {#only-one-unique-index-or-constraint-or-pk}

If more than one upstream is configured or the downstream accepts local
writes, only one `UNIQUE` index should be present on downstream replicated
tables. Conflict resolution can only use one index at a time, so conflicting
rows may `ERROR` if a row satisfies the `PRIMARY KEY` but violates a `UNIQUE`
constraint on the downstream side.

You can have additional unique constraints upstream if the downstream consumer
gets writes from that upstream and nowhere else. The rule is that the
downstream constraints must not be more restrictive than those on the
upstream(s).

Partial secondary unique indexes are permitted, but will be ignored for
conflict resolution purposes.

`spock.check_all_uc_indexes` is an experimental
[GUC](/pgedge/spock/configuration/) that
adds `INSERT` conflict resolution by allowing Spock to consider all unique
constraints, not just the primary key or replica identity.

## Unique Constraints Must Not Be Deferrable {#unique-constraints-must-not-be-deferrable}

Deferrable unique constraints and primary keys are silently skipped during
INSERT conflict resolution. This means that if your only unique constraint on
a table is deferrable, INSERT conflicts will not be detected, potentially
leading to duplicate rows on subscriber nodes.

On the downstream end, spock may also emit the error:

```sql
ERROR: spock doesn't support index rechecks needed for deferrable indexes
DETAIL: relation "public"."test_relation" has deferrable indexes: "index1",
"index2"
```

Recommendation: Ensure all tables have at least one non-deferrable unique
constraint (preferably the primary key) for reliable conflict detection.

## No Replication Queue Flush {#no-replication-queue-flush}

There is no support for freezing transactions on the master and waiting until
all pending queued xacts are replayed from slots.

This means that care must be taken when applying table structure changes. If
there are committed transactions that are not yet replicated and the table
structure of the provider and subscriber are changed at the same time in a
way that makes the subscriber table incompatible with the queued transactions
replication will stop.

Administrators should either ensure that writes to the provider are stopped
before making schema changes, or use the `spock.replicate_ddl` function to
queue schema changes so they are replayed at a consistent point on the
subscriber.

In multi-master configurations, using `spock.replicate_ddl` alone is not
sufficient. The subscriber may be generating new transactions with the old
structure after the schema change is committed on the provider. Users must
ensure writes are stopped on all nodes and all slots are caught up before
making schema changes.

## FOREIGN KEYS {#foreign-keys}

Foreign keys constraints are not enforced for the replication process - what
succeeds on provider side gets applied to subscriber even if the `FOREIGN KEY`
would be violated.

## TRUNCATE {#truncate}

Using `TRUNCATE ... CASCADE` will only apply the `CASCADE` option on the
provider side.

(Properly handling this would probably require the addition of `ON TRUNCATE CASCADE`
support for foreign keys in PostgreSQL).

`TRUNCATE ... RESTART IDENTITY` is replicated. The sequence restart is
applied on subscriber nodes. Note that this may cause sequence value
divergence if sequences are not managed via pgEdge Snowflake.

## Sequences {#sequences}

We strongly recommend that you use pgEdge [Snowflake
Sequences](https://github.com/pgEdge/snowflake) rather than using the legacy
sequences described below.

The state of sequences added to replication sets is replicated periodically
and not in real-time. Dynamic buffer is used for the value being replicated
so that the subscribers actually receive future state of the sequence. This
minimizes the chance of subscriber's notion of sequence's `last_value`
falling behind but does not completely eliminate the possibility.

It might be desirable to call `sync_sequence` to ensure all subscribers have
up to date information about given sequence after big events in the database
such as data loading or during the online upgrade.

It is generally recommended to use `bigserial` and `bigint` types for
sequences on multi-node systems as smaller sequences might reach end of the
sequence space fast.

Users who want to have independent sequences on provider and subscriber can
avoid adding sequences to replication sets and create sequences with step
interval equal to or greater than the number of nodes. And then setting a
different offset on each node. Use the `INCREMENT BY` option for `CREATE
SEQUENCE` or `ALTER SEQUENCE`, and use `setval(...)` to set the start point.

## Triggers {#triggers}

Apply process and the initial COPY process both run with
`session_replication_role` set to `replica` which means that `ENABLE REPLICA`
and `ENABLE ALWAYS` triggers will be fired.

## PostgreSQL Version Differences {#postgresql-version-differences}

Spock can replicate across PostgreSQL major versions. Despite that, long
term cross-version replication is not considered a design target, though it may
often work. Issues where changes are valid on the provider but not on the
subscriber are more likely to arise when replicating across versions.

It is safer to replicate from an old version to a newer version since PostgreSQL
maintains solid backward compatibility but only limited forward compatibility.
Initial schema synchronization is only supported when replicating between same
version of PostgreSQL or from lower version to higher version.

Replicating between different minor versions makes no difference at all.

## Database Encoding Differences {#database-encoding-differences}

Spock does not support replication between databases with different encoding.
The encoding must match on all nodes in the cluster. While `UTF-8` is
commonly used and recommended for international character support, any
encoding is acceptable as long as it is consistent across all nodes.

## Large Objects {#large-objects}

PostgreSQL's logical decoding facility does not support decoding changes to
[large objects](https://www.postgresql.org/docs/current/largeobjects.html);
we recommend using the [LOLOR extension](https://github.com/pgEdge/lolor)
to manage large objects.

Note that DDL limitations apply, so extra care needs to be taken when using
`replicate_ddl_command()`.

## Delta-Apply Column Requirements {#delta-apply-column-requirements}

Columns configured for Delta-Apply conflict resolution must have a `NOT NULL`
constraint. If a NULL value is encountered during delta application, the apply
worker will error with:

```text
ERROR: delta apply column can't operate NULL values
```

Ensure all Delta-Apply columns are defined with `NOT NULL` before enabling
this feature.

## Mixed Spock and Native Logical Replication {#mixed-spock-and-native-logical-replication}

Spock uses its own 16-bit node_id (derived from node name hash) to track
transaction origins in commit timestamps, rather than PostgreSQL's
RepOriginId. Both ID spaces overlap (0-65535), which can cause ambiguity if
Spock and native PostgreSQL logical replication run on the same database.

Recommendation: Avoid running Spock and native logical replication
subscriptions on the same database.

## Row and Column Filters {#row-and-column-filters}

Row and column filters have the following limitations.

### System Columns Cannot Be Filtered {#system-columns-cannot-be-filtered}

System columns (such as `oid` or `xmin`) cannot be used in row filters or
column filters. Column and row filters work correctly on tables with OIDs,
but the system columns themselves cannot be filtered.

### Row Filter Expression Constraints {#row-filter-expression-constraints}

Row filters are normal PostgreSQL expressions with the same limitations as
CHECK constraints.

Volatile functions (like `random()` or `now()`) can be used in row
filters, but they may produce different results on evaluation and cause
errors that stop replication. Use volatile functions with caution.

### Row Filter Session Context {#row-filter-session-context}

Row filters run in the replication session context, not the original
session context. This means that session-specific expressions (like
`CURRENT_USER`) will have replication session values, not the original
session values.

### Column Filter Behavior {#column-filter-behavior}

When using column filters, note the following behaviors:

- Dropping a filtered column automatically removes it from the filter.
- New columns are not automatically included in existing filters.
- Column filters must be updated manually to include new columns.

## Partitioned Tables {#partitioned-tables}

Partitioned tables have specific replication limitations.

### New Partitions Not Automatically Replicated {#new-partitions-not-automatically-replicated}

When partitions are added after initial synchronization, they must be
added manually using the `spock.repset_add_partition()` function.

The parent table is synchronized during initial sync, but individual
partitions are not synced directly. New partitions created after sync
require explicit addition to the replication set.

### Detached Partitions Not Automatically Removed {#detached-partitions-not-automatically-removed}

Detaching a partition does not automatically remove it from replication.
You must use `spock.repset_remove_partition()` to update cluster metadata
and remove the partition from the replication set.

## DDL Replication Limitations {#ddl-replication-limitations}

Some DDL statements are intentionally not replicated.

### DDL Statements Not Replicated {#ddl-statements-not-replicated}

The following types of DDL statements are not replicated:

- `CREATE DATABASE` - Database creation is not replicated.
- `CREATE TABLE...AS...` - This statement is replicated but may be unsafe
  because the table is replicated before being added to the replication
  set.

In multi-node clusters with three or more nodes, some DDL statements (such
as `DROP TABLE`) may cause replication issues.

### DDL Replication Best Practices {#ddl-replication-best-practices}

For best results, enable automatic DDL replication only when the schema
matches exactly on all nodes. This means either all databases have no
objects, or all databases have exactly the same objects with all tables in
the replication sets.

## Spock Schema {#spock-schema}

The `spock` schema is managed internally by Spock and has the following
restriction.

### Direct Modification Prohibited {#direct-modification-prohibited}

Do not delete, create, or modify files in the `spock` schema directly. Use
Spock functions and procedures to manage replication. Direct schema
modification can corrupt replication metadata and cause replication
failures.

## Read-Only Mode {#read-only-mode}

Read-only mode has the following limitation.

### Read-Only at SQL Level Only {#read-only-at-sql-level-only}

The `spock.readonly` parameter enforces read-only restrictions at the SQL
level for non-superusers. However, background processes (checkpointer,
background writer, WAL writer, and autovacuum) continue to run and may
write to disk.

This means that database files are not truly read-only, and some disk
writes may still occur even when read-only mode is enabled.

## Replication Position Skipping {#replication-position-skipping}

Using `spock.sub_alter_skiplsn()` to skip replication positions has the
following critical limitation.

### Skipped Data Not Replayed or Repaired {#skipped-data-not-replayed-or-repaired}

The `spock.sub_alter_skiplsn()` operation does not replay or repair
skipped data. Any changes between the old LSN and the specified LSN are
permanently ignored by the subscriber.

Use this function only when you understand the data implications and accept
that skipped changes will be lost on the subscriber node.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/limitations.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
