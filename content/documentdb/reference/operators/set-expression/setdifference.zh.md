---
title: $setDifference
description: $setDifference 运算符返回一个集合，其中包含存在于第一个集合但不存在于第二个集合的元素。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/set-expression/$setdifference.md
weight: 30
translation_source_sha256: b0960555d17a8b90947c23861fa96433924bc54a491e75a718204b20fb891d33
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$setDifference` 运算符返回一个集合，其中包含存在于一个集合但不存在于另一个集合的元素。它将数组视为集合，忽略重复值和元素顺序。

## 语法 {#syntax}

```javascript
{
  $setDifference: [ <array1>, <array2> ]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| `array1` | 要比较的第一个数组。返回仅存在于此数组中的元素。 |
| `array2` | 与第一个数组进行比较的第二个数组。两个数组中都存在的元素会从结果中排除。 |
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

### 示例 1：查找有售但未打折的产品类别 {#example-1-find-categories-of-products-for-sale-but-not-discounted}

此查询检索有销售数据但没有折扣的产品类别。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      soldCategories: "$sales.salesByCategory.categoryName",
      discountedCategories: {
        $reduce: {
          input: "$promotionEvents",
          initialValue: [],
          in: {
            $concatArrays: ["$$value", "$$this.discounts.categoryName"]
          }
        }
      }
    }
  },
  {
    $project: {
      name: 1,
      soldCategories: 1,
      discountedCategories: 1,
      categoriesWithoutDiscounts: {
        $setDifference: ["$soldCategories", "$discountedCategories"]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "soldCategories": [
      "Sound Bars",
      "Game Controllers",
      "Remote Controls",
      "VR Games"
    ],
    "discountedCategories": [
      "DVD Players",
      "Projector Lamps",
      "Media Players",
      "Blu-ray Players",
      "Home Theater Systems",
      "Televisions"
    ],
    "categoriesWithoutDiscounts": [
      "Sound Bars",
      "Home Theater Projectors",
      "Game Controllers",
      "Remote Controls",
      "VR Games"
    ]
  }
]
```

### 示例 2：比较员工配置类型 {#example-2-compare-staff-distribution-types}

此查询找出两份假设的员工需求列表之间的差集。

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      requiredSkills: ["Sales", "Customer Service", "Technical Support", "Inventory Management"],
      availableSkills: ["Sales", "Customer Service", "Marketing", "Administration"],
      missingSkills: {
        $setDifference: [
          ["Sales", "Customer Service", "Technical Support", "Inventory Management"],
          ["Sales", "Customer Service", "Marketing", "Administration"]
        ]
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "requiredSkills": [
      "Sales",
      "Customer Service", 
      "Technical Support",
      "Inventory Management"
    ],
    "availableSkills": [
      "Sales",
      "Customer Service",
      "Marketing",
      "Administration"
    ],
    "missingSkills": [
      "Technical Support",
      "Inventory Management"
    ]
  }
]
```
