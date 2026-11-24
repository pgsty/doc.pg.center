---
title: "使用 Z0DAN 调整集群"
description: "使用 Z0DAN 在不停机的情况下添加或移除 Spock 节点。"
weight: 20
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/index.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
linkTitle: "Z0DAN"
icon: fa-solid fa-book-open
type: docs
translation_status: translated
translation_notice: en
---

Z0DAN 用于在线添加和移除节点。脚本位于 [Spock 仓库](https://github.com/pgEdge/spock)的 [samples/Z0DAN 目录](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN)。

添加节点时，Z0DAN 会创建节点及双向订阅，创建复制槽，同步数据，推进复制槽的位置，最后启用订阅。

Z0DAN 既可移除运行正常的节点，也可移除故障节点。数据库、数据目录和日志文件等 PostgreSQL 资源会保留在原主机上。

> [!NOTE]
> 添加节点失败后，可用 Z0DAN 移除尚未添加完成的节点。在同一主机再次部署之前，可能还需清理遗留资源。

> [!NOTE]
> 每个脚本都必须在要添加或移除的目标节点上运行。

## Z0DAN 与手动添加节点的区别 {#key-differences-between-using-zodan-and-the-manual-process}

添加节点时，Z0DAN 会完成以下工作。

- 保存同步位置（LSN）。即使两个步骤之间相隔数小时，订阅也能从正确的位置启动。
- 检测新节点上已有的模式，并填入 `skip_schema`，避免同步结构时产生冲突。
- 启动前检查 Spock 版本。所有节点都须使用 5.0.9 或更高版本。新节点的主、次版本组合须不低于每个已有节点，补丁版本可以不同。因此 6.0.x 节点可以加入 5.0.x 集群。此后再添加 6.0.x 节点时，可以选择混合集群中的任何节点作为数据源。如果新节点的主、次版本低于任何已有节点，则拒绝添加。
- 启用订阅后，调用 `verify_subscription_replicating()` 确认订阅已进入复制状态。
- 向单节点集群添加节点时采用单独的流程，无需预先创建已禁用的订阅。
- 列出整个集群中所有节点和订阅的最终状态。

延伸阅读：

- [Z0DAN 使用说明](/zh/pgedge/spock/modify/zodan/zodan-readme/)
- [在线添加节点教程](/zh/pgedge/spock/modify/zodan/zodan-tutorial/)
- [Z0DAN 脚本与工作流程](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN)
- [Spock 上游文档](https://docs.pgedge.com/spock-v5/)
- [使用 Z0DAN 滚动升级 PostgreSQL](/zh/pgedge/spock/modify/zodan/zodan-rolling-pg-version-tutorial/)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/index.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/).
