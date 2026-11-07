---
title: $derivative
description: The $derivative operator calculates the average rate of change of the value of a field within a specified
  window.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$derivative.md
weight: 40
---

> [!NOTE] Edition note
> The parameter table says “rate of range” and calls unit a “time window”; the page definition describes a rate of change. The Chinese translation interprets the obvious “range” typo as “change”, while retaining the source's unit description.

The `$derivative` operator sorts documents on one or more fields within a partition and calculates the average rate of change of a field between the first and last documents within the window.

## Syntax {#syntax}

```javascript
{
    $derivative: {
        input: < expression >,
        unit: < timeWindow >
    }
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`input`** | The expression or the field to calculate the rate of range|
| **`unit`** | The time window for the rate of change|
{.fields}

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

<span id="example-1-calculate-the-derivative-for-total-sales"></span>

### Example 1 - Calculate the derivative for total sales {#example-1---calculate-the-derivative-for-total-sales}

To calculate the derivative of total sales for each store in the First Up Consultants company, first run a query to filter on the company, sort the resulting documents in ascending order of their last updated timestamps, and calculate the derivate (average rate of change) of total sales between the first and current document in the result set.

```javascript
db.stores.aggregate([{
        "$match": {
            "company": {
                "$in": [
                    "First Up Consultants"
                ]
            },
            "$and": [{
                    "lastUpdated": {
                        "$gt": ISODate("2024-12-01T03:06:24.180Z")
                    }
                },
                {
                    "lastUpdated": {
                        "$lt": ISODate("2025-12-01T03:55:17.557Z")
                    }
                }
            ]
        }
    },
    {
        "$setWindowFields": {
            "partitionBy": "$company",
            "sortBy": {
                "lastUpdated": 1
            },
            "output": {
                "storeAverageSales": {
                    "$derivative": {
                        "input": "$sales.totalSales",
                        "unit": "week"
                    },
                    "window": {
                        "range": [
                            -1,
                            0
                        ],
                        "unit": "week"
                    }
                }
            }
        }
    },
    {
        "$project": {
            "lastUpdated": 1,
            "storeAverageSales": 1
        }
    }
])
```

This query returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "lastUpdated": "2025-06-11T10:48:01.291Z",
        "storeAverageSales": 21554495.708753344
    }
]
```
