---
title: collStats
description: Return collection statistics in DocumentDB with a configurable size scale.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/collStats.md
weight: 10
---

Returns collection statistics, including document count, document size, storage size, and index sizes.

```javascript
db.flights.stats({ scale: 1024 })
```

The shell's `stats()` helper obtains collection statistics through aggregation. The fields below describe the direct `collStats` wire request.

| Parameter | Description |
| --- | --- |
| **`collStats`** | (Required) A string specifying the collection name. |
| **`scale`** | (Optional) A number specifying the scale divisor for applicable byte-size fields; defaults to `1`. Numeric BSON types are accepted and the backend truncates the value to an integer. |
{.fields}

`null` or undefined `scale` uses `1`; invalid types and invalid scale values fail. Options of the aggregation [`$collStats`](/documentdb/reference/operators/aggregation/collstats/) stage, such as `latencyStats` or `queryExecStats`, are not options forwarded by this wire-command adapter.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: gateway `processor/data_management.rs`, `process_coll_stats`, and backend `pg_documentdb/src/commands/coll_stats.c`.
