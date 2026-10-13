---
title: 将 etcd 从 v3.7 降级到 v3.6
weight: 6600
description: 降级 etcd 3.7 至 3.6 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
aliases: [/etcd/downgrades/downgrade_3_7/]
---

在一般情况下，从 etcd v3.7 降级到 v3.6 可以实现零停机、滚动降级：

- 逐一停止 etcd v3.7 进程，并替换为 etcd v3.6 进程
- 启用降级后，集群将不再支持 v3.7 中的新特性

开始 [降级](#downgrade-procedure)前，请阅读本指南其余内容并做好准备。

### 降级检查列表 {#downgrade-checklists}

v3.7 与 v3.6 之间的主要差异：

#### 不同标志 {#difference-in-flags}

v3.7 未引入任何新标志，因此 v3.6 进程可接受 v3.7 配置中的所有标志，降级时无需进行配置更改。

> [!NOTE]
> 本次差异对比基于版本 v3.7.0-rc.0 与 v3.6.13。实际差异取决于所用补丁版本，请先查阅 `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`。

在 v3.7 中已移除的弃用标志 `--experimental-*` 在 v3.6 中仍存在，但降级后不得重新添加；应使用其非实验性等效标志或 `--feature-gates` 条目，两者在两个版本中均有效。

#### Prometheus 指标差异 {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### 服务器降级检查清单 {#server-downgrade-checklists}

#### 降级要求 {#downgrade-requirements}

为确保平滑的滚动降级，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在将 etcd 降级之前，务必在预发环境中测试依赖 etcd 的服务，确认无误后再将降级操作部署到生产环境。

在开始之前，[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。若降级过程中出现异常，可使用此备份[回滚](#rollback)至现有 etcd 版本。

在开始之前，请下载 etcd v3.6 的最新版本。

#### 混合版本 {#mixed-versions}

降级过程中，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。当通过 `etcdctl downgrade enable 3.6` 启用降级后，集群即被视为已降级。内部上，集群整体版本被设置为降级目标版本，该版本控制报告的版本号以及所支持的功能。

#### 回滚 {#rollback}

在降级 etcd 集群之前，请创建并 [下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。如需恢复集群至降级前的状态，可使用该快照。若用户在降级过程中遇到问题，应首先识别并解决根本原因。

如果降级操作在执行 `etcdctl downgrade enable` 之后开始，且集群仍处于混合版本状态（即至少有一个成员仍运行在 v3.7 版本），用户可以通过执行 `etcdctl downgrade cancel` 取消正在进行的降级过程，并使用原始的 v3.7 二进制文件重启所有已降级的成员。

当所有成员均降级至 v3.6 版本后，集群即被视为已完全降级。若用户在完成完全降级后希望恢复至原始版本，应遵循官方 [升级指南](/zh/docs/etcd/upgrades/upgrade_3_7/)，以确保一致性并避免数据损坏。

### 降级操作 {#downgrade-procedure}

本示例演示如何将运行在本地机器上的 3 个成员 v3.7 etcd 集群降级。以下输出来自在单个主机上使用三个环回端口，对 v3.7.0-rc.0 和 v3.6.13 版本的 etcd 执行的实际运行，该集群在不久之前从 v3.6.13 升级而来。

#### 第 1 步：检查降级要求 {#step-1-check-downgrade-requirements}

集群是否健康且运行 v3.7.x 版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
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

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### 第 2 步：从领导者下载快照备份 {#step-2-download-snapshot-backup-from-leader}

[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便出现问题时回退本次降级、恢复到降级前的状态：

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### 第 3 步：验证降级目标版本 {#step-3-validate-downgrade-target-version}

在启用降级前，验证降级目标版本：

- 我们仅支持逐次降级一个次版本。例如，不允许从 v3.7 降级到 v3.5。
- 请在验证成功前不要进行下一步操作。

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### 第 4 步：启用降级模式 {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

启用降级后，集群将开始使用 v3.6 协议运行，该版本即为降级目标版本。此外，etcd 会自动将存储模式（schema）迁移至降级目标版本，此过程通常非常迅速。在继续下一步之前，请通过检查端点状态确认所有服务器的存储版本均已迁移至 v3.6。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> 启用降级后，即使所有服务器仍在运行 v3.7 二进制文件，集群仍将继续使用 v3.6 协议运行，除非使用 `etcdctl downgrade cancel` 取消降级。

#### 第 5 步：停止一个现有的 etcd 服务器 {#step-5-stop-one-existing-etcd-server}

在停止服务器之前，请检查其是否为领导者。我们建议最后再降级领导者。如果要停止的服务器是领导者，可以在停止该服务器前通过 `move-leader` 将领导者角色转移至其他服务器，以减少停机时间。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### 第 6 步：使用相同配置重启 etcd 服务器 {#step-6-restart-the-etcd-server-with-same-configuration}

使用相同配置，但以 v3.6 版本的 etcd 二进制文件重启 etcd 服务器。

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

验证每个成员以及整个集群在使用 v3.6 etcd 二进制文件后是否恢复正常状态：

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> 与 v3.5 不同，v3.6 的状态端点会报告降级信息，因此已降级的成员会持续显示 `DOWNGRADE ENABLED` 为 true 以及其存储版本，直至降级完成。

#### 第 7 步：重复第 5 步和第 6 步，直至所有成员完成 {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

当所有成员均完成降级后，降级操作将自动完成，`DOWNGRADE ENABLED` 被重置为 false。检查集群的健康状况和状态，确认所有成员的次版本以及存储版本均为 v3.6：

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

在领导者的日志中，应能看到类似以下的消息：

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
