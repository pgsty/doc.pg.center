---
title: $currentDate
description: $currentDate 运算符将字段值设置为当前日期，类型可以是 Date 或时间戳。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/field-update/$currentdate.md
weight: 10
translation_source_sha256: 037dfc08268d3a6ff2ab7e720ab781d86bf07dc786b2821899bf2f921608a8a1
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 说明中的“typestamp”与代码里的 timestamp 类型不一致。此处保留了原文拼写。

`$currentDate` 运算符将字段值设置为当前日期，类型可以是 Date 或时间戳。该运算符可用于跟踪文档的最后修改时间，或设置创建时间戳。

## 语法 {#syntax}

```javascript
{
  $currentDate: {
    <field1>: <typeSpecification1>,
    <field2>: <typeSpecification2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要设置为当前日期的字段名称。 |
| **`typeSpecification`** | 可选。指定日期值的类型。可以为 `true`（表示 Date 类型），或 `{ $type: "timestamp" }`（表示时间戳类型）。默认为 `true`（Date）。 |
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
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### 示例 1：设置当前日期 {#example-1-setting-current-date}

要向商店文档添加值为当前日期的 `lastUpdated` 字段，可使用 $currentDate 运算符创建该字段，并将当前日期作为 Date 对象写入。

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastUpdated": true
    }
  }
)
```

此操作返回以下结果。

```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}

```

### 示例 2：设置当前时间戳 {#example-2-setting-current-timestamp}

要同时添加日期字段和时间戳字段以跟踪修改，可分别使用 true 值和 typestamp 值调用 $currentDate 运算符。

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastModified": true,
      "lastModifiedTimestamp": { $type: "timestamp" }
    }
  }
)
```

此操作返回以下结果

```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: Long("1"),
  modifiedCount: Long("1"),
  upsertedCount: 0
}
```

### 示例 3：更新嵌套字段 {#example-3-updating-nested-fields}

将文档结构中的嵌套字段设置为当前日期。

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "sales.lastSalesUpdate": true,
      "staff.lastStaffUpdate": { $type: "timestamp" }
    }
  }
)
```

此操作返回以下结果。

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "lastUpdated": ISODate("2025-02-12T10:30:45.123Z"),
    "lastModified": ISODate("2025-02-12T10:30:45.123Z"),
    "lastModifiedTimestamp": Timestamp(1739450445, 1),
    "sales": {
      "totalSales": 37701,
      "lastSalesUpdate": ISODate("2025-02-12T10:30:45.123Z"),
      "salesByCategory": [
        {
          "categoryName": "Mattress Toppers",
          "totalSales": 37701
        }
      ]
    },
    "staff": {
      "totalStaff": {
        "fullTime": 18,
        "partTime": 17
      },
      "lastStaffUpdate": Timestamp(1739450445, 1)
    }
  }
]
```
