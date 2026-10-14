---
title: "保守"
weight: 4450
description: "etcdクラスターの定期保守ガイド"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/maintenance.md"
---

## 概要 {#overview}

etcdクラスターの信頼性を維持するには、定期的な保守が必要です。etcdを使うアプリケーションの要件にもよりますが、通常は保守を自動化でき、停止や大幅な性能低下なしに実施できます。

etcdの保守はすべて、キー空間が消費するストレージリソースを管理するためのものです。キー空間のサイズを十分に管理できない場合に備え、ストレージ容量のクォータが設けられています。etcdメンバーの空き容量が少なくなると、クォータによってクラスター全体にアラームが発報され、システムは操作が制限された保守モードに移行します。キー空間への書き込み領域が不足しないよう、キー空間の履歴をコンパクションしなければなりません。ストレージ領域そのものは、etcdメンバーのデフラグメンテーションで回収できます。また、メンバーの状態のスナップショットを定期的にバックアップしておくと、操作ミスによる意図しない論理的なデータ損失や破損からリカバリーできます。

## Raftログの保持 {#raft-log-retention}

`etcd --snapshot-count`は、コンパクション前にメモリに保持する、適用済みRaftエントリーの数を設定します。`--snapshot-count`に達すると、サーバーはまずスナップショットのデータをディスクに永続化し、その後で古いエントリーを切り詰めます。遅いフォロワーがコンパクション済みのインデックスより前のログを要求すると、リーダーはスナップショットを送信し、フォロワーの状態を上書きさせます。

`--snapshot-count`を大きくすると、スナップショットまでに多くのRaftエントリーをメモリに保持するため、[メモリ使用量の増大が繰り返し発生します](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156)。リーダーが最新のRaftエントリーを長く保持する分、遅いフォロワーはリーダーのスナップショット作成前に追いつく時間を長く取れます。`--snapshot-count`は、メモリ使用量の増加と遅いフォロワーの可用性向上とのトレードオフです。

v3.2では、`--snapshot-count`のデフォルト値が[10,000から100,000に変更されました](https://github.com/etcd-io/etcd/pull/7160)。v3.7.0のデフォルト値は10,000です。

性能面では、`--snapshot-count`を100,000より大きくすると、書き込みスループットに影響する可能性があります。メモリ上のオブジェクトが増えると、[Go GCのマーク段階である`runtime.scanobject`](https://golang.org/src/runtime/mgc.go)が遅くなることがあり、メモリの回収頻度が下がると割り当ても遅くなります。性能はワークロードとシステム環境によって異なりますが、一般にコンパクションが頻繁すぎるとクラスターの可用性と書き込みスループットに影響します。頻度が低すぎても、Goのガベージコレクターに過大な負荷をかけるため有害です。詳しい調査結果は、[etcdとRaftの性能特性の理解](https://www.slideshare.net/mitakeh/understanding-performance-aspects-of-etcd-and-raft)を参照してください。

## 履歴のコンパクション：v3 APIキー・バリューデータベース {#history-compaction-v3-api-key-value-database}

etcdはキー空間の履歴を正確に保持するため、性能低下や最終的なストレージ容量の枯渇を防ぐには、履歴を定期的にコンパクションすることを推奨します。キー空間の履歴をコンパクションすると、指定したリビジョンより前に置き換えられたキーの情報をすべて破棄します。これらのキーが使っていた領域は、キー空間への追加書き込みに利用できるようになります。

キー空間は、`etcd`の時間範囲に基づく履歴保持ポリシーで自動的にコンパクションすることも、`etcdctl`で手動実行することもできます。`etcdctl`では処理を細かく制御できます。一方、自動コンパクションは、一定期間のキー履歴だけを必要とするアプリケーションに適しています。

`etcdctl`から開始するコンパクションは、次のように行います。

```sh
# compact up to revision 3
$ etcdctl compact 3
```

コンパクション対象のリビジョンより前のリビジョンにはアクセスできなくなります。

```sh
$ etcdctl get --rev=2 somekey
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

### 自動コンパクション {#auto-compaction}

`--auto-compaction-mode`と`--auto-compaction-retention`オプションで、キー空間を自動的にコンパクションするよう`etcd`を設定できます。モードは`periodic`（デフォルト）と`revision`の2種類です。

#### 定期コンパクション {#periodic-compaction}

定期コンパクションでは、時間に基づく範囲のキー空間履歴を保持します。

```sh
# keep one hour of history
$ etcd --auto-compaction-retention=1h
```

保持値は、履歴をどれだけ残すかを指定します。レコードは、作成からおよそその期間が経過するまでコンパクションされません。そのため、遅いウォッチャーでも保持期間内であれば追いつくことができます。

保持期間が1時間より長い場合、etcdは保持期間全体の履歴を維持しながら、1時間ごとにコンパクションします。保持期間が1時間以下の場合は、その保持期間と同じ間隔でコンパクションします。

たとえば`--auto-compaction-retention=10h`では、etcdは最初のコンパクションまで10時間待機し、その後は1時間ごとにコンパクションします。

```text
0hr  (rev = 1)
1hr  (rev = 10)
...
8hr  (rev = 80)
9hr  (rev = 90)
10hr (rev = 100, Compact(1))
11hr (rev = 110, Compact(10))
...
```

推奨値は用途によって異なります。

- 同じキーを頻繁に更新する場合：`1h`や`30m`などの短い期間
- 更新が少ない場合：`24h`、`48h`、`72h`などの長い期間
- 汎用的なデフォルト：`10h`

#### リビジョンによるコンパクション {#revision-compaction}

リビジョンによるコンパクションでは、固定数のリビジョンを保持します。

```sh
# keep 1000 revisions
$ etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcdは5分ごとに確認し、`"latest revision" - 1000`のリビジョンを対象にコンパクションします。たとえば最新リビジョンが30000の場合、リビジョン29000を対象にコンパクションします。

## デフラグメンテーション {#defragmentation}

キー空間をコンパクションした後、バックエンドデータベースに内部断片化が生じる場合があります。内部断片化した領域はバックエンドが自由に再利用できますが、ストレージ容量を消費し続けます。古いリビジョンのコンパクションは、バックエンドデータベースに隙間を残すことで`etcd`の内部断片化を引き起こします。この断片化した領域は`etcd`には利用できても、ホストのファイルシステムには利用できません。つまり、アプリケーションのデータを削除しても、ディスク領域は回収されません。

デフラグメンテーションは、このストレージ領域をファイルシステムに返します。クラスター全体でレイテンシーが急増するのを避けられるよう、メンバー単位で実行します。

etcdメンバーをデフラグメンテーションするには、`etcdctl defrag`コマンドを使用します。

```sh
$ etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
```

> [!WARNING]
> 稼働中のメンバーに対するデフラグメンテーションは、状態の再構築中、システムのデータ読み書きをブロックする点に注意してください。

> [!WARNING]
> デフラグメンテーションのリクエストは、クラスター内で複製されません。リクエストはローカルノードだけに適用されます。`--endpoints`フラグにすべてのメンバーを指定するか、`--cluster`フラグでクラスターメンバーをすべて自動検出してください。

デフォルトのエンドポイントが属するクラスター内のすべてのエンドポイントに対して、デフラグメンテーションを実行します。

```bash
$ etcdctl defrag --cluster
Finished defragmenting etcd member[http://127.0.0.1:2379]
Finished defragmenting etcd member[http://127.0.0.1:22379]
Finished defragmenting etcd member[http://127.0.0.1:32379]
```

etcdが停止している間にデータディレクトリを直接デフラグメンテーションするには、次のコマンドを使用します。

```sh
etcdutl defrag --data-dir <path-to-etcd-data-dir>
```

## 容量クォータ {#space-quota}

`etcd`の容量クォータは、クラスターの信頼性のある動作を確保します。クォータがなければ、`etcd`のキー空間が大きくなりすぎて性能が低下したり、ストレージ容量が尽きてクラスターが予測不能な動作をしたりする可能性があります。いずれかのメンバーでキー空間のバックエンドデータベースが容量クォータを超えると、`etcd`はクラスター全体にアラームを発報し、キーの読み取りと削除だけを受け付ける保守モードに移行します。キー空間に十分な空きを確保し、バックエンドデータベースをデフラグメンテーションし、容量クォータのアラームを解除して初めて、クラスターは通常の動作に戻れます。

`etcd`はデフォルトで、ほとんどのアプリケーションに適した控えめな容量クォータを設定します。コマンドラインで、バイト単位の値を設定することもできます。

```sh
# set a very small 16 MiB quota
$ etcd --quota-backend-bytes=$((16*1024*1024))
```

次のループで容量クォータに達する状態を作れます。

```sh
# fill keyspace
$ while [ 1 ]; do dd if=/dev/urandom bs=1024 count=1024  | ETCDCTL_API=3 etcdctl put key  || break; done
...
Error:  rpc error: code = 8 desc = etcdserver: mvcc: database space exceeded
# confirm quota space is exceeded
$ ETCDCTL_API=3 etcdctl --write-out=table endpoint status
+----------------+------------------+-----------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        |  VERSION  | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
| 127.0.0.1:2379 | bf9071f4639c75cc | 2.3.0+git | 18 MB   | true      |         2 |       3332 |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
# confirm alarm is raised
$ ETCDCTL_API=3 etcdctl alarm list
memberID:13803658152347727308 alarm:NOSPACE
```

キー空間の余分なデータを削除し、バックエンドデータベースをデフラグメンテーションすると、クラスターの使用量をクォータの範囲内に戻せます。

```sh
# get current revision
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# compact away all old revisions
$ ETCDCTL_API=3 etcdctl compact $rev
compacted revision 1516
# defragment away excessive space
$ ETCDCTL_API=3 etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
# disarm alarm
$ ETCDCTL_API=3 etcdctl alarm disarm
memberID:13803658152347727308 alarm:NOSPACE
# test puts are allowed again
$ ETCDCTL_API=3 etcdctl put newkey 123
OK
```

メトリクス`etcd_mvcc_db_total_size_in_use_in_bytes`は、履歴コンパクション後の実際のデータベース使用量を表します。一方、`etcd_debugging_mvcc_db_total_size_in_bytes`は、デフラグメンテーションを待つ空き領域を含むデータベースのサイズを表します。後者が増えるのは前者が後者に近づいたときだけです。つまり、両方がクォータに近い場合、容量クォータに達するのを防ぐため、履歴のコンパクションが必要です。

v3.4以降、`etcd_debugging_mvcc_db_total_size_in_bytes`は`etcd_mvcc_db_total_size_in_bytes`に改名されています。

> [!WARNING]
> Put/Txn/LeaseGrantリクエストで`ErrGRPCNoSpace`エラーが返っても、バックエンドでは書き込みが成功している場合があります。etcdはAPI層と内部のApply層で容量クォータをチェックしますが、Apply層は`NOSPACE`アラームを発報するだけで、トランザクションの進行をブロックしないためです。

## スナップショットのバックアップ {#snapshot-backup}

`etcd`クラスターのスナップショットを定期的に作成すると、キー空間の永続的なバックアップになります。メンバーのバックエンドデータベースのスナップショットを定期的に取得することで、`etcd`クラスターを正常であると確認できた時点にリカバリーできます。

スナップショットは`etcdctl`で取得します。

```sh
$ etcdctl snapshot save backup.db
$ etcdutl --write-out=table snapshot status backup.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| fe01cf57 |       10 |          7 | 2.1 MB     |
+----------+----------+------------+------------+
```
