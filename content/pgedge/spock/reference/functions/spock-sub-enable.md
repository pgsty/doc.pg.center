---
title: spock.sub_enable
description: The spock.subenable() function enables a subscription.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_enable.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



The `spock.sub_enable()` function enables a subscription. Replication workers
then resume normal processing for that subscription.

## Synopsis {#synopsis}

```sql
spock.sub_enable(subscription_name name, immediate boolean)
```

## Description {#description}

The `spock.sub_enable()` function enables a subscription.

This fails if another subscription on this node already has origin
forwarding active; see
[Origin Forwarding](/pgedge/spock/reference/sub-mgmt/#origin-forwarding).

## Arguments {#arguments}

The function accepts the following arguments:

- `subscription_name` - The name of an existing subscription.
- `immediate` - If `true`, the subscription is started immediately; otherwise
  the subscription will be started only at the end of the current transaction.
  The default is `false`.

## Example {#example}

In the following example, the `spock.sub_enable()` function enables a
subscription named `sub_n1_n2`:

```sql
SELECT spock.sub_enable('sub_n1_n2');
 sub_enable
-------------
 t
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_enable.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
