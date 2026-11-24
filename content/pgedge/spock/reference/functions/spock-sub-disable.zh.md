---
title: "spock.sub_disable"
description: "spock.sub_disable 的用途、参数和用法。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_disable.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_disable()` 禁用订阅，并断开与提供方的连接。

## 概要 {#synopsis}

```sql
spock.sub_disable(subscription_name name, immediate boolean DEFAULT false)
```

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：已有订阅的名称。
- `immediate`：若为 `true`，立即禁用订阅。否则等到当前事务结束时才禁用。默认为 `false`。

## 示例 {#example}

以下示例使用 `spock.sub_disable()` 禁用名为 `sub_n1_n2` 的订阅。

```sql
SELECT spock.sub_disable('sub_n1_n2');
 sub_disable
-------------
 t
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_disable.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
