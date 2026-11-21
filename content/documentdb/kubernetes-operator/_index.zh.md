---
title: Kubernetes Operator
description: 使用 DocumentDB Kubernetes Operator在 Kubernetes 上运行 DocumentDB。了解何时选择它、你的集群需要什么，以及如何找到Operator的文档。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/kubernetes-operator/index.md
weight: 60
translation_source_sha256: 4f9b3e6e12013a4fdc6fe8435460d8bf47477f1b045e1e212cffef8b43d3c776
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

[DocumentDB Kubernetes Operator](https://github.com/documentdb/documentdb-kubernetes-operator) 负责在 Kubernetes 上运行和管理 DocumentDB 集群。你通过 `DocumentDB` 资源描述集群，Operator 则负责创建集群，并处理高可用、故障切换、备份和升级；PostgreSQL 层以 [CloudNativePG](https://cloudnative-pg.io/docs/) 为基础。每个实例都将 PostgreSQL 容器与一个 DocumentDB 网关 sidecar 配对运行，因此应用可以像连接其他 DocumentDB 部署一样，直接使用兼容 MongoDB 的驱动连接。

Operator 是独立项目，有自己的代码仓库、发布节奏和文档。本页介绍适用场景与集群前提条件，其余内容请参阅 Operator 自身的文档。

## 版本 {#versions}

Operator **1.1.1** 运行 DocumentDB 引擎 **1.0-0**。请固定 Helm Chart 版本，以便重复安装时得到一致结果（必须先安装 cert-manager，参见下方快速入门）：

```bash
helm install documentdb-operator oci://ghcr.io/documentdb/documentdb-operator \
  --version 1.1.1 \
  --namespace documentdb-operator \
  --create-namespace \
  --wait
```

## 何时使用它 {#when-to-use-it}

| 方案 | 适用场景 |
|---|---|
| [DocumentDB Local](/documentdb/documentdb-local/) | 单容器运行，适合开发、原型验证和集成测试。 |
| [预编译软件包](/documentdb/getting-started/prebuilt-packages/) | 将 DocumentDB 添加到已经运行并自行维护的 PostgreSQL 服务器中。 |
| Kubernetes Operator | 将 DocumentDB 部署为有副本的服务，提供自动故障切换、滚动升级、备份恢复和多区域部署。 |

## 集群前提条件 {#what-your-cluster-needs}

Operator 要求 Kubernetes 1.32 或更高版本。规划部署前，还应确认 DocumentDB 扩展如何进入 PostgreSQL Pod。默认情况下，集群支持时，Operator 通过 Kubernetes 的 [ImageVolume](https://kubernetes.io/docs/concepts/storage/volumes/#image) 功能挂载扩展：

- **Kubernetes 1.35 或更新版本。** ImageVolume 自 1.36 起正式可用（GA）。在 1.35 中，它处于 Beta 阶段且默认开启，需确认集群没有关闭 `ImageVolume` 特性门控。1.33 和 1.34 默认关闭该功能，必须同时在 API 服务器和 kubelet 上开启门控才能使用。
- 容器运行时使用 **containerd 2.1 或更高版本，或 CRI-O 1.33 或更高版本**。Docker 运行时不支持 ImageVolume。

否则，Operator 使用同时包含 PostgreSQL 18 和该扩展的组合镜像。它在创建 `DocumentDB` 集群时决定采用哪种布局，之后集群保持该布局。各托管 Kubernetes 服务提供的版本和运行时不同，本地工具通常也需要显式指定选项才能使用受支持的运行时，因此若要使用 ImageVolume，请提前确认这两点。[开始之前](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/getting-started/before-you-start/)列出了完整的前提条件，包括支持的工具版本和资源规模。

## Operator 文档 {#operator-documentation}

Operator 文档按版本维护，随各发布版一同发布：

- [概述](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/) — Operator 安装的内容以及各组件如何协同工作
- [快速入门：Kind](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/getting-started/quickstart-kind/) 和 [快速入门：K3s](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/getting-started/quickstart-k3s/) — 在本地部署集群
- [连接 DocumentDB](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/getting-started/connecting-to-documentdb/) — `mongosh` 和 Python、Node.js、Go 与 Java 的驱动程序示例
- [架构概述](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/architecture/overview/) — Operator、CloudNativePG 与网关之间的交互方式
- 配置：[网络](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/configuration/networking/)、[存储](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/configuration/storage/) 和 [TLS](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/configuration/tls/)
- [高可用性](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/high-availability/overview/) — 副本、故障切换行为与恢复目标
- 运维：[备份与恢复](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/operations/backup-and-restore/) 和 [升级](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/operations/upgrades/)
- [监控](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/monitoring/overview/) 与 [kubectl 插件](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/kubectl-plugin/)
- [API 参考](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/api-reference/) — `DocumentDB`、`Backup` 和 `ScheduledBackup` 资源
- [常见问题](https://documentdb.io/documentdb-kubernetes-operator/latest/preview/faq/)

Operator 的问题请提交到 [Operator 仓库](https://github.com/documentdb/documentdb-kubernetes-operator/issues)，而不是本仓库。
