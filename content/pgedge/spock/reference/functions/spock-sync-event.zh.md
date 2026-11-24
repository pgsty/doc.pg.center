---
title: "spock.sync_event"
description: "spock.sync_event() 在复制流中创建同步事件并返回其 LSN。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_event.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sync_event()` 在复制流中创建同步事件，并返回该事件的日志序列号（LSN）。

## 概要 {#synopsis}

```sql
spock.sync_event(transactional boolean DEFAULT false)
```

## 返回值 {#returns}

返回所创建同步事件的日志序列号（LSN），类型为 `pg_lsn`。

## 说明 {#description}

`spock.sync_event()` 在复制流中创建同步事件并返回其 LSN。

函数在当前写入位置向逻辑复制流插入一个专用同步标记。返回的 LSN 标识该标记在预写日志中的位置，可与 `spock.wait_slot_confirm_lsn()` 等函数配合使用，以确认订阅方已将复制变更处理到该位置。

同步事件可用于协调复制拓扑中多个节点的操作。在提供方创建同步事件，再等待订阅方到达其 LSN，即可确保所有节点处理过同一组变更，然后再执行依赖这些节点状态一致的操作。

同步事件本身不含数据，也不修改任何表，只在复制流中起协调标记的作用。

此函数通过插入同步标记来修改复制流。

## 参数 {#arguments}

- `transactional`（可选，默认 `false`）：为 `false` 时，同步事件标记立即写入 WAL 流，独立于调用该函数的事务。为 `true` 时，标记与调用事务绑定，只有事务提交后订阅方才能看到它。

## 示例 {#example}

以下示例通过 `spock.sync_event()` 创建同步事件，并返回其 LSN。

```sql
SELECT spock.sync_event();
-[ RECORD 1 ]---------
sync_event | 0/333F410
```

关于零停机添加节点时如何使用同步事件，详见 [ZODAN 教程](/zh/pgedge/spock/modify/zodan/zodan-tutorial/)。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_event.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
