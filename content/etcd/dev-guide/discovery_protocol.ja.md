---
title: 検出サービスのプロトコル
weight: 1500
description: "クラスターの初期構築時に他のetcdメンバーを検出する"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/discovery_protocol.md"
---

> [!NOTE]
> このページでは、etcd 3.7で削除された旧v2ディスカバリープロトコルを説明しています。新しいv3.7環境のデプロイには、[v3ディスカバリープロトコル](/ja/etcd/dev-internal/discovery_protocol/)を使用してください。

検出サービスのプロトコルは、共有の検出URLを使い、クラスターの初期構築時に新しいetcdメンバーが他のすべてのメンバーを検出するためのものです。

検出サービスのプロトコルは、クラスターの初期構築時に*のみ*使用します。実行時の再構成やクラスターの監視には使用できません。

このプロトコルは、新しい検出トークンを使って、*一意の*etcdクラスターを1つ初期構築します。1つの検出トークンが表せるetcdクラスターは1つだけです。そのトークンで検出プロトコルを開始した後は、途中で失敗した場合でも、別のetcdクラスターの初期構築に再利用してはいけません。

以降では、自前でホストする検出クラスターの例を使って、検出の流れを説明します。公開検出サービスのdiscovery.etcd.ioも同じ仕組みで動作しますが、複雑なURLを隠し、UUIDを自動生成し、過剰なリクエストをある程度防ぐための層が追加されています。公開検出サービスも、内部ではこのドキュメントで説明するようにetcdクラスターをデータストアとして使用しています。

## プロトコルの処理の流れ {#protocol-workflow}

検出プロトコルは、内部のetcdクラスターを使って、新しいクラスターの初期構築を調整します。まず、すべての新しいメンバーが検出サービスとやり取りして、予定されたメンバーの一覧を作成します。次に、各新規メンバーはこの一覧を使ってサーバーを初期構築します。これは-initial-clusterフラグと同じ役割を果たします。

以下の処理例では、理解しやすいように、プロトコルの各手順をcurl形式で示します。

慣例として、etcdの検出プロトコルはキーの接頭辞`_etcd/registry`を使用します。`http://example.com`で検出サービス用のetcdクラスターをホストしている場合、検出キー空間の完全なURLは`http://example.com/v2/keys/_etcd/registry`です。この例では、これをURLの接頭辞として使用します。

### 新しい検出トークンの作成 {#creating-a-new-discovery-token}

新しいクラスターを識別する一意のトークンを生成します。以降の手順では、検出キー空間内の一意の接頭辞として使用します。`uuidgen`を使うと簡単に生成できます。

```
UUID=$(uuidgen)
```

### 予定するクラスターサイズの指定 {#specifying-the-expected-cluster-size}

検出トークンには、予定するクラスターサイズを指定する必要があります。検出サービスはこのサイズを使い、クラスターを初期構成するすべてのメンバーが見つかったかどうかを判断します。

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size -d value=${cluster_size}
```

クラスターサイズは通常、3、5、7のいずれかです。詳細は[最適なクラスターサイズ][cluster-size]を参照してください。

### etcdプロセスの起動 {#bringing-up-etcd-processes}

検出URLを`-discovery`フラグに指定して、etcdプロセスを起動します。`-discovery`フラグが指定された各etcdプロセスは、内部で以下の手順を実行します。

### 自身の登録 {#registering-itself}

etcdプロセスは最初に、検出URLに自身をメンバーとして登録します。検出URL内にメンバーIDをキーとして作成することで登録します。

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/${member_id}?prevExist=false -d value="${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}"
```

### 状態の確認 {#checking-the-status}

検出URLから予定されたクラスターサイズと登録状態を確認し、次の動作を決めます。

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}
```

登録済みのメンバーがまだ足りなければ、残りのメンバーが現れるのを待ちます。

登録済みのメンバー数が予定サイズNを超える場合、最初に登録されたN個のメンバーを、そのクラスターのメンバー一覧として扱います。自分自身が一覧に含まれていれば検出は成功し、その一覧からすべてのピアを取得します。一覧に含まれていなければ、クラスターが満員であるというエラーで検出処理を終了します。

etcdの実装では、自身を登録する前にメンバーがクラスターの状態を確認することもあります。そのため、クラスターがすでに満員の場合、速やかに失敗できます。

### すべてのメンバーを待機 {#waiting-for-all-members}

待機処理の詳細は、[etcd APIドキュメント][api]を参照してください。

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}?wait=true&waitIndex=${current_etcd_index}
```

すべてのメンバーが見つかるまで待機を続けます。

## 公開検出サービス {#public-discovery-service}

CoreOS Inc.は、https://discovery.etcd.io/ で公開検出サービスをホストしています。このサービスは、使いやすさのためにいくつかの便利な機能を提供します。

### キーの接頭辞の隠蔽 {#mask-key-prefix}

公開検出サービスは、`https://discovery.etcd.io/${UUID}`を、背後のetcdクラスターの`/v2/keys/_etcd/registry`にあるキーへリダイレクトします。登録キーの接頭辞を隠すことで、短く読みやすい検出URLを提供します。

### 新しいトークンの取得 {#get-new-token}

```
GET /new

Sent query:
	size=${cluster_size}
Possible status codes:
	200 OK
	400 Bad Request
200 Body:
	generated discovery url
```

サービス内の生成処理は、[新しい検出トークンの作成][new-discovery-token]から[予定するクラスターサイズの指定][expected-cluster-size]までの手順に従います。

### 検出状態の確認 {#check-discovery-status}

```
GET /${UUID}
```

UUIDの値を要求することで、登録済みのマシンを含む、その検出トークンの状態を確認できます。

### オープンソースリポジトリ {#open-source-repository}

リポジトリは https://github.com/coreos/discovery.etcd.io にあります。独自の検出サービスを構築するために使用できます。

[api]: https://etcd.io/docs/v2.3/api#waiting-for-a-change
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
