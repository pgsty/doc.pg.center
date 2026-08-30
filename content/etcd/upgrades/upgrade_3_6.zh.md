---
title: 将 etcd 从 v3.5 升级到 v3.6
weight: 6600
description: 升级 etcd 3.5 至 3.6 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
---

在一般情况下，从 etcd v3.5 升级到 v3.6 可以实现零停机时间的滚动升级：

- 逐一停止 etcd v3.5 进程，并替换为 etcd v3.6 进程
- 所有 v3.6 进程运行后，集群即可使用 v3.6 中的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

#### 更新 3.5 {#update-35}

> [!IMPORTANT]
> 升级至 3.6 之前，请确保 [所有 3.5 版本的成员均已更新至 3.5.32 或更高版本](https://etcd.io/blog/2026/july-patch-release/)。补丁版本 3.5.24 至 3.5.26 修复了多个潜在的升级障碍；[3.5.32](https://etcd.io/blog/2026/july-patch-release/) 增加了 `--v2-deprecation=write-only-skip-check` 功能，并将 `etcdutl check v2store` 扩展至可检查 WAL 记录以及 v2 快照。

#### V2 存储系统 {#v2-store}

> [!NOTE]
> 如果未配置 `--enable-v2` 标志或将其设置为 false，则无需采取进一步操作。

如果配置了 `--enable-v2`，请运行命令 `etcdutl check v2store`，以验证 v2store 中是否存在非成员关系（自定义）数据。若不存在自定义数据，可安全移除该标志。否则，请参阅 [v2 迁移指南](https://etcd.io/docs/v3.4/op-guide/v2-migration/) 获取更多详情。

### 新增标志 {#flags-added}

```diff
+etcd --discovery-token ''
+etcd --discovery-endpoints ''
+etcd --discovery-dial-timeout '2s'
+etcd --discovery-request-timeout '5s'
+etcd --discovery-keepalive-time '2s'
+etcd --discovery-keepalive-timeout '6s'
+etcd --discovery-insecure-transport 'true'
+etcd --discovery-insecure-skip-tls-verify 'false'
+etcd --discovery-cert ''
+etcd --discovery-key ''
+etcd --discovery-cacert ''
+etcd --discovery-user ''
+etcd --discovery-password ''
+etcd --feature-gates
+etcd --log-format
```

### 已移除标志 {#flags-removed}

```diff
-etcd --enable-v2
-etcd --experimental-enable-v2v3
-etcd --proxy
-etcd --proxy-failure-wait
-etcd --proxy-refresh-interval
-etcd --proxy-dial-timeout
-etcd --proxy-write-timeout
-etcd --proxy-read-timeout
```

### 标志已弃用 {#flags-deprecated}

**`etcd --experimental-bootstrap-defrag-threshold-megabytes` 标志已被弃用.**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**`etcd --experimental-compaction-batch-limit` 标志已被弃用.**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**`etcd --experimental-compact-hash-check-time` 标志已被弃用.**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**`etcd --experimental-compaction-sleep-interval` 标志已被弃用.**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**`etcd --experimental-corrupt-check-time` 标志已被弃用.**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**`etcd --experimental-enable-distributed-tracing` 标志已弃用.**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**`etcd --experimental-distributed-tracing-address` 标志已被弃用.**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**`etcd --experimental-distributed-tracing-instance-id` 标志已弃用.**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**`etcd --experimental-distributed-tracing-sampling-rate` 标志已被弃用.**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**`etcd --experimental-distributed-tracing-service-name` 标志已弃用.**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**`etcd --experimental-downgrade-check-time` 标志已被弃用.**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**`etcd --experimental-max-learners` 标志已被弃用.**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**`etcd --experimental-memory-mlock` 标志已被弃用.**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**`etcd --experimental-peer-skip-client-san-verification` 标志已被弃用.**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**`etcd --experimental-snapshot-catchup-entries` 标志已被弃用.**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**`etcd --experimental-warning-apply-duration` 标志已弃用.**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**`etcd --experimental-warning-unary-request-duration` 标志已被弃用.**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**`etcd --experimental-watch-progress-notify-interval` 标志已被弃用.**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### v3.5 功能门控的等效标志 {#equivalent-flags-of-v35-feature-gates}

**对应的功能门控标志 `etcd --experimental-compact-hash-check-enabled=true`**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**对应的功能门控标志 `etcd --experimental-initial-corrupt-check=true`**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**对应的功能门控标志 `etcd --experimental-enable-lease-checkpoint=true`**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**对应的功能门控标志 `etcd --experimental-enable-lease-checkpoint-persist=true`**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**对应的功能门控标志 `etcd --experimental-stop-grpc-service-on-defrag=true`**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**对应的功能门控标志 `etcd --experimental-txn-mode-write-with-shared-buffer=false`**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### 带有新默认值的标志 {#flags-with-new-defaults}

**原始默认标志 `etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**原始默认标志 `etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**原始默认标志 `etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### Prometheus 指标差异 {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有的 etcd 部署升级至 v3.6，运行中的集群版本必须为 v3.5 或更高。若版本低于 v3.5，请先 [升级至 v3.5](/zh/etcd/upgrades/upgrade_3_4/)，再升级至 v3.6。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

开始前，请先 [下载快照备份](/zh/etcd/op-guide/maintenance/#snapshot-backup)。如果升级出现问题，可以使用此备份 [回滚](#rollback)到现有 etcd 版本。请注意，`snapshot` 命令只备份 v3 数据。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 v3.6 版本后，才认为集群已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及支持的功能。

#### 回滚 {#rollback}

升级 etcd 集群前，请创建并 [下载快照备份](/zh/etcd/op-guide/maintenance/#snapshot-backup)。该快照可用于在需要时将集群恢复至升级前的状态。若用户在升级过程中遇到问题，应首先识别并解决根本原因。若集群仍处于混合版本状态——即至少有一个成员仍运行在 v3.5 版本——则可选择将二进制文件或镜像替换为旧版 v3.5，或直接使用快照恢复集群。在此混合状态下，集群仍以 v3.5 集群模式运行，支持回滚而无需执行正式的降级流程。

然而，一旦所有成员均升级至 v3.6 版本，集群即被视为已完全升级，此时使用二进制文件回滚将不再可行。在此情况下，唯一的恢复方式是恢复升级前创建的快照。若用户希望在完成完整升级后返回原始版本，应遵循官方降级指南，以确保一致性并避免数据损坏。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.5 etcd 集群。

#### 步骤 1: 检查升级要求 {#step-1-check-upgrade-requirements}

集群是否健康且运行 v3.5.x 版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.555774ms
localhost:32379 is healthy: successfully committed proposal: took = 2.631133ms
localhost:22379 is healthy: successfully committed proposal: took = 3.020958ms
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

#### Step 2: 从领导者下载快照备份 {#step-2-download-snapshot-backup-from-leader}

[下载快照备份](/zh/etcd/op-guide/maintenance/#snapshot-backup)，以便在出现任何问题时提供回退路径。

etcd 领导者保证拥有最新的应用数据，因此应从领导者获取快照：

```bash
curl -sL http://localhost:2379/metrics | grep etcd_server_is_leader
<<COMMENT
# HELP etcd_server_is_leader Whether or not this member is a leader. 1 if is, 0 otherwise.
# TYPE etcd_server_is_leader gauge
etcd_server_is_leader 1
COMMENT

curl -sL http://localhost:22379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

curl -sL http://localhost:32379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### 第 3 步：停止一个现有的 etcd 服务器 {#step-3-stop-one-existing-etcd-server}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```bash
{"level":"info","ts":"2025-03-01T04:31:50.654520+0530","caller":"etcdserver/server.go:2676","msg":"cluster version is updated","cluster-version":"3.5"}
{"level":"info","ts":"2025-03-01T04:34:10.345927+0530","caller":"v3rpc/maintenance.go:130","msg":"sending database snapshot to client","total-bytes":20480,"size":"20 kB"}
{"level":"info","ts":"2025-03-01T04:34:10.346094+0530","caller":"v3rpc/maintenance.go:170","msg":"sending database sha256 checksum to client","total-bytes":20480,"checksum-size":32}
{"level":"info","ts":"2025-03-01T04:34:10.346108+0530","caller":"v3rpc/maintenance.go:179","msg":"successfully sent database snapshot to client","total-bytes":20480,"size":"20 kB","took":"now"}
^C
{"level":"info","ts":"2025-03-01T04:35:01.443045+0530","caller":"osutil/interrupt_unix.go:64","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":"2025-03-01T04:35:01.443088+0530","caller":"embed/etcd.go:408","msg":"closing etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
{"level":"info","ts":"2025-03-01T04:35:01.443417+0530","caller":"etcdserver/server.go:1503","msg":"leadership transfer starting","local-member-id":"bf9071f4639c75cc","current-leader-member-id":"bf9071f4639c75cc","transferee-member-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443441+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term 2] starts to transfer leadership to 91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443455+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc sends MsgTimeoutNow to 91bc3c398fb3c146 immediately as 91bc3c398fb3c146 already has up-to-date log"}
{"level":"warn","ts":"2025-03-01T04:35:01.443517+0530","caller":"embed/serve.go:179","msg":"stopping insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"warn","ts":"2025-03-01T04:35:01.443548+0530","caller":"embed/serve.go:181","msg":"stopped insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"info","ts":"2025-03-01T04:35:01.445536+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term: 2] received a MsgVote message with higher term from 91bc3c398fb3c146 [term: 3]"}
{"level":"info","ts":"2025-03-01T04:35:01.445556+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc became follower at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445565+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [logterm: 2, index: 12, vote: 0] cast MsgVote for 91bc3c398fb3c146 [logterm: 2, index: 12] at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445572+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc lost leader bf9071f4639c75cc at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.446773+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc elected leader 91bc3c398fb3c146 at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.544062+0530","caller":"etcdserver/server.go:1520","msg":"leadership transfer finished","local-member-id":"bf9071f4639c75cc","old-leader-member-id":"bf9071f4639c75cc","new-leader-member-id":"91bc3c398fb3c146","took":"100.640374ms"}
{"level":"info","ts":"2025-03-01T04:35:01.544160+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.544956+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.544984+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545050+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545065+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545099+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545156+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545178+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"91bc3c398fb3c146","error":"failed to read 91bc3c398fb3c146 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545199+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545246+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545263+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545272+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545282+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545307+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545328+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545359+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545379+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545410+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545467+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545485+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"fd422379fda50e48","error":"failed to read fd422379fda50e48 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545504+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545560+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545577+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545592+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545669+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545698+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545732+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545765+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"info","ts":"2025-03-01T04:35:01.549658+0530","caller":"embed/etcd.go:613","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550532+0530","caller":"embed/etcd.go:618","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550561+0530","caller":"embed/etcd.go:410","msg":"closed etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
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

新的 v3.6 etcd 将向集群发布其信息。此时，集群仍以 v3.5 协议运行，该版本为最低公共版本。

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

验证每个成员以及整个集群在使用新的 v3.6 etcd 二进制文件后是否恢复正常健康状态：

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

未升级的成员将持续记录如下警告，直至整个集群完成升级。

这是预期行为，当所有 etcd 集群成员都升级到 v3.6 后，该现象将停止。

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### 第 5 步：重复第 3 步和第 4 步，对剩余的成员进行操作 {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

所有成员升级完成后，集群将成功报告升级至 v3.6：

成员 1：

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

成员 2：

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

成员 3：

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"fd422379fda50e48","from":"3.5","to":"3.6"}`

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT
```
