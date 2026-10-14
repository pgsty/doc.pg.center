---
title: etcdをv3.6からv3.7にアップグレード
weight: 6550
description: etcdをv3.6からv3.7にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
---

通常、etcd v3.6からv3.7へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。

- etcd v3.6のプロセスを1つずつ停止し、etcd v3.7のプロセスに置き換えます。
- すべてのプロセスがv3.7で稼働すると、クラスターでv3.7の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

#### 3.6の更新 {#update-36}

> [!IMPORTANT]
> 3.7にアップグレードする前に、すべての3.6メンバーが3.6.11以降に更新されていることを確認してください。それより前の3.6パッチリリースは、3.7へのローリングアップグレードと互換性がない可能性があります。

#### V2ストア {#v2-store}

v3.7ではv2ストアが完全に削除されました。v2 HTTP API（`--enable-v2`）、v2-on-v3エミュレーション（`--experimental-enable-v2v3`）、v2ディスカバリーサービス、`client/v2`パッケージ、v2スナップショットファイルの読み込みは、すべて削除されています。[CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md)にある互換性を損なう変更の参照先を確認してください。

3.6クラスターからアップグレードする場合、これらのフラグはすでに存在せず、作業は不要です。カスタムv2データがある古いリリースから移行する場合は、アップグレード前に[v2移行ガイド](https://etcd.io/docs/v3.4/op-guide/v2-migration/)に従ってください。

#### Goのリファクタリング {#go-refactoring}

v3.7には大規模な内部リファクタリングが含まれています。通常のアップグレードには影響しませんが、独自の連携機能をアップグレードする際には把握しておくと役立ちます。

- `gogo/protobuf`から標準の`google.golang.org/protobuf`への移行（[#14533](https://github.com/etcd-io/etcd/issues/14533)で追跡）。
- 非推奨の`go-grpc-middleware` v1のログおよびタグライブラリから、v2インターセプターへの移行（[#20420](https://github.com/etcd-io/etcd/pull/20420)）。
- OpenTelemetryのgRPCインターセプターを`otelgrpc` v0.61.0に更新し、非推奨の`UnaryServerInterceptor`と`StreamServerInterceptor`を`NewServerHandler`に置き換えました（[#20017](https://github.com/etcd-io/etcd/pull/20017)）。

etcdをライブラリとして組み込んでいる場合、`clientv3` APIを使用してビルドしている場合、または内部パッケージに依存している場合は、アップグレード前に[CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md)を確認してください。

### 削除されたフラグ {#flags-removed}

v3.7では、非推奨の`--experimental-*`フラグがすべて削除されました（[#19959](https://github.com/etcd-io/etcd/pull/19959)）。v3.6では、それぞれ同名の非実験的フラグ、または`--feature-gates`のエントリーに置き換えられています。これらのフラグがまだ設定されている場合は、v3.7へのローリングアップグレードを行う**前に**、v3.6の対応する設定に置き換えてください。そうしないと、v3.7のプロセスは起動に失敗します。

```diff
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-compact-hash-check-enabled
-etcd --experimental-compact-hash-check-time
-etcd --experimental-compaction-batch-limit
-etcd --experimental-compaction-sleep-interval
-etcd --experimental-corrupt-check-time
-etcd --experimental-distributed-tracing-address
-etcd --experimental-distributed-tracing-instance-id
-etcd --experimental-distributed-tracing-sampling-rate
-etcd --experimental-distributed-tracing-service-name
-etcd --experimental-downgrade-check-time
-etcd --experimental-enable-distributed-tracing
-etcd --experimental-enable-lease-checkpoint
-etcd --experimental-enable-lease-checkpoint-persist
-etcd --experimental-initial-corrupt-check
-etcd --experimental-memory-mlock
-etcd --experimental-peer-skip-client-san-verification
-etcd --experimental-snapshot-catchup-entries
-etcd --experimental-stop-grpc-service-on-defrag
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-warning-apply-duration
-etcd --experimental-warning-unary-request-duration
-etcd --experimental-watch-progress-notify-interval
```

削除された各フラグと、対応する非実験的フラグまたは`--feature-gates`のエントリーとの対応関係は、[v3.5からv3.6へのアップグレードガイド](/ja/etcd/upgrades/upgrade_3_6/)を参照してください。

### 追加されたフラグ {#flags-added}

ありません。

### デフォルト値が変更されたフラグ {#flags-with-new-defaults}

ありません。

### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境をv3.7にアップグレードするには、稼働中のクラスターがv3.6.11以降でなければなりません。それより古いマイナーバージョンを使用している場合は、先に[v3.6にアップグレード](/ja/etcd/upgrades/upgrade_3_6/)してください。etcdでサポートされるのは、マイナーバージョンを1つずつ上げるアップグレードだけです。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[スナップショットバックアップをダウンロード](/ja/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ロールバック](#rollback)できます。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョンv3.7にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### ロールバック {#rollback}

etcdクラスターをアップグレードする前に、クラスターのスナップショットバックアップを作成して[ダウンロード](/ja/etcd/op-guide/maintenance/#snapshot-backup)してください。このスナップショットを使えば、必要に応じてクラスターをアップグレード前の状態にリストアできます。アップグレード中に問題が発生した場合は、まず根本原因を特定して解決することをお勧めします。少なくとも1つのメンバーがv3.6のままで、クラスターのバージョンがまだ混在している場合は、バイナリまたはイメージを以前のv3.6のものに置き換えるか、スナップショットを使用してクラスターを直接リストアできます。この混在状態ではクラスターはv3.6クラスターとして動作し続けるため、正式なダウングレード手順を踏まずにロールバックできます。

ただし、すべてのメンバーをv3.7にアップグレードすると、クラスターのアップグレードは完了したと見なされ、バイナリによるロールバックはできなくなります。その場合、アップグレードに問題があったときのリカバリー方法は、アップグレード前に取得したスナップショットからリストアするか、公式の[ダウングレードガイド](/ja/etcd/downgrades/downgrading-etcd/)に従うかのいずれかに限られます。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.6 etcdクラスターをアップグレードする方法を説明します。以下の出力は、1台のホスト上で3つのループバックポートを使用し、etcd v3.6.12とetcd v3.7.0-rc.0を実際に稼働させたときのものです。

#### 手順1：アップグレード要件の確認 {#step-1-check-upgrade-requirements}

クラスターは正常で、v3.6.11以降で稼働していますか。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 7.681459ms
localhost:22379 is healthy: successfully committed proposal: took = 7.691750ms
localhost:32379 is healthy: successfully committed proposal: took = 7.698000ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.12","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

#### 手順2：リーダーからスナップショットバックアップをダウンロード {#step-2-download-snapshot-backup-from-leader}

問題が発生した場合にダウングレードできるよう、[スナップショットバックアップをダウンロード](/ja/etcd/op-guide/maintenance/#snapshot-backup)してください。

etcdのリーダーには最新のアプリケーションデータがあることが保証されているため、リーダーからスナップショットを取得します。

```bash
for p in 2379 22379 32379; do
  echo -n "localhost:$p leader="
  curl -sL http://localhost:$p/metrics | grep "^etcd_server_is_leader " | awk '{print $2}'
done
<<COMMENT
localhost:2379 leader=1
localhost:22379 leader=0
localhost:32379 leader=0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-06-02T07:01:41.863225+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-06-02T07:01:41.866451+0300","logger":"client","caller":"v3@v3.6.12/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-06-02T07:01:41.874080+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-06-02T07:01:41.877203+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"13.822583ms","etcd-version":"3.6.0"}
{"level":"info","ts":"2026-06-02T07:01:41.877303+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.6.0
COMMENT
```

#### 手順3：既存のetcdサーバーを1つ停止 {#step-3-stop-one-existing-etcd-server}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。リーダーは終了前にリーダーシップを移譲します。

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
```

#### 手順4：同じ設定でetcdサーバーを再起動 {#step-4-restart-the-etcd-server-with-same-configuration}

同じ設定で、新しいetcdバイナリを使用してetcdサーバーを再起動します。

```diff
-etcd-old --name ${name} \
+etcd-new --name ${name} \
  --data-dir /path/to/${name}.etcd \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

新しいv3.7のetcdは、自身の情報をクラスターに公開します。この時点では、クラスターは引き続き全メンバーに共通する最も低いバージョンであるv3.6のプロトコルで動作します。

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

新しいv3.7のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | LEADER | RAFT TERM |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  false |         3 |
| localhost:22379 | 729934363faa4a24 |     3.6.12 |           3.6.0 |   98 kB |  false |         3 |
| localhost:32379 |  b548c2511513015 |     3.6.12 |           3.6.0 |   98 kB |   true |         3 |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
COMMENT
```

クラスター全体のアップグレードが完了するまでは、未アップグレードのメンバーとアップグレード済みのメンバーに、バージョンの混在状態に関するメッセージが記録されます。これは想定された動作で、すべてのetcdクラスターメンバーをv3.7にアップグレードすると表示されなくなります。

#### 手順5：残りのメンバーで*手順3*と*手順4*を繰り返す {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

すべてのメンバーのアップグレードが完了すると、クラスターはv3.7へのアップグレードが成功したことを報告します。

> `{"level":"info","ts":"2026-06-02T07:02:36.054783+0300","caller":"etcdserver/server.go:2311","msg":"updating cluster version using v3 API","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059345+0300","caller":"membership/cluster.go:593","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059409+0300","caller":"etcdserver/server.go:2326","msg":"cluster version is updated","cluster-version":"3.7"}`

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 550.833µs
localhost:32379 is healthy: successfully committed proposal: took = 733.458µs
localhost:22379 is healthy: successfully committed proposal: took = 714.416µs
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
```
