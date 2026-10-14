---
title: etcd 学习者成员设计
weight: 2375
description: 缓解成员重新配置中的常见挑战
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-learner.md"
---

etcd 学习者成员 {#etcd-learner}
====================

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


背景 {#background}
==========

成员关系重配置一直是运维中最大的挑战之一。回顾常见问题。

### 1. 新集群成员使领导者过载 {#1-new-cluster-member-overloads-leader}
新加入的 etcd 成员初始时无任何数据，因此需要从领导者获取更多更新，直到其日志与领导者同步。此时，领导者网络更可能因负载过重而阻塞或丢弃发往跟随者的心跳。在这种情况下，跟随者可能因选举超时而发起新的领导者选举。也就是说，包含新成员的集群更容易发生领导者选举。领导者选举以及随后向新成员传播更新的过程均可能导致集群不可用的时段（参见 *图 1*）。

![server-learner-figure-01](/etcd/learning/img/server-learner-figure-01.png)

### 2. 网络分区场景 {#2-network-partitions-scenarios}
网络分区发生时会怎样？这取决于领导者是否仍能维持法定人数。如果领导者仍能保持活跃的法定人数，集群将继续运行（参见 *图 2*）。

![server-learner-figure-02](/etcd/learning/img/server-learner-figure-02.png)

#### 2.1 领导者隔离 {#21-leader-isolation}
如果领导者与集群其余部分隔离，会发生什么？领导者会监控每个跟随者的进度。当领导者与法定人数失去连接时，它将回退为跟随者，这会影响集群的可用性（参见 *图 3*）。

![server-learner-figure-03](/etcd/learning/img/server-learner-figure-03.png)

当向 3 个节点的集群添加新节点时，集群规模变为 4，法定人数规模变为 3。如果新节点加入集群后发生网络分区，结果取决于新成员在分区后位于哪个分区。

#### 2.2 集群分裂 3+1 {#22-cluster-split-31}
如果新节点恰好位于领导者所在的同一分区中，领导者仍能维持由 3 个节点组成的活跃法定人数。不会发生领导权选举，集群可用性也不会受到影响（参见 *图 4*）。

![server-learner-figure-04](/etcd/learning/img/server-learner-figure-04.png)

#### 2.3 集群分裂 2+2 {#23-cluster-split-22}
如果集群出现 2-2 分区，则任一分区均无法维持 3 个节点的法定人数。此时将触发领导权选举（参见 *图 5*）。

![server-learner-figure-05](/etcd/learning/img/server-learner-figure-05.png)

#### 2.4 法定人数丢失 {#24-quorum-lost}
如果网络分区先发生，随后再添加新成员会怎样？一个已处于分区状态的 3 节点集群中，已有 1 个跟随者与集群断开连接。当添加新成员后，法定人数从 2 变为 3。此时，集群中仅有 4 个节点中的 2 个处于活跃状态，导致失去法定人数，并启动新的领导权选举（参见 *图 6*）。

![server-learner-figure-06](/etcd/learning/img/server-learner-figure-06.png)

由于成员添加操作可能改变法定人数规模，因此始终建议先执行“member remove”以替换不健康的节点。

向单节点集群添加新成员会将法定人数大小更改为 2，当原领导者发现法定人数不再活跃时，会立即触发选举。这是因为“member add”操作是一个两步过程，用户需先执行“member add”命令，然后启动新节点进程（参见 *图 7*）。

![server-learner-figure-07](/etcd/learning/img/server-learner-figure-07.png)

### 3. 集群配置错误 {#3-cluster-misconfigurations}
更严重的情况是，当新增成员配置错误时。成员变更是一项两步操作：首先执行“etcdctl member add”，然后使用指定的对等成员 URL 启动 etcd 服务器进程。也就是说，“member add” 命令的执行不依赖于 URL 的有效性，即使 URL 值无效也会被应用。若第一步使用了无效的 URL，第二步将无法启动新的 etcd 实例。一旦集群失去法定人数，就无法回滚成员变更（参见 *图 8*）。

![server-learner-figure-08](/etcd/learning/img/server-learner-figure-08.png)

多节点集群情况亦同。例如，集群中有两个成员离线（一个已故障，另一个配置错误），两个成员在线，但此时更改集群成员关系至少需要 3 票（参见 *图 9*）。

![server-learner-figure-09](/etcd/learning/img/server-learner-figure-09.png)

如上所述，一个简单的配置错误可能导致整个集群进入无法运行的状态。在此情况下，运维人员需手动使用 `etcd --force-new-cluster` 标志重建集群。随着 etcd 成为 Kubernetes 的关键任务服务，哪怕是最轻微的中断也可能对用户造成重大影响。我们能否进一步优化，使 etcd 的此类操作更加简便？在诸多方面中，领导者选举对集群可用性最为关键：能否通过不改变法定人数规模的方式，降低成员配置变更的干扰？新节点是否可以处于空闲状态，仅从领导者请求最小量的更新，直至完成同步？成员配置错误是否始终可逆，并以更安全的方式处理（错误执行成员添加命令不应导致集群失败）？用户在添加新成员时是否需要担心网络拓扑？成员添加 API 是否应与节点位置及正在进行的网络分区无关而正常工作？

Raft 学习者成员 {#raft-learner}
====================

为缓解上一节所述的可用性缺口，[Raft §4.2.1](https://github.com/ongardie/dissertation/blob/master/stanford.pdf) 引入了一种新的节点状态“学习者成员”，该成员以**非投票成员**身份加入集群，直至其日志与领导者日志同步。

v3.4 版本特性 {#features-in-v34}
--------------------

添加新学习者成员应尽可能少地要求运维人员手动操作。使用 `member add --learner` 命令添加新的学习者成员，该成员以非投票成员身份加入集群，但仍接收来自领导者的全部数据（参见 *图 10*）。

![server-learner-figure-10](/etcd/learning/img/server-learner-figure-10.png)

当学习者成员已追上领导者进度时，可使用 `member promote` API 将其晋升为投票成员，该成员将计入法定人数（参见 *图 11*）。

![server-learner-figure-11](/etcd/learning/img/server-learner-figure-11.png)

etcd 服务器会验证提升请求，以确保操作安全。只有当学习者成员的日志已追赶上领导者时，才能将其提升为投票成员（参见 *图 12*）。

![server-learner-figure-12](/etcd/learning/img/server-learner-figure-12.png)

学习者成员仅作为备用节点，直到被提升：领导权无法转移至学习者成员。学习者成员拒绝客户端读写请求（客户端负载均衡器不应将请求路由至学习者成员）。这意味着学习者成员无需向领导者发起读索引请求。此限制简化了 v3.4 版本中学习者成员功能的初始实现（参见 *图 13*）。

![server-learner-figure-13](/etcd/learning/img/server-learner-figure-13.png)

此外，etcd 限制了集群可拥有的学习者成员总数，以避免领导者因日志复制而过载。学习者成员不会自行晋升。尽管 etcd 提供了学习者成员状态信息和安全检查，但集群运维人员必须最终决定是否晋升学习者成员。

未来版本提议的功能 {#proposed-features-for-future-releases}
--------------------

*仅启用学习者成员状态并设为默认*：将新成员状态默认设为学习者成员可显著提升成员配置变更的安全性，因为学习者成员不会影响法定人数的大小。配置错误始终可逆，且不会导致法定人数丢失。

*实现学习者成员晋升的完全自动化*：当学习者成员追赶上领导者的日志后，集群可自动将其晋升为投票成员。etcd 要求用户定义特定阈值，一旦满足条件，学习者成员将自动晋升为投票成员。从用户视角看，“member add” 命令的使用方式与当前一致，但通过学习者成员功能提供了更高的安全性。

*将学习者成员设为备用故障转移节点*：学习者成员以备用节点身份加入集群，当集群可用性受到影响时，将自动晋升为投票成员。

*使学习者成员为只读*：学习者成员可作为只读节点，且永远不会被提升为投票成员。在弱一致性模式下，学习者成员仅从领导者接收数据，且从不处理写入操作。通过本地提供读取服务而无需共识开销，可显著降低领导者的工作负载，但可能提供陈旧数据。在强一致性模式下，学习者成员会向领导者请求读索引以提供最新数据，但仍拒绝写入操作。

学习者成员与镜像制作器 {#learner-vs-mirror-maker}
====================

etcd 使用监听 API 实现“镜像制作器”，以持续将键的创建和更新同步到另一个集群。镜像同步在完成初始同步后，通常具有较低的延迟开销。学习者成员与镜像同步存在重叠，二者均可用于复制现有数据以供只读访问。然而，镜像同步不保证线性一致性。在网络断开期间，先前的键值可能已被丢弃，客户端应验证监听响应以确保正确顺序。因此，镜像同步不提供顺序保证。在需要最低延迟（例如跨数据中心）的场景下，可使用镜像同步，但需承担一致性损失。如需保留所有历史数据及其顺序，应使用学习者成员。

附录：v3.4 中的学习者成员实现 {#appendix-learner-implementation-in-v34}
====================

*将“Learner”节点类型暴露给“MemberAdd”API。*

etcd 客户端在 “MemberAdd” API 中添加了一个用于学习者成员的标志。etcd 服务器处理程序会以 `pb.ConfChangeAddLearnerNode` 类型应用成员变更条目。命令应用完成后，服务器将以 `etcd --initial-cluster-state=existing` 标志加入集群。该学习者成员既不能投票，也不能计入法定人数。

etcd 服务器不得将领导权转移给学习者成员，因为学习者成员可能仍存在延迟，且不计入法定人数。etcd 服务器限制集群中学习者成员的数量为一个：学习者成员越多，领导者需传播的数据就越多。客户端可以与学习者成员通信，但学习者成员仅接受可串行化读取和成员状态 API 请求，拒绝所有其他请求。这是为了简化初始实现。未来，学习者成员可扩展为持续同步集群数据的只读服务器。客户端负载均衡器必须提供辅助函数以排除学习者成员的端点。否则，发送至学习者成员的请求可能失败。客户端同步成员调用应考虑学习者成员类型。客户端端点更新调用也应如此。

`MemberList` 和 `MemberStatus` 的响应应明确指出哪个节点是学习者成员。

*添加 "MemberPromote" API。*

在 Raft 内部，对学习者成员的第二次 `MemberAdd` 调用会将其提升为投票成员。领导者维护每个跟随者和学习者成员的进度。若学习者成员尚未完成其快照消息，则拒绝提升请求。仅当且仅当满足以下条件时，才接受提升请求：学习者成员处于健康状态；学习者成员与领导者同步，或偏差在阈值范围内（例如，需复制至学习者成员的条目数量少于快照数量的 1/10，这意味着即使在提升后，领导者也较不可能需要向学习者成员发送快照）。所有这些逻辑均硬编码在 `etcdserver` 包中，不可配置。

参考 {#reference}
====================

- 原始 GitHub 问题：[etcd#9161](https://github.com/etcd-io/etcd/issues/9161)
- 使用场景：[etcd#3715](https://github.com/etcd-io/etcd/issues/3715)
- 使用场景：[etcd#8888](https://github.com/etcd-io/etcd/issues/8888)
- 使用场景：[etcd#10114](https://github.com/etcd-io/etcd/issues/10114)
