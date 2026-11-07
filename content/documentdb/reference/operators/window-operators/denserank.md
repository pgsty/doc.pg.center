---
title: $denseRank
description: The $denseRank operator assigns and returns a positional ranking for each document within a partition
  based on a specified sort order
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$denserank.md
weight: 30
---

The `$denseRank` operator sorts documents on one or more fields within a partition and assigns a ranking for each document relative to other documents in the result set.

## Syntax {#syntax}

```javascript
{
  $denseRank: {}
}
```

## Examples {#examples}

Consider this sample document from the stores collection.

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

<span id="example-1-retrieve-a-document-rank-for-each-store"></span>

### Example 1 - Retrieve a document rank for each store {#example-1---retrieve-a-document-rank-for-each-store}

To calculate a document rank for each store under the First Up Consultants company, first run a query to filter on the company, then sort the resulting documents in descending order of sales and assign a document rank to each document in the sorted result set.

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["First Up Consultants"]
        }
    }
}, {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "sales.totalSales": -1
        },
        "output": {
            "denseRank": {
                "$denseRank": {}
            }
        }
    }
}, {
    "$project": {
        "company": 1,
        "sales.totalSales": 1,
        "denseRank": 1
    }
}])
```

The first five results returned by this query are:

```json
[
    {
        "_id": "a0386810-b6f8-4b05-9d60-e536fb2b0026",
        "sales": {
            "revenue": 327583
        },
        "company": "First Up Consultants",
        "denseRank": 1
    },
    {
        "_id": "ad8af64a-d5bb-4162-9bb6-e5104126566d",
        "sales": {
            "revenue": 288582
        },
        "company": "First Up Consultants",
        "denseRank": 2
    },
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "sales": {
            "revenue": 279183
        },
        "company": "First Up Consultants",
        "denseRank": 3
    },
    {
        "_id": "cd3d3782-17d1-451e-8b0f-4f10a68a8db7",
        "sales": {
            "revenue": 271604
        },
        "company": "First Up Consultants",
        "denseRank": 4
    },
    {
        "_id": "63ac4722-fc87-4526-a5e0-b5767d2807f7",
        "sales": {
            "revenue": 260409
        },
        "company": "First Up Consultants",
        "denseRank": 5
    }
]
```
