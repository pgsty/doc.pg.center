---
title: 将 etcd 从 3.4 升级到 3.5
weight: 6650
description: 升级 etcd 3.4 至 3.5 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
aliases: [/etcd/upgrades/upgrade_3_5/]
---

在一般情况下，从 etcd 3.4 升级到 3.5 可以实现零停机滚动升级：

- 逐一停止 etcd v3.4 进程，并替换为 etcd v3.5 进程
- 在所有 v3.5 进程运行后，集群即可使用 v3.5 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。



### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

> [!WARNING]
> 如果集群启用了认证，将无法执行从 3.4 或更早版本的滚动升级，因为 3.5 [更改了与认证相关的 WAL 条目格式](https://github.com/etcd-io/etcd/pull/11943)。

3.5 版本中的重点变更。

#### 已弃用 `etcd_debugging_mvcc_db_total_size_in_bytes` Prometheus 指标 {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.5 将 `etcd_debugging_mvcc_db_total_size_in_bytes` 的 Prometheus 指标提升至 `etcd_mvcc_db_total_size_in_bytes`，以鼓励对 etcd 存储进行监控。v3.5 完全弃用了 `etcd_debugging_mvcc_db_total_size_in_bytes`。

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 已弃用 `etcd_debugging_mvcc_put_total` Prometheus 指标 {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.5 将 `etcd_debugging_mvcc_put_total` 的 Prometheus 指标提升至 `etcd_mvcc_put_total`，以鼓励对 etcd 存储进行监控。v3.5 完全弃用了 `etcd_debugging_mvcc_put_total`。

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 已弃用 `etcd_debugging_mvcc_delete_total` Prometheus 指标 {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.5 将 `etcd_debugging_mvcc_delete_total` 的 Prometheus 指标提升至 `etcd_mvcc_delete_total`，以鼓励对 etcd 存储进行监控。v3.5 完全弃用了 `etcd_debugging_mvcc_delete_total`。

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 已弃用 `etcd_debugging_mvcc_txn_total` Prometheus 指标 {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.5 将 `etcd_debugging_mvcc_txn_total` 的 Prometheus 指标提升至 `etcd_mvcc_txn_total`，以鼓励对 etcd 存储进行监控。v3.5 完全弃用了 `etcd_debugging_mvcc_txn_total`。

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 已弃用 `etcd_debugging_mvcc_range_total` Prometheus 指标 {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.5 将 `etcd_debugging_mvcc_range_total` Prometheus 指标提升至 `etcd_mvcc_range_total` 级别，以鼓励对 etcd 存储进行监控。v3.5 完全弃用了 `etcd_debugging_mvcc_range_total`。

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 已弃用 `etcd --logger capnslog` {#deprecated-etcd---logger-capnslog}

v3.4 默认使用 `--logger=zap`，以支持多日志输出和结构化日志。

`etcd --logger=capnslog` 在 v3.5 中已被弃用，现在 `--logger=zap` 为默认值。

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 增加 `etcd --logger=zap` 对结构化日志和多日志输出的支持。主要动机是推动 etcd 的自动化监控，而非在服务出现异常时回溯服务器日志。未来开发将尽量减少 etcd 的日志输出，并通过指标和告警使 etcd 更易于监控。**`etcd --logger=capnslog` 将在 v3.5 中弃用。**

#### 已弃用 `etcd --log-output` {#deprecated-etcd---log-output}

v3.4 将 [`etcd --log-output` 重命名为 `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624)，以支持多日志输出。

**`etcd --log-output` 已在 v3.5 中弃用.**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### 已弃用 `etcd --debug` 标志（现已 `--log-level=debug`） {#deprecated-etcd---debug-flag-now---log-leveldebug}

**`etcd --debug` 标志已弃用.**

```diff
-etcd --debug
+etcd --log-level debug
```

#### 已弃用 `etcd --log-package-levels` {#deprecated-etcd---log-package-levels}

**`etcd --log-package-levels` 标志在 `capnslog` 中已弃用.**

现在，**`etcd --logger=zap`** 为默认值。

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### 已弃用 `[CLIENT-URL]/config/local/log` {#deprecated-client-urlconfiglocallog}

**`/config/local/log` 端点在 v3.5 中正在被弃用，同时 `etcd --log-package-levels` 标志也将被弃用.**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### 变更 gRPC 网关 HTTP 端点（已弃用 `/v3beta`） {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

本文未提供内容。

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

之后

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3beta` 已在 3.5 版本中移除。



### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 3.5 版本，运行中的集群版本必须为 3.4 或更高。若版本低于 3.4，请先 [升级至 3.4](/zh/docs/etcd/upgrades/upgrade_3_3/)，再升级至 3.5。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

在开始之前，[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。若升级过程中出现异常，可使用此备份将 etcd 版本 [回退](#downgrade)至当前版本。请注意，`snapshot`命令仅备份 v3 数据。如需备份 v2 数据，请参见[备份 v2 数据存储](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.5 版本后，才认为集群已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及支持的功能。

#### 限制 {#limitations}

请注意：如果集群仅包含 v3 数据且无 v2 数据，则不受此限制影响。

如果集群正在服务的数据集大小超过 50MB，每个新升级的成员可能需要最多 2 分钟才能追上现有集群。请检查最近快照的大小以估算总数据量。换句话说，升级每个成员之间应至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.5，则集群将升级至 v3.5，从该完成状态回退**不可行**。然而，若任一成员仍为 v3.4，则集群及其操作仍保持 "v3.4"，在此混合集群状态下，可将所有成员恢复为使用 v3.4 etcd 二进制文件。

请 [下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便在集群完成升级后仍可执行降级操作。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.4 etcd 集群。

#### 步骤 1: 检查升级要求 {#step-1-check-upgrade-requirements}

集群是否健康且运行 v3.4.x 版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT
```

#### Step 2: 从领导者下载快照备份 {#step-2-download-snapshot-backup-from-leader}

[下载快照备份](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便在出现任何问题时提供回退路径。

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
{"level":"info","ts":1526585787.148433,"caller":"snapshot/v3_snapshot.go:109","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":1526585787.1485257,"caller":"snapshot/v3_snapshot.go:120","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":1526585787.1519694,"caller":"snapshot/v3_snapshot.go:133","msg":"fetched snapshot","endpoint":"localhost:2379","took":0.003502721}
{"level":"info","ts":1526585787.1520295,"caller":"snapshot/v3_snapshot.go:142","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### 第 3 步：停止一个现有的 etcd 服务器 {#step-3-stop-one-existing-etcd-server}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```bash
{"level":"info","ts":1526587281.2001143,"caller":"etcdserver/server.go:2249","msg":"updating cluster version","from":"3.0","to":"3.4"}
{"level":"info","ts":1526587281.2010646,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}
{"level":"info","ts":1526587281.2012327,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}
{"level":"info","ts":1526587281.2013083,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}



^C{"level":"info","ts":1526587299.0717514,"caller":"osutil/interrupt_unix.go:63","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":1526587299.0718873,"caller":"embed/etcd.go:285","msg":"closing etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
{"level":"info","ts":1526587299.0722554,"caller":"etcdserver/server.go:1341","msg":"leadership transfer starting","local-member-id":"7339c4e5e833c029","current-leader-member-id":"7339c4e5e833c029","transferee-member-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.0723994,"caller":"raft/raft.go:1107","msg":"7339c4e5e833c029 [term 3] starts to transfer leadership to 729934363faa4a24"}
{"level":"info","ts":1526587299.0724802,"caller":"raft/raft.go:1113","msg":"7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log"}
{"level":"info","ts":1526587299.0737045,"caller":"raft/raft.go:797","msg":"7339c4e5e833c029 [term: 3] received a MsgVote message with higher term from 729934363faa4a24 [term: 4]"}
{"level":"info","ts":1526587299.0737681,"caller":"raft/raft.go:656","msg":"7339c4e5e833c029 became follower at term 4"}
{"level":"info","ts":1526587299.073831,"caller":"raft/raft.go:882","msg":"7339c4e5e833c029 [logterm: 3, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 3, index: 9] at term 4"}
{"level":"info","ts":1526587299.0738947,"caller":"raft/node.go:312","msg":"raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 4"}
{"level":"info","ts":1526587299.0748374,"caller":"raft/node.go:306","msg":"raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 4"}
{"level":"info","ts":1526587299.1726425,"caller":"etcdserver/server.go:1362","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"729934363faa4a24","took":0.100389359}
{"level":"info","ts":1526587299.1728148,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1751974,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1752589,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.177348,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1774004,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.177515,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1777067,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34636->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1778402,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1780295,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34634->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1780987,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781602,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781986,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1802843,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1803446,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1824749,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.18255,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.18261,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1827736,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"read tcp 127.0.0.1:51482->127.0.0.1:22380: use of closed network connection"}
{"level":"info","ts":1526587299.182845,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1830168,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"context canceled"}
{"level":"warn","ts":1526587299.1831107,"caller":"rafthttp/peer_status.go:65","msg":"peer became inactive","peer-id":"729934363faa4a24","error":"failed to read 729934363faa4a24 on stream Message (context canceled)"}
{"level":"info","ts":1526587299.1831737,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.1832306,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1837125,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1840093,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1842315,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1844475,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"info","ts":1526587299.2056687,"caller":"embed/etcd.go:473","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.205819,"caller":"embed/etcd.go:480","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.2058413,"caller":"embed/etcd.go:289","msg":"closed etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
```

#### 第 4 步：使用相同配置重启 etcd 服务器 {#step-4-restart-the-etcd-server-with-same-configuration}

使用相同配置但采用新 etcd 二进制文件重启 etcd 服务器。

```diff
-etcd-old --name s1 \
+etcd-new --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

新的 v3.5 etcd 将向集群发布其信息。此时，集群仍以 v3.4 协议运行，该版本为最低公共版本。

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

验证每个成员以及整个集群在使用新的 v3.5 etcd 二进制文件后是否恢复正常健康状态：

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

未升级的成员将持续记录如下警告，直至整个集群完成升级。

这是预期行为，当所有 etcd 集群成员都升级到 v3.5 后，该现象将停止。

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### 第 5 步：重复第 3 步和第 4 步，对剩余的成员进行操作 {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

所有成员升级完成后，集群将成功报告升级至 3.5：

成员 1：

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

成员 2：

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

成员 3：

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
