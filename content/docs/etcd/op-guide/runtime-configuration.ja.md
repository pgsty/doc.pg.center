---
title: "実行時再構成"
weight: 4700
description: "etcdの段階的な実行時再構成"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
aliases: [/etcd/op-guide/runtime-configuration/]
---

etcdは段階的な実行時再構成をサポートしており、稼働中にクラスターのメンバー構成を更新できます。

再構成リクエストを処理できるのは、クラスターメンバーの過半数が稼働している場合だけです。本番環境では、クラスターを常に2を超えるメンバーで構成することを**強く推奨します**。2メンバーのクラスターからメンバーを削除するのは安全ではありません。2メンバーのクラスターの過半数も2だからです。削除処理中に障害が発生すると、クラスターが処理を継続できなくなり、[過半数の障害から再起動][majority failure]する必要が生じる可能性があります。

実行時再構成の設計について理解を深めるには、[実行時再構成の設計ドキュメント][runtime-reconf]を参照してください。

## 再構成の用途 {#reconfiguration-use-cases}

このセクションでは、クラスターを再構成する主な理由を説明します。多くの場合、後述の[クラスター再構成の操作][cluster-reconf]で説明するメンバーの追加と削除を組み合わせるだけで対応できます。

### 複数マシンの入れ替えやアップグレード {#cycle-or-upgrade-multiple-machines}

計画保守（ハードウェアのアップグレード、ネットワーク停止など）で複数のクラスターメンバーを移動する必要がある場合は、1つずつ変更することを推奨します。

リーダーの削除は安全ですが、選挙中に短い停止時間が発生します。クラスターが50MBを超えるv2データを保持している場合は、[メンバーのデータディレクトリの移行][member migration]を推奨します。

### クラスターサイズの変更 {#change-the-cluster-size}

クラスターサイズを大きくすると、[耐障害性][fault tolerance table]と読み取り性能を向上できます。クライアントは任意のメンバーから読み取れるため、メンバーを増やすと、直列化可能読み取りの全体的なスループットが向上します。

クラスターサイズを小さくすると、耐障害性が低下する一方で、書き込み性能を向上できます。クラスターへの書き込みは、過半数のメンバーに複製されてからコミット済みと見なされます。クラスターサイズが小さくなると、過半数に必要な数が減るため、各書き込みをより早くコミットできます。

### 障害が発生したマシンの置き換え {#replace-a-failed-machine}

ハードウェアの故障、データディレクトリの破損、その他の致命的な問題でマシンが停止した場合は、できるだけ早い置き換えを推奨します。障害が発生していても削除されていないマシンはクォーラムに悪影響を与え、追加の障害への耐性を低下させます。

マシンを置き換えるには、クラスターからの[メンバー削除][remove member]の手順に従い、その後で代わりとなる[新しいメンバーを追加][add member]します。クラスターが50MBを超えるデータを保持しており、障害が発生したメンバーのデータディレクトリにまだアクセスできる場合は、[そのデータディレクトリの移行][member migration]を推奨します。

### 過半数の障害からクラスターを再起動 {#restart-cluster-from-majority-failure}

クラスターの過半数を失った場合や、すべてのノードのIPアドレスが変わった場合は、安全なリカバリーのために手動操作が必要です。基本的な手順は、[古いデータから新しいクラスターを作成][disaster recovery]し、単一メンバーを強制的にリーダーとして動作させ、最後に実行時構成でそのクラスターに[新しいメンバーを1つずつ追加][add member]することです。

### 少数の障害からクラスターをリカバリー {#recover-cluster-from-minority-failure}

特定のメンバーを失った場合は、障害が発生したマシンの置き換えと同じです。手順は[障害が発生したマシンの置き換え](/ja/docs/etcd/op-guide/runtime-configuration/#replace-a-failed-machine)に記載しています。

## クラスター再構成の操作 {#cluster-reconfiguration-operations}

上記の用途を踏まえて、それぞれの操作を説明します。

変更を行う前に、etcdメンバーの単純過半数（クォーラム）が利用可能でなければなりません。これは、etcdへのあらゆる書き込みに必要な条件と基本的に同じです。

クラスターへの変更は、すべて順番に行わなければなりません。

* 単一メンバーのpeerURLsを更新するには、更新操作を実行する
* 正常な単一メンバーを置き換えるには、古いメンバーを削除してから新しいメンバーを追加する
* メンバーを3から5に増やすには、追加操作を2回実行する
* メンバーを5から3に減らすには、削除操作を2回実行する

これらの例ではすべて、etcdに付属するコマンドラインツール`etcdctl`を使用します。`etcdctl`を使わずにメンバー構成を変更するには、[v3 gRPCメンバーAPI][member-api-grpc]を使用してください。

### メンバーの更新 {#update-a-member}

#### 通知するクライアントURLの更新 {#update-advertise-client-urls}

メンバーが通知するクライアントURLを更新するには、クライアントURLのフラグ（`--advertise-client-urls`）または環境変数（`ETCD_ADVERTISE_CLIENT_URLS`）を変更して、そのメンバーを再起動するだけです。再起動したメンバーは、更新後のURLを自動的に公開します。クライアントURLの更新を誤っても、etcdクラスターの健全性には影響しません。

#### 通知するピアURLの更新 {#update-advertise-peer-urls}

メンバーが通知するピアURLを更新するには、まずmemberコマンドで明示的に更新し、その後でメンバーを再起動します。ピアURLの更新はクラスター全体の構成を変え、健全性に影響する可能性があるため、この追加操作が必要です。

通知するピアURLを更新するには、まず対象メンバーのIDを確認します。`etcdctl`で全メンバーを一覧表示するには、次のようにします。

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

この例では、メンバーID a8266ecf031671f3を`update`し、そのpeerURLsを`http://10.0.1.10:2380`に変更します。

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### メンバーの削除 {#remove-a-member}

削除するメンバーIDがa8266ecf031671f3であるとします。`remove`コマンドで削除します。

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

対象メンバーはこの時点で自身を停止し、削除されたことをログに出力します。

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

リーダーの削除は安全ですが、新しいリーダーの選出中はクラスターが動作しません。この時間は、通常、選挙タイムアウトと投票処理の時間の合計です。

### 新しいメンバーの追加 {#add-a-new-member}

メンバーの追加は、2段階で行います。

 * [v3 gRPCメンバーAPI][member-api-grpc]または`etcdctl member add`コマンドで、新しいメンバーをクラスターに追加します。
 * 更新後のメンバー一覧（既存メンバーと新しいメンバー）を含む新しいクラスター構成で、新しいメンバーを起動します。

`etcdctl`では、メンバーの[名前][conf-name]と[通知するピアURL][conf-adv-peer]を指定して、クラスターに新しいメンバーを追加します。

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

`etcdctl`は新しいメンバーをクラスターに通知し、正常に起動するために必要な環境変数を出力しました。続いて、新しいメンバーに対応するフラグで新しいetcdプロセスを起動します。

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

新しいメンバーはクラスターの一員として稼働し、直ちにほかのメンバーへの追従を開始します。

複数のメンバーを追加する場合は、1つずつ構成し、正しく起動することを確認してから次を追加するのがベストプラクティスです。1ノードのクラスターに新しいメンバーを追加すると、コンセンサスに必要な過半数が2メンバーになるため、新しいメンバーが起動するまでクラスターは処理を進められません。この動作は、`etcdctl member add`が新しいメンバーをクラスターに通知してから、新しいメンバーが既存メンバーへの接続を確立するまでの間だけ発生します。

#### 新しいメンバーを学習者メンバーとして追加 {#add-a-new-member-as-learner}

v3.4以降、etcdは新しいメンバーを学習者メンバー、つまり投票しないメンバーとして追加できます。
その背景と設計は、[設計ドキュメント][design-learner]を参照してください。
追加処理の安全性を高め、追加時のクラスター停止時間を減らすため、新しいメンバーは追従が完了するまで学習者メンバーとして追加することを推奨します。手順は次の3段階です。

 * [gRPCメンバーAPI][member-api-grpc]または`etcdctl member add --learner`コマンドで、新しいメンバーを学習者メンバーとして追加します。

 * 更新後のメンバー一覧（既存メンバーと新しいメンバー）を含む新しいクラスター構成で、新しいメンバーを起動します。
 この手順は前述とまったく同じです。

 * [gRPCメンバーAPI][member-api-grpc]または`etcdctl member promote`コマンドで、新しく追加した学習者メンバーを投票メンバーに昇格させます。
 etcdサーバーは、操作の安全性を確保するため、昇格リクエストを検証します。
 学習者メンバーは、そのRaftログがリーダーに追いついてからでなければ、投票メンバーに昇格できません。
 リーダーのRaftログに追いついていない場合、昇格リクエストは失敗します（詳しくは[メンバー昇格時のエラー][error cases when promoting a member]を参照）。
 この場合は、待ってから再試行することを推奨します。

v3.4では、etcdサーバーはクラスター内の学習者メンバー数を1つに制限します。主な目的は、リーダーから学習者メンバーへのデータ配信による、リーダーの追加負荷を抑えることです。

`etcdctl member add`に`--learner`フラグを指定し、新しいメンバーを学習者メンバーとしてクラスターに追加します。

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

新しく追加した学習者メンバーのetcdプロセスを起動した後、`etcdctl member promote`で投票メンバーに昇格させます。
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### メンバー追加時のエラー {#error-cases-when-adding-members}

次の例では、新しいホストがノード一覧に含まれていません。新しいクラスターの場合は、初期クラスターメンバーの一覧にこのノードを追加しなければなりません。

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

この失敗例では、登録したピアアドレス（10.0.1.13:2380）とは異なるアドレス（10.0.1.14:2380）でメンバーを起動しています。

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

削除済みメンバーのデータディレクトリを使ってetcdを起動すると、クラスター内の稼働中メンバーに接続した時点で、etcdは自動的に終了します。

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### 学習者メンバー追加時のエラー {#error-cases-when-adding-a-learner-member}

すでに学習者メンバーが1つあるクラスターには、学習者メンバーを追加できません（v3.4）。
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### 学習者メンバー昇格時のエラー {#error-cases-when-promoting-a-learner-member}

学習者メンバーを投票メンバーに昇格できるのは、リーダーと同期している場合だけです。
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

学習者メンバーでないメンバーの昇格は失敗します。
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

クラスターに存在しないメンバーの昇格は失敗します。
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### 厳格な再構成チェックモード（`-strict-reconfig-check`） {#strict-reconfiguration-check-mode--strict-reconfig-check}

前述のとおり、新しいメンバーを追加するときは、1つずつ構成し、正しく起動することを確認してから次を追加するのがベストプラクティスです。新しいメンバーの設定が正しくないと（ピアURLの誤りなど）、クラスターがクォーラムを失う可能性があるため、この段階的な方法は非常に重要です。ほかの既存メンバーから新しいメンバーに到達できなくても、新しいメンバーはクォーラムの計算に含まれるため、クォーラムを失うことになります。接続の問題や運用上の問題でも、クォーラムを失う可能性があります。

この問題を防ぐため、etcdは`-strict-reconfig-check`オプションを提供します。このオプションを指定すると、再構成後のクラスターのクォーラムに必要な数より起動済みメンバーが少なくなる再構成リクエストを、etcdは拒否します。

このオプションは、デフォルトで有効です。

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /ja/docs/etcd/op-guide/configuration#clustering
[conf-name]: /ja/docs/etcd/op-guide/configuration#member
[design-learner]: /ja/docs/etcd/learning/design-learner
[disaster recovery]: /ja/docs/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /ja/docs/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /ja/docs/etcd/op-guide/runtime-reconf-design/
