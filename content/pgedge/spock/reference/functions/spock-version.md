---
title: spock.version()
description: Returns the Spock version in a human-readable major/minor form (for example, 5.0.5).
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_version.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
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

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_version.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
