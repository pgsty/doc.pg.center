---
title: "spock.node_drop_interface()"
description: "从 Spock 节点移除已有的网络接口定义。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_drop_interface.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_drop_interface()

## 概要 {#synopsis}

spock.node_drop_interface (node_name name, interface_name name)

## 返回值 {#returns}

  - 成功删除接口时返回 true。

  - 如果接口不存在、参数无效、权限不足或无法删除接口，则抛出 ERROR。

## 说明 {#description}

从 Spock 节点移除已有的网络接口定义。

函数会从 Spock 系统目录删除接口定义。它只移除 Spock 对该接口的逻辑表示，不改动 PostgreSQL 服务器配置或网络设置。

原先使用此接口连接的其他节点将无法再使用它。删除前请确认没有活动订阅依赖该接口，以免客户端报错。

此函数向 Spock 系统目录写入元数据，不修改 PostgreSQL 服务器配置或网络设置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`node_name`**

已有 Spock 节点的名称。

**`interface_name`**

要从节点移除的接口名称。

## 示例 {#example}

以下示例删除名为 `'private_net'` 的接口。

    inventory=# SELECT spock.node_drop_interface('n3', 'private_net');
     node_drop_interface
    ---------------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_drop_interface.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
