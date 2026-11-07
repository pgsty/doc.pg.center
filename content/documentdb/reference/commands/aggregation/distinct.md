---
title: Distinct
description: The distinct command is used to find the unique values for a specified field across a single collection.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/aggregation/distinct.md
weight: 30
---

The `distinct` command is used to find the unique values for a specified field across a single collection. This command is useful when you need to identify the set of distinct values for a field without retrieving all the documents or when you need to perform operations like filtering or grouping based on unique values.

Returns unique values for a field path in `values`. This command does not create a cursor, so its result is not continued with `getMore`.

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`distinct`** | (Required) A string specifying the collection name. |
| **`key`** | (Required) A string specifying the field path. |
| **`query`** | (Optional) A document specifying the match filter; omitted or `null` means no filter. |
| **`hint`** | (Optional) A string or document specifying the index name or key pattern. |
| **`maxTimeMS`** | (Optional) A number specifying the execution timeout in milliseconds. |
| **`collation`** | (Optional) A document specifying the comparison rules; requires `documentdb_core.enableCollation` and cluster version 1.1 or later. Rejected otherwise. |
{.fields}

## Example: list arrival airports from one departure airport {#example-list-arrival-airports-from-one-departure-airport}

Using the [airline example dataset](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset):

```javascript
db.flights.distinct("arrival_airport", { departure_airport: "SVO" }, { maxTimeMS: 5000 })
```

The returned array contains `"LED"` and `"KZN"`. The helper extracts the command response's `values` array. Do not depend on the order of distinct values.

To collect fare classes from the embedded ticket segments instead:

```javascript
db.flights.distinct("segments.fare_conditions")
```

The values are `"Economy"` and `"Business"`, without duplicates.

## Shell syntax {#shell-syntax}

```javascript
db.collection.distinct(field, query, options)
```

## Detailed Examples {#detailed-examples}

Here are examples using the provided sample JSON structure.

### Example 1: Find distinct categories in sales {#example-1-find-distinct-categories-in-sales}

To find the distinct `categoryName` in the `salesByCategory` array:

```javascript
db.stores.distinct("sales.salesByCategory.categoryName")
```

#### Sample output {#sample-output}

```json
[
  "Music Theory Books",
  "Superfoods",
  "Harmonicas",
  "Garden Tools"
]
```

### Example 2: Find distinct event names in promotion events {#example-2-find-distinct-event-names-in-promotion-events}

To find the distinct `eventName` in the `promotionEvents` array:

```javascript
db.stores.distinct("promotionEvents.eventName")
```

#### Sample output {#sample-output-1}

```json
[
  "Super Saver Celebration",
  "Incredible Discount Days"
]
```

### Example 3: Find distinct discount percentages for a specific event {#example-3-find-distinct-discount-percentages-for-a-specific-event}

To find the distinct `discountPercentage` in the `discounts` array for the "Summer Sale" event:

```javascript
db.stores.distinct("promotionEvents.discounts.discountPercentage", { "promotionEvents.eventName": "Incredible Discount Days" })
```

#### Sample output {#sample-output-2}

```json
[
  6, 17, 22, 25, 9, 15, 14,
  7, 12, 19, 24, 5, 20, 10,
  23, 16, 18, 21, 13, 11, 8
]
```

## Implementation {#implementation}

Source: `pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`, `GenerateDistinctQuery`. See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for source scope and shared metadata.
