---
title: $setOnInsert
description: $setOnInsert 运算符仅在 upsert 操作插入新文档时设置字段值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/field-update/$setoninsert.md
weight: 50
translation_source_sha256: e8663b8ec1f0f8e49ead124c928142f66535c2275ca1afd5d285cfa3ef6f9e59
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$setOnInsert` 运算符仅在 upsert 操作插入新文档时设置字段值。如果文档已存在且正在更新，`$setOnInsert` 运算符不会产生任何影响。该运算符特别适用于设置仅应在创建新文档时应用的默认值或初始化数据。

## 语法 {#syntax}

```javascript
{
  $setOnInsert: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 仅在插入时设置的字段名称。可以是顶层字段，也可以使用点号表示法指定嵌套字段。 |
| **`value`** | 仅在插入新文档时赋给字段的值。可以是任意有效的 BSON 类型。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

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

<span id="example-1-basic-set-on-insert-usage"></span>

### 示例 1：$setOnInsert 的基本用法 {#example-1-basic-setoninsert-usage}

创建或更新商店记录，但仅在创建新商店时设置某些初始化字段。

```javascript
db.stores.updateOne(
  { "_id": "new-store-001" },
  {
    $set: {
      "name": "Trey Research Electronics - Downtown",
      "sales.totalSales": 0
    },
    $setOnInsert: {
      "createdDate": new Date(),
      "status": "new",
      "staff.totalStaff.fullTime": 0,
      "staff.totalStaff.partTime": 0,
      "version": 1
    }
  },
  { upsert: true }
)
```

此操作返回以下结果。

```json
{
  acknowledged: true,
  insertedId: 'new-store-001',
  matchedCount: 0,
  modifiedCount: Long("0"),
  upsertedCount: 1
}
```

由于 `_id: "new-store-001"` 的文档不存在，此操作会创建以下新文档：

```json
{
  "_id": "new-store-001",
  "name": "Trey Research Electronics - Downtown",
  "sales": {
    "totalSales": 0
  },
  "createdDate": ISODate("2025-06-05T10:30:00.000Z"),
  "status": "new",
  "staff": {
    "totalStaff": {
      "fullTime": 0,
      "partTime": 0
    }
  },
  "version": 1
}
```

<span id="example-2-set-on-insert-with-existing-document"></span>

### 示例 2：对已有文档使用 $setOnInsert {#example-2-setoninsert-with-existing-document}

现在尝试使用不同的值，再次对同一文档执行 upsert：

```javascript
db.stores.updateOne(
  { "_id": "new-store-001" },
  {
    $set: {
      "name": "Trey Research Electronics - Downtown Branch",
      "sales.totalSales": 5000
    },
    $setOnInsert: {
      "createdDate": new Date(),
      "status": "updated",
      "staff.totalStaff.fullTime": 10,
      "staff.totalStaff.partTime": 5,
      "version": 2
    }
  },
  { upsert: true }
)
```

由于文档已存在，只会应用 `$set` 操作，`$setOnInsert` 将被忽略：

```json
{
  "_id": "new-store-001",
  "name": "Trey Research Electronics - Downtown Branch",
  "sales": {
    "totalSales": 5000
  },
  "createdDate": ISODate("2025-06-05T10:30:00.000Z"),
  "status": "new",
  "staff": {
    "totalStaff": {
      "fullTime": 0,
      "partTime": 0
    }
  },
  "version": 1
}
```

<span id="example-3-complex-set-on-insert-with-nested-objects"></span>

### 示例 3：对嵌套对象使用复杂的 $setOnInsert 操作 {#example-3-complex-setoninsert-with-nested-objects}

可以使用 `$setOnInsert` 初始化复杂的嵌套结构：

```javascript
db.stores.updateOne(
  { "name": "Adatum Gaming Paradise - Mall Location" },
  {
    $set: {
      "location.lat": 35.6762,
      "location.lon": 139.6503
    },
    $setOnInsert: {
      "_id": "gaming-store-mall-001",
      "createdDate": new Date(),
      "status": "active",
      "staff": {
        "totalStaff": {
          "fullTime": 8,
          "partTime": 12
        },
        "manager": "Alex Johnson",
        "departments": ["gaming", "accessories", "repairs"]
      },
      "sales": {
        "totalSales": 0,
        "salesByCategory": []
      },
      "operatingHours": {
        "weekdays": "10:00-22:00",
        "weekends": "09:00-23:00"
      },
      "metadata": {
        "version": 1,
        "source": "store-management-system"
      }
    }
  },
  { upsert: true }
)
```

<span id="example-4-using-set-on-insert-with-arrays"></span>

### 示例 4：对数组使用 $setOnInsert {#example-4-using-setoninsert-with-arrays}

可以初始化数组和复杂的数据结构：

```javascript
db.stores.updateOne(
  { "address.city": "New Tech City" },
  {
    $set: {
      "name": "Future Electronics Hub",
      "sales.totalSales": 25000
    },
    $setOnInsert: {
      "_id": "future-electronics-001",
      "establishedDate": new Date(),
      "categories": ["electronics", "gadgets", "smart-home"],
      "promotionEvents": [],
      "ratings": {
        average: 0,
        count: 0,
        reviews: []
      },
      "inventory": {
        lastUpdated: new Date(),
        totalItems: 0,
        lowStockAlerts: []
      }
    }
  },
  { upsert: true }
)
```

> [!IMPORTANT]
> 
> `$setOnInsert` 运算符仅在 upsert 操作（`{ upsert: true }`）中生效。
> 
> 如果文档已存在，`$setOnInsert` 中的字段将被完全忽略。
> 
> `$setOnInsert` 常与 `$set` 搭配，在单次操作中处理更新和插入两种情况。
> 
> 可以将 `$setOnInsert` 与 `$inc`、`$push` 等其他更新运算符组合使用。
> 
> `$setOnInsert` 运算符非常适合设置创建时间戳、默认值和初始化数据。
