---
title: 过滤
description: 在提供者和订阅者上配置 Spock 的基于行数据过滤器及其会话限制。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/filtering.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 允许在提供者侧和订阅者侧进行基于行的过滤。

## 提供者上的行过滤 {#row-filtering-on-the-provider}

在提供者上，你可以通过 `spock.repset_add_table` 函数的 `row_filter` 属性实现行过滤。`row_filter` 是普通 PostgreSQL 表达式，具有与 `CHECK` 约束相同的限制。

一个简单的 `row_filter` 类似于 `row_filter := 'id > 0'`；该过滤器确保只复制 `id` 列值大于零的行。

你可以在 `row_filter` 内使用易变函数，但要对 `writes` 保持谨慎，因为任何会执行写入的表达式都可能抛出错误并停止复制。

值得注意的是，`row_filter` 在复制会话内运行；因此，诸如 `CURRENT_USER` 这类特定于会话的表达式会使用复制会话的值，而不是执行写入的会话的值。

## 订阅者上的行过滤 {#row-filtering-on-the-subscriber}

在订阅者上，可以使用标准 `BEFORE TRIGGER` 机制实现基于行的过滤。你必须把触发器标记为 `ENABLE REPLICA` 或 `ENABLE ALWAYS`，否则复制进程不会执行它们。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/filtering.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
