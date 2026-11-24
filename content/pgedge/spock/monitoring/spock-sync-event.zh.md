---
title: "使用 spock.sync_event 确认同步进度"
description: "在提供方创建同步事件，在订阅方确认指定 LSN 已收到并应用。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/spock_sync_event.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sync_event` 用于跟踪 Spock 逻辑复制中提供方与订阅方之间的同步事件。通过 `spock.sync_event` 和 PostgreSQL 的日志序列号（LSN），可以确认订阅方已收到并应用提供方截至指定位置的全部变更。

先在选作提供方的节点调用函数，写入同步标记，并取得供订阅方等待的事件 LSN。

`spock.sync_event()`

再在选作订阅方的节点调用等待过程，以确认该位置的事件已经收到并应用。

`spock.wait_for_sync_event(...)`（必需参数见[概要](#synopsis)）

## 语法 {#synopsis}

在提供方调用时，此函数返回当前 `pg_lsn`，标记复制流中的一个位置。`spock.sync_event` 语法如下。

`spock.sync_event(transactional boolean DEFAULT false) RETURNS pg_lsn`

`transactional` 为 `false`（默认）时，标记立即写入 WAL 流，与调用方事务独立。`transactional` 为 `true` 时，标记与当前事务绑定，只有该事务提交后订阅方才能看到。

在订阅方调用的 `spock.wait_for_sync_event` 有两种形式，一种用 origin_id（类型 `oid`）标识节点，另一种用节点名。

- `spock.wait_for_sync_event(OUT result boolean, origin_id oid, lsn pg_lsn, timeout int DEFAULT 0, wait_if_disabled bool DEFAULT false)`

- `spock.wait_for_sync_event(OUT result boolean, origin name, lsn pg_lsn, timeout int DEFAULT 0, wait_if_disabled bool DEFAULT false)`

此过程在订阅方等待，直到收到并应用提供方的指定 LSN，再告知调用者。

参数如下。

- `origin_id` 或 `origin`：提供方节点的 OID 或名称。
- `lsn`：要等待的目标 LSN。
- `timeout`（可选）：等待时长，单位为秒。默认 0，表示无限等待。
- `wait_if_disabled`（可选）：订阅不存在或已禁用时如何处理，默认 `false`。

  `wait_if_disabled` 为 `false`（默认）时，从来源节点到本节点的订阅必须已经存在且已启用。找不到订阅或订阅在等待期间任何时候被禁用，都会报错。

  ```
  ERROR:  No subscription found for replication 16443 => 16444
  ERROR:  Subscription 16443 => 16444 has been disabled
  ```

  `wait_if_disabled` 为 `true` 时，这两种情形都不会报错。过程持续轮询，直到订阅存在、已启用并到达目标 LSN，或 `timeout` 到期。适用于新加入的节点仍在建订阅，或维护中临时禁用订阅等情况。由于缺少订阅时不会报错，应传入非零 `timeout`，防止一直等候一个永远不会创建的订阅。

  `wait_if_disabled` 仅影响订阅检查。两种形式都先校验参数，无论该值如何，下列错误仍会立即抛出。

  ```
  ERROR:  Origin node 'provider_node' not found
  ERROR:  Invalid NULL origin_id
  ```

  按名称调用时，来源节点必须已登记在 `spock.node` 中。若节点仍在加入集群，相应记录可能尚不存在。可在登记完成后取得 `origin_id`，或稍后重试。

返回结果如下。

- `result = true`：已收到并应用目标 LSN。
- `result = false`：到达目标位置之前超时。若 `wait_if_disabled = true`，也可能是订阅在期限内一直未创建或未启用。

## 示例 {#examples}

在提供方节点上执行：

`SELECT spock.sync_event();` `-- Returns: 0/16342B0 (example output)`

在订阅方节点上执行：

```sql
CALL spock.wait_for_sync_event(NULL, 'provider_node', '0/16342B0', 10);
-- result: true  (if applied within 10s), false otherwise
```

第一个参数是 OUT 参数 `result` 的占位符。在 `CALL` 语句中传入 `NULL`，再从过程结果中读取输出值。

若节点的订阅可能尚未创建或启用，可同时传入 `wait_if_disabled = true` 和超时值。

```sql
CALL spock.wait_for_sync_event(NULL, 'provider_node', '0/16342B0', 300, true);
-- result: true once the subscription is enabled and has applied the LSN,
-- false if 300s elapse first (including if the subscription never appeared)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/spock_sync_event.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
