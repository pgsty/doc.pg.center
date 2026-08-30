---
title: 将 etcd 从 3.3 升级到 3.4
weight: 6700
description: 升级 etcd 3.3 至 3.4 的流程、检查清单与注意事项
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
---

在一般情况下，从 etcd 3.3 升级到 3.4 可以实现零停机滚动升级：

- 逐一停止 etcd v3.3 进程，并替换为 etcd v3.4 进程
- 在所有 v3.4 进程运行后，集群即可使用 v3.4 的新特性

在 [开始升级](#upgrade-procedure) 之前，请通读本指南其余部分以做好准备。



### 升级检查列表 {#upgrade-checklists}

> [!WARNING]
> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。

3.4 版本中的重点变更。

#### 设置 `ETCDCTL_API=3 etcdctl` 为默认值 {#make-etcdctl_api3-etcdctl-default}

`ETCDCTL_API=3` 现为默认值。

```diff
etcdctl set foo bar
Error: unknown command "set" for "etcdctl"

-etcdctl set foo bar
+ETCDCTL_API=2 etcdctl set foo bar
bar

ETCDCTL_API=3 etcdctl put foo bar
OK

-ETCDCTL_API=3 etcdctl put foo bar
+etcdctl put foo bar
```

#### 设置 `etcd --enable-v2=false` 为默认值 {#make-etcd---enable-v2false-default}

[`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) 现为默认值。

这意味着，除非指定了 `etcd --enable-v2=true`，否则 etcd v3.4 服务器将不会提供 v2 API 请求服务。

如果使用了 v2 API，请确保在 v3.4 版本中启用了 v2 API：

```diff
-etcd
+etcd --enable-v2=true
```

其他 HTTP API 仍可正常工作（例如 `[CLIENT-URL]/metrics`、`[CLIENT-URL]/health`、v3 gRPC 网关）。

#### 已弃用 `etcd --ca-file` 和 `etcd --peer-ca-file` 标志 {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

`--ca-file` 和 `--peer-ca-file` 标志已弃用；自 v2.1 版本起已弃用。

请注意，设置此参数将自动启用客户端证书身份认证，无论 `--client-cert-auth` 设置为何值。

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### 废弃的`grpc.ErrClientConnClosing`错误 {#deprecated-grpcerrclientconnclosing-error}

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

#### 要求 `grpc.WithBlock` 进行客户端连接 {#require-grpcwithblock-for-client-dial}

[新的客户端负载均衡器](/zh/etcd/learning/design-client/)使用异步解析器，将端点传递给 gRPC 连接函数。因此，v3.4 客户端必须使用 `grpc.WithBlock` 连接选项，以等待底层连接建立完成。

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

#### 废弃 `etcd_debugging_mvcc_db_total_size_in_bytes` Prometheus 指标 {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.4 将 `etcd_debugging_mvcc_db_total_size_in_bytes` Prometheus 指标提升至 `etcd_mvcc_db_total_size_in_bytes`，以鼓励对 etcd 存储进行监控。

`etcd_debugging_mvcc_db_total_size_in_bytes` 在 v3.4 版本中仍为向后兼容而提供，将在 v3.5 版本中完全弃用。

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 废弃 `etcd_debugging_mvcc_put_total` Prometheus 指标 {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.4 将 `etcd_debugging_mvcc_put_total` Prometheus 指标提升至 `etcd_mvcc_put_total`，以鼓励对 etcd 存储进行监控。

`etcd_debugging_mvcc_put_total` 在 v3.4 版本中仍为向后兼容而提供，将在 v3.5 版本中完全弃用。

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 废弃 `etcd_debugging_mvcc_delete_total` Prometheus 指标 {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.4 将 `etcd_debugging_mvcc_delete_total` Prometheus 指标提升至 `etcd_mvcc_delete_total`，以鼓励对 etcd 存储进行监控。

`etcd_debugging_mvcc_delete_total` 在 v3.4 版本中仍为向后兼容而提供，将在 v3.5 版本中完全弃用。

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 废弃 `etcd_debugging_mvcc_txn_total` Prometheus 指标 {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.4 将 `etcd_debugging_mvcc_txn_total` Prometheus 指标提升至 `etcd_mvcc_txn_total`，以鼓励对 etcd 存储进行监控。

`etcd_debugging_mvcc_txn_total` 在 v3.4 版本中仍为向后兼容而提供，将在 v3.5 版本中完全弃用。

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 废弃 Prometheus 元度指标`etcd_debugging_mvcc_range_total` {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.4 将 `etcd_debugging_mvcc_range_total` 的 Prometheus 指标提升至 `etcd_mvcc_range_total`，以鼓励对 etcd 存储进行监控。

`etcd_debugging_mvcc_range_total` 在 v3.4 版本中仍为向后兼容而提供，将在 v3.5 版本中完全弃用。

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

请注意，`etcd_debugging_*` 命名空间指标已被标记为实验性。随着监控指南的完善，我们可能会将更多指标升级为正式支持。

#### 弃用 `etcd --log-output` 标志（现已 `--log-outputs`） {#deprecating-etcd---log-output-flag-now---log-outputs}

将 [`etcd --log-output` 重命名为 `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624)，以支持多日志输出。**`etcd --logger=capnslog` 不支持多日志输出。**

**`etcd --log-output`** 将在 v3.5 版本中弃用。**`etcd --logger=capnslog` 将在 v3.5 版本中弃用**。

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 增加 `etcd --logger=zap --log-outputs=stderr` 对结构化日志和多日志输出的支持。主要动机是推动 etcd 的自动化监控，而非在服务出现异常时回溯服务器日志。未来开发将尽量减少 etcd 的日志输出，并通过指标和告警使 etcd 更易于监控。**`etcd --logger=capnslog` 将在 v3.5 中弃用**。

#### 将 `log-outputs` 字段类型在 `etcd --config-file` 中更改为 `[]string` {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

现在 `log-outputs`（旧字段名 `log-output`）支持多个写入者，因此 etcd 配置 YAML 文件 `log-outputs` 字段必须更改为如下所示的 `[]string` 类型：

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### 将`embed.Config.LogOutput`重命名为`embed.Config.LogOutputs` {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

将 [**`embed.Config.LogOutput`** 重命名为 **`embed.Config.LogOutputs`**](https://github.com/etcd-io/etcd/pull/9624)，以支持多日志输出。并将 [`embed.Config.LogOutput` 类型从 `string` 改为 `[]string`](https://github.com/etcd-io/etcd/pull/9579)，以支持多日志输出。

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5 弃用`capnslog` {#v35-deprecates-capnslog}

*v3.5 将弃用 `etcd --log-package-levels` 标志的 `capnslog` 功能；`etcd --logger=zap --log-outputs=stderr` 将成为默认值。v3.5 将弃用 `[CLIENT-URL]/config/local/log` 端点。*

```diff
-etcd
+etcd --logger zap
```

#### 弃用 `etcd --debug` 标志（现已 `--log-level=debug`） {#deprecating-etcd---debug-flag-now---log-leveldebug}

v3.4 已弃用 [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947) 标志。应改用 `etcd --log-level=debug` 标志。

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### 弃用的 `pkg/transport.TLSInfo.CAFile` 字段 {#deprecated-pkgtransporttlsinfocafile-field}

已弃用 `pkg/transport.TLSInfo.CAFile` 字段。

```diff
import "github.com/coreos/etcd/pkg/transport"

tlsInfo := transport.TLSInfo{
    CertFile: "/tmp/test-certs/test.pem",
    KeyFile: "/tmp/test-certs/test-key.pem",
-   CAFile: "/tmp/test-certs/trusted-ca.pem",
+   TrustedCAFile: "/tmp/test-certs/trusted-ca.pem",
}
tlsConfig, err := tlsInfo.ClientConfig()
if err != nil {
    panic(err)
}
```

#### 将 `embed.Config.SnapCount` 更改为 `embed.Config.SnapshotCount` {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

为与标志名称 `etcd --snapshot-count` 保持一致，`embed.Config.SnapCount` 字段已重命名为 `embed.Config.SnapshotCount`：

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### 将 `etcdserver.ServerConfig.SnapCount` 更改为 `etcdserver.ServerConfig.SnapshotCount` {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

为与标志名称 `etcd --snapshot-count` 保持一致，`etcdserver.ServerConfig.SnapCount` 字段已重命名为 `etcdserver.ServerConfig.SnapshotCount`：

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### 修改了包 `wal` 的函数签名 {#changed-function-signature-in-package-wal}

修改 `wal` 函数签名以支持结构化日志记录。

```diff
import "github.com/coreos/etcd/wal"
+import "go.uber.org/zap"

+lg, _ = zap.NewProduction()

-wal.Open(dirpath, snap)
+wal.Open(lg, dirpath, snap)

-wal.OpenForRead(dirpath, snap)
+wal.OpenForRead(lg, dirpath, snap)

-wal.Repair(dirpath)
+wal.Repair(lg, dirpath)

-wal.Create(dirpath, metadata)
+wal.Create(lg, dirpath, metadata)
```

#### 更改了 `IntervalTree` 类型 在 `pkg/adt` 包中 {#changed-intervaltree-type-in-package-pkgadt}

`pkg/adt.IntervalTree` 现已定义为 `interface`。

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### 已弃用 `embed.Config.SetupLogging` {#deprecated-embedconfigsetuplogging}

`embed.Config.SetupLogging` 已被移除，以防止错误的日志配置，现在将自动设置。

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### Changed gRPC 网关 HTTP 端点（替换 `/v3beta` 为 `/v3`） {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

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

对 `/v3beta` 端点的请求将重定向至 `/v3`，`/v3beta` 将在 3.5 版本中移除。

#### 已弃用的容器镜像标签 {#deprecated-container-image-tags}

`latest` 及其小版本镜像标签已弃用：

```diff
-docker pull gcr.io/etcd-development/etcd:latest
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.1

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.2
```

### 服务器升级检查清单 {#server-upgrade-checklists}

#### 升级要求 {#upgrade-requirements}

要将现有 etcd 部署升级至 3.4 版本，运行中的集群版本必须为 3.3 或更高。若版本低于 3.3，请先 [升级至 3.3](/zh/etcd/upgrades/upgrade_3_3/)，再升级至 3.4。

此外，为确保滚动升级顺利进行，运行中的集群必须处于健康状态。在继续操作前，请使用 `etcdctl endpoint health` 命令检查集群健康状况。

#### 准备 {#preparation}

在升级 etcd 之前，请务必在预发环境中测试依赖 etcd 的服务，再将升级部署到生产环境。

在开始之前，[下载快照备份](/zh/etcd/op-guide/maintenance/#snapshot-backup)。若升级过程中出现异常，可使用此备份将 etcd 版本 [回退](#downgrade)至当前版本。请注意，`snapshot`命令仅备份 v3 数据。如需备份 v2 数据，请参见[备份 v2 数据存储](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore)。

#### 混合版本 {#mixed-versions}

升级期间，etcd 集群支持不同版本的 etcd 成员共存，并以最低公共版本的协议运行。只有当集群中所有成员均升级至 3.4 版本后，该集群才被视为已完成升级。内部机制上，etcd 成员之间会相互协商以确定集群的整体版本，该版本控制报告的版本及支持的功能。

#### 限制 {#limitations}

请注意：如果集群仅包含 v3 数据且无 v2 数据，则不受此限制影响。

如果集群正在服务的数据集大小超过 50MB，每个新升级的成员可能需要最多 2 分钟才能追上现有集群。请检查最近快照的大小以估算总数据量。换句话说，升级每个成员之间应至少等待 2 分钟。

对于数据总量更大（例如 100MB 或更多）的情况，此一次性操作可能需要更长时间。对于规模达到此类程度的大型 etcd 集群，系统管理员可在升级前自由联系 [etcd 团队][etcd-contact]，我们将乐意提供升级流程方面的建议。

#### 降级 {#downgrade}

如果所有成员均已升级至 v3.4 版本，集群将升级至 v3.4 版本，从该完成状态回退**不可行**。然而，若任一成员仍为 v3.3 版本，则集群及其操作仍保持 "v3.3" 状态，此时可从该混合集群状态恢复至所有成员均使用 v3.3 etcd 二进制文件。

请 [下载快照备份](/zh/etcd/op-guide/maintenance/#snapshot-backup)，以便在集群完成升级后仍可执行降级操作。

### 升级流程 {#upgrade-procedure}

本示例演示如何升级在本地计算机上运行的 3 个成员的 v3.3 etcd 集群。

#### 步骤 1: 检查升级要求 {#step-1-check-upgrade-requirements}

集群是否健康且运行 v3.3.x 版本？

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
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
10.237579 I | etcdserver: updating the cluster version from 3.0 to 3.3
10.238315 N | etcdserver/membership: updated the cluster version from 3.0 to 3.3
10.238451 I | etcdserver/api: enabled capabilities for version 3.3


^C21.192174 N | pkg/osutil: received interrupt signal, shutting down...
21.192459 I | etcdserver: 7339c4e5e833c029 starts leadership transfer from 7339c4e5e833c029 to 729934363faa4a24
21.192569 I | raft: 7339c4e5e833c029 [term 8] starts to transfer leadership to 729934363faa4a24
21.192619 I | raft: 7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log
WARNING: 2018/05/17 12:45:21 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 0  <nil>}
WARNING: 2018/05/17 12:45:21 grpc: addrConn.transportMonitor exits due to: grpc: the connection is closing
21.193589 I | raft: 7339c4e5e833c029 [term: 8] received a MsgVote message with higher term from 729934363faa4a24 [term: 9]
21.193626 I | raft: 7339c4e5e833c029 became follower at term 9
21.193651 I | raft: 7339c4e5e833c029 [logterm: 8, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 8, index: 9] at term 9
21.193675 I | raft: raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 9
21.194424 I | raft: raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 9
21.292898 I | etcdserver: 7339c4e5e833c029 finished leadership transfer from 7339c4e5e833c029 to 729934363faa4a24 (took 100.436391ms)
21.292975 I | rafthttp: stopping peer 729934363faa4a24...
21.293206 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 writer)
21.293225 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293437 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream Message writer)
21.293459 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293514 I | rafthttp: stopped HTTP pipelining with peer 729934363faa4a24
21.293590 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293610 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293680 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream Message reader)
21.293700 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream Message reader)
21.293711 I | rafthttp: stopped peer 729934363faa4a24
21.293720 I | rafthttp: stopping peer b548c2511513015...
21.293987 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 writer)
21.294063 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294467 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream Message writer)
21.294561 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294742 I | rafthttp: stopped HTTP pipelining with peer b548c2511513015
21.294867 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 reader)
21.294892 I | rafthttp: stopped streaming with peer b548c2511513015 (stream MsgApp v2 reader)
21.294990 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream Message reader)
21.295004 E | rafthttp: failed to read b548c2511513015 on stream Message (context canceled)
21.295013 I | rafthttp: peer b548c2511513015 became inactive
21.295024 I | rafthttp: stopped streaming with peer b548c2511513015 (stream Message reader)
21.295035 I | rafthttp: stopped peer b548c2511513015
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
+ --initial-cluster-state new \
+ --logger zap \
+ --log-outputs stderr
```

新的 v3.4 etcd 将向集群发布其信息。此时，集群仍以 v3.3 协议运行，该版本为最低公共版本。

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

验证每个成员以及整个集群在使用新的 v3.4 etcd 二进制文件后是否恢复正常健康状态：

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

未升级的成员将持续记录如下警告，直至整个集群完成升级。

这是预期行为，当所有 etcd 集群成员都升级到 v3.4 后，该现象将停止。

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### 第 5 步：重复第 3 步和第 4 步，对剩余的成员进行操作 {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

所有成员升级完成后，集群将成功报告升级至 3.4：

成员 1：

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

成员 2：

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

成员 3：

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
