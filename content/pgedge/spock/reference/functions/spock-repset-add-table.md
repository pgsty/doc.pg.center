---
title: spock.repset_add_table()
description: spock.repsetaddtable ( setname name, relation regclass, synchronizedata boolean, columns text[], rowfilter
  text, includepartitions boolean )
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_add_table.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



`spock.repset_add_table()`

## SYNOPSIS {#synopsis}

spock.repset_add_table (
    set_name name,
    relation regclass,
    synchronize_data boolean,
    columns text[],
    row_filter text,
    include_partitions boolean
)

## RETURNS {#returns}

    - true if the table was successfully added to the replication set.
    - Raises an ERROR if the table is already a member of the replication
      set, or if the call has invalid parameters or insufficient
      privileges.

## DESCRIPTION {#description}

Adds a specific table to an existing Spock replication set.

This function allows fine-grained control over what data is replicated by
optionally specifying:

    - A subset of columns to replicate.
    - A row filter to restrict which rows are replicated.
    - Whether partitions of a partitioned table should also be included.

If synchronize_data is set to true, existing table data is copied to all
subscribers that are subscribed to this replication set. Otherwise, only
future changes are replicated.

When used with partitioned tables, include_partitions controls whether
child partitions are automatically included in the replication set.

This function writes metadata into the Spock catalogs and does not modify
PostgreSQL configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

set_name

    The name of an existing replication set.

relation

    The table to add, specified as a regclass (for example,
    'public.mytable').

synchronize_data

    If true, existing table data is synchronized to all
    subscribers. Default is false.

columns

    An optional list of column names to replicate. If NULL,
    all columns are replicated.

row_filter

    An optional SQL WHERE clause used to filter which rows
    are replicated.

include_partitions

    If true and the table is partitioned, all partitions are
    included automatically. Default is true.

## EXAMPLE {#example}

The following command adds a table named public.accounts to the demo_repset 
replication set with full replication:

    SELECT spock.repset_add_table('demo_repset', 'public.accounts');

The following command adds a table named public.accounts to the demo_repset 
replication set, and synchronizes existing data:

    SELECT spock.repset_add_table('demo_repset',
        'public.accounts',
        synchronize_data := true);

The following command adds only specific columns (id and balance) from the
public.accounts table to the demo_repset replication set, and filters the
rows:

    SELECT spock.repset_add_table('demo_repset',
        'public.accounts',
        columns := ARRAY['id','balance'],
        row_filter := 'balance > 0');

**WARNING: Use caution when synchronizing data with a valid row filter.**
Using `synchronize_data=true` with a valid `row_filter` is usually a
one-time operation for a table. Executing it again with a modified
`row_filter` won't synchronize data to the subscriber. You may need to call
`spock.sub_resync_table()` to fix it.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_add_table.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
