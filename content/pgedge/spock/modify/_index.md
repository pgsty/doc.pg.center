---
title: Adding a Node to a Replicating Cluster
description: 'There are several tools and scripts you can use to add a node to a cluster; the way that you choose
  should depend on the use and state of your cluster:'
weight: 70
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/modify/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Changing the cluster
icon: fa-solid fa-book-open
type: docs
---



There are several tools and scripts you can use to add a node to a cluster; the way that you choose should depend on the use and state of your cluster:

* **Use Z0DAN to Add or Remove a Node with Zero Downtime**

[Z0DAN](/pgedge/spock/modify/zodan/) is a spock utility that provides scripts that you can use to seamlessly add or remove a node from your cluster with zero downtime.

* **Use pgBackRest to Add a Node to a Replicating Cluster with Minimal Downtime**

[pgBackRest](/pgedge/spock/modify/add-node-pgbackrest/) is an open-source tool that you can use to add a node to a replicating cluster with minimal interruption.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/modify/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
