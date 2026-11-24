---
title: "spock.sub_alter_sync"
description: "spock.sub_alter_sync() 一次处理所有复制集中尚未同步的表，逐表复制并同步。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_sync.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_alter_sync()` 在一次操作中同步所有复制集中尚未同步的表。

## 概要 {#synopsis}

```sql
spock.sub_alter_sync(subscription_name name, truncate boolean DEFAULT false)
RETURNS boolean
```

## 说明 {#description}

`spock.sub_alter_sync()` 一次处理所有复制集中尚未同步的表，逐表复制并同步。函数会在操作完成前返回。可使用 `spock.sub_wait_for_sync()` 等待同步完成。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name` 指定已有订阅的名称。
- `truncate` 为布尔值。设为 `true` 时，在复制前截断表，默认为 `false`。

## 示例 {#example}

以下示例调用 `spock.sub_alter_sync()`，同步订阅 `sub_n1_n2` 中所有尚未同步的表。

```sql
SELECT spock.sub_alter_sync('sub_n1_n2', true);
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_sync.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
