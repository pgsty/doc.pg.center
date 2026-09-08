---
title: 将 etcd 从 2.3 升级到 3.0
weight: 6900
description: 升级 etcd 2.3 至 3.0 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
aliases: [/etcd/upgrades/upgrade_3_0/]
---

在一般情况下，从 etcd 2.3 升级到 3.0 可以实现零停机滚动升级：

- 逐一停止 etcd v2.3 进程，并替换为 etcd v3.0 进程
- 在所有 v3.0 进程运行后，集群即可使用 v3.0 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

#### 升级要求 {#upgrade-requirements}

要将现有的 etcd 部署升级至 3.0，运行中的集群版本必须为 2.3 或更高。若版本低于 2.3，请先升级至 [2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8)，再升级至 3.0。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。请在继续操作前，使用 `etcdctl cluster-health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

开始前，请先 [备份 etcd 数据目录](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。如果升级出现问题，可以使用此备份 [降级](#downgrade)回现有 etcd 版本。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.0 版本后，才认为集群已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及支持的功能。

#### 限制 {#limitations}

当集群总数据量超过 50MB 时，新升级的成员可能需要最多 2 分钟才能追上现有集群。可通过检查最近快照的大小来估算总数据量。换句话说，为确保安全，应在升级每个成员之间至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.0，则集群将升级至 v3.0，从该完成状态回退**不可行**。然而，若任一成员仍为 v2.3，则集群及其操作仍处于“v2.3”状态，此时可从该混合集群状态恢复至所有成员均使用 v2.3 etcd 二进制文件。

请备份所有 etcd 成员的数据目录 [，以便在集群完成升级后仍可执行降级操作](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。

### 升级流程 {#upgrade-procedure}

本示例详细说明如何升级运行在本地机器上的三成员 v2.3 etcd 集群。

#### 1. 检查升级要求。 {#1-check-upgrade-requirements}

集群是否健康且运行 v.2.3.x 版本？

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. 停止现有 etcd 进程 {#2-stop-the-existing-etcd-process}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

此时建议 [备份 etcd 数据目录](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)，以便在出现任何问题时能够回退。

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. 插入 etcd v3.0 二进制文件并启动新 etcd 进程 {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

新版 v3.0 etcd 将向集群发布其信息：

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

验证每个成员以及整个集群在使用新的 v3.0 etcd 二进制文件后是否均恢复正常状态：

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


升级后的成员将在整个集群完成升级前持续记录如下警告信息。这是预期行为，当所有 etcd 集群成员均升级至 v3.0 后，警告将停止出现。

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. 对所有其他成员重复步骤 2 至步骤 3 {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完成 {#5-finish}

所有成员升级完成后，集群将成功报告升级至 3.0：

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## 进一步考虑事项 {#further-considerations}

- etcdctl 环境变量已更新。如果 `ETCDCTL_API=2 etcdctl cluster-health` 运行正常但 `ETCDCTL_API=3 etcdctl endpoints health` 返回 `Error:  grpc: timed out when dialing`，请务必使用 [新的变量名](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl)。

## 已知问题 {#known-issues}

- etcd &lt; v3.1 在使用 Go &gt; v1.7 构建时无法正常工作。详情请参见 [Issue 6951](https://github.com/etcd-io/etcd/issues/6951)。
- 若 etcd 服务器日志中出现 `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.` 类似错误，请确保 etcd 为预构建版本，或使用以下组合构建：(etcd v3.1+ &amp; go v1.7+) 或 (etcd &lt;v3.1 &amp; go v1.6.x)。
- 在升级过程中向 v2.3 集群添加 v3 成员不被支持，可能引发 panic。详情请参见 [Issue 7249](https://github.com/etcd-io/etcd/issues/7429)。仅在 v3 迁移期间允许混合版本的 etcd 成员。完成升级前不得进行任何成员变更操作。

[etcd-contact]: https://groups.google.com/g/etcd-dev
