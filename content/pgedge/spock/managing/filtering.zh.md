---
title: 过滤
description: 在提供者和订阅者上配置 Spock 的基于行数据过滤器及其会话限制。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/filtering.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 支持在提供方和订阅方按行过滤。

## 在提供方过滤行 {#row-filtering-on-the-provider}

在提供方，`spock.repset_add_table` 的 `row_filter` 属性用于指定行过滤条件。它是普通的 PostgreSQL 表达式，受到与 `CHECK` 约束相同的限制。

一个简单的 `row_filter` 类似于 `row_filter := 'id > 0'`；该过滤器确保只复制 `id` 列值大于零的行。

可以在 `row_filter` 中使用易变函数。如果表达式会执行写入，要格外谨慎：写入可能报错并中断复制。

`row_filter` 在复制会话中运行。因此，`CURRENT_USER` 等与会话有关的表达式取复制会话中的值，而非最初执行写入的会话中的值。

## 在订阅方过滤行 {#row-filtering-on-the-subscriber}

在订阅方，可以使用标准的 `BEFORE TRIGGER` 机制按行过滤。必须将触发器标记为 `ENABLE REPLICA` 或 `ENABLE ALWAYS`，复制进程才会执行它。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/filtering.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
