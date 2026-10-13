---
title: "ディスカバリーサービスのプロトコル"
weight: 1500
description: "クラスターのブートストラップ時に他のetcdメンバーを検出する"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
aliases: [/etcd/dev-internal/discovery_protocol/]
---

ディスカバリーサービスのプロトコルは、共有のディスカバリートークンとエンドポイントリストを使用して、クラスターのブートストラップ時に新しいetcdメンバーが他のすべてのメンバーを検出できるようにします。

ディスカバリーサービスのプロトコルは、クラスターのブートストラップ時に*のみ*使用します。実行時の再構成やクラスターの監視には使用できません。

このプロトコルでは、新しいディスカバリートークンを使って*一意の*etcdクラスターをブートストラップします。1つのディスカバリートークンが表せるetcdクラスターは1つだけであることに注意してください。そのトークンを使ったディスカバリープロトコルが開始されたら、途中で失敗した場合でも、別のetcdクラスターのブートストラップに再利用してはなりません。

以降では、自前で運用するディスカバリークラスターに対応した例を使い、検出処理を順に説明します。

このドキュメントはv3ディスカバリーのみを対象とします。[v2ディスカバリー][v2-discovery]の詳細は、以前のドキュメントを参照してください。

## プロトコルの流れ {#protocol-workflow}

ディスカバリープロトコルは、内部のetcdクラスターを使って新しいクラスターのブートストラップを調整する仕組みです。まず、新しいメンバーすべてがディスカバリーサービスとやり取りし、想定するメンバーリストを生成します。次に、新しい各メンバーはこのリストを使ってサーバーをブートストラップします。これは-initial-clusterフラグと同じ役割を果たします。

以下の手順例では、理解しやすいように`etcdctl`コマンドで各ステップを示します。`http://example.com:2379`でディスカバリーサービス用のetcdクラスターが稼働しているものとします。

etcdのディスカバリープロトコルでは、慣例としてキープレフィックス`/_etcd/registry`を使用します。


### 新しいディスカバリートークンの作成 {#creating-a-new-discovery-token}

新しいクラスターを識別する一意のトークンを生成します。以降の手順では、ディスカバリー用のキー空間で一意のプレフィックスとして使用します。`uuidgen`を使うと簡単に生成できます。

```
UUID=$(uuidgen)
```

### 想定するクラスターサイズの指定 {#specifying-the-expected-cluster-size}

ディスカバリートークンには、想定するクラスターサイズを必ず指定する必要があります。ディスカバリーサービスはこのサイズを使い、初期クラスターを構成するすべてのメンバーが見つかったかどうかを判断します。

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

通常のクラスターサイズは3、5、7です。詳細は[最適なクラスターサイズ][cluster-size]を参照してください。

### etcdプロセスの起動 {#bringing-up-etcd-processes}

`--discovery-token`フラグにディスカバリートークン`${UUID}`を設定し、`--discovery-endpoints`フラグにディスカバリーサービスを支えるetcdクラスターのエンドポイントを設定します。これにより、v3ディスカバリーを使ってetcdクラスターをブートストラップできます。

`--discovery-token`と`--discovery-endpoints`フラグを指定すると、各etcdプロセスは内部で以下の手順を実行します。

ディスカバリーサービスでクライアント証明書認証を有効にしている場合は、次のフラグを設定します。使い方は、`etcdctl`でetcdクラスターと通信する場合とまったく同じです。
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

ディスカバリーサービスでロールベースの認証を有効にしている場合は、次のフラグを設定します。使い方は、`etcdctl`でetcdクラスターと通信する場合とまったく同じです。
```
--discovery-user
--discovery-password
```

時間やタイムアウトのデフォルト値も、次のフラグで変更できます。使い方は、`etcdctl`でetcdクラスターと通信する場合とまったく同じです。
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### 自身の登録 {#registering-itself}

各etcdプロセスはまず、指定した新しいクラスターに自分自身をメンバーとして登録します。これは、レジストリーの完全なキーパス内に、メンバーIDをキーとして作成することで行います。

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### 状態の確認 {#checking-the-status}

想定するクラスターサイズと登録状況を確認し、次の操作を決定します。

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

登録済みのメンバーがまだ足りない場合は、他のメンバーが現れるまで待機します。

登録済みメンバー数が想定サイズNを超えている場合は、最初に登録したN個のメンバーをクラスターのメンバーリストとします。自身がこのリストに含まれていれば、検出手順は成功し、メンバーリストを通じてすべてのピアを取得します。含まれていなければ、クラスターが満員であるため、検出手順は失敗して終了します。

メンバーは自身を登録する前にクラスターの状態を確認することもできます。そのため、クラスターが満員の場合はすぐに失敗できます。

### 全メンバーの待機 {#waiting-for-all-members}

待機処理では、すべてのメンバーが見つかるまでキープレフィックス`/_etcd/registry/${UUID}/members`を監視し続けます。

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
