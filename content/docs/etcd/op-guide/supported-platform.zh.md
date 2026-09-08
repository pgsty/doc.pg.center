---
title: 支持的平台
weight: 4800
description: etcd 支持常见架构与操作系统
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/supported-platform.md"
aliases: [/etcd/op-guide/supported-platform/]
---

## 支持层级 {#support-tiers}

etcd 可在不同平台上运行，但其提供的保证取决于平台的支持级别：

- **Tier 1**：由 [etcd 维护者][] 完全支持；etcd 保证通过所有测试，包括功能测试和健壮性测试。
- **Tier 2**：etcd 保证通过集成测试和端到端测试，但不保证通过功能测试或健壮性测试。
- **Tier 3**：etcd 保证可构建，可能仅进行轻度测试（或未测试），因此应视为 _不稳定_。

## 当前支持 {#current-support}

下表列出了当前支持的平台及其对应的 etcd 支持级别：

| 架构 | 操作系统 | 支持层级 | 维护者 |
|:------------:|:----------------:|:------------:|:--------------------:|
| AMD64        | Linux            |      1       | [etcd maintainers][] |
| ARM64        | Linux            |      1       | [etcd maintainers][] |
| AMD64        | Darwin           |      3       |                      |
| ARM64        | Darwin           |      3       |                      |
| AMD64        | Windows          |      3       |                      |
| ppc64le      | Linux            |      3       |                      |
| s390x        | Linux            |      3       |                      |

未列出的平台不受支持。

## 支持新平台 {#supporting-a-new-platform}

希望作为新平台的“官方”维护者参与 etcd 贡献？除承诺支持该平台外，还必须设置 etcd 持续集成（CI），满足以下要求，具体取决于支持层级：

| etcd 持续集成 | Tier 1 | Tier 2 | Tier 3 |
|---------------|:------:|:------:|:------:|
| 构建通过      | &check; | &check; | &check; |
| 单元测试通过  | &check; | &check; |        |
| 集成与端到端测试通过 | &check; | &check; |        |
| 健壮性测试通过 | &check; |        |        |

有关为 ARM64 设置二级 CI 的示例，请参见 [etcd PR #12928][]。

## 不支持的平台 {#unsupported-platforms}

为避免意外在不支持的平台上运行 etcd 服务器，除非环境变量 `ETCD_UNSUPPORTED_ARCH` 被设置为目标架构，否则 etcd 会打印警告信息并立即退出。

> [!WARNING]
> **32 位系统**
>   由于 Go 运行时存在缺陷，etcd 在 32 位系统上存在**已知问题**。
>   详细信息请参见 [Go 问题 #599][go-issue] 以及 [atomic 包缺陷说明][go-atomic]。
>
>   [go-atomic]: https://golang.org/pkg/sync/atomic/#pkg-note-BUG
>   [go-issue]: https://github.com/golang/go/issues/599

[etcd maintainers]: https://github.com/etcd-io/etcd/blob/main/OWNERS
[etcd PR #12928]: https://github.com/etcd-io/etcd/pull/12928
