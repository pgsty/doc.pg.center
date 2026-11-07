---
title: $inc
description: $inc 运算符按指定增量增加字段值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/field-update/$inc.md
weight: 20
translation_source_sha256: d5bc572bca611582306a8e972ec673b94270a70fe359c806c5b235e721c48cc9
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$inc` 运算符按指定增量增加字段值。如果字段不存在，`$inc` 会创建该字段并将其设置为指定值。该运算符接受正值和负值，分别用于增加和减少字段值。

## 语法 {#syntax}

`$inc` 运算符的语法如下：

```javascript
{
  $inc: {
    <field1>: <amount1>,
    <field2>: <amount2>,
    ...
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`field`** | 要增加值的字段名称。 |
| **`amount`** | 增量值。必须为数值（正值表示增加，负值表示减少）。 |
{.fields}

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
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
  }
}
```

### 示例 1：增加员工人数 {#example-1-incrementing-staff-count}

要将全职员工人数增加 3，可对 fullTime 员工字段使用 $inc 运算符，并将增量设为 3。

```javascript
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $inc: {
      "staff.totalStaff.fullTime": 3
    }
  }
)
```

### 示例 2：减少和增加数值 {#example-2-decreasing-and-increasing-values}

要将兼职员工人数减少 2，并将总销售额增加 5000，可对这两个字段使用 $inc 运算符，分别指定 -2 和 5000。

```javascript
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $inc: {
      "staff.totalStaff.partTime": -2,
      "sales.totalSales": 5000
    }
  }
)
```

### 示例 3：创建新字段 {#example-3-creating-new-fields}

如果字段不存在，`$inc` 会创建该字段并将其设置为指定值。

```javascript
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $inc: {
      "staff.contractorCount": 5,
      "sales.monthlyTarget": 200000
    }
  }
)
```

### 示例 4：增加数组元素的值 {#example-4-incrementing-array-element-values}

使用位置运算符更新 salesByCategory 数组中的特定销售数据。

```javascript
db.stores.updateOne(
  { 
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "sales.salesByCategory.categoryName": "Sound Bars"
  },
  {
    $inc: {
      "sales.salesByCategory.$.totalSales": 500
    }
  }
)
```

执行这些操作后，文档更新如下：

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "staff": {
    "totalStaff": {
      "fullTime": 22,
      "partTime": 18
    },
    "contractorCount": 5
  },
  "sales": {
    "totalSales": 156864,
    "monthlyTarget": 200000,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2620
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
  }
}
```
