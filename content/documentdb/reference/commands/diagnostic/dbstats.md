---
title: dbStats
description: Return statistics for the current logical DocumentDB database.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/dbStats.md
weight: 50
---

Returns statistics for the current logical database.

```javascript
db.stats({ scale: 1024 })
```

| Parameter | Description |
| --- | --- |
| **`dbStats`** | (Required) A command marker, conventionally `1`; the target database is supplied by the connection's `$db`. |
| **`scale`** | (Optional) A number specifying the divisor for applicable byte-size fields; defaults to `1`. The backend truncates numeric values to an integer. |
{.fields}

`null` or undefined `scale` uses `1`. The default wire adapter forwards only the database and scale, not a `freeStorage` option.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: gateway `processor/data_management.rs`, `process_db_stats`, and backend `pg_documentdb/src/commands/db_stats.c`.
