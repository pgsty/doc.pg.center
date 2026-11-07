---
title: spock.sub_show_table
description: The spock.subshowtable() function displays the synchronization status of a table.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_show_table.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



The `spock.sub_show_table()` function displays the synchronization status of a
table.

## Synopsis {#synopsis}

```sql
spock.sub_show_table(subscription_name name, relation regclass,
                     OUT nspname text, OUT relname text, OUT status text)
```

## Description {#description}

The `spock.sub_show_table()` function shows the synchronization status of a
table.

## Arguments {#arguments}

The function accepts the following arguments:

- `subscription_name` - The name of an existing subscription.
- `relation` - The name of an existing table, optionally qualified.

## Example {#example}

In the following example, the `spock.sub_show_table()` function displays the
synchronization status of a table named `test` for a subscription named
`sub_n2`:

```sql
SELECT * FROM spock.sub_show_table('sub_n2', 'test');
-[ RECORD 1 ]----
nspname | public
relname | test
status  | unknown
```

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_show_table.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
