---
title: spock.sub_remove_repset
description: The spock.subremoverepset() function removes a replication set from a subscription.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_remove_repset.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
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

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_remove_repset.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
