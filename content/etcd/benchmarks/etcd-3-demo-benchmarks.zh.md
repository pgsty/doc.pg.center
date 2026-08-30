---
title: etcd v3 基准测试
weight: 5375
description: etcd v3 性能指标
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
---

## 物理机 {#physical-machines}

GCE n1-highcpu-2 机器类型

- 1x 专用本地 SSD，挂载于 /var/lib/etcd
- 1x 专用慢速磁盘，用于操作系统
- 1.8 GB 内存
- 2x CPU
- etcd 版本 2.2.0

## etcd 集群 {#etcd-cluster}

1 以 v3 演示模式运行的 etcd 成员

## 测试 {#testing}

使用 [etcd v3 基准测试工具][etcd-v3-benchmark]。

## 性能 {#performance}

### 读取单一键 {#reading-one-single-key}

| 键大小（字节） | 客户端数量 | 读取 QPS | 第 90 百分位延迟（毫秒） |
|----------------|------------|----------|------------------------|
| 256            | 1          | 2716     | 0.4                    |
| 256            | 64         | 16623    | 6.1                    |
| 256            | 256        | 16622    | 21.7                   |

性能几乎与空服务器处理器的情况相同。

### 读取单个键的操作 {#reading-one-single-key-after-putting}

| 键大小（字节） | 客户端数量 | 读取 QPS | 第 90 百分位延迟（毫秒） |
|----------------|------------|----------|------------------------|
| 256            | 1          | 2269     | 0.5                    |
| 256            | 64         | 13582    | 8.6                    |
| 256            | 256        | 13262    | 47.5                   |

空服务器处理器的性能不受单次写入操作影响。因此，性能下降应由存储系统导致。

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
