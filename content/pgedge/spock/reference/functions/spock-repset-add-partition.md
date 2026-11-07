---
title: spock.repset_add_partition()
description: spock.repsetaddpartition ( parent regclass, partition regclass, rowfilter text)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_add_partition.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



`spock.repset-add-partition ()`

## SYNOPSIS {#synopsis}

spock.repset_add_partition (
    parent regclass,
    partition regclass,
    row_filter text)

## RETURNS {#returns}

  - 0 if the parent table is not a partitioned table or if all partitions
    are already in the replication sets.

  - A positive integer indicating the count of partitions successfully
    added to replication sets.

## DESCRIPTION {#description}

Adds a partition of a table to the same replication set(s) as its parent
table.

This function is used when working with partitioned tables to ensure that
new or existing partitions are properly included in replication. If the
partition argument is omitted, Spock automatically discovers and adds all
partitions of the specified parent table.

An optional row_filter can be supplied to limit which rows from the
partition are replicated.

This function writes metadata into the Spock catalogs and does not modify
PostgreSQL configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

parent

    The parent partitioned table, specified as a regclass.

partition

    A specific partition table to add. If omitted, all
    partitions of the parent are added. The default is NULL.

row_filter

    An optional SQL expression used to filter which rows
    from the partition are replicated. The default is NULL.

## EXAMPLE {#example}

Add all four partitions of a parent table (named 'public.sales_parent') to
the replication set to which the parent belongs:

    SELECT spock.repset_add_partition('public.sales_parent');
    -[ RECORD 1 ]--------+--
    repset_add_partition | 4

Add a specific partition (named public.sales_2026_q1) to the replication
set to which the parent table belongs:

    postgres=# SELECT spock.repset_add_partition(
        'public.sales_parent',
        'public.sales_2026_q1',
        'region = ''US'''
    );
    -[ RECORD 1 ]--------+--
    repset_add_partition | 1


---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_add_partition.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
