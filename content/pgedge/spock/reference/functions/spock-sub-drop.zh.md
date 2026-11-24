---
title: "spock.sub_drop()"
description: "断开订阅连接，并从集群中移除该订阅。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_drop.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.sub_drop()

## 概要 {#synopsis}

spock.sub_drop (subscription_name name, ifexists boolean)

## 返回值 {#returns}

已删除订阅的 OID。

## 说明 {#description}

断开订阅连接，并从集群中移除该订阅。

函数终止指定订阅的复制连接，并从 Spock 系统目录删除其全部关联元数据。已复制到订阅方的数据不受影响。

如果 ifexists 为 false（默认值），指定的订阅不存在时会报错。如果 ifexists 为 true，函数在这种情况下正常返回。

只要任一参数为 NULL，就返回 NULL。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`subscription_name`**

要移除的已有订阅的名称。

**`ifexists`**

设为 true 时，如果订阅不存在也不报错。默认为 false。

## 示例 {#example}

    SELECT spock.sub_drop('sub_n2_n1');

    SELECT spock.sub_drop('sub_n2_n1', true);

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_drop.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
