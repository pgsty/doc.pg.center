---
title: "gRPCプロキシー"
weight: 4350
description: "gRPC層で動作するステートレスなetcdリバースプロキシー"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/grpc_proxy.md"
---

gRPCプロキシーは、gRPC層（L7）で動作するステートレスなetcdリバースプロキシーです。中核となるetcdクラスターの処理負荷を減らすために設計されています。水平スケーラビリティーのために、監視APIとリースAPIのリクエストを集約します。また、過剰なリクエストを送るクライアントからクラスターを守るため、キー範囲のリクエストをキャッシュします。

gRPCプロキシーは、複数のetcdサーバーのエンドポイントに対応します。起動時に使用するエンドポイントをランダムに1つ選び、その障害を検出するまで、すべてのリクエストをそのエンドポイントで処理します。障害を検出すると、ほかに利用可能なエンドポイントがあれば切り替え、クライアントが障害を意識せずに済むようにします。将来は、重み付きラウンドロビンなど、ほかの再試行方針に対応する可能性もあります。

## スケーラブルな監視API {#scalable-watch-api}

gRPCプロキシーは、同じキーや範囲を監視する複数のクライアントウォッチャー（`c-watchers`）を、etcdサーバーに接続する1つのウォッチャー（`s-watcher`）に集約します。プロキシーは、`s-watcher`からのすべてのイベントを`c-watchers`に配信します。

N個のクライアントが同じキーを監視するとき、1つのgRPCプロキシーでetcdサーバーの監視負荷をNから1に減らせます。複数のgRPCプロキシーを配置すれば、サーバーの負荷をさらに分散できます。

次の例では、3つのクライアントがキーAを監視します。gRPCプロキシーは3つのウォッチャーを集約し、etcdサーバーに接続する1つのウォッチャーを作成します。

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### 制限事項 {#limitations}

複数のクライアントウォッチャーを効率よく1つに集約するため、gRPCプロキシーは可能であれば、新しい`c-watchers`を既存の`s-watcher`にまとめます。この集約先の`s-watcher`は、ネットワークの遅延やバッファー内の未配信イベントによって、etcdサーバーと同期していないことがあります。監視するリビジョンを指定しない場合、gRPCプロキシーは`c-watcher`がストアの最新リビジョンから監視を開始することを保証しません。たとえば、リビジョン1000のetcdサーバーをクライアントが監視すると、リビジョン1000から始まります。一方、gRPCプロキシーを介して監視すると、リビジョン990から始まる場合があります。

取り消しにも同様の制限があります。ウォッチャーを取り消したとき、etcdサーバーのリビジョンが取り消しレスポンスのリビジョンより大きい場合があります。

この2つの制限は、ほとんどの用途では問題にならないはずです。将来は、より正確なリビジョンのレスポンスを得るため、ウォッチャーにgRPCプロキシーを迂回させる追加オプションが用意される可能性があります。

## スケーラブルなリースAPI {#scalable-lease-api}

リースを維持するには、クライアントはetcdサーバーへのgRPCストリームを少なくとも1つ確立し、定期的にハートビートを送信しなければなりません。多くのクライアントにまたがって大量のリース操作が行われる場合、これらのストリームがCPUの過剰な使用につながることがあります。中核クラスターのストリーム総数を減らすため、プロキシーはリースストリームの集約に対応しています。

N個のクライアントがリースを更新するとき、1つのgRPCプロキシーでetcdサーバーのストリーム負荷をNから1に減らせます。gRPCプロキシーを追加し、複数のプロキシーにストリームをさらに分散することもできます。

次の例では、3つのクライアントが独立した3つのリース（`L1`、`L2`、`L3`）を更新します。gRPCプロキシーは、3つのクライアント側リースストリーム（`c-streams`）を、etcdサーバーに接続する1つのリース維持ストリーム（`s-stream`）に集約します。プロキシーは、クライアント側のリースハートビートをc-streamsからs-streamに転送し、対応するc-streamsにレスポンスを返します。

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## 過剰なリクエストを送るクライアントからの保護 {#abusive-clients-protection}

gRPCプロキシーは、一貫性の要件に違反しない場合に、リクエストのレスポンスをキャッシュします。これにより、高速なforループでリクエストを繰り返すクライアントからetcdサーバーを保護できます。

## etcd gRPCプロキシーの起動 {#start-etcd-grpc-proxy}

次の静的エンドポイントを持つetcdクラスターを考えます。

|名前|アドレス|ホスト名|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

次のコマンドで、これらの静的エンドポイントを使用するetcd gRPCプロキシーを起動します。

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

etcd gRPCプロキシーは起動し、ポート2379でリッスンします。クライアントのリクエストは、上記の3つのエンドポイントのいずれかに転送されます。

プロキシーを通じてリクエストを送信します。

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## クライアントエンドポイントの同期と名前解決 {#client-endpoint-synchronization-and-name-resolution}

プロキシーは、ユーザー定義のエンドポイントに書き込むことで、自身のエンドポイントをディスカバリー用に登録できます。これには2つの目的があります。1つは、クライアントがプロキシーのエンドポイント群と自身のエンドポイントを同期し、高可用性を得ることです。もう1つは、etcdの[gRPC名前解決](/ja/etcd/dev-guide/grpc_naming/)にエンドポイントを提供することです。

ユーザー定義の接頭辞を指定して、プロキシーを登録します。

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

メンバー一覧を要求すると、プロキシーは自身のすべてのメンバーを返します。

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

これにより、クライアントはSyncを通じてプロキシーのエンドポイントを自動検出できます。

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

一方、リゾルバーの接頭辞を指定せずにプロキシーを構成すると、

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

grpc-proxyのメンバー一覧APIは、自身の`advertise-client-url`を返します。

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## 名前空間 {#namespacing}

アプリケーションがキー空間全体を完全に制御できることを想定していても、etcdクラスターはほかのアプリケーションと共有している場合があります。すべてのアプリケーションが互いに干渉せずに動作できるよう、プロキシーはキー空間を分割し、各クライアントからはキー空間全体にアクセスできるように見せられます。`--namespace`フラグを指定すると、プロキシーに入るすべてのクライアントリクエストのキーに、ユーザー定義の接頭辞を付けます。etcdクラスターへのアクセスはその接頭辞の配下に限定し、プロキシーが返すレスポンスからは接頭辞を取り除きます。クライアントには、接頭辞が存在しないように見えます。

プロキシーに名前空間を設定するには、`--namespace`を指定して起動します。

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

以後、プロキシーへのアクセスには、etcdクラスター上で透過的に接頭辞が付きます。

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## TLSの終端 {#tls-termination}

gRPCプロキシーで暗号化されていないローカルエンドポイントを提供し、保護されたetcdクラスターからのTLSを終端します。

試すには、まずクライアント接続にHTTPSを使う単一メンバーのetcdクラスターを起動します。

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

クライアントポートがHTTPSを提供していることを確認します。

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

次に、クライアント証明書を使ってetcdエンドポイント`https://localhost:2379`に接続し、`localhost:12379`でgRPCプロキシーを起動します。

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

最後に、HTTPでプロキシーにキーを書き込み、TLSの終端をテストします。

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## メトリクスと健全性 {#metrics-and-health}

gRPCプロキシーは、`--endpoints`で指定したetcdメンバーの`/health`とPrometheusの`/metrics`エンドポイントを公開します。`--metrics-addr`フラグで追加のURLを定義し、`/metrics`と`/health`の両方に応答させることもできます。

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### 既知の問題 {#known-issue}

プロキシーのメインインターフェースは、HTTP2とHTTP/1.1の両方を提供します。上記の例のようにTLSを設定したプロキシーのリッスンインターフェースにcURLなどのクライアントでアクセスする場合、`/metrics`や`/health`を取得するには、リクエストでプロトコルをHTTP/1.1に明示的に設定する必要があります。`--metrics-addr`フラグによる追加インターフェースには、この要件はありません。

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
