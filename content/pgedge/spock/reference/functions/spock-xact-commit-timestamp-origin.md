---
title: spock.xact_commit_timestamp_origin()
description: spock.xactcommittimestamporigin (xid xid, OUT timestamp timestamptz, OUT roident oid)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_xact_commit_timestamp_origin.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.xact_commit_timestamp_origin()

## SYNOPSIS {#synopsis}

spock.xact_commit_timestamp_origin (xid xid, OUT timestamp timestamptz,
OUT roident oid)

## RETURNS {#returns}

A record containing transaction commit information:

  - timestamp is the commit timestamp of the transaction.
  - roident is the replication origin identifier of the transaction.

## DESCRIPTION {#description}

Returns the commit timestamp and replication origin identifier for a given
transaction ID.

This function queries PostgreSQL's commit timestamp tracking system to
retrieve when a specific transaction was committed and which replication
origin it came from. The replication origin identifies the source node
in a multi-node replication topology, allowing you to trace where
changes originated.

The commit timestamp tracking feature (track_commit_timestamp) must be
enabled in PostgreSQL for this function to return meaningful results.
If commit timestamp tracking is disabled, the function may return NULL
or raise an error.

The replication origin identifier (roident) will be `0` for transactions
committed locally on this node (i.e., not replicated in from another node).
For replicated transactions, it identifies the origin node from which the
changes were received. A `NULL` result for the timestamp or origin means the
origin metadata is unavailable or unknown (for example, because
`track_commit_timestamp` was not enabled at the time of the commit) — `NULL`
is distinct from `0` and does not indicate a local change.

This is a read-only query function that does not modify any data.

## ARGUMENTS {#arguments}

xid

    The transaction ID to query.

## EXAMPLE {#example}

    SELECT * FROM spock.xact_commit_timestamp_origin('12345'::xid);

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_xact_commit_timestamp_origin.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
