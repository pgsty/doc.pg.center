---
title: spock.repset_remove_table()
description: spock.repsetremovetable ( setname name, relation regclass, includepartitions boolean)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_remove_table.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



`spock.repset_remove_table ()`

## SYNOPSIS {#synopsis}

spock.repset_remove_table (
    set_name name,
    relation regclass,
    include_partitions boolean)

## RETURNS {#returns}

    - true if the table was successfully removed from the replication set.
    - Raises an ERROR if the table is not a member of the replication set,
      or if the call has invalid parameters or insufficient privileges.

## DESCRIPTION {#description}

Removes a table from an existing Spock replication set.  After removal, 
changes to this table will no longer be replicated to subscribers that
are subscribed to the replication set.

If the table is partitioned, the include_partitions argument controls
whether all child partitions are also removed from the replication set.

This function updates metadata stored in the Spock catalogs and does not
modify the PostgreSQL configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

set_name

    The name of an existing replication set.

relation

    The table to remove, specified as a regclass
    (for example, 'public.mytable').

include_partitions

    If true and the table is partitioned, all partitions are
    also removed from the replication set. Default is true.

## EXAMPLE {#example}

Remove a table (public.users) from the default replication set:

    postgres=# SELECT spock.repset_remove_table('default', 'public.users');
     repset_remove_table 
    ---------------------
     t
    (1 row)

Remove a partitioned table named public.sales_parent from the default
replication set without removing its partitions:

    postgres=# SELECT spock.repset_remove_table('default',
    'public.users',
    include_partitions := false);
    ---------------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_remove_table.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
