---
title: createIndexes
description: 使用受支持的标准选项和 DocumentDB 专有选项创建索引。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/indexing/createIndexes.md
weight: 10
translation_source_sha256: f3c7634438d830630b381cc176437e55a264732847a05c6bae956c9567163677
translation_review: AI-assisted bilingual review; 2026-11-07
---

创建一个或多个索引。

示例使用 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)。向量索引示例对每个航班的三元素 `route_vector` 进行索引，且需要 HNSW 支持。

```javascript
db.flights.createIndex({ route_no: 1 })
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`createIndexes`** | (必需) 指定集合名称的字符串。 |
| **`indexes`** | (必需) 包含索引规范的文档数组。 |
| **`ignoreUnknownIndexOptions`** | (可选) 类布尔值，忽略未知的索引规范选项，而不是拒绝它们；默认为 `false`。不允许任意的命令级字段。 |
| **`blocking`** | (可选) DocumentDB 扩展选项，类布尔值，用于请求阻塞式索引创建；默认为 `false`。 |
| **`skipWaitForIndex`** | (可选) DocumentDB 扩展选项，类布尔值，在构建路径支持时提交后台构建并跳过通常的等待。 |
| **`maxTimeMS`** | (可选) 限制网关等待后台索引构建时长的数字。超时不代表已提交的构建被取消。 |
| **`comment`** | (可选) 携带网关请求追踪上下文的字符串；参见[通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

## 索引规范 {#index-specification}

| 参数 | 描述 |
| --- | --- |
| **`key`** | (必需) 指定索引路径和索引类型（如 `1`、`-1`、`"text"`、`"2d"`、`"2dsphere"` 或 `"cosmosSearch"`）的文档。 |
| **`name`** | (在线协议中必需) 指定索引名称的字符串。在使用 shell 的 `createIndex()` 辅助函数时可选。 |
| **`unique`** | (可选) 类布尔值，强制要求索引值唯一。 |
| **`partialFilterExpression`** | (可选) 仅对匹配此过滤条件的文档进行索引的文档。 |
| **`sparse`** | (可选) 类布尔值，指定稀疏索引行为，受支持的索引组合限制。 |
| **`wildcardProjection`** | (可选) 指定通配符索引包含或排除的路径的文档。 |
| **`v`** | (可选) 指定索引规范版本的整数；不支持的版本将被拒绝。 |
| **`expireAfterSeconds`** | (可选) 指定 TTL 间隔的非负数，范围在支持的 32 位整数范围内。 |
| **`default_language`** | (可选) 指定默认文本索引语言的字符串。 |
| **`language_override`** | (可选) 指定选择文本索引语言的文档字段的字符串。 |
| **`weights`** | (可选) 指定文本索引字段权重或通配符权重的文档或 `"$**"`。 |
| **`textIndexVersion`** | (可选) 指定文本索引版本的数字；当必须实际构建新索引时进行验证。 |
| **`cosmosSearchOptions`** | (可选) 指定向量索引选项的文档，如下所述。 |
| **`min`** | (可选) 指定 `2d` 索引边界的数字。 |
| **`max`** | (可选) 指定 `2d` 索引边界的数字。 |
| **`bits`** | (可选) 指定 `2d` 精度的整数，范围从 `1` 到 `32`。 |
| **`collation`** | (可选) 指定非空比较规则的文档；需要排序规则支持。 |
| **`prepareUnique`** | (可选) 仅被 prepare-unique 创建路径识别的布尔值；不是通用的创建选项。 |
| **`storageEngine`** | (可选) 包含以下 DocumentDB 特定选项的文档，而非 PostgreSQL 存储引擎的选择。 |
{.fields}

<span id="document-db-specific-index-options"></span>

### DocumentDB 特定索引选项 {#documentdb-specific-index-options}

这些选项既可直接放在索引规范中，也可放在 `storageEngine` 内：

| 参数 | 描述 |
| --- | --- |
| **`buildAsUnique`** | (可选) 类布尔值，用于为 [现有数据上的阶段式唯一索引转换工作流](#build-a-unique-index-on-existing-data) 构建索引，但不声明其为唯一索引。 |
| **`blocking`** | (可选) 类布尔值，请求为此索引进行阻塞式构建。`storageEngine.blocking` 与顶层命令的 `blocking` 选项作用相同。 |
{.fields}

### 普通索引与复合索引 {#regular-and-composite-indexes}

两个示例均使用默认的有序/复合索引格式，未显式选择。

**普通索引：** 为到达机场查找创建单字段索引：

```javascript
db.flights.createIndex(
  { arrival_airport: 1 },
  { name: "arrival_airport_1" }
)

db.flights.find({ arrival_airport: "LED" })
```

**复合（有序）索引：** 依次对出发机场和计划出发时间建立索引，用于按机场过滤并按出发时间排序的查询：

```javascript
db.flights.createIndex(
  { departure_airport: 1, scheduled_departure: 1 },
  { name: "departure_airport_1_scheduled_departure_1" }
)

db.flights.find({ departure_airport: "SVO" }).sort({ scheduled_departure: 1 })
```

有序/复合索引也可以仅包含一个字段。键文档指定索引字段及其顺序。

### 唯一索引、阻塞索引与 TTL 索引 {#unique-blocking-and-ttl-indexes}

**唯一索引：** 保证航线编号与计划出发时间的组合唯一。现有文档必须已经满足该约束。

```javascript
db.flights.createIndex(
  { route_no: 1, scheduled_departure: 1 },
  { name: "route_no_1_scheduled_departure_1_unique", unique: true }
)
```

**阻塞索引：** 通过 `storageEngine.blocking` 请求为此索引进行阻塞式构建。阻塞式构建在运行期间可能阻塞对集合的写入操作。

```javascript
db.flights.createIndex(
  { departure_airport: 1 },
  {
    name: "departure_airport_1_blocking",
    storageEngine: { blocking: true }
  }
)
```

**TTL 索引：** 应用程序可将短期航班事件存储在单独的 `flight_events` 集合中。将 `recorded_at` 存储为 BSON 日期，并在该时间戳后 24 小时自动过期：

```javascript
db.flight_events.insertOne({
  flight_id: 101,
  event: "check_in_opened",
  recorded_at: new Date()
})

db.flight_events.createIndex(
  { recorded_at: 1 },
  { name: "recorded_at_ttl", expireAfterSeconds: 86400 }
)
```

TTL 索引必须是单字段索引，且不能针对 `_id`。删除操作通过 TTL 清理异步执行，而非精确在过期时间点发生。

### 向量索引选项 {#vector-index-options}

| 参数 | 描述 |
| --- | --- |
| **`kind`** | (必需) 指定索引类型的字符串。内置类型包括 `"vector-ivf"` 和 `"vector-hnsw"`；HNSW 需要启用其服务器功能。 |
| **`similarity`** | (必需) 选择 `"COS"`、`"L2"` 或 `"IP"` 的字符串。 |
| **`dimensions`** | (必需) 指定向量维度数量的数字，必须大于 `1`，且在实现的维度限制范围内。 |
| **`compression`** | (可选) 选择压缩模式的字符串。`"half"` 需要半向量支持及其功能门控。 |
| **`numLists`** | (可选) 指定 IVF 列表数量的数字，必须在实现支持的范围内。 |
| **`m`** | (可选) 指定 HNSW 图连通性的数字，必须在支持范围内。 |
| **`efConstruction`** | (可选) 指定 HNSW 构建搜索宽度的数字，必须在支持范围内。 |
{.fields}

其他向量实现可以注册更多类型和选项；这些不属于默认内置的线协议接口。

```javascript
db.flights.createIndex(
  { route_vector: "cosmosSearch" },
  {
    name: "route_vector_index",
    cosmosSearchOptions: {
      kind: "vector-hnsw",
      similarity: "COS",
      dimensions: 3,
      m: 16,
      efConstruction: 64
    }
  }
)
```

### 文本索引的表示形式 {#text-index-representations}

文本索引支持两种表示形式。下面的示例描述的是同一个文本索引，索引字段为航班的出发机场和到达机场；选择其中一种表示形式即可，不要创建两个索引。

**字段名表示形式：** 在键文档中，将每个索引字段设为 `"text"`。除非用 `weights` 覆盖，否则字段的权重均为 `1`。

```javascript
db.flights.createIndex(
  { departure_airport: "text", arrival_airport: "text" },
  { name: "flight_airports_text" }
)
```

**元数据表示形式：** 使用 `{ _fts: "text", _ftsx: 1 }` 作为键文档，在 `weights` 中指定实际的索引字段及其权重。`_fts` 和 `_ftsx` 是索引元数据标记，无需将它们添加到文档中。[`listIndexes`](/documentdb/reference/commands/indexing/listindexes/) 的输出也使用这种键表示形式。

```javascript
db.flights.createIndex(
  { _fts: "text", _ftsx: 1 },
  {
    name: "flight_airports_text",
    weights: { departure_airport: 1, arrival_airport: 1 }
  }
)
```

对于通配符文本索引，可在字段名表示形式中使用 `{ "$**": "text" }`，也可使用元数据键文档并设置 `weights: { "$**": 1 }`。

## 在已有数据上建立唯一索引 {#build-a-unique-index-on-existing-data}

对已有文档的集合添加唯一性约束时，采用以下分阶段流程。部署必须已启用 prepare-unique 和唯一索引转换支持。该示例是上面直接设置 `unique: true` 示例的替代方案；开始时应尚未创建该索引。

### 1. 构建用于唯一性转换的索引 {#1-build-the-index-for-uniqueness-conversion}

使用 `storageEngine.buildAsUnique: true` 创建索引，不要设置 `unique: true`。等待索引创建完成后再继续。创建时未设置 `buildAsUnique` 的普通非唯一索引不能用于此流程。

```javascript
db.flights.createIndex(
  { route_no: 1, scheduled_departure: 1 },
  {
    name: "route_no_1_scheduled_departure_1_unique",
    storageEngine: { buildAsUnique: true }
  }
)
```

### 2. 阻止新增重复键 {#2-prevent-new-duplicate-keys}

使用 [`collMod`](/documentdb/reference/commands/administration/collmod/) 设置 `prepareUnique: true`。此后，会拒绝引入重复索引键的写入；但不会消除已有的重复值。在下一步之前，修正已有的航线编号与计划出发时间的重复组合。

```javascript
db.runCommand({
  collMod: "flights",
  index: {
    name: "route_no_1_scheduled_departure_1_unique",
    prepareUnique: true
  }
})
```

### 3. 验证已有数据并转换 {#3-validate-existing-data-and-convert}

在单独的 `collMod` 请求中设置 `unique: true`。这会验证已有的索引数据；若验证通过，则将索引转换为唯一索引。如果仍有重复键，转换会失败；修正冲突数据后重试此步骤。

```javascript
db.runCommand({
  collMod: "flights",
  index: {
    name: "route_no_1_scheduled_departure_1_unique",
    unique: true
  }
})
```

不要在同一个请求中同时设置 `prepareUnique` 和 `unique`。转换成功后，索引会被报告为唯一索引，并对索引键组合强制执行唯一性约束。

## 附录：有序索引选项 {#appendix-ordered-index-option}

默认已启用有序/复合索引，因此正常创建索引时无需指定 `enableOrderedIndex`。需要时，可以直接在索引规范中或在 `storageEngine` 内指定该选项。

| 参数 | 描述 |
| --- | --- |
| **`enableOrderedIndex`** | (可选) 控制有序/复合索引的布尔值或整数。数值必须为 `-1`、`1` 或 `2`；建议使用布尔值。 |
{.fields}

参见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/create_indexes.c`、`ParseCreateIndexesArg`、`ParseIndexDefDoc`、`ParseCustomIndexDefOption` 和 `pg_documentdb/src/vector/vector_index_kind_impl.c`；唯一性转换：`pg_documentdb/src/commands/coll_mod.c`、`HandleUniqueConversion` 和 `UpdatePostgresIndexesForUnique`。
