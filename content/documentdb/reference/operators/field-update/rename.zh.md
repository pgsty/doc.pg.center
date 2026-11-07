---
title: $rename
description: $rename 运算符可在更新操作中重命名文档字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/field-update/$rename.md
weight: 40
translation_source_sha256: cf2cf4efabb821ac6204ef4d760799b562ccee6395c53c4fd60d6ab674846d6a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$rename` 运算符用于在更新操作中重命名文档字段。它删除旧名称的字段，创建具有指定名称的新字段，并保留原始值。该运算符可用于重构文档模式或修正字段命名约定。

## 语法 {#syntax}

```javascript
{
  $rename: {
    <field1>: <newName1>,
    <field2>: <newName2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要重命名的字段的当前名称。 |
| **`newName`** | 字段的新名称。 |
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

### 示例 1：重命名顶层字段 {#example-1-renaming-top-level-fields}

要将 `name` 字段重命名为 `storeName`，并将 `location` 重命名为 `storeLocation`，可对这两个字段使用 $rename 运算符。

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $rename: {
      "name": "storeName",
      "location": "storeLocation"
    }
  }
)
```

### 示例 2：重命名嵌套字段 {#example-2-renaming-nested-fields}

也可以使用点号表示法重命名嵌套字段。

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $rename: {
      "location.lat": "location.latitude",
      "location.lon": "location.longitude",
      "staff.totalStaff.fullTime": "staff.totalStaff.fullTimeEmployees"
    }
  }
)
```

### 示例 3：批量重命名操作 {#example-3-bulk-rename-operations}

可以使用 `updateMany()` 重命名多个文档中的字段。

```javascript
db.stores.updateMany(
  {},
  {
    $rename: {
      "sales.totalSales": "sales.revenue",
      "staff.totalStaff": "staff.employeeCount"
    }
  }
)
```

> [!IMPORTANT]
> 
> 如果 `$rename` 指定的字段不存在，该操作不会对该字段产生任何影响。
> 
> 如果新字段名称已存在，`$rename` 操作会覆盖已有字段。
> 
> `$rename` 运算符不能用于重命名数组元素或数组元素内的字段。
> 
> 字段名称不能是空字符串，也不能包含空字符。
