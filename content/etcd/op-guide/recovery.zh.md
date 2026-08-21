---
title: 灾难恢复
weight: 4275
description: etcd v3 快照与恢复功能
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/op-guide/recovery.md"
---

etcd 设计用于抵御机器故障。etcd 集群可自动从临时故障（例如机器重启）中恢复，并能容忍最多 *(N−1)/2* 个成员的永久性故障，适用于由 N 个成员组成的集群。当某个成员发生永久性故障（无论是硬件故障还是磁盘损坏）时，该成员将失去对集群的访问权限。若集群永久性丢失超过 *(N−1)/2* 个成员，则将发生灾难性故障，法定人数不可逆地丢失。一旦法定人数丢失，集群将无法达成共识，因而无法继续接受更新。

为从灾难性故障中恢复，etcd v3 提供了快照与恢复功能，可在不丢失 v3 键数据的情况下重建集群。如需恢复 v2 键，请参阅 [v2 管理指南][v2_recover]。

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## 键空间快照 {#snapshotting-the-keyspace}

恢复集群首先需要从 etcd 成员获取键空间的快照。快照可通过以下方式获取：使用 `etcdctl snapshot save` 命令从运行中的成员获取，或从 etcd 数据目录中复制 `member/snap/db` 文件。例如，以下命令将 `$ENDPOINT` 提供的键空间快照保存至文件 `snapshot.db`：

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

请注意，从 `member/snap/db` 文件获取快照可能会丢失尚未写入但已包含在 wal（预写日志）文件夹中的数据。

## 快照状态 {#status-of-a-snapshot}

要了解某个快照所包含的修订版本和哈希值，可以使用 `etcdutl snapshot status` 命令：

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## 恢复集群 {#restoring-a-cluster}

### 修订版本差异 {#revision-difference}

在恢复集群时，现有客户端可能会感知到修订版本倒退数百甚至数千个。这是因为特定快照仅包含截至其创建时刻的数据版本历史，而当前状态可能已向前推进得更远。

当使用 etcd 运行 Kubernetes 时，此问题尤为突出，控制器和操作员可能使用所谓的 `informers` 作为本地缓存，并通过监听机制获取更新通知。恢复到较早的修订版本可能无法正确刷新缓存，导致控制器出现不可预测且不一致的行为。

在从快照恢复的场景下，例如已知的监听 API 消费者、etcd 数据的本地缓存副本，或在一般情况下使用 Kubernetes 时，强烈建议使用以下“修订版本提升”方式进行恢复。

### 从快照恢复 {#restoring-from-snapshot}

要恢复集群，仅需一个快照“db”文件即可。使用 `etcdutl snapshot restore` 执行集群恢复时，会创建新的 etcd 数据目录；所有成员应使用相同的快照进行恢复。恢复操作会覆盖部分快照元数据（特别是成员 ID 和集群 ID）；成员将失去原有身份。此元数据覆盖可防止新成员意外加入现有集群。因此，要从快照启动集群，恢复操作必须启动一个新的逻辑集群。

简单的恢复操作可按如下方式执行：

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### 完整性检查 {#integrity-checks}

快照完整性可在恢复时选择性地进行验证。若快照是使用 `etcdctl snapshot save` 创建的，则会包含完整性哈希，该哈希由 `etcdutl snapshot restore` 进行校验。若快照是从数据目录复制的，则不包含完整性哈希，只能通过 `--skip-hash-check` 恢复。


### 使用修订版本恢复 {#restoring-with-revision-bump}

为确保恢复后修订版本永不递减，可提供 `--bump-revision` 选项。该选项接受一个 64 位整数，表示在快照当前修订版本基础上增加的修订版本数。由于每次向 etcd 写入都会使修订版本加一，因此只要 etcd 每秒写入次数少于 1500 次，即可通过增加 1'000'000'000 个修订版本来覆盖一周前的快照。

在 Kubernetes 控制器的上下文中，还应使用 `--mark-compacted` 标记所有修订版本，包括版本递增操作，以执行压缩。这可确保所有监听操作被终止，且 etcd 不再响应关于快照创建后发生的修订版本的请求——从而有效使 informer 缓存失效。

完整调用示例如下：

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### 使用更新后的成员信息恢复 {#restoring-with-updated-membership}

etcd 集群的成员信息存储在 etcd 自身中，并通过 Raft 共识算法进行维护。当完全失去法定人数时，应重新考虑新集群的组建位置和方式，例如在一组全新的成员上进行组建。

从快照恢复时，可直接将新的成员信息提供给数据存储，如下所示：

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

这确保了新构建的集群仅与具有指定令牌的其他已恢复成员连接，而不会连接到可能仍处于活跃状态的旧成员。

另一种做法是在启动 etcd 时提供 `--force-new-cluster`，在保留现有应用数据的同时覆盖集群成员关系。强烈不建议采用此方法；如果旧集群的其他成员仍在运行，etcd 将发生 panic。务必定期保存快照。


### 全流程示例 {#end-2-end-example}

使用以下命令从运行中的集群获取快照：

```sh
$ etcdctl snapshot save snapshot.db
```

接续上一示例，以下为三成员集群创建新的 etcd 数据目录（`m1.etcd`、`m2.etcd`、`m3.etcd`）：

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

接下来，使用新的数据目录启动 `etcd`：

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

现在，已恢复的 etcd 集群应已可用，并开始提供快照中的键空间服务。

从 etcd v3.6 开始，用户只能使用 `etcdctl` 将数据保存为快照，而必须使用 `etcdutl` 从快照恢复数据。若未指定 `--data-dir`，则默认 `--data-dir` 值为 `<name>.etcd`（其中 `<name>` 为 `--name` 的值）。例如，若未提供 `--data-dir`，且成员名称为 `m1`、`m2` 和 `m3`，则 `--data-dir` 目录分别为 `m1.etcd`、`m2.etcd` 和 `m3.etcd`。
