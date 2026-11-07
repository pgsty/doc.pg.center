---
title: $setField
description: setField 命令用于在嵌入式文档中添加、更新或移除字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/object-expression/$setField.md
weight: 30
translation_source_sha256: bf87bba1b4c8233f32f179bbf64ce85bfc1b8c709d2487d97961b3e7e47eb0f0
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> field 参数的说明谈的是转换为键值对，与本页设置字段的操作不符。原文还称 null 会移除字段。这些表述作为来源问题保留；本版本未独立验证所述移除行为。

`$setField` 运算符用于在嵌入式文档中添加、更新或移除字段。它支持精确操作文档字段，适用于更新嵌套字段、重构文档，乃至完全移除字段等任务。

## 语法 {#syntax}

```javascript
{
  $setField: {
    field: <fieldName>,
    input: <expression>,
    value: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<field>`** | 要转换为键值对数组的文档（对象）。 |
| **`<input>`** | 正在处理的文档或字段。 |
| **`<value>`** | 要赋给字段的新值。如果 `value` 为 `null`，则移除该字段。|
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

### 示例 1：更新嵌套字段 {#example-1-updating-a-nested-field}

此查询对匹配指定 `_id` 的文档执行条件更新，更新其促销活动中嵌套的折扣值。

```javascript
db.stores.updateOne(
  { "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4" },
  [
    {
      $set: {
        "store.promotionEvents": {
          $map: {
            input: "$store.promotionEvents",
            as: "event",
            in: {
              $setField: {
                field: "discounts",
                input: "$$event",
                value: {
                  $map: {
                    input: "$$event.discounts",
                    as: "discount",
                    in: {
                      $cond: {
                        if: { $eq: ["$$discount.categoryName", "Laptops"] },
                        then: {
                          categoryName: "$$discount.categoryName",
                          discountPercentage: 18
                        },
                        else: "$$discount"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
)
```

### 示例 2：移除字段 {#example-2-removing-a-field}

此查询从 `staff` 对象中移除 `totalStaff` 字段。

```javascript
db.collection.updateOne(
  { "store.storeId": "12345" },
  [{
    $set: {
      "store.staff": {
        $setField: {
          field: "totalStaff",
          input: "$store.staff",
          value: null
        }
      }
    }
  }]
)
```
