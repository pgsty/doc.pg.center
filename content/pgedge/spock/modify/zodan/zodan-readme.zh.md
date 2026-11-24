---
title: "使用 Zodan 不停机增删 Spock 节点"
description: "Zodan 提供不停机添加或移除 Spock 节点的工具。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_readme.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



Zodan 提供不停机添加和移除节点的工具。相关脚本位于 [Spock 的 GitHub 仓库](https://github.com/pgEdge/spock) 中的 [samples/Z0DAN](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN) 目录。

Zodan 用以下脚本和工作流程简化 Spock 集群的节点增删操作。

- [zodan.sql](#using-the-zodansql-sql-workflow) 提供完整的 SQL 工作流程，使用 `dblink` 在 PostgreSQL 内完成添加节点的操作。
- [zodremove.sql](#the-zodremovesql-workflow) 提供完整的 SQL 工作流程，使用 `dblink` 在 PostgreSQL 内完成移除节点的操作。

## 组成部分 {#components}

Zodan 提供下列脚本和工作流程。

### 使用 zodan.sql 添加节点 {#using-the-zodansql-sql-workflow}

SQL 实现通过 PostgreSQL 的 `dblink` 扩展直接在数据库内添加节点，适用于无法使用 shell 或 Python 的环境。

工作流程中的 SQL 命令协调以下操作。

- `add_node` 是负责统筹完整流程的主过程。
- `create_node` 通过 `spock.node_create` 登记新节点。
- `get_spock_nodes` 从远端节点获取当前节点元数据。
- `create_sub` 和 `enable_sub` 负责创建并启用订阅。
- `create_replication_slot` 创建并配置逻辑复制槽。
- `sync_event` 和 `wait_for_sync_event` 协调数据同步事件。
- `get_commit_timestamp` 和 `advance_replication_slot` 对齐复制进度。

在 PostgreSQL 会话中执行下列命令即可运行该流程。示例通过 `spock.add_node` 过程向集群添加新节点。

```sql
CALL spock.add_node(
  'source_node_name',
  'src_dsn',
  'new_node_name',
  'new_node_dsn',
  true|false,               -- verbose? optional
  'new_node_location',      -- optional
  'new_node_country',       -- optional
  '{}'::jsonb               -- optional info
);
```

以下命令将节点 `n4` 加入集群。

```sql
CALL spock.add_node(
  'n1',
  'host=127.0.0.1 dbname=pgedge port=5431 user=pgedge password=<PASSWORD>',
  'n4',
  'host=127.0.0.1 dbname=pgedge port=5434 user=pgedge password=<PASSWORD>'
);
```

### 使用 zodremove.sql 移除节点 {#the-zodremovesql-workflow}

SQL 实现通过 PostgreSQL 的 `dblink` 扩展直接在数据库内移除节点，适用于无法使用 shell 或 Python 的环境。

工作流程中的 SQL 命令协调以下操作。

- `spock.remove_node` 是统筹完整流程的主过程。
- `spock.remove_node_subscriptions` 负责移除订阅。若未留下任何订阅，还会移除复制槽。
- `spock.remove_node_replication_sets` 移除待下线节点上已发布的复制集。
- `spock.remove_node_from_cluster_registry` 从集群中移除该节点。

工作流程位于 [Spock 的 GitHub 仓库](https://github.com/pgEdge/spock) 中的 [samples/Z0DAN](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN) 目录。

在 PostgreSQL 会话中调用相应命令即可。此例通过 Z0DAN 的 `spock.remove_node` 过程移除节点。`spock.remove_node` 是 `zodremove.sql` 提供的工具过程，Spock 扩展本身不内置这个函数。

```sql
CALL spock.remove_node(
  'target_node_name',
  'target_dsn',
  true                      -- verbose_mode, optional boolean
);
```

以下命令将节点 `n4` 从集群中移除。

```sql
CALL spock.remove_node(
  'n4',
  'host=127.0.0.1 dbname=pgedge port=5434 user=pgedge password=<PASSWORD>'
);
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_readme.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
