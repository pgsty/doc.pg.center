---
title: "spock.sub_show_table"
description: "spock.sub_show_table() 用于查看指定表的同步状态。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_show_table()` 显示表的同步状态。

## 概要 {#synopsis}

```sql
spock.sub_show_table(subscription_name name, relation regclass,
                     OUT nspname text, OUT relname text, OUT status text)
```

## 说明 {#description}

`spock.sub_show_table()` 用于查看指定表的同步状态。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：已有订阅的名称。
- `relation`：已有表的名称，可带模式名。

## 示例 {#example}

以下示例使用 `spock.sub_show_table()` 查看订阅 `sub_n2` 中 `test` 表的同步状态。

```sql
SELECT * FROM spock.sub_show_table('sub_n2', 'test');
-[ RECORD 1 ]----
nspname | public
relname | test
status  | unknown
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
