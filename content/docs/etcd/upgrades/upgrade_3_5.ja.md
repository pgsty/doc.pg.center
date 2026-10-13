---
title: etcdを3.4から3.5にアップグレード
weight: 6650
description: etcdを3.4から3.5にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
aliases: [/etcd/upgrades/upgrade_3_5/]
---

通常、etcd 3.4から3.5へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v3.4のプロセスを1つずつ停止し、etcd v3.5のプロセスに置き換えます。
 - すべてのプロセスがv3.5で稼働すると、クラスターでv3.5の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。



### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

> [!WARNING]
> クラスターで認証を有効にしている場合、3.5では[認証に関するWALエントリーの形式が変更される](https://github.com/etcd-io/etcd/pull/11943)ため、3.4以前のバージョンからのローリングアップグレードはサポートされません。

3.5の主な互換性を損なう変更は次のとおりです。

#### Prometheusメトリクス`etcd_debugging_mvcc_db_total_size_in_bytes`の非推奨化 {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.5では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_db_total_size_in_bytes`を`etcd_mvcc_db_total_size_in_bytes`に昇格させました。また、v3.5では`etcd_debugging_mvcc_db_total_size_in_bytes`が完全に非推奨になります。

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_put_total`の非推奨化 {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.5では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_put_total`を`etcd_mvcc_put_total`に昇格させました。また、v3.5では`etcd_debugging_mvcc_put_total`が完全に非推奨になります。

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_delete_total`の非推奨化 {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.5では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_delete_total`を`etcd_mvcc_delete_total`に昇格させました。また、v3.5では`etcd_debugging_mvcc_delete_total`が完全に非推奨になります。

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_txn_total`の非推奨化 {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.5では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_txn_total`を`etcd_mvcc_txn_total`に昇格させました。また、v3.5では`etcd_debugging_mvcc_txn_total`が完全に非推奨になります。

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### Prometheusメトリクス`etcd_debugging_mvcc_range_total`の非推奨化 {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.5では、etcdストレージの監視を促すため、Prometheusメトリクス`etcd_debugging_mvcc_range_total`を`etcd_mvcc_range_total`に昇格させました。また、v3.5では`etcd_debugging_mvcc_range_total`が完全に非推奨になります。

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

`etcd_debugging_*`名前空間のメトリクスは、実験的機能と位置付けられていることに注意してください。監視ガイドの改善に伴い、さらに多くのメトリクスを昇格させる可能性があります。

#### `etcd --logger capnslog`の非推奨化 {#deprecated-etcd---logger-capnslog}

v3.5では、複数のログ出力と構造化ログをサポートするため、`--logger=zap`がデフォルトです。

**v3.5では`etcd --logger=capnslog`が非推奨となり**、`--logger=zap`がデフォルトになりました。

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4では、構造化ログと複数のログ出力に対応するため、`etcd --logger=zap`のサポートを追加しています。主な狙いは、障害が発生してからサーバーログを調べるのではなく、etcdの監視を自動化することです。今後の開発ではetcdのログ出力をできるだけ少なくし、メトリクスとアラートでetcdを監視しやすくします。**`etcd --logger=capnslog`はv3.5で非推奨になります。**

#### `etcd --log-output`の非推奨化 {#deprecated-etcd---log-output}

v3.4では、複数のログ出力をサポートするため、[`etcd --log-output`を`--log-outputs`に改名しました](https://github.com/etcd-io/etcd/pull/9624)。

**v3.5では`etcd --log-output`が非推奨になりました。**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### `etcd --debug`フラグの非推奨化（現在は`--log-level=debug`） {#deprecated-etcd---debug-flag-now---log-leveldebug}

**`etcd --debug`フラグは非推奨になりました。**

```diff
-etcd --debug
+etcd --log-level debug
```

#### `etcd --log-package-levels`の非推奨化 {#deprecated-etcd---log-package-levels}

**`capnslog`用の`etcd --log-package-levels`フラグは非推奨になりました。**

現在は、**`etcd --logger=zap`**がデフォルトです。

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### `[CLIENT-URL]/config/local/log`の非推奨化 {#deprecated-client-urlconfiglocallog}

**v3.5では、`/config/local/log`エンドポイントと`etcd --log-package-levels`フラグが非推奨になります。**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### gRPCゲートウェイのHTTPエンドポイントの変更（`/v3beta`を非推奨化） {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

変更前

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

変更後

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3beta`は3.5リリースで削除されました。



### サーバーアップグレードのチェックリスト {#server-upgrade-checklists}

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.5にアップグレードするには、稼働中のクラスターが3.4以降でなければなりません。3.4より前の場合は、3.5にアップグレードする前に[3.4にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_4/)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。v2データについては、[v2データストアのバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)を参照してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.5にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

注：クラスターにv3データしかなく、v2データがない場合、この制限は適用されません。

クラスターが50MBを超えるv2データセットを提供している場合、新しくアップグレードした各メンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.5にアップグレードすると、クラスターもv3.5にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv3.4のメンバーが残っていれば、クラスターとその動作は「v3.4」のままであり、この混在状態からすべてのメンバーでv3.4のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、[スナップショットバックアップをダウンロード](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.4 etcdクラスターをアップグレードする方法を説明します。

#### 手順1：アップグレード要件の確認 {#step-1-check-upgrade-requirements}

クラスターは正常で、v3.4.xで稼働していますか。

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
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
{"level":"info","ts":1526585787.148433,"caller":"snapshot/v3_snapshot.go:109","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":1526585787.1485257,"caller":"snapshot/v3_snapshot.go:120","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":1526585787.1519694,"caller":"snapshot/v3_snapshot.go:133","msg":"fetched snapshot","endpoint":"localhost:2379","took":0.003502721}
{"level":"info","ts":1526585787.1520295,"caller":"snapshot/v3_snapshot.go:142","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### 手順3：既存のetcdサーバーを1つ停止 {#step-3-stop-one-existing-etcd-server}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

```bash
{"level":"info","ts":1526587281.2001143,"caller":"etcdserver/server.go:2249","msg":"updating cluster version","from":"3.0","to":"3.4"}
{"level":"info","ts":1526587281.2010646,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}
{"level":"info","ts":1526587281.2012327,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}
{"level":"info","ts":1526587281.2013083,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}



^C{"level":"info","ts":1526587299.0717514,"caller":"osutil/interrupt_unix.go:63","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":1526587299.0718873,"caller":"embed/etcd.go:285","msg":"closing etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
{"level":"info","ts":1526587299.0722554,"caller":"etcdserver/server.go:1341","msg":"leadership transfer starting","local-member-id":"7339c4e5e833c029","current-leader-member-id":"7339c4e5e833c029","transferee-member-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.0723994,"caller":"raft/raft.go:1107","msg":"7339c4e5e833c029 [term 3] starts to transfer leadership to 729934363faa4a24"}
{"level":"info","ts":1526587299.0724802,"caller":"raft/raft.go:1113","msg":"7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log"}
{"level":"info","ts":1526587299.0737045,"caller":"raft/raft.go:797","msg":"7339c4e5e833c029 [term: 3] received a MsgVote message with higher term from 729934363faa4a24 [term: 4]"}
{"level":"info","ts":1526587299.0737681,"caller":"raft/raft.go:656","msg":"7339c4e5e833c029 became follower at term 4"}
{"level":"info","ts":1526587299.073831,"caller":"raft/raft.go:882","msg":"7339c4e5e833c029 [logterm: 3, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 3, index: 9] at term 4"}
{"level":"info","ts":1526587299.0738947,"caller":"raft/node.go:312","msg":"raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 4"}
{"level":"info","ts":1526587299.0748374,"caller":"raft/node.go:306","msg":"raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 4"}
{"level":"info","ts":1526587299.1726425,"caller":"etcdserver/server.go:1362","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"729934363faa4a24","took":0.100389359}
{"level":"info","ts":1526587299.1728148,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1751974,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1752589,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.177348,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1774004,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.177515,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1777067,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34636->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1778402,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1780295,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34634->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1780987,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781602,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781986,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1802843,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1803446,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1824749,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.18255,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.18261,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1827736,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"read tcp 127.0.0.1:51482->127.0.0.1:22380: use of closed network connection"}
{"level":"info","ts":1526587299.182845,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1830168,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"context canceled"}
{"level":"warn","ts":1526587299.1831107,"caller":"rafthttp/peer_status.go:65","msg":"peer became inactive","peer-id":"729934363faa4a24","error":"failed to read 729934363faa4a24 on stream Message (context canceled)"}
{"level":"info","ts":1526587299.1831737,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.1832306,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1837125,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1840093,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1842315,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1844475,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"info","ts":1526587299.2056687,"caller":"embed/etcd.go:473","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.205819,"caller":"embed/etcd.go:480","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.2058413,"caller":"embed/etcd.go:289","msg":"closed etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
```

#### 手順4：同じ設定でetcdサーバーを再起動 {#step-4-restart-the-etcd-server-with-same-configuration}

同じ設定で、新しいetcdバイナリを使用してetcdサーバーを再起動します。

```diff
-etcd-old --name s1 \
+etcd-new --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

新しいv3.5のetcdは、自身の情報をクラスターに公開します。この時点では、クラスターは引き続き全メンバーに共通する最も低いバージョンであるv3.4のプロトコルで動作します。

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

新しいv3.5のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

クラスター全体のアップグレードが完了するまでは、未アップグレードのメンバーに次のような警告が記録されます。

これは想定された動作で、すべてのetcdクラスターメンバーをv3.5にアップグレードすると表示されなくなります。

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### 手順5：残りのメンバーで*手順3*と*手順4*を繰り返す {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

すべてのメンバーのアップグレードが完了すると、クラスターは3.5へのアップグレードが成功したことを報告します。

メンバー1：

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

メンバー2：

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

メンバー3：

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
