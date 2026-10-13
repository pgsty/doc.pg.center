---
title: "クラスター構成ガイド"
weight: 4150
description: "etcdクラスターのブートストラップ：静的構成、etcdディスカバリー、DNSディスカバリー"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/clustering.md"
aliases: [/etcd/op-guide/clustering/]
---

## 概要 {#overview}

etcdクラスターを静的に起動するには、各メンバーがクラスター内のほかのメンバーを把握している必要があります。ただし、メンバーのIPアドレスを事前に把握できない場合もあります。その場合は、ディスカバリーサービスを利用してクラスターをブートストラップできます。

etcdクラスターの起動後、メンバーの追加や削除は[実行時再構成][runtime-conf]で行います。その設計をより深く理解するには、[実行時構成の設計ドキュメント][runtime-reconf-design]を参照することを推奨します。

このガイドでは、etcdクラスターをブートストラップする次の方法を説明します。

* [静的構成](#static)
* [etcdディスカバリー](#etcd-discovery)
* [DNSディスカバリー](#dns-discovery)

いずれの方法でも、次の3台のマシンでetcdクラスターを作成します。

|名前|アドレス|ホスト名|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## 静的構成 {#static}

起動前にクラスターメンバー、そのアドレス、クラスターサイズがわかっているため、`initial-cluster`フラグを設定してオフラインでブートストラップを構成できます。各マシンに、次の環境変数またはコマンドラインを指定します。

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

`initial-cluster`に指定するURLは、*通知するピアURL*です。各ノードの`initial-advertise-peer-urls`の値と一致させることを推奨します。

テストのために同じ設定で複数のクラスターを起動する場合や、単一のクラスターを作成、破棄する場合は、各クラスターに一意の`initial-cluster-token`を指定することを強く推奨します。これにより、ほかの設定が完全に同じでも、etcdは各クラスターに一意のクラスターIDとメンバーIDを生成できます。クラスター間の相互作用を防ぎ、それによる破損からetcdを保護できます。

etcdは、クライアントのトラフィックを受け付けるため、[`listen-client-urls`][conf-listen-client]でリッスンします。etcdメンバーは、[`advertise-client-urls`][conf-adv-client]に指定されたURLを、ほかのメンバー、プロキシー、クライアントに通知します。対象のクライアントから`advertise-client-urls`に到達できることを確認してください。リモートクライアントからetcdにアクセスする必要があるのに、`advertise-client-urls`をlocalhostに設定したり、デフォルトのままにしたりするのは、よくある誤りです。

各マシンで、次のフラグを指定してetcdを起動します。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

`--initial-cluster`で始まるコマンドラインパラメーターは、etcdの2回目以降の実行では無視されます。初回のブートストラップ後は、環境変数やコマンドラインフラグを削除してかまいません。後から構成を変更する場合（メンバーの追加や削除など）は、[実行時構成][runtime-conf]ガイドを参照してください。

### TLS {#tls}

etcdは、TLSプロトコルによる暗号化通信に対応します。TLSチャネルは、ピア間のクラスター内部通信とクライアントのトラフィックの両方を暗号化できます。このセクションでは、ピアとクライアントにTLSを使うクラスターの設定例を示します。etcdのTLS対応の詳細は、[セキュリティーガイド][security-guide]を参照してください。

#### 自己署名証明書 {#self-signed-certificates}

自己署名証明書を使うクラスターは、通信を暗号化するとともに接続を認証します。そのようなクラスターを起動するには、各メンバーが、共通のクラスターCA証明書（`ca.crt`）で署名された一意の鍵ペア（`member.crt`、`member.key`）を持ち、ピア接続とクライアント接続の両方に使用することを推奨します。証明書は、etcdの[TLS設定例][tls-setup]に従って生成できます。

各マシンで、次のフラグを指定してetcdを起動します。

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### 証明書の自動生成 {#automatic-certificates}

暗号化通信が必要でも接続の認証は不要な場合、etcdに鍵を自動生成させることができます。初期化時に、各メンバーは通知するIPアドレスとホスト名に基づいて、自身の鍵を作成します。

各マシンで、次のフラグを指定してetcdを起動します。

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### エラーの例 {#error-cases}

次の例では、新しいホストをノード一覧に含めていません。新しいクラスターの場合は、初期クラスターメンバーの一覧に、このノードを*追加しなければなりません*。

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

この例では、ノードinfra0を、クラスター一覧のアドレス（10.0.1.10:2380）と異なるアドレス（127.0.0.1:2380）に割り当てようとしています。このノードが複数のアドレスでリッスンする場合は、すべてのアドレスを"initial-cluster"設定に*反映しなければなりません*。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

異なる設定引数で構成されたピアがこのクラスターに参加しようとすると、etcdはクラスターIDの不一致を報告して終了します。

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## ディスカバリー {#discovery}

クラスターピアのIPアドレスを事前に把握できない場合があります。クラウドプロバイダーの利用時や、ネットワークがDHCPを使う場合にはよくあります。その場合は、静的構成を指定する代わりに、既存のetcdクラスターを使って新しいクラスターをブートストラップします。この処理を「ディスカバリー」と呼びます。

ディスカバリーには、次の2つの方法を使用できます。

* etcdディスカバリーサービス
* DNS SRVレコード

### etcdディスカバリー {#etcd-discovery}

> [!NOTE]
> このセクションのディスカバリーサービスの例は、etcd 3.7で削除された旧v2プロトコルを説明しています。新しいv3.7クラスターには、[v3ディスカバリー](/ja/docs/etcd/dev-internal/discovery_protocol/)、またはこのガイドの静的構成やDNS SRVによるブートストラップ方法を使用してください。

ディスカバリーサービスプロトコルの設計をより深く理解するには、その[ドキュメント][discovery-proto]を参照することを推奨します。

#### ディスカバリーURLの有効期間 {#lifetime-of-a-discovery-url}

ディスカバリーURLは、etcdクラスターを一意に識別します。既存のURLを再利用せず、各etcdインスタンスで新しいURLを共有して、新しいクラスターをブートストラップします。

また、ディスカバリーURLはクラスターの初回ブートストラップにのみ使用することを推奨します。稼働開始後にメンバー構成を変更するには、[実行時再構成][runtime-conf]ガイドを参照してください。

#### 独自のetcdディスカバリーサービス {#custom-etcd-discovery-service}

ディスカバリーでは、既存のクラスターを使って新しいクラスターをブートストラップします。非公開のetcdクラスターを使う場合は、次のようにURLを作成します。

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

このURLにsizeキーを設定することで、想定するクラスターサイズが3のディスカバリーURLを作成します。

この場合に使用するURLは`https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`で、etcdメンバーは起動時に`https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`ディレクトリで登録を行います。

**各メンバーのnameフラグには、異なる名前を指定しなければなりません。`Hostname`や`machine-id`が適しています。同じ名前を指定すると、重複によってディスカバリーが失敗します。**

各メンバーで、対応するフラグを指定してetcdを起動します。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

各メンバーは独自のetcdディスカバリーサービスに登録し、すべてのマシンの登録が完了するとクラスターを開始します。

#### 公開etcdディスカバリーサービス {#public-etcd-discovery-service}

利用できる既存のクラスターがなければ、`discovery.etcd.io`の公開ディスカバリーサービスを使います。"new"エンドポイントで専用のディスカバリーURLを作成するには、次のコマンドを使用します。

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

これにより、初期サイズが3メンバーのクラスターを作成します。サイズを指定しない場合は、デフォルトの3を使用します。

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**各メンバーのnameフラグには、異なる名前を指定しなければなりません。同じ名前を指定すると、重複によってディスカバリーが失敗します。`Hostname`や`machine-id`が適しています。**

各メンバーで、対応するフラグを指定してetcdを起動します。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

各メンバーはディスカバリーサービスに登録し、すべてのメンバーの登録が完了するとクラスターを開始します。

環境変数`ETCD_DISCOVERY_PROXY`を使うと、etcdはHTTPプロキシーを経由してディスカバリーサービスに接続します。

#### エラーと警告の例 {#error-and-warning-cases}

##### ディスカバリーサーバーのエラー {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### 警告 {#warnings}

これは、このマシンではディスカバリーURLを無視するという、無害な警告です。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### DNSディスカバリー {#dns-discovery}

DNSの[SRVレコード][rfc-srv]をディスカバリーに使用できます。
`--discovery-srv`フラグで、ディスカバリー用SRVレコードを検索するDNSドメイン名を設定できます。
`--discovery-srv example.com`を指定すると、次の順にDNS SRVレコードを検索します。

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

`_etcd-server-ssl._tcp.example.com`が見つかると、etcdはTLSでのブートストラップを試みます。

クライアントがetcdクラスターを発見できるよう、次のDNS SRVレコードをこの順に検索します。

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

`_etcd-client-ssl._tcp.example.com`が見つかると、クライアントはSSL/TLSでetcdクラスターとの通信を試みます。

etcdでTLSを使う場合、SSL証明書のDNS SANにホスト名とともにディスカバリーSRVレコード（`example.com`など）を含めなければなりません。含めないと、次のようなログメッセージを出力してクラスター構成に失敗します。

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

etcdで独自の認証局を使わずにTLSを使う場合、ディスカバリードメイン（example.comなど）はSRVレコードのドメイン（infra1.example.comなど）と一致しなければなりません。これは、別のドメインを指す偽のSRVレコードを使う攻撃を軽減するためです。そのドメインは、PKI上は有効な証明書を持っていても、未知の第三者に管理されている可能性があります。

`-discovery-srv-name`フラグを使うと、ディスカバリーで問い合わせるSRV名に接尾辞を追加できます。
同じドメイン内の複数のetcdクラスターを区別するために使います。
たとえば、`discovery-srv=example.com`と`-discovery-srv-name=foo`を設定すると、次のDNS SRVクエリーを実行します。

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### DNS SRVレコードの作成 {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### DNSを使ったetcdクラスターのブートストラップ {#bootstrap-the-etcd-cluster-using-dns}

etcdのクラスターメンバーは、ドメイン名またはIPアドレスを通知できます。ブートストラップ処理はDNS Aレコードを解決します。
3.2以降、`--listen-peer-urls`と`--listen-client-urls`は、ネットワークインターフェースのバインドにドメイン名を指定すると拒否します（3.1では警告を出力します）。

`--initial-advertise-peer-urls`の名前解決後のアドレスは、SRVターゲットを名前解決したアドレスのいずれかと*一致しなければなりません*。etcdメンバーは、このアドレスを読み取り、SRVレコードが定義するクラスターに属するかどうかを判断します。

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

ドメイン名の代わりにIPアドレスを使って、クラスターをブートストラップすることもできます。

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

v3.1.0以降（v3.2.9を除く）、`etcd --discovery-srv=example.com`をTLSとともに設定すると、サーバーは、提供された証明書のSubject Alternative Name（SAN）フィールドにルートドメイン`example.com`が含まれる場合にのみ、ピアやクライアントを認証します。[DNS SRVに関する注意][security-guide-dns-srv]を参照してください。

### ゲートウェイ {#gateway}

etcdゲートウェイは、ネットワークデータをetcdクラスターに転送する単純なTCPプロキシーです。詳しくは[ゲートウェイガイド][gateway]を参照してください。

### プロキシー {#proxy}

以前のetcdリリースでは、`--proxy`によるv2専用の[プロキシーモード][proxy]をサポートしていました。このモードは削除され、etcd 3.7では利用できません。v3 APIには[gRPCプロキシー](/ja/docs/etcd/op-guide/grpc_proxy/)を使用してください。

過去のv2プロキシーのデプロイについては、[etcd 2.3リリースのクラスター構成ドキュメント][clustering_etcd2]を参照してください。

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /ja/docs/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /ja/docs/etcd/op-guide/configuration/#member
[discovery-proto]: /ja/docs/etcd/dev-internal/discovery_protocol/
[gateway]: /ja/docs/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /ja/docs/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /ja/docs/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /ja/docs/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /ja/docs/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
