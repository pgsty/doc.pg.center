---
title: listDatabases
description: List logical DocumentDB databases and filter the returned metadata.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/listDatabases.md
weight: 50
---

Lists logical databases. Run against `admin`.

```javascript
db.getMongo().getDBs({ nameOnly: true, filter: { name: "bookings" } })
```

| Parameter | Description |
| --- | --- |
| **`listDatabases`** | (Required) A command marker, conventionally `1`. |
| **`nameOnly`** | (Optional) A boolean-like value that returns database names without size fields; defaults to `false`. |
| **`filter`** | (Optional) A document that filters the returned database documents. |
{.fields}

The default implementation reports placeholder per-database `sizeOnDisk: 0` and `empty: false`; `totalSize` measures the underlying PostgreSQL database, not the sum of separately measured logical-database sizes. `authorizedDatabases` is not recognized. This command returns a `databases` array, not a cursor.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: `pg_documentdb/src/commands/db_stats.c`, `command_list_databases`.
