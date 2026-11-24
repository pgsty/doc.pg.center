---
title: "spock.sub_add_repset()"
description: "将复制集添加到已有订阅。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_add_repset.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.sub_add_repset()

## 概要 {#synopsis}

spock.sub_add_repset (subscription_name name, replication_set name)

## 返回值 {#returns}

  - 成功添加复制集时返回 true。

  - 如果订阅不存在、复制集已经加入该订阅、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

将复制集添加到已有订阅。

函数修改订阅，使其同时接收提供方节点上另一个复制集的变更。订阅会立即开始消费新加入复制集的事件。

此操作仅启用对该复制集后续事件的接收，不做数据同步。若需要同步复制集中已有的数据，必须另行处理。

此函数向 Spock 系统目录写入元数据。

只要任一参数为 NULL，就返回 NULL。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`subscription_name`**

已有订阅的名称。

**`replication_set`**

要添加到订阅的复制集名称。

## 示例 {#example}

以下示例将名为 audit_only 的复制集添加到名为 sub_n2_n1 的订阅。

    postgres=# SELECT spock.sub_add_repset('sub_n2_n1', 'audit_only');
    -[ RECORD 1 ]--+--
    sub_add_repset | t

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_add_repset.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
