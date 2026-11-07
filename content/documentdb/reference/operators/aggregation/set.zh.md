---
title: $set
description: DocumentDB 中的 $set 运算符将字段更新为指定值，或创建具有指定值的新字段
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$set.md
weight: 290
translation_source_sha256: 2ab6266b35ad3e1b5f144c481ddb75c2e5ad188c973be908e46098ccf441e4c7
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$set` 运算符将现有字段更新为指定值；如果字段不存在，则创建字段并赋予该值。可以更新或创建列出的一个或多个字段。使用点表示法可更新或创建嵌套对象。

## 语法 {#syntax}

```javascript
{
  $set: {
    newField: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`newField`** | 要更新或创建的字段名称 |
| **`expression`** | 定义新字段或更新后字段值的表达式 |
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

<span id="example-1-update-an-existing-field"></span>

### 示例 1 - 更新现有字段 {#example-1---update-an-existing-field}

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

### 示例 2 - 更新嵌套对象中的现有字段 {#example-2---update-an-existing-field-in-a-nested-object}

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

### 示例 3 - 创建不存在的新字段 {#example-3---create-a-new-field-that-does-not-exist}

创建一个名为 "formerName" 的新字段，用于存储商店的旧名称。

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

### 示例 4 - 在嵌套对象中创建新字段 {#example-4---create-a-new-field-in-a-nested-object}

在嵌套的 totalStaff 对象中创建一个新字段，用于指定临时员工的数量。

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

### 示例 5 - 更新多个字段 {#example-5---update-multiple-fields}

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
