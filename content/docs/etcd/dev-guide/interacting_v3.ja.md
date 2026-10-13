---
title: etcdの操作
weight: 3250
description: "etcdctl：etcdサーバーを操作するコマンドラインツール"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/interacting_v3.md"
aliases: [/etcd/dev-guide/interacting_v3/]
---

ユーザーは主に、キーの値を書き込んだり取得したりしてetcdを操作します。このセクションでは、etcdサーバーを操作するコマンドラインツールetcdctlを使う方法を説明します。ここで説明する概念は、gRPC APIやクライアントライブラリーのAPIにも当てはまるはずです。

etcdctl v3.7はv3 APIを使用します。v2 APIと`ETCDCTL_API`によるバージョン選択は削除されています。

> [!NOTE]
> 以下の例には過去のコマンド出力が含まれるため、表示されるバージョン番号はインストールしたものと異なる場合があります。以前のetcdリリースではv2とv3のキーを別々のストアで保持していました。v3.7へアップグレードする前に、既存のv2データを移行してください。

## バージョンの確認 {#find-versions}

etcdctlのバージョンとサーバーAPIのバージョンを確認すると、etcdの各種操作に適したコマンドを見つけるのに役立ちます。

バージョンを確認するコマンドは、次のとおりです。

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## キーへの書き込み {#write-a-key}

アプリケーションはキーに書き込むことで、etcdクラスターにキーを保存します。保存された各キーは、一貫性と信頼性を確保するため、Raftプロトコルによってetcdクラスターのすべてのメンバーに複製されます。

キー`foo`の値を`bar`に設定するコマンドは、次のとおりです。

```bash
$ etcdctl put foo bar
OK
```

リースを関連付けると、キーを指定した時間だけ有効にすることもできます。

キー`foo1`の値を10sの間`bar1`に設定するコマンドは、次のとおりです。

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> 上のコマンドのリースID`1234abcd`は、10sのリースを作成したときに返されるIDです。このIDをキーに関連付けます。

## キーの読み取り {#read-keys}

アプリケーションは、etcdクラスターからキーの値を読み取れます。クエリーは、単一のキーまたはキーの範囲を読み取ることができます。

etcdクラスターに、次のキーが保存されているとします。

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

キー`foo`の値を読み取るコマンドは、次のとおりです。

```bash
$ etcdctl get foo
foo
bar
```

キー`foo`の値を16進数形式で読み取るコマンドは、次のとおりです。

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

キー`foo`の値だけを読み取るコマンドは、次のとおりです。

```bash
$ etcdctl get foo --print-value-only
bar
```

`foo`から`foo3`までの範囲のキーを取得するコマンドは、次のとおりです。

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> 範囲は`foo3`を含まない半開区間`[foo, foo3)`なので、`foo3`は除外されます。

`foo`を接頭辞に持つすべてのキーを取得するコマンドは、次のとおりです。

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`foo`を接頭辞に持つすべてのキーを対象とし、結果を2件までに制限するコマンドは、次のとおりです。

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

[`RangeStream`](/ja/docs/etcd/learning/api/#rangestream) RPCを使って、`foo`を接頭辞に持つすべてのキーを取得するコマンドは、次のとおりです。結果は単項の`Range`と同じです。

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream`は、`--order`、`--sort-by`、リビジョンフィルターをサポートしません。

## キーの過去のバージョンの読み取り {#read-past-version-of-keys}

アプリケーションは、更新によって古くなったキーのバージョンを読み取りたい場合があります。たとえば、キーの以前のバージョンにアクセスして、古い構成に戻したい場合です。また、キーの履歴にアクセスすることで、複数のリクエストを通じて複数のキーを一貫した状態で読み取りたい場合もあります。
etcdクラスターのキー・バリューストアを変更するたびに、クラスター全体のリビジョンが増加するため、古いetcdリビジョンを指定すれば、過去のキーを読み取れます。

etcdクラスターに、次のキーがすでに存在するとします。

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

キーの過去のバージョンにアクセスする例は、次のとおりです。

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## 指定したキーのバイト値以上のキーの読み取り {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

アプリケーションは、指定したキーのバイト値以上のキーを読み取りたい場合があります。

etcdクラスターに、次のキーがすでに存在するとします。

```bash
a = 123
b = 456
z = 789
```

キー`b`のバイト値以上のキーを読み取るコマンドは、次のとおりです。

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## キーの削除 {#delete-keys}

アプリケーションは、etcdクラスターから単一のキーまたはキーの範囲を削除できます。

etcdクラスターに、次のキーがすでに存在するとします。

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

キー`foo`を削除するコマンドは、次のとおりです。

```bash
$ etcdctl del foo
1 # one key is deleted
```

`foo`から`foo9`までの範囲のキーを削除するコマンドは、次のとおりです。

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

キー`zoo`を削除し、削除したキー・バリューペアを返すコマンドは、次のとおりです。

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

`zoo`を接頭辞に持つキーを削除するコマンドは、次のとおりです。

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

キー`b`のバイト値以上のキーを削除するコマンドは、次のとおりです。

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## キーの変更の監視 {#watch-key-changes}

アプリケーションは、単一のキーまたはキーの範囲を監視して、更新を検知できます。

キー`foo`を監視するコマンドは、次のとおりです。

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

キー`foo`を16進数形式で監視するコマンドは、次のとおりです。

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

`foo`から`foo9`までの範囲のキーを監視するコマンドは、次のとおりです。

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

`foo`を接頭辞に持つキーを監視するコマンドは、次のとおりです。

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

複数のキー`foo`と`zoo`を監視するコマンドは、次のとおりです。

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## キーの過去の変更の監視 {#watch-historical-changes-of-keys}

アプリケーションは、etcd内のキーの過去の変更を監視したい場合があります。たとえば、あるキーのすべての変更を受け取りたい場合、etcdへの接続を維持していれば`watch`で十分です。しかし、アプリケーションやetcdに障害が起きると、その間に変更が発生しても、アプリケーションは更新をリアルタイムで受信できません。更新の配信を保証するには、アプリケーションがキーの過去の変更を監視できる必要があります。そのためには、キーの過去のバージョンを読み取るときと同様に、監視に過去のリビジョンを指定します。

次の一連の操作を終えたとします。

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

過去の変更を監視する例は、次のとおりです。

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

過去の最後の変更からだけ監視する例は、次のとおりです。

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## 監視の進捗 {#watch-progress}

アプリケーションは、監視ストリームがどの程度最新の状態に追いついているかを判断するために、監視の進捗を確認したい場合があります。たとえば、監視でキャッシュを更新する場合、クォーラム読み取りで得たリビジョンと比べてキャッシュが古いかどうかを把握すると役立ちます。

対話型の監視セッションで"progress"コマンドを使用すると、進捗リクエストを発行し、監視ストリームで進捗通知を送るようetcdサーバーに要求できます。

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> 進捗通知レスポンスのリビジョン番号は、監視ストリームが接続しているローカルのetcdサーバーノードのリビジョンです。このノードがネットワーク分断によってクォーラムから外れている場合、進捗通知のリビジョンは、分断されていないetcdサーバーノードへのクォーラム読み取りで返されるリビジョンより小さいことがあります。

## コンパクション済みリビジョン {#compacted-revisions}

すでに説明したとおり、etcdはリビジョンを保持し、アプリケーションがキーの過去のバージョンを読み取れるようにします。ただし、履歴が無制限に蓄積するのを防ぐには、過去のリビジョンのコンパクションが重要です。コンパクション後、etcdは過去のリビジョンを削除し、今後の使用のためにリソースを解放します。コンパクションしたリビジョンより前の、更新によって古くなったデータはすべて利用できなくなります。

リビジョンをコンパクションするコマンドは、次のとおりです。

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> etcdサーバーの現在のリビジョンは、任意のキー（存在するキーでも、存在しないキーでも）に対してgetコマンドを実行し、json形式で取得できます。以下は、etcdサーバーに存在しないmykeyの例です。

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## リースの付与 {#grant-leases}

アプリケーションは、etcdクラスターからキー用のリースを取得できます。キーをリースに関連付けると、その有効期間はリースの有効期間に結び付けられます。リースの有効期間は生存時間（TTL）によって決まります。各リースには、アプリケーションが付与時に指定する最小TTLがあります。実際のTTLは最小TTL以上で、etcdクラスターが選択します。リースのTTLが経過すると、リースは期限切れになり、関連付けられたすべてのキーが削除されます。

リースを付与するコマンドは、次のとおりです。

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## リースの取り消し {#revoke-leases}

アプリケーションは、リースIDを指定してリースを取り消します。リースを取り消すと、関連付けられたすべてのキーが削除されます。

次の一連の操作を終えたとします。

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

このリースを取り消すコマンドは、次のとおりです。

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## リースの維持 {#keep-leases-alive}

アプリケーションは、TTLを更新することでリースの期限切れを防ぎ、維持できます。

次の一連の操作を終えたとします。

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

このリースを維持するコマンドは、次のとおりです。

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## リース情報の取得 {#get-lease-information}

アプリケーションは、リースを更新するため、またはリースがまだ存在するか、期限切れになったかを確認するために、リース情報を取得したい場合があります。また、特定のリースに関連付けられているキーを確認したい場合もあります。

次の一連の操作を終えたとします。

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

リース情報を取得するコマンドは、次のとおりです。

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

リースに関連付けられたキーとともにリース情報を取得するコマンドは、次のとおりです。

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
