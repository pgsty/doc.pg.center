---
title: "災害復旧"
weight: 4275
description: "etcd v3のスナップショットとリストア機能"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/recovery.md"
aliases: [/etcd/op-guide/recovery/]
---

etcdは、マシンの障害に耐えるよう設計されています。etcdクラスターは一時的な障害（マシンの再起動など）から自動的にリカバリーし、Nメンバーのクラスターでは最大*(N-1)/2*の恒久的な障害に耐えます。ハードウェアの故障やディスク破損などでメンバーが恒久的に停止すると、そのメンバーはクラスターにアクセスできなくなります。クラスターが*(N-1)/2*を超えるメンバーを恒久的に失うと、重大な障害となり、クォーラムを回復不能な形で失います。クォーラムを失うと、クラスターはコンセンサスに達することができず、更新を受け付け続けられません。

重大な障害からリカバリーするため、etcd v3はv3のキーデータを失わずにクラスターを再作成するスナップショットとリストア機能を提供します。v2のキーをリカバリーするには、[v2管理ガイド][v2_recover]を参照してください。

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## キー空間のスナップショット作成 {#snapshotting-the-keyspace}

クラスターのリカバリーには、まずetcdメンバーのキー空間のスナップショットが必要です。稼働中のメンバーから`etcdctl snapshot save`コマンドで取得する方法と、etcdのデータディレクトリから`member/snap/db`ファイルをコピーする方法があります。たとえば次のコマンドは、`$ENDPOINT`が提供するキー空間のスナップショットを`snapshot.db`ファイルに保存します。

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

`member/snap/db`ファイルからスナップショットを取得すると、wal（先行書き込みログ）フォルダーには含まれていても、まだ書き込まれていないデータが失われる場合がある点に注意してください。

## スナップショットの状態 {#status-of-a-snapshot}

スナップショットに含まれるリビジョンとハッシュを確認するには、`etcdutl snapshot status`コマンドを使用できます。

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## クラスターのリストア {#restoring-a-cluster}

### リビジョンの差 {#revision-difference}

クラスターをリストアすると、既存のクライアントにはリビジョンが数百、数千も前に戻ったように見えることがあります。スナップショットには取得時点までのデータ履歴しか含まれず、現在の状態はそれより先に進んでいる可能性があるためです。

これは、etcdを使ってKubernetesを実行している場合に特に問題になります。コントローラーやOperatorは、ローカルキャッシュとして機能し、監視で更新通知を受ける`informers`を使用することがあります。古いリビジョンにリストアすると、キャッシュが正しく更新されず、コントローラーが予測不能で不整合な動作をする可能性があります。

監視APIの利用者がいることがわかっている場合、etcdデータをローカルにキャッシュしている場合、またはKubernetesを使用している場合は、スナップショットからのリストアに、後述の「リビジョンの引き上げ」を使うことを強く推奨します。

### スナップショットからのリストア {#restoring-from-snapshot}

クラスターのリストアに必要なのは、1つのスナップショット「db」ファイルだけです。`etcdutl snapshot restore`によるリストアは、新しいetcdデータディレクトリを作成します。すべてのメンバーで同じスナップショットを使ってリストアすることを推奨します。リストア時には、スナップショットの一部のメタデータ（具体的にはメンバーIDとクラスターID）を上書きし、メンバーは以前の識別情報を失います。この上書きによって、新しいメンバーが既存のクラスターに誤って参加することを防ぎます。したがって、スナップショットからクラスターを起動するには、新しい論理クラスターとしてリストアしなければなりません。

単純なリストアは次のように実行できます。

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### 整合性チェック {#integrity-checks}

リストア時には、任意でスナップショットの整合性を検証できます。`etcdctl snapshot save`で取得したスナップショットには整合性ハッシュが含まれ、`etcdutl snapshot restore`が検証します。データディレクトリからコピーしたスナップショットには整合性ハッシュがないため、リストアには`--skip-hash-check`が必要です。


### リビジョンを引き上げてリストア {#restoring-with-revision-bump}

リストア後にリビジョンが減少しないよう、`--bump-revision`オプションを指定できます。このオプションは64ビット整数を受け取り、スナップショットの現在のリビジョンに加える数を表します。etcdへの書き込みごとにリビジョンは1増えるため、毎秒の書き込みが1500未満であれば、1'000'000'000引き上げることで1週間前のスナップショットにも対応できます。

Kubernetesコントローラーを使う場合は、`--mark-compacted`で引き上げ分も含めたすべてのリビジョンをコンパクション済みとしてマークすることも重要です。これにより、すべての監視を終了させ、スナップショット取得後に生じたリビジョンについてのリクエストにetcdが応答しないようにして、informerのキャッシュを事実上無効化します。

呼び出し全体の例は次のとおりです。

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### メンバー構成を更新してリストア {#restoring-with-updated-membership}

etcdクラスターのメンバー情報はetcd自身に保存され、Raftコンセンサスアルゴリズムで管理されます。クォーラムを完全に失った場合、たとえばまったく新しいメンバー群を使うなど、新しいクラスターをどこでどのように構成するかを見直すこともできます。

スナップショットからリストアするときは、次のように新しいメンバー構成をデータストアに直接指定できます。

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

これにより、新しく構成したクラスターは、指定されたトークンでリストアしたほかのメンバーだけに接続し、まだ稼働していて接続を試みる可能性がある古いメンバーには接続しません。

別の方法として、etcdの起動時に`--force-new-cluster`を指定し、既存のアプリケーションデータを保持したままメンバー構成を上書きできます。ただし、以前のクラスターのほかのメンバーがまだ稼働しているとパニックになるため、この方法は強く非推奨です。スナップショットを必ず定期的に保存してください。


### 一連の操作例 {#end-2-end-example}

稼働中のクラスターから、次のようにスナップショットを取得します。

```sh
$ etcdctl snapshot save snapshot.db
```

前の例に続いて、次のコマンドで3メンバーのクラスター用の新しいetcdデータディレクトリ（`m1.etcd`、`m2.etcd`、`m3.etcd`）を作成します。

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

次に、新しいデータディレクトリを指定して`etcd`を起動します。

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

これで、リストアしたetcdクラスターが利用可能になり、スナップショットのキー空間を提供しているはずです。

etcd v3.6以降、スナップショットの取得には`etcdctl`だけを使用でき、スナップショットからのリストアには`etcdutl`を使用します。`--data-dir`を指定しない場合、`--data-dir`のデフォルト値は`<name>.etcd`です（`<name>`は`--name`の値）。たとえば、`--data-dir`を指定せず、メンバー名が`m1`、`m2`、`m3`であれば、`--data-dir`のディレクトリは`m1.etcd`、`m2.etcd`、`m3.etcd`になります。
