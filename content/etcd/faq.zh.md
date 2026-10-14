---
title: 常见问题
weight: 1200
description: 常见问题解答
icon: fa-solid fa-circle-question
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/faq.md"
---

## etcd，通用 {#etcd-general}

### etcd 是什么？ {#what-is-etcd}

etcd 是一个一致性的分布式键值存储。主要用于分布式系统中的独立协调服务，专为存储可完全容纳在内存中的少量数据而设计。

### 如何发音 etcd？ {#how-do-you-pronounce-etcd}

etcd 读作 **/ˈɛtsiːdiː/**，意为“分布式 `etc` 目录”。

### 客户端是否需要向 etcd 领导者发送请求？ {#do-clients-have-to-send-requests-to-the-etcd-leader}

[Raft][raft] 采用领导者机制；所有需要集群共识的客户端请求均由领导者处理。然而，客户端无需知晓哪个节点是领导者。任何发送至跟随者的需共识请求将自动转发至领导者。无需共识的请求（例如可串行化读取）可由集群任意成员处理。

## 配置 {#configuration}

### listen-<client,peer>-urls、advertise-client-urls 或 initial-advertise-peer-urls 之间有什么区别？ {#what-is-the-difference-between-listen-clientpeer-urls-advertise-client-urls-or-initial-advertise-peer-urls}

`listen-client-urls` 和 `listen-peer-urls` 指定 etcd 服务器用于接受入站连接的本地地址。若需监听所有接口的端口，请将 `0.0.0.0` 作为监听 IP 地址。

`advertise-client-urls` 和 `initial-advertise-peer-urls` 指定 etcd 客户端或其他 etcd 成员应使用的地址，以联系 etcd 服务器。通告地址必须可从远程机器访问。生产环境不应通告 `localhost` 或 `0.0.0.0` 等地址，因为这些地址无法从远程机器访问。

### 为什么修改 `--listen-peer-urls` 或 `--initial-advertise-peer-urls` 不会更新 `etcdctl member list` 中的对等成员通告 URL？ {#why-doesnt-changing---listen-peer-urls-or---initial-advertise-peer-urls-update-the-advertised-peer-urls-in-etcdctl-member-list}

成员的已通告对等成员 URL 来自 `--initial-advertise-peer-urls`，在集群初始启动时确定。在成员启动后更改监听对等成员 URL 或初始通告对等成员 URL，不会影响已导出的通告对等成员 URL，因为此类变更必须通过法定人数达成一致，以避免成员配置出现脑裂。请使用 `etcdctl member update` 更新成员的对等成员 URL。

## 部署 {#deployment}

### 系统要求 {#system-requirements}

由于 etcd 将数据写入磁盘，其性能高度依赖磁盘性能。因此，强烈建议使用 SSD。为评估磁盘是否足够快以满足 etcd 需求，一种方法是使用磁盘基准测试工具，例如 [fio][fio]。有关具体操作示例，请参阅 [这里][fio-blog-post]。为防止性能下降或意外过度负载键值存储，etcd 默认强制执行 2GB 的可配置存储大小配额。为避免交换或内存不足，机器应至少具备与配额相当的 RAM。在常规环境中，建议将存储配额最大设为 8GB，若配置值超过此值，etcd 在启动时会发出警告。在 CoreOS，etcd 集群通常部署在专用的 CoreOS Container Linux 机器上，至少配备双核处理器、2GB 内存和 80GB SSD。**请注意，性能本质上与工作负载相关；请在生产部署前进行测试**。更多建议请参见 [硬件指南][hardware-setup]。

最稳定的生产环境为基于 amd64 架构的 Linux 操作系统；详见 [支持的平台][supported-platform]。

### 为什么集群成员数要为奇数？ {#why-an-odd-number-of-cluster-members}

etcd 集群需要多数节点达成一致，才能对集群状态进行更新，这一多数即为法定人数。对于包含 n 个成员的集群，法定人数为 (n/2)+1。对于任意奇数规模的集群，增加一个节点始终会提高达成法定人数所需的节点数量。尽管向奇数规模集群添加节点看似更优（因为机器数量更多），但其容错能力反而更差，因为可容忍的故障数量没有增加，而可能发生故障的节点数量却增加了。当集群处于无法容忍更多故障的状态时，若在移除节点之前添加新节点，则存在风险：如果新节点无法成功注册到集群（例如地址配置错误），将永久性地失去法定人数。

### 集群最大规模是多少？ {#what-is-maximum-cluster-size}

理论上，没有硬性限制。然而，etcd 集群的节点数量通常不应超过七个。[Google Chubby 锁服务][chubby]，与 etcd 类似，并在谷歌内部广泛部署多年，建议运行五个节点。五成员 etcd 集群可容忍两个成员故障，在大多数情况下已足够。尽管更大规模的集群能提供更好的容错能力，但写入性能会因数据需在更多机器间复制而下降。

### 什么是故障容忍度？ {#what-is-failure-tolerance}

etcd 集群只要能够建立成员法定人数即可正常运行。若因临时网络故障（例如网络分区）导致法定人数丢失，etcd 在网络恢复并重新建立法定人数后会自动且安全地恢复；Raft 保证了集群的一致性。对于断电情况，etcd 会将 Raft 日志持久化到磁盘；etcd 会回放日志至故障点并恢复集群参与。对于永久性硬件故障，可通过 [运行时重配置][runtime reconfiguration]将节点从集群中移除。

建议在集群中配置奇数个成员。奇数规模的集群在容忍故障数量上与偶数规模的集群相同，但所需节点更少。通过对比偶数规模与奇数规模集群，可以明显看出这一差异：

| 集群规模 | 多数成员数 | 故障容忍度 |
|:-:|:-:|:-:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

将成员添加到集群以使集群规模变为偶数，并不会带来额外的容错能力。同样，当网络分裂为两个分区时，奇数个成员可确保始终存在一个占多数的分区；该分区可继续运行，并在分区结束后成为权威数据源。

### etcd 在跨区域或跨数据中心部署时是否可用？ {#does-etcd-work-in-cross-region-or-cross-data-center-deployments}

跨区域部署 etcd 可提升 etcd 的容错能力，因为成员位于不同的故障域中。代价是跨数据中心边界带来的更高共识请求延迟。由于 etcd 依赖成员法定人数达成共识，因此跨数据中心的延迟会较为明显，因为至少需要集群中多数成员响应共识请求。此外，集群数据必须复制到所有对等成员，因此还会产生带宽开销。

在较长的延迟情况下，etcd 的默认配置可能导致频繁的选举或心跳超时。请参阅 [调优][tuning] 以调整高延迟部署的超时设置。

## 操作 {#operation}

### 如何备份 etcd 集群？ {#how-to-backup-a-etcd-cluster}

etcdctl 提供了 `snapshot` 命令用于创建备份。详见 [备份][backup] 以获取更多详情。

### 在移除不健康成员之前，我应该先添加一个成员吗？ {#should-i-add-a-member-before-removing-an-unhealthy-member}

替换 etcd 节点时，务必先移除成员，再添加其替代节点。

etcd 基于法定人数模型实现分布式共识；在集群中，必须有 (n/2)+1 个成员就某项提案达成一致，该提案才能被提交至集群。此类提案包括键值更新和成员变更。该模型完全避免了脑裂不一致的可能性。其缺点是，一旦永久性丢失法定人数，将造成灾难性后果。

对成员关系的影响如下：若一个 3 成员集群中有 1 个成员离线，集群仍可继续推进，因为法定人数为 2，仍有 2 个成员处于正常运行状态。然而，向 3 成员集群添加新成员后，法定人数将增至 3，因为 4 个成员中需要 3 票才能达成多数。由于法定人数增加，新增成员在容错能力方面并未带来任何提升；集群再发生一次节点故障便无法恢复。

此外，该新成员存在风险，因为它可能配置错误，或无法加入集群。在这种情况下，无法恢复法定人数，因为集群中有两个成员离线、两个成员在线，但要更改成员关系以撤销错误的成员添加操作，需要三个投票。etcd 默认会拒绝可能以这种方式导致集群瘫痪的成员添加尝试。

另一方面，如果先将故障成员从集群成员关系中移除，成员数量将变为 2，法定人数仍为 2。在移除该成员后，再添加新成员，法定人数仍可保持在 2。因此，即使新节点无法启动，仍可通过剩余的存活成员通过法定人数移除新成员。

### 为什么 etcd 不接受我的成员变更？ {#why-wont-etcd-accept-my-membership-changes}

etcd 设置 `strict-reconfig-check`，以拒绝可能导致法定人数丢失的重新配置请求。放弃法定人数风险极高（尤其当集群已处于不健康状态时）。尽管在出现法定人数丢失时，可能倾向于禁用法定人数检查以添加新成员，但这可能导致集群完全不一致。对许多应用而言，这会使问题更加严重（“磁盘几何结构损坏”可能是最令人恐惧的案例）。

### 为什么 etcd 因磁盘延迟峰值而失去领导者？ {#why-does-etcd-lose-its-leader-from-disk-latency-spikes}

这是有意为之的设计；磁盘延迟是领导者活跃性的一部分。假设集群领导者需要一分钟才能将 Raft 日志更新同步到磁盘，但 etcd 集群的选举超时时间为 1 秒。尽管领导者能在选举周期内处理网络消息（例如发送心跳），但由于无法提交任何新的提案而实际上处于不可用状态；它正在等待缓慢的磁盘。如果集群因磁盘延迟频繁失去领导者，请尝试 [调优][tuning] 磁盘设置或 etcd 时间参数。

### etcd 警告“请求忽略（集群 ID 不匹配）”是什么意思？ {#what-does-the-etcd-warning-request-ignored-cluster-id-mismatch-mean}

每个新的 etcd 集群都会根据初始集群配置和用户提供的唯一 `initial-cluster-token` 值生成一个新的集群 ID。通过确保集群 ID 唯一，etcd 可防止跨集群交互，避免造成集群损坏。

通常，此警告出现在拆除旧集群后，又将部分对等成员地址用于新集群时。如果旧集群中的任何 etcd 进程仍在运行，它将尝试联系新集群。新集群会识别出集群 ID 不匹配，从而忽略该请求并发出此警告。通过确保不同集群之间的对等成员地址互不重叠，通常可清除此警告。

### “mvcc: 数据库空间超限”是什么意思，如何修复？ {#what-does-mvcc-database-space-exceeded-mean-and-how-do-i-fix-it}

etcd 中的 [多版本并发控制][api-mvcc] 数据模型会完整保留键空间的精确历史记录。若未定期执行压缩（例如，通过设置 `--auto-compaction-mode` 和 `--auto-compaction-retention`），etcd 最终将耗尽存储空间。当 etcd 存储空间不足时，会触发空间配额告警，以保护集群免受进一步写入操作的影响。只要告警处于激活状态，etcd 对写入请求的响应将返回错误 `mvcc: database space exceeded`。

从低空间配额告警中恢复：

1. [压缩][maintenance-compact] etcd 的历史记录。
2. 对每个 etcd 端点执行[碎片整理][maintenance-defragment]。
3. [解除][maintenance-disarm]告警。

### etcd 警告“etcdserver/api/v3rpc: transport: http2Server.HandleStreams failed to read frame: read tcp 127.0.0.1:2379->127.0.0.1:43020: read: connection reset by peer”是什么意思？ {#what-does-the-etcd-warning-etcdserverapiv3rpc-transport-http2serverhandlestreams-failed-to-read-frame-read-tcp-1270012379-12700143020-read-connection-reset-by-peer-mean}

这是 gRPC 侧警告，当服务器接收到客户端流提前关闭时的 TCP RST 标志。例如，客户端关闭连接时，gRPC 服务器尚未处理完 TCP 队列中的所有 HTTP/2 帧。服务器端可能丢失部分数据，但只要客户端连接已关闭，这种情况是可以接受的。

仅 [旧版本的 gRPC](https://github.com/grpc/grpc-go/issues/1362) 会记录此日志。etcd [>=v3.2.13](https://github.com/etcd-io/etcd/pull/9080) 默认以 DEBUG 级别记录此日志，因此仅在 `--log-level=debug` 标志启用时可见。

## 性能 {#performance}

### 如何对 etcd 进行基准测试？ {#how-should-i-benchmark-etcd}

尝试使用 [benchmark] 工具。当前的 [benchmark 结果][benchmark-result] 可用于对比。

### etcd 警告“应用条目花费时间过长”是什么意思？ {#what-does-the-etcd-warning-apply-entries-took-too-long-mean}

在多数 etcd 成员就提交请求达成一致后，每个 etcd 服务器会将请求应用到其数据存储，并将结果持久化到磁盘。即使使用速度较慢的机械磁盘或虚拟化网络磁盘（如 Amazon 的 EBS 或 Google 的 PD），正常情况下应用请求的时间也应少于 50 毫秒。如果平均应用时间超过 100 毫秒，etcd 将发出警告，提示条目应用耗时过长。

通常此问题由磁盘速度过慢引起。磁盘可能正遭受 etcd 与其他应用程序之间的资源争用，或磁盘本身过于缓慢（例如，共享的虚拟化磁盘）。为排除磁盘过慢导致此警告的可能性，请监控 [backend_commit_duration_seconds][backend_commit_metrics]（p99 延迟应低于 25ms），以确认磁盘速度处于合理范围。若磁盘确实过慢，为 etcd 分配专用磁盘或使用更快速的磁盘通常可解决该问题。

第二个最常见的原因是 CPU 资源不足。若监控显示机器的 CPU 使用率过高，etcd 可能无法获得足够的计算资源。通常可通过将 etcd 迁移到专用机器、增加进程资源隔离（cgroups）或将 etcd 服务器进程的优先级提升来解决该问题。

访问过多键（例如获取整个键空间）的昂贵用户请求也可能导致较长的应用延迟。然而，每个请求访问的键少于数百个时，性能应始终良好。

如果上述建议均未能消除警告，请提供详细的日志、监控数据、指标信息，以及可选的工作负载信息，[创建一个 Issue][new_issue]。

### etcd 警告“未按时发送心跳”是什么意思？ {#what-does-the-etcd-warning-failed-to-send-out-heartbeat-on-time-mean}

etcd 使用基于领导者的共识协议，实现数据的一致性复制和日志执行。集群成员选举出一个单一的领导者，其余所有成员成为跟随者。被选举出的领导者必须定期向其跟随者发送心跳，以维持领导权。如果跟随者在选举间隔内未收到心跳，则推断领导者发生故障，并触发选举。若领导者虽仍在运行但未能及时发送心跳，将导致一次不必要的选举，通常由资源不足引起。为检测此类软故障，若领导者跳过两个心跳间隔，etcd 将发出警告，提示其未能按时发送心跳。

通常此问题由磁盘速度过慢引起。在领导者发送附带元数据的心跳前，可能需要将元数据持久化到磁盘。磁盘可能存在 etcd 与其他应用程序之间的争用，或磁盘本身过于缓慢（例如共享虚拟磁盘）。为排除磁盘过慢导致此警告的可能性，可监控 [wal_fsync_duration_seconds][wal_fsync_duration_seconds]（p99 延迟应低于 10ms），以确认磁盘速度是否合理。若磁盘过慢，为 etcd 分配专用磁盘或使用更快的磁盘通常可解决问题。为判断磁盘是否足够快以满足 etcd 需求，可使用 [fio][fio] 等基准测试工具。请参阅 [这里][fio-blog-post] 以获取示例。

第二个最常见的原因是 CPU 资源不足。如果监控显示机器的 CPU 使用率过高，etcd 可能无法获得足够的计算资源。通常可通过将 etcd 迁移到专用机器、使用 cgroups 增强进程资源隔离，或将 etcd 服务器进程的优先级提升来解决该问题。

慢速网络也可能导致此问题。如果 etcd 机器之间的网络指标显示延迟较长或丢包率较高，可能表明网络容量不足以支撑 etcd。将 etcd 成员迁移到负载较低的网络通常可解决该问题。然而，若 etcd 集群跨数据中心部署，成员间的高延迟属于正常现象。对于此类部署，应将 `heartbeat-interval` 配置调整为大致匹配机器间的往返时间，并将 `election-timeout` 配置设为至少 5 倍 `heartbeat-interval`。有关详细信息，请参阅 [调优文档][tuning]。

如果上述建议均未能消除警告，请提供详细的日志、监控数据、指标信息，以及可选的工作负载信息，[创建一个 Issue][new_issue]。

### etcd 警告“快照生成花费了超过 x 秒时间……”是什么意思？ {#what-does-the-etcd-warning-snapshotting-is-taking-more-than-x-seconds-to-finish--mean}

etcd 会向缓慢的跟随者发送其完整键值存储的快照，以实现状态同步并用于 [备份][backup]。快照传输速度过慢会增加平均恢复时间（MTTR）；若集群正在以高吞吐量接收数据，缓慢的跟随者可能因在完成接收前就需要新的快照而陷入活锁。为检测快照性能缓慢问题，当快照发送耗时超过三十秒且超出 1Gbps 连接的预期传输时间时，etcd 会发出警告。


[api-mvcc]: /zh/etcd/learning/api/#revisions
[backend_commit_metrics]: /zh/etcd/metrics/#disk
[backup]: /zh/etcd/op-guide/recovery/#snapshotting-the-keyspace
[benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
[benchmark-result]: /zh/etcd/op-guide/performance/
[chubby]: http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[hardware-setup]: /zh/etcd/op-guide/hardware/
[maintenance-compact]:  /zh/etcd/op-guide/maintenance/#history-compaction-v3-api-key-value-database
[maintenance-defragment]: /zh/etcd/op-guide/maintenance/#defragmentation
[maintenance-disarm]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#alarm-disarm
[new_issue]: https://github.com/etcd-io/etcd/issues/new
[raft]: https://raft.github.io/raft.pdf
[runtime reconfiguration]: /zh/etcd/op-guide/runtime-configuration/
[supported-platform]: /zh/etcd/op-guide/supported-platform/
[tuning]: /zh/etcd/tuning/
[wal_fsync_duration_seconds]: /zh/etcd/metrics/#disk
