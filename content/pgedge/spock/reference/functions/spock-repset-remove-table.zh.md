---
title: "spock.repset_remove_table()"
description: "从已有的 Spock 复制集中移除表。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_remove_table ()`

## 概要 {#synopsis}

spock.repset_remove_table (
    set_name name,
    relation regclass,
    include_partitions boolean)

## 返回值 {#returns}

- 成功从复制集移除表时返回 true。
- 如果表不属于该复制集、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

从已有的 Spock 复制集中移除表。此后，该表的变更将不再复制到订阅此复制集的订阅方。

如果是分区表，include_partitions 参数控制是否也将其所有子分区移出复制集。

函数更新 Spock 系统目录中的元数据，不修改 PostgreSQL 配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`relation`**

要移除的表，以 regclass 指定，例如 `'public.mytable'`。

**`include_partitions`**

如果设为 true 且目标是分区表，其所有分区也会从复制集中移除。默认为 true。

## 示例 {#example}

从 default 复制集中移除表 public.users。

    postgres=# SELECT spock.repset_remove_table('default', 'public.users');
     repset_remove_table 
    ---------------------
     t
    (1 row)

从 default 复制集中移除分区表 public.sales_parent，并保留其分区的成员资格。

    postgres=# SELECT spock.repset_remove_table('default',
    'public.users',
    include_partitions := false);
    ---------------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
