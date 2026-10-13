---
title: etcdを3.0から3.1にアップグレード
weight: 6850
description: etcdを3.0から3.1にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
aliases: [/etcd/upgrades/upgrade_3_1/]
---

通常、etcd 3.0から3.1へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v3.0のプロセスを1つずつ停止し、etcd v3.1のプロセスに置き換えます。
 - すべてのプロセスがv3.1で稼働すると、クラスターでv3.1の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

#### 監視 {#monitoring}

v3.0.xの次のメトリクスは非推奨となり、[go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus)に置き換えられました。

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.1にアップグレードするには、稼働中のクラスターが3.0以降でなければなりません。3.0より前の場合は、3.1にアップグレードする前に[3.0にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_0)してください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl endpoint health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[etcdのデータをバックアップ](/ja/docs/etcd/op-guide/maintenance/#snapshot-backup)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。`snapshot`コマンドでバックアップされるのはv3データのみであることに注意してください。v2データについては、[v2データストアのバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)を参照してください。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.1にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

注：クラスターにv3データしかなく、v2データがない場合、この制限は適用されません。

クラスターが50MBを超えるv2データセットを提供している場合、新しくアップグレードした各メンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.1にアップグレードすると、クラスターもv3.1にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv3.0のメンバーが残っていれば、クラスターとその動作は「v3.0」のままであり、この混在状態からすべてのメンバーでv3.0のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、すべてのetcdメンバーの[データディレクトリをバックアップ](/ja/docs/etcd/op-guide/maintenance#snapshot-backup)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv3.0 etcdクラスターをアップグレードする方法を説明します。

#### 1. アップグレード要件の確認 {#1-check-upgrade-requirements}

クラスターは正常で、v3.0.xで稼働していますか。

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. 既存のetcdプロセスの停止 {#2-stop-the-existing-etcd-process}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

問題が発生した場合にダウングレードできるよう、この時点で[etcdのデータをバックアップ](/ja/docs/etcd/op-guide/maintenance#snapshot-backup)することをお勧めします。

```
$ etcdctl snapshot save backup.db
```

#### 3. etcd v3.1バイナリへの置き換えと新しいetcdプロセスの起動 {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

新しいv3.1のetcdは、自身の情報をクラスターに公開します。

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

新しいv3.1のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

クラスター全体のアップグレードが完了するまでは、アップグレード済みのメンバーに次のような警告が記録されます。これは想定された動作で、すべてのetcdクラスターメンバーをv3.1にアップグレードすると表示されなくなります。

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. 残りのすべてのメンバーで手順2から手順3を繰り返す {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完了 {#5-finish}

すべてのメンバーのアップグレードが完了すると、クラスターは3.1へのアップグレードが成功したことを報告します。

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
