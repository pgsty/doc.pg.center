---
title: spock.version()
description: Returns the Spock version in a human-readable major/minor form (for example, 5.0.5).
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



`spock.spock_version()`

## SYNOPSIS {#synopsis}

`spock.spock_version ()`

## DESCRIPTION {#description}

Returns the Spock version in a human-readable major/minor form (for example, `5.0.5`).

## EXAMPLE {#example}

```sql
postgres=# SELECT spock.spock_version();
 spock_version
---------------
 5.0.5
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
