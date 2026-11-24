---
title: "spock.cleanup_resolutions"
description: "从 spock.resolutions 中删除 log_time 早于保留窗口起点的行，返回删除的行数。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_cleanup_resolutions.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.cleanup_resolutions()` 用于手动删除 `spock.resolutions` 表中的旧记录。

## 概要 {#synopsis}

```sql
spock.cleanup_resolutions(days integer DEFAULT NULL) RETURNS bigint
```

## 说明 {#description}

从 `spock.resolutions` 中删除 `log_time` 早于保留窗口起点的行，返回删除的行数。

应用进程每天自动清理一次。超级用户可以通过此函数手动执行同一项清理，例如用 `pg_cron` 立即清理，或在应用进程未运行时清理。

显式传入的 `days` 优先于 `spock.resolutions_retention_days`，即使该 GUC 为 `0`（关闭自动清理）也一样。省略 `days` 时采用 GUC 的值。如果此值也是 `0`，函数返回 `0`，不删除任何行。

## 参数 {#arguments}

此函数接受以下参数。

- `days`：保留天数。本次调用使用该值覆盖 `spock.resolutions_retention_days`。如果已关闭自动清理（`resolutions_retention_days = 0`），仍可显式传值执行一次清理。默认值为 `NULL`，即采用 GUC 的值。

## 示例 {#example}

删除早于已配置保留窗口的记录。

```sql
SELECT spock.cleanup_resolutions();
```

删除 60 天以前的记录，忽略 GUC 设置。

```sql
SELECT spock.cleanup_resolutions(60);
```

## 另请参阅 {#see-also}

`spock.resolutions_retention_days`

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_cleanup_resolutions.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
