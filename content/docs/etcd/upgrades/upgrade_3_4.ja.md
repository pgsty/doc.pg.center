---
title: etcdを3.3から3.4にアップグレード
weight: 6700
description: etcdを3.3から3.4にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
aliases: [/etcd/upgrades/upgrade_3_4/]
---

通常、etcd 3.3から3.4へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v3.3のプロセスを1つずつ停止し、etcd v3.4のプロセスに置き換えます。
 - すべてのプロセスがv3.4で稼働すると、クラスターでv3.4の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。



### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

3.4の主な互換性を損なう変更は次のとおりです。

#### `ETCDCTL_API=3 etcdctl`をデフォルトに変更 {#make-etcdctl_api3-etcdctl-default}

`ETCDCTL_API=3`がデフォルトになりました。

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

#### `etcd --enable-v2=false`をデフォルトに変更 {#make-etcd---enable-v2false-default}

[`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935)がデフォルトになりました。

つまり、`etcd --enable-v2=true`を指定しない限り、etcd v3.4サーバーはv2 APIリクエストを処理しません。

v2 APIを使用していた場合は、v3.4で必ずv2 APIを有効にしてください。

```diff
-etcd
+etcd --enable-v2=true
```

その他のHTTP APIは引き続き動作します（例：`[CLIENT-URL]/metrics`、`[CLIENT-URL]/health`、v3 gRPCゲートウェイ）。

#### `etcd --ca-file`および`etcd --peer-ca-file`フラグの非推奨化 {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

`--ca-file`および`--peer-ca-file`フラグは非推奨です。これらはv2.1から非推奨となっています。

このパラメーターを設定すると、`--client-cert-auth`の値にかかわらず、クライアント証明書認証も自動的に有効になることに注意してください。

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### `grpc.ErrClientConnClosing`エラーの非推奨化 {#deprecated-grpcerrclientconnclosing-error}

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

#### クライアントの接続に`grpc.WithBlock`が必要 {#require-grpcwithblock-for-client-dial}

[新しいクライアントバランサー](/ja/docs/etcd/learning/design-client/)は、非同期リゾルバーを使用してgRPCの接続関数にエンドポイントを渡します。そのため、v3.4クライアントでは、基盤となる接続の確立を待つために、接続オプション`grpc.WithBlock`が必要です。

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

#### Prometheusメトリクス`etcd_debugging_mvcc_db_total_size_in_bytes`の非推奨化 {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.4では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_db_total_size_in_bytes`を`etcd_mvcc_db_total_size_in_bytes`に昇格させています。

後方互換性のため、v3.4では`etcd_debugging_mvcc_db_total_size_in_bytes`も引き続き提供されます。v3.5で完全に非推奨になります。

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_put_total`の非推奨化 {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.4では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_put_total`を`etcd_mvcc_put_total`に昇格させています。

後方互換性のため、v3.4では`etcd_debugging_mvcc_put_total`も引き続き提供されます。v3.5で完全に非推奨になります。

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_delete_total`の非推奨化 {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.4では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_delete_total`を`etcd_mvcc_delete_total`に昇格させています。

後方互換性のため、v3.4では`etcd_debugging_mvcc_delete_total`も引き続き提供されます。v3.5で完全に非推奨になります。

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_txn_total`の非推奨化 {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.4では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_txn_total`を`etcd_mvcc_txn_total`に昇格させています。

後方互換性のため、v3.4では`etcd_debugging_mvcc_txn_total`も引き続き提供されます。v3.5で完全に非推奨になります。

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_range_total`の非推奨化 {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.4では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_range_total`を`etcd_mvcc_range_total`に昇格させています。

後方互換性のため、v3.4では`etcd_debugging_mvcc_range_total`も引き続き提供されます。v3.5で完全に非推奨になります。

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### `etcd --log-output`フラグの非推奨化（現在は`--log-outputs`） {#deprecating-etcd---log-output-flag-now---log-outputs}

複数のログ出力をサポートするため、[`etcd --log-output`を`--log-outputs`に改名しました](https://github.com/etcd-io/etcd/pull/9624)。**`etcd --logger=capnslog`は複数のログ出力をサポートしません。**

**`etcd --log-output`**はv3.5で非推奨になります。**`etcd --logger=capnslog`はv3.5で非推奨になります**。

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4では、構造化ログと複数のログ出力に対応するため、`etcd --logger=zap --log-outputs=stderr`のサポートを追加しています。主な狙いは、障害が発生してからサーバーログを調べるのではなく、etcdの監視を自動化することです。今後の開発ではetcdのログ出力をできるだけ少なくし、メトリクスとアラートでetcdを監視しやすくします。**`etcd --logger=capnslog`はv3.5で非推奨になります**。

#### `etcd --config-file`の`log-outputs`フィールドの型を`[]string`に変更 {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

`log-outputs`（以前のフィールド名は`log-output`）が複数のライターを受け付けるようになったため、etcdの設定YAMLファイルの`log-outputs`フィールドは、次のように`[]string`型に変更しなければなりません。

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### `embed.Config.LogOutput`を`embed.Config.LogOutputs`に改名 {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

複数のログ出力をサポートするため、[**`embed.Config.LogOutput`**を**`embed.Config.LogOutputs`**に改名しました](https://github.com/etcd-io/etcd/pull/9624)。また、複数のログ出力をサポートするため、[`embed.Config.LogOutput`の型を`string`から`[]string`に変更しました](https://github.com/etcd-io/etcd/pull/9579)。

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5で`capnslog`を非推奨化 {#v35-deprecates-capnslog}

**v3.5では、`capnslog`用の`etcd --log-package-levels`フラグが非推奨になります**。`etcd --logger=zap --log-outputs=stderr`がデフォルトになります。**v3.5では、`[CLIENT-URL]/config/local/log`エンドポイントが非推奨になります。**

```diff
-etcd
+etcd --logger zap
```

#### `etcd --debug`フラグの非推奨化（現在は`--log-level=debug`） {#deprecating-etcd---debug-flag-now---log-leveldebug}

v3.4では、[`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947)フラグが非推奨になります。代わりに`etcd --log-level=debug`フラグを使用してください。

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### `pkg/transport.TLSInfo.CAFile`フィールドの非推奨化 {#deprecated-pkgtransporttlsinfocafile-field}

`pkg/transport.TLSInfo.CAFile`フィールドは非推奨になりました。

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

#### `embed.Config.SnapCount`を`embed.Config.SnapshotCount`に変更 {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

フラグ名`etcd --snapshot-count`と一貫性を持たせるため、`embed.Config.SnapCount`フィールドは`embed.Config.SnapshotCount`に改名されました。

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### `etcdserver.ServerConfig.SnapCount`を`etcdserver.ServerConfig.SnapshotCount`に変更 {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

フラグ名`etcd --snapshot-count`と一貫性を持たせるため、`etcdserver.ServerConfig.SnapCount`フィールドは`etcdserver.ServerConfig.SnapshotCount`に改名されました。

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### `wal`パッケージの関数シグネチャの変更 {#changed-function-signature-in-package-wal}

構造化ロガーをサポートするため、`wal`の関数シグネチャを変更しました。

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

#### `pkg/adt`パッケージの`IntervalTree`型の変更 {#changed-intervaltree-type-in-package-pkgadt}

`pkg/adt.IntervalTree`は`interface`として定義されるようになりました。

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### `embed.Config.SetupLogging`の非推奨化 {#deprecated-embedconfigsetuplogging}

誤ったログ設定を防ぐため、`embed.Config.SetupLogging`は削除され、ログ設定は自動的に行われるようになりました。

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### gRPCゲートウェイのHTTPエンドポイントの変更（`/v3beta`を`/v3`に置き換え） {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

変更前

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

変更後

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3beta`エンドポイントへのリクエストは`/v3`にリダイレクトされ、`/v3beta`は3.5リリースで削除されます。

#### コンテナーイメージタグの非推奨化 {#deprecated-container-image-tags}

`latest`およびマイナーバージョンのイメージタグは非推奨になりました。

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

### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.4にアップグレードするには、稼働中のクラスターが3.3以降でなければなりません。3.3より前の場合は、3.4にアップグレードする前に[3.3にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_3/)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。v2データについては、[v2データストアのバックアップ](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore)を参照してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.4にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

注：クラスターにv3データしかなく、v2データがない場合、この制限は適用されません。

クラスターが50MBを超えるv2データセットを提供している場合、新しくアップグレードした各メンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.4にアップグレードすると、クラスターもv3.4にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv3.3のメンバーが残っていれば、クラスターとその動作は「v3.3」のままであり、この混在状態からすべてのメンバーでv3.3のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.3 etcdクラスターをアップグレードする方法を説明します。

#### 手順1：アップグレード要件の確認 {#step-1-check-upgrade-requirements}

クラスターは正常で、v3.3.xで稼働していますか。

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

#### 手順2：リーダーからスナップショットバックアップをダウンロード {#step-2-download-snapshot-backup-from-leader}

問題が発生した場合にダウングレードできるよう、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。

etcdのリーダーには最新のアプリケーションデータがあることが保証されているため、リーダーからスナップショットを取得します。

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

#### 手順3：既存のetcdサーバーを1つ停止 {#step-3-stop-one-existing-etcd-server}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

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

#### 手順4：同じ設定でetcdサーバーを再起動 {#step-4-restart-the-etcd-server-with-same-configuration}

同じ設定で、新しいetcdバイナリを使用してetcdサーバーを再起動します。

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

新しいv3.4のetcdは、自身の情報をクラスターに公開します。この時点では、クラスターは引き続き全メンバーに共通する最も低いバージョンであるv3.3のプロトコルで動作します。

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

新しいv3.4のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

クラスター全体のアップグレードが完了するまでは、未アップグレードのメンバーに次のような警告が記録されます。

これは想定された動作で、すべてのetcdクラスターメンバーをv3.4にアップグレードすると表示されなくなります。

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### 手順5：残りのメンバーで*手順3*と*手順4*を繰り返す {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

すべてのメンバーのアップグレードが完了すると、クラスターは3.4へのアップグレードが成功したことを報告します。

メンバー1：

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

メンバー2：

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

メンバー3：

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
