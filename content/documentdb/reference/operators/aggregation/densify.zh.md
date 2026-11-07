---
title: $densify
description: $densify 运算符在数组或集合内的值序列中添加缺失的数据点。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$densify.md
weight: 80
translation_source_sha256: d316e033fa645b1f6591d477f90dafd511608d99d37cc4fd8e1c527dbf78f855
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$densify` 流水线阶段用于填充序列中缺失的数据点。它通过基于指定字段、范围和步长生成缺失值，帮助创建更完整的数据集。这在时间序列数据分析等场景中非常有用，可填补数据点之间的空缺，以确保分析的准确性。

## 语法 {#syntax}

```javascript
{
  $densify: {
    field: <field>,
    range: {
      step: <number>,
      unit: <string>, // Optional, e.g., "hour", "day", "month", etc.
      bounds: [<lowerBound>, <upperBound>] // Optional
    },
    partitionByFields: [<field1>, <field2>, ...] // Optional
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`field`** | 执行填充操作的字段。 |
| **`range.step`** | 生成缺失值的步长大小。 |
| **`range.unit`** | (可选) 步长大小的单位，例如时间单位（如 "hour"、"day"）。 |
| **`range.bounds`** | (可选) 指定填充的范围（下界和上界）。 |
| **`partitionByFields`** | (可选) 用于对数据分组以进行填充的字段。 |
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

### 示例 1：填充时间序列数据 {#example-1-densify-a-time-series-dataset}

此查询用于填补 date 字段中缺失的日期。

```javascript
db.aggregate([
    {
      $documents: [
        { date: new ISODate("2024-01-01"), value: 10 },
        { date: new ISODate("2024-01-03"), value: 15 }
      ]
    },
    {
      $densify: {
        field: "date",
        range: {
          step: 1,
          unit: "day",
          bounds: "full"
        }
      }
    }
  ]);
```

此查询返回以下结果：

```json
[
    {
        "date": "ISODate('2024-01-01T00:00:00.000Z')",
        "value": 10
    },
    {
        "date": "ISODate('2024-01-02T00:00:00.000Z')"
    },
    {
        "date": "ISODate('2024-01-03T00:00:00.000Z')",
        "value": 15
    }
]

```

### 示例 2：填充数值型数据 {#example-2-densify-numeric-data}

此查询用于填补 `sales.fullSales` 字段中缺失的数值：

```javascript
db.aggregate([
    {
      $documents: [
        { level: 1, score: 10 },
        { level: 3, score: 30 }
      ]
    },
    {
      $densify: {
        field: "level",
        range: {
          step: 1,
          bounds: [1, 5] 
        }
      }
    }
  ]);
```

此查询返回以下结果：

```json
[
    {
        "level": 1,
        "score": 10
    },
    {
        "level": 2
    },
    {
        "level": 3,
        "score": 30
    },
    {
        "level": 4
    }
]
```

## 限制条件 {#limitations}

下表总结了与 $densify 流水线阶段在聚合流水线中相关的关键限制和行为：

| 类别 | 条件 / 行为 |
| --- | --- |
| 字段限制 | - 若任一文档包含 **date** 值且未指定 `unit`，则报错。 <br> - 若任一文档包含 **numeric** 值且指定了 `unit`，则报错。 <br> - 字段名称以 `$` 开头。请使用 `$project` 重命名。|
| partitionByFields | - 任意字段的值为 **非字符串** 类型。 <br> - 字段名称以 `$` 开头。 |
| range.bounds | - **下界** 定义起始值，与现有文档无关。 <br> - **下界包含在内**。 <br> - **上界不包含**。 <br> - `$densify` 不会过滤掉范围外的文档。 |
