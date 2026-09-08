---
title: 监听内存使用量基准测试
weight: 5250
description: etcd 监听器的性能指标
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-3-watch-memory-benchmark.md"
aliases: [/etcd/benchmarks/etcd-3-watch-memory-benchmark/]
---

> [!NOTE]
> 监听功能正处于积极开发中，其内存使用量可能随开发进展而变化。我们预计其内存使用量不会显著超过以下所述数值。

etcd 的一个核心目标是支持大量客户端执行海量监听操作。etcd 旨在支持 O(10k) 个客户端、O(100K) 个监听流（每个客户端约 O(10) 个监听流）以及 O(10M) 个总监听操作（每个监听流约 O(100) 个监听）。每个单独监听操作所消耗的内存占 etcd 整体内存使用量的最大部分，因此成为当前及未来优化的重点。


etcd 监听功能的三个相关组件会占用物理内存：每个 `grpc.Conn`、每个监听流以及每次监听活动的实例。`grpc.Conn` 维护实际的 TCP 连接及其他 gRPC 连接状态。每个 `grpc.Conn` 消耗约 10 KB 内存，且可能关联多个监听流。

每个监听流都是一个独立的 HTTP2 连接，消耗额外约 10 kB 的内存。
多个监听操作可能共享一个监听流。

监听是实际用于跟踪键值存储变更的结构。每个监听操作的内存消耗应低于 < 1 KB。

```
                                          +-------+
                                          | watch |
                              +---------> | foo   |
                              |           +-------+
                       +------+-----+
                       |   stream   |
      +--------------> |            |
      |                +------+-----+     +-------+
      |                       |           | watch |
      |                       +---------> | bar   |
+-----+------+                            +-------+
|            |         +------------+
|   conn     +-------> |   stream   |
|            |         |            |
+-----+------+         +------------+
      |
      |
      |
      |                +------------+
      +--------------> |   stream   |
                       |            |
                       +------------+
```

监听的理论内存消耗可通过以下公式近似计算：`memory = c1 * number_of_conn + c2 * avg_number_of_stream_per_conn + c3 * avg_number_of_watch_stream`

## 测试环境 {#testing-environment}

etcd 版本
- git 提交哈希 https://github.com/etcd-io/etcd/commit/185097ffaa627b909007e772c175e8fefac17af3

GCE n1-standard-2 机器类型
- 7.5 GB 内存
- 2 个 CPU

## 整体内存使用情况 {#overall-memory-usage}

总体内存使用量反映了 etcd 在客户端监听器存在的情况下所消耗的 [RSS][rss]。尽管结果可能有高达 10% 的波动，但该数据仍具有意义，因为目标是了解内存使用的粗略情况及分配模式。

根据基准测试结果，我们可以粗略计算出 `c1 = 17kb`、`c2 = 18kb` 和 `c3 = 350bytes`。因此，每个额外的客户端连接消耗 17 KB 内存，每个额外的流消耗 18 KB 内存，而每个额外的监听仅消耗 350 字节。在正常情况下，单个 etcd 服务器可使用几 GB 内存维持数百万个监听。


| 客户端数量 | 每客户端流数量 | 每流监听数量 | 总监听数量 | 内存占用 |
|---------|---------|-----------|----------------|--------------|
| 1k | 1 | 1 | 1k | 50MB |
| 2k | 1 | 1 | 2k | 90MB |
| 5k | 1 | 1 | 5k | 200MB |
| 1k | 10 | 1 | 10k | 217MB |
| 2k | 10 | 1 | 20k | 417MB |
| 5k | 10 | 1 | 50k | 980MB |
| 1k | 50 | 1 | 50k | 1001MB |
| 2k | 50 | 1 | 100k | 1960MB |
| 5k | 50 | 1 | 250k | 4700MB |
| 1k | 50 | 10 | 500k | 1171MB |
| 2k | 50 | 10 | 1M | 2371MB |
| 5k | 50 | 10 | 2.5M | 5710MB |
| 1k | 50 | 100 | 5M | 2380MB |
| 2k | 50 | 100 | 10M | 4672MB |
| 5k | 50 | 100 | 25M | *OOM* |

[rss]: https://en.wikipedia.org/wiki/Resident_set_size
