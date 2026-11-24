---
title: "spock.node_drop()"
description: "从集群元数据中移除已有的 Spock 节点。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_drop.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_drop()

## 概要 {#synopsis}

spock.node_drop(node_name name, ifexists boolean)

## 返回值 {#returns}

  - 成功删除节点时返回 true。

  - 如果节点不存在且 ifexists 为 true，则返回 false。

  - 如果参数无效、调用者权限不足，或现有依赖关系阻止删除节点，则报 ERROR。

## 说明 {#description}

从集群元数据中移除已有的 Spock 节点。

函数会从 Spock 系统目录中删除节点定义及其所有关联元数据。它只移除 Spock 对节点的逻辑表示，不删除 PostgreSQL 数据目录，也不停止 PostgreSQL 服务器。

如果 ifexists 为 false（默认值），指定的节点不存在时会报错。如果 ifexists 为 true，函数在这种情况下返回 false。

此命令必须由超级用户执行，并会修改 Spock 系统目录表。

## 参数 {#arguments}

**`node_name`**

要删除的已有 Spock 节点的名称。

**`ifexists`**

设为 true 时，节点不存在就返回 false，不抛出错误。默认为 false。

## 示例 {#example}

以下函数调用删除名为 `'n3'` 的节点。

    inventory=# SELECT spock.node_drop('n3');
     node_drop
    -----------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_drop.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
