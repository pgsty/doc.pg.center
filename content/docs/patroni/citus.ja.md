---
title: "Citusサポート"
weight: 130
icon: fas fa-lemon
description: "Citusのコーディネーターとワーカーグループに対するPatroniの統合の詳細。"
module: [PATRONI]
categories: [概念]
aliases: [/patroni/citus/]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
Patroniを使用すると、[マルチノードCitus](https://docs.citusdata.com/en/stable/installation/multi_node.html)クラスターを極めて簡単にデプロイできます。

--------

## 要点 {#tldr}

必要なのは、次の簡単なルールに従うことだけです。

1. PostgreSQLのデータベース拡張[Citus](https://github.com/citusdata/citus)は、すべてのノードで利用可能になっている必要があります。絶対的な最小サポートバージョンはCitus 10.0ですが、ワーカーの透過的なスイッチオーバーと再起動の利点をすべて活用するには、Citus 11.2以降の使用を推奨します。
2. クラスター名（`scope`）は、すべてのCitusノードで同じにする必要があります。
3. スーパーユーザーの認証情報は、コーディネーターとすべてのワーカーノードで同じである必要があります。また、`pg_hba.conf`では、全ノード間のスーパーユーザーアクセスを許可しておくべきです。
4. ワーカーノードからコーディネーターへの[REST API](/ja/docs/patroni/config/yaml#restapi_settings)アクセスは許可しておくべきです。たとえば認証情報は同じにし、クライアント証明書を設定している場合は、コーディネーターがワーカーノードの証明書を受け入れなければなりません。
5. `patroni.yaml`に次のセクションを追加します。

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

後はPatroniを起動するだけで、残りの処理を実行します。

0. `bootstrap.dcs.synchronous_mode`が他の値に明示的に設定されていない場合、Patroniはこれを[quorum](/ja/docs/patroni/replication_modes#quorum_mode)に設定します。
1. [citus](/ja/docs/patroni/citus#citus)拡張を`shared_preload_libraries`に自動的に追加します。
2. グローバルな[動的設定](/ja/docs/patroni/config/dynamic#dynamic)で`max_prepared_transactions`が明示的に設定されていない場合、Patroniは自動的にこれを`2*max_connections`に設定します。
3. `citus.local_hostname`のGUC値を、`localhost`からPatroniがローカルのPostgreSQLインスタンスへの接続に使用する値へ変更します。PostgreSQLが`localhost`でリッスンしていない場合があるため、別の値が必要になることがあります。
4. `citus.database`で指定したデータベースを自動的に作成し、続いて`CREATE EXTENSION citus`を実行します。
5. ノード間の通信を可能にするため、現在のスーパーユーザーの[認証情報](/ja/docs/patroni/config/yaml#postgresql_settings)を`pg_dist_authinfo`テーブルに追加します。後からスーパーユーザーのusername/password/sslcert/sslkeyを変更する場合は、この情報の更新も忘れないでください。
6. コーディネーターのプライマリーノードは、ワーカーのプライマリーノードを自動検出し、`citus_add_node()`関数で`pg_dist_node`テーブルに追加します。
7. コーディネーターまたはワーカーのクラスターでフェイルオーバーやスイッチオーバーが発生した場合も、Patroniが`pg_dist_node`を維持します。

--------

## patronictl {#patronictl}

コーディネーターとワーカーのクラスターは、物理的には異なるPostgreSQL/Patroniクラスターです。PostgreSQLのデータベース拡張[Citus](https://github.com/citusdata/citus)で論理的にまとめているだけなので、多くの場合は単一の実体として管理できません。

このため、`patroni.yaml`に[citus](/ja/docs/patroni/citus#citus)セクションがある場合、[patronictl](/ja/docs/patroni/patronictl#patronictl)の動作には通常と比べて2つの主な違いがあります。

1. `list`と`topology`は、デフォルトでCitus構成全体のメンバー（コーディネーターとワーカー）を出力します。新しい`Group`列に、所属するCitusグループが表示されます。
2. すべての[patronictl](/ja/docs/patroni/patronictl#patronictl)コマンドに、新しい`--group`オプションが追加されます。一部のコマンドでは、グループのデフォルト値を`patroni.yaml`から取得する場合があります。たとえば[`patronictl pause`](/ja/docs/patroni/patronictl#patronictl_pause)は、デフォルトで[citus](/ja/docs/patroni/citus#citus)セクションの`group`に対してメンテナンスモードを有効にします。一方、[`patronictl switchover`](/ja/docs/patroni/patronictl#patronictl_switchover)や[`patronictl remove`](/ja/docs/patroni/patronictl#patronictl_remove)などでは、グループを明示的に指定する必要があります。

Citusクラスターでの[`patronictl list`](/ja/docs/patroni/patronictl#patronictl_list)の出力例：

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     1 | work1-2 | 172.27.0.2  | Leader         | running |  1 |             |     |            |     |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

`--group`オプションを追加すると、出力は次のように変わります。

    postgres@coord1:~$ patronictl list demo --group 0
    + Citus cluster: demo (group: 0, 7179854923829112860) -+-------------+-----+------------+-----+
    | Member | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    | coord1 | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord2 | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord3 | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+

    postgres@coord1:~$ patronictl list demo --group 1
    + Citus cluster: demo (group: 1, 7179854923881963547) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work1-1 | 172.27.0.8 | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    | work1-2 | 172.27.0.2 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+

--------

## Citusワーカーのスイッチオーバー {#citus-worker-switchover}

Citusワーカーノードのスイッチオーバーを調整して実行する場合、Citusでは、アプリケーションからほぼ透過的に切り替えることができます。アプリケーションはコーディネーターに接続し、そこからワーカーノードへ接続するため、ワーカーノード上のシャードに対するSQLトラフィックを、Citusでコーディネーター上に一時停止できます。そのトラフィックをコーディネーターに保持している間にスイッチオーバーを行い、新しいプライマリーのワーカーノードが読み書きのクエリーを受け付ける準備を終え次第、トラフィックを再開します。

ワーカークラスターでの[`patronictl switchover`](/ja/docs/patroni/patronictl#patronictl_switchover)の例：

    postgres@coord1:~$ patronictl switchover demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    Citus group: 2
    Primary [work2-2]:
    Candidate ['work2-1'] []:
    When should the switchover take place (e.g. 2024-08-26T08:02 )  [now]:
    Current cluster topology
    + Citus cluster: demo (group: 2, 7179854924063375386) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work2-1 | 172.27.0.5 | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    | work2-2 | 172.27.0.7 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    Are you sure you want to switchover cluster demo, demoting current primary work2-2? [y/N]: y
    2024-08-26 07:02:40.33003 Successfully switched over to "work2-1"
    + Citus cluster: demo (group: 2, 7179854924063375386) --------+---------+------------+---------+
    | Member  | Host       | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+
    | work2-1 | 172.27.0.5 | Leader  | running |  1 |             |         |            |         |
    | work2-2 | 172.27.0.7 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Leader         | running |  2 |             |     |            |     |
    |     2 | work2-2 | 172.27.0.7  | Quorum Standby | running |  2 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

コーディネーター側では、次のようになります。

    # The worker primary notifies the coordinator that it is going to execute "pg_ctl stop".
    2024-08-26 07:02:38,636 DEBUG: query(BEGIN, ())
    2024-08-26 07:02:38,636 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.7-demoted', 5432, 10000))
    # From this moment all application traffic on the coordinator to the worker group 2 is paused.

    # The old worker primary is assigned as a secondary.
    2024-08-26 07:02:40,084 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (7, '172.19.0.7', 5432, 10000))

    # The future worker primary notifies the coordinator that it acquired the leader lock in DCS and about to run "pg_ctl promote".
    2024-08-26 07:02:40,085 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.5', 5432, 10000))

    # The new worker primary just finished promote and notifies coordinator that it is ready to accept read-write traffic.
    2024-08-26 07:02:41,485 DEBUG: query(COMMIT, ())
    # From this moment the application traffic on the coordinator to the worker group 2 is unblocked.

--------

## セカンダリーノード {#secondary-nodes}

Patroni v4.0.0以降では、`noloadbalance`[タグ](/ja/docs/patroni/config/yaml#tags_settings)が付いていないCitusセカンダリーノードも`pg_dist_node`に登録されます。ただし、アプリケーションが読み取り専用クエリーにセカンダリーノードを使用するには、[citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum)のGUCを変更する必要があります。

--------

## DCSの内部構造 {#peek-into-dcs}

Citusクラスター（コーディネーターとワーカー）は、論理的にまとめたPatroniクラスター群としてDCSに保存されます。

    /service/batman/              # scope=batman
    /service/batman/0/            # citus.group=0, coordinator
    /service/batman/0/initialize
    /service/batman/0/leader
    /service/batman/0/members/
    /service/batman/0/members/m1
    /service/batman/0/members/m2
    /service/batman/1/            # citus.group=1, worker
    /service/batman/1/initialize
    /service/batman/1/leader
    /service/batman/1/members/
    /service/batman/1/members/m3
    /service/batman/1/members/m4
    ...

この方式を採用したのは、ほとんどのDCSで、1回の再帰的な読み取り要求によりCitusクラスター全体を取得できるためです。ツリー全体を読み取るのは、ワーカーノードを検出する必要があるCitusコーディネーターノードだけです。ワーカーノードは、自身のグループのサブツリーだけを読み取り、場合によってはコーディネーターグループのサブツリーも読み取ります。

--------

## Kubernetes上のCitus {#citus-on-kubernetes}

Kubernetesは階層構造をサポートしないため、Patroniが作成するすべてのK8sオブジェクトにcitusグループを含める必要がありました。

    batman-0-leader  # the leader config map for the coordinator
    batman-0-config  # the config map holding initialize, config, and history "keys"
    ...
    batman-1-leader  # the leader config map for worker group 1
    batman-1-config
    ...

つまり、命名パターンは`${scope}-${citus.group}-${type}`です。

Patroniは[ラベルセレクター](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)を使用してすべてのKubernetesオブジェクトを検出します。そのため、PatroniとCitusを実行するすべてのPodとEndpoints/ConfigMapsには共通のラベルセレクターに一致するラベルを付け、Patroniがそれらを使用するようにKubernetesの[設定](/ja/docs/patroni/config/yaml#kubernetes_settings)または[環境変数](/ja/docs/patroni/config/env#kubernetes_environment)で指定する必要があります。

Podの環境変数を使用したPatroni設定の例を2つ示します。

1. コーディネータークラスターの場合

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "0"
    citus-type: coordinator
    cluster-name: citusdemo
  name: citusdemo-0-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "0"
```

2. グループ2のワーカークラスターの場合

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "2"
    citus-type: worker
    cluster-name: citusdemo
  name: citusdemo-2-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "2"
```

どちらの例でも、`citus-group`ラベルが設定されています。このラベルにより、PatroniはオブジェクトがどのCitusグループに属するかを識別します。また、`citus-group`ラベルと同じ値を持つ`PATRONI_CITUS_GROUP`環境変数もあります。Patroniが新しいKubernetesのConfigMapsやEndpointsを作成すると、自動的に`citus-group: ${env.PATRONI_CITUS_GROUP}`ラベルを付けます。

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: citusdemo-0-leader  # Is generated as ${env.PATRONI_SCOPE}-${env.PATRONI_CITUS_GROUP}-leader
  labels:
    application: patroni    # Is set from the ${env.PATRONI_KUBERNETES_LABELS}
    cluster-name: citusdemo # Is automatically set from the ${env.PATRONI_SCOPE}
    citus-group: '0'        # Is automatically set from the ${env.PATRONI_CITUS_GROUP}
```

Citusに対応したPatroniをKubernetesにデプロイする完全な例は、Patroniリポジトリの[kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes)フォルダーにあります。

重要なファイルは次の2つです。

1. Dockerfile.citus
2. citus_k8s.yaml

--------

## CitusのアップグレードとPostgreSQLのメジャーアップグレード {#citus-upgrades-and-postgresql-major-upgrades}

まず、[ドキュメント](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html)でCitusのバージョンアップグレードについて確認してください。手順に小さな違いが1つあります。アップグレード時にPostgreSQLを再起動するには、`systemctl restart`の代わりに[`patronictl restart`](/ja/docs/patroni/patronictl#patronictl_restart)を使用する必要があります。

Citusを使用したPostgreSQLのメジャーアップグレードは、もう少し複雑です。Citusのメジャーアップグレードのドキュメントと、Patroniの[PostgreSQLのメジャーバージョンアップグレード](/ja/docs/patroni/existing_data#major_upgrade)のドキュメントにある手法を組み合わせる必要があります。Citusクラスターは多数のPatroniクラスター（コーディネーターとワーカー）で構成されており、それぞれを個別にアップグレードする必要がある点に注意してください。
