---
title: 性能
weight: 4550
description: "理解性能：延迟与吞吐量"
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/performance.md"
---

## 理解性能 {#understanding-performance}

etcd 提供稳定、持续的高性能。性能由两个因素决定：延迟和吞吐量。延迟是指完成操作所需的时间。吞吐量是指在一定时间周期内完成的总操作数。通常情况下，当 etcd 接受并发客户端请求时，平均延迟会随着整体吞吐量的增加而上升。在常见的云环境（如 Google Compute Engine (GCE) 上的标准 `n-4` 实例，或 AWS 上相当的机器类型）中，三成员 etcd 集群在轻负载下请求完成时间小于 1 毫秒，重负载下每秒可完成超过 30,000 次请求。

etcd 使用 Raft 共识算法在成员之间复制请求并达成一致。共识性能，尤其是提交延迟，受限于两个物理因素：网络 I/O 延迟和磁盘 I/O 延迟。完成一次 etcd 请求所需的最短时间，是成员之间的网络往返时间（RTT），加上 `fdatasync` 将数据提交至持久存储所需的时间。数据中心内部的 RTT 可能长达数百微秒。美国境内的典型 RTT 约为 50ms，跨洲际的 RTT 可能慢至 400ms。传统旋转磁盘的典型 fdatasync 延迟约为 10ms。对于 SSD，延迟通常低于 1ms。为提升吞吐量，etcd 将多个请求批量处理并提交至 Raft。该批处理策略使 etcd 即便在高负载下也能实现高吞吐量。

其他子系统也会影响 etcd 的整体性能。每个序列化的 etcd 请求都必须经过基于 boltdb 的 MVCC 存储引擎处理，通常需要数十微秒完成。etcd 会周期性地对其最近应用的请求进行增量快照，并将其与之前的磁盘快照合并。此过程可能导致延迟突增。尽管在 SSD 上通常不是问题，但在 HDD 上可能导致观测到的延迟翻倍。同样，正在进行的压缩操作也可能影响 etcd 的性能。幸运的是，影响通常不显著，因为压缩操作是分阶段执行的，不会与常规请求争用资源。gRPC 作为 RPC 系统，为 etcd 提供了定义明确且可扩展的 API，但也引入了额外延迟，尤其在本地读取时更为明显。

## 基准测试 {#benchmarks}

使用 etcd 自带的 [benchmark](https://github.com/etcd-io/etcd/tree/main/tools/benchmark) 命令行工具可对 etcd 性能进行基准测试。

针对一些基准性能数据，我们以具有以下硬件配置的三成员 etcd 集群为例：

- Google Cloud Compute Engine
- 3 台 8 个 vCPU + 16GB 内存 + 50GB SSD 的机器
- 1 台客户端机器（16 个 vCPU + 30GB 内存 + 50GB SSD）
- Ubuntu 17.04
- etcd 3.2.0，go 1.8.3

使用此配置时，etcd 大约可写入：

| 键数量 | 键大小（字节） | 值大小（字节） | 连接数 | 客户端数 | 目标 etcd 服务器 | 平均写入 QPS | 平均每次请求延迟 | 平均服务器 RSS |
|---------------:|------------------:|--------------------:|----------------------:|------------------:|--------------------|------------------:|----------------------------:|-------------------:|
| 10,000 | 8 | 256 | 1 | 1 | 仅领导者 | 583 | 1.6ms | 48 MB |
| 100,000 | 8 | 256 | 100 | 1000 | 仅领导者 | 44,341 | 22ms | 124 MB |
| 100,000 | 8 | 256 | 100 | 1000 | 所有成员 | 50,104 | 20ms | 126 MB |

示例命令如下：

```sh
# write to leader
benchmark --endpoints=${HOST_1} --target-leader --conns=1 --clients=1 \
    put --key-size=8 --sequential-keys --total=10000 --val-size=256
benchmark --endpoints=${HOST_1} --target-leader  --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256

# write to all members
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256
```

线性一致读取请求需通过集群成员的法定人数达成共识，以获取最新数据。可串行化读取比线性一致读取成本更低，因为其可由任意单个 etcd 成员提供服务，而非需经过成员法定人数，但可能提供过时数据作为代价。etcd 可执行以下读取操作：

| 请求次数 | 键大小（字节） | 值大小（字节） | 连接数 | 客户端数 | 线性一致性 | 平均读取 QPS | 每次请求的平均延迟 |
|-------------------:|------------------:|--------------------:|----------------------:|------------------:|-------------|-----------------:|----------------------------:|
| 10,000 | 8 | 256 | 1 | 1 | 线性一致 | 1,353 | 0.7ms |
| 10,000 | 8 | 256 | 1 | 1 | 可串行化 | 2,909 | 0.3ms |
| 100,000 | 8 | 256 | 100 | 1000 | 线性一致 | 141,578 | 5.5ms |
| 100,000 | 8 | 256 | 100 | 1000 | 可串行化 | 185,758 | 2.2ms |

示例命令如下：

```sh
# Single connection read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=l --total=10000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=s --total=10000

# Many concurrent read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=l --total=100000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=s --total=100000
```

建议在新环境中首次搭建 etcd 集群时运行基准测试，以确保集群达到足够的性能；集群延迟和吞吐量可能对环境的微小差异较为敏感。
