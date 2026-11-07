---
title: Count
description: Count command is used to count the number of documents in a collection that match a specified query.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/aggregation/count.md
weight: 20
---

The `count` command is used to count the number of documents in a collection that match a specified query. This command is useful for obtaining quick statistics about the data stored in your collections, such as the number of documents that meet certain criteria.

Returns a count in `n`, rather than a cursor. An omitted or empty query without other query modifiers can use collection statistics; supplying a query or hint selects a query-based counting path.

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`count`** | (Required) A string specifying the collection name. |
| **`query`** | (Optional) A document specifying the match filter. Omit it to count the collection without a filter. |
| **`skip`** | (Optional) A non-negative integer that skips this many matches before counting. |
| **`limit`** | (Optional) An integer specifying the maximum count; `0` means no limit. Negative values use their absolute value. |
| **`hint`** | (Optional) A string or document specifying the index name or key pattern; forces the query-based counting path. |
| **`maxTimeMS`** | (Optional) A number specifying the execution timeout in milliseconds. |
| **`collation`** | (Optional) A document specifying the comparison rules; requires `documentdb_core.enableCollation`. |
{.fields}

## Example: count delayed flights {#example-count-delayed-flights}

Using the [airline example dataset](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset):

```javascript
db.flights.count({ status: "Delayed" })
```

The helper returns `2`. Unlike the raw command response, this is a number rather than a document containing `n`.

To count at most one matching flight after skipping the first match:

```javascript
db.flights.count({ departure_airport: "SVO" }, { skip: 1, limit: 1 })
```

This returns `1`. The `count()` helper targets the command documented here; current mongosh marks that helper as deprecated.

## Shell syntax {#shell-syntax}

```javascript
db.collection.count(query, options)
```

## Detailed Examples {#detailed-examples}

Here are some examples to demonstrate the usage of the `count` command:

### Example 1. Counting all documents in a collection {#example-1-counting-all-documents-in-a-collection}

To count all documents in the `stores` collection:

```javascript
db.stores.count({})
```

#### Sample output {#sample-output}

```json
60570
```

### Example 2. Counting documents with specific criteria {#example-2-counting-documents-with-specific-criteria}

To count the number of stores with a specific `_id` store ID:

```javascript
db.stores.count({ "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
```

#### Sample output {#sample-output-1}

```json
1
```

### Example 3. Counting documents with nested criteria {#example-3-counting-documents-with-nested-criteria}

To count the number of stores that have a specific promotion event:

```javascript
db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })   
```

#### Sample output {#sample-output-2}

```json
2156
```

### Example 4. Counting documents with multiple criteria {#example-4-counting-documents-with-multiple-criteria}

To count the number of stores located at a specific latitude and longitude:

```javascript
db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
```

#### Sample output {#sample-output-3}

```json
1
```

## Implementation {#implementation}

Source: `pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`, `GenerateCountQuery`. See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for source scope and shared metadata.
