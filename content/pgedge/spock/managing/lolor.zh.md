---
title: 使用 LOLOR 管理大对象
description: Spock 逻辑复制建议使用 LOLOR 扩展管理 PostgreSQL 大对象。
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/lolor.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



PostgreSQL 的逻辑解码机制不支持解码[大对象](https://www.postgresql.org/docs/current/largeobjects.html)的变更；我们建议改用 [LOLOR 扩展](https://github.com/pgEdge/lolor)管理大对象。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/lolor.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
