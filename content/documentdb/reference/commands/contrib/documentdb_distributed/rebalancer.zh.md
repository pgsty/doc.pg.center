---
title: 分布式再平衡器
description: 通过线协议命令启动、检查和停止 DocumentDB 分布式分片再平衡。
type: docs
search_keywords: [rebalancer, balancerStart, balancerStatus, balancerStop, documentdb_distributed]
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/rebalancer.md
weight: 20
translation_source_sha256: 6fdc1efe906c148ac4bd0721686d04d29de73d85673088832aed21fb9fea450b
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

`balancerStart`、`balancerStatus` 和 `balancerStop` 命令需要 [documentdb_distributed 及其依赖项](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation)。这些命令管理跨集群的后台分片再平衡作业，不会改变集合的逻辑分片键。请在 `admin` 数据库上运行这些线协议命令。

## 可用性 {#availability}

是否可用取决于提供商的网关实现。提供商网关必须将这些线协议命令接入分布式再平衡器实现，包括转发用户指定的 `strategy` 选项。

部署还必须单独启用再平衡器功能；在核查过的实现中，此功能默认关闭。启动再平衡要求部署中已禁用变更流。

## 检查状态 {#inspect-status}

```javascript
db.adminCommand({ balancerStatus: 1 })
```

响应包含 `ok` 和 `mode`；有已调度或正在运行的作业时，后者为 `full`，否则为 `off`。响应还可能包含 `runningJobs`、`otherJobs` 和 `strategies`。还应检查各作业的状态：即使 `mode` 为 `off`，正在取消或正在处理失败的作业仍可能阻止新的再平衡。

`strategies` 条目标明可用策略名称以及各策略是否为默认策略。`runningJobs` 和 `otherJobs` 包含分片再平衡作业信息，包括任务状态计数和可用的任务详情。

## 启动再平衡 {#start-rebalancing}

使用当前默认策略启动后台再平衡：

```javascript
db.adminCommand({ balancerStart: 1 })
```

命令启动后台工作后返回 `{ ok: 1 }`，不会等待再平衡结束；请通过 `balancerStatus` 监视进度。

| 参数 | 说明 |
| --- | --- |
| **`balancerStart`** | （必需）命令标记，通常为 `1`。 |
| **`strategy`** | （可选）字符串，选择分片再平衡策略。使用状态响应中 `strategies` 列出的名称。指定此值会在启动作业前更改默认再平衡策略。 |
{.fields}

指定策略时，在命令文档中将 `strategy` 与 `balancerStart` 并列。策略名称来自具体部署，而不是固定的 DocumentDB 列表；请使用 `balancerStatus` 返回的 `strategies` 条目中的 `strategy_name`。

例如，当状态列出至少一个策略时，以下命令选择第一个列出的策略，并以此启动再平衡。它是上方默认策略启动方式的另一种选择，不要在前一个再平衡仍活跃时运行：

```javascript
const status = db.adminCommand({ balancerStatus: 1 })
const strategy = status.strategies[0].strategy_name
db.adminCommand({ balancerStart: 1, strategy: strategy })
```

同一时间只能有一个活跃的再平衡。处于 `scheduled`、`running`、`cancelling` 或 `failing` 状态的作业会阻止新的启动请求。

## 停止再平衡 {#stop-rebalancing}

```javascript
db.adminCommand({ balancerStop: 1 })
```

响应包含 `ok` 和 `wasActive`。`wasActive: true` 表示找到了活跃作业并已请求停止，并不证明所有任务都已停止。再次调用 `balancerStatus` 确认最终作业状态。如果没有活跃作业，调用仍成功，但返回 `wasActive: false`。

## 实现 {#implementation}

源码修订见[线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

`balancerStart`、`balancerStatus` 和 `balancerStop` 线协议 API 分别映射到 SQL UDF `documentdb_api_distributed.rebalancer_start`、`documentdb_api_distributed.rebalancer_status` 和 `documentdb_api_distributed.rebalancer_stop`。

源码：[分布式分片再平衡器](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/rebalancer/shard_rebalancer.c)、`command_rebalancer_start`、`command_rebalancer_status` 和 `command_rebalancer_stop`；配置：`src/documentdb_distributed_init.c`、`documentdb_distributed.enable_shard_rebalancer_apis`。
