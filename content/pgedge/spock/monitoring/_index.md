---
title: Monitoring the Configuration and Health of Your Cluster
description: 'The Spock extension provides several ways you can monitor data health in your Postgres cluster:'
weight: 80
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/monitoring/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Monitoring
icon: fa-solid fa-book-open
type: docs
---



The Spock extension provides several ways you can monitor data health in your Postgres cluster:

* You can [query informational tables](/pgedge/spock/monitoring/spock-info/) in the `spock` schema to review information about your cluster configuration and status.
* The [status views](/pgedge/spock/monitoring/node-monitoring/) `spock.node_status`, `spock.subscription_status`, `spock.worker_status`, `spock.slot_status` and `spock.events` give a complete picture of a node without reading the server log.
* The Spock extension's [Lag Tracking](/pgedge/spock/monitoring/lag-tracking/) utility allows you to review node-specific metrics for replication lag.
* Use Spock's [Sync Event](/pgedge/spock/monitoring/spock-sync-event/) utility to watch for a specific transaction to replicate.
* Use the [ACE (Active Consistency Engine)](https://docs.pgedge.com/platform/ace) to evaluate cluster health.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/monitoring/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
