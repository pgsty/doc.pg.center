---
title: "複数のデータセンターにまたがるHA"
weight: 170
icon: fa-solid fa-globe
description: "Patroniのレプリケーションを使用した、複数のデータセンターにまたがる高可用性の構成パターン。"
module: [PATRONI]
categories: [概念]
aliases: [/patroni/ha_multi_dc/]
upstream_link: "https://patroni.readthedocs.io/en/latest/ha_multi_dc.html"
---

<a id="ha_multi_dc"></a>
複数のデータセンターにデプロイしたPostgreSQLクラスターの高可用性は、レプリケーションに基づきます。レプリケーションには同期と非同期があります（[レプリケーションモード](/ja/docs/patroni/replication_modes#replication_modes)を参照）。

どちらの場合も、次の概念を明確に理解することが重要です。

- Postgresがプライマリーまたはスタンバイリーダーとして動作できるのは、リーダーキーを所有し、それを更新できる場合だけです。
- etcd、ZooKeeper、Consulのノードは、3または5という奇数台で実行することを推奨します。

--------

## 同期レプリケーション {#synchronous-replication}

ゾーンの停止に自動的に耐えられる複数DCのクラスターにするには、少なくとも3つのゾーンが必要です。

アーキテクチャーの図は次のとおりです。

![構成図](/img/docs/patroni/multi-dc-synchronous-replication.png)

etcd、ZooKeeper、Consulのいずれかのクラスターを、複数のDCにまたがって、各ゾーンに一つずつ、少なくとも3ノードでデプロイしなければなりません。

Postgresについては、異なるDCに少なくとも2ノードをデプロイしなければなりません。そのうえで、グローバルな[動的構成](/ja/docs/patroni/config/dynamic#dynamic)に`synchronous_mode: true`を設定する必要があります。

これにより同期レプリケーションが有効になり、プライマリーノードはいずれかのノードを同期ノードとして選択します。

--------

## 非同期レプリケーション {#asynchronous-replication}

データセンターが二つだけの場合は、独立したetcdクラスターを二つ用意し、二つ目のデータセンターでPatroniの[スタンバイクラスター](/ja/docs/patroni/standby_cluster#standby_cluster)を実行する方が適切です。最初のサイトが停止した場合は、[standby_cluster](/ja/docs/patroni/standby_cluster#standby_cluster)を手動で昇格させられます。

アーキテクチャーの図は次のとおりです。

![構成図](/img/docs/patroni/multi-dc-asynchronous-replication.png)

DC2はDC1の状態を判断できないため、自動昇格はできません。

この状況では`pg_ctl promote`を使用すべきではありません。[動的構成](/ja/docs/patroni/config/dynamic#dynamic)から[standby_cluster](/ja/docs/patroni/standby_cluster#standby_cluster)セクションを削除して、正常なクラスターを「手動で昇格」させる必要があります。

> [!WARNING]
> ソースクラスターがまだ稼働している状態でスタンバイクラスターを昇格させると、スプリットブレインが発生します。

「初期」の状態に戻したい場合、解決する方法は次の二つだけです。

- standby_clusterセクションを再び追加すると、`pg_rewind`が実行されます。ただし、`pg_rewind`を正しく動作させるには、`data page checksums`（`initdb`の`--data-checksums`オプション）を有効にしてクラスターを初期化するか、`wal_log_hints`を`on`に設定する、あるいはその両方を行わなければなりません。それでも、他の要因で`pg_rewind`が失敗する可能性は残ります。
- スタンバイクラスターを最初から再構築します。

スタンバイクラスターを昇格させる前に、ソースクラスターが停止していることを手動で確認しなければなりません（STONITH）。DC1が復旧したら、そのクラスターをスタンバイクラスターに変換する必要があります。

その前に、データベースを手動で調べて、DC1とDC2の間のネットワークが機能しなくなった時点から、DC1のクラスターを手動で停止した時点までに発生したすべての変更を抽出できます。

抽出した変更は、DC2のクラスターに手動で適用することもできます。
