---
title: "環境構成の設定"
linkTitle: "環境設定"
weight: 30
icon: fa-solid fa-sliders
description: "Patroni 構成パラメーターをオーバーライドするための環境変数。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/patroni/config/env/]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
システム環境変数を使用して、Patroni 構成ファイルで定義されている構成パラメーターの一部をオーバーライドすることができます。このドキュメントには、Patroni によって処理されるすべての環境変数がリストされています。これらの変数を介して設定された値は、Patroni 構成ファイルで設定された値よりも常に優先されます。

--------

## グローバル/ユニバーサル {#globaluniversal}

- **PATRONI_CONFIGURATION**: [PATRONI_CONFIGURATION](/ja/docs/patroni/config#config) 環境変数を介して Patroni の構成全体を設定できます。この場合、他の環境変数は一切考慮されません!
- **PATRONI_THREAD_POOL_SIZE**: リーダー競合またはフェールセーフ チェック中に、非同期タスクを実行し、REST API を介して他のメンバーと通信するために Patroni によって使用されるスレッド プールのサイズ。最小値は `5`、デフォルト値は `5` です。
- **PATRONI_THREAD_STACK_SIZE**: Patroni によって開始されるスレッドに使用されるスタック サイズを指定します。値は `64kB` によってアライメントされる必要があります。最小値は `64kB` 、デフォルト値 (Patroni によって設定) は `512kB` です。
- **PATRONI_NAME**: Patroni の現在のインスタンスが実行されているノードの名前。クラスター内で一意である必要があります。
- **PATRONI_NAMESPACE**: Patroni がクラスターに関する情報を保持する構成ストア内のパス。デフォルト値: 「/service」
- **PATRONI_SCOPE**: クラスター名
- **PG_MALLOC_ARENA_MAX**: `postmaster` プロセスの `MALLOC_ARENA_MAX` 環境変数のカスタム値。設定されていない場合、`postmaster` は `MALLOC_ARENA_MAX` 値を継承します。

--------

## ログ {#log}

- **PATRONI_LOG_TYPE**: ログの形式を設定します。 **plain** または **json** のいずれかになります。 **json** 形式を使用するには、[jsonlogger](/ja/docs/patroni/installation#extras) がインストールされている必要があります。デフォルト値は **plain** です。
- **PATRONI_LOG_LEVEL**: 一般的なログ レベルを設定します。デフォルト値は **INFO** です ([Python ロギングのドキュメント](https://docs.python.org/3.6/library/logging.html#levels) を参照)
- **PATRONI_LOG_TRACEBACK_LEVEL**: トレースバックが表示されるレベルを設定します。デフォルト値は **ERROR** です。**PATRONI_LOG_LEVEL=DEBUG** を有効にした場合にのみトレースバックを表示したい場合は、**DEBUG** に設定します。
- **PATRONI_LOG_FORMAT**: ログのフォーマット文字列を設定します。ログ タイプが **plain** の場合、ログ形式は文字列で指定することを推奨します。使用可能な属性については、[LogRecord 属性](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) を参照してください。ログ タイプが **json** の場合、ログ形式は文字列に加えてリストにすることもできます。各リスト項目は LogRecord 属性に対応させることを推奨します。フィールド名のみが必要であり、**%(** と **)** は省略する必要があることに注意してください。別のキー名でログ フィールドを出力する場合は、辞書キーがログ フィールドで、値がログに出力するフィールドの名前である辞書を使用します。デフォルト値は **%(asctime)s %(levelname)s: %(message)s** です。
- **PATRONI_LOG_DATEFORMAT**: 日時フォーマット文字列を設定します。 ([formatTime() ドキュメント](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime) を参照)
- **PATRONI_LOG_STATIC_FIELDS**: ログに追加のフィールドを付加します。このオプションは、ログタイプが **json** に設定されている場合にのみ使用できます。例 `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE**: Patroni は 2 段階のロギングを使用しています。ログ レコードはメモリ内のキューに書き込まれ、キューからログ レコードを取得して stderr またはファイルに書き込む別のスレッドがあります。内部キューの最大サイズはデフォルトで **1000** レコードによって制限されており、過去 1 時間 20 分までのログを保持するには十分なサイズです。
- **PATRONI_LOG_DIR**: アプリケーションログを書き込むディレクトリ。ディレクトリは存在し、Patroni を実行するユーザーによる書き込みが可能である必要があります。この環境変数を設定すると、アプリケーションはデフォルトで 25MB のログを 4 つ保持します。これらの保持値は、`PATRONI_LOG_FILE_NUM` と `PATRONI_LOG_FILE_SIZE` で調整できます (以下を参照)。
- **PATRONI_LOG_MODE**: ログ ファイルのアクセス許可 (`0644` など)。指定しない場合、権限は現在の umask 値に基づいて設定されます。
- **PATRONI_LOG_FILE_NUM**: 保持するアプリケーション ログの数。
- **PATRONI_LOG_FILE_SIZE**: ログ ローリングをトリガーする patroni.log ファイルのサイズ (バイト単位)。
- **PATRONI_LOG_LOGGERS**: Python モジュールごとにログ レベルを再定義します。例 `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS**: `true` に設定すると、同一のハートビートログが連続して出力されなくなります。デフォルト値は `false` です。

> [!WARNING]
> HA ループの実行時間は、リソースの枯渇や同様の問題によるフェイルオーバーを診断する際に非常に貴重な情報となる可能性があります。 `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` が `true` に設定されている場合、(リーダーが変更されない限り) HA ループ実行のログは生成されないため、この潜在的に役立つ情報はログから取得できません。

--------

## Citus {#citus}

Patroni と [Citus](https://docs.citusdata.com) の統合を有効にします。構成されている場合、Patroni はコーディネーター上での Citus ワーカーノードの登録を管理します。Citus サポートの詳細については、[こちら](/ja/docs/patroni/citus#citus) を参照してください。

- **PATRONI_CITUS_GROUP**: Citus グループ ID、整数。コーディネーターには `0` を使用し、ワーカーには `1`、`2` などを使用します。
- **PATRONI_CITUS_DATABASE**: [citus](/ja/docs/patroni/citus#citus) 拡張を作成するデータベース。コーディネーターとすべてのワーカーで同じである必要があります。現在サポートされているデータベースは 1 つだけです。

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST**: Consul ローカル エージェントのホスト:ポート。
- **PATRONI_CONSUL_URL**: Consul ローカル エージェントの URL (形式: http(s)://host:port)
- **PATRONI_CONSUL_PORT**: (オプション) Consul ポート
- **PATRONI_CONSUL_SCHEME**: (オプション) **http** または **https**、デフォルトは **http**
- **PATRONI_CONSUL_TOKEN**: (オプション) ACL トークン
- **PATRONI_CONSUL_VERIFY**: (オプション) HTTPS リクエストの SSL 証明書を検証するかどうか
- **PATRONI_CONSUL_CACERT**: (オプション) CA 証明書。存在する場合、検証が有効になります。
- **PATRONI_CONSUL_CERT**: (オプション) クライアント証明書を含むファイル
- **PATRONI_CONSUL_KEY**: (オプション) クライアント キーを含むファイル。キーが証明書の一部である場合は空にすることができます。
- **PATRONI_CONSUL_DC**: (オプション) 通信するデータセンター。デフォルトでは、ホストのデータセンターが使用されます。
- **PATRONI_CONSUL_CONSISTENCY**: (オプション) Consul の整合性モードを選択します。可能な値は `default`、`consistent`、または `stale` です (詳細については [Consul API リファレンス](https://www.consul.io/api/features/consistency.html/) を参照)
- **PATRONI_CONSUL_CHECKS**: (オプション) セッションに使用される Consul ヘルス チェックのリスト。デフォルトでは、空のリストが使用されます。
- **PATRONI_CONSUL_REGISTER_SERVICE**: (オプション) スコープパラメーターで定義された名前と、ノードのロールに応じた master、primary、replica、standby-leader のタグを持つサービスを登録するかどうか。デフォルトは **false** です
- **PATRONI_CONSUL_SERVICE_TAGS**: (オプション) ロール (`primary`/`replica`/`standby-leader`) とは別に Consul サービスに追加する追加の静的タグ。デフォルトでは、空のリストが使用されます。
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL**: (オプション) 登録された URL に対してヘルスチェックを実行する頻度
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME**: (オプション) TLS 経由で接続するときに SNI ホストをオーバーライドします。[Consul エージェントチェック API リファレンス](https://www.consul.io/api-docs/agent/check#tlsservername) も参照してください。

--------

## Etcd {#etcd}

- **PATRONI_ETCD_PROXY**: etcd のプロキシ URL。プロキシを使用して etcd に接続している場合は、**PATRONI_ETCD_URL** の代わりにこのパラメータを使用します。
- **PATRONI_ETCD_URL**: etcd の URL、形式: http(s)://(username:password@)host:port
- **PATRONI_ETCD_HOSTS**: 'host1:port1'、'host2:port2' などの形式の etcd エンドポイントのリスト
- **PATRONI_ETCD_USE_PROXIES**: このパラメーターが true に設定されている場合、Patroni は **hosts** をプロキシのリストとして考慮し、etcd クラスターのトポロジ検出を実行せず、**hosts** の固定リストに固執します。
- **PATRONI_ETCD_PROTOCOL**: http または https (指定しない場合は http が使用されます)。 **url** または **proxy** が指定されている場合は、それらからプロトコルを取得します。
- **PATRONI_ETCD_HOST**: etcd エンドポイントのホスト:ポート。
- **PATRONI_ETCD_SRV**: クラスター自動検出のために SRV レコードを検索するドメイン。 Patroni は、指定されたドメインの SRV サービス名 (最初に成功するまでこの順序で) のクエリーを試行します: `_etcd-client-ssl`、`_etcd-client`、`_etcd-ssl`、`_etcd`、`_etcd-server-ssl`、`_etcd-server`。 `_etcd-server-ssl` または `_etcd-server` の SRV レコードが取得された場合、ETCD ピア プロトコルが使用され、利用可能なメンバーについて ETCD がクエリーされます。それ以外の場合は、SRV レコードのホストが使用されます。
- **PATRONI_ETCD_SRV_SUFFIX**: 検出中にクエリーされる SRV 名のサフィックスを構成します。このフラグを使用して、同じドメイン内の複数の etcd クラスターを区別します。 **PATRONI_ETCD_SRV** と組み合わせた場合にのみ機能します。たとえば、`PATRONI_ETCD_SRV_SUFFIX=foo` と `PATRONI_ETCD_SRV=example.org` が設定されている場合、DNS SRV クエリーが作成されます:`_etcd-client-ssl-foo._tcp.example.org` (考えられるすべての ETCD SRV サービス名に対して同様)。
- **PATRONI_ETCD_USERNAME**: etcd 認証用のユーザー名。
- **PATRONI_ETCD_PASSWORD**: etcd 認証用のパスワード。
- **PATRONI_ETCD_CACERT**: CA 証明書。存在する場合、検証が有効になります。
- **PATRONI_ETCD_CERT**: クライアント証明書を含むファイル。
- **PATRONI_ETCD_KEY**: クライアント キーを含むファイル。キーが証明書の一部である場合は空にすることができます。

--------

## Etcdv3 {#etcdv3}

Etcdv3 の環境名は etcd の場合と似ており、変数名に `ETCD` の代わりに `ETCD3` を使用する必要があるだけです。例: `PATRONI_ETCD3_HOST`、`PATRONI_ETCD3_CACERT` など。

> [!WARNING]
> プロトコル バージョン 2 で作成されたキーは、プロトコル バージョン 3 では表示されず、その逆も同様であるため、Patroni 構成を更新するだけでは etcd から Etcdv3 に切り替えることはできません。さらに、Patroni は etcd の gRPC ゲートウェイ (プロキシ) を使用して V3 API と通信します。これは、TLS 共通名認証が不可能であることを意味します。

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS**: ZooKeeper クラスター メンバーのカンマ区切りリスト: "'host1:port1','host2:port2','etc...'"。各要素を引用符で囲むことが重要です。
- **PATRONI_ZOOKEEPER_USE_SSL**: (オプション) SSL が使用されているかどうか。デフォルトは `false` です。 `false` に設定すると、SSL 固有のパラメーターはすべて無視されます。
- **PATRONI_ZOOKEEPER_CACERT**: (オプション) CA 証明書。存在する場合、検証が有効になります。
- **PATRONI_ZOOKEEPER_CERT**: (オプション) クライアント証明書を含むファイル。
- **PATRONI_ZOOKEEPER_KEY**: (オプション) クライアント キーを含むファイル。
- **PATRONI_ZOOKEEPER_KEY_PASSWORD**: (オプション) クライアント キーのパスワード。
- **PATRONI_ZOOKEEPER_VERIFY**: (オプション) 証明書を検証するかどうか。デフォルトは `true` です。
- **PATRONI_ZOOKEEPER_SET_ACLS**: (オプション) 設定した場合、作成する各 ZNode にデフォルトの ACL を適用するように Kazoo を構成します。 ACL では、`x509` スキーマ (デフォルト)、または `digest` などの他のサポートされている ZooKeeper スキーマのいずれかを使用できます。これらは、キーが完全なプリンシパル (オプションでスキームの接頭辞が付けられる) であり、値がアクセス許可のリストであるディクショナリとして指定する必要があります。権限は、`CREATE`、`READ`、`WRITE`、`DELETE`、`ADMIN`、または `ALL` の 1 つ以上です。たとえば、`set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}` です。
- **PATRONI_ZOOKEEPER_AUTH_DATA**: (オプション) 接続に使用する認証資格情報。 `scheme` がキー、`credential` が値という形式の辞書である必要があります。デフォルトは空の辞書です。

> [!NOTE]
> SSL をサポートするには、`kazoo>=2.6.0` をインストールする必要があります。

--------

## Exhibitor {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS**: Exhibitor (ZooKeeper) ノードの初期リスト (形式: 'host1,host2,etc...')。このリストは、Exhibitor (ZooKeeper) クラスターのトポロジーが変更されるたびに自動的に更新されます。
- **PATRONI_EXHIBITOR_PORT**: Exhibitor ポート。

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE**: (オプション) Kubernetes API と通信する場合、Patroni は通常 [Kubernetes](/ja/docs/patroni/kubernetes#kubernetes) サービスに依存し、そのアドレスは `KUBERNETES_SERVICE_HOST` 環境変数を介してポッド内で公開されます。 `PATRONI_KUBERNETES_BYPASS_API_SERVICE` が `true` に設定されている場合、Patroni はサービスの背後にある API ノードのリストを解決し、それらのノードに直接接続します。
- **PATRONI_KUBERNETES_NAMESPACE**: (オプション) Patroni ポッドが実行されている Kubernetes 名前空間。デフォルト値は `default` です。
- **PATRONI_KUBERNETES_LABELS**: `{label1: value1, label2: value2}` 形式のラベル。これらのラベルは、現在のクラスターに関連付けられている既存のオブジェクト (ポッドとエンドポイントまたは ConfigMaps) を検索するために使用されます。また、Patroni は、作成するすべてのオブジェクト (エンドポイントまたは ConfigMap) にそれらを設定します。
- **PATRONI_KUBERNETES_SCOPE_LABEL**: (オプション) クラスター名を含むラベルの名前。デフォルト値は `cluster-name` です。
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS**: (オプション) `{label1: value1, label2: value2}` 形式のラベル。これらのラベルは、Patroni ポッドの状態が `initializing new cluster`、`running custom bootstrap script`、`starting after custom bootstrap`、または `creating replica` のいずれかである場合にそのポッドに割り当てられます。
- **PATRONI_KUBERNETES_ROLE_LABEL**: (オプション) ロールを含むラベルの名前 (`primary`、`replica`、またはその他のカスタム値)。 Patroni は、実行されるポッドにこのラベルを設定します。デフォルト値は `role` です。
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE**: (オプション) Postgres ロールが `primary` の場合のポッド ラベルの値。デフォルト値は `primary` です。
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE**: (オプション) Postgres ロールが `replica` の場合のポッド ラベルの値。デフォルト値は `replica` です。
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE**: (オプション) Postgres ロールが `standby_leader` の場合のポッド ラベルの値。デフォルト値は `primary` です。
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL**: (オプション) ロールを含む一時ラベルの名前 (`primary` または `replica`)。このラベルの値には、対応するロールのデフォルトが常に使用されます。必要な場合のみ設定してください。
- **PATRONI_KUBERNETES_USE_ENDPOINTS**: (オプション) true に設定すると、Patroni は ConfigMaps の代わりにエンドポイントを使用してリーダーの選出を実行し、クラスターの状態を維持します。
- **PATRONI_KUBERNETES_POD_IP**: (オプション) Patroni が実行されているポッドの IP アドレス。 この値は `PATRONI_KUBERNETES_USE_ENDPOINTS` が有効な場合に必須であり、ポッドの PostgreSQL が昇格されるときにリーダー エンドポイント サブセットを設定するために使用されます。
- **PATRONI_KUBERNETES_PORTS**: (オプション) Service オブジェクトにポートの名前がある場合、同じ名前が Endpoint オブジェクトに表示される必要があります。そうでない場合、サービスは機能しません。たとえば、サービスが `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}` として定義されている場合、`PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'` を設定する必要があります。これにより、Patroni はリーダー エンドポイントのサブセットの更新にそれを使用します。このパラメータは、`PATRONI_KUBERNETES_USE_ENDPOINTS` が設定されている場合にのみ使用されます。
- **PATRONI_KUBERNETES_CACERT**: (オプション) Kubernetes API SSL 証明書の検証中に使用する、信頼できる CA の証明書を含む CA_BUNDLE ファイルを指定します。指定されない場合、Patroni は ServiceAccount シークレットによって提供される値を使用します。
- **PATRONI_RETRIABLE_HTTP_CODES**: (オプション) 再試行する K8s API からの HTTP ステータス コードのリスト。デフォルトでは、Patroni は、`500`、`503`、および `504`、または K8s API 応答に `retry-after` HTTP ヘッダーがある場合に再試行します。

--------

## Raft (非推奨) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR**: Raft 接続をリッスンする `ip:port`。 `self_addr` はクラスターの他のノードからアクセスできる必要があります。設定されていない場合、ノードはコンセンサスに参加しません。
- **PATRONI_RAFT_BIND_ADDR**: (オプション) Raft 接続をリッスンする `ip:port`。指定しない場合は、`self_addr` が使用されます。
- **PATRONI_RAFT_PARTNER_ADDRS**: `"'ip1:port1','ip2:port2'"` 形式のクラスター内の他の Patroni ノードのリスト。各要素を引用符で囲むことが重要です。
- **PATRONI_RAFT_DATA_DIR**: Raft ログとスナップショットを保存するディレクトリ。指定しない場合は、現在の作業ディレクトリが使用されます。
- **PATRONI_RAFT_PASSWORD**: (オプション) 指定されたパスワードで Raft トラフィックを暗号化します。`cryptography` Python モジュールが必要です。
- **PATRONI_RAFT_MIN_TIMEOUT**: (オプション) 基礎となる pysyncobj Raft 実装の最小選出タイムアウト (秒単位)。 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD` より大きくなければなりません。デフォルト： `0.4`。
- **PATRONI_RAFT_MAX_TIMEOUT**: (オプション) 基礎となる pysyncobj Raft 実装の最大選出タイムアウト (秒単位)。 `PATRONI_RAFT_MIN_TIMEOUT` より大きくなければなりません。デフォルト： `1.4`。
- **PATRONI_RAFT_CONNECTION_TIMEOUT**: (オプション) データを受信しなかった接続が切断されたとみなされるまでの秒数。 `PATRONI_RAFT_MAX_TIMEOUT` 以上である必要があります。デフォルト： `3.5`。
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD**: (オプション) ハートビート コマンドを送信する間隔 (秒単位)。 `PATRONI_RAFT_MIN_TIMEOUT` の 3 分の 1 未満である必要があります。デフォルト： `0.1`。
- **PATRONI_RAFT_CONNECTION_RETRY_TIME**: (オプション) オフライン ノードへの再接続試行間の秒単位の間隔。デフォルト： `5.0`。
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT**: (オプション) 過半数からの応答がないリーダーがフォロワー状態に戻るまでの秒数。 `PATRONI_RAFT_APPEND_ENTRIES_PERIOD` より大きくなければなりません。デフォルト： `30.0`。

> [!NOTE]
> Patroni は起動時にこれらの制約を検証し、違反している場合は起動を拒否します。これらの値は実行時に変更できないため、再起動が必要です。高遅延の制限などの詳細については、[Raft 設定](/ja/docs/patroni/config/yaml#raft_settings) を参照してください。

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN**: Postgres がリッスンする IP アドレス + ポート。ポートコンポーネントが最後のアドレスの後ろにコロンで追加されている限り、カンマで区切られた複数のアドレスが許可されます (例: `listen: 127.0.0.1,127.0.0.2:5432`)。 Patroni は、このリストの最初のアドレスを使用して、PostgreSQL ノードへのローカル接続を確立します。
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS**: IP アドレス + 他のノードおよびアプリケーションから Postgres にアクセスできるポート。
- **PATRONI_POSTGRESQL_PROXY_ADDRESS**: IP アドレス + Postgres の隣で実行されている接続プール (pgbouncer など) にアクセスできるポート。この値は、DCS のメンバー キーに `proxy_url` として書き込まれ、サービス検出に使用または役立つ可能性があります。
- **PATRONI_POSTGRESQL_DATA_DIR**: Postgres データ ディレクトリの場所。既存であるか、Patroni によって初期化されます。
- **PATRONI_POSTGRESQL_CONFIG_DIR**: Postgres 構成ディレクトリの場所。デフォルトはデータ ディレクトリです。 Patroni によって書き込み可能である必要があります。
- **PATRONI_POSTGRESQL_BIN_DIR**: PostgreSQL バイナリへのパス。 (pg_ctl、initdb、pg_controldata、pg_basebackup、postgres、pg_isready、pg_rewind) デフォルト値は空の文字列で、PATH 環境変数が実行可能ファイルの検索に使用されることを意味します。
- **PATRONI_POSTGRESQL_BIN_PG_CTL**: (オプション) `pg_ctl` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_INITDB**: (オプション) `initdb` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA**: (オプション) `pg_controldata` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP**: (オプション) `pg_basebackup` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_POSTGRES**: (オプション) `postgres` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_IS_READY**: (オプション) `pg_isready` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_BIN_PG_REWIND**: (オプション) `pg_rewind` バイナリのカスタム名。
- **PATRONI_POSTGRESQL_PGPASS**: [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html) パスワード ファイルへのパス。 Patroni は、pg_basebackup を実行する前および他の状況下でこのファイルを作成します。この場所は Patroni によって書き込み可能である必要があります。
- **PATRONI_REPLICATION_USERNAME**: レプリケーション ユーザー名。ユーザーは初期化中に作成されます。レプリカはこのユーザーを使用して、ストリーミング レプリケーション経由でレプリケーション ソースにアクセスします。
- **PATRONI_REPLICATION_PASSWORD**: レプリケーションのパスワード。ユーザーは初期化中に作成されます。
- **PATRONI_REPLICATION_SSLMODE**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
- **PATRONI_REPLICATION_SSLKEY**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
- **PATRONI_REPLICATION_SSLPASSWORD**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`PATRONI_REPLICATION_SSLKEY`で指定した秘密鍵のパスワードを指定します。
- **PATRONI_REPLICATION_SSLCERT**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
- **PATRONI_REPLICATION_SSLROOTCERT**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
- **PATRONI_REPLICATION_SSLCRL**: (オプション) [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) 接続パラメーターにマップされ、証明書失効リストを含むファイルの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_REPLICATION_SSLCRLDIR**: (オプション) [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) 接続パラメーターにマップされ、証明書失効リストを含むファイルが格納されたディレクトリの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_REPLICATION_SSLNEGOTIATION**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
- **PATRONI_REPLICATION_GSSENCMODE**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
- **PATRONI_REPLICATION_CHANNEL_BINDING**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメーターにマップされ、クライアントによるチャネル バインディングの使用を制御します。
- **PATRONI_SUPERUSER_USERNAME**: スーパーユーザーの名前。初期化 (initdb) 中に設定され、後で postgres に接続するために Patroni によって使用されます。また、このユーザーは pg_rewind によって使用されます。
- **PATRONI_SUPERUSER_PASSWORD**: スーパーユーザーのパスワード。初期化 (initdb) 中に設定されます。
- **PATRONI_SUPERUSER_SSLMODE**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
- **PATRONI_SUPERUSER_SSLKEY**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
- **PATRONI_SUPERUSER_SSLPASSWORD**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`PATRONI_SUPERUSER_SSLKEY`で指定した秘密鍵のパスワードを指定します。
- **PATRONI_SUPERUSER_SSLCERT**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
- **PATRONI_SUPERUSER_SSLROOTCERT**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
- **PATRONI_SUPERUSER_SSLCRL**: (オプション) [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) 接続パラメーターにマップされ、証明書失効リストを含むファイルの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_SUPERUSER_SSLCRLDIR**: (オプション) [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) 接続パラメーターにマップされ、証明書失効リストを含むファイルが格納されたディレクトリの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_SUPERUSER_SSLNEGOTIATION**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
- **PATRONI_SUPERUSER_GSSENCMODE**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
- **PATRONI_SUPERUSER_CHANNEL_BINDING**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメーターにマップされ、クライアントによるチャネル バインディングの使用を制御します。
- **PATRONI_REWIND_USERNAME**: (オプション) `pg_rewind` のユーザーの名前。ユーザーは postgres 11+ の初期化中に作成され、必要なすべての [権限](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) が付与されます。
- **PATRONI_REWIND_PASSWORD**: (オプション) `pg_rewind` のユーザーのパスワード。ユーザーは初期化中に作成されます。
- **PATRONI_REWIND_SSLMODE**: (オプション) [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) 接続パラメータにマップします。これにより、クライアントはサーバーとの TLS ネゴシエーション モードのタイプを指定できます。各モードの動作の詳細については、[PostgreSQL ドキュメント](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS) を参照してください。デフォルトのモードは `prefer` です。
- **PATRONI_REWIND_SSLKEY**: (オプション) [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) 接続パラメータにマップします。これは、クライアントの証明書で使用される秘密キーの場所を指定します。
- **PATRONI_REWIND_SSLPASSWORD**: （任意）[sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)接続パラメーターに対応し、`PATRONI_REWIND_SSLKEY`で指定した秘密鍵のパスワードを指定します。
- **PATRONI_REWIND_SSLCERT**: (オプション) [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) 接続パラメータにマップされ、クライアント証明書の場所を指定します。
- **PATRONI_REWIND_SSLROOTCERT**: （任意）[sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)接続パラメーターに対応します。クライアントがサーバー証明書の検証に使用する、1つ以上の認証局（CA）の証明書を含むファイルの場所を指定します。
- **PATRONI_REWIND_SSLCRL**: (オプション) [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) 接続パラメーターにマップされ、証明書失効リストを含むファイルの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_REWIND_SSLCRLDIR**: (オプション) [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR) 接続パラメーターにマップされ、証明書失効リストを含むファイルが格納されたディレクトリの場所を指定します。クライアントは、このリストに存在する証明書を持つサーバーへの接続を拒否します。
- **PATRONI_REWIND_SSLNEGOTIATION**: （任意）[sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)接続パラメーターに対応し、SSLを使用する場合に、サーバーとのSSL暗号化のネゴシエーション方法を制御します。
- **PATRONI_REWIND_GSSENCMODE**: （任意）[gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)接続パラメーターに対応します。サーバーと安全なGSS TCP/IP接続をネゴシエートするかどうか、またその優先順位を決定します。
- **PATRONI_REWIND_CHANNEL_BINDING**: (オプション) [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING) 接続パラメーターにマップされ、クライアントによるチャネル バインディングの使用を制御します。

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE**: REST API リクエストを処理するために Patroni によって使用されるスレッド プールのサイズ。最小値は `5`、デフォルト値は `5` です。
- **PATRONI_RESTAPI_CONNECT_ADDRESS**: REST API にアクセスするための IP アドレスとポート。
- **PATRONI_RESTAPI_LISTEN**: HAProxy のヘルスチェック情報を提供するために、Patroni がリッスンする IP アドレスとポート。
- **PATRONI_RESTAPI_USERNAME**: 安全でない REST API エンドポイントを保護するための Basic 認証ユーザー名。
- **PATRONI_RESTAPI_PASSWORD**: 安全でない REST API エンドポイントを保護するための Basic 認証パスワード。
- **PATRONI_RESTAPI_CERTFILE**: PEM 形式の証明書を含むファイルを指定します。 certfile が指定されていないか空のままの場合、API サーバーは SSL を使用せずに動作します。
- **PATRONI_RESTAPI_KEYFILE**: 秘密鍵を含むファイルを PEM 形式で指定します。
- **PATRONI_RESTAPI_KEYFILE_PASSWORD**: キーファイルを復号化するためのパスワードを指定します。
- **PATRONI_RESTAPI_CAFILE**: クライアント証明書の検証中に使用する、信頼できる CA の証明書を含むファイルを CA_BUNDLE で指定します。
- **PATRONI_RESTAPI_CIPHERS**: （任意）許可する暗号スイートを指定します（例："ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1"）。
- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (デフォルト)、`optional`、または `required`。`none` の場合、REST API はクライアント証明書をチェックしません。`required` の場合、すべての REST API 呼び出しにクライアント証明書が必要です。`optional` の場合、すべての安全でない REST API エンドポイントにクライアント証明書が必要です。`required` が使用されている場合、証明書の署名の検証が成功するとクライアント認証は成功します。`optional` の場合、クライアント証明書がチェックされるのは `PUT`、`POST`、`PATCH`、および `DELETE` リクエストに対してのみです。
- **PATRONI_RESTAPI_ALLOWLIST**: (オプション): 安全でない REST API エンドポイントの呼び出しを許可するホストのセットを指定します。単一の要素は、ホスト名、IP アドレス、または CIDR 表記を使用したネットワーク アドレスです。デフォルトでは `allow all` が使用されます。 `allowlist` または `allowlist_include_members` が設定されている場合、含まれていないものはすべて拒否されます。
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS**: (オプション): `true` に設定すると、DCS に登録されている他のクラスターメンバーから安全でない REST API エンドポイントへのアクセスが許可されます (IP アドレスまたはホスト名はメンバーの `api_url` から取得されます)。OS が送信接続に別の IP を使用する可能性があることに注意してください。
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS**: （任意）REST APIサーバーがHTTP応答に追加情報を含めるためのHTTPヘッダー。
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS**: (オプション) HTTPS ヘッダーは、TLS が有効な場合に REST API サーバーが HTTP 応答とともに追加情報を渡せるようにします。これにより、`http_extra_headers` で設定された追加情報も渡されます。
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE**: (オプション): Patroni REST API が使用する TCP ソケットのリクエストキューサイズを設定します。キューがいっぱいになると、それ以降のリクエストでは "Connection denied" エラーが発生します。デフォルト値は 5 です。
- **PATRONI_RESTAPI_SERVER_TOKENS**: (オプション) `Server` HTTP ヘッダーの値を構成します。`Original` (デフォルト) は元の動作を公開し、BaseHTTP および Python のバージョンを表示します (例: `BaseHTTP/0.6 Python/3.12.3`)。`Minimal`: ヘッダーには Patroni のバージョンのみが含まれます (例: `Patroni/4.0.0`)。`ProductOnly`: ヘッダーには製品名のみが含まれます (例: `Patroni`)。

<div class="warning">

<div class="title">

警告

</div>

- `PATRONI_RESTAPI_CONNECT_ADDRESS` は、特定の Patroni クラスターのすべてのノードからアクセス可能である必要があります。内部的には、Patroni がリーダー レース中にこれを使用して、レプリケーション ラグが最小限のノードを見つけます。
- クライアント証明書の検証を有効にした場合 (`PATRONI_RESTAPI_VERIFY_CLIENT` が `required` に設定されている場合)、`PATRONI_CTL_CERTFILE`、`PATRONI_CTL_KEYFILE`、`PATRONI_CTL_KEYFILE_PASSWORD` で **有効なクライアント証明書** を提供することが**必須**です。提供しない場合、Patroni は正しく動作しません。

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE**: (オプション) 構成ファイルの場所。
- **PATRONI_CTL_USERNAME**: (オプション) 保護された REST API エンドポイントにアクセスするための Basic 認証ユーザー名。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "username" パラメーターに指定された値を使用します。
- **PATRONI_CTL_PASSWORD**: (オプション) 保護された REST API エンドポイントにアクセスするための Basic 認証パスワード。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "password" パラメーターに指定された値を使用します。
- **PATRONI_CTL_INSECURE**: (オプション) SSL 証明書を検証せずに、REST API への接続を許可します。
- **PATRONI_CTL_CACERT**: (オプション) REST API SSL 証明書の検証中に使用する、CA_BUNDLE ファイルまたは信頼できる CA の証明書が含まれるディレクトリを指定します。指定されない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は REST API "cafile" パラメーターに指定された値を使用します。
- **PATRONI_CTL_CERTFILE**: (オプション) PEM 形式のクライアント証明書を含むファイルを指定します。
- **PATRONI_CTL_KEYFILE**: (オプション) クライアント秘密鍵を含むファイルを PEM 形式で指定します。
- **PATRONI_CTL_KEYFILE_PASSWORD**: (オプション) クライアントのキーファイルを復号化するためのパスワードを指定します。
