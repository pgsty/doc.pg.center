---
title: "使用 pgBackRest 添加节点"
description: "用 pgBackRest 备份初始化新节点，再通过 Spock 扩展将它加入集群。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/add_node_pgbackrest.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



可以用 pgBackRest 备份初始化新节点，再通过 Spock 扩展将它加入集群。下面以已有的三个节点（`n1`、`n2`、`n3`）为例，说明添加第四个节点 `n4` 的主要步骤。

1. 创建 [pgBackRest stanza](https://pgbackrest.org/user-guide.html#quickstart/create-stanza)。stanza 定义了备份和恢复所需的集群配置，这是必需步骤。

2. 对主节点 `n1` 执行全量备份。备份可以存放在 S3 存储桶、网络共享目录，或本地目录（所有节点位于同一台机器时）。

3. 将 `n1` 的备份[恢复](https://pgbackrest.org/user-guide.html#restore) 到 `n4` 的数据目录，为后续将 `n4` 配置为 `n1` 的副本做好准备。

4. 在 `n4` 配置流复制，作为 `n1` 的副本。让 `n4` 追上 `n1` 自备份以来的全部事务，直至 `n4` 与 `n1` 完全同步。

5. 用 `ALTER` 将 `n1`、`n2` 和 `n3` 设为只读，并在这些节点上重新加载配置。`n4` 从 `n1` 复制来的配置有些不适用于 `n4`。临时切换只读模式，可防止配置变更期间出现新事务。

6. 终止 `n1`、`n2` 和 `n3` 上仍在运行的事务，防止长查询干扰配置变更。

7. 编辑 `n4` 的 `shared_preload_libraries`，移除 `spock`，防止 Spock 在 `n4` 上启用从 `n1` 继承的旧配置。

8. 启动 `n4`，让它作为 `n1` 的副本运行，以确保 `n4` 收到 `n1` 的全部事务。

9. 将 `n4` 提升为主节点，或将它配置为禁用 Spock 的独立节点。这一步确定 `n4` 在新配置中的主节点角色。

10. 清除配置中的所有复制集和节点，移除不再需要的旧复制定义。

11. 将 `spock` 重新加入 `n4` 的 `shared_preload_libraries`，为 `n4` 按新角色参与复制做好准备。

12. 重启 `n4`，使此前的更改生效。

13. 将 `n4` 加入 `n1`、`n2`、`n3` 所在的复制集群。

14. 解除 `n1`、`n2` 和 `n3` 的只读模式，恢复正常操作。

15. 在新节点 `n4` 和原有三个节点（`n1`、`n2`、`n3`）之间添加以下订阅。

    - 订阅 `subn1n4` 用于同步 n1 与 n4。
    - 订阅 `subn2n4` 用于同步 n2 与 n4。
    - 订阅 `subn3n4` 用于同步 n3 与 n4。
    - 订阅 `subn4n1` 用于同步 n4 与 n1。
    - 订阅 `subn4n2` 用于同步 n4 与 n2。
    - 订阅 `subn4n3` 用于同步 n4 与 n3。

16. 检查集群内所有节点（`n1`、`n2`、`n3`、`n4`）的状态，确认配置正确、数据已同步，且复制运行正常。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/add_node_pgbackrest.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
