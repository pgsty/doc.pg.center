---
title: $natural
description: $natural 运算符强制查询使用集合中文档的自然顺序，从而控制文档的排序和检索。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/miscellaneous-query/$natural.md
weight: 20
translation_source_sha256: db6b50a83a0acee8ab604911aca2a5dda6c9a5a2b8a3feea987b936e131d5a86
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$natural` 运算符强制查询使用集合中文档的自然顺序。它可用于排序操作，按文档插入的顺序或其逆序检索文档。需要在不依赖索引字段的情况下获得可预测顺序时，可使用此运算符。

## 语法 {#syntax}

```javascript
{
  $natural: <1 | -1>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`1`** | 按正向自然顺序（插入顺序）排序。 |
| **`-1`** | 按反向自然顺序（插入顺序的逆序）排序。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        }
      ]
    }
  ]
}
```

### 示例 1：基本自然顺序排序 {#example-1-basic-natural-order-sorting}

此查询按商店插入集合的顺序检索所有商店。

```javascript
db.stores.find({}).sort({
    $natural: 1
})
```

### 示例 2：反向自然顺序 {#example-2-reverse-natural-order}

此查询按插入顺序的逆序返回所有商店，最近添加的文档排在最前面。

```javascript
db.stores.find({}).sort({
    $natural: -1
})
```

### 示例 3：自然顺序与筛选结合 {#example-3-natural-order-with-filtering}

此查询筛选总销售额大于 50,000 的商店，并按自然插入顺序返回。

```javascript
db.stores.find({
    "sales.totalSales": {
        $gt: 50000
    }
}).sort({
    $natural: 1
})
```

### 示例 4：自然顺序与投影结合 {#example-4-natural-order-with-projection}

此查询按自然插入顺序返回结果，且仅返回商店名称、总销售额和位置坐标。

```javascript
db.stores.find({}, {
  name: 1,
  "sales.totalSales": 1,
  "location.lat": 1,
  "location.lon": 1
}).sort({ $natural: 1 })
```

### 示例 5：自然顺序与数量限制结合 {#example-5-natural-order-with-limit}

此查询按自然插入顺序返回前三家商店。

```javascript
db.stores.find({}).sort({
    $natural: 1
}).limit(3)
```

## 使用场景 {#use-cases}

`$natural` 运算符适用于以下场景：

- 审计跟踪：需要按文档创建顺序处理文档时
- 按时间顺序处理：适用于插入顺序至关重要的时间敏感数据
- 批量处理：在没有索引的情况下，按可预测的顺序处理文档时
- 调试：了解集合中文档的自然存储顺序
