---
title: 将 etcd 从 3.2 升级到 3.3
weight: 6750
description: 升级 etcd 3.2 至 3.3 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
aliases: [/etcd/upgrades/upgrade_3_3/]
---

在一般情况下，从 etcd 3.2 升级到 3.3 可以实现零停机滚动升级：

- 逐一停止 etcd v3.2 进程，并替换为 etcd v3.3 进程
- 在所有 v3.3 进程运行后，集群即可使用 v3.3 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。

### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

> [!WARNING]
> 若启用认证并使用租约（租约 TTL 较小），极有可能遇到 [问题](https://github.com/etcd-io/etcd/issues/11689)，导致数据不一致。强烈建议先升级至 3.2.31+ 以修复此问题，再升级至 3.3。此外，在升级过程中，若无权限用户向 3.3 节点发送 `LeaseRevoke` 请求，仍可能导致数据损坏，因此建议在升级前确保环境中不存在此类异常调用，详情请参见 [#11691](https://github.com/etcd-io/etcd/pull/11691)。


3.3 版本中的重点变更。

#### 将 `etcd --auto-compaction-retention` 标志的价值类型更改为 `string` {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

将 `--auto-compaction-retention` 标志改为 [接受字符串值](https://github.com/etcd-io/etcd/pull/8563)，并支持 [更细粒度](https://github.com/etcd-io/etcd/issues/8503)。由于 `--auto-compaction-retention` 现在接受字符串值，etcd 配置 YAML 文件 `auto-compaction-retention` 字段必须改为 `string` 类型。此前 `--config-file etcd.config.yaml` 可包含 `auto-compaction-retention: 24` 字段，现在必须为 `auto-compaction-retention: "24"` 或 `auto-compaction-retention: "24h"`。若配置为 `--auto-compaction-mode periodic --auto-compaction-retention "24h"`，则 `--auto-compaction-retention` 标志的时间持续值必须对 Go 中的 [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration) 函数有效。

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### 将 `etcdserver.EtcdServer.ServerConfig` 更改为 `*etcdserver.EtcdServer.ServerConfig` {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

`etcdserver.EtcdServer` 已将成员字段 `*etcdserver.ServerConfig` 的类型更改为 `etcdserver.ServerConfig`。现在 `etcdserver.NewServer` 接受 `etcdserver.ServerConfig`，而非 `*etcdserver.ServerConfig`。

之前和之后（例如 [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55)）

```diff
import "github.com/coreos/etcd/etcdserver"

type EtcdServer struct {
	*etcdserver.EtcdServer
-	config *etcdserver.ServerConfig
+	config etcdserver.ServerConfig
}

func NewEtcd(dataDir string) *EtcdServer {
-	config := &etcdserver.ServerConfig{
+	config := etcdserver.ServerConfig{
		DataDir: dataDir,
        ...
	}
	return &EtcdServer{config: config}
}

func (e *EtcdServer) Start() error {
	var err error
	e.EtcdServer, err = etcdserver.NewServer(e.config)
    ...
```

#### 添加了 `embed.Config.LogOutput` 结构体 {#added-embedconfiglogoutput-struct}

> [!WARNING]
> 请注意，此字段在 v3.4 版本中已重命名为 `embed.Config.LogOutputs`，适用于 `[]string` 类型。详情请参阅 [v3.4 升级指南](/zh/docs/etcd/upgrades/upgrade_3_4/)。

字段 `LogOutput` 已添加至 `embed.Config`：

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

在 gRPC 服务器警告被记录到 etcdserver 之前。

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

从 v3.3 版本开始，gRPC 服务器日志默认已禁用。

> [!WARNING]
> 请注意，`embed.Config.SetupLogging` 方法已在 v3.4 版本中弃用。详情请参阅 [v3.4 升级指南](/zh/docs/etcd/upgrades/upgrade_3_4/)。

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

将 `embed.Config.Debug` 字段设置为 `true` 以启用 gRPC 服务器日志。

#### Changed `/health` 端点响应 {#changed-health-endpoint-response}

此前，`[endpoint]:[client-port]/health` 返回手动序列化的 JSON 值。3.3 版本现在定义了 [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health) 结构体。

请注意，在 v3.3.0-rc.0、v3.3.0-rc.1 和 v3.3.0-rc.2 版本中，`etcdhttp.Health` 的 `"health"` 和 `"errors"` 字段为布尔类型。为保持向后兼容性，已将 `"health"` 字段恢复为 `string` 类型，并移除了 `"errors"` 字段。后续的健康信息将通过独立的 API 提供。

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### Changed gRPC 网关 HTTP 端点（替换 `/v3alpha` 为 `/v3beta`） {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

本文未提供内容。

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

之后

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

对 `/v3alpha` 端点的请求将重定向至 `/v3beta`，`/v3alpha` 将在 3.4 版本中移除。

#### 调整了最大请求大小限制 {#changed-maximum-request-size-limits}

3.3 现在允许为服务器端和客户端分别设置自定义请求大小限制。在之前版本（v3.2.10、v3.2.11）中，客户端响应大小限制仅为 4 MiB。

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

#### 更改了原始 gRPC 客户端包装函数的签名 {#changed-raw-grpc-client-wrapper-function-signatures}

3.3 修改了 `clientv3` gRPC 客户端封装的函数签名。此变更旨在支持 [自定义 `grpc.CallOption` 消息大小限制](https://github.com/etcd-io/etcd/pull/9047)。

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

#### Changed clientv3 `Snapshot` API 错误类型 {#changed-clientv3-snapshot-api-error-type}

此前，clientv3 `Snapshot` API 返回原始的 [`grpc/*status.statusError`] 类型错误。v3.3 现已将这些错误转换为对应的公开错误类型，以与其他 API 保持一致。

本文未提供内容。

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err.Error() == "rpc error: code = Canceled desc = context canceled"

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err.Error() == "rpc error: code = DeadlineExceeded desc = context deadline exceeded"
```

之后

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err == context.Canceled

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err == context.DeadlineExceeded
```

#### Changed `etcdctl lease timetolive` 命令输出 {#changed-etcdctl-lease-timetolive-command-output}

此前，对已过期租约执行 `lease timetolive LEASE_ID` 命令时会输出 `-1s` 表示剩余秒数。3.3 版本现在输出更清晰的提示信息。

本文未提供内容。


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

之后

```bash
lease 2d8257079fa1bc0c already expired
```

#### 变更 `golang.org/x/net/context` 导入 {#changed-golangorgxnetcontext-imports}

`clientv3` 已弃用 `golang.org/x/net/context`。若项目在其他代码中引入 `golang.org/x/net/context`（例如 etcd 生成的协议缓冲区代码）并导入 `github.com/coreos/etcd/clientv3`，则编译时需使用 Go 1.9 或更高版本。

本文未提供内容。

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

之后

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### 更改了 gRPC 依赖 {#changed-grpc-dependency}

3.3 必须使用 [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`。

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

此前，在客户端连接超时时返回 `grpc.ErrClientConnTimeout` 错误。3.3 版本改为返回 `context.DeadlineExceeded`（参见 [#8504](https://github.com/etcd-io/etcd/issues/8504)）。

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

#### 变更官方容器注册表 {#changed-official-container-registry}

etcd 现在使用 [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) 作为主容器注册表，使用 [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) 作为备用。

本文未提供内容。

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

之后

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### 升级至>=v3.3.14 {#upgrades-to--v3314}

[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) 在尽量减少客户端负载均衡实现差异的前提下，引入了部分 3.4 版本的特性。此版本修复了 [“当首个 etcd-server 不可用时，kube-apiserver 1.13.x 拒绝运行”（kubernetes#72102）](https://github.com/kubernetes/kubernetes/issues/72102) 的问题。

`grpc.ErrClientConnClosing` 在 gRPC ≥ 1.10 中已被 [弃用](https://github.com/grpc/grpc-go/pull/1854)。

```diff
import (
+	"go.etcd.io/etcd/clientv3"

	"google.golang.org/grpc"
+	"google.golang.org/grpc/codes"
+	"google.golang.org/grpc/status"
)

_, err := kvc.Get(ctx, "a")
-if err == grpc.ErrClientConnClosing {
+if clientv3.IsConnCanceled(err) {

// or
+s, ok := status.FromError(err)
+if ok {
+  if s.Code() == codes.Canceled
```

[新的客户端负载均衡器](/zh/docs/etcd/learning/design-client/)使用异步解析器将端点传递给 gRPC dial 函数。因此，[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) 或更高版本必须使用 `grpc.WithBlock` dial 选项，以等待底层连接建立完成。

```diff
import (
	"time"
	"go.etcd.io/etcd/clientv3"
+	"google.golang.org/grpc"
)

+// "grpc.WithBlock()" to block until the underlying connection is up
ccfg := clientv3.Config{
  Endpoints:            []string{"localhost:2379"},
  DialTimeout:          time.Second,
+ DialOptions:          []grpc.DialOption{grpc.WithBlock()},
  DialKeepAliveTime:    time.Second,
  DialKeepAliveTimeout: 500 * time.Millisecond,
}
```

请参阅 [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) 以获取完整变更列表。

### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 3.3 版本，运行中的集群版本必须为 3.2 或更高。若版本低于 3.2，请先 [升级至 3.2](/zh/docs/etcd/upgrades/upgrade_3_2/)，再升级至 3.3。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

升级前，请对 etcd 数据执行 [备份 etcd 数据](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)。若升级过程中出现异常，可使用此备份将系统 [降级](#downgrade)至现有 etcd 版本。请注意，`snapshot`命令仅备份 v3 数据。如需备份 v2 数据，请参阅 [备份 v2 数据存储](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore)。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.3 版本后，该集群才被视为已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及所支持的功能。

#### 限制 {#limitations}

请注意：如果集群仅包含 v3 数据且无 v2 数据，则不受此限制影响。

如果集群正在服务的数据集大小超过 50MB，每个新升级的成员可能需要最多 2 分钟才能追上现有集群。请检查最近快照的大小以估算总数据量。换句话说，升级每个成员之间应至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.3 版本，集群将升级至 v3.3 版本，从该完成状态回退**不可行**。然而，若任一成员仍为 v3.2 版本，则集群及其操作仍保持 "v3.2" 状态，此时可从该混合集群状态恢复至所有成员均使用 v3.2 etcd 二进制文件。

请备份所有 etcd 成员的数据目录 [backup the data directory](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以确保在集群完全升级后仍可执行降级操作。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.2 etcd 集群。

#### 1. 检查升级要求 {#1-check-upgrade-requirements}

集群是否健康且运行 v3.2.x 版本？

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. 停止现有 etcd 进程 {#2-stop-the-existing-etcd-process}

当每个 etcd 进程停止时，集群中的其他成员会记录预期的错误。这是正常的，因为集群成员之间的连接已（暂时）中断：

```
14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

此时建议 [备份 etcd 数据](/zh/docs/etcd/op-guide/maintenance/#snapshot-backup)，以便在出现任何问题时可回退至之前版本：

```
$ etcdctl snapshot save backup.db
```

#### 3. 插入 etcd v3.3 二进制文件并启动新 etcd 进程 {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

新的 v3.3 版 etcd 将向集群发布其信息：

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

验证每个成员以及整个集群在使用新的 v3.3 etcd 二进制文件后是否恢复正常健康状态：

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

升级后的成员将在整个集群完成升级前持续记录类似以下的警告日志。这是预期行为，当所有 etcd 集群成员均升级至 v3.3 后，警告将停止出现。

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. 重复第 2 步到第 3 步，对所有其他成员执行 {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完成 {#5-finish}

所有成员升级完成后，集群将成功报告升级至 3.3：

```
14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.2 to 3.3
14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.3
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
