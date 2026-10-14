---
title: etcdを3.1から3.2にアップグレード
weight: 6800
description: etcdを3.1から3.2にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

通常、etcd 3.1から3.2へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v3.1のプロセスを1つずつ停止し、etcd v3.2のプロセスに置き換えます。
 - すべてのプロセスがv3.2で稼働すると、クラスターでv3.2の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

3.2の主な互換性を損なう変更は次のとおりです。

#### `snapshot-count`のデフォルト値の変更 {#changed-default-snapshot-count-value}

`--snapshot-count`を大きくすると、スナップショットを作成するまでより多くのRaftエントリーをメモリーに保持するため、[メモリー使用量が繰り返し増大](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156)します。リーダーが最新のRaftエントリーをより長く保持するので、遅いフォロワーはリーダーのスナップショット作成前に追いつくための時間を多く確保できます。`--snapshot-count`は、メモリー使用量の増加と遅いフォロワーの可用性向上とのトレードオフです。

v3.2以降、`--snapshot-count`のデフォルト値は[10,000から100,000に変更されました](https://github.com/etcd-io/etcd/pull/7160)。

#### gRPC依存関係の変更（>=3.2.10） {#changed-grpc-dependency-3210}

3.2.10以降では、[grpc/grpc-go](https://github.com/grpc/grpc-go/releases)の`v1.7.5`が必要になりました（<=3.2.9では`v1.2.1`が必要です）。

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

以前は、クライアントの接続タイムアウト時に`grpc.ErrClientConnTimeout`エラーが返されていました。3.2では代わりに`context.DeadlineExceeded`を返します（[#8504](https://github.com/etcd-io/etcd/issues/8504)を参照）。

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

#### リクエストの最大サイズ制限の変更（>=3.2.10） {#changed-maximum-request-size-limits-3210}

3.2.10と3.2.11では、サーバー側のリクエストサイズ制限をカスタマイズできます。>=3.2.12では、サーバー側と**クライアント側**の両方でリクエストサイズ制限をカスタマイズできます。以前のバージョン（v3.2.10、v3.2.11）では、クライアントのレスポンスサイズはわずか4 MiBに制限されていました。

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

#### 低水準gRPCクライアントラッパーの変更 {#changed-raw-grpc-client-wrappers}

3.2.12以降では、`clientv3`のgRPCクライアントラッパーの関数シグネチャが変更されています。この変更は、[メッセージサイズ制限を指定するカスタム`grpc.CallOption`](https://github.com/etcd-io/etcd/pull/9047)をサポートするために必要でした。

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

#### `clientv3.Lease.TimeToLive` APIの変更 {#changed-clientv3leasetimetolive-api}

以前は、`clientv3.Lease.TimeToLive` APIに存在しないリースIDを指定すると、`lease.ErrLeaseNotFound`が返されていました。3.2では代わりにレスポンスでTTL=-1を返し、エラーは返しません（[#7305](https://github.com/etcd-io/etcd/pull/7305)を参照）。

変更前

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

変更後

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### `clientv3.NewFromConfigFile`を`clientv3.yaml.NewConfig`に移動 {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile`は`yaml.NewConfig`に移動しました。

変更前

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

変更後

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### `--listen-peer-urls`と`--listen-client-urls`の変更 {#change-in---listen-peer-urls-and---listen-client-urls}

ドメイン名はネットワークインターフェースのバインド先として無効であるため、3.2では`--listen-peer-urls`と`--listen-client-urls`のドメイン名を拒否するようになりました（3.1では警告の表示のみでした）。これらのURLが`scheme://IP:port`の正しい形式であることを確認してください。

背景については、[issue #6336](https://github.com/etcd-io/etcd/issues/6336)を参照してください。

### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.2にアップグレードするには、稼働中のクラスターが3.1以降でなければなりません。3.1より前の場合は、3.2にアップグレードする前に[3.1にアップグレード](/ja/etcd/upgrades/upgrade_3_1)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[etcdのデータをバックアップ](/ja/etcd/op-guide/maintenance#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。v2データについては、[v2データストアのバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)を参照してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.2にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

注：クラスターにv3データしかなく、v2データがない場合、この制限は適用されません。

クラスターが50MBを超えるv2データセットを提供している場合、新しくアップグレードした各メンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.2にアップグレードすると、クラスターもv3.2にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv3.1のメンバーが残っていれば、クラスターとその動作は「v3.1」のままであり、この混在状態からすべてのメンバーでv3.1のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、すべてのetcdメンバーの[データディレクトリをバックアップ](/ja/etcd/op-guide/maintenance#snapshot-backup)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.1 etcdクラスターをアップグレードする方法を説明します。

#### 1. アップグレード要件の確認 {#1-check-upgrade-requirements}

クラスターは正常で、v3.1.xで稼働していますか。

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. 既存のetcdプロセスの停止 {#2-stop-the-existing-etcd-process}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

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

問題が発生した場合にダウングレードできるよう、この時点で[etcdのデータをバックアップ](/ja/etcd/op-guide/maintenance#snapshot-backup)することをお勧めします。

```
$ etcdctl snapshot save backup.db
```

#### 3. etcd v3.2バイナリへの置き換えと新しいetcdプロセスの起動 {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

新しいv3.2のetcdは、自身の情報をクラスターに公開します。

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

新しいv3.2のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

クラスター全体のアップグレードが完了するまでは、アップグレード済みのメンバーに次のような警告が記録されます。これは想定された動作で、すべてのetcdクラスターメンバーをv3.2にアップグレードすると表示されなくなります。

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. 残りのすべてのメンバーで手順2から手順3を繰り返す {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完了 {#5-finish}

すべてのメンバーのアップグレードが完了すると、クラスターは3.2へのアップグレードが成功したことを報告します。

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
