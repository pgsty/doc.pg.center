---
title: $currentOp
description: The $currentOp stage returns information on active and queued operations for the database.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$currentop.md
weight: 70
---

The `$currentOp` stage returns a stream of documents containing information on active and queued operations for the database instance. This stage must be the first stage in the pipeline and is run on the `admin` database.

## Syntax {#syntax}

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    {
      $currentOp: {
        allUsers: <boolean>,
        idleConnections: <boolean>,
        idleCursors: <boolean>,
        idleSessions: <boolean>,
        localOps: <boolean>
      }
    }
  ],
  cursor: {}
})
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`allUsers`** | Optional. Boolean. If `true`, reports operations for all users. Default: `false`. |
| **`idleConnections`** | Optional. Boolean. If `true`, reports on idle connections. Default: `false`. |
| **`idleCursors`** | Optional. Boolean. If `true`, reports on idle cursors. Default: `false`. |
| **`idleSessions`** | Optional. Boolean. If `true`, reports on idle sessions. Default: `false`. |
| **`localOps`** | Optional. Boolean. If `true`, reports operations running locally on the current instance. Default: `false`. |
{.fields}

## Examples {#examples}

### Example 1: List active operations {#example-1-list-active-operations}

Return all currently active operations:

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    { $currentOp: { allUsers: true } }
  ],
  cursor: {}
})
```

### Example 2: Filter active operations {#example-2-filter-active-operations}

Return active operations for a specific database, combined with `$match`:

```javascript
db.adminCommand({
  aggregate: 1,
  pipeline: [
    { $currentOp: { allUsers: true } },
    { $match: { "ns": /^mydb\./ } }
  ],
  cursor: {}
})
```

## Key Takeaways {#key-takeaways}

- **Must be first stage** — `$currentOp` must be the first stage in the aggregation pipeline
- **Admin database only** — this stage must be run against the `admin` database using `db.adminCommand()`
- **Collection-agnostic** — does not operate on a specific collection
