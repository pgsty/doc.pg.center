---
title: Using LOLOR to Manage Large objects
description: PostgreSQL's logical decoding facility does not support decoding changes to large objects; we recommend
  instead using the LOLOR extension to manage large objects.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/lolor.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



PostgreSQL's logical decoding facility does not support decoding changes to
[large objects](https://www.postgresql.org/docs/current/largeobjects.html);
we recommend instead using the
[LOLOR extension](https://github.com/pgEdge/lolor) to manage large objects.

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/lolor.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
