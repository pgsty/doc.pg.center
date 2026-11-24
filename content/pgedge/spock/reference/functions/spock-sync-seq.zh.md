---
title: "spock.sync_seq"
description: "函数读取提供方节点上序列的当前值，并将其写入复制流，以便订阅方将本地副本更新为相同的值，从而协调各节点的序列值。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_seq.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sync_seq()` 将序列的当前状态同步到所有相关订阅方。

## 概要 {#synopsis}

```sql
spock.sync_seq(relation regclass) RETURNS boolean
```

## 说明 {#description}

函数读取提供方节点上序列的当前值，并将其写入复制流，以便订阅方将本地副本更新为相同的值，从而协调各节点的序列值。

必须在提供方节点上执行此函数。序列状态更新包含在调用函数的事务中。订阅方复制该事务时会同时应用这项更新。

复制集过滤规则仍然适用。只有订阅了该序列所属复制集的订阅方才会收到这项更新。

## 参数 {#arguments}

此函数接受以下参数。

- `relation`：要同步的序列名称，可带模式名。

## 示例 {#example}

以下示例使用 `spock.sync_seq()` 同步序列 `public.sales_order_no_seq`。

```sql
SELECT spock.sync_seq('public.sales_order_no_seq');
 sync_seq
----------
 t
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sync_seq.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
