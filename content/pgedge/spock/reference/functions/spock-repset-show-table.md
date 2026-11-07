---
title: spock.repset_show_table()
description: spock.repsetshowtable (relation regclass, repsets text[])
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_show_table.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.repset_show_table()

## SYNOPSIS {#synopsis}

spock.repset_show_table (relation regclass, repsets text[])

## RETURNS {#returns}

A record containing detailed information about how a table is configured
for replication:

  - relid is the OID of the table relation.
  - nspname is the schema name of the table.
  - relname is the table name.
  - att_list is an array of column names included in replication.
  - has_row_filter is true if a row filter is applied to the table.
  - relkind is the relation kind ('r' for regular table, 'p' for
    partitioned table).
  - relispartition is true if the table is a partition of a partitioned
    table.

## DESCRIPTION {#description}

Returns detailed replication configuration information for a specific table
within the specified replication sets.

This function queries how a table is configured for replication across one
or more replication sets. It shows which columns are included in
replication, whether row filtering is applied, and metadata about the table
type and partition status.

The att_list field shows the specific columns that will be replicated. If
all columns are replicated, this will contain all column names. If column
filtering was configured when the table was added to a replication set,
only the specified columns appear in this list.

The has_row_filter field indicates whether a row filter expression is
applied to the table, which would limit which rows are replicated based on
custom criteria.

The repsets parameter allows you to check the table's configuration across
multiple replication sets. The function returns information based on how
the table is configured in those sets.

This is a read-only query function that does not modify any data.

## ARGUMENTS {#arguments}

relation

    The table to query information about.

repsets

    An array of replication set names to check the table's
    configuration within.

## EXAMPLE {#example}

The following command shows detailed information about the public.invoices
table:

    postgres=# SELECT * FROM spock.repset_show_table('public.invoices',
        ARRAY['default', 'ddl_sql']);
    -[ RECORD 1 ]--+-----------------------------------------
    relid          | 17241
    nspname        | public
    relname        | invoices
    att_list       | {order_id,customer_id,order_date,amount}
    has_row_filter | f
    relkind        | r
    relispartition | f

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_show_table.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
