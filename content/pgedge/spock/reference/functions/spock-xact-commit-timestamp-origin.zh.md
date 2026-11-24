---
title: "spock.xact_commit_timestamp_origin()"
description: "返回指定事务 ID 对应的提交时间戳和复制来源标识符。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_xact_commit_timestamp_origin.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.xact_commit_timestamp_origin()

## 概要 {#synopsis}

spock.xact_commit_timestamp_origin (xid xid, OUT timestamp timestamptz,
OUT roident oid)

## 返回值 {#returns}

包含事务提交信息的一条记录，字段如下。

  - timestamp 是事务提交时间戳。
  - roident 是事务的复制来源标识符。

## 说明 {#description}

返回指定事务 ID 对应的提交时间戳和复制来源标识符。

函数查询 PostgreSQL 的提交时间戳跟踪系统，获取指定事务的提交时间及其复制来源。在多节点复制拓扑中，复制来源标识出源节点，可据此追溯变更来自何处。

必须在 PostgreSQL 中启用提交时间戳跟踪（track_commit_timestamp），函数才能返回有意义的结果。未启用时，函数可能返回 NULL 或报错。

对于在本节点本地提交的事务（即并非由其他节点复制而来），复制来源标识符 roident 为 `0`。对于复制过来的事务，该标识符指出变更来自哪个源节点。如果时间戳或来源返回 `NULL`，表示来源元数据不可用或未知，例如事务提交时未启用 `track_commit_timestamp`。`NULL` 与 `0` 含义不同，不能据此判定为本地变更。

此函数只执行查询，不修改任何数据。

## 参数 {#arguments}

**`xid`**

要查询的事务 ID。

## 示例 {#example}

    SELECT * FROM spock.xact_commit_timestamp_origin('12345'::xid);

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_xact_commit_timestamp_origin.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
