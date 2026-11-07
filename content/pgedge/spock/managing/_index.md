---
title: Managing a Spock Installation
description: 'The Spock extension is a powerful addition to any PostgreSQL installation; management features of
  the Spock extension allow you to seamlessly:'
weight: 60
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: Managing replication
icon: fa-solid fa-book-open
type: docs
---



The Spock extension is a powerful addition to any PostgreSQL installation; management features of the Spock extension allow you to seamlessly:

* [replicate partitioned tables](/pgedge/spock/managing/partition-mgmt/).
* create logical [row-based data filters](/pgedge/spock/managing/filtering/).
* set a cluster to [READ-ONLY mode](/pgedge/spock/managing/read-only/); this restricts non-superusers to read-only operations, while superusers can still perform both read and write operations.
* use a [trigger](/pgedge/spock/managing/repset-trigger/) to manage replication set membership.
* use [Snowflake sequences](/pgedge/spock/managing/snowflake/) for sequence management in a distributed cluster.
* use [the Lolor extension](/pgedge/spock/managing/lolor/) to replicate large objects.
* enable [automatic DDL replication](/pgedge/spock/managing/spock-autoddl/).

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
