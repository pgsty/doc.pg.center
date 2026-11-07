---
title: spock.sub_wait_for_sync
description: The spock.subwaitforsync() function waits until a specified subscription has completed its initial
  schema and data synchronization.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_wait_for_sync.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



The `spock.sub_wait_for_sync()` function waits until a specified subscription
has completed its initial schema and data synchronization.

## Synopsis {#synopsis}

```sql
spock.sub_wait_for_sync(subscription_name name)
```

## Description {#description}

The `spock.sub_wait_for_sync()` function waits until the specified subscription
has completed its initial schema and data synchronization, and any pending
table resynchronizations have finished.

This function blocks the current session until the subscription is fully
synchronized. The function monitors both the initial sync phase (if the
subscription is newly created) and any tables that are undergoing individual
resynchronization due to replication set changes or manual resync operations.

For optimal results, execute `spock.wait_slot_confirm_lsn()` on the provider
node after making replication set changes that trigger resyncs. This approach
ensures the provider has flushed all necessary changes before checking sync
status on the subscriber. Only after the provider confirms the LSN should you
call `spock.sub_wait_for_sync()` on the subscriber.

The function will continue waiting indefinitely until synchronization completes,
so callers should ensure the subscription is actively processing and that there
are no blocking issues preventing sync completion.

## Arguments {#arguments}

The function accepts the following argument:

- `subscription_name` - The name of the subscription to monitor for sync
  completion.

## Example {#example}

In the following example, the `spock.sub_wait_for_sync()` function waits for a
subscription named `sub_n2_n1` to complete synchronization:

```sql
SELECT spock.sub_wait_for_sync('sub_n2_n1');
-[ RECORD 1 ]-----+-
sub_wait_for_sync |
```

For more information about using subscription synchronization with Zero-Downtime
Add Node, see the [ZODAN Tutorial](/pgedge/spock/modify/zodan/zodan-tutorial/).

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_wait_for_sync.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
