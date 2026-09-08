---
title: "YAML 構成設定"
linkTitle: "YAML 構成"
weight: 10
icon: fa-solid fa-code
description: "Patroni YAML 構成オプションとセクションの完全なリファレンス。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/patroni/config/yaml/]
upstream_link: "https://patroni.readthedocs.io/en/latest/yaml_configuration.html"
---

<a id="yaml"></a>

--------

## グローバル/ユニバーサル {#globaluniversal}

- **thread_pool_size**: リーダー競合またはフェールセーフ チェック中に、非同期タスクを実行し、REST API を介して他のメンバーと通信するために Patroni によって使用されるスレッド プールのサイズ。最小値は `5`、デフォルト値は `5` です。
- **thread_stack_size**: Patroni によって開始されるスレッドに使用されるスタック サイズを指定します。値は `64kB` によってアライメントされる必要があります。最小値は `64kB` 、デフォルト値 (Patroni によって設定) は `512kB` です。
- **name**: ホストの名前。クラスター内で一意である必要があります。値 `__patroni_strict_sync_replica_placeholder__` は、Patroni による内部使用のために予約されており、ノード名として使用することはできません。
- **namespace**: Patroni がクラスターに関する情報を保持する構成ストア内のパス。デフォルト値: 「/service」
- **scope**: クラスター名

<a id="log_settings"></a>

--------

## ログ {#log}

- **type**: ログの形式を設定します。 **plain** または **json** のいずれかになります。 **json** 形式を使用するには、[jsonlogger](/ja/docs/patroni/installation#extras) がインストールされている必要があります。デフォルト値は **plain** です。
- **level**: 一般的なログ レベルを設定します。デフォルト値は **INFO** です ([Python ロギングのドキュメント](https://docs.python.org/3.6/library/logging.html#levels) を参照)
- **traceback_level**: トレースバックが表示されるレベルを設定します。デフォルト値は **ERROR** です。 **DEBUG** を有効にした場合にのみトレースバックを表示したい場合は、**DEBUG** に設定します。
- **format**: ログのフォーマット文字列を設定します。ログ タイプが **plain** の場合、ログ形式は文字列である必要があります。使用可能な属性については、[LogRecord 属性](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) を参照してください。ログ タイプが **json** の場合、ログ形式は文字列に加えてリストにすることもできます。各リスト項目は LogRecord 属性に対応する必要があります。フィールド名のみが必要であり、**%(** と **)** は省略する必要があることに注意してください。別のキー名でログ フィールドを出力する場合は、辞書キーがログ フィールドで、値がログに出力するフィールドの名前である辞書を使用します。デフォルト値は **%(asctime)s %(レベル名)s: %(メッセージ)s** です。
- **dateformat**: 日時フォーマット文字列を設定します。 ([formatTime() ドキュメント](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime) を参照)
- **static_fields**: ログにフィールドを追加します。このオプションは、ログ タイプが **json** に設定されている場合にのみ使用できます。
- **max_queue_size**: Patroni は 2 段階のロギングを使用しています。ログ レコードはメモリ内のキューに書き込まれ、キューからログ レコードを取得して stderr またはファイルに書き込む別のスレッドがあります。内部キューの最大サイズはデフォルトで **1000** レコードによって制限されており、過去 1 時間 20 分までのログを保持するには十分なサイズです。
- **dir**: アプリケーション ログを書き込むディレクトリ。ディレクトリは存在し、Patroni を実行するユーザーによって書き込み可能である必要があります。この値を設定すると、アプリケーションはデフォルトで 4 25MB ログを保持します。これらの保持値は、`file_num` および `file_size` を使用して調整できます (以下を参照)。
- **mode**: ログ ファイルのアクセス許可 (`0644` など)。指定しない場合、権限は現在の umask 値に基づいて設定されます。
- **file_num**: 保持するアプリケーション ログの数。
- **file_size**: ログ ローリングをトリガーする patroni.log ファイルのサイズ (バイト単位)。
- **loggers**: このセクションでは、Python モジュールごとにログ レベルを再定義できます。
  - **patroni.postmaster: WARNING**
  - **urllib3: DEBUG**
- **deduplicate_heartbeat_logs**: `true` に設定すると、同一のハートビート ログが連続して出力されなくなります。デフォルト値は `false` です。

> [!WARNING]
> HA ループの実行時間は、リソースの枯渇や同様の問題によるフェイルオーバーを診断する際に非常に貴重な情報となる可能性があります。 `deduplicate_heartbeat_logs` が `true` に設定されている場合、(リーダーが変更されない限り) HA ループ実行のログは生成されないため、この潜在的に役立つ情報はログから取得できません。

ここでは、JSON 形式でログを記録するように Patroni を設定する方法の例を示します。

```yaml
log:
   type: json
   format:
      - message
      - module
      - asctime: '@timestamp'
      - levelname: level
   static_fields:
      app: patroni
```

<a id="bootstrap_settings"></a>

--------

## Bootstrap 構成 {#bootstrap-configuration}

> [!NOTE]
> Patroni が初めてクラスターを初期化し、設定が DCS に保存されると、YAML 構成の `bootstrap.dcs` セクションに対する今後の変更はすべて反映されなくなります。変更したい場合は、[patronictl_edit_config](/ja/docs/patroni/patronictl#patronictl_edit_config) または Patroni [REST API](/ja/docs/patroni/rest_api#rest_api) を使用してください。

- **bootstrap**:
  - **dcs**: このセクションは、新しいクラスターの初期化後に、指定された構成ストアの <span class="title-ref">/\<namespace\>/\<scope\>/config</span> に書き込まれます。クラスターのグローバル動的構成。 [動的構成設定](/ja/docs/patroni/config/dynamic#dynamic) で説明されているパラメーターのいずれかを `bootstrap.dcs` の下に置くことができ、Patroni が新しいクラスターを初期化 (ブートストラップ) した後、このセクションが構成ストアの <span class="title-ref">/\<namespace\>/\<scope\>/config</span> に書き込まれます。

  - **method**: このクラスターのブートストラップに使用するカスタム スクリプト。

    詳細については、[カスタム ブートストラップ メソッドのドキュメント](/ja/docs/patroni/replica_bootstrap#custom_bootstrap) を参照してください。 `initdb` が指定されている場合は、デフォルトの `initdb` コマンドに戻ります。 `initdb` は、構成ファイルに `method` パラメーターが存在しない場合にもトリガーされます。

  - **initdb**: (オプション) initdb に渡されるオプションをリストします。

    - **- データチェックサム**: 9.3 で pg_rewind が必要な場合は有効にする必要があります。
    - **- エンコーディング: UTF8**: 新しいデータベースのデフォルトのエンコード。
    - **- ロケール: UTF8**: 新しいデータベースのデフォルトのロケール。

  - **post_bootstrap** または **post_init**: クラスターの初期化後に実行される追加のスクリプト。スクリプトは、接続文字列 URL (ユーザー名としてクラスター スーパーユーザーを含む) を受け取ります。 PGPASSFILE 変数は、pgpass ファイルの場所に設定されます。

<a id="citus_settings"></a>

--------

## シタス {#citus}

Patroni と [Citus](https://docs.citusdata.com) の統合を有効にします。構成されている場合、Patroni はコーディネーターへの Citus ワーカー ノードの登録を処理します。 Citus サポート [ここで](/ja/docs/patroni/citus#citus) の詳細については、こちらをご覧ください。

- **group**: Citus グループ ID、整数。コーディネーターには `0` を使用し、ワーカーには `1`、`2` などを使用します。
- **database**: [柑橘類](/ja/docs/patroni/citus#citus) 拡張機能を作成するデータベース。コーディネーターとすべてのワーカーで同じである必要があります。現在サポートされているデータベースは 1 つだけです。

<a id="consul_settings"></a>

--------

## Consul {#consul}

ほとんどのパラメーターはオプションですが、**host** または **url** のいずれかを指定する必要があります。

- **host**: Consul ローカル エージェントのホスト:ポート。
- **url**: Consul ローカル エージェントの URL (形式: http(s)://host:port)。
- **port**: (オプション) Consul ポート。
- **scheme**: (オプション) **http** または **https**、デフォルトは **http** です。
- **token**: (オプション) ACL トークン。
- **verify**: (オプション) HTTPS リクエストの SSL 証明書を検証するかどうか。
- **cacert**: (オプション) CA 証明書。存在する場合、検証が有効になります。
- **cert**: (オプション) クライアント証明書を含むファイル。
- **key**: (オプション) クライアント キーを含むファイル。キーが **cert** の一部である場合は空にすることができます。
- **dc**: (オプション) 通信するデータセンター。デフォルトでは、ホストのデータセンターが使用されます。
- **consistency**: (オプション) consul 整合性モードを選択します。可能な値は `default`、`consistent`、または `stale` です (詳細については [領事 API リファレンス](https://www.consul.io/api/features/consistency.html/) を参照)
- **checks**: (オプション) セッションに使用される Consul ヘルス チェックのリスト。デフォルトでは、空のリストが使用されます。
- **register_service**: (オプション) スコープ パラメーターと、ノードのロールに応じたタグ マスター、プライマリー、レプリカ、またはスタンバイ リーダーによって定義された名前でサービスを登録するかどうか。デフォルトは **false** です。
- **service_tags**: (オプション) ロール (`primary`/`replica`/`standby-leader`) とは別に Consul サービスに追加する追加の静的タグ。デフォルトでは、空のリストが使用されます。
- **service_check_interval**: (オプション) 登録された URL に対してヘルス チェックを実行する頻度。デフォルトは「5s」です。
- **service_check_tls_server_name**: (オプション) TLS 経由で接続するときに SNI ホストをオーバーライドします。[領事エージェントチェック API リファレンス](https://www.consul.io/api-docs/agent/check#tlsservername) も参照してください。

`token` には、次の ACL 権限が必要です。

    service_prefix "${scope}" {
        policy = "write"
    }
    key_prefix "${namespace}/${scope}" {
        policy = "write"
    }
    session_prefix "" {
        policy = "write"
    }

--------

## など {#etcd}

ほとんどのパラメーターはオプションですが、**host**、**hosts**、**url**、**proxy**、または **srv** のいずれかを指定する必要があります。

- **host**: etcd エンドポイントのホスト:ポート。
- **hosts**: host1:port1、host2:port2 などの形式の etcd エンドポイントのリスト。カンマ区切りの文字列または実際の yaml リストの可能性があります。
- **use_proxies**: このパラメータが true に設定されている場合、Patroni は **hosts** をプロキシのリストと見なし、etcd クラスターのトポロジ検出を実行しません。
- **url**: etcd の URL。
- **proxy**: etcd のプロキシ URL。プロキシを使用して etcd に接続している場合は、**url** の代わりにこのパラメーターを使用します。
- **srv**: クラスター自動検出のために SRV レコードを検索するドメイン。 Patroni は、指定されたドメインの SRV サービス名 (最初に成功するまでこの順序で) のクエリーを試行します: `_etcd-client-ssl`、`_etcd-client`、`_etcd-ssl`、`_etcd`、`_etcd-server-ssl`、`_etcd-server`。 `_etcd-server-ssl` または `_etcd-server` の SRV レコードが取得された場合、ETCD ピア プロトコルが使用され、利用可能なメンバーについて ETCD がクエリーされます。それ以外の場合は、SRV レコードのホストが使用されます。
- **srv_suffix**: 検出中にクエリーされる SRV 名のサフィックスを構成します。このフラグを使用して、同じドメイン内の複数の etcd クラスターを区別します。 **srv** と組み合わせた場合にのみ機能します。たとえば、`srv_suffix: foo` と `srv: example.org` が設定されている場合、DNS SRV クエリーが作成されます:`_etcd-client-ssl-foo._tcp.example.com` (考えられるすべての ETCD SRV サービス名に対して同様)。
- **protocol**: (オプション) http または https (指定しない場合は http が使用されます)。 **url** または **proxy** が指定されている場合は、それらからプロトコルを取得します。
- **username**: (オプション) etcd 認証用のユーザー名。
- **password**: (オプション) etcd 認証用のパスワード。
- **cacert**: (オプション) CA 証明書。存在する場合、検証が有効になります。
- **cert**: (オプション) クライアント証明書を含むファイル。
- **key**: (オプション) クライアント キーを含むファイル。キーが **cert** の一部である場合は空にすることができます。

--------

## etcdv3 {#etcdv3}

Patroni をプロトコル バージョン 3 経由で etcd クラスターと連携させたい場合は、Patroni 構成ファイルの `etcd3` セクションを使用する必要があります。すべての構成パラメータは `etcd` の場合と同じです。

> [!WARNING]
> プロトコル バージョン 2 で作成された Key は、プロトコル バージョン 3 では表示されず、その逆も同様であるため、Patroni 構成ファイルを更新するだけで `etcd` から `etcd3` に切り替えることはできません。さらに、Patroni は etcd の gRPC ゲートウェイ (プロキシ) を使用して V3 API と通信します。これは、TLS 共通名認証が不可能であることを意味します。

--------

## ZooKeeper {#zookeeper}

- **hosts**: ZooKeeper クラスター メンバーのリスト (形式: \['host1:port1', 'host2:port2', 'etc...'\])。
- **use_ssl**: (オプション) SSL が使用されているかどうか。デフォルトは `false` です。 `false` に設定すると、SSL 固有のパラメーターはすべて無視されます。
- **cacert**: (オプション) CA 証明書。存在する場合、検証が有効になります。
- **cert**: (オプション) クライアント証明書を含むファイル。
- **key**: (オプション) クライアント キーを含むファイル。
- **key_password**: (オプション) クライアント キーのパスワード。
- **verify**: (オプション) 証明書を検証するかどうか。デフォルトは `true` です。
- **set_acls**: (オプション) 設定した場合、作成する各 ZNode にデフォルトの ACL を適用するように Kazoo を構成します。 ACL では、`x509` スキーマ (デフォルト)、または `digest` などの他のサポートされている ZooKeeper スキーマのいずれかを使用できます。これらは、キーが完全なプリンシパル (オプションでスキームの接頭辞が付けられる) であり、値がアクセス許可のリストであるディクショナリとして指定する必要があります。権限は、`CREATE`、`READ`、`WRITE`、`DELETE`、`ADMIN`、または `ALL` の 1 つ以上です。たとえば、`set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}` です。
- **auth_data**: (オプション) 接続に使用する認証資格情報。 `scheme` がキー、`credential` が値という形式の辞書である必要があります。デフォルトは空の辞書です。

> [!NOTE]
> SSL をサポートするには、`kazoo>=2.6.0` をインストールする必要があります。

--------

## 出展者 {#exhibitor}

- **hosts**: エキシビター (ZooKeeper) ノードの初期リスト (形式: 「host1、host2、etc...」)。このリストは、エキシビター (ZooKeeper) クラスター トポロジが変更されるたびに自動的に更新されます。
- **poll_interval**: ZooKeeper およびエキシビター ノードのリストをエキシビターから更新する頻度。
- **port**: エキシビターポート。

<a id="kubernetes_settings"></a>

--------

## Kubernetes {#kubernetes}

- **bypass_api_service**: (オプション) Kubernetes API と通信する場合、Patroni は通常 [Kubernetes](/ja/docs/patroni/kubernetes#kubernetes) サービスに依存し、そのアドレスは `KUBERNETES_SERVICE_HOST` 環境変数を介してポッド内で公開されます。 `bypass_api_service` が `true` に設定されている場合、Patroni はサービスの背後にある API ノードのリストを解決し、それらのノードに直接接続します。
- **namespace**: (オプション) Patroni ポッドが実行されている Kubernetes 名前空間。デフォルト値は `default` です。
- **labels**: `{label1: value1, label2: value2}` 形式のラベル。これらのラベルは、現在のクラスターに関連付けられている既存のオブジェクト (ポッドとエンドポイントまたは ConfigMaps) を検索するために使用されます。また、Patroni は、作成するすべてのオブジェクト (エンドポイントまたは ConfigMap) にそれらを設定します。
- **scope_label**: (オプション) クラスター名を含むラベルの名前。デフォルト値は `cluster-name` です。
- **bootstrap_labels**: (オプション) `{label1: value1, label2: value2}` 形式のラベル。これらのラベルは、Patroni ポッドの状態が `initializing new cluster`、`running custom bootstrap script`、`starting after custom bootstrap`、または `creating replica` のいずれかである場合にそのポッドに割り当てられます。
- **role_label**: (オプション) ロールを含むラベルの名前 (`primary`、`replica`、またはその他のカスタム値)。 Patroni は、実行されるポッドにこのラベルを設定します。デフォルト値は `role` です。
- **leader_label_value**: (オプション) Postgres ロールが `primary` の場合のポッド ラベルの値。デフォルト値は `primary` です。
- **follower_label_value**: (オプション) Postgres ロールが `replica` の場合のポッド ラベルの値。デフォルト値は `replica` です。
- **standby_leader_label_value**: (オプション) Postgres ロールが `standby_leader` の場合のポッド ラベルの値。デフォルト値は `primary` です。
- **tmp_role_label**: (オプション) ロールを含む一時ラベルの名前 (`primary` または `replica`)。このラベルの値には、対応するロールのデフォルトが常に使用されます。必要な場合のみ設定してください。
- **use_endpoints**: (オプション) true に設定すると、Patroni は ConfigMaps の代わりにエンドポイントを使用してリーダーの選出を実行し、クラスターの状態を維持します。
- **pod_ip**: (オプション) Patroni が実行されているポッドの IP アドレス。 この値は `use_endpoints` が有効な場合に必須であり、ポッドの PostgreSQL が昇格されるときにリーダー エンドポイント サブセットを設定するために使用されます。
- **ports**: (オプション) Service オブジェクトにポートの名前がある場合、同じ名前が Endpoint オブジェクトに表示される必要があります。そうでない場合、サービスは機能しません。たとえば、サービスが `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}` として定義されている場合、`kubernetes.ports: [{"name": "postgresql", "port": 5432}]` を設定する必要があります。これにより、Patroni はリーダー エンドポイントのサブセットの更新にそれを使用します。このパラメータは、`kubernetes.use_endpoints` が設定されている場合にのみ使用されます。
- **cacert**: (オプション) Kubernetes API SSL 証明書の検証中に使用する、信頼できる CA の証明書を含む CA_BUNDLE ファイルを指定します。指定されない場合、Patroni は ServiceAccount シークレットによって提供される値を使用します。
- **retriable_http_codes**: (オプション) 再試行する K8s API からの HTTP ステータス コードのリスト。デフォルトでは、Patroni は、`500`、`503`、および `504`、または K8s API 応答に `retry-after` HTTP ヘッダーがある場合に再試行します。

<a id="raft_settings"></a>

--------

## Raft (非推奨) {#raft-deprecated}

- **self_addr**: Raft 接続をリッスンする `ip:port`。 `self_addr` はクラスターの他のノードからアクセスできる必要があります。設定されていない場合、ノードはコンセンサスに参加しません。

- **bind_addr**: (オプション) Raft 接続をリッスンする `ip:port`。指定しない場合は、`self_addr` が使用されます。

- **partner_addrs**: クラスター内の他の Patroni ノードのリスト (形式: \['ip1:port', 'ip2:port', 'etc...'\])

- **data_dir**: Raft ログとスナップショットを保存するディレクトリ。指定しない場合は、現在の作業ディレクトリが使用されます。

- **password**: (オプション) 指定されたパスワードで Raft トラフィックを暗号化します。`cryptography` Python モジュールが必要です。
- **min_timeout**: (オプション) 基礎となる pysyncobj Raft 実装の最小選出タイムアウト (秒単位)。 3 * `append_entries_period` より大きくなければなりません。デフォルト： `0.4`。
- **max_timeout**: (オプション) 基礎となる pysyncobj Raft 実装の最大選出タイムアウト (秒単位)。 `min_timeout` より大きくなければなりません。デフォルト： `1.4`。
- **connection_timeout**: (オプション) データを受信しなかった接続が切断されたとみなされるまでの秒数。 `max_timeout` 以上である必要があります。デフォルト： `3.5`。
- **append_entries_period**: (オプション) ハートビート (append_entries) コマンドを送信する間隔 (秒単位)。 `min_timeout` の 3 分の 1 未満である必要があります。デフォルト： `0.1`。
- **connection_retry_time**: (オプション) オフライン ノードへの再接続試行間の秒単位の間隔。デフォルト： `5.0`。
- **leader_fallback_timeout**: (オプション) 過半数からの応答がないリーダーがフォロワー状態に戻るまでの秒数。 `append_entries_period` より大きくなければなりません。デフォルト： `30.0`。

> [!NOTE]
> これらのタイムアウト パラメーターは、デフォルトの pysyncobj タイムアウトが長すぎる高遅延ネットワークに役立ちます。次の制約を満たす必要があります: `min_timeout` > 3 * `append_entries_period`、`max_timeout` > `min_timeout`、`connection_timeout` >= `max_timeout`、および `leader_fallback_timeout` > `append_entries_period`。 Patroni は起動時にこれらを検証し、違反している場合は起動を拒否します。これらの値は実行時に変更できないため、再起動が必要です。
>
> [!WARNING]
> これらのノブは、pysyncobj の選択と接続のタイムアウトを緩和するだけです。 Patroni が Raft 操作に適用するコマンドごとの期限は延長されません。各 Raft コマンド (リーダー ロックのリフレッシュ、クラスター状態の書き込み) は依然として `retry_timeout` (デフォルト `10`) 内で完了する必要があります。遅延が非常に長いリンク (ラウンドトリップ時間がおよそ数秒を超える場合) では、`connection_timeout` が RTT を大きく上回っていても、1 つのコマンドが `retry_timeout` を超える可能性があるため、DCS は到達不能であるように見え、プライマリーが降格される可能性があります。このようなリンクでは、`loop_wait + 2 * retry_timeout <= ttl` を維持しながら、それに応じて `retry_timeout` および `ttl` も発生させる必要があります。

Raft 実装に関する短い FAQ

  - Q: コンセンサスを提供するすべてのノードをリストするにはどうすればよいですか?

    A: `syncobj_admin -conn host:port -status` ここで、host:port はクラスター ノードの 1 つのアドレスです。

  - Q: コンセンサスの一部であったノードがなくなったため、同じ IP を他のノードに再利用できません。このノードをコンセンサスから削除するにはどうすればよいですか?

    A: `syncobj_admin -conn host:port -remove host2:port2` ここで、`host2:port2` はコンセンサスから削除するノードのアドレスです。

  - Q: `syncobj_admin` ユーティリティはどこで入手できますか?

    A: Patroni 依存関係である `pysyncobj` モジュール (Python RAFT 実装) と一緒にインストールされます。

  - Q: コンセンサスに追加せずに Patroni ノードを実行することは可能ですか?

    A: はい、Patroni 構成から `raft.self_addr` をコメントアウトするか削除してください。

  - Q: Patroni と PostgreSQL は 2 つのノードでのみ実行できますか?

    A: はい、3 番目のノードでは `patroni_raft_controller` を実行できます (Patroni と PostgreSQL は使用しません)。このような設定では、プライマリーに影響を与えることなく、一時的に 1 つのノードを失う可能性があります。

<a id="postgresql_settings"></a>

--------

## PostgreSQL {#postgresql}

- **postgresql**:
  - **authentication**:

    - **superuser**:
      - **username**: スーパーユーザーの名前。初期化 (initdb) 中に設定され、後で postgres に接続するために Patroni によって使用されます。
      - **password**: スーパーユーザーのパスワード。初期化 (initdb) 中に設定されます。
      - **sslmode**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
      - **sslkey**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
      - **sslpassword**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`sslkey`で指定した秘密鍵のパスワードを指定します。
      - **sslcert**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
      - **sslrootcert**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
      - **sslcrl**: (optional) maps to the [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) connection parameter, which specifies the location of a file containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslcrldir**: (optional) maps to the [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) connection parameter, which specifies the location of a directory with files containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslnegotiation**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
      - **gssencmode**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
      - **channel_binding**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメータにマップされ、クライアントによるチャネル バインディングの使用を制御します。
    - **replication**:
      - **username**: レプリケーション ユーザー名。ユーザーは初期化中に作成されます。レプリカはこのユーザーを使用して、ストリーミング レプリケーション経由でレプリケーション ソースにアクセスします。
      - **password**: レプリケーションのパスワード。ユーザーは初期化中に作成されます。
      - **sslmode**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
      - **sslkey**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
      - **sslpassword**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`sslkey`で指定した秘密鍵のパスワードを指定します。
      - **sslcert**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
      - **sslrootcert**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
      - **sslcrl**: (optional) maps to the [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) connection parameter, which specifies the location of a file containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslcrldir**: (optional) maps to the [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) connection parameter, which specifies the location of a directory with files containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslnegotiation**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
      - **gssencmode**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
      - **channel_binding**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメータにマップされ、クライアントによるチャネル バインディングの使用を制御します。
    - **rewind**:
      - **username**: (オプション) `pg_rewind` のユーザーの名前。ユーザーは postgres 11+ の初期化中に作成され、必要なすべての [権限](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) が付与されます。
      - **password**: (オプション) `pg_rewind` のユーザーのパスワード。ユーザーは初期化中に作成されます。
      - **sslmode**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
      - **sslkey**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
      - **sslpassword**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`sslkey`で指定した秘密鍵のパスワードを指定します。
      - **sslcert**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
      - **sslrootcert**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
      - **sslcrl**: (optional) maps to the [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) connection parameter, which specifies the location of a file containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslcrldir**: (optional) maps to the [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) connection parameter, which specifies the location of a directory with files containing a certificate revocation list.クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
      - **sslnegotiation**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
      - **gssencmode**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
      - **channel_binding**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメーターにマップされ、クライアントによるチャネル バインディングの使用を制御します。

  - **callbacks**: 特定のアクションで実行するコールバック スクリプト。 Patroni は、アクション、ロール、クラスター名を渡します。 (記述方法の例として scripts/aws.py を参照してください。)

    - **on_reload**: 構成のリロードがトリガーされたときにこのスクリプトを実行します。
    - **on_restart**: postgres の再起動時に (ロールを変更せずに) このスクリプトを実行します。
    - **on_role_change**: postgres が昇格または降格されるときにこのスクリプトを実行します。
    - **on_start**: postgres の起動時にこのスクリプトを実行します。
    - **on_stop**: postgres が停止したときにこのスクリプトを実行します。

  - **connect_address**: IP アドレス + 他のノードおよびアプリケーションから Postgres にアクセスできるポート。

  - **proxy_address**: IP アドレス + Postgres の隣で実行されている接続プール (pgbouncer など) にアクセスできるポート。この値は、DCS のメンバー キーに `proxy_url` として書き込まれ、サービス検出に使用または役立つ可能性があります。

  - **create_replica_methods**: Patroni ノードを新しいレプリカに変換するための作成メソッドの順序付きリスト。 "basebackup" がデフォルトのメソッドです。他のメソッドはスクリプトを参照すると想定され、それぞれが独自の構成アイテムとして構成されます。詳細については、[カスタム レプリカの作成方法のドキュメント](/ja/docs/patroni/replica_bootstrap#custom_replica_creation) を参照してください。

  - **data_dir**: Postgres データ ディレクトリの場所。[既存の](/ja/docs/patroni/existing_data#existing_data)、または Patroni によって初期化されます。

  - **config_dir**: Postgres 構成ディレクトリの場所。デフォルトはデータ ディレクトリです。 Patroni によって書き込み可能である必要があります。

  - **bin_dir**: (オプション) PostgreSQL バイナリ (pg_ctl、initdb、pg_controldata、pg_basebackup、postgres、pg_isready、pg_rewind) へのパス。指定されない場合、または空の文字列の場合は、PATH 環境変数を使用して実行可能ファイルが検索されます。

  - **bin_name**: (オプション) カスタム Postgres ディストリビューションを使用している場合、Postgres バイナリ名をオーバーライドできるようにします。

    - **pg_ctl**: (オプション) `pg_ctl` バイナリのカスタム名。
    - **initdb**: (オプション) `initdb` バイナリのカスタム名。
    - **pgcontroldata**: (オプション) `pg_controldata` バイナリのカスタム名。
    - **pg_basebackup**: (オプション) `pg_basebackup` バイナリのカスタム名。
    - **postgres**: (オプション) `postgres` バイナリのカスタム名。
    - **pg_isready**: (オプション) `pg_isready` バイナリのカスタム名。
    - **pg_rewind**: (オプション) `pg_rewind` バイナリのカスタム名。

  - **listen**: Postgres がリッスンする IP アドレス + ポート。ストリーミング レプリケーションを使用している場合は、クラスター内の他のノードからアクセスできる必要があります。ポートコンポーネントが最後のアドレスの後ろにコロンで追加されている限り、カンマで区切られた複数のアドレスが許可されます (例: `listen: 127.0.0.1,127.0.0.2:5432`)。 Patroni は、このリストの最初のアドレスを使用して、PostgreSQL ノードへのローカル接続を確立します。

  - **use_unix_socket**: Patroni がクラスターへの接続に Unix ソケットの使用を優先することを指定します。デフォルト値は `false` です。 `unix_socket_directories` が定義されている場合、Patroni はその中の最初の適切な値を使用してクラスターに接続し、適切なものがない場合は tcp にフォールバックします。 `postgresql.parameters` で `unix_socket_directories` が指定されていない場合、Patroni はデフォルト値を使用する必要があると想定し、接続パラメーターから `host` を省略します。

  - **use_unix_socket_repl**: Patroni がレプリケーション ユーザー クラスター接続に UNIX ソケットの使用を優先することを指定します。デフォルト値は `false` です。 `unix_socket_directories` が定義されている場合、Patroni はその中の最初の適切な値を使用してクラスターに接続し、適切なものがない場合は tcp にフォールバックします。 `postgresql.parameters` で `unix_socket_directories` が指定されていない場合、Patroni はデフォルト値を使用する必要があると想定し、接続パラメーターから `host` を省略します。

  - **pgpass**: [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html) パスワード ファイルへのパス。 Patroni は、pg_basebackup、post_init スクリプトを実行する前、およびその他の状況下でこのファイルを作成します。この場所は Patroni によって書き込み可能である必要があります。

  - **recovery_conf**: フォロワーの構成時に recovery.conf に書き込まれる追加の構成設定。

  - **custom_conf** : `postgresql.base.conf` の代わりに使用される、オプションのカスタム `postgresql.conf` ファイルへのパス。ファイルはすべてのクラスター ノードに存在し、PostgreSQL によって読み取り可能であり、実際の `postgresql.conf` 上の場所からインクルードされる必要があります。 Patroni は、このファイルの変更を監視したり、バックアップしたりしないことに注意してください。ただし、その設定は Patroni 独自の構成機能によってオーバーライドできます。詳細については、[動的構成](/ja/docs/patroni/config#config) を参照してください。

  - **parameters**: `{ssl: "on", ssl_cert_file: "cert_file"}` 形式の Postgres の構成パラメーター (GUC)。
  - **parameters_primary**: (オプション) プライマリーのロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** とマージされ、上書きされます。
  - **parameters_replica**: (オプション) レプリカのロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** とマージされ、上書きされます。
  - **parameters_standby_leader**: (オプション)standby_leader のロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** とマージされ、上書きされます。

  - **pg_hba**: Patroni が `pg_hba.conf` を生成するために使用する行のリスト。 `hba_file` PostgreSQL パラメータがデフォルト以外の値に設定されている場合、Patroni はこのパラメータを無視します。このパラメータを [動的構成](/ja/docs/patroni/config/dynamic#dynamic) と組み合わせると、`pg_hba.conf` の管理が簡素化されます。

    - **- host すべて すべて 0.0.0.0/0 md5**
    - **- ホスト レプリケーション レプリケーター 127.0.0.1/32 md5**: レプリケーションには次のような行が必要です。
  - **pg_hba_primary**: (オプション) プライマリーのロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。
  - **pg_hba_replica**: (オプション) レプリカのロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。
  - **pg_hba_standby_leader**: (オプション)standby_leader のロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。

  - **pg_ident**: Patroni が `pg_ident.conf` を生成するために使用する行のリスト。 `ident_file` PostgreSQL パラメータがデフォルト以外の値に設定されている場合、Patroni はこのパラメータを無視します。このパラメータを [動的構成](/ja/docs/patroni/config/dynamic#dynamic) と組み合わせると、`pg_ident.conf` の管理が簡素化されます。

    - **- マップ名1 システム名1 pguser1**
    - **- マップ名1 システム名2 pguser2**
  - **pg_ident_primary**: (オプション) プライマリーのロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。
  - **pg_ident_replica**: (オプション) レプリカのロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。
  - **pg_ident_standby_leader**: (オプション)standby_leader のロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。

  - **pg_ctl_timeout**: `start`、`stop`、または `restart` を実行するときに pg_ctl が待機する時間。デフォルト値は 60 秒です。

  - **use_pg_rewind**: 前のリーダーがレプリカとしてクラスターに参加するときに、元のリーダーで pg_rewind を使用してみます。クラスターは `data page checksums` (`initdb` の `--data-checksums` オプション) で初期化するか、`wal_log_hints` を `on` に設定する必要があります。そうしないと、`pg_rewind` は機能しません。

  - **rewind**: (オプション) `pg_rewind` コマンドに渡すカスタム オプション。文字列のリストまたは単一のキーと値の辞書として指定できます。許可されないオプションには、`target-pgdata`、`source-pgdata`、`source-server`、`write-recovery-conf`、`dry-run`、`restore-target-wal`、`config-file`、`no-ensure-shutdown`、`version`、`help` があります。使用例:

    ```yaml
    postgresql:
      rewind:
        - debug
        - progress
        - sync-method: fsync
    ```

  - **remove_data_directory_on_rewind_failure**: このオプションが有効な場合、Patroni は PostgreSQL データ ディレクトリを削除し、レプリカを再作成します。そうでなければ、新しいリーダーに従おうとするでしょう。デフォルト値は **false** です。

  - **remove_data_directory_on_diverged_timelines**: Patroni は、タイムラインが分岐し、以前のプライマリーが新しいプライマリーからストリーミングを開始できないことを認識した場合、PostgreSQL データ ディレクトリを削除し、レプリカを再作成します。このオプションは、`pg_rewind` が使用できない場合に役立ちます。 PostgreSQL でタイムラインの相違チェックを実行している間、v10 および古い Patroni はレプリケーション資格情報を使用して "postgres" データベースに接続しようとします。したがって、そのようなアクセスは pg_hba.conf で許可される必要があります。デフォルト値は **false** です。

  - **replica_method**:basebackup 以外の create_replica_method ごとに、同じ名前の構成セクションを追加します。少なくとも、実行される実際のスクリプトへのフルパスを含む "command" を含める必要があります。他の構成パラメータは、「パラメータ=値」の形式でスクリプトに渡されます。

  - **pre_promote**: フェイルオーバー中にリーダー ロックを取得した後、レプリカを昇格する前に実行するフェンシング スクリプト。スクリプトがゼロ以外のコードで終了した場合、Patroni はレプリカを昇格させず、リーダー キーを DCS から削除します。

  - **before_stop**: postgres を停止する直前に実行されるスクリプト。コールバックとは対照的に、このスクリプトは同期的に実行され、完了するまでシャットダウンをブロックします。このスクリプトのリターン コードは、その後シャットダウンが続行されるかどうかには影響しません。

<a id="restapi_settings"></a>

--------

## REST API {#rest-api}

- **restapi**:
  - **thread_pool_size**: REST API リクエストを処理するために Patroni によって使用されるスレッド プールのサイズ。最小値は `5`、デフォルト値は `5` です。
  - **connect_address**: Patroni の [REST API](/ja/docs/patroni/rest_api#rest_api) にアクセスするための IP アドレス (またはホスト名) とポート。クラスターのすべてのメンバーがこのアドレスに接続できる必要があるため、Patroni セットアップがローカルホスト内のデモを目的としている場合を除き、このアドレスは非 "localhost" またはループバック アドレス (つまり、"localhost" または "127.0.0.1") である必要があります。これは、HTTP ヘルス チェック ("listen" REST API パラメーターについては以下を参照してください) のエンドポイントとして機能し、ユーザー クエリー (直接または REST API 経由) や、リーダーの選出中にクラスター メンバーによって実行されるヘルス チェック (たとえば、リーダーがまだ実行されているかどうか、またはエラーが発生したノードがあるかどうかを判断するため) のエンドポイントとしても機能します。クエリーを実行する位置よりも前の WAL 位置など) connect_address が DCS のメンバー キーに入れられ、メンバー名をアドレスに変換して REST API に接続できるようになります。
  - **listen**: Patroni が REST API をリッスンする IP アドレス (またはホスト名) とポート - 前述のように、参加ノード間で同じヘルス チェックとクラスター メッセージングも提供します。 HAProxy (または HTTP "OPTION" または "GET" チェックを実行できるその他のロード バランサー) のヘルスチェック情報を提供します。
  - **authentication**: (オプション)
    - **username**: 安全でない REST API エンドポイントを保護するための Basic 認証ユーザー名。
    - **password**: 安全でないREST APIエンドポイントを保護するBasic認証のパスワード。
  - **certfile**: （任意）PEM形式の証明書ファイルを指定します。certfileが未指定または空の場合、APIサーバーはSSLを使用せずに動作します。
  - **keyfile**: （任意）PEM形式の秘密鍵ファイルを指定します。
  - **keyfile_password**: （任意）keyfileを復号するパスワードを指定します。
  - **cafile**: （任意）クライアント証明書の検証に使用する、信頼されたCAの証明書を含むCA_BUNDLEファイルを指定します。
  - **ciphers**: （任意）許可する暗号スイートを指定します（例："ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1"）。
  - **verify_client**: （任意）`none`（デフォルト）、`optional`、`required`のいずれか。`none`の場合、REST APIはクライアント証明書を検証しません。`required`の場合、すべてのREST API呼び出しでクライアント証明書が必要です。`optional`の場合、安全でないすべてのREST APIエンドポイントでクライアント証明書が必要です。`required`では、証明書の署名検証に成功するとクライアント認証が成功します。`optional`では、`PUT`、`POST`、`PATCH`、`DELETE`の要求だけでクライアント証明書を検証します。
  - **allowlist**: （任意）安全でないREST APIエンドポイントを呼び出せるホストの集合を指定します。各要素にはホスト名、IPアドレス、CIDR表記のネットワークアドレスを使用できます。デフォルトは`allow all`です。`allowlist`または`allowlist_include_members`が設定されている場合、含まれないものはすべて拒否されます。
  - **allowlist_include_members**: （任意）`true`の場合、DCSに登録された他のクラスターメンバーから安全でないREST APIエンドポイントへのアクセスを許可します。IPアドレスまたはホスト名は、メンバーの`api_url`から取得します。OSが外向きの接続に異なるIPを使用する場合がある点に注意してください。
  - **http_extra_headers**: （任意）REST APIサーバーがHTTP応答に追加情報を含めるためのHTTPヘッダー。
  - **https_extra_headers**: （任意）TLSが有効な場合に、REST APIサーバーがHTTP応答に追加情報を含めるためのHTTPSヘッダー。`http_extra_headers`に設定した追加情報も含まれます。
  - **request_queue_size**: （任意）Patroni REST APIが使用するTCPソケットの要求キューサイズを設定します。キューが満杯になると、それ以降の要求は「Connection denied」エラーになります。デフォルトは5です。
  - **server_tokens**: （任意）HTTPの`Server`ヘッダーの値を設定します。
    - `Minimal`: ヘッダーには Patroni バージョンのみが含まれます。 `Patroni/4.0.0`。
    - `ProductOnly`: ヘッダーには製品名のみが含まれます。 `Patroni`。
    - `Original` (デフォルト): ヘッダーは元の動作を公開し、BaseHTTP および Python のバージョンを表示します。 `BaseHTTP/0.6 Python/3.12.3`。

次に、**http_extra_headers** と **https_extra_headers** の両方の例を示します。

```yaml
restapi:
  listen: <listen>
  connect_address: <connect_address>
  authentication:
    username: <username>
    password: <password>
  http_extra_headers:
    'X-Frame-Options': 'SAMEORIGIN'
    'X-XSS-Protection': '1; mode=block'
    'X-Content-Type-Options': 'nosniff'
  cafile: <ca file>
  certfile: <cert>
  keyfile: <key>
  https_extra_headers:
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
```

<div class="warning">

<div class="title">

警告

</div>

- `restapi.connect_address` は、特定の Patroni クラスターのすべてのノードからアクセス可能である必要があります。内部的には、Patroni がリーダー レース中にこれを使用して、レプリケーション ラグが最小限のノードを見つけます。
- クライアント証明書の検証を有効にした場合 (`restapi.verify_client` が `required` に設定されている場合)、**しなければならない** は `ctl.certfile`、`ctl.keyfile`、`ctl.keyfile_password` で **有効なクライアント証明書** も提供します。指定しない場合、Patroni は正しく動作しません。

</div>

<a id="patronictl_settings"></a>

--------

## CTL {#ctl}

- **ctl**: (オプション)
  - **authentication**:
    - **username**: 保護された REST API エンドポイントにアクセスするための基本認証ユーザー名。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "username" パラメーターに指定された値を使用します。
    - **password**: 保護された REST API エンドポイントにアクセスするための基本認証パスワード。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "password" パラメーターに指定された値を使用します。
  - **insecure**: SSL 証明書を検証せずに、REST API への接続を許可します。
  - **cacert**: REST API SSL 証明書の検証中に使用する、CA_BUNDLE ファイルまたはディレクトリを含む信頼できる CA の証明書を含むファイルを指定します。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "cafile" パラメーターに指定された値を使用します。
  - **certfile**: クライアント証明書を含むファイルを PEM 形式で指定します。
  - **keyfile**: クライアント秘密鍵を含むファイルを PEM 形式で指定します。
  - **keyfile_password**: クライアントのキーファイルを復号化するためのパスワードを指定します。

--------

## ウォッチドッグ {#watchdog}

- **mode**: `off`、`automatic`、または `required`。 `off` ウォッチドッグが無効になっている場合。 `automatic` の場合、ウォッチドッグが使用可能な場合は使用されますが、使用できない場合は無視されます。 `required` の場合、ウォッチドッグを正常に有効にできない限り、ノードはリーダーになりません。
- **device**: ウォッチドッグ デバイスへのパス。デフォルトは `/dev/watchdog` です。
- **safety_margin**: ウォッチドッグのトリガーとリーダー キーの有効期限の間の安全マージンの秒数。

<a id="tags_settings"></a>

--------

## タグ {#tags}

- **clonefrom**: `true` または `false`。 `true` に設定すると、他のノードはブートストラップにこのノードの使用を優先する可能性があります (`pg_basebackup` から取得します)。 `clonefrom` タグが `true` に設定されているノードが複数ある場合、ブートストラップ元のノードがランダムに選択されます。デフォルト値は `false` です。
- **noloadbalance**: `true` または `false`。 `true` に設定すると、ノードは `GET /replica` REST API ヘルスチェックに対して HTTP ステータス コード 503 を返すため、ロード バランシングから除外されます。デフォルトは `false` です。
- **replicatefrom**: 複製元の別のレプリカの名前。カスケード レプリケーションをサポートするために使用されます。
- **nosync**: `true` または `false`。 `true` に設定すると、ノードは同期レプリカとして選択されなくなります。
- **sync_priority**: 整数。[synchronous_mode](/ja/docs/patroni/replication_modes#synchronous_mode) が `on` に設定されている場合に、同期レプリカの選択中にこのノードが持つべき優先順位を制御します。優先順位の高いノードは、優先順位の低いノードよりも優先されます。 `sync_priority` が 0 または負の場合、そのようなノードは `synchronous_standby_names` PostgreSQL パラメーターに書き込むことができません (`nosync: true` と同様)。このパラメータは、`pg_stat_replication` ビューで報告される `sync_priority` 値とは逆の意味をもつことに注意してください。
- **nofailover**: `true` または `false` は、このノードがリーダー レースに参加してリーダーになることを許可するかどうかを制御します。デフォルトは `false` で、このノード <span id="can">can</span>\_ がリーダー レースに参加できることを意味します。
- **failover_priority**: 整数。フェイルオーバー中にこのノードが持つべき優先順位を制御します。同じ量の WAL を受信/再生した場合、優先順位の高いノードが優先順位の低いノードよりも優先されます。ただし、優先度に関係なく、受信/再生 LSN の値が高いノードが優先されます。 `failover_priority` が 0 または負の場合、そのようなノードはリーダー レースに参加したり、リーダーになることは許可されません (`nofailover: true` と同様)。既知の制限: `failover_priority` は現在、[クォーラムベースの同期レプリケーション](/ja/docs/patroni/replication_modes#quorum_mode) では動作しません。
- **nostream**: `true` または `false`。 `true` に設定すると、ノードは WAL をストリーミングするためにレプリケーション プロトコルを使用しません。代わりに、アーカイブのリカバリ (`restore_command` が構成されている場合) と `pg_wal`/`pg_xlog` ポーリングに依存します。また、ノード自体とそのすべてのカスケード レプリカ上の永続的な論理レプリケーション スロットのコピーと同期も無効になります。このタグをプライマリー ノードに設定しても効果はありません。

> [!WARNING]
> `nofailover` または `failover_priority` のいずれか 1 つだけを指定します。 `nofailover: true` を指定することは `failover_priority: 0` と同じであり、`nofailover: false` を指定するとノードの優先順位 1 が与えられます。

これらの定義済みタグに加えて、独自のタグを追加することもできます。

- **key1**: `true`
- **key2**: `false`
- **key3**: `1.4`
- **key4**: `"RandomString"`

タグは [REST API](/ja/docs/patroni/rest_api#rest_api) および [patronictl_list](/ja/docs/patroni/patronictl#patronictl_list) で表示されます。これらのタグを使用してインスタンスの健全性を確認することもできます。タグがインスタンスに定義されていない場合、またはそれぞれの値がクエリー値と一致しない場合は、HTTP ステータス コード 503 が返されます。
