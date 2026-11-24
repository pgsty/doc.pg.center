---
title: "常见问题"
description: "带 OID 的表可以使用列过滤，但 Spock 不支持按 oid 或 xmin 等系统列过滤。"
weight: 130
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/FAQ.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: "FAQ"
type: docs
translation_notice: en
translation_status: translated
---



### 使用列过滤 {#using-a-column-filter}

* 对于带 OID 的表，可以设置列过滤吗？能按 xmin 过滤吗？

  带 OID 的表可以使用列过滤，但 Spock 不支持按 `oid` 或 `xmin` 等系统列过滤。

* 删除用于过滤的列会怎样？

  目前，即使表在提供方参与 Spock 复制，也可以删除主键。如果在提供方删除参与过滤的列，列过滤列表也会移除它。可用 `spock.repset_show_table()` 核实。

  各订阅方仍保留原来的列定义，这是预期行为。在此状态下可以复制 INSERT，但不能复制 UPDATE 或 DELETE。

* 新增列会自动纳入过滤列表吗？

  在提供方给表新增列时，系统不会自动将该列加入列过滤列表。

### 使用行过滤 {#using-a-row-filter}

* 带 OID 的表能否使用 `row_filter`？能按 xmin 过滤吗？

  可以在带 OID 的表上使用 `row_filter`，但 Spock 无法按 `xmin` 等系统列过滤。

* `row_filter` 中可以使用哪些函数？例如，是否可以使用易变的采样函数？

  `row_filter` 可以调用不可变、稳定和易变函数。涉及写入时应谨慎，任何执行写入的表达式都有可能出错，导致复制停止。

  在 `row_filter` 中使用易变的采样函数，理论上适用于静态数据，但在运行中的系统上无法得到正确的数据快照，因而不适用。

* 可以按 JSONB 属性过滤吗？

  可以，`row_filter` 支持按 JSONB 值中的属性过滤。

### apply_delay 与时区变化 {#using-apply_delay-with-time-changes}

* `apply_delay` 如何处理夏令时等时区变化？

  注意，物理复制参数 `recovery_min_apply_delay` 的行为不同。若在夏令时期间设置它，实际延迟可能受时钟调整影响（例如，预期 2 小时，实际为 1 小时），因此可能需要每年两次停止并重新启动数据库服务。

  Spock 的 `apply_delay` 按时间间隔计算。即使切换夏令时或调整时区，配置的间隔也保持不变。但 Spock 复制需要约 5 分钟恢复，因此不建议在时钟调整期间运行重负载。

### 节点故障与恢复 {#node-failure-and-recovery}

* 如果一个节点崩溃，另一个节点滞后（例如缺少部分事务），该如何处理？

  若节点故障前订阅方尚未收到它的全部事务，可用 Active Consistency Engine（ACE）恢复落后节点。ACE 比较幸存节点的表数据，找出落后节点缺少的内容，并以已完全同步的节点为基准修复。修复时可以保留原始时间戳和来源 ID，确保复制元数据正确。操作步骤见[灾难性节点故障恢复](/zh/pgedge/spock/recovery/catastrophic-node-failure/)。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/FAQ.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
