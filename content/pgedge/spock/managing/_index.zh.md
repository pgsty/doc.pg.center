---
title: 管理 Spock 安装
description: 概览 Spock 的分区复制、数据过滤、只读模式、复制集、序列和大对象管理功能。
weight: 60
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/index.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
linkTitle: 管理复制
icon: fa-solid fa-book-open
type: docs
---



Spock 提供以下复制管理功能。

* [复制分区表](/zh/pgedge/spock/managing/partition-mgmt/)。
* 创建基于行的逻辑[数据过滤器](/zh/pgedge/spock/managing/filtering/)。
* 把集群设置为[只读模式](/zh/pgedge/spock/managing/read-only/)；这会限制非超级用户只能执行只读操作，而超级用户仍可执行读和写操作。
* 使用[触发器](/zh/pgedge/spock/managing/repset-trigger/)管理复制集成员关系。
* 在分布式集群中使用 [Snowflake 序列](/zh/pgedge/spock/managing/snowflake/)管理序列。
* 使用 [Lolor 扩展](/zh/pgedge/spock/managing/lolor/)复制大对象。
* 启用[自动 DDL 复制](/zh/pgedge/spock/managing/spock-autoddl/)。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/index.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
