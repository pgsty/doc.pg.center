---
title: "spock.node_create()"
description: "新建 Spock 节点定义。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_create.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_create()

## 概要 {#synopsis}

spock.node_create (node_name name, dsn text, location text,
country text, info jsonb)

## 返回值 {#returns}

新建 Spock 节点的 OID。

## 说明 {#description}

新建 Spock 节点定义。

节点表示参与 Spock 复制的一个 PostgreSQL 实例。节点定义包含其他节点与本节点通信所需的连接信息。

可以提供位置、国家和其他信息等可选元数据，以便对节点进行组织和管理。这些值存储在 Spock 系统目录中，复制本身无需这些字段。

此函数向 Spock 系统目录写入元数据，不修改 Postgres 服务器配置或网络设置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`node_name`**

Spock 节点的唯一名称。

**`dsn`**

其他节点连接到本节点时使用的 PostgreSQL 连接字符串。

**`location`**

可选的说明文字，指明节点的物理或逻辑位置。默认值为 `NULL`。

**`country`**

可选，节点关联的国家代码或名称。默认值为 `NULL`。

**`info`**

可选的 JSONB 字段，用于存储节点的任意元数据。默认值为 `NULL`。

此字段中的 `tiebreaker` 键可覆盖节点在“最后更新者胜出”规则下使用的默认冲突裁决值，默认值为节点的唯一 ID。每个节点初次获知该节点时，会将此值缓存在本地。之后通过推荐的 `spock.node_alter` 或直接 `UPDATE` 修改时，变更会自动传播到所有直接订阅方。遗漏变更的节点可以调用 `spock.node_refresh_info` 更新。详见 conflict_types.md 的 Tiebreaker 一节。

## 示例 {#example}

以下示例创建名为 `n3` 的 Spock 节点，并指定到 `inventory` 数据库的连接。

    inventory=# SELECT spock.node_create('n3','host=10.0.0.12 port=5432 dbname=inventory');
     node_create
    -------------
            9057
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_create.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
