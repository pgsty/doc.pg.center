---
title: spock.sub_show_table
description: The spock.subshowtable() function displays the synchronization status of a table.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
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

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
