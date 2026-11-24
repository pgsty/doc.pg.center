---
title: "spock.node_refresh_info()"
description: "直接从已知的对等节点重新读取其 location、country 和 info（包括 info 中的 tiebreaker 键），并覆盖本节点缓存的副本。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_refresh_info.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_refresh_info()

## 概要 {#synopsis}

spock.node_refresh_info (p_node_name name DEFAULT NULL)

## 返回值 {#returns}

刷新成功时返回 `true`。不传参数时，所有尝试的刷新都成功才返回 `true`，只要有一个节点未刷新成功就返回 `false`。显式指定 `node_name` 时，如果节点不存在、指定的是本地节点，或刷新该节点失败，则报错。失败原因包括接口不可达或配置有误、DSN 实际连接到另一节点，以及远程读取时遇到的其他错误。

## 说明 {#description}

直接从已知的对等节点重新读取其 `location`、`country` 和 `info`（包括 `info` 中的 `tiebreaker` 键），并覆盖本节点缓存的副本。

`spock.node` 是本地系统目录。在创建对等节点或首次为其创建订阅时，每个节点都会为该对等节点填入一条记录。以后若对方修改 `location`、`country` 或 `info`（最常见的是设置自定义 `tiebreaker` 来解决裁决值相同的冲突），变更会自动传播给*直接订阅*它的每个节点，无须调用本函数，详见[自动传播节点元数据](/zh/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)。消息不会继续转发。通常，只有直接订阅对方的节点才有它的记录，因此未订阅该对等节点的级联节点没有可刷新的记录。如果节点漏掉更新（例如承载更新的事务被跳过或丢弃），或需要主动重新获取特定对等节点的信息，可以调用本函数。若提供方的记录与缓存不一致，`spock.sub_resync_table()` 会发出警告。有关这种差异的影响，以及不整表复制 `spock.node` 的原因，见[冲突处理](/zh/pgedge/spock/conflicts/)的 Tiebreaker 一节。

指定 `node_name` 时只刷新该节点的记录，任何失败均报错。不传参数时，函数会尽量刷新本地节点以外的所有已知节点。任一节点刷新失败都会记录 `WARNING`，其余节点继续刷新。只要有一处失败，最终就返回 `false`。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`p_node_name`**

可选。要刷新的单个对等节点名称。省略或传入 NULL 时，刷新本地节点以外的所有节点。

## 示例 {#example}

以下示例在 `n1` 上设置自定义冲突裁决值，以消除裁决值相同的冲突。

    n1=# UPDATE spock.node SET info = COALESCE(info, '{}'::jsonb) ||
           '{"tiebreaker": 42}' WHERE node_name = 'n1';

在其他各节点上刷新这条记录。

    n2=# SELECT spock.node_refresh_info('n1');
     node_refresh_info
    --------------------
     t
    (1 row)

也可以一次刷新本节点已知的所有对等节点。

    n3=# SELECT spock.node_refresh_info();
     node_refresh_info
    --------------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_refresh_info.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
