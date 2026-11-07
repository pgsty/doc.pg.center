---
title: create
description: Create a DocumentDB collection or view and configure its supported options.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/create.md
weight: 20
---

Creates a collection or view in the current database.

## Syntax {#syntax}

```javascript
db.createCollection("airports")
db.createView("delayed_flights", "flights", [{ $match: { status: "Delayed" } }])
```

The view uses the [airline example dataset](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset). Run the `airports` creation before inserting the airport examples; it creates an empty collection.

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`create`** | (Required) A string specifying the non-empty collection or view name. |
| **`viewOn`** | (Optional) A string specifying the source collection or view in the same database. |
| **`pipeline`** | (Optional) An array specifying the view aggregation pipeline; requires `viewOn`. `$out`, `$merge`, and `$changeStream` are not allowed in a view definition. |
| **`validator`** | (Optional) A document specifying the schema validation rules; requires schema validation to be enabled. |
| **`validationLevel`** | (Optional) A string selecting `off`, `strict`, or `moderate`; requires schema validation support. |
| **`validationAction`** | (Optional) A string selecting `error` or `warn`; requires schema validation support. |
| **`collation`** | (Optional) A document specifying the default collection comparison rules. Requires collation and collection-collation support. |
| **`statsEnabled`** | (Optional) A boolean-like value provided as a DocumentDB extension controlling collection planner statistics. |
| **`changeStreamPreAndPostImages`** | (Optional) A document with the following behavior: `{ enabled: <boolean> }`; requires pre-image support and cluster version 0.112 or later. Rejected if unavailable. |
| **`enableUpdateDescription`** | (Optional) A boolean-like value provided as a DocumentDB extension controlling change-stream update descriptions. |
| **`comment`** | (Optional) A string carrying trace context for gateway request tracing; see [common request fields](/documentdb/reference/commands/diagnostic/wire-protocol/). |
{.fields}

`validator`, `validationLevel`, and `validationAction` are rejected when schema validation is disabled. When enabled, `null` or undefined values mean no explicit setting. See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for shared metadata and source scope.

## Implementation {#implementation}

Source: `pg_documentdb/src/commands/create_collection_view.c`, `ParseCreateSpec`, and `pg_documentdb/src/metadata/collection.c`.
