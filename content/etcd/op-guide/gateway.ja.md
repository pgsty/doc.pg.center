---
title: "etcdゲートウェイ"
weight: 4300
description: "etcdゲートウェイの用途と設定方法"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/gateway.md"
---

## etcdゲートウェイとは {#what-is-etcd-gateway}

etcdゲートウェイは、ネットワークデータをetcdクラスターに転送する単純なTCPプロキシーです。状態を持たず、透過的に動作し、クライアントのリクエストを検査したりクラスターのレスポンスに介入したりしません。TLS接続の終端、クライアントに代わるTLSハンドシェイク、接続が保護されているかの検証も行いません。

ゲートウェイは複数のetcdサーバーのエンドポイントに対応し、単純なラウンドロビン方式で動作します。利用可能なエンドポイントだけに転送し、クライアントが障害を意識せずに済むようにします。将来は、重み付きラウンドロビンなど、ほかの再試行方針に対応する可能性もあります。

## etcdゲートウェイを使う場面 {#when-to-use-etcd-gateway}

etcdにアクセスするすべてのアプリケーションは、まずetcdクラスターのクライアントエンドポイントのアドレスを把握しなければなりません。同じサーバー上の複数のアプリケーションが同じetcdクラスターにアクセスする場合も、それぞれがクラスターの通知するクライアントエンドポイントを知る必要があります。再構成によってetcdクラスターのエンドポイントが変わると、すべてのアプリケーションでエンドポイント一覧の更新が必要になる可能性があります。この広範囲の再構成は手間がかかり、誤りも生じやすい操作です。

etcdゲートウェイは、安定したローカルエンドポイントとして機能することで、この問題を解決します。典型的な構成では、各マシンでローカルアドレスをリッスンするゲートウェイを動かし、etcdを使う各アプリケーションはローカルのゲートウェイに接続します。その結果、個々のアプリケーションを更新せず、ゲートウェイのエンドポイントを更新するだけで済みます。

つまり、同じetcdクラスターにアクセスする複数のアプリケーションを実行する各マシンでetcdゲートウェイを動かすことで、クラスターのエンドポイント変更を自動的に反映できます。

## etcdゲートウェイが適さない場面 {#when-not-to-use-etcd-gateway}

- 性能の改善

ゲートウェイは、etcdクラスターの性能改善を目的として設計されていません。キャッシュ、監視の集約、バッチ処理は提供しません。etcdチームは、クラスターのスケーラビリティーを向上させるためのキャッシュプロキシーを開発しています。

- クラスター管理システム上での実行

Kubernetesのような高度なクラスター管理システムは、サービスディスカバリーを標準で提供します。アプリケーションは、システムが管理するDNS名や仮想IPアドレスでetcdクラスターにアクセスできます。たとえば、kube-proxyはetcdゲートウェイに相当します。

## etcdゲートウェイの起動 {#start-etcd-gateway}

次の静的エンドポイントを持つetcdクラスターを考えます。

|名前|アドレス|ホスト名|ポート|
|------|---------|------------------|----|
|infra0|10.0.1.10|infra0.example.com|2379|
|infra1|10.0.1.11|infra1.example.com|2379|
|infra2|10.0.1.12|infra2.example.com|2379|

次のコマンドで、これらの静的エンドポイントを使用するetcdゲートウェイを起動します。

```bash
$ etcd gateway start --endpoints=infra0.example.com:2379,infra1.example.com:2379,infra2.example.com:2379
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

DNSでサービスディスカバリーを行う場合は、次のDNS SRVエントリーを考えます。

```bash
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```bash
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

次のコマンドで、DNS SRVエントリーからエンドポイントを取得するetcdゲートウェイを起動します。

```bash
$ etcd gateway start --discovery-srv=example.com
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

## 設定フラグ {#configuration-flags}

### etcdクラスター {#etcd-cluster}

#### --endpoints {#endpoints}

 * クライアント接続の転送先となるetcdサーバーを、カンマ区切りで指定します。
 * デフォルト：`127.0.0.1:2379`
 * ポートを含めなければなりません。
 * 無効な例：`https://127.0.0.1:2379`（ゲートウェイはTLSを終端しません）。ゲートウェイはHTTPスキームの検証やリクエストの検査を行わず、指定されたエンドポイントにリクエストを転送するだけである点に注意してください。

#### --discovery-srv {#discovery-srv}

 * SRVレコードを通じてクラスターのエンドポイントをブートストラップするためのDNSドメイン。
 * デフォルト：（未設定）

### ネットワーク {#network}

#### --listen-addr {#listen-addr}

 * クライアントのリクエストを受け付けるためにバインドするインターフェースとポート。
 * デフォルト：`127.0.0.1:23790`

#### --retry-delay {#retry-delay}

 * 障害が発生したエンドポイントへの再接続を試みるまでの待機時間。
 * デフォルト：1m0s
 * 無効な例："123"（時間の単位を含む形式が必要）

### セキュリティー {#security}

#### --insecure-discovery {#insecure-discovery}

 * 安全でない、または中間者攻撃を受けるおそれのあるSRVレコードを受け入れます。
 * デフォルト：`false`

#### --trusted-ca-file {#trusted-ca-file}

 * SRVディスカバリーが返すエンドポイントを検証するための、etcdクラスターのクライアントTLS CAファイルのパス。このファイルは発見したエンドポイントの認証にのみ使い、データ転送用の接続を作成するためには使わない点に注意してください。ゲートウェイはTLS接続を終端せず、クライアントに代わってTLS接続を作成することもありません。
 * デフォルト：（未設定）
