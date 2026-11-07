---
title: $set
description: The $set operator in DocumentDB updates or creates a new field with a specified value
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$set.md
weight: 290
---

The `$set` operator updates an existing field or creates a new field with the specified value if it does not exist. One or more fields listed are updated or created. The dot notation is used to update or create nested objects.

## Syntax {#syntax}

```javascript
{
  $set: {
    newField: <expression>
  }
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`newField`** | The name of the field to update or create|
| **`expression`** | The expression that defines the value of the new or updated field|
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

<span id="example-1-update-an-existing-field"></span>

### Example 1 - Update an existing field {#example-1---update-an-existing-field}

```javascript
db.stores.updateOne({
		_id: "8eefe8bd-5d6f-4038-90e8-05a8277637f0"
	},
	{
		$set: {
			name: "Lakeshore Retail"
		}
	})
```

<span id="example-2-update-an-existing-field-in-a-nested-object"></span>

### Example 2 - Update an existing field in a nested object {#example-2---update-an-existing-field-in-a-nested-object}

```javascript
db.stores.updateOne({
		_id: "8eefe8bd-5d6f-4038-90e8-05a8277637f0"
	},
	{
		$set: {
			"staff.totalStaff.partTime": 9
		}
	})
```

<span id="example-3-create-a-new-field-that-does-not-exist"></span>

### Example 3 - Create a new field that does not exist {#example-3---create-a-new-field-that-does-not-exist}

Create a new field called "formerName" with the old name of the store.

```javascript
db.stores.updateOne({
		_id: "8eefe8bd-5d6f-4038-90e8-05a8277637f0"
	},
	{
		$set: {
			formerName: "Tailwind Traders | Drone Shoppe - New Theodora"
		}
	})
```

<span id="example-4-create-a-new-field-in-a-nested-object"></span>

### Example 4 - Create a new field in a nested object {#example-4---create-a-new-field-in-a-nested-object}

Create a new field within the nested totalStaff object to specify a count of temporary staff members.

```javascript
db.stores.updateOne({
		_id: "8eefe8bd-5d6f-4038-90e8-05a8277637f0"
	},
	{
		$set: {
			"staff.totalStaff.temporary": 3
		}
	})
```

<span id="example-5-update-multiple-fields"></span>

### Example 5 - Update multiple fields {#example-5---update-multiple-fields}

```javascript
db.stores.updateOne({
		_id: "8eefe8bd-5d6f-4038-90e8-05a8277637f0"
	},
	{
		$set: {
			"staff.totalStaff.partTime": 9,
			"sales.totalSales": 3611
		}
	})
```
