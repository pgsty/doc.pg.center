---
title: gRPCの名前解決と検出
weight: 3500
description: "go-grpc：etcdをバックエンドとしてgRPCエンドポイントを解決する"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/grpc_naming.md"
aliases: [/etcd/dev-guide/grpc_naming/]
---

etcdは、etcdからエンドポイントを取得してgRPCサービスを検出する代替の名前システムを、gRPCリゾルバーで提供します。その仕組みは、サービス名を接頭辞に持つキーの更新の監視に基づいています。

この機能は、grpc-goでまだ実験的な[google.golang.org/grpc/resolver][]パッケージに依存しているため、実験的機能です。

## go-grpcでetcdの検出機能を使う {#using-etcd-discovery-with-go-grpc}

etcdクライアントは、etcdをバックエンドとしてgRPCエンドポイントを解決するgRPCリゾルバーを提供します。リゾルバーはetcdクライアントで初期化します。

```go
import (
	clientv3 "go.etcd.io/etcd/client/v3"
	etcdnaming "go.etcd.io/etcd/client/v3/naming/resolver"

	"google.golang.org/grpc"
)

...

cli, err := clientv3.NewFromURL("http://localhost:2379")
if err != nil {
    // ...
}
r, err := etcdnaming.NewBuilder(cli)
if err != nil {
    // ...
}
conn, gerr := grpc.NewClient("my-service", grpc.WithResolvers(r), ...)
```

## サービスエンドポイントの管理 {#managing-service-endpoints}

etcdリゾルバーは、解決対象に"/"を付けた接頭辞（例："foo/bar/my-service/"）の下にあるすべてのキーのうち、
JSONでエンコードされた値（従来はgo-grpcの`naming.Update`）を持つものを、サービスエンドポイントの候補として扱います。
新しいキーを作成するとエンドポイントがサービスに追加され、キーを削除するとサービスから削除されます。

### エンドポイントの追加 {#adding-an-endpoint}

`etcdctl`で新しいエンドポイントをサービスに追加できます。

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

etcdクライアントの`endpoints.Manager`メソッドでも、`Addr`に対応するキーを使って新しいエンドポイントを登録できます。

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
複数のエンドポイントを持つサービスへの接続時にラウンドロビン負荷分散を有効にするには、grpc内蔵の
ラウンドロビンロードバランサーを使用するように接続を設定します。

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### エンドポイントの削除 {#deleting-an-endpoint}

`etcdctl`でホストをサービスから削除できます。

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

etcdクライアントの`endpoints.Manager`メソッドでも、エンドポイントを削除できます。

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### リース付きのエンドポイント登録 {#registering-an-endpoint-with-a-lease}

リース付きでエンドポイントを登録すると、ホストがキープアライブのハートビートを維持できなくなった場合（マシンの故障など）に、そのホストがサービスから確実に削除されます。

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
Goでは、次のように記述します。

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### エンドポイントのアトミックな更新 {#atomically-updating-endpoints}

1つのトランザクションで複数のエンドポイントを変更するには、`endpoints.Manager`を直接使用できます。

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
