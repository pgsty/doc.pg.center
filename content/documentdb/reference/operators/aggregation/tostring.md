---
title: $toString
description: The $toString operator converts an expression into a String
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$tostring.md
weight: 410
---

The `$toString` operator simply returns the value of the specified expression as a String.

## Syntax {#syntax}

```javascript
{
    $toString: < expression >
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`expression`** | The specified value to convert into a String value|
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

### Example 1: Convert a Double value into a String value {#example-1-convert-a-double-value-into-a-string-value}

To convert the value of the latitude field from a Double to a String, run a query using the $toString operator on the field to make the conversion.

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalLatitude: "$location.lat",
        latitudeAsString: {
            $toString: "$location.lat"
        }
    }
}])
```

This query returns the following result:

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalLatitude": 72.8377,
        "latitudeAsString": "72.8377"
    }
]
```

### Example 2: Convert an Int value into a String value {#example-2-convert-an-int-value-into-a-string-value}

To convert the value of the totalSales field from an Int to a String, run a query using the $toString operator on the field to make the conversion.

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        originalTotalSales: "$sales.totalSales",
        totalSalesAsString: {
            $toString: "$sales.totalSales"
        }
    }
}])
```

This query returns the following result:

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "originalTotalSales": 9366,
        "totalSalesAsString": "9366"
    }
]
```

This table delineates the expected behavior of the $toString operator based on the data type of the input value.

| **Value Type**                                                         | **Behavior/Output**                  |
|------------------------------------------------------------------------|--------------------------------------|
| Boolean value true                                                     | Output -> "true"                     |
| Boolean value false                                                    | Output -> "false"                    |
| Any Double, Int, Long or Decimal value. For example, 72                | Output -> "72"                       |
| Any ObjectId value. For example, ObjectId("b010763193704acdaafa8ac3")  | Output -> "b010763193704acdaafa8ac3" |
