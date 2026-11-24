---
title: "spock.node_add_interface()"
description: "给已有的 Spock 节点添加网络接口定义。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_add_interface.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---




`spock.node_add_interface()`

## 概要 {#synopsis}

spock.node_add_interface (node_name name, interface_name name, dsn text)

## 返回值 {#returns}

新建接口的 OID。只要有一个参数为 `NULL`，就返回 `NULL`。

## 说明 {#description}

给已有的 Spock 节点添加网络接口定义。其他节点引用此接口时，会使用与它关联的连接字符串。

接口使同一节点可以通过多个连接端点访问。这常见于通过不同主机名、IP 地址、私有网络、公共网络或负载均衡器访问节点的环境。

接口定义由名称和 PostgreSQL DSN 连接字符串组成，后者说明其他节点如何连接到本节点。

此函数向 Spock 系统目录写入元数据，不修改 PostgreSQL 服务器配置或网络设置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`node_name`**

已有 Spock 节点的名称。

**`interface_name`**

该接口在节点内的唯一名称。

**`dsn`**

其他节点连接到本节点时使用的 PostgreSQL 连接字符串。字符串中的用户名应与操作系统用户名相同。外部节点应能按该字符串建立连接，且它应与稍后创建订阅时使用的连接字符串一致。例如 `host=10.1.2.5 port=5432 user=rocky`。

## 示例 {#example}

以下示例添加名为 `private_net` 的接口，连接字符串由最后一个参数指定，即 `'host=10.0.0.10 port=5432 dbname=postgres'`。

    postgres=# SELECT spock.node_add_interface('n1', 'private_net',
        'host=10.0.0.10 port=5432 dbname=postgres');

    node_add_interface
        --------------------
                 1239112588
        (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_add_interface.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
