---
title: explain
description: 解释支持的 DocumentDB 读取命令，并选择诊断详细程度。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/explain.md
weight: 60
translation_source_sha256: 746467107201bccb495cca9e29286b3786e262cb4498191c487279d1389876b2
translation_review: AI-assisted bilingual review; 2026-11-07
---

返回 `find`、`aggregate`、`count` 或 `distinct` 的规划信息。默认网关不解释写入命令。

```javascript
db.flights.find({ status: "Delayed" }).explain("executionStats")
```

| 参数 | 描述 |
| --- | --- |
| **`explain`** | (必需) 指定嵌套读取命令的文档，具有与其命令页面相同的选项。 |
| **`verbosity`** | (可选) 选择 `queryPlanner`（默认）、`executionStats` 或 `allPlansExecution` 的字符串。DocumentDB 还识别 `allShardsQueryPlan` 和 `allShardsExecution` 用于分布式诊断。 |
{.fields}

`allPlansExecution` 提供详细的执行计划，包括基于游标的规划细节以及执行统计信息。使用它来调查游标查询的规划方式。

执行统计信息模式会执行底层读取操作以收集统计信息。未识别的详细程度字符串将遵循实现的默认模式，而不是选择新的诊断模式。`aggregate` 也接受 `explain: true` 直接传入。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：网关 `explain/mod.rs`、`process_explain` 和 `Verbosity`。
