---
title: $regex
description: $regex 运算符提供正则表达式功能，用于在查询中进行模式匹配，支持灵活的字符串匹配和搜索。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/evaluation-query/$regex.md
weight: 40
translation_source_sha256: 165c84867b77414fc88e9520fd0cf28db557b10f1f50572294f40434b8ec979d
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$regex` 运算符提供正则表达式功能，用于在查询中进行模式匹配。它可以搜索字段值与指定正则表达式模式匹配的文档，适用于灵活的字符串搜索、模式验证和复杂的文本筛选操作。

## 语法 {#syntax}

`$regex` 运算符的语法如下：

```javascript
{
  <field>: { $regex: <pattern>, $options: <options> }
}
```

也可以使用以下简写形式：

```javascript
{
  <field>: { $regex: /<pattern>/<options> }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<field>`** | 要搜索的字段。必须包含字符串值。 |
| **`<pattern>`** | 用于匹配的正则表达式模式。 |
| **`<options>`** | 可选。正则表达式选项，例如不区分大小写匹配。常用选项包括 'i'（不区分大小写）、'm'（多行）、's'（点号匹配所有字符）和 'x'（扩展）。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
  "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
  "location": {
    "lat": 87.2239,
    "lon": -129.0506
  },
  "staff": {
    "employeeCount": {
      "fullTime": 8,
      "partTime": 7
    }
  },
  "sales": {
    "salesByCategory": [
      { "categoryName": "Towel Sets", "totalSales": 520 },
      { "categoryName": "Bath Accessories", "totalSales": 41710 },
      { "categoryName": "Drapes", "totalSales": 42893 },
      { "categoryName": "Towel Racks", "totalSales": 30773 },
      { "categoryName": "Hybrid Mattresses", "totalSales": 39491 },
      { "categoryName": "Innerspring Mattresses", "totalSales": 6410 },
      { "categoryName": "Bed Frames", "totalSales": 41917 },
      { "categoryName": "Mattress Protectors", "totalSales": 44124 },
      { "categoryName": "Bath Towels", "totalSales": 5671 },
      { "categoryName": "Turkish Towels", "totalSales": 25674 }
    ],
    "revenue": 279183
  },
  "promotionEvents": [
    {
      "eventName": "Discount Derby",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 5 }
      },
      "discounts": [
        { "categoryName": "Microfiber Towels", "discountPercentage": 6 },
        { "categoryName": "Bath Sheets", "discountPercentage": 16 },
        { "categoryName": "Towels", "discountPercentage": 10 },
        { "categoryName": "Hand Towels", "discountPercentage": 11 },
        { "categoryName": "Kitchen Towels", "discountPercentage": 21 },
        { "categoryName": "Placemat", "discountPercentage": 11 },
        { "categoryName": "Bath Accessories", "discountPercentage": 11 },
        { "categoryName": "Bedspreads", "discountPercentage": 21 },
        { "categoryName": "Shower Curtains", "discountPercentage": 24 },
        { "categoryName": "Pillow Top Mattresses", "discountPercentage": 10 }
      ]
    },
    {
      "eventName": "Big Bargain Blitz",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
        "endDate": { "Year": 2024, "Month": 4, "Day": 3 }
      },
      "discounts": [
        { "categoryName": "Mattress Toppers", "discountPercentage": 24 },
        { "categoryName": "Pillow Cases", "discountPercentage": 14 },
        { "categoryName": "Soap Dispensers", "discountPercentage": 20 },
        { "categoryName": "Beach Towels", "discountPercentage": 18 },
        { "categoryName": "Bath Mats", "discountPercentage": 22 },
        { "categoryName": "Blankets", "discountPercentage": 12 },
        { "categoryName": "Kitchen Towels", "discountPercentage": 8 },
        { "categoryName": "Memory Foam Mattresses", "discountPercentage": 14 },
        { "categoryName": "Placemat", "discountPercentage": 17 },
        { "categoryName": "Bed Frames", "discountPercentage": 23 }
      ]
    },
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 30 }
      },
      "discounts": [
        { "categoryName": "Bed Skirts", "discountPercentage": 17 },
        { "categoryName": "Shower Curtains", "discountPercentage": 23 },
        { "categoryName": "Bath Towels", "discountPercentage": 21 },
        { "categoryName": "Memory Foam Mattresses", "discountPercentage": 11 },
        { "categoryName": "Bathrobes", "discountPercentage": 19 },
        { "categoryName": "Bath Accessories", "discountPercentage": 5 },
        { "categoryName": "Box Springs", "discountPercentage": 21 },
        { "categoryName": "Hand Towels", "discountPercentage": 13 },
        { "categoryName": "Tablecloths", "discountPercentage": 19 },
        { "categoryName": "Duvet Covers", "discountPercentage": 23 }
      ]
    },
    {
      "eventName": "Unbeatable Bargain Bash",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 9, "Day": 21 },
        "endDate": { "Year": 2024, "Month": 9, "Day": 30 }
      },
      "discounts": [
        { "categoryName": "Adjustable Beds", "discountPercentage": 19 },
        { "categoryName": "Mattress Toppers", "discountPercentage": 23 },
        { "categoryName": "Washcloths", "discountPercentage": 7 },
        { "categoryName": "Comforters", "discountPercentage": 24 },
        { "categoryName": "Kitchen Towels", "discountPercentage": 7 },
        { "categoryName": "Pillows", "discountPercentage": 13 },
        { "categoryName": "Bath Sheets", "discountPercentage": 25 },
        { "categoryName": "Napkins", "discountPercentage": 25 },
        { "categoryName": "Bath Towels", "discountPercentage": 15 },
        { "categoryName": "Beach Towels", "discountPercentage": 15 }
      ]
    }
  ],
  "company": "First Up Consultants",
  "city": "Port Antone",
  "storeOpeningDate": { "$date": "2024-09-19T17:31:59.665Z" },
  "lastUpdated": { "$timestamp": { "t": 1729359119, "i": 1 } }
}
```

### 示例 1：按名称模式查找商店 {#example-1-find-stores-by-name-pattern}

此查询检索名称中包含 "Consultants" 的所有商店（不区分大小写）。

```javascript
db.stores.find(
  { name: { $regex: "Consultants", $options: "i" } },
  { _id: 1, name: 1, storeOpeningDate: 1 }
).limit(3)
```

此查询返回的前三个结果如下：

```json
[
  {
    "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
    "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
    "storeOpeningDate": "2024-09-19T17:31:59.665Z"
  },
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "storeOpeningDate": "2024-09-10T13:43:51.209Z"
  },
  {
    "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
    "name": "First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort",
    "storeOpeningDate": "2024-09-19T08:27:44.268Z"
  }
]
```

### 示例 2：对类别名称进行高级模式匹配 {#example-2-advanced-pattern-matching-for-category-names}

此查询检索所售产品的类别名称以元音字母开头的商店。

```javascript
db.stores.find(
  {
    "sales.salesByCategory.categoryName": { $regex: "^[AEIOUaeiou]" }
  },
  { _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }
).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "name": "Relecloud | Toy Collection - North Jaylan",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Educational Toys" } 
      ] 
    }
  },
  {
    "_id": "4e064f0a-7e30-4701-9a80-eff3caf46ce8",
    "name": "Fourth Coffee | Outdoor Furniture Deals - Lucianohaven",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Outdoor Swings" },
        { "categoryName": "Hammocks" }
      ]
    }
  }
]
```

### 示例 3：查找符合特定命名约定的商店 {#example-3-find-stores-with-specific-naming-conventions}

此查询检索名称中包含竖线字符（|）分隔符的商店。

```javascript
db.stores.find(
{ name: { $regex: "\\|" }},
{ _id: 1, name: 1, "sales.salesByCategory.categoryName": 1}).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Desk Lamps" } 
      ] 
    }
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Stockings" } 
      ] 
    }
  }
]
```

### 示例 4：折扣类别的复杂模式 {#example-4-complex-pattern-for-discount-categories}

此查询检索类别名称包含 "Bath" 且以 "s" 结尾的商店。

```javascript
db.stores.aggregate([
  { $match: { "promotionEvents.discounts.categoryName": { $regex: "Bath.*s$", $options: "i" } } },
  { $project: { "_id": 1, "name": 1, "promotionEvents.discounts.categoryName":1 }},
  { $match: {"promotionEvents.discounts.categoryName": { $ne: [] }} },
  { $limit: 2 }])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
    "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "Bath Sheets", "discountPercentage": 16 },
          { "categoryName": "Bath Accessories", "discountPercentage": 11 }
        ]
      },
      {
        "discounts": [ 
          { "categoryName": "Bath Mats", "discountPercentage": 22 } 
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bath Towels", "discountPercentage": 21 },
          { "categoryName": "Bathrobes", "discountPercentage": 19 },
          { "categoryName": "Bath Accessories", "discountPercentage": 5 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bath Sheets", "discountPercentage": 25 },
          { "categoryName": "Bath Towels", "discountPercentage": 15 }
        ]
      }
    ]
  },
  {
    "_id": "27ef6004-70fa-4217-8395-0eabc4cc9841",
    "name": "Fabrikam, Inc. | Bed and Bath Store - O'Connerborough",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "Bath Accessories", "discountPercentage": 24 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bathrobes", "discountPercentage": 18 },
          { "categoryName": "Bath Towels", "discountPercentage": 14 },
          { "categoryName": "Bath Accessories", "discountPercentage": 20 }
        ]
      }
    ]
  }
]
```
