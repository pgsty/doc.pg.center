---
title: "spock.sub_resync_table"
description: "spock.sub_resync_table() 重新同步一张已有的表。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_resync_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_resync_table()` 重新同步一张已有的表。

## 概要 {#synopsis}

```sql
spock.sub_resync_table(subscription_name name, relation regclass, truncate boolean DEFAULT true)
```

## 说明 {#description}

`spock.sub_resync_table()` 重新同步一张已有的表。

安排重新同步后，函数会将本地缓存中该订阅提供方的 `spock.node` 记录与提供方自身的记录进行比较。若两者不同，它会发出 `WARNING`，提示使用 [`spock.node_refresh_info()`](/zh/pgedge/spock/reference/functions/spock-node-refresh-info/)。此检查不会更改 `spock.node`。如果无法连接到提供方进行检查，也只会发出 `WARNING`，重新同步仍会继续。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：已有订阅的名称。
- `relation`：已有表的名称，可带模式名。
- `truncate`：是否在同步前截断表，默认值为 `true`。省略此参数会截断目标表。显式传入 `false` 将保留已有行，此时新复制的行可能与之冲突并报错。

## 示例 {#example}

以下示例使用 `spock.sub_resync_table()`，为订阅 `sub_n1_n2` 重新同步 `public.users` 表。

```sql
SELECT spock.sub_resync_table('sub_n1_n2', 'public.users');
 sub_resync_table
------------------
 t
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_resync_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
