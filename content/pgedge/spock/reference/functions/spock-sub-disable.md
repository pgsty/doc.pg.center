---
title: spock.sub_disable
description: The spock.subdisable() function disables a subscription and disconnects from the provider.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_disable.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



The `spock.sub_disable()` function disables a subscription and disconnects
from the provider.

## Synopsis {#synopsis}

```sql
spock.sub_disable(subscription_name name, immediate boolean DEFAULT false)
```

## Arguments {#arguments}

The function accepts the following arguments:

- `subscription_name` - The name of an existing subscription.
- `immediate` - If `true`, the subscription is disabled immediately; otherwise
  it is disabled at the end of the current transaction. The default is `false`.

## Example {#example}

In the following example, the `spock.sub_disable()` function disables a
subscription named `sub_n1_n2`:

```sql
SELECT spock.sub_disable('sub_n1_n2');
 sub_disable
-------------
 t
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_disable.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
