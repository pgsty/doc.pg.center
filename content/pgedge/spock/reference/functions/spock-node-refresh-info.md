---
title: spock.node_refresh_info()
description: spock.noderefreshinfo (pnodename name DEFAULT NULL)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_refresh_info.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.node_refresh_info()

## SYNOPSIS {#synopsis}

spock.node_refresh_info (p_node_name name DEFAULT NULL)

## RETURNS {#returns}

`true` if the refresh (or, with no argument, every refresh attempted)
succeeded; `false` if one or more nodes could not be refreshed when called
with no argument. Raises an error if called with a specific `node_name`
that does not exist or that names the local node, or if refreshing that
node fails for any reason -- including an unreachable or misconfigured
interface, a dsn that now answers as a different node, or any other error
from the remote fetch.

## DESCRIPTION {#description}

Re-fetches a known peer node's `location`, `country`, and `info` (including
any `tiebreaker` key within `info`) directly from that node, and overwrites
this node's locally cached copy.

`spock.node` is a local catalog: each node populates its row for a peer
once, either when that node is created or when a subscription to it is
first created. A peer's later `location`/`country`/`info` change -- most
commonly to assign a custom `tiebreaker` and resolve an equal-tiebreaker
collision -- propagates automatically to every node that subscribes to
that peer *directly* (see
[Automatic Node Metadata Propagation](/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)),
with no call to this function needed. The message is not forwarded, and a
node normally has a row for a peer only through its own subscription to it,
so a cascade node that does not subscribe to the changed peer has no row to
refresh. This function is needed when a node's cached row missed an update,
for example because the transaction carrying it was skipped or discarded,
and to force a specific peer's info to be re-fetched on demand.
`spock.sub_resync_table()` warns when the provider's row differs from the
cached one. See the Tiebreaker section in
[conflict_types.md](/pgedge/spock/conflicts/) for why this matters and why
`spock.node` is not simply replicated wholesale.

Called with a specific `node_name`, only that node's row is refreshed and
any failure refreshing it is reported as an error. Called with no
argument, every known node other than the local one is refreshed on a
best-effort basis: a node that fails to refresh for any reason logs a
`WARNING` and does not stop the others from being refreshed, and the
overall return value is `false` if any node failed.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

p_node_name

    Optional. The name of a single peer node to refresh. If omitted (or
    NULL), every node other than the local one is refreshed.

## EXAMPLE {#example}

After assigning a custom tiebreaker on `n1` to resolve a collision:

    n1=# UPDATE spock.node SET info = COALESCE(info, '{}'::jsonb) ||
           '{"tiebreaker": 42}' WHERE node_name = 'n1';

Refresh that on every other node:

    n2=# SELECT spock.node_refresh_info('n1');
     node_refresh_info
    --------------------
     t
    (1 row)

Or refresh everything this node knows about in one call:

    n3=# SELECT spock.node_refresh_info();
     node_refresh_info
    --------------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_refresh_info.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
