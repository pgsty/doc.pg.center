---
title: 监控集群配置与健康状态
description: 使用 Spock 信息表、状态视图、延迟跟踪、同步事件和 ACE 检查集群健康状况。
weight: 80
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/monitoring/index.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
linkTitle: 监控
icon: fa-solid fa-book-open
type: docs
---



Spock 扩展提供了多种方式来监控 Postgres 集群中的数据健康状况：

* 你可以查询 `spock` 模式中的[信息表](/pgedge/spock/monitoring/spock-info/)，查看集群配置和状态的相关信息。
* [状态视图](/pgedge/spock/monitoring/node-monitoring/) `spock.node_status`、`spock.subscription_status`、`spock.worker_status`、`spock.slot_status` 和 `spock.events` 无需读取服务器日志即可完整呈现一个节点的状态。
* Spock 扩展的[延迟跟踪](/pgedge/spock/monitoring/lag-tracking/)工具允许你查看各节点的复制延迟指标。
* 使用 Spock 的[同步事件](/pgedge/spock/monitoring/spock-sync-event/)工具来观察某笔特定事务何时完成复制。
* 使用 [ACE（Active Consistency Engine）](https://docs.pgedge.com/platform/ace)评估集群健康状况。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/monitoring/index.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
