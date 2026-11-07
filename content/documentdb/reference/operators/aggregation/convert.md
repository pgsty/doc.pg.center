---
title: $convert
description: The $convert operator converts an expression into the specified type
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$convert.md
weight: 60
---

The $convert operator converts an expression into a value of the specified type.

## Syntax {#syntax}

```javascript
{
    $convert: {
        input: < expression > ,
        to: < type > ,
        format: < binData format > ,
        onError: < value to return on error > ,
        onNull: < value to return on null >
    }
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`input`** | The input value to be converted to the specified type|
| **`to`** | The type to convert the input value into|
| **`format`** | (Optional) The binData format of the input or output when converting a value to or from binData|
| **`onError`** | (Optional) The value to return when the conversion of the input to the specified type fails|
| **`onNull`** | (Optional) The value to return when the input value to be converted to the specified type is null or missing|
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

### Example 1: Convert an Int value into a String {#example-1-convert-an-int-value-into-a-string}

To convert the fullTime field from an integer to a string, run a query using the $convert operator to make the conversion.

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsString: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "string"
            }
        }
    }
}])
```

This query returns the following result:

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "fulltimeStaff": 3,
        "fulltimeStaffAsString": "3"
    }
]
```

### Example 2: Convert an Int value into a Boolean value {#example-2-convert-an-int-value-into-a-boolean-value}

To convert the fullTime field from an integer to a boolean, run a query using the $convert operator to make the conversion. Any positive value for the fullTime field will be converted to true.

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsBool: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "bool"
            }
        }
    }
}])
```

This query returns the following result:

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "fulltimeStaff": 3,
        "fulltimeStaffAsBool": true
    }
]
```

### Example 3: Convert an Int value into a Decimal value {#example-3-convert-an-int-value-into-a-decimal-value}

To convert the fullTime staff field from an integer to a decimal value, run a query using the $convert operator to make the conversion.

```javascript
db.stores.aggregate([{
    $match: {
        _id: "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
}, {
    $project: {
        fulltimeStaff: "$staff.totalStaff.fullTime",
        fulltimeStaffAsDecimal: {
            $convert: {
                input: "$staff.totalStaff.fullTime",
                to: "decimal"
            }
        }
    }
}])
```

This query returns the following result:

```json
[
    {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
        "fulltimeStaff": 3,
        "fulltimeStaffAsDecimal": "Decimal128('3')"
    }
]
```
