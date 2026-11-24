---
title: "spock.repset_add_seq()"
description: "向已有的 Spock 复制集添加一个序列。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_seq.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_add_seq()`

## 概要 {#synopsis}

spock.repset_add_seq (
    set_name name,
    relation regclass,
    synchronize_data boolean)

## 返回值 {#returns}

- 序列成功加入复制集时返回 true。
- 如果序列已是复制集成员、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

向已有的 Spock 复制集添加一个序列。

序列加入后，其值的变更会复制到订阅了该复制集的订阅方，从而使多主环境中各节点的 nextval 操作保持一致。

若 synchronize_data 为 true，序列的当前值会立即同步到所有订阅方。

函数更新 Spock 系统目录中的元数据，不修改 PostgreSQL 配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`relation`**

要添加的序列，以 regclass 指定，例如 `'public.my_sequence'`。

**`synchronize_data`**

若为 true，序列的当前值会同步到所有订阅方。默认为 false。

## 示例 {#example}

将序列 public.sales_order_no_seq 添加到 `'default'` 复制集。

    postgres=# SELECT spock.repset_add_seq('default', 'public.sales_order_no_seq');
     repset_add_seq
    ----------------
     t
    (1 row)

添加序列 public.sales_invoice_no_seq，并同步其当前值。

    postgres=# SELECT spock.repset_add_seq(
        'default',
        'public.sales_invoice_no_seq',
        synchronize_data := true
    );
     repset_add_seq
    ----------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_seq.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
