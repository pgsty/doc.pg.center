---
title: $gte
description: The $gte operator retrieves documents where the value of a field is greater than or equal to a specified
  value
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$gte.md
weight: 40
---

> [!NOTE] Edition note
> The parameter table omits “or equal to”. As stated in the definition and examples, `$gte` includes equality at the threshold.

The `$gte` operator retrieves documents where the value of a field is greater than or equal to a specified value. The `$gte` operator retrieves documents that meet a minimum threshold for the value of a field.

## Syntax {#syntax}

```javascript
{
    field: {
        $gte: <value>
    }
}
```

## Parameters {#parameters}

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to compare|
| **`value`** | The value that the field should be greater than|
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

<span id="example-1-find-a-store-with-sales-35-000"></span>

### Example 1: Find a store with sales >= $35,000 {#example-1-find-a-store-with-sales--35000}

To retrieve a store with at least $35,000 in sales, first run a query using the $gte operator on the sales.totalSales field. Then project only the name of the store and its total sales and limit the result set to one document.

```javascript
db.stores.find({
    "sales.totalSales": {
        $gte: 35000
    }
}, {
    name: 1,
    "sales.totalSales": 1
}, {
    limit: 1
})
```

The first result returned by this query is:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "sales": { "totalSales": 37701 }
    }
]
```

### Example 2: Find a store with 12 or more full-time staff {#example-2-find-a-store-with-12-or-more-full-time-staff}

To retrieve a store with at least 12 full time staff, first run a query with the $gte operator on the staff.totalStaff.fullTime field. Then, project only the name and full time staff count and limit the results to a single document from the result set.

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        $gte: 12
    }
}, {
    name: 1,
    "staff.totalStaff.fullTime": 1
}, {
    limit: 1
})
```

The first result returned by this query is:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "staff": { "totalStaff": { "fullTime": 18 } }
    }
]
```

### Example 3: Find promotion events with a discount percentage greater than or equal to 15% for Laptops {#example-3-find-promotion-events-with-a-discount-percentage-greater-than-or-equal-to-15-for-laptops}

To find two stores with promotions with a discount of at least 15% for laptops, first run a query to filter stores with laptop promotions. Then use the $gte operator on the discountPercentage field. Lastly, project only the name of the store and limit the results to two documents from the result set.

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        $elemMatch: {
            categoryName: "Laptops",
            discountPercentage: {
                $gte: 15
            }
        }
    }
}, {
    name: 1
}, {
    limit: 2
})
```

The first two results returned by this query are:

```json
[
  {
    "_id": "60e43617-8d99-4817-b1d6-614b4a55c71e",
    "name": "Wide World Importers | Electronics Emporium - North Ayanashire"
  },
  {
    "_id": "3c441d5a-c9ad-47f4-9abc-ac269ded44ff",
    "name": "Contoso, Ltd. | Electronics Corner - New Kiera"
  }
]
```
