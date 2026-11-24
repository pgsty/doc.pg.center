---
title: "spock.version()"
description: "以便于阅读的主、次版本形式返回 Spock 版本，例如 5.0.5。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.spock_version()`

## 概要 {#synopsis}

`spock.spock_version ()`

## 说明 {#description}

以便于阅读的主、次版本形式返回 Spock 版本，例如 `5.0.5`。

## 示例 {#example}

```sql
postgres=# SELECT spock.spock_version();
 spock_version
---------------
 5.0.5
(1 row)
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
