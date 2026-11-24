---
title: "spock.sub_remove_repset"
description: "spock.sub_remove_repset() 从订阅中移除一个复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_remove_repset.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_remove_repset()` 从订阅中移除一个复制集。

## 概要 {#synopsis}

```sql
spock.sub_remove_repset(subscription_name name, replication_set name)
```

## 说明 {#description}

`spock.sub_remove_repset()` 从订阅中移除一个复制集。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：已有订阅的名称。
- `replication_set`：要移除的复制集名称。

## 示例 {#example}

以下示例使用 `spock.sub_remove_repset()` 从订阅 `sub_n1_n2` 中移除复制集 `test`。

```sql
select spock.sub_remove_repset('sub_n1_n2', 'test');
 sub_remove_repset 
-------------------
 t
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_remove_repset.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
