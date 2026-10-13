---
title: 将 etcd 从 v3.6 升级到 v3.7
weight: 6550
description: 升级 etcd 3.6 至 3.7 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
aliases: [/etcd/upgrades/upgrade_3_7/]
---

在一般情况下，从 etcd v3.6 升级到 v3.7 可以实现零停机滚动升级：

- 逐一停止 etcd v3.6 进程，并替换为 etcd v3.7 进程
- 在所有 v3.7 进程运行后，集群即可使用 v3.7 中的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

#### 更新 3.6 {#update-36}

> [!IMPORTANT]
> 在升级到 3.7 之前，请确保所有 3.6 成员均已更新至 3.6.11 或更高版本。较早的 3.6 补丁版本可能与 3.7 的滚动升级不兼容。

#### V2 存储系统 {#v2-store}

v3.7 版本中已完全移除 v2 存储系统。v2 HTTP API（`--enable-v2`）、v2-on-v3 模拟层（`--experimental-enable-v2v3`）、v2 发现服务、`client/v2` 包，以及 v2 快照文件的加载功能均已不可用。请参阅 [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md) 中的破坏性变更说明。

如果从 3.6 版本集群升级，这些标志已不存在，无需采取任何操作。如果从包含自定义 v2 数据的旧版本升级，请在升级前遵循 [v2 迁移指南](https://etcd.io/docs/v3.4/op-guide/v2-migration/)。

#### Go 重构 {#go-refactoring}

v3.7 包含重大的内部重构，对正常升级流程无影响，但在升级自定义集成时值得留意：

- 从 `gogo/protobuf` 迁移到标准 `google.golang.org/protobuf`（跟踪于 [#14533](https://github.com/etcd-io/etcd/issues/14533)）。
- 已将已弃用的 `go-grpc-middleware` v1 日志和标签库迁移至 v2 拦截器（[#20420](https://github.com/etcd-io/etcd/pull/20420)）。
- OpenTelemetry gRPC 拦截器已更新至 `otelgrpc` v0.61.0，用 `NewServerHandler` 替代已弃用的 `UnaryServerInterceptor` 和 `StreamServerInterceptor`（[#20017](https://github.com/etcd-io/etcd/pull/20017)）。

如果将 etcd 作为库嵌入，或针对 `clientv3` API 进行构建，或依赖内部包，请在升级前查阅 [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md)。

### 已移除标志 {#flags-removed}

v3.7 版本已移除所有已弃用的 `--experimental-*` 标志（[#19959](https://github.com/etcd-io/etcd/pull/19959)）。在 v3.6 版本中，这些标志均已被同名的非实验性标志或 `--feature-gates` 条目替代。如果仍存在这些标志的设置，请务必在升级至 v3.7 **之前**，将其替换为 v3.6 对应的等效设置，否则 v3.7 进程将无法启动。

```diff
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-compact-hash-check-enabled
-etcd --experimental-compact-hash-check-time
-etcd --experimental-compaction-batch-limit
-etcd --experimental-compaction-sleep-interval
-etcd --experimental-corrupt-check-time
-etcd --experimental-distributed-tracing-address
-etcd --experimental-distributed-tracing-instance-id
-etcd --experimental-distributed-tracing-sampling-rate
-etcd --experimental-distributed-tracing-service-name
-etcd --experimental-downgrade-check-time
-etcd --experimental-enable-distributed-tracing
-etcd --experimental-enable-lease-checkpoint
-etcd --experimental-enable-lease-checkpoint-persist
-etcd --experimental-initial-corrupt-check
-etcd --experimental-memory-mlock
-etcd --experimental-peer-skip-client-san-verification
-etcd --experimental-snapshot-catchup-entries
-etcd --experimental-stop-grpc-service-on-defrag
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-warning-apply-duration
-etcd --experimental-warning-unary-request-duration
-etcd --experimental-watch-progress-notify-interval
```

请参阅 [v3.5 到 v3.6 升级指南](/zh/docs/etcd/upgrades/upgrade_3_6/)，以获取每个已移除标志与其非实验性等效标志或 `--feature-gates` 条目的映射关系。

### 新增标志 {#flags-added}

无。

### 带有新默认值的标志 {#flags-with-new-defaults}

无。

### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 v3.7，运行中的集群必须为 v3.6.11 或更高版本。若当前为较旧的次版本，请先 [升级至 v3.6](/zh/docs/etcd/upgrades/upgrade_3_6/)；etcd 仅支持一次升级一个次版本。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

开始之前，[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。若升级过程中出现异常，可使用此备份 [回滚](#rollback)至现有 etcd 版本。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 v3.7 版本后，该集群才被视为已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及所支持的功能。

#### 回滚 {#rollback}

升级 etcd 集群前，请创建并 [下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。该快照可用于在需要时将集群恢复至升级前的状态。若用户在升级过程中遇到问题，应首先识别并解决根本原因。若集群仍处于混合版本状态（即至少有一个成员仍运行在 v3.6 版本），可选择将二进制文件或镜像替换为旧版 v3.6 版本，或直接使用快照恢复集群。在此混合状态下，集群仍以 v3.6 版本运行，支持回滚而无需执行正式的降级流程。

然而，一旦所有成员均升级至 v3.7 版本，集群即被视为已完全升级，此时使用二进制文件回滚将不再可行。在此情况下，唯一的恢复选项为从升级前的快照进行恢复，或在升级失败时遵循官方 [降级指南](/zh/docs/etcd/downgrades/downgrading-etcd/)。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地主机上运行的 3 个成员的 v3.6 etcd 集群。以下输出来自在单个主机上使用三个环回端口对 etcd v3.6.12 和 etcd v3.7.0-rc.0 的实际运行结果。

#### 第 1 步：检查升级要求 {#step-1-check-upgrade-requirements}

集群是否健康且运行 v3.6.11 或更高版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 7.681459ms
localhost:22379 is healthy: successfully committed proposal: took = 7.691750ms
localhost:32379 is healthy: successfully committed proposal: took = 7.698000ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.12","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

#### 第 2 步：从领导者下载快照备份 {#step-2-download-snapshot-backup-from-leader}

[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便在出现任何问题时提供回退路径。

etcd 领导者保证拥有最新的应用数据，因此应从领导者获取快照：

```bash
for p in 2379 22379 32379; do
  echo -n "localhost:$p leader="
  curl -sL http://localhost:$p/metrics | grep "^etcd_server_is_leader " | awk '{print $2}'
done
<<COMMENT
localhost:2379 leader=1
localhost:22379 leader=0
localhost:32379 leader=0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-06-02T07:01:41.863225+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-06-02T07:01:41.866451+0300","logger":"client","caller":"v3@v3.6.12/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-06-02T07:01:41.874080+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-06-02T07:01:41.877203+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"13.822583ms","etcd-version":"3.6.0"}
{"level":"info","ts":"2026-06-02T07:01:41.877303+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.6.0
COMMENT
```

#### 第 3 步：停止一个现有的 etcd 服务器 {#step-3-stop-one-existing-etcd-server}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误日志。这是正常的，因为集群成员之间的连接已（暂时）中断。领导者将在退出前转移领导权：

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
```

#### 第 4 步：使用相同配置重启 etcd 服务器 {#step-4-restart-the-etcd-server-with-same-configuration}

使用相同配置但采用新 etcd 二进制文件重启 etcd 服务器。

```diff
-etcd-old --name ${name} \
+etcd-new --name ${name} \
  --data-dir /path/to/${name}.etcd \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

新的 v3.7 etcd 将向集群发布其信息。此时，集群仍以 v3.6 协议运行，该版本为最低公共版本。

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

验证每个成员以及整个集群在使用新的 v3.7 etcd 二进制文件后是否恢复正常健康状态：

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | LEADER | RAFT TERM |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  false |         3 |
| localhost:22379 | 729934363faa4a24 |     3.6.12 |           3.6.0 |   98 kB |  false |         3 |
| localhost:32379 |  b548c2511513015 |     3.6.12 |           3.6.0 |   98 kB |   true |         3 |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
COMMENT
```

未升级的成员和已升级的成员将持续记录关于混合版本状态的日志，直到整个集群完成升级。这是预期行为，当所有 etcd 集群成员均升级至 v3.7 后，日志将停止。

#### 第 5 步：重复第 3 步和第 4 步，对剩余的成员进行操作 {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

所有成员升级完成后，集群将成功报告升级至 v3.7：

> `{"level":"info","ts":"2026-06-02T07:02:36.054783+0300","caller":"etcdserver/server.go:2311","msg":"updating cluster version using v3 API","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059345+0300","caller":"membership/cluster.go:593","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059409+0300","caller":"etcdserver/server.go:2326","msg":"cluster version is updated","cluster-version":"3.7"}`

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 550.833µs
localhost:32379 is healthy: successfully committed proposal: took = 733.458µs
localhost:22379 is healthy: successfully committed proposal: took = 714.416µs
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT
```
