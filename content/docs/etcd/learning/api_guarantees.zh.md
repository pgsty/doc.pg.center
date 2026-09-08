---
title: etcd API 保证
weight: 2750
description: etcd 提供的 API 保证
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/api_guarantees.md"
aliases: [/etcd/learning/api_guarantees/]
---

etcd 是一个一致且持久的键值存储系统。
键值存储通过 [gRPC Services] 暴露。etcd 为分布式系统提供最强的一致性和持久性保证。
本文规范列出了 etcd 所提供的 API 保证。

### 值得考虑的 API {#apis-to-consider}

* KV API
  * [范围](/zh/docs/etcd/learning/api/#range)
  * [范围流](/zh/docs/etcd/learning/api/#rangestream)
  * [写入](/zh/docs/etcd/learning/api/#put)
  * [删除](/zh/docs/etcd/learning/api/#delete-range)
  * [事务](/zh/docs/etcd/learning/api/#transaction)
* 监听 API
  * [监听](/zh/docs/etcd/learning/api/#watch-api)
* 租约 API
  * [授予](/zh/docs/etcd/learning/api/#obtaining-leases)
  * [撤销]
  * [保活](/zh/docs/etcd/learning/api/#keep-alives)

KV API 支持对键值存储进行直接读取和操作。
监听 API 支持订阅键值存储的变更。
租约 API 支持为键指定生存时间（TTL）。

KV 和 Watch API 均允许访问键的最新版本，同时也可在连续的历史窗口内访问之前的版本，该窗口受压缩操作的限制。

调用 KV API 会立即生效，而监听 API 可能会返回存在不可预测的延迟。

在正常运行的 etcd 集群中，通常应能在事件发生后 10 ms 内观察到监听事件。

然而，该延迟没有上限，不健康的集群中事件可能永远不会到达。

## 键值 API {#kv-apis}

etcd 保证所有 KV API 调用的持久性和严格可串行化。
这是分布式事务数据库系统所能提供的最强隔离保证。

### 持久性 {#durability}

任何已完成的操作都是持久的。所有可访问的数据也是持久数据。
读操作绝不会返回尚未持久化的数据。

### 严格的串行一致性 {#strict-serializability}

KV 服务操作具有原子性，并按全局顺序执行，该顺序与操作的实际时间顺序一致。全局顺序通过 [revision] 隐式确定。有关 [strict serializability] 的更多信息，请参阅相关文档。

对于不包含嵌套事务的事务，操作的执行顺序保证与其操作列表中的顺序一致，这意味着事务内部的 GET 操作响应具有稳定性。
对于包含嵌套事务的事务，执行顺序未作规定。

严格串行化意味着具备其他较弱的保证，这些保证可能更容易理解：

#### 原子性 {#atomicity}

所有 API 请求均具有原子性；操作要么完全完成，要么完全不执行。对于监听请求，单次操作生成的所有事件将包含在同一个监听响应中。监听不会观察到单次操作的部分事件。

#### 线性一致性 {#linearizability}

从客户端的角度来看，线性一致性提供了有用的性质，使推理变得简便。这是来自[原始论文][linearizability]的一段清晰描述：`线性一致性提供了这样的假象：并发进程执行的每个操作，都在其调用与响应之间某个时刻瞬间生效。`

例如，考虑一个客户端在时间点 1（*t1*）完成写入操作。在 *t2*（*t2* > *t1*）时刻发起读取的客户端，应获取到至少与 *t1* 时刻完成的写入操作同等最新的值。然而，该读取操作可能实际仅在 *t3* 时刻才完成。线性一致性保证读取返回的是最新值。若无线性一致性保证，读取返回的值在读取开始时刻 *t2* 时是最新值，但在 *t3* 时刻可能已“过时”，因为 *t2* 与 *t3* 之间可能存在并发写入。

etcd 默认对所有其他操作保证线性一致性。
然而，线性一致性会带来开销，因为线性化请求必须经过 Raft 共识流程。为降低读请求的延迟并提高吞吐量，客户端可将请求的一致性模式配置为 `serializable`，该模式可能访问相对于法定人数过时的数据，但可消除线性化访问依赖实时共识所带来的性能开销。

## 监听 API {#watch-apis}

监听保证事件满足以下特性：
* 有序性 - 事件按修订版本排序。
  若某个事件在时间上早于已发布的事件，则该事件不会出现在监听中。对于不含嵌套事务的事务，生成的事件顺序与操作列表中的顺序一致。对于包含嵌套事务的事务，生成事件的顺序未作规定。
* 唯一性 - 事件不会在监听中重复出现。
* 可靠性 - 事件序列不会丢失可用历史窗口内的任何子序列。若事件按时间顺序为 a < b < c，且监听收到了事件 a 和 c，则只要 b 仍在可用历史窗口内，就保证会收到事件 b。
* 原子性 - 事件列表保证涵盖完整的修订版本。同一修订版本中对多个键的更新不会被拆分到多个事件列表中。
* 可恢复性 - 若监听中断，可通过建立新的监听来恢复，新监听从中断前最后一个事件的修订版本之后开始，只要该修订版本仍在历史窗口内。
* 可标记性 - 进度通知事件保证所有至指定修订版本的事件均已送达。

etcd 不保证监听操作的线性一致性。应验证监听事件的修订版本，以确保其与其他操作的顺序正确。

## 租约 API {#lease-apis}

etcd 提供 [租约机制][lease]。租约的主要用途是实现分布式协调机制，例如分布式锁。租约机制本身较为简单：可通过 grant API 创建租约，通过 put API 将其绑定到键，通过 revoke API 撤销租约，并在生存时间（TTL）到期后由墙钟时间自动过期。然而，用户需注意 [API 和使用方式的重要特性][why]，以正确实现分布式协调机制。

## etcd 特定定义 {#etcd-specific-definitions}

### 操作完成 {#operation-completed}

etcd 操作在通过共识达成一致并由 etcd 存储引擎“执行”（即永久存储）后，被视为已完成。客户端在收到 etcd 服务器的响应时，即可确认操作已完成。请注意，若客户端超时，或客户端与 etcd 成员之间发生网络中断，客户端可能无法确定操作的状态。在发生领导者选举时，etcd 也可能中止操作。在此情况下，etcd 不会向客户端的未完成请求发送 `abort` 响应。

### 修订版本 {#revision}

对 etcd 键值存储执行修改操作时，将分配一个单一且递增的修订版本。事务操作可能多次修改键值存储，但仅分配一个修订版本。由该操作修改的键值对的修订版本属性，与操作的修订版本值相同。修订版本可作为键值存储的逻辑时钟。修订版本较大的键值对，其修改时间晚于修订版本较小的键值对。具有相同修订版本的两个键值对，是由一个操作“并发”修改的。

[grpc Services]: /zh/docs/etcd/learning/api/#grpc-services
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[linearizability]: https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf
[serializable_isolation]: https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable
[strict serializability]: http://jepsen.io/consistency/models/strict-serializable
[txn]: /zh/docs/etcd/learning/api/#transaction
[why]: /zh/docs/etcd/learning/why/#notes-on-the-usage-of-lock-and-lease
[revision]: #revision
