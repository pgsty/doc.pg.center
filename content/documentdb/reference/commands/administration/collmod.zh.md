---
title: collMod
description: 在 DocumentDB 中修改集合、视图、模式验证和索引设置。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/administration/collMod.md
weight: 10
translation_source_sha256: f7643a85419a2b60fb10fb50ea6a4c8c0a27263e08252b0d42c5132b769a0741
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

修改受支持的集合或索引属性。

示例使用 [`createIndexes`](/documentdb/reference/commands/indexing/createindexes/) 在 [airline 数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 上创建的 `route_no_1` 索引。

## 语法 {#syntax}

```javascript
db.flights.hideIndex("route_no_1")
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`collMod`** | (必需) 指定集合或视图名称的字符串。 |
| **`index`** | (可选) 指定索引选择器和修改操作的文档，如下所述。 |
| **`viewOn`** | (可选) 替换视图源的字符串。 |
| **`pipeline`** | (可选) 替换视图聚合流水线的数组；必须与 `viewOn` 一同提供，不可与其他修改类别混合使用。 |
| **`validator`** | (可选) 当启用模式验证时，替换模式验证规则的文档。 |
| **`validationLevel`** | (可选) 选择 `off`、`strict` 或 `moderate` 的字符串；当模式验证被禁用时被拒绝。 |
| **`validationAction`** | (可选) 选择 `error` 或 `warn` 的字符串；当模式验证被禁用时被拒绝。 |
| **`enableStats`** | (可选) 作为 DocumentDB 扩展提供的布尔值，用于启用或禁用各集合的规划器统计信息。要求部署支持按集合维护规划器统计信息；不能用于视图。 |
| **`colocation`** | (可选) 作为 DocumentDB 扩展提供的文档，传递给部署的集合共置钩子；默认单节点后端无变化；嵌套选项为部署特定。 |
| **`changeStreamPreAndPostImages`** | (可选) 具有以下行为的文档：`{ enabled: <boolean> }`；当启用修改前镜像支持且集群版本不低于 0.112 时应用；否则被忽略。 |
| **`enableUpdateDescription`** | (可选) 类布尔值，用于启用或禁用变更流更新描述。 |
{.fields}

其他行为见[附加模块部分](/documentdb/reference/commands/contrib/)。

`index` 文档接受：

| 参数 | 描述 |
| --- | --- |
| **`name`** | (可选) 通过名称选择索引的字符串；需提供此项或 `keyPattern`。重命名要求两者同时提供。 |
| **`keyPattern`** | (可选) 通过键规范选择索引的文档。重命名要求同时提供此项和 `name`；其他索引修改只接受一个选择器。 |
| **`newName`** | (可选) DocumentDB 扩展提供的字符串，用于重命名所选索引。要求同时提供 `name` 和 `keyPattern`，且不能与其他修改组合使用。 |
| **`hidden`** | (可选) 类布尔值；为 `true` 时对查询规划隐藏索引，为 `false` 时使其可见。不能修改无效索引、唯一索引或 `_id_` 索引的可见性。 |
| **`prepareUnique`** | (可选) 类布尔值，为支持的非唯一索引准备唯一性转换。 |
| **`unique`** | (可选) 类布尔值，请求唯一性转换，受现有数据验证和索引类型约束。 |
| **`expireAfterSeconds`** | (可选) 非负数，用于更改 TTL 索引的过期间隔，或将符合条件的索引转为 TTL 索引。 |
| **`reindex`** | (可选) 类布尔值，必须为 `true`。排队重新索引请求。通过 [`currentOp`](/documentdb/reference/commands/diagnostic/currentop/) 监控进度。 |
| **`updateOptions`** | (可选) 类布尔值，控制重建时刷新索引选项。只能与 `reindex` 一同提供；不能对 `_id_` 索引启用。 |
{.fields}

`dryRun` 不是受支持的顶层字段。当模式验证被禁用时，模式验证设置（包括 `validator`）被拒绝。共享字段如 `writeConcern` 和 `comment` 被接受，且不改变修改语义。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

参见 [在现有数据上构建唯一索引](/documentdb/reference/commands/indexing/createindexes/#build-a-unique-index-on-existing-data) 了解分阶段的 `buildAsUnique`、`prepareUnique` 和 `unique` 工作流。

## 示例 {#examples}

以下示例使用 `bookings` 数据库。请按顺序运行航班索引示例：可见性示例会在重建索引前恢复索引可见性；重命名示例会改变索引名称，后续请求需使用新名称。

### 启用规划器统计信息 {#enable-planner-statistics}

启用统计信息前，检查 `flights` 的 [`listCollections`](/documentdb/reference/commands/administration/listcollections/) 输出（例如使用 `db.getCollectionInfos({ name: "flights" })`）。若 `options.statsEnabled` 为 `true`，说明规划器统计信息已启用。

为 `flights` 启用按集合维护的规划器统计信息：

```javascript
db.runCommand({ collMod: "flights", enableStats: true })
```

规划器可在选择计划时，使用索引值的统计信息估算查询选择性。此选项要求部署支持按集合维护规划器统计信息，且只适用于集合，不适用于视图。它不是 [`collStats`](/documentdb/reference/commands/diagnostic/collstats/) 这样的集合大小报告，启用后也不保证采用某个特定查询计划。

要禁用此集合的规划器统计信息：

```javascript
db.runCommand({ collMod: "flights", enableStats: false })
```

禁用会移除相关规划器统计信息，不会删除索引或集合数据。要在保持启用的同时刷新统计信息，参见 [`compact` 的 `mode: "updateStats"`](/documentdb/reference/commands/diagnostic/compact/)。

### 隐藏和取消隐藏索引 {#hide-and-unhide-an-index}

暂时让查询规划不使用 `route_no_1`，但不删除它，然后恢复其可见性：

```javascript
db.flights.hideIndex("route_no_1")
db.flights.unhideIndex("route_no_1")
```

这些 shell 辅助函数通过 `collMod` 设置 `index.hidden`。隐藏时保留索引及其定义，因此取消隐藏无需创建新索引。可见性变更要求索引有效、非唯一，且不是 `_id_` 索引。

### 重建索引 {#rebuild-an-index}

使用 `collMod.index.reindex` 重建索引。DocumentDB 特有的选项没有专用 shell 辅助函数：

```javascript
db.runCommand({ collMod: "flights", index: { name: "route_no_1", reindex: true } })
```

请求会将异步重建加入队列；命令响应成功不代表重建已经完成。使用 [`currentOp`](/documentdb/reference/commands/diagnostic/currentop/#monitor-index-builds) 监视构建。

索引必须有效且可见，并且不能启用 `buildAsUnique` 或 `prepareUnique`。请将重建索引与其他修改分开提交。可选的 `updateOptions` 设置只能与 `reindex` 一同使用。

### 重命名索引 {#rename-an-index}

为航线索引取一个更明确的名称：

```javascript
db.runCommand({
  collMod: "flights",
  index: {
    name: "route_no_1",
    keyPattern: { route_no: 1 },
    newName: "flight_route_lookup"
  }
})
```

此 DocumentDB 扩展要求同时提供现有名称及其匹配的键模式。它只更改索引元数据中的名称，不重建索引或改变其键。之后，按名称操作索引时使用 `flight_route_lookup`。

索引必须有效，不能是 `_id_`，且新名称不能与其他索引冲突。请将重命名与其他修改分开发送。

### 更新 TTL 过期间隔 {#update-a-ttl-expiration-interval}

使用 [TTL 示例](/documentdb/reference/commands/indexing/createindexes/#unique-blocking-and-ttl-indexes)中由应用管理的 `flight_events` 集合，避免使共享航班数据集过期。先为日期字段创建过期间隔为 24 小时的索引，再将间隔缩短为一小时：

```javascript
db.flight_events.createIndex(
  { recorded_at: 1 },
  { name: "recorded_at_ttl", expireAfterSeconds: 86400 }
)

db.runCommand({
  collMod: "flight_events",
  index: { name: "recorded_at_ttl", expireAfterSeconds: 3600 }
})
```

新间隔从各事件 `recorded_at` 中的 BSON 日期开始计算，不是从修改时刻开始。缩短间隔可能使已有事件立即满足过期条件；但删除是异步进行的。

`expireAfterSeconds` 还可将符合条件的单字段、非 `_id` 索引转为 TTL 索引；适用的 TTL 索引类型限制与创建时相同。更新已有 TTL 过期间隔只修改元数据，不会重建索引。

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/coll_mod.c`、`ParseSpecSetCollModOptions`、`ParseIndexSpecSetCollModOptions` 和 `ModifyIndexSpecsInCollection`；规划器统计信息：`pg_documentdb/src/metadata/index.c`、`UpdateCollectionPlannerStatistics`。
