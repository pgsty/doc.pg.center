---
title: $comment
description: $comment 运算符为查询添加注释，便于在日志和性能分析器输出中识别该查询。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/miscellaneous-query/$comment.md
weight: 10
translation_source_sha256: 5f3f4ebdb88f0188df57a3e5633177263afbb2a051bb43b3427df7c618ed8de6
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$comment` 运算符为查询添加注释，便于在日志和性能分析器输出中识别查询。这对于调试和监控数据库操作尤其有用。

## 语法 {#syntax}

```javascript
{
  $comment: <string>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`string`** | 包含随查询附加的注释的字符串。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        },
        "endDate": {
          "Year": 2023,
          "Month": 7,
          "Day": 9
        }
      },
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        }
      ]
    }
  ]
}
```

<span id="example-1-find-stores-with-total-sales-over-100-000-and-add-a-log-comment-for-reference"></span>

### 示例 1：查找总销售额超过 100,000 的商店，并添加日志注释以供参考 {#example-1-find-stores-with-total-sales-over-100000-and-add-a-log-comment-for-reference}

此查询检索总销售额大于 100,000 的商店，并附加注释，便于在日志中识别。

```javascript
db.stores.find(
   { "sales.totalSales": { $gt: 100000 } },
   { name: 1, "sales.totalSales": 1 }
).comment("Query to find high-performing stores")
```

此查询返回以下结果。

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "sales": {
      "totalSales": 151864
    }
  }
]
```
