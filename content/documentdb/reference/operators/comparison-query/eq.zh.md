---
title: $eq
description: $eq 查询运算符将字段值与指定值进行比较
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/comparison-query/$eq.md
weight: 20
translation_source_sha256: d9bc41122bef317dc862543895461ed095337d503ec997e07d60cd7c2603db16
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$eq` 运算符用于匹配字段值等于指定值的文档。$eq 运算符根据查询谓词进行精确匹配筛选，以获取包含特定值、对象和数组的文档。

## 语法 {#syntax}

```javascript
{
    field: {
        $eq: <value>
    }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 要比较的字段。|
| **`value`** | 要与字段进行比较的值。|
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

### 示例 1：使用 $eq 筛选根级字段 {#example-1-use-eq-filter-on-a-root-level-field}

要查找名称为 "Boulder Innovations | Home Security Place - Ankundingburgh" 的商店，可运行查询，使用 $eq 谓词匹配 name 字段，并在结果中仅投影 ID 和 name 字段。

```javascript
db.stores.find({
    name: {
        $eq: "Boulder Innovations | Home Security Place - Ankundingburgh"
    }
}, {
    name: 1
})
```

此查询返回以下结果：

```json
[
    {
        "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
        "name": "Boulder Innovations | Home Security Place - Ankundingburgh"
    }
]
```

### 示例 2：使用 $eq 筛选嵌套字段 {#example-2-use-eq-filter-on-a-nested-field}

要查找总销售额恰好为 $37,015 的商店，可运行查询，使用点号表示法对嵌套字段 sales.totalSales 应用 $eq 运算符。

```javascript
db.stores.find({
    "sales.totalSales": {
        $eq: 37015
    }
}, {
    name: 1,
    "sales.totalSales": 1
})
```

此操作返回以下结果：

```json
[
    {
        "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
        "name": "Boulder Innovations | Home Security Place - Ankundingburgh",
        "sales": { "totalSales": 37015 }
    }
]
```

### 示例 3：对数组中的单个元素使用 $eq {#example-3-use-eq-for-individual-items-in-an-array}

以下查询对嵌套的 promotionEvents.discounts 数组中的单个元素使用相等谓词，以获取文档。

此查询在嵌套的 discounts 数组中查找任意一个相等的对象。

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        $eq: {
            categoryName: "Alarm Systems",
            discountPercentage: 5
        }
    }
}, {
    name: 1
}, {
    limit: 2
})
```

此查询返回以下结果：

```json
[
  {
    "_id": "ece5bf6c-3255-477e-bf2c-d577c82d6995",
    "name": "Proseware, Inc. | Home Security Boutique - Schambergertown"
  },
  {
    "_id": "7baa8fd8-113a-4b10-a7b9-2c116e976491",
    "name": "Tailwind Traders | Home Security Pantry - Port Casper"
  }
]
```

### 示例 4：使用 $eq 匹配整个数组 {#example-4-use-eq-to-match-the-entire-array}

此查询通过精确匹配 promotionEvents.discounts 数组中的全部值来查找文档。

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        $eq: [{
            categoryName: "Alarm Systems",
            discountPercentage: 5
        }, {
            categoryName: "Door Locks",
            discountPercentage: 12
        }]
    }
}, {
    name: 1
})
```

此查询返回以下结果：

```json
[
    {
        "_id": "aa9ad64c-29da-42f8-a1f0-30e03bf04a2d",
        "name": "Boulder Innovations | Home Security Market - East Sheridanborough"
    }
]
```

> [!NOTE]
> 对整个数组进行相等匹配时，相等谓词中指定值的顺序也必须完全一致。
