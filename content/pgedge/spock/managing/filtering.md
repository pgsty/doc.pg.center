---
title: Filtering
description: Spock allows row based filtering on both the provider side and the subscriber side.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/filtering.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



Spock allows row based filtering on both the provider side and the
subscriber side.

## Row Filtering on the Provider {#row-filtering-on-the-provider}

On the provider, you can implement row filtering with the `row_filter`
property of the `spock.repset_add_table` function. The `row_filter` is a
normal PostgreSQL expression with the same limitations as the `CHECK`
constraint.

A simple `row_filter` would look something like `row_filter := 'id > 0'`;
this filter ensures that only rows where values of `id` column is greater
than zero are replicated.

You can use a volatile function inside `row_filter` but use caution with
regard to `writes` as any expression that will do writes could potentially
throw an error and stop replication.

It's worth noting that the `row_filter` is running inside the
replication session, so session specific expressions such as `CURRENT_USER`
will have the values of the replication session and not the session that did
the writes.

## Row Filtering on the Subscriber {#row-filtering-on-the-subscriber}

On the subscriber, row-based filtering can be implemented using the standard
`BEFORE TRIGGER` mechanism. You must mark triggers as either `ENABLE REPLICA`
 or `ENABLE ALWAYS` or they will not be executed by the replication
process.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/filtering.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
