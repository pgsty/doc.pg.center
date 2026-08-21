---
title: 指标
weight: 1350
description: 实时监控和调试指标
icon: fa-solid fa-chart-line
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/metrics/_index.md"
---

etcd 使用 [Prometheus][prometheus] 进行指标报告。指标可用于实时监控和调试。etcd 不会持久化其指标；若成员重启，指标将被重置。

查看可用指标最简单的方法是使用 cURL 访问指标端点 `/metrics`。其格式详见 [Prometheus 文档](http://prometheus.io/docs/instrumenting/exposition_formats/)。

请按照 [Prometheus 入门指南][prometheus-getting-started] 启动 Prometheus 服务器，以收集 etcd 指标。

指标命名遵循建议的 [Prometheus 最佳实践][prometheus-naming]。指标名称以 `etcd` 或 `etcd_debugging` 作为命名空间前缀，并可包含子系统前缀（例如 `wal` 和 `etcdserver`）。

## etcd 命名空间指标 {#etcd-namespace-metrics}

以 `etcd` 为前缀的指标用于监控和告警。这些是稳定且高层次的指标。若此类指标有任何变更，将包含在发布说明中。

与 etcd2 相关的指标在 [v2 指标指南][v2-http-metrics] 中有详细说明。

### 服务器 {#server}

这些指标描述了 etcd 服务器的运行状态。为检测故障或排查问题，应密切监控每个生产环境 etcd 集群的服务器指标。

所有这些指标均以 `etcd_server_` 为前缀

| 名称                      | 描述                                              | 类型    |
|---------------------------|---------------------------------------------------|---------|
| has_leader                | 是否存在领导者。1 表示存在，0 表示不存在。         | 仪表     |
| leader_changes_seen_total | 观察到的领导者变更次数。                            | 计数器   |
| proposals_committed_total | 已提交的共识提案总数。                              | 仪表     |
| proposals_applied_total   | 已应用的共识提案总数。                              | 仪表     |
| proposals_pending         | 当前待处理的提案数量。                              | 仪表     |
| proposals_failed_total    | 观察到的失败提案总数。                              | 计数器   |

`has_leader` 表示成员是否具有领导者。如果某个成员没有领导者，则该成员完全不可用。如果集群中的所有成员均无领导者，则整个集群完全不可用。

`leader_changes_seen_total` 统计该成员自启动以来所经历的领导者变更次数。频繁的领导权变更会显著影响 etcd 的性能，同时也表明领导者不稳定，可能是由于网络连接问题或 etcd 集群负载过高所致。

`proposals_committed_total` 记录已提交的共识提案总数。如果集群运行正常，该指标应随时间持续增长。etcd 集群中多个健康成员可能在某一时刻拥有不同的已提交提案总数。这种差异可能是由于启动后正在恢复对等成员、落后于领导者，或本身是领导者而拥有最多提交记录所致。必须在集群所有成员上监控此指标；若某个成员与领导者之间持续存在较大延迟，表明该成员运行缓慢或状态异常。

`proposals_applied_total` 记录已应用的共识提案总数。etcd 服务器异步应用每个已提交的提案。`proposals_committed_total` 与 `proposals_applied_total` 之间的差值通常应较小（即使在高负载下也应在数千以内）。如果两者之间的差值持续增大，表明 etcd 服务器已过载。这可能发生在应用高开销查询（如大量范围查询或大型事务操作）时。

`proposals_pending` 表示待提交的提案数量。待提交的提案数量上升，表明客户端负载较高，或成员无法提交提案。

`proposals_failed_total` 通常与两个问题相关：领导者选举期间的临时故障，或因集群失去法定人数而导致的长时间停机。

### 磁盘 {#disk}

这些指标描述了磁盘操作的状态。

所有这些指标均以 `etcd_disk_` 为前缀。

| 名称                               | 描述                                           | 类型      |
|------------------------------------|------------------------------------------------|-----------|
| wal_fsync_duration_seconds         | WAL 调用 fsync 的延迟分布                     | 直方图    |
| backend_commit_duration_seconds    | 后端调用 commit 的延迟分布                     | 直方图    |

在 etcd 将日志条目写入磁盘并应用之前，会调用 `wal_fsync`。

当 etcd 将其最近的增量快照写入磁盘时，会调用 `backend_commit`。

高磁盘操作延迟（`wal_fsync_duration_seconds` 或 `backend_commit_duration_seconds`）通常表明存在磁盘问题。可能导致请求延迟升高或使集群不稳定。

### 网络 {#network}

这些指标描述了网络状态。

所有这些指标均以 `etcd_network_` 为前缀

| 名称                            | 描述                                                        | 类型          |
|---------------------------------|--------------------------------------------------------------------|---------------|
| peer_sent_bytes_total           | 发送到 ID 为 `To` 的对等成员的总字节数。           | 计数器（To）   |
| peer_received_bytes_total       | 从 ID 为 `From` 的对等成员接收的总字节数。           | 计数器（From） |
| peer_sent_failures_total        | 发送到 ID 为 `To` 的对等成员时发生的失败总次数。 | 计数器（To）   |
| peer_received_failures_total    | 从 ID 为 `From` 的对等成员接收时发生的失败总次数。 | 计数器（From） |
| peer_round_trip_time_seconds    | 对等成员之间的往返时间（RTT）直方图。           | 直方图（To）   |
| client_grpc_sent_bytes_total    | 发送到 gRPC 客户端的总字节数。                    | 计数器       |
| client_grpc_received_bytes_total| 从 gRPC 客户端接收的总字节数。                | 计数器       |

`peer_sent_bytes_total` 统计发送至特定对等成员的总字节数。通常，领导者成员发送的数据量多于其他成员，因为它负责传输已复制的数据。

`peer_received_bytes_total` 统计从特定对等成员接收的总字节数。通常，跟随者成员仅从领导者成员接收数据。

### gRPC 请求 {#grpc-requests}

这些指标通过 [go-grpc-prometheus][go-grpc-prometheus] 暴露。

## etcd 调试命名空间指标 {#etcd_debugging-namespace-metrics}

以 `etcd_debugging` 为前缀的指标用于调试。这些指标高度依赖实现且不稳定，可能在新的 etcd 版本中未经通知即被修改或移除。当部分指标趋于稳定后，可能会被迁移至 `etcd` 前缀。

### 快照 {#snapshot}

| 名称                                       | 描述                                                       | 类型      |
|--------------------------------------------|------------------------------------------------------------|-----------|
| snapshot_save_total_duration_seconds       | 快照调用保存操作的总延迟分布                                 | 直方图     |

快照持续时间异常高（`snapshot_save_total_duration_seconds`）表明存在磁盘问题，可能导致集群不稳定。

## Prometheus 供应的指标 {#prometheus-supplied-metrics}

Prometheus 客户端库在 `go` 和 `process` 命名空间下提供了一系列指标。其中有一些尤为值得关注。

| 名称                              | 描述                                       | 类型         |
|-----------------------------------|--------------------------------------------|--------------|
| process_open_fds                  | 打开的文件描述符数量。                     | 仪表         |
| process_max_fds                   | 最大打开文件描述符数量。                   | 仪表         |

> [!NOTE]
> 当前版本不支持在 Darwin（macOS）系统上使用进程指标，例如 `process_open_fds` 和 `process_max_fds`。

高文件描述符（`process_open_fds`）使用率（即接近进程的文件描述符限制，`process_max_fds`）表明可能存在文件描述符耗尽问题。若文件描述符耗尽，etcd 可能因无法创建新的 WAL 文件而发生崩溃。

## 生成的指标列表 {#generated-list-of-metrics}

[go-grpc-prometheus]: https://github.com/grpc-ecosystem/go-grpc-prometheus
[prometheus]: https://prometheus.io/
[prometheus-getting-started]: https://prometheus.io/docs/introduction/getting_started/
[prometheus-naming]: https://prometheus.io/docs/practices/naming/
[v2-http-metrics]: https://etcd.io/docs/v2.3/metrics/#http-requests
