---
title: spock.sub_remove_repset
description: The spock.subremoverepset() function removes a replication set from a subscription.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_remove_repset.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



The `spock.sub_remove_repset()` function removes a replication set from a
subscription.

## Synopsis {#synopsis}

```sql
spock.sub_remove_repset(subscription_name name, replication_set name)
```

## Description {#description}

The `spock.sub_remove_repset()` function removes a replication set from a
subscription.

## Arguments {#arguments}

The function accepts the following arguments:

- `subscription_name` - The name of an existing subscription.
- `replication_set` - The name of the replication set to remove.

## Example {#example}

In the following example, the `spock.sub_remove_repset()` function removes a
replication set named `test` from a subscription named `sub_n1_n2`:

```sql
select spock.sub_remove_repset('sub_n1_n2', 'test');
 sub_remove_repset 
-------------------
 t
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_remove_repset.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
