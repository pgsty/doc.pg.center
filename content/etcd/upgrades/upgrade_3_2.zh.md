---
title: 将 etcd 从 3.1 升级到 3.2
weight: 6800
description: 升级 etcd 3.1 至 3.2 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

在一般情况下，从 etcd 3.1 升级到 3.2 可以实现零停机滚动升级：

- 逐一停止 etcd v3.1 进程，并替换为 etcd v3.2 进程
- 在所有 v3.2 进程运行后，集群即可使用 v3.2 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

3.2 版本中的重点变更。

#### Changed default `snapshot-count` value {#changed-default-snapshot-count-value}

较高的 `--snapshot-count` 会在生成快照前将更多 Raft 条目保留在内存中，从而导致 [内存使用量持续较高](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156)。由于领导者会更长时间保留最新的 Raft 条目，缓慢的跟随者有更多时间在领导者生成快照前完成追赶。`--snapshot-count` 是较高内存使用与缓慢跟随者更高可用性之间的权衡。

自 v3.2 起，`--snapshot-count` 的默认值已 [从 10,000 改为 100,000](https://github.com/etcd-io/etcd/pull/7160)。

#### 更新了 gRPC 依赖 (>=3.2.10) {#changed-grpc-dependency-3210}

3.2.10 及更高版本现在要求 [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`（3.2.9 及更早版本要求 `v1.2.1`）。

##### 已弃用 `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` 已被弃用，建议改用 [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go)。`clientv3.Logger` 现已改为 `grpclog.LoggerV2`。

本文未提供内容。

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

之后

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### 已弃用 `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

此前，在客户端连接超时时返回 `grpc.ErrClientConnTimeout` 错误。3.2 版本改为返回 `context.DeadlineExceeded`（参见 [#8504](https://github.com/etcd-io/etcd/issues/8504)）。

本文未提供内容。

```go
// expect dial time-out on ipv4 blackhole
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == grpc.ErrClientConnTimeout {
	// handle errors
}
```

之后

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### 调整了最大请求大小限制（>=3.2.10） {#changed-maximum-request-size-limits-3210}

3.2.10 和 3.2.11 版本允许在服务端自定义请求大小限制。从 3.2.12 版本开始，服务端和客户端均支持自定义请求大小限制。在之前的版本（v3.2.10、v3.2.11）中，客户端响应大小仅限于 4 MiB。

服务器端请求限制可通过 `--max-request-bytes` 标志进行配置：

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

或配置 `embed.Config.MaxRequestBytes` 字段：

```go
import "github.com/coreos/etcd/embed"
import "github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes"

// limit requests to 5 MiB
cfg := embed.NewConfig()
cfg.MaxRequestBytes = 5 * 1024 * 1024

// client writes exceeding 5 MiB will be rejected
_, err := cli.Put(ctx, "foo", [LARGE VALUE...])
err == rpctypes.ErrRequestTooLarge
```

如果未指定，服务器端限制默认为 1.5 MiB。

客户端请求限制必须根据服务器端限制进行配置。

```bash
# limits request size to 1 MiB
etcd --max-request-bytes 1048576
```

```go
import "github.com/coreos/etcd/clientv3"

cli, _ := clientv3.New(clientv3.Config{
    Endpoints: []string{"127.0.0.1:2379"},
    MaxCallSendMsgSize: 2 * 1024 * 1024,
    MaxCallRecvMsgSize: 3 * 1024 * 1024,
})


// client writes exceeding "--max-request-bytes" will be rejected from etcd server
_, err := cli.Put(ctx, "foo", strings.Repeat("a", 1*1024*1024+5))
err == rpctypes.ErrRequestTooLarge


// client writes exceeding "MaxCallSendMsgSize" will be rejected from client-side
_, err = cli.Put(ctx, "foo", strings.Repeat("a", 5*1024*1024))
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: trying to send message larger than max (5242890 vs. 2097152)"


// some writes under limits
for i := range []int{0,1,2,3,4} {
    _, err = cli.Put(ctx, fmt.Sprintf("foo%d", i), strings.Repeat("a", 1*1024*1024-500))
    if err != nil {
        panic(err)
    }
}
// client reads exceeding "MaxCallRecvMsgSize" will be rejected from client-side
_, err = cli.Get(ctx, "foo", clientv3.WithPrefix())
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: received message larger than max (5240509 vs. 3145728)"
```

如果未指定，客户端发送限制默认为 2 MiB（1.5 MiB + gRPC 开销字节），接收限制为 `math.MaxInt32`。请参阅 [clientv3 godoc](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) 获取更多详细信息。

#### 更改了原始 gRPC 客户端包装器 {#changed-raw-grpc-client-wrappers}

3.2.12 及更高版本更改了 `clientv3` gRPC 客户端封装的函数签名。此更改旨在支持 [自定义 `grpc.CallOption` 消息大小限制](https://github.com/etcd-io/etcd/pull/9047)。

之前和之后

```diff
-func NewKVFromKVClient(remote pb.KVClient) KV {
+func NewKVFromKVClient(remote pb.KVClient, c *Client) KV {

-func NewClusterFromClusterClient(remote pb.ClusterClient) Cluster {
+func NewClusterFromClusterClient(remote pb.ClusterClient, c *Client) Cluster {

-func NewLeaseFromLeaseClient(remote pb.LeaseClient, keepAliveTimeout time.Duration) Lease {
+func NewLeaseFromLeaseClient(remote pb.LeaseClient, c *Client, keepAliveTimeout time.Duration) Lease {

-func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient) Maintenance {
+func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient, c *Client) Maintenance {

-func NewWatchFromWatchClient(wc pb.WatchClient) Watcher {
+func NewWatchFromWatchClient(wc pb.WatchClient, c *Client) Watcher {
```

#### 变更 `clientv3.Lease.TimeToLive` API {#changed-clientv3leasetimetolive-api}

此前，`clientv3.Lease.TimeToLive` API 在不存在的租约 ID 上返回 `lease.ErrLeaseNotFound`。3.2 版本改为在响应中返回 TTL=-1 且不返回错误（参见 [#7305](https://github.com/etcd-io/etcd/pull/7305)）。

本文未提供内容。

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

之后

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### 将`clientv3.NewFromConfigFile`移动到`clientv3.yaml.NewConfig` {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile` 已移至 `yaml.NewConfig`。

本文未提供内容。

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

之后

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### Change in `--listen-peer-urls` and `--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

3.2 现在拒绝为 `--listen-peer-urls` 和 `--listen-client-urls` 使用域名（3.1 仅输出警告），因为域名对网络接口绑定无效。请确保这些 URL 已正确格式化为 `scheme://IP:port`。

有关更多上下文，请参见 [issue #6336](https://github.com/etcd-io/etcd/issues/6336)。

### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 3.2 版本，运行中的集群版本必须为 3.1 或更高。若版本低于 3.1，请先 [升级至 3.1](/zh/etcd/upgrades/upgrade_3_1)，再升级至 3.2。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

升级前，请对 etcd 数据执行 [备份 etcd 数据](/zh/etcd/op-guide/maintenance#snapshot-backup)。若升级过程中出现异常，可使用此备份将系统 [降级](#downgrade)至现有 etcd 版本。请注意，`snapshot`命令仅备份 v3 数据。如需备份 v2 数据，请参阅 [备份 v2 数据存储](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.2 版本后，才认为集群已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及支持的功能。

#### 限制 {#limitations}

请注意：如果集群仅包含 v3 数据且无 v2 数据，则不受此限制影响。

如果集群正在服务的数据集大小超过 50MB，每个新升级的成员可能需要最多 2 分钟才能追上现有集群。请检查最近快照的大小以估算总数据量。换句话说，升级每个成员之间应至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.2 版本，集群将升级至 v3.2 版本，从该完成状态回退**不可行**。然而，若任一成员仍为 v3.1 版本，则集群及其操作仍保持 "v3.1" 状态，此时可从该混合集群状态恢复至所有成员均使用 v3.1 etcd 二进制文件。

请注意，务必对所有 etcd 成员的数据目录 [backup the data directory](/zh/etcd/op-guide/maintenance#snapshot-backup) 进行备份，以确保在集群完全升级后仍可执行降级操作。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.1 etcd 集群。

#### 1. 检查升级要求 {#1-check-upgrade-requirements}

集群是否健康且运行 v3.1.x 版本？

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. 停止现有 etcd 进程 {#2-stop-the-existing-etcd-process}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```
2017-04-27 14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
2017-04-27 14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
2017-04-27 14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
2017-04-27 14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
2017-04-27 14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
2017-04-27 14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
2017-04-27 14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
2017-04-27 14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
2017-04-27 14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
2017-04-27 14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
2017-04-27 14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
2017-04-27 14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

此时建议 [备份 etcd 数据](/zh/etcd/op-guide/maintenance#snapshot-backup)，以便在出现任何问题时提供回退路径：

```
$ etcdctl snapshot save backup.db
```

#### 3. 直接部署 etcd v3.2 二进制文件并启动新 etcd 进程 {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

新的 v3.2 版 etcd 将向集群发布其信息：

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

验证每个成员，然后整个集群，使用新的 v3.2 etcd 二进制文件后是否健康：

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

升级后的成员将在整个集群完成升级前持续记录如下警告信息。这是正常现象，待所有 etcd 集群成员均升级至 v3.2 后，警告将停止出现。

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. 重复第 2 步到第 3 步，对所有其他成员执行 {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完成 {#5-finish}

所有成员升级完成后，集群将成功报告升级至 3.2：

```
2017-04-27 14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.1 to 3.2
2017-04-27 14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.2
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
