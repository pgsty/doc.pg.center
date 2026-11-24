---
title: "spock.node_info()"
description: "返回本地 Spock 节点的信息。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_info.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_info()

## 概要 {#synopsis}

spock.node_info()

## 返回值 {#returns}

包含本地 Spock 节点信息的一条记录，各字段如下。

  - node_id 是节点的 OID。
  - node_name 是节点名称。
  - sysid 是系统标识符。
  - dbname 是数据库名称。
  - replication_sets 列出可用的复制集。
  - location 是节点位置（若已设置）。
  - country 是节点所在国家（若已设置）。
  - info 是以 JSONB 格式存储的附加元数据（若已设置）。

## 说明 {#description}

返回本地 Spock 节点的信息。

函数查询 Spock 系统目录并返回当前节点的元数据，包括标识符、名称、数据库信息，以及创建节点时设置的可选描述字段。

此函数只执行查询，不修改数据。

## 参数 {#arguments}

此函数不接受参数。

## 示例 {#example}

    postgres=# SELECT * FROM spock.node_info();

    -[ RECORD 1 ]----+--------------------------------------
    node_id          | 49708
    node_name        | n1
    sysid            | 7600444661598442547
    dbname           | postgres
    replication_sets | "default",default_insert_only,ddl_sql
    location         |
    country          |
    info             | 

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_info.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
