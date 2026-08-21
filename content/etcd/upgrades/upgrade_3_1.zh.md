---
title: 将 etcd 从 3.0 升级到 3.1
weight: 6850
description: 升级 etcd 3.0 至 3.1 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
---

在一般情况下，从 etcd 3.0 升级到 3.1 可以实现零停机滚动升级：

- 逐一停止 etcd v3.0 进程，并替换为 etcd v3.1 进程
- 在所有 v3.1 进程运行后，集群即可使用 v3.1 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

#### 监控 {#monitoring}

以下来自 v3.0.x 的指标已弃用，建议改用 [go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus)：

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 3.1 版本，运行中的集群版本必须为 3.0 或更高。若版本低于 3.0，请先 [升级至 3.0](/zh/etcd/upgrades/upgrade_3_0)，再升级至 3.1。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

升级前，请对 etcd 数据执行 [备份 etcd 数据](/zh/etcd/op-guide/maintenance/#snapshot-backup)。若升级过程中出现异常，可使用此备份将系统 [降级](#downgrade)至现有 etcd 版本。请注意，`snapshot`命令仅备份 v3 数据。如需备份 v2 数据，请参阅 [备份 v2 数据存储](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。

#### 混合版本 {#mixed-versions}

升级过程中，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.1 版本后，才认为集群已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本号以及所支持的功能。

#### 限制 {#limitations}

请注意：如果集群仅包含 v3 数据且无 v2 数据，则不受此限制影响。

如果集群正在服务的数据集大小超过 50MB，每个新升级的成员可能需要最多 2 分钟才能追上现有集群。请检查最近快照的大小以估算总数据量。换句话说，升级每个成员之间应至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.1 版本，集群将升级至 v3.1 版本，从该完成状态回退**不可行**。然而，若任一成员仍为 v3.0 版本，则集群及其操作仍保持 "v3.0" 状态，此时可从该混合集群状态恢复至所有成员均使用 v3.0 etcd 二进制文件。

请注意，务必对所有 etcd 成员的数据目录 [backup the data directory](/zh/etcd/op-guide/maintenance#snapshot-backup) 进行备份，以确保在集群完全升级后仍可执行降级操作。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.0 etcd 集群。

#### 1. 检查升级要求 {#1-check-upgrade-requirements}

集群是否健康且运行 v3.0.x 版本？

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. 停止现有 etcd 进程 {#2-stop-the-existing-etcd-process}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

此时建议 [备份 etcd 数据](/zh/etcd/op-guide/maintenance#snapshot-backup)，以便在出现任何问题时提供回退路径：

```
$ etcdctl snapshot save backup.db
```

#### 3. 直接替换 etcd v3.1 二进制文件并启动新 etcd 进程 {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

新版 v3.1 etcd 将向集群发布其信息：

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

验证每个成员以及整个集群在使用新的 v3.1 etcd 二进制文件后是否恢复正常健康状态：

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

升级后的成员将在整个集群完成升级前持续记录如下警告信息。这是预期行为，待所有 etcd 集群成员升级至 v3.1 后，警告将停止出现。

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. 对所有其他成员重复步骤 2 至步骤 3 {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完成 {#5-finish}

所有成员升级完成后，集群将成功报告升级至 3.1：

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
