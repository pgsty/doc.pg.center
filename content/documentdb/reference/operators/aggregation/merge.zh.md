---
title: $merge
description: 聚合流水线中的 $merge 阶段将聚合结果写入指定集合。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$merge.md
weight: 210
translation_source_sha256: f5ad63aa86e4d32f65a5c5b2ecfb651716ddeafe76b41e3f5c14f827f84c920b
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$merge` 流水线阶段用于将聚合查询的结果写入指定的集合。该阶段特别适用于根据聚合操作的输出，将文档更新或插入目标集合的任务。通过将数据转换与数据持久化结合在单一操作中，该阶段有助于简化工作流。

## 语法 {#syntax}

```javascript
{
  $merge: {
    into: <collection>,
    on: <field or fields>,
    whenMatched: <action>,
    whenNotMatched: <action>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`into`** | 指定聚合结果将被写入的目标集合。 |
| **`on`** | 指定用于在目标集合中识别匹配文档的字段。 |
| **`whenMatched`** | 指定在找到匹配文档时采取的操作。选项包括 `merge`、`replace`、`keepExisting`、`fail`，或自定义流水线。 |
| **`whenNotMatched`** | 指定在未找到匹配文档时采取的操作。选项包括 `insert` 或 `discard`。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
   "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### 示例 1：将数据合并到集合 {#example-1-merge-data-into-a-collection}

此查询对文档进行聚合，并将结果写入名为 `salesSummary` 的集合，当 `_id` 字段匹配时更新现有文档，否则插入新文档。

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      totalSales: { $sum: "$sales.salesByCategory.totalSales" }
    }
  },
  {
    $merge: {
      into: "salesSummary",
      on: "_id",
      whenMatched: "merge",
      whenNotMatched: "insert"
    }
  }
])
```

### 示例 2：替换目标集合中的文档 {#example-2-replace-documents-in-the-target-collection}

此示例根据 `_id` 字段替换 `promotionEventsSummary` 集合中的文档。

```javascript
db.promotionEvents.aggregate([
  {
    $project: {
      _id: "$eventName",
      startDate: "$promotionalDates.startDate",
      endDate: "$promotionalDates.endDate",
      totalDiscounts: { $size: "$discounts" }
    }
  },
  {
    $merge: {
      into: "promotionEventsSummary",
      on: "_id",
      whenMatched: "replace",
      whenNotMatched: "insert"
    }
  }
])
```
