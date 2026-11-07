---
title: create
description: 创建 DocumentDB 集合或视图并配置其支持的选项。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/create.md
weight: 20
translation_source_sha256: 5f45b29202a483e06a991db02b7db8efa591bd93b4d30ca049fa2dc192659b19
translation_review: AI-assisted bilingual review; 2026-11-07
---

在当前数据库中创建一个集合或视图。

## 语法 {#syntax}

```javascript
db.createCollection("airports")
db.createView("delayed_flights", "flights", [{ $match: { status: "Delayed" } }])
```

该视图使用 [airline 示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)。请在插入机场示例之前运行 `airports` 的创建操作；它将创建一个空集合。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`create`** | (必需) 指定非空集合或视图名称的字符串。 |
| **`viewOn`** | (可选) 指定同一数据库中源集合或视图的字符串。 |
| **`pipeline`** | (可选) 指定视图聚合流水线的数组；需要 `viewOn`。`$out`、`$merge` 和 `$changeStream` 在视图定义中不允许使用。 |
| **`validator`** | (可选) 指定模式验证规则的文档；需要启用模式验证。 |
| **`validationLevel`** | (可选) 选择 `off`、`strict` 或 `moderate` 的字符串；需要支持模式验证。 |
| **`validationAction`** | (可选) 选择 `error` 或 `warn` 的字符串；需要支持模式验证。 |
| **`collation`** | (可选) 指定默认集合比较规则的文档。需要支持排序规则和集合排序规则。 |
| **`statsEnabled`** | (可选) 作为 DocumentDB 扩展提供的类布尔值，用于控制集合规划器统计信息。 |
| **`changeStreamPreAndPostImages`** | (可选) 一个文档，具有以下行为：`{ enabled: <boolean> }`；需要修改前镜像支持且集群版本为 0.112 或更高。若不可用则被拒绝。 |
| **`enableUpdateDescription`** | (可选) 作为 DocumentDB 扩展提供的类布尔值，用于控制变更流更新描述。 |
| **`comment`** | (可选) 用于网关请求追踪的跟踪上下文字符串；参见 [通用请求字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。 |
{.fields}

当模式验证被禁用时，`validator`、`validationLevel` 和 `validationAction` 被拒绝。启用后，`null` 或未定义值表示无显式设置。有关共享元数据和源码范围，请参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/create_collection_view.c`、`ParseCreateSpec` 和 `pg_documentdb/src/metadata/collection.c`。
