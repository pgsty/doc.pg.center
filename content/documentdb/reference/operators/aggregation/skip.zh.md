---
title: $skip
description: 聚合流水线中的 $skip 流水线阶段用于跳过输入中的指定数量文档，并将剩余文档传递给流水线中的下一阶段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$skip.md
weight: 310
translation_source_sha256: 51b8e0207fe07d2aed224192aed631c215440a1f2425f987107d79a3f642d922
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 $skip 流水线阶段用于跳过输入中的指定数量文档，并将剩余文档传递给流水线中的下一阶段。该阶段适用于在查询中实现分页，以及控制后续流水线阶段操作的文档子集。

## 语法 {#syntax}

```javascript
{
  $skip: <number>
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`number`** | 在将剩余文档传递给下一阶段之前跳过的文档数量。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
    _id: '0fcc0bf0-ed18-4ab8-b558-9848e18058f4',
    name: 'First Up Consultants | Beverage Shop - Satterfieldmouth',
    location: { lat: -89.2384, lon: -46.4012 },
    staff: { employeeCount: { fullTime: 2, partTime: 20 } },
    sales: {
      salesByCategory: [
        { categoryName: 'Wine Accessories', totalSales: 34450 },
        { categoryName: 'Bitters', totalSales: 39496 },
        { categoryName: 'Rum', totalSales: 1734 }
      ],
      revenue: 75670
    },
    promotionEvents: [
      {
        eventName: 'Unbeatable Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 7, Day: 2 }
        },
        discounts: [
          { categoryName: 'Whiskey', discountPercentage: 7 },
          { categoryName: 'Bitters', discountPercentage: 15 },
          { categoryName: 'Brandy', discountPercentage: 8 },
          { categoryName: 'Sports Drinks', discountPercentage: 22 },
          { categoryName: 'Vodka', discountPercentage: 19 }
        ]
      },
      {
        eventName: 'Steal of a Deal Days',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 29 }
        },
        discounts: [
          { categoryName: 'Organic Wine', discountPercentage: 19 },
          { categoryName: 'White Wine', discountPercentage: 20 },
          { categoryName: 'Sparkling Wine', discountPercentage: 19 },
          { categoryName: 'Whiskey', discountPercentage: 17 },
          { categoryName: 'Vodka', discountPercentage: 23 }
        ]
      },
      {
        eventName: 'Summer Sale',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 1 },
          endDate: { Year: 2024, Month: 6, Day: 15 }
        },
        discounts: [ { categoryName: 'DJ Speakers', discountPercentage: 20 } ]
      }
    ],
    company: 'First Up Consultants',
    city: 'Satterfieldmouth',
    storeOpeningDate: ISODate("2024-09-20T18:28:57.302Z"),
    lastUpdated: Timestamp({ t: 1729448937, i: 1 }),
    store: { promotionEvents: null },
    tag: [ '#ShopLocal' ]
  }
```

### 示例 1：在集合中跳过文档 {#example-1-skipping-documents-in-a-collection}

要跳过前 2 个文档并返回其余文档，可以使用以下聚合流水线：

```javascript
db.stores.aggregate([
  { $skip: 2 }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
    "store": {
      "name": "Uptown Store",
      "promotionEvents": ["Back to School", "Winter Sale"]
    }
  }
]
```

### 示例 2：跳过文档后再限制结果 {#example-2-skipping-documents-and-then-limiting-the-result}

要跳过前 2 个文档，然后将结果限制为接下来的 3 个文档，可以将 $skip 与 $limit 结合使用：

```javascript
db.stores.aggregate([
  { $skip: 2 },
  { $limit: 3 }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "728c068a-638c-40af-9172-8ccfa7dddb49",
        "name": "Contoso, Ltd. | Book Store - Lake Myron",
        "location": {
            "lat": 29.416,
            "lon": 21.5231
        },
        "staff": {
            "employeeCount": {
                "fullTime": 7,
                "partTime": 16
            }
        },
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Science Fiction",
                    "totalSales": 34879
                }
            ],
            "revenue": 34879
        },
        "promotionEvents": [
            {
                "eventName": "Blowout Bonanza",
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
                        "categoryName": "Children's Books",
                        "discountPercentage": 11
                    },
                    {
                        "categoryName": "Fiction",
                        "discountPercentage": 21
                    }
                ]
            }
        ],
        "company": "Contoso, Ltd.",
        "city": "Lake Myron",
        "storeOpeningDate": "ISODate('2024-09-28T18:23:21.591Z')",
        "lastUpdated": "Timestamp({ t: 1730139801, i: 1 })",
        "storeFeatures": 239
    },
    {
        "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
        "name": "Fourth Coffee | Storage Solution Gallery - Port Camilla",
        "location": {
            "lat": 78.3889,
            "lon": 0.6784
        },
        "staff": {
            "employeeCount": {
                "fullTime": 17,
                "partTime": 15
            }
        },
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Storage Boxes",
                    "totalSales": 2236
                }
            ],
            "revenue": 2236
        },
        "promotionEvents": [
            {
                "eventName": "Major Discount Mania",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 6,
                        "Day": 23
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 7,
                        "Day": 3
                    }
                },
                "discounts": [
                    {
                        "categoryName": "Bathroom Storage",
                        "discountPercentage": 19
                    },
                    {
                        "categoryName": "Kitchen Storage",
                        "discountPercentage": 10
                    }
                ]
            },
            {
                "eventName": "Flash Deal Frenzy",
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
                        "categoryName": "Under-Bed Storage",
                        "discountPercentage": 20
                    },
                    {
                        "categoryName": "Closet Organizers",
                        "discountPercentage": 21
                    }
                ]
            }
        ],
        "company": "Fourth Coffee",
        "city": "Port Camilla",
        "storeOpeningDate": "ISODate('2024-09-23T06:02:53.844Z')",
        "lastUpdated": "Timestamp({ t: 1729663373, i: 1 })",
        "storeFeatures": 222
    }
]
```

### 示例 3：在复杂流水线中跳过文档 {#example-3-skipping-documents-in-a-complex-pipeline}

要跳过第一个促销事件，然后为特定商店投影剩余事件：

```javascript
db.stores.aggregate([
  { $match: { "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4", } },
  { $unwind: "$promotionEvents" },
  { $skip: 1 },
  { $project: { "promotionEvents": 1, _id: 0 } }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "promotionEvents": {
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
    },
    {
        "promotionEvents": {
            "eventName": "Summer Sale",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 1
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 15
                }
            },
            "discounts": [
                {
                    "categoryName": "DJ Speakers",
                    "discountPercentage": 20
                }
            ]
        }
    }
]
```
