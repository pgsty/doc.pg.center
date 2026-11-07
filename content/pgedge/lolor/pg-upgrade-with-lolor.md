---
title: Using pg_upgrade with lolor
description: The pgupgrade utility is used for upgrading Postgres versions.
weight: 200
upstream_source: pgedge-lolor
upstream_link: https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/pg_upgrade_with_lolor.md
upstream_modified: true
upstream_ref: ac3893a7707a
source_kind: pinned-main-snapshot
type: docs
---



The `pg_upgrade` utility is used for upgrading Postgres versions.

You can use `pg_upgrade` with the `lolor` extension installed provided that you are using lolor version 1.2.2 or later. If you are using an older version of lolor, you will need to upgrade the extension first.

Both clusters must list `lolor` in `shared_preload_libraries`; without it the new cluster cannot load lolor's library, so restoring the extension fails.

Before running `pg_upgrade`, you must disable `lolor`. After executing pg_upgrade, you can enable lolor.  Use `psql` or another client to disable lolor:

```
db1_17=# SELECT lolor.disable();
```

Next, execute the upgrade. A sample `pg_ugrade` command appears below:

```
# pg_upgrade --old-datadir=/data/db1_17 \
		--new-datadir=/data/db1_18 \
		--old-bindir=/usr/lib/postgresql/17/bin \
		--new-bindir=/usr/lib/postgresql/18/bin \
		--link
```

Then, use psql to enable `lolor`:

```
db1_18=# SELECT lolor.enable();
```

Reconnect any client sessions afterwards. `lolor.enable()` and
`lolor.disable()` change which function OID owns each `pg_catalog.lo_*` name,
and libpq resolves those OIDs once per connection and caches them for the life
of the connection. A session that used a large object before the switch would
otherwise keep calling the previous implementation.

---

[Upstream source](https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/pg_upgrade_with_lolor.md) · `ac3893a7707a` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL License](/pgedge/about/license/).
