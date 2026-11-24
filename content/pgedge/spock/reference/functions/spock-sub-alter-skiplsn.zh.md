---
title: "spock.sub_alter_skiplsn()"
description: "将已有订阅的复制位置推进到指定的日志序列号（LSN）。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_skiplsn.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_alter_skiplsn()`

## 概要 {#synopsis}

`spock.sub_alter_skiplsn (subscription_name name, lsn pg_lsn) RETURNS boolean`

## 返回值 {#returns}

成功设置跳过位置的 LSN 时返回 `true`，否则返回 `false`。

## 说明 {#description}

将已有订阅的复制位置推进到指定的日志序列号（LSN）。通常在复制流中的某项变更使订阅无法继续时，用此函数恢复复制。旧 LSN 到指定 LSN 之间的所有变更都会被永久跳过。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`subscription_name`**

已有订阅的名称。

**`lsn`**

订阅应推进到的日志序列号。

## 示例 {#example}

`SELECT spock.sub_alter_skiplsn('sub_n1_to_n2', '0/16B6A50');`

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_skiplsn.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
