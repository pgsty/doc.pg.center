---
title: etcdをv3.5からv3.6にアップグレード
weight: 6600
description: etcdをv3.5からv3.6にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
aliases: [/etcd/upgrades/upgrade_3_6/]
---

通常、etcd v3.5からv3.6へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。

- etcd v3.5のプロセスを1つずつ停止し、etcd v3.6のプロセスに置き換えます。
- すべてのプロセスがv3.6で稼働すると、クラスターでv3.6の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

#### 3.5の更新 {#update-35}

> [!IMPORTANT]
> 3.6にアップグレードする前に、[すべての3.5メンバーが3.5.32以降に更新されている](https://etcd.io/blog/2026/july-patch-release/)ことを確認してください。パッチリリース3.5.24から3.5.26では、アップグレードを妨げる可能性のある問題がいくつか修正されています。[3.5.32](https://etcd.io/blog/2026/july-patch-release/)では`--v2-deprecation=write-only-skip-check`が追加され、`etcdutl check v2store`が拡張されてv2スナップショットに加えてWALレコードも検査するようになりました。

#### V2ストア {#v2-store}

> [!NOTE]
> `--enable-v2`フラグを設定していない、またはfalseに設定している場合、追加の作業は不要です。

`--enable-v2`を**設定している**場合は、`etcdutl check v2store`コマンドを実行し、v2storeにメンバー構成以外の（カスタム）データが含まれていないか確認してください。カスタムデータがなければ、このフラグを安全に削除できます。含まれている場合は、[v2移行ガイド](https://etcd.io/docs/v3.4/op-guide/v2-migration/)で詳細を確認してください。

### 追加されたフラグ {#flags-added}

```diff
+etcd --discovery-token ''
+etcd --discovery-endpoints ''
+etcd --discovery-dial-timeout '2s'
+etcd --discovery-request-timeout '5s'
+etcd --discovery-keepalive-time '2s'
+etcd --discovery-keepalive-timeout '6s'
+etcd --discovery-insecure-transport 'true'
+etcd --discovery-insecure-skip-tls-verify 'false'
+etcd --discovery-cert ''
+etcd --discovery-key ''
+etcd --discovery-cacert ''
+etcd --discovery-user ''
+etcd --discovery-password ''
+etcd --feature-gates
+etcd --log-format
```

### 削除されたフラグ {#flags-removed}

```diff
-etcd --enable-v2
-etcd --experimental-enable-v2v3
-etcd --proxy
-etcd --proxy-failure-wait
-etcd --proxy-refresh-interval
-etcd --proxy-dial-timeout
-etcd --proxy-write-timeout
-etcd --proxy-read-timeout
```

### 非推奨になったフラグ {#flags-deprecated}

**`etcd --experimental-bootstrap-defrag-threshold-megabytes`フラグは非推奨になりました。**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**`etcd --experimental-compaction-batch-limit`フラグは非推奨になりました。**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**`etcd --experimental-compact-hash-check-time`フラグは非推奨になりました。**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**`etcd --experimental-compaction-sleep-interval`フラグは非推奨になりました。**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**`etcd --experimental-corrupt-check-time`フラグは非推奨になりました。**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**`etcd --experimental-enable-distributed-tracing`フラグは非推奨になりました。**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**`etcd --experimental-distributed-tracing-address`フラグは非推奨になりました。**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**`etcd --experimental-distributed-tracing-instance-id`フラグは非推奨になりました。**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**`etcd --experimental-distributed-tracing-sampling-rate`フラグは非推奨になりました。**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**`etcd --experimental-distributed-tracing-service-name`フラグは非推奨になりました。**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**`etcd --experimental-downgrade-check-time`フラグは非推奨になりました。**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**`etcd --experimental-max-learners`フラグは非推奨になりました。**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**`etcd --experimental-memory-mlock`フラグは非推奨になりました。**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**`etcd --experimental-peer-skip-client-san-verification`フラグは非推奨になりました。**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**`etcd --experimental-snapshot-catchup-entries`フラグは非推奨になりました。**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**`etcd --experimental-warning-apply-duration`フラグは非推奨になりました。**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**`etcd --experimental-warning-unary-request-duration`フラグは非推奨になりました。**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**`etcd --experimental-watch-progress-notify-interval`フラグは非推奨になりました。**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### v3.5の実験的フラグからフィーチャーゲートへの移行 {#equivalent-flags-of-v35-feature-gates}

**`etcd --experimental-compact-hash-check-enabled=true`に対応するフィーチャーゲート**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**`etcd --experimental-initial-corrupt-check=true`に対応するフィーチャーゲート**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**`etcd --experimental-enable-lease-checkpoint=true`に対応するフィーチャーゲート**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**`etcd --experimental-enable-lease-checkpoint-persist=true`に対応するフィーチャーゲート**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**`etcd --experimental-stop-grpc-service-on-defrag=true`に対応するフィーチャーゲート**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**`etcd --experimental-txn-mode-write-with-shared-buffer=false`に対応するフィーチャーゲート**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### デフォルト値が変更されたフラグ {#flags-with-new-defaults}

**以前のデフォルトフラグ`etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**以前のデフォルトフラグ`etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**以前のデフォルトフラグ`etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### Prometheusメトリクスの違い {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境をv3.6にアップグレードするには、稼働中のクラスターがv3.5以降でなければなりません。v3.5より前の場合は、v3.6にアップグレードする前に[v3.5にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_5/)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ロールバック](#rollback)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョンv3.6にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### ロールバック {#rollback}

etcdクラスターをアップグレードする前に、クラスターのスナップショットバックアップを作成して[ダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。このスナップショットを使えば、必要に応じてクラスターをアップグレード前の状態にリストアできます。アップグレード中に問題が発生した場合は、まず根本原因を特定して解決することをお勧めします。少なくとも1つのメンバーがv3.5のままで、クラスターのバージョンがまだ混在している場合は、バイナリまたはイメージを以前のv3.5のものに置き換えるか、スナップショットを使用してクラスターを直接リストアできます。この混在状態ではクラスターはv3.5クラスターとして動作し続けるため、正式なダウングレード手順を踏まずにロールバックできます。

ただし、すべてのメンバーをv3.6にアップグレードすると、クラスターのアップグレードは完了したと見なされ、バイナリを置き換えるだけでは正しくロールバックできません。リカバリーするには、アップグレード前に取得したスナップショットからリストアするか、公式のダウングレードガイドに従って元のバージョンに戻し、一貫性を確保してデータ破損を防ぐ方法があります。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.5 etcdクラスターをアップグレードする方法を説明します。

#### 手順1：アップグレード要件の確認 {#step-1-check-upgrade-requirements}

クラスターは正常で、v3.5.xで稼働していますか。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.555774ms
localhost:32379 is healthy: successfully committed proposal: took = 2.631133ms
localhost:22379 is healthy: successfully committed proposal: took = 3.020958ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT
```

#### 手順2：リーダーからスナップショットバックアップをダウンロード {#step-2-download-snapshot-backup-from-leader}

問題が発生した場合にダウングレードできるよう、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。

etcdのリーダーには最新のアプリケーションデータがあることが保証されているため、リーダーからスナップショットを取得します。

```bash
curl -sL http://localhost:2379/metrics | grep etcd_server_is_leader
<<COMMENT
# HELP etcd_server_is_leader Whether or not this member is a leader. 1 if is, 0 otherwise.
# TYPE etcd_server_is_leader gauge
etcd_server_is_leader 1
COMMENT

curl -sL http://localhost:22379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

curl -sL http://localhost:32379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### 手順3：既存のetcdサーバーを1つ停止 {#step-3-stop-one-existing-etcd-server}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

```bash
{"level":"info","ts":"2025-03-01T04:31:50.654520+0530","caller":"etcdserver/server.go:2676","msg":"cluster version is updated","cluster-version":"3.5"}
{"level":"info","ts":"2025-03-01T04:34:10.345927+0530","caller":"v3rpc/maintenance.go:130","msg":"sending database snapshot to client","total-bytes":20480,"size":"20 kB"}
{"level":"info","ts":"2025-03-01T04:34:10.346094+0530","caller":"v3rpc/maintenance.go:170","msg":"sending database sha256 checksum to client","total-bytes":20480,"checksum-size":32}
{"level":"info","ts":"2025-03-01T04:34:10.346108+0530","caller":"v3rpc/maintenance.go:179","msg":"successfully sent database snapshot to client","total-bytes":20480,"size":"20 kB","took":"now"}
^C
{"level":"info","ts":"2025-03-01T04:35:01.443045+0530","caller":"osutil/interrupt_unix.go:64","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":"2025-03-01T04:35:01.443088+0530","caller":"embed/etcd.go:408","msg":"closing etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
{"level":"info","ts":"2025-03-01T04:35:01.443417+0530","caller":"etcdserver/server.go:1503","msg":"leadership transfer starting","local-member-id":"bf9071f4639c75cc","current-leader-member-id":"bf9071f4639c75cc","transferee-member-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443441+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term 2] starts to transfer leadership to 91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443455+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc sends MsgTimeoutNow to 91bc3c398fb3c146 immediately as 91bc3c398fb3c146 already has up-to-date log"}
{"level":"warn","ts":"2025-03-01T04:35:01.443517+0530","caller":"embed/serve.go:179","msg":"stopping insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"warn","ts":"2025-03-01T04:35:01.443548+0530","caller":"embed/serve.go:181","msg":"stopped insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"info","ts":"2025-03-01T04:35:01.445536+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term: 2] received a MsgVote message with higher term from 91bc3c398fb3c146 [term: 3]"}
{"level":"info","ts":"2025-03-01T04:35:01.445556+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc became follower at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445565+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [logterm: 2, index: 12, vote: 0] cast MsgVote for 91bc3c398fb3c146 [logterm: 2, index: 12] at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445572+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc lost leader bf9071f4639c75cc at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.446773+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc elected leader 91bc3c398fb3c146 at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.544062+0530","caller":"etcdserver/server.go:1520","msg":"leadership transfer finished","local-member-id":"bf9071f4639c75cc","old-leader-member-id":"bf9071f4639c75cc","new-leader-member-id":"91bc3c398fb3c146","took":"100.640374ms"}
{"level":"info","ts":"2025-03-01T04:35:01.544160+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.544956+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.544984+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545050+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545065+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545099+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545156+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545178+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"91bc3c398fb3c146","error":"failed to read 91bc3c398fb3c146 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545199+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545246+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545263+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545272+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545282+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545307+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545328+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545359+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545379+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545410+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545467+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545485+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"fd422379fda50e48","error":"failed to read fd422379fda50e48 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545504+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545560+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545577+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545592+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545669+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545698+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545732+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545765+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"info","ts":"2025-03-01T04:35:01.549658+0530","caller":"embed/etcd.go:613","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550532+0530","caller":"embed/etcd.go:618","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550561+0530","caller":"embed/etcd.go:410","msg":"closed etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
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

新しいv3.6のetcdは、自身の情報をクラスターに公開します。この時点では、クラスターは引き続き全メンバーに共通する最も低いバージョンであるv3.5のプロトコルで動作します。

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

新しいv3.6のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

クラスター全体のアップグレードが完了するまでは、未アップグレードのメンバーに次のような警告が記録されます。

これは想定された動作で、すべてのetcdクラスターメンバーをv3.6にアップグレードすると表示されなくなります。

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### 手順5：残りのメンバーで*手順3*と*手順4*を繰り返す {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

すべてのメンバーのアップグレードが完了すると、クラスターはv3.6へのアップグレードが成功したことを報告します。

メンバー1：

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

メンバー2：

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

メンバー3：

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"fd422379fda50e48","from":"3.5","to":"3.6"}`

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT
```
