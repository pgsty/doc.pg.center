---
title: $graphLookup
description: $graphLookup 流水线阶段在聚合流水线中执行对集合中文档的递归搜索。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$graphlookup.md
weight: 130
translation_source_sha256: d93308ed7a46579847200d994d416191e9af889031f9bdf142609471ddb53533
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$graphLookup` 流水线阶段在集合中执行递归搜索，并将所访问的文档附加到每个输入文档上。该阶段适用于层级结构和图结构——例如报告链、分类树、推荐网络，或任何原本需要通过应用程序中的重复查询来遍历的关系。

## 语法 {#syntax}

```javascript
{
  $graphLookup: {
    from: <collection>,
    startWith: <expression>,
    connectFromField: <string>,
    connectToField: <string>,
    as: <string>,
    maxDepth: <nonNegativeInteger>,
    depthField: <string>,
    restrictSearchWithMatch: <document>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`from`** | 必需。要递归搜索的集合。**不能是分片集合**——参见 [限制](#limitations)。 |
| **`startWith`** | 必需。给出开始遍历的值（或值数组）的表达式。 |
| **`connectFromField`** | 必需。其值将传递到下一轮搜索的字段。不能以 `$` 开头。 |
| **`connectToField`** | 必需。在 `from` 集合中与传入值匹配的字段。不能以 `$` 开头。 |
| **`as`** | 必需。添加到每个输入文档的数组字段名称，用于存储匹配的文档。不能以 `$` 开头。 |
| **`maxDepth`** | 可选。非负整数，限定递归轮次的上限。省略则表示无限制搜索。`0` 仅访问由 `startWith` 匹配的文档。 |
| **`depthField`** | 可选。添加到每个匹配文档的字段名称，用于记录其被发现时的递归深度，从 `0` 开始。不能以 `$` 开头。 |
| **`restrictSearchWithMatch`** | 可选。一个查询文档，匹配的文档必须同时满足该条件。不满足该条件的文档将被排除，且遍历不会继续通过这些文档。此处不接受 `$near`、`$nearSphere` 和 `$geoNear` —— 请使用 `$geoWithin` 代替。 |
{.fields}

所有四个字符串类型的字段名——`connectFromField`、`connectToField`、`as` 和 `depthField`——均拒绝以 `$` 开头的名称。注意，`startWith` 是一个 *表达式*，因此 `startWith: "$reportsTo"` 是正确的，而 `connectFromField: "$reportsTo"` 是解析错误。

任何其他参数都会被拒绝，并返回 `Unrecognized parameter supplied to stage $graphlookup`。

## 示例 {#examples}

本页示例使用以下文档，它们位于一个 `employees` 集合中，每个文档通过名称指向其汇报对象。

```json
[
  { "_id": 1, "name": "Ana", "title": "VP, Retail", "reportsTo": null },
  { "_id": 2, "name": "Bo", "title": "Regional Manager", "reportsTo": "Ana" },
  { "_id": 3, "name": "Cai", "title": "Store Manager", "reportsTo": "Bo" },
  { "_id": 4, "name": "Dev", "title": "Shift Lead", "reportsTo": "Cai" },
  { "_id": 5, "name": "Eve", "title": "Associate", "reportsTo": "Dev" }
]
```

### 示例 1：遍历报告链 {#example-1-walking-a-reporting-chain}

此查询从 Eve 开始，沿着 `reportsTo` 一路向上遍历至组织顶层。

```javascript
db.employees.aggregate([
  { $match: { name: "Eve" } },
  {
    $graphLookup: {
      from: "employees",
      startWith: "$reportsTo",
      connectFromField: "reportsTo",
      connectToField: "name",
      as: "managementChain"
    }
  },
  { $project: { _id: 0, name: 1, "managementChain.name": 1 } }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "Eve",
    "managementChain": [
      { "name": "Ana" },
      { "name": "Bo" },
      { "name": "Cai" },
      { "name": "Dev" }
    ]
  }
]
```

一个流水线可到达每个祖先文档。每个匹配的文档在 `as` 数组中仅出现一次，位于其被首次到达的最低深度——通过多条路径可达的文档不会被重复添加。DocumentDB 当前按 `_id` 顺序输出数组，这正是本页输出所示；但该顺序并非该运算符的契约保证，因此若你的应用程序依赖此顺序，请显式添加 `$sort`；当需要知道每个匹配项的距离时，请使用 `depthField`。

### 示例 2：限制搜索范围并记录深度 {#example-2-bounding-the-search-and-recording-depth}

此查询最多遍历起始点之外的一个额外层级，并为每个匹配项标记其被发现时的深度。

```javascript
db.employees.aggregate([
  { $match: { name: "Eve" } },
  {
    $graphLookup: {
      from: "employees",
      startWith: "$reportsTo",
      connectFromField: "reportsTo",
      connectToField: "name",
      as: "managementChain",
      maxDepth: 1,
      depthField: "level"
    }
  },
  {
    $project: {
      _id: 0,
      name: 1,
      "managementChain.name": 1,
      "managementChain.level": 1
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "Eve",
    "managementChain": [
      { "name": "Cai", "level": 1 },
      { "name": "Dev", "level": 0 }
    ]
  }
]
```

Dev 是 Eve 的直接上级，因此位于深度 `0`；Cai 则再向外一层，位于深度 `1`。使用 `maxDepth: 1` 后，搜索在此停止。

### 示例 3：过滤搜索可遍历的文档 {#example-3-filtering-which-documents-the-search-may-traverse}

此查询沿链路遍历，但仅通过职位名称包含 `Lead` 或 `Manager` 的人员。

```javascript
db.employees.aggregate([
  { $match: { name: "Eve" } },
  {
    $graphLookup: {
      from: "employees",
      startWith: "$reportsTo",
      connectFromField: "reportsTo",
      connectToField: "name",
      as: "managementChain",
      restrictSearchWithMatch: { title: { $regex: "Lead|Manager" } }
    }
  },
  {
    $project: {
      _id: 0,
      name: 1,
      "managementChain.name": 1,
      "managementChain.title": 1
    }
  }
])
```

此查询返回以下结果：

```json
[
  {
    "name": "Eve",
    "managementChain": [
      { "name": "Bo", "title": "Regional Manager" },
      { "name": "Cai", "title": "Store Manager" },
      { "name": "Dev", "title": "Shift Lead" }
    ]
  }
]
```

Ana 可达，但其职位名称为 `VP, Retail`，因此被过滤掉——由于无法通过被排除的文档继续遍历，她之上的所有人也将无法到达。

## 限制 {#limitations}

**`from` 不能是分片集合。** 遍历在开始前即被拒绝：

```
$graphLookup using 'from' on a sharded collection is currently unsupported
```

流水线所运行的集合可以是分片的；该限制仅适用于 `from` 所命名的集合。本页所有示例均在两个角色中使用 `employees`，因此若对 `employees` 进行分片，将导致所有示例失效。

## 错误情况 {#error-cases}

| 问题 | 错误 |
| --- | --- |
| `connectFromField` 或 `connectToField` 缺失 | `Both 'connectFrom' and 'connectTo' operators must be provided for a $graphLookup operation.` |
| `from` 缺失 | `$graphLookup requires 'from' field to be specified` |
| `as` 缺失 | `$graphLookup requires 'as' field to be specified` |
| `startWith` 缺失 | `You must provide a 'startWith' parameter when performing a $graphLookup operation` |
| 未知参数 | `Unrecognized parameter supplied to stage $graphlookup: <name>` |
| `maxDepth` 为负数 | `The value of graphlookup.maxDepth must always be a non‑negative integer number.` |
| `as` 以 `$` 开头 | `'as' field name cannot begin with '$'` |
| `connectFromField` 以 `$` 开头 | `FieldPath field names cannot begin with symbol such as '$'` |
| `connectToField` 以 `$` 开头 | `connectToField: FieldPath field names cannot begin with the symbol '$'` |
| `depthField` 以 `$` 开头 | `depthField:FieldPath field names cannot begin with the symbol '$'` |
| `from` 是分片集合 | `$graphLookup using 'from' on a sharded collection is currently unsupported` |
| `restrictSearchWithMatch` 使用邻近运算符 | `$near, $nearSphere and $geoNear cannot be used here. Use $geoWithin instead.` |

`maxDepth` 消息中包含一个不间断连字符（U+2011），而非 ASCII 连字符，因此对 `non-negative` 的字面字符串匹配将无法找到它。

## 相关 {#related}

- [`$lookup`](/documentdb/reference/operators/aggregation/lookup/) —— 仅连接单一层级，而非递归。
- [`$unwind`](/documentdb/reference/operators/aggregation/unwind/) —— 展平 `as` 字段中生成的数组。
