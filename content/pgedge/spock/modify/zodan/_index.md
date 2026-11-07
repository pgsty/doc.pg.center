---
title: Modifying a Cluster with Zodan
description: Zodan provides tools to add or remove a node with zero downtime.
weight: 20
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/modify/zodan/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Z0DAN
icon: fa-solid fa-book-open
type: docs
---



Zodan provides tools to add or remove a node with zero downtime. The
scripts are located in the 
[samples/Z0DAN](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN)
directory of the [Spock GitHub](https://github.com/pgEdge/spock) repository.

During node addition, Zodan seamlessly manages creation of the new node,
subscription management (both to and from the node), replication slot
creation, data synchronization, replication slot advancement, and final
activation of subscriptions.

During node removal, Zodan simplifies removing fully-functional or failed
nodes from a cluster. When you remove a node from a cluster, the removal
does not delete Postgres artifacts (the database, data directory, log
files, etc.).


> [!NOTE]
>
> Zodan simplifies removing partially added nodes created during failed
> node add operations. Additional cleanup steps may be required before
> attempting another node deployment on the target host.
>


> [!NOTE]
>
> Each script must be run from the target node being added or removed.
>

## Key Differences Between using Zodan and the Manual Process {#key-differences-between-using-zodan-and-the-manual-process}

The following differences highlight how Zodan automates and simplifies
node addition:

- Zodan stores sync LSNs and uses them later to ensure subscriptions
  start from the correct point even if hours pass between steps.

- Zodan automatically detects existing schemas on the new node and populates the
  `skip_schema` parameter, preventing conflicts during structure sync.

- Zodan checks Spock versions before starting. Every node must be 5.0.9 or
  later, and the new node must run the same or a newer major.minor version
  than every existing node (patch levels may differ). So a 6.0.x node can
  join a 5.0.x cluster, and further 6.0.x nodes can join the resulting
  mixed cluster from any source node; a new node older than an existing
  node is rejected.

- Zodan includes the `verify_subscription_replicating()` function after
  enabling subscriptions to ensure they reach replicating status.

- When adding to a single-node cluster, Zodan handles the process
  differently — no disabled subscriptions are needed.

- Zodan shows final status of all nodes and subscriptions across the
  entire cluster, not just the new node.


For more information, review the following resources:

- [Using Zodan](/pgedge/spock/modify/zodan/zodan-readme/)
- [Zodan Tutorial](/pgedge/spock/modify/zodan/zodan-tutorial/)
- [Zodan Scripts and Workflows](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN)
- [Spock Documentation](https://docs.pgedge.com/spock-v5/)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/modify/zodan/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
