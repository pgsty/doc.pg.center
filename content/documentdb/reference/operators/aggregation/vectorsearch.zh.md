---
title: $vectorSearch
description: 聚合流水线中的 $vectorSearch 阶段在向量索引上执行近似最近邻搜索。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$vectorsearch.md
weight: 450
translation_source_sha256: feea71b43a6dc0e50dfb01472dc7a40551997783f887312a1e11f151c6025d97
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$vectorSearch` 流水线阶段在向量索引上执行近似最近邻搜索，并返回其存储的嵌入与查询向量最接近的文档。它允许你将文档及其嵌入保留在同一个数据库中——语义搜索、检索增强生成以及推荐系统均可作为常规聚合流水线运行，结果可供后续每个流水线阶段使用。

`$vectorSearch` 必须是流水线中的第一个阶段，且 `path` 指定的字段必须被向量索引覆盖。

## 语法 {#syntax}

```javascript
{
  $vectorSearch: {
    queryVector: [<number>, ...],
    path: <string>,
    limit: <positiveInteger>,
    numCandidates: <integer>,
    filter: <document>
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`queryVector`** | 必需。查询嵌入，以数字数组形式表示。不能为空，且长度不得超过 16000 个元素。其长度必须与索引的 `dimensions` 匹配——除非索引设置了 `compression`，否则该值本身被限制在远低于 16000 的范围内。参见 [创建向量索引](#creating-the-vector-index)。 |
| **`path`** | 必需。存储嵌入的文档字段。必须被向量索引覆盖。 |
| **`limit`** | 必需。要返回的文档数量。必须是大于零的 BSON 32 位整数。 |
| **`numCandidates`** | 可选。对于 HNSW 索引，搜索期间探索的候选列表大小（`efSearch`）。必须是介于 1 到 1000 之间的 BSON 32 位整数；较大的值可提高召回率，但会增加延迟。**在 `vector-ivf` 索引上被忽略**——不会报错，查询行为等同于未指定。若省略，DocumentDB 会推导默认值；参见 [选择 numCandidates](#choosing-numcandidates)。 |
| **`filter`** | 可选。与向量搜索相交的查询文档，因此仅返回匹配的文档。过滤条件中使用的每个字段本身也必须建立索引，且 `filter` **在分片集合上不支持**。参见 [示例 3](#example-3-restricting-the-search-with-a-filter)。 |
{.fields}

任何其他字段均会被拒绝，并返回 `BSON field '$vectorSearch.<name>' is an unknown field`。

`limit` 和 `numCandidates` 会检查 BSON int32 线协议类型，不进行数值强制转换，因此即使双精度浮点数或 64 位整数的值在范围内，也会被拒绝：

```
The BSON field 'limit' has an incorrect type 'long'; it should be of type 'int'.
```

这对将裸整数字面量作为双精度浮点数序列化的驱动程序以及显式指定 `NumberLong(...)` 值的情况尤为重要。请注意，以下索引选项（`dimensions`、`m`、`efConstruction`、`numLists`）*确实*接受任意数值类型——相同的字面量在某一区块中有效，而在另一区块中可能致命。

## 示例 {#examples}

本页示例使用 `products` 集合中的以下文档。

```json
[
  { "_id": 1, "name": "Espresso Machine", "category": "appliance", "embedding": [0.9, 0.1, 0.05] },
  { "_id": 2, "name": "Coffee Grinder", "category": "appliance", "embedding": [0.85, 0.15, 0.1] },
  { "_id": 3, "name": "Merlot Bottle", "category": "wine", "embedding": [0.05, 0.9, 0.2] },
  { "_id": 4, "name": "Chardonnay Bottle", "category": "wine", "embedding": [0.1, 0.85, 0.25] },
  { "_id": 5, "name": "Whiskey Tumbler", "category": "glassware", "embedding": [0.2, 0.3, 0.9] }
]
```

三个元素的向量使示例更易读；实际嵌入通常包含数百或数千个元素。

### 创建向量索引 {#creating-the-vector-index}

`$vectorSearch` 需要在嵌入字段上建立索引。使用 `createIndexes` 并指定 `cosmosSearch` 索引类型来创建索引：

```javascript
db.runCommand({
  createIndexes: "products",
  indexes: [{
    key: { embedding: "cosmosSearch" },
    name: "embedding_hnsw_idx",
    cosmosSearchOptions: {
      kind: "vector-hnsw",
      similarity: "COS",
      dimensions: 3,
      m: 16,
      efConstruction: 64
    }
  }]
})
```

`kind` 和 `similarity` 均为必需。`similarity` 选择距离度量方式——`COS` 表示余弦相似度，`L2` 表示欧几里得距离，`IP` 表示内积。`dimensions` 必须与你存储和查询的向量长度匹配，且必须大于 1。

**`dimensions` 的上限由 `compression` 决定，而非 16000 的查询向量限制。** 未压缩索引的最大值为 2000：

| `compression` | 最大 `dimensions` |
| --- | --- |
| 省略（未压缩） | 2000 |
| `"half"` | 4000 |
| `"pq"` | 16000 |

超过上限将导致索引创建失败并返回 `field cannot have more than 2000 dimensions for vector index`。这是使用常见嵌入模型时最先遇到的限制——`text-embedding-3-large` 生成 3072 维度，需要 `compression: "half"` 或 `"pq"`。两种压缩模式均受服务器配置限制，且 `half` 还需要带有半向量支持的 pgvector 构建，因此在特定部署中可能不可用：

```
Compression type 'half' is not enabled.
The compression type 'half' is currently unsupported.
```

**调优选项是索引类型特定的**，且两个 HNSW 选项是耦合的：

| 选项 | 类型 | 范围 | 默认值 |
| --- | --- | --- | --- |
| `m` | `vector-hnsw` | 2 – 100 | 16 |
| `efConstruction` | `vector-hnsw` | 4 – 1000 | 64 |
| `numLists` | `vector-ivf` | 1 – 32768 | 100 |
{.wide .expand}

`efConstruction` 必须至少为 `2 * m`，否则索引创建将失败：

```
efConstruction must be greater than or equal to 2 * m for vector-hnsw indexes
```

上述示例使用 `m: 16` 配合 `efConstruction: 64`，满足该规则——将 `m` 提升至 48 而不同时提升 `efConstruction` 是不允许的。

IVF 索引以相同方式创建，使用 `numLists` 替代 HNSW 选项：

```javascript
db.runCommand({
  createIndexes: "products",
  indexes: [{
    key: { embedding: "cosmosSearch" },
    name: "embedding_ivf_idx",
    cosmosSearchOptions: {
      kind: "vector-ivf",
      similarity: "COS",
      dimensions: 3,
      numLists: 100
    }
  }]
})
```

### 示例 1：查找最近的文档 {#example-1-finding-the-nearest-documents}

此查询返回与查询向量最接近的三个产品。

```javascript
db.products.aggregate([
  {
    $vectorSearch: {
      queryVector: [0.9, 0.1, 0.05],
      path: "embedding",
      limit: 3
    }
  },
  { $project: { _id: 0, name: 1, category: 1 } }
])
```

此查询返回以下结果：

```json
[
  { "name": "Espresso Machine", "category": "appliance" },
  { "name": "Coffee Grinder", "category": "appliance" },
  { "name": "Whiskey Tumbler", "category": "glassware" }
]
```

结果按从最近到最远的顺序返回。

此处的 `$project` 不仅用于裁剪输出。`$vectorSearch` 会为每个返回的文档附加一个内部 `__cosmos_meta__` 字段，因此若不使用投影，同一流水线将返回：

```json
[
  {
    "_id": 1,
    "name": "Espresso Machine",
    "category": "appliance",
    "embedding": [0.9, 0.1, 0.05],
    "__cosmos_meta__": { "score": 1 }
  }
]
```

*排除*投影（如 `{ $project: { embedding: 0 } }`）不会移除 `__cosmos_meta__`——只有包含投影且显式省略该字段时才会移除。请通过 `$meta` 读取得分，而非直接访问该字段，并注意不要在未清除该字段的情况下将文档直接写回集合。

### 示例 2：返回相似度得分 {#example-2-returning-the-similarity-score}

搜索分配的得分可通过 `$meta: "searchScore"` 供后续阶段使用。`$meta: "vectorSearchScore"` 被接受为等效别名——这是 MongoDB Atlas 使用的 `$vectorSearch` 的关键字，因此从 Atlas 迁移的流水线无需修改即可运行。

```javascript
db.products.aggregate([
  {
    $vectorSearch: {
      queryVector: [0.9, 0.1, 0.05],
      path: "embedding",
      limit: 2
    }
  },
  { $project: { _id: 0, name: 1, score: { $meta: "searchScore" } } }
])
```

此查询返回以下结果：

```json
[
  { "name": "Espresso Machine", "score": 1 },
  { "name": "Coffee Grinder", "score": 0.9961580039320722 }
]
```

### 示例 3：使用过滤器限制搜索 {#example-3-restricting-the-search-with-a-filter}

`filter` 将结果限制为符合查询文档的文档。DocumentDB 分别执行近似最近邻扫描和过滤查询，对二者的结果取交集，再对交集应用 `limit`，因此每个返回的文档都满足过滤条件，但**只能尽力使返回数量达到 `limit`**：能否达到取决于 ANN 扫描停止前遇到多少个匹配文档。

实际后果是，在大型集合上进行高度选择性的过滤时，返回的文档数量可能少于 `limit`，且不会报错，也无法与真正没有更多匹配项的情况区分开来。在一个包含一百万条文档的集合中，`filter: { category: "wine" }` 匹配 0.1% 的文档，而 `limit: 10` 可能仅返回寥寥几行结果。提高 `numCandidates` 可以扩大扫描范围，这是解决该问题的方法。扫描范围能扩展多远还取决于部署的 pgvector 版本——迭代扫描需要 pgvector 0.8.0 或更高版本，低于该版本时会静默跳过，这使得结果偏短的情况更加常见。

**`filter` 不支持在分片集合上使用。** 即使未加过滤的 `$vectorSearch` 在同一集合上仍可正常工作，该查询也会被直接拒绝：

```
Filter is not supported for vector search on sharded collection.
```

**`filter` 中使用的每个字段都必须建立索引。** 首先对过滤路径建立索引：

```javascript
db.products.createIndex({ category: 1 }, { name: "category_idx" })
```

然后在此基础上进行过滤：

```javascript
db.products.aggregate([
  {
    $vectorSearch: {
      queryVector: [0.9, 0.1, 0.05],
      path: "embedding",
      limit: 2,
      filter: { category: "wine" }
    }
  },
  { $project: { _id: 0, name: 1, category: 1 } }
])
```

此查询返回以下结果：

```json
[
  { "name": "Chardonnay Bottle", "category": "wine" },
  { "name": "Merlot Bottle", "category": "wine" }
]
```

若缺少该索引，相同的查询将失败：

```
The index for filter path 'category' was not found, please check whether the index is created.
```

<span id="example-4-tuning-recall-with-num-candidates"></span>

### 示例 4：通过 numCandidates 调整召回率 {#example-4-tuning-recall-with-numcandidates}

```javascript
db.products.aggregate([
  {
    $vectorSearch: {
      queryVector: [0.1, 0.88, 0.2],
      path: "embedding",
      limit: 2,
      numCandidates: 200
    }
  },
  { $project: { _id: 0, name: 1, category: 1 } }
])
```

此查询返回以下结果：

```json
[
  { "name": "Merlot Bottle", "category": "wine" },
  { "name": "Chardonnay Bottle", "category": "wine" }
]
```

当搜索遗漏了你预期找到的文档时，应提高 `numCandidates`；搜索将在选择前 `limit` 个结果之前探索更大的邻域。此处使用的五文档集合规模较小，因此在任何设置下搜索都是穷尽式的，故上述值并无影响——只有当索引足够大，导致 HNSW 图被遍历而非扫描时，`numCandidates` 才开始发挥作用。

<span id="choosing-num-candidates"></span>

## 选择 numCandidates {#choosing-numcandidates}

在 HNSW 索引上，若未指定 `numCandidates`，则默认值取决于集合的大小，存在 10,000 行的硬性阈值：

| 集合中的行数 | 默认 `efSearch` |
| --- | --- |
| 少于 10,000 | 索引的 `efConstruction` |
| 10,000 或更多 | 40 |

超过这一阈值后，默认值就完全不再取决于 `efConstruction`。在包含 50,000 个文档的集合上，即使索引为了提高召回率而以 `efConstruction: 512` 构建，搜索时仍会使用 `efSearch: 40`，除非显式设置 `numCandidates`。这比配置值低很多，而问题只表现为结果缺失。对于任何达到生产规模的集合，都应手动设置 `numCandidates`。

在 `vector-ivf` 索引上，`numCandidates` 完全无效。它虽被接受并验证，但 IVF 搜索路径仅读取 `nProbes`，而 `$vectorSearch` 并未暴露该值——因此在此阶段 IVF 不存在召回率控制选项，提高 `numCandidates` 也不会产生任何差异，返回结果字节完全相同。

## 错误情况 {#error-cases}

| 问题 | 错误 |
| --- | --- |
| `path`、`queryVector` 或 `limit` 缺失 | `$path, $queryVector, and $limit are all required fields for using a vector index.` |
| `limit` 为零或负数 | `$vectorSearch.limit must be provided as a positive integer value.` |
| `queryVector` 为空 | `$vectorSearch.queryVector cannot be an empty array.` |
| `queryVector` 不是数字数组 | `$vectorSearch.queryVector must be an array of numbers.` |
| `queryVector` 长度超过 16,000 个元素 | `Length of the query vector cannot exceed 16000` |
| `queryVector` 长度与索引不匹配 | `expected <n> dimensions, not <m>` |
| `numCandidates` 小于 1 | `The vectorSearch.numCandidates should have a value that is not less than 1.` |
| `numCandidates` 大于 1000 | `$vectorSearch.numCandidates must be less than or equal to 1000.` |
| `limit` 或 `numCandidates` 不是 BSON int32 | `The BSON field 'limit' has an incorrect type 'long'; it should be of type 'int'.` |
| `$vectorSearch` 不是首个阶段 | `The $vectorSearch needs to appear as the initial stage in the processing pipeline.` |
| `path` 上无向量索引 | `Similarity index was not found for a vector similarity search query.` |
| `filter` 中存在未建立索引的字段 | `The index for filter path '<field>' was not found, please check whether the index is created.` |
| `filter` 在分片集合上使用 | `Filter is not supported for vector search on sharded collection.` |
| 字段未知 | `BSON field '$vectorSearch.<name>' is an unknown field` |

`numCandidates` 的下界消息省略了上界消息所携带的 `$` 前缀；两者均按服务器发出的内容完整复现。此外请注意，`numCandidates: 0` 是错误而非默认值请求。

首个阶段的检查比表面看起来更严格：即使 `$vectorSearch` 明确是该流水线的首个阶段，当其运行在视图上，或嵌套在 `$facet` 或 `$lookup` 内部时，也会被拒绝。

`expected <n> dimensions, not <m>` 这一错误由 pgvector 报出，而非 DocumentDB，因此其具体措辞可能随 pgvector 升级而变化。

## 注意事项 {#notes}

`index` 字段为兼容性目的而接受，但当前被忽略——搜索使用的是在 `path` 上定义的向量索引。

由 `$vectorSearch` 返回的文档包含一个内部 `__cosmos_meta__` 字段，用于存储相似度得分。该字段不会被排除投影所移除 — 请使用包含投影 `$project`，并通过 `$meta: "searchScore"` 读取得分，而非直接从字段获取。

## 相关 {#related}

- [`$limit`](/documentdb/reference/operators/aggregation/limit/) — `$vectorSearch` 有自己的 `limit`；后续的 `$limit` 可进一步缩小结果范围。
- [`$project`](/documentdb/reference/operators/aggregation/project/) — 用于调整结果，并通过 `$meta` 显示相似度得分。
- [`$meta`](/documentdb/reference/operators/projection/meta/) — 用于投影 `searchScore` 的元数据运算符。
