---
title: 如何在 etcd 集群中进行领导者选举
description: 通过 etcdctl 客户端开展领导者选举的步骤
weight: 900
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## 先决条件 {#prerequisites}

- 确保已安装 [`etcd`](/zh/etcd/install/) 和 [`etcdctl`](/zh/etcd/install/)。
- 检查 etcd 集群是否处于活跃状态。

## 进行领导者选举 {#conduct-leader-election}

`etcdctl` 命令用于在 etcd 集群中执行选举操作。该命令确保同一时间仅有一个客户端可成为领导者。

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### 选项 {#options}

- `--endpoints : $ENDPOINTS`

每个 etcd 集群成员的地址。

- `election-name` 字符串

用于选举的字符串标识符。所有竞争领导权的参与者必须使用相同的选举名称。

- `leader-name` 字符串

新领导者的提案值。

### 示例 {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
