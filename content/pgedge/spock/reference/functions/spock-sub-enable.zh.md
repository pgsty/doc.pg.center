---
title: "spock.sub_enable"
description: "spock.sub_enable() 用于启用订阅。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_enable.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_enable()` 启用订阅，随后复制进程恢复对该订阅的正常处理。

## 概要 {#synopsis}

```sql
spock.sub_enable(subscription_name name, immediate boolean)
```

## 说明 {#description}

`spock.sub_enable()` 用于启用订阅。

如果此节点上的另一个订阅已经启用了来源转发，此操作会失败。详见[来源转发](/zh/pgedge/spock/reference/sub-mgmt/#origin-forwarding)。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：已有订阅的名称。
- `immediate`：若为 `true`，立即启动订阅。否则在当前事务结束时才启动。默认为 `false`。

## 示例 {#example}

以下示例使用 `spock.sub_enable()` 启用名为 `sub_n1_n2` 的订阅。

```sql
SELECT spock.sub_enable('sub_n1_n2');
 sub_enable
-------------
 t
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_enable.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
