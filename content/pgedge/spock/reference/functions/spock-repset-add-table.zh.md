---
title: "spock.repset_add_table()"
description: "将指定的表添加到已有的 Spock 复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_add_table()`

## 概要 {#synopsis}

spock.repset_add_table (
    set_name name,
    relation regclass,
    synchronize_data boolean,
    columns text[],
    row_filter text,
    include_partitions boolean
)

## 返回值 {#returns}

- 表成功加入复制集时返回 true。
- 如果表已是成员、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

将指定的表添加到已有的 Spock 复制集。

可以通过以下可选设置精确控制需要复制的数据。

- 指定要复制的列子集。
- 指定行过滤条件，限制参与复制的行。
- 指定是否同时纳入分区表的分区。

如果 synchronize_data 为 true，表中已有的数据会复制到订阅该复制集的所有订阅方。否则只复制后续变更。

对于分区表，include_partitions 控制是否将子分区自动加入复制集。

此函数向 Spock 系统目录写入元数据，不修改 PostgreSQL 配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`relation`**

要添加的表，以 regclass 指定，例如 `'public.mytable'`。

**`synchronize_data`**

设为 true 时，将表中已有数据同步到所有订阅方。默认为 false。

**`columns`**

可选，要复制的列名列表。为 NULL 时复制所有列。

**`row_filter`**

可选的 SQL WHERE 子句，用来限定要复制的行。

**`include_partitions`**

如果为 true 且目标是分区表，则自动纳入所有分区。默认为 true。

## 示例 {#example}

以下命令将 public.accounts 添加到 demo_repset 复制集，复制整张表。

    SELECT spock.repset_add_table('demo_repset', 'public.accounts');

以下命令将 public.accounts 添加到 demo_repset 复制集，并同步已有数据。

    SELECT spock.repset_add_table('demo_repset',
        'public.accounts',
        synchronize_data := true);

以下命令只将 public.accounts 的 id 和 balance 两列加入 demo_repset 复制集，并按条件筛选行。

    SELECT spock.repset_add_table('demo_repset',
        'public.accounts',
        columns := ARRAY['id','balance'],
        row_filter := 'balance > 0');

**警告：使用有效的行过滤条件同步数据时需谨慎。** 对于一张表，指定有效的 `row_filter` 并设置 `synchronize_data=true` 通常是一次性操作。修改 `row_filter` 后再次执行不会向订阅方同步数据。可能需要调用 `spock.sub_resync_table()` 重新同步。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
