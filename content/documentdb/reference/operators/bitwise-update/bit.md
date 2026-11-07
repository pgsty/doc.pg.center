---
title: $bit
description: The `$bit` operator is used to perform bitwise operations on integer values.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/bitwise-update/$bit.md
weight: 10
---

The `$bit` operator is used to perform bitwise operations on integer values. It can be used to update integer fields in documents by applying bitwise AND, OR, and XOR operations. Bitwise operators like $bit aren't designed for incrementing values, but for manipulating bits directly (like checking, setting, or clearing specific bits).

## Syntax {#syntax}

```javascript
{
    $bit: {
        < field >: {
            < operator >: < number >
        }
    }
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`<field>`** | The field to perform the bitwise operation on. |
| **`<operator>`** | The bitwise operation to perform. Can be one of: `and`, `or`, `xor`. |
| **`<number>`** | The number to use for the bitwise operation. |
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

<span id="example-1-perform-a-bitwise-and-operation-on-the-part-time-field-in-total-staff"></span>

### Example 1: Perform a bitwise AND operation on the `partTime` field in `totalStaff` {#example-1-perform-a-bitwise-and-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            and: 1
        }
    }
})
```

This query returns the following result.

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

<span id="example-2-perform-a-bitwise-or-operation-on-the-part-time-field-in-total-staff"></span>

### Example 2:  Perform a bitwise OR operation on the `partTime` field in `totalStaff` {#example-2--perform-a-bitwise-or-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            "or": 1
        }
    }
})
```

This query returns the following result.

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

<span id="example-3-perform-a-bitwise-xor-operation-on-the-part-time-field-in-total-staff"></span>

### Example 3: Perform a bitwise XOR operation on the `partTime` field in `totalStaff` {#example-3-perform-a-bitwise-xor-operation-on-the-parttime-field-in-totalstaff}

```javascript
db.stores.updateOne({
    _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
}, {
    $bit: {
        "staff.totalStaff.partTime": {
            "xor": 1
        }
    }
})
```

This query returns the following result.

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```
