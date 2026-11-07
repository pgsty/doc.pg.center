---
title: Using LOLOR to Manage Large objects
description: PostgreSQL's logical decoding facility does not support decoding changes to large objects; we recommend
  instead using the LOLOR extension to manage large objects.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/lolor.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



PostgreSQL's logical decoding facility does not support decoding changes to
[large objects](https://www.postgresql.org/docs/current/largeobjects.html);
we recommend instead using the
[LOLOR extension](https://github.com/pgEdge/lolor) to manage large objects.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/lolor.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
