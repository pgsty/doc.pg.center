---
title: etcd 客户端设计
weight: 2250
description: 客户端架构决策及其实现细节
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-client.md"
aliases: [/etcd/learning/design-client/]
---

etcd 客户端设计 {#etcd-client-design}
====================

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


简介 {#introduction}
====================

etcd 服务器通过多年的故障注入测试验证了其稳健性。大多数复杂的应用逻辑已由 etcd 服务器及其数据存储处理（例如，集群成员关系对客户端透明，提案通过 Raft 层转发至领导者）。尽管服务器组件本身正确，但其与客户端的组合需采用一组复杂的协议，以确保在故障条件下仍能保证正确性和高可用性。理想情况下，etcd 服务器为多台物理机器提供单一逻辑集群视图，客户端则实现副本间的自动故障转移。本文档描述客户端的架构决策及其具体实现细节。


术语表 {#glossary}
====================

*clientv3*：etcd v3 API 的官方 Go 客户端。

*clientv3-grpc1.0*：官方客户端实现，包含 [`grpc-go v1.0.x`](https://github.com/grpc/grpc-go/releases/tag/v1.0.0)，在最新版 etcd v3.1 中使用。

*clientv3-grpc1.7*：官方客户端实现，包含 [`grpc-go v1.7.x`](https://github.com/grpc/grpc-go/releases/tag/v1.7.0)，用于最新版 etcd v3.2 和 v3.3。

*clientv3-grpc1.23*：官方客户端实现，包含 [`grpc-go v1.23.x`](https://github.com/grpc/grpc-go/releases/tag/v1.23.0)，在最新版 etcd v3.4 中使用。

*负载均衡器*：etcd 客户端负载均衡器，实现重试和故障转移机制。etcd 客户端应能自动在多个端点之间均衡负载。

*端点*：客户端可连接的 etcd 服务器端点列表。通常为 etcd 集群的 3 个或 5 个客户端 URL。

*固定端点*：当配置多个端点时，v3.3 及更早版本的客户端负载均衡器仅选择一个端点建立 TCP 连接，以减少与 etcd 集群的总连接数。在 v3.4 版本中，负载均衡器对固定端点采用轮询策略，每个请求均轮询不同端点，从而实现更均衡的负载分布。

*客户端连接*：通过 gRPC Dial 建立的与 etcd 服务器的 TCP 连接。

*子连接*：gRPC SubConn 接口。每个子连接包含一个地址列表。负载均衡器根据解析后的地址列表创建子连接。gRPC 客户端连接可以映射到多个子连接（例如，example.com 解析为 `10.10.10.1` 和 `10.10.10.2` 两个子连接）。etcd v3.4 负载均衡器采用内部解析器，为每个端点建立一个子连接。

*瞬时断开连接*：当 gRPC 服务器返回状态错误 [`code Unavailable`](https://godoc.org/google.golang.org/grpc/codes#Code) 时。


客户端要求 {#client-requirements}
====================

*正确性*。在服务器发生故障时，请求可能会失败。然而，这绝不会违反一致性保证：全局顺序性、永不写入损坏数据、可变操作的至多一次语义、监听不会观察到部分事件等。

*存活性*。服务器可能会短暂地发生故障或断开连接。客户端应能在这两种情况下均继续推进。除非已配置为等待，否则客户端不应在等待离线服务器恢复时 [陷入死锁](https://github.com/etcd-io/etcd/issues/8980)。理想情况下，客户端通过 HTTP/2 ping 检测不可用的服务器，并向其他节点进行故障转移，同时提供明确的错误信息。

*有效性*。客户端应以最少资源高效运行：在端点切换后，先前的 TCP 连接应 [优雅关闭](https://github.com/etcd-io/etcd/issues/9212)。故障转移机制应能有效预测下一个要连接的副本，避免对已失败节点进行无谓重试。

*可移植性*。官方客户端应有清晰的文档说明，其实现应适用于其他语言绑定。不同语言绑定之间的错误处理应保持一致。由于 etcd 全面采用 gRPC，实现应与 gRPC 长期设计目标紧密对齐（例如，可插拔重试策略应与 [gRPC retry](https://github.com/grpc/proposal/blob/master/A6-client-retries.md) 兼容）。两个客户端版本之间的升级应为非中断式。


客户端概述 {#client-overview}
====================

etcd 客户端实现了以下组件：

* 用于与 etcd 集群建立 gRPC 连接的负载均衡器，
* 用于向 etcd 服务器发送 RPC 的 API 客户端，以及
* 决定是否重试失败请求或切换端点的错误处理程序。

不同语言在建立初始连接（例如配置 TLS）、编码并发送 Protocol Buffer 消息至服务器、处理流式 RPC 等方面可能存在差异。然而，etcd 服务器返回的错误将保持一致。因此，错误处理和重试策略也应保持一致。

例如，etcd 服务器可能返回 `"rpc error: code = Unavailable desc = etcdserver: request timed out"`，该错误为瞬态错误，应进行重试。或返回 `rpc error: code = InvalidArgument desc = etcdserver: key is not provided`，表示请求无效，不应重试。Go 客户端可使用 `google.golang.org/grpc/status.FromError` 解析错误，Java 客户端可使用 `io.grpc.Status.fromThrowable`。


clientv3-grpc1.0：负载均衡器概述 {#clientv3-grpc10-balancer-overview}
--------------------

`clientv3-grpc1.0` 在配置多个 etcd 端点时，会维持多个 TCP 连接。随后选择一个地址，并使用该地址发送所有客户端请求。所固定的地址会一直保持，直至客户端对象关闭（参见 *图 1*）。当客户端收到错误时，会随机选择另一个地址并重试。

![client-balancer-figure-01.png](/docs/etcd/learning/img/client-balancer-figure-01.png)


clientv3-grpc1.0：负载均衡器限制 {#clientv3-grpc10-balancer-limitation}
--------------------

`clientv3-grpc1.0` 同时打开多个 TCP 连接可提供更快的负载均衡器故障转移，但需要更多资源。负载均衡器不了解节点的健康状态或集群成员关系，因此可能出现负载均衡器卡在某个已失败或分区的节点上的情况。


clientv3-grpc1.7：负载均衡器概述 {#clientv3-grpc17-balancer-overview}
--------------------

`clientv3-grpc1.7` 仅与选定的 etcd 服务器维持一个 TCP 连接。当提供多个集群端点时，客户端会尝试连接所有端点。一旦建立任一连接，负载均衡器即固定该地址，并关闭其他连接（参见 *图 2*）。该固定地址需保持至客户端对象关闭。若发生服务器错误或客户端网络故障，错误将被发送至客户端错误处理程序（参见 *图 3*）。

![client-balancer-figure-02.png](/docs/etcd/learning/img/client-balancer-figure-02.png)

![client-balancer-figure-03.png](/docs/etcd/learning/img/client-balancer-figure-03.png)

客户端错误处理程序接收来自 gRPC 服务器的错误，并根据错误码和错误信息决定是在同一端点重试，还是切换到其他地址（参见 *图 4* 和 *图 5*）。

![client-balancer-figure-04.png](/docs/etcd/learning/img/client-balancer-figure-04.png)

![client-balancer-figure-05.png](/docs/etcd/learning/img/client-balancer-figure-05.png)

流式 RPC，例如监听（Watch）和保活（KeepAlive），通常在无超时的情况下发起请求。客户端可定期发送 HTTP/2 保活 ping 来检查固定端点的状态；若服务器未响应 ping，负载均衡器将切换至其他端点（参见 *图 6*）。

![client-balancer-figure-06.png](/docs/etcd/learning/img/client-balancer-figure-06.png)


clientv3-grpc1.7：负载均衡器限制 {#clientv3-grpc17-balancer-limitation}
--------------------

`clientv3-grpc1.7` 负载均衡器通过 HTTP/2 保活机制检测流式请求的断连。这是一种简单的 gRPC 服务器 ping 机制，不涉及集群成员关系的判断，因此无法检测网络分区。由于被分区的 gRPC 服务器仍可响应客户端 ping，负载均衡器可能陷入与分区节点的连接中。理想情况下，保活 ping 应在请求超时前检测到分区并触发端点切换（参见 [etcd#8673](https://github.com/etcd-io/etcd/issues/8673) 和 *图 7*）。

![client-balancer-figure-07.png](/docs/etcd/learning/img/client-balancer-figure-07.png)

`clientv3-grpc1.7` 负载均衡器维护一个不健康端点列表。断开连接的地址会被加入“不健康”列表，并在等待时长过后才被视为可用，该等待时长硬编码为连接超时时间，默认值为 5 秒。负载均衡器可能对哪些端点不健康产生误判。例如，端点 A 可能在被标记为黑名单后立即恢复，但在接下来的 5 秒内仍不可用（参见 *图 8*）。

`clientv3-grpc1.0` 遇到了上述相同的问题。

![client-balancer-figure-08.png](/docs/etcd/learning/img/client-balancer-figure-08.png)

上游 gRPC Go 已经迁移到新的负载均衡接口。例如，`clientv3-grpc1.7` 的底层负载均衡实现使用了新的 gRPC 负载均衡机制，并努力与旧负载均衡行为保持一致。尽管兼容性已得到合理维护，etcd 客户端仍然 [遭受了细微的破坏性变更](https://github.com/grpc/grpc-go/issues/1649)。此外，gRPC 维护者建议 [不要依赖旧的负载均衡接口](https://github.com/grpc/grpc-go/issues/1942#issuecomment-375368665)。通常而言，为获得上游更好的支持，最好与最新的 gRPC 发布版本保持同步。此外，新功能（如重试策略）可能不会回溯到 gRPC 1.7 分支。因此，etcd 服务器和客户端都必须迁移到最新的 gRPC 版本。


clientv3-grpc1.23：负载均衡器概述 {#clientv3-grpc123-balancer-overview}
--------------------

`clientv3-grpc1.7` 与旧版 gRPC 接口耦合过于紧密，导致每次 gRPC 依赖升级都会破坏客户端行为。大部分开发与调试工作都用于修复这些客户端行为变更。结果，其实现变得过于复杂，并基于对服务器连接性的错误假设。

`clientv3-grpc1.23` 的主要目标是简化负载均衡器的故障转移逻辑：当客户端与当前端点断开连接时，不再维护一个可能已陈旧的不健康端点列表，而是直接轮询下一个端点。该机制不假设端点状态，因此无需再进行复杂的健康状态跟踪（参见 *图 8* 及以上内容）。升级至 `clientv3-grpc1.23` 不应存在问题；所有变更均为内部实现，同时保持了全部向后兼容性。

在内部实现上，当提供多个端点时，`clientv3-grpc1.23` 会创建多个子连接（每个端点对应一个子连接），而 `clientv3-grpc1.7` 仅连接到一个固定的端点（参见 *图 9*）。例如，在 5 节点集群中，`clientv3-grpc1.23` 负载均衡器需要 5 个 TCP 连接，而 `clientv3-grpc1.7` 仅需一个。通过保持 TCP 连接池，`clientv3-grpc1.23` 可能消耗更多资源，但能提供更具灵活性的负载均衡器，并具备更优的故障转移性能。默认的负载均衡策略为轮询，但可轻松扩展以支持其他类型的负载均衡器（例如，两选一（power of two）、选择领导者等）。`clientv3-grpc1.23` 使用 gRPC 解析器组并实现负载均衡选择器策略，将复杂的负载均衡工作交由上游 gRPC 处理。另一方面，`clientv3-grpc1.7` 手动处理每个 gRPC 连接及负载均衡器故障转移，这增加了实现的复杂性。`clientv3-grpc1.23` 在 gRPC 拦截器链中实现重试机制，可自动处理 gRPC 内部错误，并支持更高级的重试策略（如指数退避），而 `clientv3-grpc1.7` 则需手动解析 gRPC 错误以实现重试。

![client-balancer-figure-09.png](/docs/etcd/learning/img/client-balancer-figure-09.png)


clientv3-grpc1.23：负载均衡器限制 {#clientv3-grpc123-balancer-limitation}
--------------------

可通过缓存每个端点的状态来做出改进。例如，负载均衡器可预先 ping 每个服务器，以维护健康候选端点列表，并在轮询时使用该信息。或在断开连接时，负载均衡器可优先选择健康端点。这可能会增加负载均衡器实现的复杂性，因此可留待后续版本再行处理。

客户端保活 ping 仍不考虑网络分区情况。流式请求在与分区节点通信时可能陷入停滞。需实现高级健康检查服务以准确理解集群成员关系（详见 [etcd#8673](https://github.com/etcd-io/etcd/issues/8673)）。

![client-balancer-figure-07.png](/docs/etcd/learning/img/client-balancer-figure-07.png)

目前，重试逻辑需手动作为拦截器处理。可通过 [官方 gRPC 重试](https://github.com/grpc/proposal/blob/master/A6-client-retries.md) 简化此过程。
