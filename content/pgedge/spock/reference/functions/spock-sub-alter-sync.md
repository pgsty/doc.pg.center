---
title: spock.sub_alter_sync
description: The spock.subaltersync() function synchronizes all unsynchronized tables in all sets in a single operation.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_sync.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



The `spock.sub_alter_sync()` function synchronizes all unsynchronized tables
in all sets in a single operation.

## Synopsis {#synopsis}

```sql
spock.sub_alter_sync(subscription_name name, truncate boolean DEFAULT false)
RETURNS boolean
```

## Description {#description}

The `spock.sub_alter_sync()` function synchronizes all unsynchronized tables
in all sets in a single operation. The function copies and synchronizes
tables one by one. The function does not wait for completion before returning
to the caller; use `spock.sub_wait_for_sync()` to wait for completion.

## Arguments {#arguments}

The function accepts the following arguments:

- The `subscription_name` argument specifies the name of an existing
  subscription.
- The `truncate` argument accepts a boolean value; when set to `true`,
  the function truncates tables before copying, and the default value
  is `false`.

## Example {#example}

In the following example, the `spock.sub_alter_sync()` function synchronizes
all unsynchronized tables for a subscription named `sub_n1_n2`:

```sql
SELECT spock.sub_alter_sync('sub_n1_n2', true);
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_sync.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
