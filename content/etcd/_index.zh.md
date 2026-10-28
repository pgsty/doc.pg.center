---
title: "etcd 3.7 中文文档"
linkTitle: "etcd 3.7"
description: "etcd 3.7 开发、运维、升级、API 与内部原理中文指南"
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [概念]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcd 是一个强一致的分布式键值存储。本套指南涵盖 etcd 3.7 系列的安装与运行、API 应用开发、设计原理、性能衡量，以及集群升级与降级。

从 [快速入门](/zh/etcd/quickstart/) 开始，部署本地单成员集群；通过 [安装](/zh/etcd/install/) 了解受支持的安装路径；或参考 [操作指南](/zh/etcd/op-guide/) 进行生产环境部署。

## etcd v3.7.3 {#etcd-v3-7-3}

当前维护版本为 [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3)。本版文档的安装、Docker 和 Kubernetes 示例均以此版本为目标。

- 修复 MVCC 存储中 `Hash` 与 `Restore` 之间的数据竞争、仅返回键的 `RangeStream` 操作中的数据竞争，以及 leader 逆序发送 `MsgApp` 消息造成的复制性能回退。
- 使用 Go 1.26.10 构建，并更新 OpenTelemetry 和 `golang.org/x/net` 依赖，修复已报告的安全问题。
- 弃用 `client/pkg/v3/logutil` 中的 `NewJournalWriter`，计划在 v3.8 中移除。

完整变更请参阅[上游更新日志](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22)。
