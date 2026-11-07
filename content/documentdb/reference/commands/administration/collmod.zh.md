---
title: collMod
description: 在 DocumentDB 中修改集合、视图、模式验证和索引设置。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/collMod.md
weight: 10
translation_source_sha256: ddbfb41db8931e0a4a2f0e33a85f4128c41ba4ab0149f51b82ec392f38a0b4b9
translation_review: AI-assisted bilingual review; 2026-11-07
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
| **`enableStats`** | (可选) 作为 DocumentDB 扩展提供的布尔值，用于控制规划器统计信息。 |
| **`colocation`** | (可选) 作为 DocumentDB 扩展提供的文档，传递给部署的集合共置钩子；默认单节点后端无变化；嵌套选项为部署特定。 |
| **`changeStreamPreAndPostImages`** | (可选) 具有以下行为的文档：`{ enabled: <boolean> }`；当启用修改前镜像支持且集群版本不低于 0.112 时应用；否则被忽略。 |
| **`enableUpdateDescription`** | (可选) 类布尔值，用于启用或禁用变更流更新描述。 |
{.fields}

`index` 文档接受：

| 参数 | 描述 |
| --- | --- |
| **`name`** | (可选) 通过名称选择索引的字符串；需提供此项或 `keyPattern`。 |
| **`keyPattern`** | (可选) 通过其键规范选择索引的文档。 |
| **`newName`** | (可选) 重命名所选索引的字符串。 |
| **`hidden`** | (可选) 类布尔值，更改索引可见性，受索引限制约束。 |
| **`prepareUnique`** | (可选) 类布尔值，为支持的非唯一索引准备唯一性转换。 |
| **`unique`** | (可选) 类布尔值，请求唯一性转换，受现有数据验证和索引类型约束。 |
| **`expireAfterSeconds`** | (可选) 非负数，更改 TTL 索引的过期间隔。 |
| **`reindex`** | (可选) 类布尔值，必须为 `true`。排队重新索引请求。通过 [`currentOp`](/documentdb/reference/commands/diagnostic/currentop/) 监控进度。 |
| **`updateOptions`** | (可选) 类布尔值，控制重建时刷新索引选项。 |
{.fields}

使用 `collMod.index.reindex` 重建索引。DocumentDB 特有的选项没有专用 shell 辅助函数：

```javascript
db.runCommand({ collMod: "flights", index: { name: "route_no_1", reindex: true } })
```

`dryRun` 不是受支持的顶层字段。当模式验证被禁用时，模式验证设置（包括 `validator`）被拒绝。共享字段如 `writeConcern` 和 `comment` 被接受，且不改变修改语义。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

参见 [在现有数据上构建唯一索引](/documentdb/reference/commands/indexing/createindexes/#build-a-unique-index-on-existing-data) 了解分阶段的 `buildAsUnique`、`prepareUnique` 和 `unique` 工作流。

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/coll_mod.c`、`ParseSpecSetCollModOptions` 和 `ParseIndexSpecSetCollModOptions`。
