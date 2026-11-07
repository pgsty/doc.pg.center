---
title: $text
description: $text 运算符对已建立索引的字符串字段内容执行文本搜索，实现全文搜索功能。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/evaluation-query/$text.md
weight: 50
translation_source_sha256: 146912affbc0f6b72038837f81b9dc520ba26f09a27be0ecd096831c18667e90
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 本次固定的来源快照将区分大小写的搜索标为尚待发布，同时又给出了用法示例。该示例并不能证明所有 DocumentDB 版本都已支持这一能力。

`$text` 运算符对已建立索引的字符串字段内容执行文本搜索。它在已建立文本索引的字段中搜索指定词语或短语，从而实现全文搜索。`$text` 运算符要求集合至少具有一个文本索引，并提供词干提取、停用词去除和相关性评分等功能。

## 语法 {#syntax}

```javascript
{
  $text: {
    $search: <string>,
    $language: <string>,
    $caseSensitive: <boolean>,
    $diacriticSensitive: <boolean>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`$search`** | 必需。包含待搜索词语的搜索字符串。多个词语按 OR 运算处理，除非用引号将其括起来以进行短语匹配。 |
| **`$language`** | 可选。文本搜索使用的语言，决定词干提取规则和停用词；如果未指定，系统使用索引的默认语言。 |
| **`$caseSensitive`** | 可选。布尔标志，用于启用区分大小写的搜索。默认为 false（不区分大小写）。 |
| **`$diacriticSensitive`** | 可选。布尔标志，用于启用区分变音符号的搜索。默认为 false（不区分变音符号）。 |
{.fields}

## 前提条件 {#prerequisite}

使用 `$text` 运算符之前，必须在要搜索的字段上创建文本索引。

## 示例 {#examples}

下面通过 `stores` 数据集中的示例 JSON 了解其用法。

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

### 示例 1：简单文本搜索 {#example-1-simple-text-search}

此查询检索已建立文本索引的字段中包含单词 "Microphone" 的商店。

```javascript
// First create a text index
db.stores.createIndex({ "name": "text", "sales.salesByCategory.categoryName": "text" })

// Then perform the search
db.stores.find(
{ $text: { $search: "Microphone" }},
{ _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Lavalier Microphones" },
        { "categoryName": "Wireless Microphones" }
      ]
    }
  },
  {
    "_id": "7cecdb2d-33c2-434c-ad55-bf529f68044b",
    "name": "Contoso, Ltd. | Microphone Haven - O'Connellside",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Microphone Accessories" },
        { "categoryName": "Wireless Microphones" }
      ]
    }
  }
]
```

### 示例 2：搜索多个词语 {#example-2-multiple-term-search}

此查询检索与 "Home Decor" 相关的商店（默认对多个词语执行 `OR` 运算）。

```javascript
// First create a text index
db.stores.createIndex({ "name": "text", "sales.salesByCategory.categoryName": "text" })

// Then perform the search
db.stores.find(
{ $text: { $search: "Home Decor" }},
{ _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }).limit(5)
```

此查询返回的前五个结果如下：

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
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "sales": {
      "salesByCategory": [ 
        { "categoryName": "Lamps" }, 
        { "categoryName": "Rugs" } 
      ]
    }
  },
  {
    "_id": "1a2c387b-bb43-4b14-a6cd-cc05a5dbfbd5",
    "name": "Contoso, Ltd. | Smart Home Device Vault - Port Katarina",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Smart Locks" },
        { "categoryName": "Smart Home Hubs" }
      ]
    }
  },
  {
    "_id": "15e9ca57-ebc1-4191-81c2-5dc2f4ebd973",
    "name": "Trey Research | Gardening Supply Stop - Port Saul",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Garden Decor" },
        { "categoryName": "Pruning Shears" }
      ]
    }
  },
  {
    "_id": "dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3",
    "name": "Contoso, Ltd. | Home Improvement Closet - Jaskolskiview",
    "sales": {
      "salesByCategory": [ 
        { "categoryName": "Lumber" }, 
        { "categoryName": "Windows" } 
      ]
    }
  }
]
```

### 示例 3：短语搜索 {#example-3-phrase-search}

此查询使用引号搜索完整短语 "Home Theater"。

```javascript
db.stores.find(
 { $text: { $search: "\"Home Theater\"" }},
 { _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "0bc4f653-e64e-4342-ae7f-9611dfd37800",
    "name": "Tailwind Traders | Speaker Bazaar - North Mireyamouth",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Home Theater Speakers" } 
      ] 
    }
  },
  {
    "_id": "28bb05ed-d516-4186-9144-b9eeee30917a",
    "name": "Adatum Corporation | Home Entertainment Market - East Bennettville",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Media Players" },
        { "categoryName": "Home Theater Projectors" },
        { "categoryName": "Projector Accessories" },
        { "categoryName": "Sound Bars" },
        { "categoryName": "Blu-ray Players" }
      ]
    }
  }
]
```

### 示例 4：通过否定排除词语 {#example-4-exclude-terms-with-negation}

此查询搜索包含 "Audio" 但不包含 "Wireless" 的商店。

```javascript
db.stores.find(
 { $text: { $search: "Audio -Wireless" }},
 { _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }).limit(2)
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "32afe6ec-dd3c-46b3-a681-ed041b032c39",
    "name": "Relecloud | Audio Equipment Gallery - Margretshire",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Audio Receivers" },
        { "categoryName": "Portable Bluetooth Speakers" }
      ]
    }
  },
  {
    "_id": "a3d3e59f-54bd-44be-943c-50dca5c4d667",
    "name": "Contoso, Ltd. | Audio Equipment Shop - West Darrion",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Soundbars" } 
      ] 
    }
  }
]
```

### 示例 5：区分大小写的搜索 {#example-5-case-sensitive-search}

> [!NOTE]
> 区分大小写的功能正在开发中，预计很快发布。

此示例对 "BAZAAR" 执行区分大小写的搜索。

```javascript
db.stores.find(
  { $text: { $search: "BAZAAR", $caseSensitive: true } },
  { _id: 1, name: 1, "sales.salesByCategory.categoryName": 1 }
).limit(2)
```

此查询将匹配包含 "BAZAAR" 且大小写与之完全一致的文档。

```json
[
 {
    "_id": "future-electronics-001",
    "name": "Future Electronics Hub",
    "sales": { "totalSales": 25000 }
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Sound Bars" },
        { "categoryName": "Game Controllers" },
        { "categoryName": "Remote Controls" },
        { "categoryName": "VR Games" }
      ],
      "totalSales": 160000
    }
  }
]
```

### 示例 6：获取文本搜索得分 {#example-6-get-text-search-scores}

此查询检索文本搜索结果及其相关性得分，用于排名。

```javascript
db.stores.find(
  { $text: { $search: "Hub" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } }).limit(5)
```

此查询返回的前五个结果如下：

```json
[
  { "_id": "511c9932-d647-48dd-9bd8-baf47b593f88", "score": 2 },
  { "_id": "a0a2f05c-6085-4c99-9781-689af759662f", "score": 2 },
  { "_id": "fb5aa470-557c-43cb-8ca0-5915d6cae34b", "score": 2 },
  { "_id": "1a2c387b-bb43-4b14-a6cd-cc05a5dbfbd5", "score": 1 },
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74", "score": 1 }
]
```

### 示例 7：跨多个类别搜索 {#example-7-search-across-multiple-categories}

首先创建一个覆盖全部文本字段的文本索引，以便在所有文本字段中搜索。

```javascript
// Create comprehensive text index
db.stores.createIndex({ 
  name: "text",
  "sales.salesByCategory.categoryName": "text",
  "promotionEvents.eventName": "text",
  "promotionEvents.discounts.categoryName": "text"
})

// Search across all indexed fields
db.stores.find(
{ $text: { $search: "\"Home Theater\"" }},
{ name: 1, "sales.salesByCategory.categoryName": 1, "promotionEvents.eventName": 1, "promotionEvents.discounts.categoryName": 1}).limit(2)
```

此查询返回的前两个结果如下。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Sound Bars" },
        { "categoryName": "Game Controllers" },
        { "categoryName": "Remote Controls" },
        { "categoryName": "VR Games" }
      ]
    },
    "promotionEvents": [
      {
        "eventName": "Massive Markdown Mania",
        "discounts": [
          { "categoryName": "DVD Players" },
          { "categoryName": "Projector Lamps" },
          { "categoryName": "Media Players" },
          { "categoryName": "Blu-ray Players" },
          { "categoryName": "Home Theater Systems" },
          { "categoryName": "Televisions" }
        ]
      },
      {
        "eventName": "Fantastic Deal Days",
        "discounts": [
          { "categoryName": "TV Mounts" },
          { "categoryName": "Game Accessories" },
          { "categoryName": "Portable Projectors" },
          { "categoryName": "Projector Screens" },
          { "categoryName": "Blu-ray Players" },
          { "categoryName": "DVD Players" }
        ]
      },
      {
        "eventName": "Discount Delight Days",
        "discounts": [
          { "categoryName": "Game Controllers" },
          { "categoryName": "Home Theater Projectors" },
          { "categoryName": "Sound Bars" },
          { "categoryName": "Media Players" },
          { "categoryName": "Televisions" },
          { "categoryName": "Projector Lamps" }
        ]
      },
      {
        "eventName": "Super Sale Spectacular",
        "discounts": [
          { "categoryName": "Laser Projectors" },
          { "categoryName": "Projector Screens" },
          { "categoryName": "PC Games" },
          { "categoryName": "PlayStation Games" },
          { "categoryName": "TV Mounts" },
          { "categoryName": "Mobile Games" }
        ]
      },
      {
        "eventName": "Grand Deal Days",
        "discounts": [
          { "categoryName": "Remote Controls" },
          { "categoryName": "Televisions" },
          { "categoryName": "Business Projectors" },
          { "categoryName": "Laser Projectors" },
          { "categoryName": "Projectors" },
          { "categoryName": "Projector Screens" }
        ]
      },
      {
        "eventName": "Major Bargain Bash",
        "discounts": [
          { "categoryName": "Sound Bars" },
          { "categoryName": "VR Games" },
          { "categoryName": "Xbox Games" },
          { "categoryName": "Projector Accessories" },
          { "categoryName": "Mobile Games" },
          { "categoryName": "Projector Cases" }
        ]
      }
    ]
  },
  {
    "_id": "0bc4f653-e64e-4342-ae7f-9611dfd37800",
    "name": "Tailwind Traders | Speaker Bazaar - North Mireyamouth",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Home Theater Speakers" } 
      ] 
    },
    "promotionEvents": [
      {
        "eventName": "Epic Bargain Bash",
        "discounts": [
          { "categoryName": "Bluetooth Speakers" },
          { "categoryName": "Outdoor Speakers" }
        ]
      },
      {
        "eventName": "Fantastic Deal Days",
        "discounts": [
          { "categoryName": "Portable Speakers" },
          { "categoryName": "Home Theater Speakers" }
        ]
      }
    ]
  }
]
```
