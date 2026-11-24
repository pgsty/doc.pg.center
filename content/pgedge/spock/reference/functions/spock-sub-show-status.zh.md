---
title: "spock.sub_show_status"
description: "spock.sub_show_status() 显示当前节点上 Spock 订阅的详细运行信息。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_status.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_show_status()` 显示订阅的状态和基本信息。

## 概要 {#synopsis}

```sql
spock.sub_show_status(subscription_name name DEFAULT NULL)
```

## 返回值 {#returns}

返回描述一个或多个订阅当前状态的多行记录。每行包含以下信息。

- 订阅名称。
- 当前复制状态。
- 提供方节点名称。
- 用于连接提供方的连接字符串。
- 订阅使用的逻辑复制槽名称。
- 与订阅关联的复制集。
- 此订阅转发的复制来源。

## 状态值 {#status-values}

下表列出 `status` 列可能出现的值及其含义。

| 状态 | 含义 |
|---|---|
| `replicating` | 应用进程正在运行，初始同步已完成，正在正常应用提供方的变更。 |
| `initializing` | 应用进程正在运行，但初始同步尚未结束，仍在从提供方复制表数据。 |
| `disabled` | 该订阅已通过 `spock.sub_disable()` 显式禁用，应用进程未运行。 |
| `down` | 订阅已启用，但应用进程未运行。进程可能尚未启动，也可能异常退出。 |
| `unknown` | 应用进程正在运行，但找不到同步状态记录。此状态通常很快就会消失。 |
{.wide .expand}

## 说明 {#description}

`spock.sub_show_status()` 显示当前节点上 Spock 订阅的详细运行信息。

提供具体订阅名称时，只显示该订阅。传入 `NULL`（默认值）时返回本节点上所有订阅的状态。

此函数可用于监控复制运行状况、验证配置，以及确认当前使用的复制集和复制来源。信息取自 Spock 系统目录元数据和逻辑复制进程的当前状态。

此函数不修改任何配置。

## 参数 {#arguments}

- `subscription_name`：可选，已有订阅的名称。省略时显示本地节点上所有订阅的状态。

## 示例 {#example}

如需查看所有订阅的状态，可执行以下命令。

```sql
SELECT * FROM spock.sub_show_status();
```

以下示例使用 `spock.sub_show_status()` 显示订阅 `sub_n1_n2` 的状态。

```sql
SELECT * FROM spock.sub_show_status('sub_n1_n2');
-[ RECORD 1 ]-----+--------------------------------------------------------------------
subscription_name | sub_n1_n2
status            | replicating
provider_node     | n2
provider_dsn      | host=192.168.105.11 dbname=postgres user=postgres password=<redacted>
slot_name         | spk_postgres_n2_sub_n1
replication_sets  | {default,default_insert_only,ddl_sql,audit_only}
forward_origins   |
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_show_status.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
