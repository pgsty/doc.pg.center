---
title: etcdを3.2から3.3にアップグレード
weight: 6750
description: etcdを3.2から3.3にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
---

通常、etcd 3.2から3.3へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v3.2のプロセスを1つずつ停止し、etcd v3.3のプロセスに置き換えます。
 - すべてのプロセスがv3.3で稼働すると、クラスターでv3.3の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

> [!WARNING]
> 認証を有効にしてリースを使用している場合（リースのTTLが短い場合）、データの不整合を引き起こす[問題](https://github.com/etcd-io/etcd/issues/11689)に遭遇する可能性が高くなります。この問題を修正するため、まず3.2.31+にアップグレードしてから3.3にアップグレードすることを強くお勧めします。また、アップグレード中に権限のないユーザーが3.3ノードへ`LeaseRevoke`リクエストを送信すると、データが破損する可能性が残ります。アップグレード前に、そのような異常な呼び出しが環境内に存在しないことを確認するのが最善です。詳細は[#11691](https://github.com/etcd-io/etcd/pull/11691)を参照してください。


3.3の主な互換性を損なう変更は次のとおりです。

#### `etcd --auto-compaction-retention`フラグの値の型を`string`に変更 {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

`--auto-compaction-retention`フラグを変更して[文字列値を受け付ける](https://github.com/etcd-io/etcd/pull/8563)ようにし、[より細かい粒度](https://github.com/etcd-io/etcd/issues/8503)で指定できるようにしました。`--auto-compaction-retention`が文字列値を受け付けるようになったため、etcdの設定YAMLファイルの`auto-compaction-retention`フィールドを`string`型に変更しなければなりません。以前は`--config-file etcd.config.yaml`に`auto-compaction-retention: 24`フィールドを指定できましたが、今後は`auto-compaction-retention: "24"`または`auto-compaction-retention: "24h"`にする必要があります。`--auto-compaction-mode periodic --auto-compaction-retention "24h"`と設定する場合、`--auto-compaction-retention`フラグの期間の値は、Goの[`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration)関数で有効な値でなければなりません。

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### `*etcdserver.ServerConfig`を`etcdserver.ServerConfig`に変更 {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

`etcdserver.EtcdServer`のメンバーフィールドの型は、`*etcdserver.ServerConfig`から`etcdserver.ServerConfig`に変更されました。また、`etcdserver.NewServer`は`*etcdserver.ServerConfig`ではなく`etcdserver.ServerConfig`を受け取るようになりました。

変更前と変更後（例：[k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55)）

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

#### `embed.Config.LogOutput`フィールドの追加 {#added-embedconfiglogoutput-struct}

> [!WARNING]
> v3.4では、このフィールドが`[]string`型の`embed.Config.LogOutputs`に変更されたことに注意してください。詳細は[v3.4アップグレードガイド](/ja/etcd/upgrades/upgrade_3_4/)を参照してください。

`embed.Config`に`LogOutput`フィールドが追加されました。

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

以前は、gRPCサーバーの警告はetcdserverに記録されていました。

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

v3.3以降、gRPCサーバーのログはデフォルトで無効です。

> [!WARNING]
> v3.4では、`embed.Config.SetupLogging`メソッドが非推奨になったことに注意してください。詳細は[v3.4アップグレードガイド](/ja/etcd/upgrades/upgrade_3_4/)を参照してください。

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

gRPCサーバーのログを有効にするには、`embed.Config.Debug`フィールドを`true`に設定します。

#### `/health`エンドポイントのレスポンスの変更 {#changed-health-endpoint-response}

以前は、`[endpoint]:[client-port]/health`が手動でマーシャリングしたJSON値を返していました。3.3では[`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health)構造体を定義するようになりました。

v3.3.0-rc.0、v3.3.0-rc.1、v3.3.0-rc.2では、`etcdhttp.Health`の`"health"`と`"errors"`フィールドがboolean型であったことに注意してください。後方互換性のため、`"health"`フィールドを`string`型に戻し、`"errors"`フィールドを削除しました。追加の正常性情報は、別のAPIで提供される予定です。

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### gRPCゲートウェイのHTTPエンドポイントの変更（`/v3alpha`を`/v3beta`に置き換え） {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

変更前

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

変更後

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3alpha`エンドポイントへのリクエストは`/v3beta`にリダイレクトされ、`/v3alpha`は3.4リリースで削除されます。

#### リクエストの最大サイズ制限の変更 {#changed-maximum-request-size-limits}

3.3では、サーバー側と**クライアント側**の両方でリクエストサイズ制限をカスタマイズできるようになりました。以前のバージョン（v3.2.10、v3.2.11）では、クライアントのレスポンスサイズはわずか4 MiBに制限されていました。

サーバー側のリクエスト制限は、`--max-request-bytes`フラグで設定できます。

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

または、`embed.Config.MaxRequestBytes`フィールドで設定します。

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

**指定しない場合、サーバー側の制限のデフォルトは1.5 MiBです**。

クライアント側のリクエスト制限は、サーバー側の制限に基づいて設定しなければなりません。

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

**指定しない場合、クライアント側の送信制限のデフォルトは2 MiB（1.5 MiB + gRPCのオーバーヘッド分のバイト数）、受信制限のデフォルトは`math.MaxInt32`です**。詳細は[clientv3 godoc](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config)を参照してください。

#### 低水準gRPCクライアントラッパーの関数シグネチャの変更 {#changed-raw-grpc-client-wrapper-function-signatures}

3.3では、`clientv3`のgRPCクライアントラッパーの関数シグネチャが変更されています。この変更は、[メッセージサイズ制限を指定するカスタム`grpc.CallOption`](https://github.com/etcd-io/etcd/pull/9047)をサポートするために必要でした。

変更前と変更後

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

#### clientv3の`Snapshot` APIのエラー型の変更 {#changed-clientv3-snapshot-api-error-type}

以前は、clientv3の`Snapshot` APIが低水準の[`grpc/*status.statusError`]型のエラーを返していました。v3.3では、他のAPIとの一貫性を保つため、これらのエラーを対応する公開エラー型に変換します。

変更前

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

変更後

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

#### `etcdctl lease timetolive`コマンドの出力の変更 {#changed-etcdctl-lease-timetolive-command-output}

以前は、有効期限切れのリースに対して`lease timetolive LEASE_ID`コマンドを実行すると、残り秒数として`-1s`が表示されていました。3.3では、より明確なメッセージを出力します。

変更前


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

変更後

```bash
lease 2d8257079fa1bc0c already expired
```

#### `golang.org/x/net/context`のインポートの変更 {#changed-golangorgxnetcontext-imports}

`clientv3`では`golang.org/x/net/context`が非推奨となりました。プロジェクトが他のコード（etcdが生成したprotocol bufferコードなど）に`golang.org/x/net/context`を取り込み、`github.com/coreos/etcd/clientv3`をインポートしている場合、コンパイルにはGo 1.9+が必要です。

変更前

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

変更後

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### gRPC依存関係の変更 {#changed-grpc-dependency}

3.3では、[grpc/grpc-go](https://github.com/grpc/grpc-go/releases)の`v1.7.5`が必要になりました。

##### `grpclog.Logger`の非推奨化 {#deprecated-grpcloglogger}

`grpclog.Logger`は非推奨となり、代わりに[`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go)を使用します。`clientv3.Logger`は`grpclog.LoggerV2`になりました。

変更前

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

変更後

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### `grpc.ErrClientConnTimeout`の非推奨化 {#deprecated-grpcerrclientconntimeout}

以前は、クライアントの接続タイムアウト時に`grpc.ErrClientConnTimeout`エラーが返されていました。3.3では代わりに`context.DeadlineExceeded`を返します（[#8504](https://github.com/etcd-io/etcd/issues/8504)を参照）。

変更前

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

変更後

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### 公式コンテナーレジストリの変更 {#changed-official-container-registry}

etcdは、主なコンテナーレジストリとして[`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd)を、補助のレジストリとして[`quay.io/coreos/etcd`](https://quay.io/coreos/etcd)を使用するようになりました。

変更前

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

変更後

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### >= v3.3.14へのアップグレード {#upgrades-to--v3314}

[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14)では、クライアントバランサーの実装の差異を最小限に抑えるため、3.4の一部の機能を取り込む必要がありました。このリリースでは、[「最初のetcd-serverが利用できないとkube-apiserver 1.13.xが動作しない」（kubernetes#72102）](https://github.com/kubernetes/kubernetes/issues/72102)を修正しています。

`grpc.ErrClientConnClosing`は[gRPC >= 1.10で非推奨になりました](https://github.com/grpc/grpc-go/pull/1854)。

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

[新しいクライアントバランサー](/ja/etcd/learning/design-client/)は、非同期リゾルバーを使用してgRPCの接続関数にエンドポイントを渡します。そのため、[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14)以降では、基盤となる接続の確立を待つために、接続オプション`grpc.WithBlock`が必要です。

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

変更の全一覧は、[CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md)を参照してください。

### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.3にアップグレードするには、稼働中のクラスターが3.2以降でなければなりません。3.2より前の場合は、3.3にアップグレードする前に[3.2にアップグレード](/ja/etcd/upgrades/upgrade_3_2/)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[etcdのデータをバックアップ](/ja/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。v2データについては、[v2データストアのバックアップ](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore)を参照してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.3にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

注：クラスターにv3データしかなく、v2データがない場合、この制限は適用されません。

クラスターが50MBを超えるv2データセットを提供している場合、新しくアップグレードした各メンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.3にアップグレードすると、クラスターもv3.3にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv3.2のメンバーが残っていれば、クラスターとその動作は「v3.2」のままであり、この混在状態からすべてのメンバーでv3.2のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、すべてのetcdメンバーの[データディレクトリをバックアップ](/ja/etcd/op-guide/maintenance/#snapshot-backup)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.2 etcdクラスターをアップグレードする方法を説明します。

#### 1. アップグレード要件の確認 {#1-check-upgrade-requirements}

クラスターは正常で、v3.2.xで稼働していますか。

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. 既存のetcdプロセスの停止 {#2-stop-the-existing-etcd-process}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

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

問題が発生した場合にダウングレードできるよう、この時点で[etcdのデータをバックアップ](/ja/etcd/op-guide/maintenance/#snapshot-backup)することをお勧めします。

```
$ etcdctl snapshot save backup.db
```

#### 3. etcd v3.3バイナリへの置き換えと新しいetcdプロセスの起動 {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

新しいv3.3のetcdは、自身の情報をクラスターに公開します。

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

新しいv3.3のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

クラスター全体のアップグレードが完了するまでは、アップグレード済みのメンバーに次のような警告が記録されます。これは想定された動作で、すべてのetcdクラスターメンバーをv3.3にアップグレードすると表示されなくなります。

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. 残りのすべてのメンバーで手順2から手順3を繰り返す {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完了 {#5-finish}

すべてのメンバーのアップグレードが完了すると、クラスターは3.3へのアップグレードが成功したことを報告します。

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
