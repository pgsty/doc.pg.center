---
title: etcd v2.2.0-rc 内存基准测试
weight: 5500
description: etcd v2.2.0-rc-memory 的性能指标
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-memory-benchmarks.md"
---

## 物理机 {#physical-machine}

GCE n1-standard-2 机器类型

- 1 个专用本地 SSD，挂载于 /var/lib/etcd
- 1 个专用慢速磁盘，用于操作系统
- 7.5 GB 内存
- 2 个 CPU

## etcd {#etcd}

```
etcd Version: 2.2.0-rc.0+git
Git SHA: 103cb5c
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## 测试 {#testing}

启动一个由 3 个成员组成的 etcd 集群，每个成员使用 2 个核心。

键名的长度始终为 64 字节，这是一个合理的平均键名长度。

## 内存最大使用量 {#memory-maximal-usage}

- 当一个跟随者失效而领导者持续发送快照时，etcd 可能会使用最大内存。
- `max RSS` 是在三次运行中记录的最大内存使用量。

| 值大小（字节） | 键数量 | 数据大小（MB） | 最大 RSS（MB） | 领导者最大 RSS/数据比 |
|----------|--------|----------------|----------------|------------------------|
| 128      | 50000  | 6              | 433            | 72x                    |
| 128      | 100000 | 12             | 659            | 54x                    |
| 128      | 200000 | 24             | 1466           | 61x                    |
| 1024     | 50000  | 48             | 1253           | 26x                    |
| 1024     | 100000 | 96             | 2344           | 24x                    |
| 1024     | 200000 | 192            | 4361           | 22x                    |

## 数据大小阈值 {#data-size-threshold}

- 当 etcd 达到数据大小阈值时，可能容易触发领导者选举，并丢弃部分提案。
- 对于大多数情况，只要 etcd 集群未触及该阈值，即可正常运行。若因资源不足导致运行不佳，应减小其数据规模。

| 值大小（字节） | 键数量限制 | 建议数据大小阈值（MB） | 消耗的 RSS（MB） |
|---------------|------------|------------------------|------------------|
| 128           | 400K       | 48                     | 2400             |
| 1024          | 300K       | 292                    | 6500             |
