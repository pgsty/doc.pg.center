---
title: 监控集群配置与健康状态
description: 使用 Spock 信息表、状态视图、延迟跟踪、同步事件和 ACE 检查集群健康状况。
weight: 80
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/index.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
linkTitle: 监控
icon: fa-solid fa-book-open
type: docs
---



可通过以下方式监控 PostgreSQL 集群的复制状态和数据一致性。

* 你可以查询 `spock` 模式中的[信息表](/zh/pgedge/spock/monitoring/spock-info/)，查看集群配置和状态的相关信息。
* [状态视图](/zh/pgedge/spock/monitoring/node-monitoring/) `spock.node_status`、`spock.subscription_status`、`spock.worker_status`、`spock.slot_status` 和 `spock.events` 无需读取服务器日志即可完整呈现一个节点的状态。
* Spock 扩展的[延迟跟踪](/zh/pgedge/spock/monitoring/lag-tracking/)工具允许你查看各节点的复制延迟指标。
* 使用 Spock 的[同步事件](/zh/pgedge/spock/monitoring/spock-sync-event/)工具来观察某笔特定事务何时完成复制。
* 使用 [ACE（Active Consistency Engine）](https://docs.pgedge.com/platform/ace)评估集群健康状况。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/index.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
