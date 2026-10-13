---
title: 发现服务协议
weight: 1500
description: 在集群引导阶段发现集群其他成员
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/discovery_protocol.md"
aliases: [/etcd/dev-guide/discovery_protocol/]
---

> [!NOTE]
> 本页介绍的是旧的 v2 发现协议，该协议已在 etcd 3.7 中移除。对于新的 v3.7 部署，请使用 [v3 发现协议](/zh/docs/etcd/dev-internal/discovery_protocol/)。

发现服务协议有助于新 etcd 成员在集群引导阶段通过共享的发现 URL 发现集群中的所有其他成员。

发现服务协议仅在集群引导阶段使用，不可用于运行时重配置或集群监控。

该协议使用新的发现令牌来引导一个唯一的 etcd 集群。请注意，一个发现令牌只能代表一个 etcd 集群。只要该令牌的发现协议已启动，即使中途失败，也不得用于引导另一个 etcd 集群。

本文其余部分将通过示例介绍发现过程，这些示例对应自托管发现集群。公共发现服务 discovery.etcd.io 的工作方式相同，但增加了一层优化，用于抽象掉难看的 URL，自动生成 UUID，并对过多请求提供一定防护。其核心仍使用 etcd 集群作为数据存储系统，如本文所述。

## 协议工作流 {#protocol-workflow}

发现协议的核心思想是利用一个内部 etcd 集群来协调新集群的引导过程。首先，所有新成员与发现服务交互，协助生成预期的成员列表。随后，每个新成员使用该列表引导其服务器，这一操作实现的功能与 -initial-cluster 标志相同。

在以下示例工作流程中，我们将以 curl 格式列出协议的每一步，以便于理解。

按照惯例，etcd 发现协议使用键前缀 `_etcd/registry`。若 `http://example.com` 托管用于发现服务的 etcd 集群，则发现键空间的完整 URL 将为 `http://example.com/v2/keys/_etcd/registry`。本示例中将使用该 URL 前缀。

### 创建新的发现令牌 {#creating-a-new-discovery-token}

生成一个唯一令牌，用于标识新集群。该令牌将在后续步骤中作为发现键空间的唯一前缀使用。一种简便的方法是使用 `uuidgen`：

```
UUID=$(uuidgen)
```

### 指定预期集群规模 {#specifying-the-expected-cluster-size}

发现令牌需要指定集群大小，该大小必须明确提供。发现服务使用此大小来判断是否已找到将初始组成集群的所有成员。

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size -d value=${cluster_size}
```

通常，集群大小为 3、5 或 7。请参阅[最佳集群规模][cluster-size]以获取更多详细信息。

### 启动 etcd 进程 {#bringing-up-etcd-processes}

给定发现 URL 后，将其作为 `-discovery` 标志使用，并启动 etcd 进程。每个 etcd 进程在接收到 `-discovery` 标志时，将自动执行以下内部步骤。

### 自我注册 {#registering-itself}

etcd 进程的首要任务是将自身作为成员注册到发现 URL。具体做法是在发现 URL 下创建一个以成员 ID 为键的条目。

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/${member_id}?prevExist=false -d value="${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}"
```

### 检查状态 {#checking-the-status}

它检查发现 URL 中预期的集群大小和注册状态，并据此决定下一步操作。

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}
```

如果已注册的成员仍不足，将等待缺失的成员出现。

如果注册的成员数量大于预期的集群大小 N，则将前 N 个注册的成员视为集群的成员列表。如果该成员自身在成员列表中，发现过程成功，并通过成员列表获取所有对等成员。如果不在成员列表中，发现过程将以集群已满的失败状态结束。

在 etcd 实现中，成员可能在注册自身之前就检查集群状态。因此，如果集群已满，该成员可能会快速失败。

### 等待所有成员就位 {#waiting-for-all-members}

等待过程在 [etcd API 文档][api]中有详细描述。

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}?wait=true&waitIndex=${current_etcd_index}
```

它将持续等待，直到找到所有成员。

## 公共发现服务 {#public-discovery-service}

CoreOS Inc. 在 https://discovery.etcd.io/ 提供公开的发现服务，该服务具备多项便捷功能，便于使用。

### 隐藏键前缀 {#mask-key-prefix}

公共发现服务将 `https://discovery.etcd.io/${UUID}` 重定向至 `/v2/keys/_etcd/registry` 处的 etcd 集群。该服务可隐藏注册键前缀，使发现 URL 更短且更易读。

### 获取新令牌 {#get-new-token}

```
GET /new

Sent query:
	size=${cluster_size}
Possible status codes:
	200 OK
	400 Bad Request
200 Body:
	generated discovery url
```

服务中的生成过程遵循从 [创建新的发现令牌][new-discovery-token] 到 [指定预期集群大小][expected-cluster-size] 的步骤。

### 检查发现状态 {#check-discovery-status}

```
GET /${UUID}
```

可通过请求 UUID 的值来检查此发现令牌的状态，包括已注册的机器。

### 开源代码库 {#open-source-repository}

仓库位于 https://github.com/coreos/discovery.etcd.io，可用于构建自定义发现服务。

[api]: https://etcd.io/docs/v2.3/api#waiting-for-a-change
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
