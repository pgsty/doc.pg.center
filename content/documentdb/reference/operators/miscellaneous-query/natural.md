---
title: $natural
description: The $natural operator forces the query to use the natural order of documents in a collection, providing
  control over document ordering and retrieval.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/miscellaneous-query/$natural.md
weight: 20
---

The `$natural` operator forces the query to use the natural order of documents in a collection. It can be used in sorting operations to retrieve documents in the order they were inserted or in reverse order. This operator is useful when you need predictable ordering without relying on indexed fields.

## Syntax {#syntax}

```javascript
{
  $natural: <1 | -1>
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`1`** | Sort in forward natural order (insertion order). |
| **`-1`** | Sort in reverse natural order (reverse insertion order). |
{.fields}

## Examples {#examples}

Consider this sample document from the stores collection.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        }
      ]
    }
  ]
}
```

### Example 1: Basic Natural Order Sorting {#example-1-basic-natural-order-sorting}

This query retrieves all stores in the order they were inserted into the collection.

```javascript
db.stores.find({}).sort({
    $natural: 1
})
```

### Example 2: Reverse Natural Order {#example-2-reverse-natural-order}

This query returns all stores in reverse insertion order, with the most recently added documents appearing first.

```javascript
db.stores.find({}).sort({
    $natural: -1
})
```

### Example 3: Natural Order with Filtering {#example-3-natural-order-with-filtering}

This query filters stores with total sales greater than 50,000 and returns them in natural insertion order.

```javascript
db.stores.find({
    "sales.totalSales": {
        $gt: 50000
    }
}).sort({
    $natural: 1
})
```

### Example 4: Natural Order with Projection {#example-4-natural-order-with-projection}

This query returns only the store name, total sales, and location coordinates in natural insertion order.

```javascript
db.stores.find({}, {
  name: 1,
  "sales.totalSales": 1,
  "location.lat": 1,
  "location.lon": 1
}).sort({ $natural: 1 })
```

### Example 5: Natural Order with Limit {#example-5-natural-order-with-limit}

This query returns the first three stores in their natural insertion order.

```javascript
db.stores.find({}).sort({
    $natural: 1
}).limit(3)
```

## Use Cases {#use-cases}

The `$natural` operator is useful in the following scenarios:

- Audit trails: When you need to process documents in the order, they were created
- Chronological processing: For time-sensitive data where insertion order matters
- Batch processing: When processing documents in predictable order without indexes
- Debugging: To understand the natural storage order of documents in a collection
