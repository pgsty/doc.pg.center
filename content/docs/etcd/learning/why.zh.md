---
title: etcd 与其它键值存储系统比较
weight: 2875
description: etcd 的历史与用途及与其他工具的比较
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
aliases: [/etcd/learning/why/]
---

etcd 这个名称源自两个理念：Unix 系统中的“/etc”目录和“d”istributed（分布式）系统。其中，“/etc”目录是用于存储单个系统配置数据的路径，而 etcd 则用于存储大规模分布式系统的配置信息。因此，“d”istributed “/etc”即为 etcd。

etcd 旨在作为大规模分布式系统的通用基础架构。这类系统无法容忍脑裂（split-brain）运行，且愿意牺牲可用性以达成此目标。etcd 以一致且容错的方式存储元数据。etcd 集群旨在提供具备顶级稳定性、可靠性、可扩展性和性能的键值存储。

分布式系统使用 etcd 作为一致性的键值存储，用于配置管理、服务发现以及协调分布式任务。许多 [组织][production-users] 使用 etcd 实现生产系统，例如容器调度器、服务发现服务和分布式数据存储。使用 etcd 的常见分布式模式包括 [领导者选举][etcd-etcdctl-elect]、[分布式锁][etcd-etcdctl-lock]，以及监控机器存活状态。

## 使用场景 {#use-cases}

- Container Linux by CoreOS：在 [Container Linux][container-linux] 上运行的应用程序可获得自动、零停机的 Linux 内核更新。Container Linux 使用 [locksmith] 协调更新过程。Locksmith 通过 etcd 实现分布式信号量，确保集群中任意时刻仅有一部分节点处于重启状态。
- [Kubernetes][kubernetes] 将配置数据存储于 etcd，以实现服务发现与集群管理；etcd 的一致性对服务的正确调度与运行至关重要。Kubernetes API 服务器将集群状态持久化至 etcd。它使用 etcd 的监听（watch）API 监控集群，并推送关键配置变更。

## 对比图表 {#comparison-chart}

也许 etcd 已经看起来非常合适，但如同所有技术决策一样，仍需谨慎行事。请注意，本文由 etcd 团队编写。尽管理想情况是客观比较技术与功能，但作者的专业知识和倾向显然偏向 etcd。请仅按说明使用。

下表为快速对比 etcd 与其最流行替代方案差异的便捷参考。各列的进一步说明与详细信息请参见表格后的章节。

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| 并发原语 | [锁 RPC][etcd-v3lock], [选举 RPC][etcd-v3election], [命令行锁][etcd-etcdctl-lock], [命令行选举][etcd-etcdctl-elect], [Go 中的 recipes][etcd-recipe] | 外部 [Curator recipes][curator]（Java） | [原生锁 API][consul-lock] | [罕见][newsql-leader]，若有也极少 |
| 线性一致读取 | [是][etcd-linread] | 否 | [是][consul-linread] | 有时 |
| 多版本并发控制 | [是][etcd-mvcc] | 否 | 否 | 有时 |
| 事务 | [字段比较、读取、写入][etcd-txn] | [版本检查、写入][zk-txn] | [字段比较、锁、读取、写入][consul-txn] | SQL 风格 |
| 变更通知 | [历史与当前键区间][etcd-watch] | [当前键与目录][zk-watch] | [当前键与前缀][consul-watch] | 触发器（有时） |
| 用户权限 | [基于角色][etcd-rbac] | [ACL][zk-acl] | [ACL][consul-acl] | 不同（按表 [GRANT][cockroach-grant]，按数据库 [角色][spanner-roles]） |
| HTTP/JSON API | [是][etcd-json] | 否 | [是][consul-json] | 很少 |
| 成员关系重配置 | [是][etcd-reconfig] | [高于 3.5.0][zk-reconfig] | [是][consul-reconfig] | 是 |
| 最大可靠数据库容量 | 数 GB | 数百 MB（有时可达数 GB） | 数百 MB | 数 TB 以上 |
| 最小读取线性化延迟 | 网络 RTT | 无读取线性化 | RTT + fsync | 时钟屏障（原子时钟、NTP） |

### ZooKeeper {#zookeeper}

ZooKeeper 解决的问题与 etcd 相同：分布式系统协调与元数据存储。然而，etcd 拥有从 ZooKeeper 设计与实现的工程和运维经验中汲取的后见之明。从 ZooKeeper 中汲取的教训确实影响了 etcd 的设计，使其能够支持 Kubernetes 等大规模系统。etcd 相较于 ZooKeeper 的改进包括：

* 动态集群成员关系重配置
* 高负载下的稳定读写
* 多版本并发控制数据模型
* 可靠的键监控，永不静默丢失事件
* 租约原语将连接与会话解耦
* 用于安全分布式共享锁的 API

此外，etcd 原生支持多种语言和框架。与 Zookeeper 采用其专属的自定义 Jute RPC 协议不同，该协议完全专属于 Zookeeper 并限制了 [支持的语言绑定][zk-bindings]，etcd 的客户端协议基于 [gRPC][grpc]，一个广受欢迎的 RPC 框架，提供 Go、C++、Java 等多种语言绑定。同样，gRPC 可通过 HTTP 序列化为 JSON，因此即使是一般的命令行工具如 `curl` 也能与其通信。由于系统可自由选择多种技术方案，它们使用各自的原生工具构建在 etcd 之上，而非围绕 etcd 采用单一固定的技术栈。

在考虑功能、支持和稳定性时，计划使用 Zookeeper 作为一致键值存储的新应用程序应选择 etcd。

### Consul {#consul}

Consul 是一个端到端的服务发现框架。它提供内置的健康检查、故障检测和 DNS 服务。此外，Consul 还通过 RESTful HTTP API 暴露了一个键值存储系统。[截至 Consul 1.0 版本][dbtester-comparison-results]，其存储系统在键值操作上的扩展性不如 etcd 或 Zookeeper 等系统；对于需要管理数百万个键的系统，将面临高延迟和内存压力。键值 API 缺少关键功能，尤其是多版本键、条件事务以及可靠的流式监听。

etcd 与 Consul 解决不同的问题。若需要分布式一致的键值存储，etcd 比 Consul 更为合适。若需要端到端的集群服务发现，etcd 功能不足；应选择 Kubernetes、Consul 或 SmartStack。

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

etcd 与 NewSQL 数据库（例如 [Cockroach][cockroach]、[TiDB][tidb]、[Google Spanner][spanner]）均提供强数据一致性保证，并具备高可用性。然而，显著不同的系统设计参数导致其客户端 API 和性能特征存在显著差异。

NewSQL 数据库旨在跨数据中心水平扩展。这类系统通常将数据分区到多个一致的复制组（分片）中，这些分片可能分布于不同地理位置，存储的数据集规模可达数 TB 及以上。此类扩展方式导致其在分布式协调方面表现不佳，因为其等待时钟会产生较长延迟，且预期更新操作的依赖图大多具有局部性。数据以表格形式组织，支持类似 SQL 的查询功能，语义比 etcd 更丰富，但相应地增加了查询处理、规划和优化的复杂性。

简而言之，选择 etcd 用于存储元数据或协调分布式应用。若需存储超过几 GB 的数据，或需要完整的 SQL 查询功能，则应选择 NewSQL 数据库。

## 使用 etcd 存储元数据 {#using-etcd-for-metadata}

etcd 在单一一致的复制组内复制所有数据。对于存储几 GB 以内、需保持一致顺序的数据，这是最高效的方法。集群状态的每次修改（可能涉及多个键）都会被分配一个全局唯一标识，即 etcd 中的修订版本，该标识来自单调递增的计数器，用于推理操作顺序。由于仅存在一个复制组，修改请求只需通过 Raft 协议即可提交。通过将共识限制在单一复制组内，etcd 在采用简单协议的同时实现了分布式一致性，并达到了低延迟和高吞吐量。

etcd 的复制机制无法横向扩展，原因在于其缺乏数据分片。相比之下，NewSQL 数据库通常将数据分片存储于多个一致的复制组中，可存储规模达数 TB 及以上的数据集。然而，为确保每次修改都具有全局唯一且递增的 ID，每个请求必须在复制组之间通过额外的协调协议进行处理。这一额外的协调步骤可能导致全局 ID 冲突，迫使有序请求进行重试。最终结果是，该方案实现方式更为复杂，且在严格有序场景下的性能通常劣于 etcd。

如果应用程序主要关注元数据或元数据的顺序，例如用于协调进程，应选择 etcd。如果应用程序需要一个跨多个数据中心的大型数据存储系统，且对强全局顺序性要求不高，应选择 NewSQL 数据库。

## 使用 etcd 进行分布式协调 {#using-etcd-for-distributed-coordination}

etcd 内置了分布式协调原语，包括事件监听、租约、选举以及分布式共享锁（请注意，使用分布式共享锁时，用户需了解其非显而易见的特性，详情见下文）。这些原语均由 etcd 开发者维护和支持；若将这些原语交由外部库实现，则等于推卸了开发基础分布式软件的责任，本质上使系统变得不完整。NewSQL 数据库通常期望这些分布式协调原语由第三方提供。类似地，ZooKeeper 以其独立的 [协调算法库][curator] 著称。Consul 提供原生锁 API，甚至坦言其“[并非牢靠的方法][consul-bulletproof]”。

理论上，可以在任何提供强一致性的存储系统之上构建这些原语。然而，相关算法往往十分微妙；很容易设计出看似可行的锁机制，却因惊群效应和时序偏差而突然失效。此外，etcd 支持的其他原语（如事务内存）依赖于 etcd 的 MVCC 数据模型；仅具备简单的强一致性是不够的。

在分布式协调场景中，选择 etcd 可以避免运维困扰并节省工程投入。

### 关于锁和租约的使用说明 {#notes-on-the-usage-of-lock-and-lease}
etcd 提供 [锁 API][etcd-v3lock]，其基于 [租约机制][lease] 以及 [etcd 中的实现][etcdlease]。租约机制的基本思想是：服务器向请求客户端授予一个令牌，称为租约。当服务器授予租约时，会为其关联一个 TTL。当服务器检测到时间流逝超过 TTL 时，将撤销该租约。只要客户端持有未被撤销的租约，即可声称其拥有与该租约关联的资源的访问权。在 etcd 中，该资源是 etcd 键空间中的一个键。etcd 通过此机制提供锁 API。然而，锁 API 本身不能作为互斥机制使用。API 被称为锁，是由于 [历史原因][chubby]。不过，如以下所述，锁 API 可作为互斥机制的优化手段使用。

租约机制最重要的方面是，TTL 被定义为物理时间间隔。服务器和客户端均使用各自的时钟来衡量时间的流逝。这可能导致一种情况：服务器已撤销租约，但客户端仍声称自己拥有该租约。

租约机制如何保证锁机制的互斥性？实际上，租约机制本身并不能保证互斥性。拥有租约并不能保证租约持有者持有该资源的锁。

在使用 etcd 锁控制对 etcd 自身键的互斥访问时，互斥性基于版本号验证机制实现（在其他系统如 Consul 中有时称为比较并交换）。在 etcd 的 RPC 接口中，例如 `Put` 或 `Txn`，可指定操作所需的修订版本号和租约 ID 条件。若条件不满足，操作可能失败。借助此机制，etcd 为客户端提供分布式锁功能。这意味着，当客户端请求被 etcd 集群成功处理时，客户端可确认其已获取到某键的锁。

在分布式锁的文献中，类似的架构设计被描述如下：
* 在 [Chubby][chubby] 论文中，引入了 *sequencer* 的概念。我们理解该 sequencer 与 etcd 中的修订版本号和租约 ID 的组合几乎相同。
* 在 [如何实现分布式锁][fencing] 中，Martin Kleppmann 提出了 *fencing token* 的概念。作者认为，在 etcd 场景下，fencing token 即为修订版本号。
* 在 [分布式系统中同步时钟的实际应用][physicalclock] 中，可以找到描述：Thor 基于版本号验证和租约实现了一种分布式锁机制。

为何 etcd 及其他系统在基于版本号验证实现互斥的同时仍提供租约机制？这是因为租约可作为优化机制，有效减少被中止请求的数量。

请注意，etcd 键的锁定可高效实现，这是由于租约机制和版本号验证机制的共同作用。若用户需要保护与 etcd 无关的资源，则这些资源必须提供类似 etcd 键的版本号验证机制以及副本一致性保障。etcd 自身的锁功能无法用于保护外部资源。

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /zh/docs/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /zh/docs/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /zh/docs/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /zh/docs/etcd/learning/data_model/
[etcd-rbac]: /zh/docs/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /zh/docs/etcd/op-guide/runtime-configuration
[etcd-txn]: /zh/docs/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /zh/docs/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
