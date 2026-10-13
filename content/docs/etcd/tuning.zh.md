---
title: 调优
weight: 1450
description: 何时调整心跳间隔和选举超时设置
icon: fa-solid fa-sliders
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tuning.md"
aliases: [/etcd/tuning/]
---

默认情况下，etcd 的配置在平均网络延迟较低的本地网络环境中应能良好运行。然而，当在多个数据中心之间或高延迟网络上使用 etcd 时，可能需要调整心跳间隔和选举超时设置。

网络并非延迟的唯一来源。每个请求和响应都可能受到领导者和跟随者上慢速磁盘的影响。每个超时时间均表示从请求发出到从另一台机器成功返回响应的总时间。

## 时间参数 {#time-parameters}

底层的分布式共识协议依赖两个独立的时间参数，以确保当某个节点停滞或离线时，其他节点能够完成领导权交接。第一个参数称为 *心跳间隔*（Heartbeat Interval）。该参数规定领导者向跟随者通告自身仍为领导者的频率。

最佳实践建议，该参数应设置为成员间往返时间的近似值。默认情况下，etcd 使用 `100ms` 的心跳间隔。

第二个参数是 *选举超时时间*。该超时时间表示跟随者节点在未收到心跳消息的情况下，等待多久后将尝试自行成为领导者。默认情况下，etcd 使用 `1000ms` 选举超时时间。

调整这些值需要权衡。心跳间隔的值建议约为成员间平均往返时间（RTT）的最大值，通常为往返时间的 0.5-1.5x。如果心跳间隔过低，etcd 会发送不必要的消息，增加 CPU 和网络资源的使用。另一方面，心跳间隔过高会导致选举超时时间变长，更高的选举超时会延长对领导者故障的检测时间。测量往返时间（RTT）最简便的方法是使用 [PING 工具][ping]。

选举超时应根据心跳间隔以及成员之间的平均往返时间进行设置。选举超时必须至少为往返时间的 10 倍，以应对网络波动。例如，若成员之间的往返时间为 10ms，则选举超时应至少设置为 100ms。

选举超时的上限为 50000ms（50s），仅在部署全球分布式 etcd 集群时才应使用。美国大陆范围内的合理往返时间约为 130ms，而美国与日本之间的往返时间约为 350ms 至 400ms。若网络性能不均或存在常规的包延迟或丢包，则可能需要多次重试才能成功发送数据包。因此，5s 是全球往返时间的安全上限。由于选举超时应比广播时间大一个数量级，在全球分布式集群中约为 5s 的情况下，50 秒便成为合理的最大值。

集群中所有成员的心跳间隔和选举超时值应保持一致。为 etcd 成员设置不同的值可能会导致集群稳定性受损。

默认值可通过命令行进行覆盖：

```sh
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

值以毫秒为单位指定。

## 快照 {#snapshots}

etcd 将所有键的变更追加到日志文件中。该日志会无限增长，记录了键的所有变更的完整线性历史。完整的历史记录在轻度使用的集群中表现良好，但在高负载使用的集群中，日志会变得非常庞大。

为避免日志过大，etcd 会定期生成快照。这些快照使 etcd 能通过保存系统当前状态并删除旧日志来执行压缩。

### 快照调优 {#snapshot-tuning}

Raft 快照在应用指定数量的条目后创建；etcd 3.7 已不再使用 V2 后端。默认情况下，每发生 10,000 次变更后将生成一次快照。若 etcd 的内存使用率和磁盘使用率过高，可尝试通过命令行设置降低快照阈值：

```sh
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## 磁盘 {#disk}

etcd 集群对磁盘延迟非常敏感。由于 etcd 必须将提案持久化到日志中，其他进程的磁盘活动可能导致长时间的 `fsync` 延迟。结果是 etcd 可能错过心跳，导致请求超时和临时领导者丢失。当分配较高的磁盘优先级时，etcd 服务器有时可以与这些进程稳定共存。

在 Linux 上，etcd 的磁盘优先级可通过 `ionice` 配置：

```sh
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

## 网络 {#network}

如果 etcd 领导者处理大量并发客户端请求，可能因网络拥塞而延迟处理跟随者对等成员的请求。这会在跟随者节点上表现为发送缓冲区错误消息：

```
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
```

这些错误可通过优先处理 etcd 的对等成员流量而非客户端流量来解决。在 Linux 上，可使用流量控制机制来优先处理对等成员流量：

```
tc qdisc add dev eth0 root handle 1: prio bands 3
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1
```

[ping]: https://en.wikipedia.org/wiki/Ping_(networking_utility)


要取消 `tc`，请执行：

```
tc qdisc del dev eth0 root
```

## CPU {#cpu}

由于 etcd 对延迟非常敏感，可在 Linux 系统上通过将 CPU governor 设置为 performance 或 conservative 模式，进一步优化性能。

在 Linux 上，可将 CPU governor 配置为 performance 模式：
```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
