---
title: spock.table_wait_for_sync()
description: spock.tablewaitforsync (subscriptionname name, relation regclass)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_table_wait_for_sync.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.table_wait_for_sync()

## SYNOPSIS {#synopsis}

spock.table_wait_for_sync (subscription_name name, relation regclass)

## RETURNS {#returns}

void (returns nothing upon successful completion).

## DESCRIPTION {#description}

Waits until the specified table has completed synchronization for the given
subscription.

This function blocks the current session until the specified table finishes
its synchronization process. This is useful when you need to ensure a
specific table is fully synchronized before proceeding with operations that
depend on its data.

Unlike spock.sub_wait_for_sync() which waits for all tables in a
subscription to sync, this function targets a single table. This allows for
more granular control when monitoring synchronization progress or when only
specific tables are critical to downstream operations.

For optimal results, execute spock.wait_slot_confirm_lsn() on the provider
node after making replication set changes that trigger table resyncs. This
ensures the provider has flushed all necessary changes before checking sync
status on the subscriber. Only after the provider confirms the LSN should
you call spock.table_wait_for_sync() on the subscriber.

The function will continue waiting indefinitely until the table
synchronization completes, so callers should ensure the subscription is
actively processing and that there are no blocking issues preventing sync
completion.

## ARGUMENTS {#arguments}

subscription_name

    The name of the subscription to monitor.

relation

    The name of the table to wait for, specified as a regclass (can
    be schema-qualified).

## EXAMPLE {#example}

    SELECT spock.table_wait_for_sync('sub_n2_n1', 'public.mytable');

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_table_wait_for_sync.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
