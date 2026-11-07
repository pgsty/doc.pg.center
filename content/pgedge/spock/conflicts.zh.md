---
title: 冲突类型
description: 说明 Spock 在多主复制中检测到的冲突类型、解决策略、日志记录和与 PostgreSQL 18 原生逻辑复制的差异。
weight: 70
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/conflict_types.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 冲突类型
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



关于使用 delta-apply 列进行冲突*避免*，请参见[冲突避免与 delta-apply 列](/zh/pgedge/spock/conflict-avoidance/)。

在多主复制环境中，当两个或更多节点在重叠时间修改同一行（由主键或复制标识识别）时，就会发生冲突。Spock 在订阅者节点的 apply 阶段检测这些冲突，并按可配置的解决策略处理。

每个冲突都会归类为以下类型之一。可解决冲突会记录在 `spock.resolutions` 表中（启用 `spock.save_resolutions` 时）；不可解决冲突记录在 `spock.exception_log`。

## 摘要表 {#summary-table}

| 冲突类型 | DML | 是否可解决 |
|----------------------------|-----------|-------------------------------------|
| `insert_exists` | INSERT | 是 |
| `update_origin_differs` | UPDATE | 不适用（正常流程，不记录） |
| `update_exists` | UPDATE | 否（违反唯一约束），保存到 `spock.exception_log` |
| `update_missing` | UPDATE | 否（找不到行），保存到 `spock.exception_log` |
| `delete_origin_differs` | DELETE | 不适用（正常流程，不记录） |
| `delete_missing` | DELETE | 是 |
| `delete_exists` | DELETE | 是 |
{.wide .expand}

当 Spock 能够自动选择获胜元组并继续复制而无需运维人员介入时，该冲突是**可解决的**。`update_missing` 和 `update_exists` 不可解决，会产生 ERROR 并记录到 `spock.exception_log`。

---

## `insert_exists` {#insert_exists}

远端 INSERT 到达时，本地节点已存在具有相同主键（或复制标识）的行。这通常发生在两个节点独立插入相同键的行时。

Spock 会在唯一索引（主键、复制标识，以及在启用 `spock.check_all_uc_indexes` 时可选包含所有唯一约束）中查找传入元组来检测冲突。

**解决方式：** 可配置冲突解决器（默认 `last_update_wins`）比较本地与远端行的提交时间戳。获胜者的值作为 UPDATE 应用到既有行。

---

## `update_origin_differs` {#update_origin_differs}

远端 UPDATE 目标行的本地副本最后由另一个复制源修改。在多主拓扑中，这是正常复制流程——两个节点各自修改一行并传播变更——因此 Spock 不把它视为真正的冲突。不过 PostgreSQL 原生逻辑复制会将其归类为冲突，Spock 为完整性跟踪该类型，并通过 `spock.log_origin_change` GUC 支持可选日志记录。

Spock 通过比较 `replorigin_session_origin`（传入变更的来源）与本地元组上记录的复制源来检测它。来自同一复制源或同一本地事务的变更会被静默应用，不报告冲突。

**解决方式：** 可配置冲突解决器（默认 `last_update_wins`）决定获胜者。由于这是正常复制流程，无论哪一方获胜，事件都不会写入 `spock.resolutions`。

---

## `update_exists` {#update_exists}

远端 UPDATE 通过复制标识成功应用，但新行值违反另一个索引上的唯一约束。例如，UPDATE 修改了二级唯一索引中的列，而新值与另一既有行冲突。

该冲突类型与 PostgreSQL 18 原生逻辑复制使用的定义一致。检测到唯一约束违规时，Spock 会将其报告给 PostgreSQL 服务器日志和 PG18 冲突统计信息。

**解决方式：** 该冲突**不可**自动解决。错误会写入 `spock.exception_log`。

---

## `update_missing` {#update_missing}

远端 UPDATE 在本地节点找不到目标行。该行可能已在本地删除，也可能因复制缺口而从未到达。

Spock 会短暂等待并多次重试查找，以防并发事务正在插入该行。如果重试后仍找不到该行，则引发冲突。

**解决方式：** 该冲突**不可解决**。Spock 引发 ERROR，并记录到 `spock.exception_log`。

---

## `delete_origin_differs` {#delete_origin_differs}

远端 DELETE 目标行在本地存在，但最后由另一个复制源修改。与 `update_origin_differs` 一样，这是正常复制流程而非真正冲突——一个节点删除某行，而另一个节点较早的更新仍在传输中。Spock 跟踪该类型是因为 PostgreSQL 原生逻辑复制视其为冲突，并通过 `spock.log_origin_change` 支持可选日志记录。

如果本地元组与传入 DELETE 来自同一复制源，或来自同一本地事务，则 DELETE 会被静默应用，不报告冲突。

**解决方式：** 可配置冲突解决器（默认 `last_update_wins`）决定获胜者。远端 DELETE 获胜时，删除继续执行。本地元组获胜（即更新）时，删除被跳过并保留该行；此情况会报告为 `delete_exists`。

---

## `delete_missing` {#delete_missing}

远端 DELETE 在本地节点找不到目标行。该行很可能已被本地事务或其他复制事务删除。

与 `update_missing` 一样，Spock 会在确认行不存在前多次重试查找。

**解决方式：** 该冲突通过跳过 DELETE 自动解决（`skip`）。行已经不存在，因此期望的最终状态已达成。事件记录在 `spock.resolutions` 表中。

---

## `delete_exists` {#delete_exists}

远端 DELETE 到达时，本地行副本的提交时间戳晚于该 DELETE。这是 Spock 独有情况，在 PostgreSQL 原生逻辑复制中没有对应类型。

它发生在一个节点删除某行，而另一个节点在较晚时间戳更新该行时。DELETE 是较旧操作，因此应保留更新后的行。

**解决方式：** 跳过 DELETE 并保留本地（较新）行（`skip` / `keep_local`）。事件记录在 `spock.resolutions` 表中。

---

## 冲突解决策略 {#conflict-resolution-strategies}

`spock.conflict_resolution` GUC 控制如何裁决可解决冲突（除 `update_missing` 和 `update_exists` 外的所有类型）。当前 Spock 版本支持的值为：

| 策略 | 行为 |
|-----------------------|-----------------------------------------------------------|
| `last_update_wins` | 提交时间戳最新的行获胜（默认）。 |
{.wide .expand}

`last_update_wins` 要求设置 `track_commit_timestamp = on`，该参数位于 `postgresql.conf`。

**平局判定：** 当两行提交时间戳相同时，Spock 使用 `tiebreaker` 值决定获胜者；该值来自 `spock.node` 配置。tiebreaker 值较低的节点获胜。默认情况下，tiebreaker 设置为节点的唯一 ID。

**tiebreaker 解析始终是本地的。** 每个节点都保存自己认为的各节点 tiebreaker 值，并从*自己的* `spock.node.info` 列读取。节点自身的 `info`（包括 `tiebreaker`）只填充一次——在创建节点时，或在其他节点首次订阅它时（通过 `spock.sub_create()`，此时获取 provider 的节点元数据）。

节点自身的 `location`、`country` 和 `info`（包括 `tiebreaker`）之后可以通过 [`spock.node_alter`](/pgedge/spock/reference/functions/spock-node-alter/) 修改——这是推荐方式，因为它会验证 `tiebreaker` 值并合并 `info` 而不是替换——也可以通过原生 `UPDATE spock.node` 修改。任一方式都会**自动传播到每个直接订阅它的节点**（参见[自动节点元数据传播](/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)）：

```sql
-- on n1, one of these two (node_alter validates tiebreaker, UPDATE does not):
SELECT spock.node_alter(p_info_patch => '{"tiebreaker": <unique_integer>}'::jsonb);

UPDATE spock.node
   SET info = COALESCE(info, '{}'::jsonb) ||
              '{"tiebreaker": <unique_integer>}'
 WHERE node_id = (SELECT node_id FROM spock.node_info());
```

每个直接订阅 `n1` 的节点都会获得该变更，无需进一步操作。该消息不会通过级联拓扑转发（Node A → Node B → Node C）：Node C 通常没有 `spock.node` 行用于记录 `n1`，除非它订阅 `n1`，因此没有可更新的对象。

拥有 `n1` 行但未应用该消息的节点会保留旧值。这发生在携带消息的事务被异常处理跳过或丢弃时。可使用 [`spock.node_refresh_info`](/pgedge/spock/reference/functions/spock-node-refresh-info/) 按需追赶：

```sql
-- on a node that has a stale row for n1:
SELECT spock.node_refresh_info('n1');   -- one node

SELECT spock.node_refresh_info();       -- or every known peer at once
```

让部分节点保持未刷新状态等同于用不同值更新它们：集群对同一节点的 tiebreaker 值不一致，可能导致不同节点以不同方式解决完全相同的冲突。

## 冻结元组与缺失时间戳数据 {#frozen-tuples-and-missing-timestamp-data}

基于时间戳的冲突解决依赖本地元组的提交时间戳和复制源信息。有两种情况会缺失这些信息：

**冻结元组。** PostgreSQL 会周期性“冻结”旧行版本，将其事务 ID 替换为 `FrozenTransactionId`。一旦冻结，就无法再取得原始提交时间戳和复制源。当 Spock 在冲突解决中遇到冻结的本地元组时，会将本地时间戳视为零。任何真实的远端时间戳都大于零，因此远端变更总是获胜。由于无法确定本地复制源，因此不记录冲突。

**`track_commit_timestamp = off`。** 如果禁用提交时间戳跟踪，Spock 无法取得任何本地元组的复制源或时间戳信息。此时，Spock 会将远端复制源和时间戳复制到本地值。随后同一复制源检查会看到匹配复制源，并将该变更视为正常复制流程——不会检测或记录冲突。这实际上使冲突解决不可见：远端变更总是被静默应用。

要获得可靠的冲突检测和解决，必须将 `track_commit_timestamp` 设置为 `on`。

## 冲突日志 {#conflict-logging}

- **`spock.save_resolutions`**（默认 `off`）——启用时，已解决冲突会以 JSON 格式的完整元组详情写入 `spock.resolutions` 表。
- **`spock.conflict_log_level`**（默认 `LOG`）——控制检测到的冲突以哪个 PostgreSQL 日志级别报告。设置为低于 `log_min_messages` 的级别可抑制日志输出。
- **`spock.log_origin_change`**（默认 `none`）——控制 `update_origin_differs` 和 `delete_origin_differs` 事件（正常复制流程）是否记录到 PostgreSQL 服务器日志。这些事件永远不会写入 `spock.resolutions`。选项为 `none`、`remote_only_differs`、`since_sub_creation`。

## 与 PostgreSQL 18 原生逻辑复制比较 {#comparison-with-postgresql-18-native-logical-replication}

PostgreSQL 18 为逻辑复制引入了内建冲突检测。Spock 的冲突类型与 PostgreSQL 定义对齐（名称和枚举顺序相同），使两个系统以一致方式报告冲突。关键差异在于各自如何*解决*冲突，以及在哪里*记录*冲突。

| 冲突类型 | PostgreSQL 18 | Spock（last update wins） |
|-------------------------|----------------------------------------|----------------------------------------------|
| `insert_exists` | 记录日志并引发 ERROR。 | 通过 `last_update_wins` 解决；将 INSERT 转换为获胜元组的 UPDATE。 |
| `update_origin_differs` | 记录日志并总是应用远端元组。 | 通过 `last_update_wins` 解决；本地元组可能获胜。视为正常复制流程（非真正冲突），可通过 `log_origin_change` 可选记录。 |
| `update_exists` | 检测更新行上的唯一约束违规；记录日志。 | 记录日志并写入 `spock.exception_log`。 |
| `update_missing` | 记录日志并跳过。 | 记录日志并写入 `spock.exception_log`。 |
| `delete_origin_differs` | 记录日志并总是应用 DELETE。 | 通过 `last_update_wins` 解决；本地元组可能获胜（报告为 `delete_exists`）。视为正常复制流程（非真正冲突），可选记录日志。 |
| `delete_missing` | 记录日志并跳过。 | 记录日志并跳过。记录到 `spock.resolutions`。 |
| `delete_exists` | 无等价类型。 | Spock 独有。本地行比远端 DELETE 新，因此跳过 DELETE 并保留该行。 |
{.wide .expand}

**解决方式。** PostgreSQL 18 不解决冲突——它要么无条件应用远端变更，要么跳过操作，并记录事件。Spock 增加可配置解决策略（默认 `last_update_wins`）和平局判定机制，使较新的本地元组可以获胜。

**持久化。** PostgreSQL 18 只将冲突写入 PostgreSQL 服务器日志。Spock 还会将某些冲突持久化到 `spock.resolutions` 表（含 JSON 格式完整元组详情）——具体为 `insert_exists`、`delete_missing` 和 `delete_exists`——并将不可解决冲突（`update_missing`、`update_exists`）写入 `spock.exception_log`。复制源差异事件不会持久化到这两个表。

**统计信息。** 在 PostgreSQL 18 上，Spock 会将所有冲突类型报告给原生 `pgstat` 订阅冲突统计，因此它们会出现在内建逻辑复制使用的同一批视图中。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/conflict_types.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
