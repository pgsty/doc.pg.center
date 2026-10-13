---
title: etcdをv3.7からv3.6にダウングレード
weight: 6600
description: etcdをv3.7からv3.6にダウングレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
aliases: [/etcd/downgrades/downgrade_3_7/]
---

通常、etcd v3.7からv3.6へのダウングレードは、停止時間なしのローリングダウングレードで実行できます。

- etcd v3.7のプロセスを1つずつ停止し、etcd v3.6のプロセスに置き換えます。
- ダウングレードを有効にすると、クラスターでv3.7の新機能を利用できなくなります。

[ダウングレードを開始する](#downgrade-procedure)前に、このガイドの残りを読んで準備してください。

### ダウングレードのチェックリスト {#downgrade-checklists}

v3.7とv3.6の主な違いは次のとおりです。

#### フラグの違い {#difference-in-flags}

v3.7では新しいフラグが追加されていないため、v3.6プロセスはv3.7の設定に含まれるすべてのフラグを受け付けます。ダウングレード時に設定を変更する必要はありません。

> [!NOTE]
> この差分は、バージョンv3.7.0-rc.0とv3.6.13に基づいています。実際の差分は使用するパッチバージョンによって異なるため、先に`diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`で確認してください。

v3.7で削除された非推奨の`--experimental-*`フラグはv3.6にはまだ存在しますが、ダウングレード後に再追加しないでください。両バージョンで動作する、対応する非実験的フラグまたは`--feature-gates`のエントリーを使用してください。

#### Prometheusメトリクスの違い {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### サーバーダウングレードのチェックリスト {#server-downgrade-checklists}

#### ダウングレードの要件 {#downgrade-requirements}

ローリングダウングレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをダウングレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。ダウングレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ロールバック](#rollback)できます。

作業を始める前に、etcd v3.6の最新リリースをダウンロードしてください。

#### バージョンの混在 {#mixed-versions}

ダウングレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。`etcdctl downgrade enable 3.6`でダウングレードを有効にすると、クラスターはダウングレードされたと見なされます。内部では、クラスター全体のバージョンがダウングレード先のバージョンに設定され、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### ロールバック {#rollback}

etcdクラスターをダウングレードする前に、クラスターのスナップショットバックアップを作成して[ダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。このスナップショットを使えば、必要に応じてクラスターをダウングレード前の状態にリストアできます。ダウングレード中に問題が発生した場合は、まず根本原因を特定して解決することをお勧めします。

`etcdctl downgrade enable`を実行してダウングレードが開始され、少なくとも1つのメンバーがv3.7のままでクラスターのバージョンがまだ混在している場合は、`etcdctl downgrade cancel`を実行し、ダウングレード済みのすべてのメンバーを元のv3.7バイナリで再起動することで、進行中のダウングレードを取り消せます。

すべてのメンバーをv3.6にダウングレードすると、クラスターのダウングレードは完了したと見なされます。ダウングレードが完全に完了した後に元のバージョンに戻したい場合は、一貫性を確保しデータ破損を防ぐため、公式の[アップグレードガイド](/ja/docs/etcd/upgrades/upgrade_3_7/)に従うことをお勧めします。

### ダウングレード手順 {#downgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.7 etcdクラスターをダウングレードする方法を説明します。以下の出力は、直前にv3.6.13からアップグレードしたクラスターで、1台のホスト上の3つのループバックポートを使用し、etcd v3.7.0-rc.0とetcd v3.6.13を実際に稼働させたときのものです。

#### 手順1：ダウングレード要件の確認 {#step-1-check-downgrade-requirements}

クラスターは正常で、v3.7.xで稼働していますか。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### 手順2：リーダーからスナップショットバックアップをダウンロード {#step-2-download-snapshot-backup-from-leader}

問題が発生した場合にダウングレードをロールバックできるよう、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### 手順3：ダウングレード先バージョンの検証 {#step-3-validate-downgrade-target-version}

ダウングレードを有効にする前に、ダウングレード先のバージョンを検証します。

- サポートされるのは、マイナーバージョンを1つずつ下げるダウングレードだけです。たとえば、v3.7からv3.5へのダウングレードは許可されません。
- 検証が成功するまでは、次の手順に進まないでください。

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### 手順4：ダウングレードを有効化 {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

ダウングレードを有効にすると、クラスターはダウングレード先のバージョンであるv3.6のプロトコルで動作し始めます。また、etcdはスキーマをダウングレード先のバージョンに自動的に移行します。この処理は通常、非常に短時間で完了します。次の手順に進む前に、エンドポイントのステータスを確認し、すべてのサーバーのストレージバージョンがv3.6に移行済みであることを確認してください。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> ダウングレードを有効にすると、すべてのサーバーがまだv3.7バイナリで稼働していても、`etcdctl downgrade cancel`でダウングレードを取り消さない限り、クラスターはv3.6のプロトコルで動作し続けます。

#### 手順5：既存のetcdサーバーを1つ停止 {#step-5-stop-one-existing-etcd-server}

サーバーを停止する前に、そのサーバーがリーダーかどうかを確認します。リーダーは最後にダウングレードすることをお勧めします。停止するサーバーがリーダーの場合、停止前に`move-leader`で別のサーバーへ移譲すると、停止時間の一部を回避できます。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### 手順6：同じ設定でetcdサーバーを再起動 {#step-6-restart-the-etcd-server-with-same-configuration}

同じ設定で、v3.6のetcdバイナリを使用してetcdサーバーを再起動します。

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

v3.6のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> v3.5とは異なり、v3.6のステータスエンドポイントはダウングレード情報を報告するため、ダウングレード済みのメンバーは、ダウングレードが完了するまで`DOWNGRADE ENABLED`をtrueとして表示し、ストレージバージョンも表示し続けます。

#### 手順7：残りのメンバーで*手順5*と*手順6*を繰り返す {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

すべてのメンバーのダウングレードが終わると、ダウングレードは自動的に完了し、`DOWNGRADE ENABLED`はfalseに戻ります。クラスターの正常性とステータスを確認し、すべてのメンバーのマイナーバージョンとストレージバージョンがv3.6であることを確認します。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

リーダーのログには、次のようなメッセージが表示されるはずです。

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
