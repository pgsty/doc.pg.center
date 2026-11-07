---
title: $group
description: $group 流水线阶段根据指定的标识符表达式对文档进行分组，并应用累加器表达式。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$group.md
weight: 140
translation_source_sha256: 67992f33fb354938abb5dcc44ef67af16899773021bf112d488276d2725d1535
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$group` 聚合流水线阶段根据指定的标识符表达式对文档进行分组，并应用累加器表达式为每个组创建计算字段。此阶段对于数据聚合和汇总操作至关重要。

## 语法 {#syntax}

```javascript
{
  $group: {
    _id: <expression>,
    <field1>: { <accumulator1>: <expression1> },
    <field2>: { <accumulator2>: <expression2> }
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`_id`** | 必需。用于分组的表达式。使用 null 可对所有输入文档计算累加值。 |
| **`field`** | 可选。使用累加器运算符（如 $sum、$avg、$max、$min、$count 等）计算。 |
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
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        }
      ]
    }
  ]
}
```

### 示例 1：按城市 对人员配置情况进行分组分析 {#example-1-group-staffing-analysis-by-city}

此查询按城市对商店进行分组，并分析不同地点的人员配置模式。

```javascript
db.stores.aggregate([
  {
    $group: {
      _id: "$city",
      totalFullTimeStaff: { $sum: "$staff.employeeCount.fullTime" },
      totalPartTimeStaff: { $sum: "$staff.employeeCount.partTime" },
      avgFullTimeStaff: { $avg: "$staff.employeeCount.fullTime" },
      storesInCity: { $count: {} }
    }
  },
  {
    $project: {
      city: "$_id",
      totalFullTimeStaff: 1,
      totalPartTimeStaff: 1,
      avgFullTimeStaff: { $round: ["$avgFullTimeStaff", 1] },
      storesInCity: 1,
      fullTimeRatio: {
        $round: [
          { $divide: ["$totalFullTimeStaff", { $add: ["$totalFullTimeStaff", "$totalPartTimeStaff"] }] },
          2
        ]
      }
    }
  },
  { $limit : 2}
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "New Ellsworth",
    "totalFullTimeStaff": 11,
    "totalPartTimeStaff": 1,
    "avgFullTimeStaff": 11,
    "storesInCity": 1,
    "city": "New Ellsworth",
    "fullTimeRatio": 0.92
  },
  {
    "_id": "Jalonborough",
    "totalFullTimeStaff": 4,
    "totalPartTimeStaff": 1,
    "avgFullTimeStaff": 4,
    "storesInCity": 1,
    "city": "Jalonborough",
    "fullTimeRatio": 0.8
  }
]
```
