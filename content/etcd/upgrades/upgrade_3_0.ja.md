---
title: etcdを2.3から3.0にアップグレード
weight: 6900
description: etcdを2.3から3.0にアップグレードする手順、チェックリスト、注意事項
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

通常、etcd 2.3から3.0へのアップグレードは、停止時間なしのローリングアップグレードで実行できます。
 - etcd v2.3のプロセスを1つずつ停止し、etcd v3.0のプロセスに置き換えます。
 - すべてのプロセスがv3.0で稼働すると、クラスターでv3.0の新機能を利用できます。

[アップグレードを開始する](#upgrade-procedure)前に、このガイドの残りを読んで準備してください。

### アップグレードのチェックリスト {#upgrade-checklists}

> [!WARNING]
> [v3データのないv2から移行する](https://github.com/etcd-io/etcd/issues/9480)場合、v3の`ETCD_DATA_DIR/member/snap/db`ファイルがない状態で既存のスナップショットからリストアすると、etcdサーバーv3.2+でパニックが発生します。これは、以前のv3データがないままサーバーをv2から移行した場合に起こります。この動作は、v3データの意図しない消失（たとえば`db`ファイルが移動された場合）を防ぐ役割も果たします。etcdでは、v3への移行後はv3データが存在する場合にのみ、さらに移行を進められます。v3.0サーバーにv3データが存在するまでは、それより新しいv3バージョンにアップグレードしないでください。

#### アップグレードの要件 {#upgrade-requirements}

既存のetcd環境を3.0にアップグレードするには、稼働中のクラスターが2.3以降でなければなりません。2.3より前の場合は、3.0にアップグレードする前に[2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8)にアップグレードしてください。

また、ローリングアップグレードを円滑に進めるには、稼働中のクラスターが正常でなければなりません。作業を進める前に、`etcdctl cluster-health`コマンドでクラスターの正常性を確認してください。

#### 準備 {#preparation}

etcdをアップグレードする際は、必ず本番環境に適用する前に、etcdに依存するサービスをステージング環境でテストしてください。

作業を始める前に、[etcdのデータディレクトリをバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)してください。アップグレードで問題が発生した場合は、このバックアップを使用して元のetcdバージョンに[ダウングレード](#downgrade)できます。

#### バージョンの混在 {#mixed-versions}

アップグレード中のetcdクラスターでは、異なるバージョンのetcdメンバーの混在がサポートされ、全メンバーに共通する最も低いバージョンのプロトコルで動作します。すべてのメンバーがバージョン3.0にアップグレードされて初めて、クラスターのアップグレードが完了したと見なされます。内部では、etcdメンバーが相互にネゴシエーションを行ってクラスター全体のバージョンを決定し、そのバージョンによって報告されるバージョンとサポートされる機能が決まります。

#### 制限事項 {#limitations}

データの総量が50MBを超える場合、新しくアップグレードしたメンバーが既存のクラスターに追いつくまでに最大2分かかることがあります。直近のスナップショットのサイズを調べて、データの総量を見積もってください。つまり、各メンバーのアップグレードの間に2分待つのが最も安全です。

データの総量が100MB以上とさらに大きい場合、この1回限りの処理にはより長い時間がかかることがあります。この規模の非常に大きなetcdクラスターを管理している場合は、アップグレード前に[etcdチーム][etcd-contact]までお気軽にお問い合わせください。手順についてアドバイスします。

#### ダウングレード {#downgrade}

すべてのメンバーをv3.0にアップグレードすると、クラスターもv3.0にアップグレードされ、この完了状態からのダウングレードは**できません**。ただし、1つでもv2.3のメンバーが残っていれば、クラスターとその動作は「v2.3」のままであり、この混在状態からすべてのメンバーでv2.3のetcdバイナリを使用する状態に戻せます。

アップグレード完了後でもクラスターをダウングレードできるように、すべてのetcdメンバーの[データディレクトリをバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)してください。

### アップグレード手順 {#upgrade-procedure}

この例では、ローカルマシンで稼働する3メンバー構成のv2.3 etcdクラスターをアップグレードする手順を詳しく説明します。

#### 1. アップグレード要件の確認 {#1-check-upgrade-requirements}

クラスターは正常で、v.2.3.xで稼働していますか。

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. 既存のetcdプロセスの停止 {#2-stop-the-existing-etcd-process}

各etcdプロセスを停止すると、他のクラスターメンバーに想定どおりのエラーが記録されます。クラスターメンバーへの接続が（一時的に）切断されたためであり、正常な動作です。

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

問題が発生した場合にダウングレードできるよう、この時点で[etcdのデータディレクトリをバックアップ](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)することをお勧めします。

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. etcd v3.0バイナリへの置き換えと新しいetcdプロセスの起動 {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

新しいv3.0のetcdは、自身の情報をクラスターに公開します。

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

新しいv3.0のetcdバイナリで、各メンバー、続いてクラスター全体が正常になることを確認してください。

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


クラスター全体のアップグレードが完了するまでは、アップグレード済みのメンバーに次のような警告が記録されます。これは想定された動作で、すべてのetcdクラスターメンバーをv3.0にアップグレードすると表示されなくなります。

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. 残りのすべてのメンバーで手順2から手順3を繰り返す {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. 完了 {#5-finish}

すべてのメンバーのアップグレードが完了すると、クラスターは3.0へのアップグレードが成功したことを報告します。

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## その他の考慮事項 {#further-considerations}

- etcdctlの環境変数が更新されています。`ETCDCTL_API=2 etcdctl cluster-health`は正常に動作するのに、`ETCDCTL_API=3 etcdctl endpoints health`が`Error:  grpc: timed out when dialing`を返す場合は、必ず[新しい変数名](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl)を使用してください。

## 既知の問題 {#known-issues}

- etcd &lt; v3.1は、Go &gt; v1.7でビルドすると正常に動作しません。詳細は[Issue 6951](https://github.com/etcd-io/etcd/issues/6951)を参照してください。
- etcdサーバーのログに`transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.`などのエラーが表示される場合は、ビルド済みのリリース、または（etcd v3.1+ &amp; go v1.7+）もしくは（etcd &lt;v3.1 &amp; go v1.6.x）でビルドしたetcdを使用していることを確認してください。
- アップグレード中にv2.3クラスターへv3ノードを追加することはサポートされておらず、パニックを引き起こす可能性があります。詳細は[Issue 7249](https://github.com/etcd-io/etcd/issues/7429)を参照してください。etcdメンバーのバージョン混在が許可されるのは、v3への移行中のみです。メンバー構成を変更する前に、アップグレードを完了してください。

[etcd-contact]: https://groups.google.com/g/etcd-dev
