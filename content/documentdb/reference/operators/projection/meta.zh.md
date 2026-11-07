---
title: $meta
description: $meta 运算符随返回的数据集一同返回计算得到的元数据列。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/projection/$meta.md
weight: 10
translation_source_sha256: 1aa323f7b3ccd8a386516b2e8c51c2fafa8c3848c9cdc374df94c506934a81a1
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$meta` 投影运算符用于将元数据包含在查询结果中。它可将文本搜索得分或其他计算值等元数据加入输出文档。

## 语法 {#syntax}

`$meta` 投影运算符的用法如下：

```javascript
db.collection.find({
    $text: {
        $search: < string >
    }
}, {
    field: {
        $meta: < metaDataKeyword >
    }
})
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 输出文档中用于存放元数据的字段名称。 |
| **`metaDataKeyword`** | 要包含的元数据类型。参见下方的关键字。 |
{.fields}

| 关键字 | 返回值 |
| --- | --- |
| **`textScore`** | `$text` 搜索的相关性得分。 |
| **`searchScore`** | [`$vectorSearch`](/documentdb/reference/operators/aggregation/vectorsearch/) 的相似度得分。 |
| **`vectorSearchScore`** | `searchScore` 的别名；MongoDB Atlas 在 `$vectorSearch` 中使用的关键字。 |
| **`indexKey`** | 不支持，会被拒绝并返回错误 `Returning indexKey for $meta not supported`。 |

其他任何关键字都会被拒绝，并返回错误 `Argument provided to the $meta is not supported: <keyword>`。

`$meta` 不仅限于 `find()` 投影；在 `$vectorSearch` 之后的聚合 `$project` 阶段中，可以读取 `searchScore` 和 `vectorSearchScore`：

```javascript
db.products.aggregate([
  { $vectorSearch: { queryVector: [0.9, 0.1, 0.05], path: "embedding", limit: 2 } },
  { $project: { _id: 0, name: 1, score: { $meta: "searchScore" } } }
])
```

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "34f462fe-5085-4a77-a3de-53f4117466bd",
  "name": "Wide World Importers",
  "location": {
    "lat": -63.5435,
    "lon": 77.7226
  },
  "staff": {
    "totalStaff": {
      "fullTime": 16,
      "partTime": 16
    }
  },
  "sales": {
    "totalSales": 41481,
    "salesByCategory": [
      {
        "categoryName": "Holiday Tableware",
        "totalSales": 41481
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 11,
          "Day": 13
        },
        "endDate": {
          "Year": 2023,
          "Month": 11,
          "Day": 22
        }
      },
      "discounts": [
        {
          "categoryName": "Gift Boxes",
          "discountPercentage": 9
        },
        {
          "categoryName": "Holiday Tableware",
          "discountPercentage": 24
        }
      ]
    },
    {
      "eventName": "Incredible Savings Showcase",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 20
        }
      },
      "discounts": [
        {
          "categoryName": "Ribbons",
          "discountPercentage": 15
        },
        {
          "categoryName": "Gift Bags",
          "discountPercentage": 25
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}

```

### 示例 1：包含文本搜索得分 {#example-1-including-text-search-scores}

将文本搜索得分包含在文本搜索查询的结果中。

```javascript
db.stores.createIndex({ "name": "text"});

db.stores.find(
    { $text: { $search: "Equipment Furniture Finds" } },
    { _id: 1, name: 1, score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } }).limit(2)

```

此查询返回的前两个结果如下：

```json
[
  {
    _id: 'cf1448e9-5493-49b5-95da-ab8a105b5240',
    name: 'Tailwind Traders | Camera Market - Wolfmouth',
    score: 4
  },
  {
    _id: '4fd389af-4693-4c02-93cf-0d80ae8ace07',
    name: 'Wide World Importers | Camera Collection - South Cordelia',
    score: 4
  }
]
```

## 限制 {#limitation}

- 不支持 `{ $meta: "indexKey" }`。无论查询是否使用索引，都会被拒绝并返回错误 `Returning indexKey for $meta not supported`。
