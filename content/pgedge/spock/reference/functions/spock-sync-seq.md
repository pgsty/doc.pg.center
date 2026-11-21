---
title: spock.sync_seq
description: The spock.syncseq() function synchronizes the current state of a sequence to all subscribers.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_seq.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



The `spock.sync_seq()` function synchronizes the current state of a sequence
to all subscribers.

## Synopsis {#synopsis}

```sql
spock.sync_seq(relation regclass) RETURNS boolean
```

## Description {#description}

Captures the current value of a sequence on the provider node and pushes it
into the replication stream so that subscribers can update their local copy to
match. This ensures sequence values remain coordinated across nodes.

This function must be executed on the provider node. The sequence state update
is embedded in the transaction where this function is called, and subscribers
apply the update when they replicate that transaction.

Replication set filtering applies — only subscribers whose subscriptions
include the replication set containing this sequence will receive the update.

## Arguments {#arguments}

The function accepts the following argument:

- `relation` - The name of the sequence to synchronize, optionally
  schema-qualified.

## Example {#example}

In the following example, the `spock.sync_seq()` function synchronizes a
sequence named `public.sales_order_no_seq`:

```sql
SELECT spock.sync_seq('public.sales_order_no_seq');
 sync_seq
----------
 t
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_seq.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
