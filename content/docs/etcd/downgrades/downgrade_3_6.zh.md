---
title: 将 etcd 从 v3.6 降级到 v3.5
weight: 6650
description: 降级 etcd 3.6 至 3.5 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/downgrades/downgrade_3_6.md"
aliases: [/etcd/downgrades/downgrade_3_6/]
---

在一般情况下，从 etcd v3.6 降级到 v3.5 可以实现零停机、滚动降级：

- 逐一停止 etcd v3.6 进程，并替换为 etcd v3.5 进程
- 启用降级后，集群将不再支持 v3.6 中的新特性

开始 [降级](#downgrade-procedure)前，请阅读本指南其余内容并做好准备。

### 降级检查列表 {#downgrade-checklists}

v3.6 版本到 v3.5 版本的突出变更：

#### 不同标志 {#difference-in-flags}

如果在 v3.6 配置中使用了以下任一标志，请在降级至 v3.5 时确保移除、重命名或更改其默认值。

> [!NOTE]
> 本文的差异对比基于版本 v3.6.0 和 v3.5.18。实际差异取决于所用补丁版本，请先与 `diff <(etcd-3.6/bin/etcd -h | grep \\-\\-) <(etcd-3.5/bin/etcd -h | grep \\-\\-)` 核对。

```diff
# flags not available in v3.5
-etcd --discovery-token ''
-etcd --discovery-endpoints ''
-etcd --discovery-dial-timeout '2s'
-etcd --discovery-request-timeout '5s'
-etcd --discovery-keepalive-time '2s'
-etcd --discovery-keepalive-timeout '6s'
-etcd --discovery-insecure-transport 'true'
-etcd --discovery-insecure-skip-tls-verify 'false'
-etcd --discovery-cert ''
-etcd --discovery-key ''
-etcd --discovery-cacert ''
-etcd --discovery-user ''
-etcd --discovery-password ''
-etcd --feature-gates
-etcd --log-format

# same flag with different names
-etcd --bootstrap-defrag-threshold-megabytes
+etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --compaction-batch-limit
+etcd --experimental-compaction-batch-limit
-etcd --compact-hash-check-time
+etcd --experimental-compact-hash-check-time
-etcd --compaction-sleep-interval
+etcd --experimental-compaction-sleep-interval
-etcd --corrupt-check-time
+etcd --experimental-corrupt-check-time
-etcd --enable-distributed-tracing
+etcd --experimental-enable-distributed-tracing
-etcd --distributed-tracing-address
+etcd --experimental-distributed-tracing-address
-etcd --distributed-tracing-instance-id
+etcd --experimental-distributed-tracing-instance-id
-etcd --distributed-tracing-sampling-rate
+etcd --experimental-distributed-tracing-sampling-rate
-etcd --distributed-tracing-service-name
+etcd --experimental-distributed-tracing-service-name
-etcd --downgrade-check-time
+etcd --experimental-downgrade-check-time
-etcd --max-learners
+etcd --experimental-max-learners
-etcd --memory-mlock
+etcd --experimental-memory-mlock
-etcd --peer-skip-client-san-verification
+etcd --experimental-peer-skip-client-san-verification
-etcd --snapshot-catchup-entries
+etcd --experimental-snapshot-catchup-entries
-etcd --warning-apply-duration
+etcd --experimental-warning-apply-duration
-etcd --warning-unary-request-duration
+etcd --experimental-warning-unary-request-duration
-etcd --watch-progress-notify-interval
+etcd --experimental-watch-progress-notify-interval

# equivalent flags of v3.6 feature gates
-etcd --feature-gates=CompactHashCheck=true
+etcd --experimental-compact-hash-check-enabled=true
-etcd --feature-gates=InitialCorruptCheck=true
+etcd --experimental-enable-initial-corrupt-check=true
-etcd --feature-gates=LeaseCheckpoint=true
+etcd --experimental-enable-lease-checkpoint=true
-etcd --feature-gates=LeaseCheckpointPersist=true
+etcd --experimental-enable-lease-checkpoint-persist=true
-etcd --feature-gates=StopGRPCServiceOnDefrag=true
+etcd --experimental-stop-grpc-service-on-defrag=true
-etcd --feature-gates=TxnModeWriteWithSharedBuffer=false
+etcd --experimental-txn-mode-write-with-shared-buffer=false

# same flag different defaults
-etcd --snapshot-count=10000
+etcd --snapshot-count=100000
-etcd --v2-deprecation='write-only'
+etcd --v2-deprecation='not-yet'
-etcd --discovery-fallback='exit'
+etcd --discovery-fallback='proxy'

```

#### Prometheus 指标差异 {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.5
-etcd_network_known_peers
-etcd_server_feature_enabled
```

### 服务器降级检查清单 {#server-downgrade-checklists}

#### 降级要求 {#downgrade-requirements}

为确保平滑的滚动降级，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在将 etcd 降级之前，务必在预发环境中测试依赖 etcd 的服务，确认无误后再将降级操作部署到生产环境。

在开始之前，[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。若降级过程中出现异常，可使用此备份对 [回滚](#rollback)至现有 etcd 版本。

在开始之前，请下载 etcd v3.5 的最新版本。

#### 混合版本 {#mixed-versions}

降级过程中，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。当通过 `etcdctl downgrade enable 3.5` 启用降级后，集群即被视为已降级。内部上，集群整体版本被设置为降级目标版本，该版本控制报告的版本号以及所支持的功能。

#### 回滚 {#rollback}

在降级 etcd 集群之前，请创建并 [下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。该快照可用于在需要时将集群恢复至升级前的状态。若用户在降级过程中遇到问题，应首先识别并解决根本原因。

如果降级操作在执行 `etcdctl downgrade enabled` 之后开始，且集群仍处于混合版本状态（即至少有一个成员仍运行在 v3.6 版本），用户可以通过执行 `etcdctl downgrade cancel` 取消正在进行的降级过程，并使用原始的 v3.6 二进制文件重启所有已降级的成员。

当所有成员均降级至 v3.5 版本后，集群即被视为已完全降级。若用户在完成完全降级后希望恢复至原始版本，应遵循官方 [升级指南](/zh/docs/etcd/upgrades/upgrade_3_6/)，以确保一致性并避免数据损坏。

### 降级操作 {#downgrade-procedure}

本示例演示如何将运行在本地机器上的 3 个成员 v3.6 etcd 集群降级。

#### 步骤 1: 检查降级要求 {#step-1-check-downgrade-requirements}

集群是否健康且运行 v3.6.x 版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Step 2: 从领导者下载快照备份 {#step-2-download-snapshot-backup-from-leader}

[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便在出现任何问题时提供回退路径。

#### 第 3 步：验证降级目标版本 {#step-3-validate-downgrade-target-version}

在启用降级前，验证降级目标版本：

- 仅支持逐次降级一个次版本。例如，不允许从 v3.6 降级至 v3.4。
- 请在验证成功前不要进行下一步操作。

```bash
etcdctl downgrade validate 3.5
<<COMMENT
Downgrade validate success, cluster version 3.6
COMMENT
```

#### 第 4 步：启用降级模式 {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.5
<<COMMENT
Downgrade enable success, cluster version 3.6
COMMENT
```

启用降级后，集群将开始使用 v3.5 协议运行，该版本即为降级目标版本。此外，etcd 会自动将模式迁移至降级目标版本，此过程通常非常迅速。在继续下一步之前，请通过检查端点状态确认所有服务器的存储版本均已迁移至 v3.5。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> 启用降级后，即使所有服务器仍在运行 v3.6 二进制文件，集群仍将以 v3.5 协议持续运行，除非使用 `etcdctl downgrade cancel` 取消降级。

#### 第 5 步：停止一个现有的 etcd 服务器 {#step-5-stop-one-existing-etcd-server}

在停止服务器之前，请检查其是否为领导者。建议最后再降级领导者。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

如果要停止的服务器是领导者，可以在停止该服务器之前通过 `move-leader` 将领导者转移至其他服务器，以减少停机时间。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```bash
{"level":"warn","ts":"2025-02-28T17:35:43.795069Z","caller":"etcdserver/cluster_util.go:259","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:43.795149Z","caller":"etcdserver/cluster_util.go:160","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368651Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"483.01µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368726Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_RAFT_MESSAGE","remote-peer-id":"8211f1d0f64f3269","rtt":"735.659µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### 第 6 步：使用相同配置重启 etcd 服务器（不包含 v3.5 中移除或替换的参数） {#step-6-restart-the-etcd-server-with-same-configuration-minus-the-flags-that-are-removed-or-replaced-in-v35}

使用相同配置但采用新 etcd 二进制文件重启 etcd 服务器。

```diff
-etcd-3.6/bin --name s1 \
+etcd-3.5/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

验证每个成员以及整个集群在使用新的 v3.5 etcd 二进制文件后是否恢复正常健康状态：

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |        3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
COMMENT
```

> [!NOTE]
> 在 v3.5 版本的服务器中，将看到 `DOWNGRADE ENABLED` 为 false，因为 v3.5 的状态端点尚未实现降级信息，此时集群的降级功能仍处于启用状态。

#### 第 7 步：重复第 5 步和第 6 步，直至所有成员完成 {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

当所有成员均降级后，请检查集群的健康状况和状态，并确认所有成员的次要版本均为 v3.5，且存储版本为空：

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT
```

在领导者的日志中，应能看到类似以下的消息：

```bash
{"level":"info","ts":"2025-02-28T17:59:50.019862Z","caller":"etcdserver/server.go:2749","msg":"the cluster has been downgraded","cluster-version":"3.5.0"}
```
