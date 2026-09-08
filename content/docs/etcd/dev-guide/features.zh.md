---
title: etcd 功能
weight: 3750
description: 使用 etcd 功能
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/features.md"
aliases: [/etcd/dev-guide/features/]
---

本文概述了 etcd 的各项功能，旨在帮助用户更好地理解这些功能及其相关弃用流程。若想了解 etcd 功能的开发方式，请参阅 [开发指南](https://github.com/etcd-io/etcd/blob/main/Documentation/contributor-guide/features.md)。

etcd 功能分为三个阶段：实验性、稳定和不安全。可通过运行 `etcd --help` 获取功能列表。

## 实验性 {#experimental}

为获取早期反馈，任何新功能通常以实验性功能的形式添加。可通过标志名称识别实验性功能，其名称应以 `--experimental` 为前缀。使用实验性功能时，请注意以下事项：
- 由于缺乏用户测试，该功能可能存在缺陷。启用该功能可能无法按预期工作。
- 默认情况下处于禁用状态。
- 项目团队可能随时停止支持该功能，恕不另行通知。
    - 若该功能未晋升为稳定功能，则可在下一个次要版本或主要版本中直接移除，无需遵循[功能弃用](#feature-deprecation)政策。
    - 项目团队欢迎用户报告与实验性功能相关的问题。但此类问题的优先级可能低于与稳定功能相关的问题。
- 实验性功能[晋升为稳定功能](#feature-deprecation)时，其实验性功能标志将被弃用。应尽快改用稳定功能标志。

## 稳定 {#stable}

这是 etcd 中功能最常见的阶段。稳定功能具有以下特征：
- 作为 etcd 支持版本的一部分提供支持。
- 可以默认启用。
- 停止支持必须遵循[功能弃用](#feature-deprecation)政策。

## 不安全 {#unsafe}

不安全功能较为罕见，列于 etcd 使用文档的 `Unsafe feature:` 章节中。默认情况下，这些功能处于禁用状态。使用时应谨慎，并遵循文档说明。不安全功能可能在下一个次要版本或主要版本中被移除，且无需遵循功能弃用策略。

## 功能弃用 {#feature-deprecation}

### 实验性 {#experimental-1}
当实验性功能进入稳定阶段时，即被弃用。
- 实验性功能的文档将显示弃用提示，并建议使用相关的稳定功能标志。例如 `DEPRECATED. Use <feature-name> instead.`
- 已弃用的功能将在后续版本中移除。

### 稳定 {#stable-1}
随着项目演进，某些稳定功能有时可能需要被弃用并移除。当发生这种情况时：

- 功能文档将在计划发布前显示警告消息。例如 `To be deprecated in <release>.`。若已有新功能计划替代 `To be deprecated` 功能，则文档还将提供相应说明。例如 `Use <feature-name> instead.`。
- 该功能将在计划发布中被弃用。此时，功能文档将显示弃用消息，并建议使用相关稳定功能。例如 `DEPRECATED. Use <feature-name> instead.`。
- 已弃用的功能将在后续发布中移除。
