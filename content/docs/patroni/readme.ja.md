---
title: "はじめに"
weight: 10
icon: fa-solid fa-circle-info
description: "Patroniの紹介、クイックスタート、高可用性の基本概念。"
module: [PATRONI]
categories: [概念]
aliases: [/patroni/readme/]
upstream_link: "https://patroni.readthedocs.io/en/latest/README.html"
---

<a id="readme"></a>
Patroniは、Pythonを使用した高可用性（HA）PostgreSQLソリューションのテンプレートです。PatroniはComposeのプロジェクトである[Governor](https://github.com/compose/governor)のフォークとして誕生し、多くの新機能を備えています。

背景については、次も参照してください。

- [KubernetesとPatroniによるPostgreSQLのHA](https://www.youtube.com/watch?v=iruaCgeG7qs)、KubeCon 2016でのJosh Berkusの講演（動画）
- [2016年二月のZalando Techブログ記事](https://engineering.zalando.com/posts/2016/02/zalandos-patroni-a-template-for-high-availability-postgresql.html)

--------

## 開発状況 {#development-status}

Patroniは活発に開発されており、貢献を受け付けています。詳しくは、[貢献](/ja/docs/patroni/contributing_guidelines#contributing_guidelines)のセクションを参照してください。

新しいリリースの情報は[こちら](/ja/docs/patroni/releases#releases)でお知らせしています。

--------

## 技術要件とインストール {#technical-requirementsinstallation}

各プラットフォームでのPatroniのインストールとアップグレードについては、[こちら](/ja/docs/patroni/installation#installation)を参照してください。

<a id="running_configuring"></a>

--------

## PostgreSQLノード数の計画 {#planning-the-number-of-postgresql-nodes}

Patroni/PostgreSQLのノードは、Patroni自身がRAFTを実装する場合を除き、DCSノードから独立しているため、最小ノード数に関する要件はありません。プライマリー一つとスタンバイ一つからなるクラスターでも問題なく動作します。後からスタンバイノードを追加できます。

**2ノードのクラスター**（プライマリーとスタンバイ）は一般的な構成で、高可用性を備えた自動フェイルオーバーを提供します。ただし、フェイルオーバー中は、障害が発生したノードが再参加するまで、一時的に冗長性がなくなることに注意してください。

**DCSの要件**：適切なコンセンサスと耐障害性を確保するには、DCS（etcd、ZooKeeper、Consul）を**3または5ノード**で実行する必要があります。単一のDCSクラスターに、異なるnamespaceとscopeの組み合わせを使用して、数百から数千のPatroniクラスターの情報を保存できます。

--------

## 実行と構成 {#running-and-configuring}

以下では、Patroniリポジトリを<https://github.com/patroni/patroni>からクローンしていることを前提とします。具体的には、構成ファイルの例である`postgres0.yml`と`postgres1.yml`が必要です。pipでPatroniをインストールした場合は、gitリポジトリからこれらのファイルを取得し、以下の`./patroni.py`を`patroni`コマンドに置き換えられます。

以下のコマンドはetcd v2 APIを使用し、etcd 3.5など、`--enable-v2`をサポートするetcdのバージョンが必要です。etcd 3.6以降では、[etcd 3.6でv2 APIのサポートが削除された](https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/)ため、代わりにPatroniの`etcd3`構成を使用してください。

開始するには、それぞれ別のターミナルで次を実行します。

    > etcd --data-dir=data/etcd --enable-v2=true
    > ./patroni.py postgres0.yml
    > ./patroni.py postgres1.yml

これで高可用性クラスターが起動します。YAMLファイルの設定を変更して、クラスターの動作がどのように変化するか試してください。一部のコンポーネントを強制終了して、システムの動作を確認してください。

`postgres*.yml`ファイルを追加すると、さらに大きなクラスターを作成できます。

Patroniは[HAProxy](https://www.haproxy.org/)の構成を提供しており、アプリケーションからクラスターのリーダーへ接続するための単一のエンドポイントを用意できます。構成するには、次を実行します。

    > haproxy -f haproxy.cfg

    > psql --host 127.0.0.1 --port 5000 postgres

--------

## YAMLによる構成 {#yaml-configuration}

etcd、Consul、ZooKeeperの設定に関する詳しい情報は、[こちら](/ja/docs/patroni/config/yaml#yaml)を参照してください。例は[postgres0.yml](https://github.com/patroni/patroni/blob/master/postgres0.yml)を参照してください。

--------

## 環境変数による構成 {#environment-configuration}

環境変数を使用して設定を構成、上書きする方法については、[こちら](/ja/docs/patroni/config/env#env)を参照してください。

--------

## レプリケーションの選択肢 {#replication-choices}

Patroniは、デフォルトで非同期となるPostgresのストリーミングレプリケーションを使用します。Patroniの非同期レプリケーションでは、`maximum_lag_on_failover`を設定できます。この設定により、フォロワーがリーダーから設定されたバイト数を超えて遅れている場合、そのフォロワーはフェイルオーバー時に昇格できなくなります。業務要件に応じて、この設定値を増減することを推奨します。より強い永続性の保証を得るため、同期レプリケーションを使用することもできます。詳しくは、[レプリケーションモードのドキュメント](/ja/docs/patroni/replication_modes#replication_modes)を参照してください。

--------

## アプリケーションでスーパーユーザーを使用しない {#applications-should-not-use-superusers}

アプリケーションから接続するときは、常にスーパーユーザー以外を使用してください。Patroniが正しく動作するには、データベースへのアクセスが必要です。アプリケーションでスーパーユーザーを使用すると、`superuser_reserved_connections`設定でスーパーユーザー用に予約された接続まで含めて、コネクションプール全体を使い切る可能性があります。コネクションプールがいっぱいになってPatroniがプライマリーにアクセスできなくなると、望ましくない動作につながります。

--------

## HAソリューションのテスト {#testing-your-ha-solution}

HAソリューションのテストには、多くの変数が関係し、時間がかかります。複数のプラットフォームに対応するアプリケーションでは、特にそうです。この作業には、訓練を受けたシステム管理者またはコンサルタントが必要です。ドキュメントで詳しく扱いきれるものではありません。

そのうえで、インフラストラクチャーの次の要素は、必ずテストすることを推奨します。

- ネットワーク（システムの手前にあるネットワークと、NIC［物理または仮想］自体）
- ディスクI/O
- ファイルディスクリプタの制限（Linuxではnofile）
- RAM。oomkillerを無効にしていても、RAMを利用できなくなると問題が生じる可能性があります。
- CPU
- 仮想化環境のリソース競合（ハイパーバイザーのオーバーコミット）
- cgroupによるあらゆる制限（上記に関連する可能性があります）
- postgresプロセスに対する`kill -9`（postmasterは除く）。これはセグメンテーションフォールトの適切なシミュレーションになります。

行うべきでないのは、postmasterプロセスに対する`kill -9`です。プロセスを強制終了するだけでは、リソース枯渇やその他のインフラストラクチャー障害の実際の条件を再現できないためです。インフラストラクチャーが安全でなく、攻撃者が`kill -9`を実行できることを懸念しているのであれば、どのようなHAの仕組みでも解決できません。攻撃者は単にプロセスを再び強制終了するか、別の方法で混乱を引き起こすだけです。
