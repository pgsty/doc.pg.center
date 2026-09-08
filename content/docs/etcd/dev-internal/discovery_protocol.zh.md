---
title: 发现服务协议
weight: 1500
description: 在集群引导阶段发现集群其他成员
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
aliases: [/etcd/dev-internal/discovery_protocol/]
---

发现服务协议有助于新 etcd 成员在集群引导阶段，通过共享的发现令牌和端点列表，发现集群中的所有其他成员。

发现服务协议仅在集群引导阶段使用，不可用于运行时重配置或集群监控。

该协议使用新的发现令牌来引导一个唯一的 etcd 集群。请注意，一个发现令牌只能代表一个 etcd 集群。只要该令牌的发现协议已启动，即使中途失败，也不得用于引导另一个 etcd 集群。

本文其余部分将通过示例介绍发现过程，这些示例对应自托管发现集群。

请注意，本文仅适用于 v3 发现机制。有关 [v2 发现][v2-discovery] 的更多详情，请参阅前文文档。

## 协议工作流 {#protocol-workflow}

发现协议的核心思想是利用一个内部 etcd 集群来协调新集群的引导过程。首先，所有新成员与发现服务交互，协助生成预期的成员列表。随后，每个新成员使用该列表引导其服务器，这一操作实现的功能与 -initial-cluster 标志相同。

在以下示例工作流程中，我们将使用 `etcdctl` 命令列出协议的每一步，以便于理解，并假设 `http://example.com:2379` 主机提供 etcd 集群作为发现服务。

按照惯例，etcd 发现协议使用键前缀 `/_etcd/registry`。


### 创建新的发现令牌 {#creating-a-new-discovery-token}

生成一个唯一令牌，用于标识新集群。该令牌将在后续步骤中作为发现键空间的唯一前缀使用。一种简便的方法是使用 `uuidgen`：

```
UUID=$(uuidgen)
```

### 指定预期集群规模 {#specifying-the-expected-cluster-size}

发现令牌需要指定集群大小，该大小必须明确提供。发现服务使用此大小来判断是否已找到将初始组成集群的所有成员。

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

通常，集群大小为 3、5 或 7。请参阅 [optimal cluster size][cluster-size] 以获取更多详细信息。

### 启动 etcd 进程 {#bringing-up-etcd-processes}

将发现令牌 `${UUID}` 设置为 `--discovery-token` 标志，并将支持发现服务的 etcd 集群端点设置为 `--discovery-endpoints` 标志。这将启用 v3 发现以引导 etcd 集群。

如果给定 `--discovery-token` 和 `--discovery-endpoints` 标志，每个 etcd 进程将内部遵循以下步骤。

如果发现服务启用了客户端证书身份认证，请配置以下标志。其使用方式与使用 `etcdctl` 与 etcd 集群通信完全相同。
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

如果发现服务启用了基于角色的身份认证，请配置以下标志。其使用方式与使用 `etcdctl` 与 etcd 集群通信完全相同。
```
--discovery-user
--discovery-password
```

默认的超时时间值也可通过以下标志进行修改，其使用方式与使用 `etcdctl` 与 etcd 集群通信时完全相同。
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### 自我注册 {#registering-itself}

每个 etcd 进程首先会将自身注册为指定新集群中的成员。这是通过在完整注册键中创建成员 ID 作为键来实现的。

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### 检查状态 {#checking-the-status}

它检查预期的集群大小和注册状态，并决定下一步操作。

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

如果已注册的成员仍不足，系统将等待其他成员出现。

如果注册的成员数量大于预期的集群大小 N，则将前 N 个注册的成员视为集群的成员列表。如果该成员自身位于成员列表中，发现过程成功，并通过成员列表获取所有对等成员。如果不在成员列表中，发现过程将以集群已满的失败结果结束。

成员可在注册自身之前检查集群状态。因此，如果集群已满，成员可能迅速失败。

### 等待所有成员就位 {#waiting-for-all-members}

等待过程将持续监听键前缀 `/_etcd/registry/${UUID}/members`，直至发现所有成员。

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
