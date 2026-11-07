---
title: spock.sub_resync_table
description: The spock.subresynctable() function resynchronizes one existing table.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_resync_table.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



The `spock.sub_resync_table()` function resynchronizes one existing table.

## Synopsis {#synopsis}

```sql
spock.sub_resync_table(subscription_name name, relation regclass, truncate boolean DEFAULT true)
```

## Description {#description}

The `spock.sub_resync_table()` function resynchronizes one existing table.

After the resynchronization is scheduled, the function compares the cached
`spock.node` row of the subscription's provider with the provider's own row.
If they differ, it raises a `WARNING` that suggests
[`spock.node_refresh_info()`](/pgedge/spock/reference/functions/spock-node-refresh-info/). The check does not
change `spock.node`, and a provider that cannot be reached for the check
produces a `WARNING` without failing the resynchronization.

## Arguments {#arguments}

The function accepts the following arguments:

- `subscription_name` - The name of an existing subscription.
- `relation` - The name of an existing table, optionally schema qualified.
- `truncate` - Truncate the table before synchronization; the default value is
  `true`. If you do not include the truncate argument, conflicts between
  existing rows and newly arriving rows may cause errors.

## Example {#example}

In the following example, the `spock.sub_resync_table()` function 
resynchronizes a table named `public.users` for a subscription named
`sub_n1_n2`:

```sql
SELECT spock.sub_resync_table('sub_n1_n2', 'public.users');
 sub_resync_table
------------------
 t
(1 row)
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_resync_table.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
