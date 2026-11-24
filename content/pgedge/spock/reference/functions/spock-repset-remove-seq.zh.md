---
title: "spock.repset_remove_seq()"
description: "从已有的 Spock 复制集中移除序列。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_seq.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_remove_seq ()`

## 概要 {#synopsis}

spock.repset_remove_seq (
    set_name name,
    relation regclass)

## 返回值 {#returns}

- 成功从复制集移除序列时返回 true。
- 如果序列不属于该复制集、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

从已有的 Spock 复制集中移除序列。

移除后，序列值的变更将不再复制到该复制集的订阅方。

函数更新 Spock 系统目录中的元数据，不修改 PostgreSQL 配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`relation`**

要移除的序列，以 regclass 指定，例如 `'public.my_sequence'`。

## 示例 {#example}

从 demo_repset 复制集中移除序列 public.orders_id_seq。

    postgres=# SELECT spock.repset_remove_seq('demo_repset', 'public.orders_id_seq');
     repset_remove_seq 
    -------------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_seq.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
