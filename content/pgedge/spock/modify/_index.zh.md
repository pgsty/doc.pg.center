---
title: "为复制集群添加节点"
description: "按停机要求选择 Z0DAN 或 pgBackRest。"
weight: 70
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/index.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: "调整集群"
icon: fa-solid fa-book-open
type: docs
translation_status: translated
translation_notice: en
---

根据集群的用途、当前状态和可接受的停机时间选择添加节点的方法。

* **使用 Z0DAN，可在不停机的情况下添加或移除节点。**

[Z0DAN](/zh/pgedge/spock/modify/zodan/) 是 Spock 提供的一组脚本，在集群继续提供服务期间处理节点的加入和移除。

* **使用 pgBackRest，只需短暂停机即可向复制集群添加节点。**

[pgBackRest](/zh/pgedge/spock/modify/add-node-pgbackrest/) 是开源备份工具，可用来添加节点，并尽量缩短服务中断时间。

- [使用 pgBackRest 添加节点](/zh/pgedge/spock/modify/add-node-pgbackrest/)
- [教程：使用 pg_upgrade 原地升级 PostgreSQL 版本](/zh/pgedge/spock/modify/pg-upgrade-rolling-tutorial/)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/index.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/).
