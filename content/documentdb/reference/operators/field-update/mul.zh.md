---
title: $mul
description: $mul 运算符将字段值乘以指定数值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/field-update/$mul.md
weight: 30
translation_source_sha256: c9147e6d0be45664b3a4897c7dd6ced3b8a88983988c94817531f3f6d9f6da5e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$mul` 运算符将字段值乘以指定数值。如果字段不存在，`$mul` 会创建该字段并将其设置为零。该运算符可用于按百分比调整数值、缩放数值，或对数值字段执行批量计算。

## 语法 {#syntax}

```javascript
{
  $mul: {
    <field1>: <number1>,
    <field2>: <number2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要执行乘法的字段名称。 |
| **`number`** | 字段值所乘的数。必须为数值。 |
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

### 示例 1：按百分比增加 {#example-1-applying-percentage-increase}

将总销售额增加 10%（乘以 1.1）。这会将 `totalSales` 从 24863 改为 27349.3（24863 × 1.1）。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "sales.totalSales": 1.1
    }
  }
)
```

### 示例 2：应用折扣 {#example-2-applying-discount}

对销售额应用 20% 的折扣（乘以 0.8）。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "sales.totalSales": 0.8
    }
  }
)
```

### 示例 3：操作多个字段 {#example-3-multiple-field-operations}

同时对多个字段应用不同的乘数。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "staff.totalStaff.fullTime": 1.5,
      "staff.totalStaff.partTime": 2,
      "sales.totalSales": 1.25
    }
  }
)
```

这将执行以下操作：

- 将 `fullTime` 从 8 增加到 12（8 × 1.5）
- 将 `partTime` 从 5 增加到 10（5 × 2）
- 将 `totalSales` 增加 25%（乘以 1.25）

### 示例 4：创建新字段 {#example-4-creating-new-fields}

如果字段不存在，`$mul` 会创建该字段并将其设置为 0。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "sales.bonusPoints": 100,
      "staff.overtimeHours": 40
    }
  }
)
```

将创建 `bonusPoints` 和 `overtimeHours` 两个字段，值均为 0。

### 示例 5：使用小数 {#example-5-working-with-decimals}

使用精确的小数乘数进行财务计算。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "sales.totalSales": 0.915
    }
  }
)
```

### 示例 6：更新数组元素 {#example-6-updating-array-elements}

使用位置运算符，对数组中的特定元素应用乘数。

```javascript
db.stores.updateOne(
  {
    "_id": "438db151-04b8-4422-aa97-acf94bc69cfc",
    "sales.salesByCategory.categoryName": "Direct-Drive Turntables"
  },
  {
    $mul: {
      "sales.salesByCategory.$.totalSales": 1.15
    }
  }
)
```

### 示例 7：负值和零 {#example-7-negative-values-and-zero}

处理负乘数和零值。

```javascript
db.stores.updateOne(
  { "_id": "438db151-04b8-4422-aa97-acf94bc69cfc" },
  {
    $mul: {
      "sales.totalSales": -1,
      "staff.totalStaff.fullTime": 0
    }
  }
)
```

这将执行以下操作：

- 将 `totalSales` 变为负值（适用于冲销）
- 将 `fullTime` 设置为 0

对员工人数应用 1.5 的乘数、对销售额应用 1.25 的乘数后，文档将更新如下：

```json
{
  "_id": "438db151-04b8-4422-aa97-acf94bc69cfc",
  "name": "Fourth Coffee | Turntable Boutique - Tromptown",
  "staff": {
    "totalStaff": {
      "fullTime": 12,
      "partTime": 10
    },
    "overtimeHours": 0
  },
  "sales": {
    "totalSales": 31078.75,
    "bonusPoints": 0,
    "salesByCategory": [
      {
        "categoryName": "Direct-Drive Turntables",
        "totalSales": 28592.45
      }
    ]
  }
}
```
