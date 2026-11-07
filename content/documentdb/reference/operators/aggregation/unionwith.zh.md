---
title: $unionWith
description: $unionWith 阶段对两个集合执行并集操作，将两个集合的流水线结果合并为单个结果集。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$unionwith.md
weight: 420
translation_source_sha256: d28868590194964edd903725967393c18ac28857288f0fa3671c2522095ee08a
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$unionWith` 流水线阶段对两个集合中的文档执行并集操作。它将两个集合的流水线结果合并为单个结果集，类似于 SQL 中的 `UNION ALL`。该阶段输出两个集合中的所有文档，包括重复项。

## 语法 {#syntax}

**字符串形式（简单并集）：**

```javascript
{
  $unionWith: "<collection>"
}
```

**文档形式（带流水线）：**

```javascript
{
  $unionWith: {
    coll: "<collection>",
    pipeline: [ <stage1>, <stage2>, ... ]
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`coll`** | 可选（如果未提供 `pipeline` 或其不以 `$documents` 开头则为必填）。要并集的集合名称。 |
| **`pipeline`** | 可选。在并集前应用于指定集合的聚合流水线。 |
{.fields}

## 示例 {#examples}

考虑一个 `stores` 集合和一个 `warehouses` 集合。

**stores 集合：**

```json
{
  "_id": "store-001",
  "name": "First Up Consultants | Beverage Shop",
  "city": "Seattle",
  "type": "retail"
}
```

**warehouses 集合：**

```json
{
  "_id": "wh-001",
  "name": "West Coast Distribution Center",
  "city": "Portland",
  "type": "warehouse"
}
```

### 示例 1：简单并集 {#example-1-simple-union}

合并两个集合中的所有文档：

```javascript
db.stores.aggregate([
  { $project: { name: 1, city: 1, type: 1 } },
  {
    $unionWith: "warehouses"
  }
])
```

### 示例 2：带流水线的并集 {#example-2-union-with-pipeline}

将 stores 集合与 warehouses 集合的筛选并投影后的子集进行并集：

```javascript
db.stores.aggregate([
  { $project: { name: 1, city: 1 } },
  {
    $unionWith: {
      coll: "warehouses",
      pipeline: [
        { $match: { city: "Portland" } },
        { $project: { name: 1, city: 1 } }
      ]
    }
  }
])
```

### 示例 3：使用 $documents 执行并集操作 {#example-3-union-with-documents}

使用 `$documents` 将字面文档注入并集：

```javascript
db.stores.aggregate([
  { $project: { name: 1, city: 1 } },
  {
    $unionWith: {
      pipeline: [
        { $documents: [
          { name: "Pop-Up Shop", city: "Austin" },
          { name: "Online Store", city: "Remote" }
        ]}
      ]
    }
  }
])
```

## 限制条件 {#limitations}

- 以下阶段在 `$unionWith` 流水线中**不允许使用**：`$out`、`$merge`、`$changeStream`
- 如果 `coll` 被省略，则流水线必须以 `$documents` 开头
- 最大嵌套流水线深度为 20 层

## 关键要点 {#key-takeaways}

- **UNION ALL 语义** — 不会移除重复项；如需去重，请在并集后使用 `$group`
- **模式灵活性** — 两个集合无需具有相同模式
- **流水线支持** — 可在并集前对第二个集合应用转换
- **字符串简写** — 当第二个集合无需流水线转换时，可使用简单字符串形式
