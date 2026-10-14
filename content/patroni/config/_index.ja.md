---
title: "Patroni 構成"
weight: 30
icon: fa-solid fa-code
description: "Patroni 構成モデル、優先順位ルール、および検証ツール。"
sidebar_expanded: true
module: [PATRONI]
categories: [リファレンス]
upstream_link: "https://patroni.readthedocs.io/en/latest/patroni_configuration.html"
---

<a id="config"></a>
Patroni 構成には 3 タイプがあります。

- グローバル [動的構成](/ja/patroni/config/dynamic#dynamic)。   これらのオプションは DCS (分散構成ストア) に保存され、すべてのクラスター ノードに適用されます。動的構成は、[patronictl_edit_config](/ja/patroni/patronictl#patronictl_edit_config) ツールまたは Patroni [REST API](/ja/patroni/rest_api#rest_api) を使用していつでも設定できます。変更されたオプションがスタートアップ コンフィギュレーションの一部ではない場合、オプションはすべてのノードに非同期的に (次のウェイクアップ サイクル時に) 適用され、その後リロードされます。構成を適用するためにノードの再起動が必要な場合 (コンテキストが postmaster で、値が変更された [PostgreSQL パラメータ](https://www.postgresql.org/docs/current/view-pg-settings.html) の場合)、これを示す特別なフラグ `pending_restart` が members.data JSON に設定されます。さらに、ノードのステータスは `"restart_pending": true` を表示することでこれを示します。

- ローカル [設定ファイル](/ja/patroni/config/yaml#yaml) (patroni.yml)。   これらのオプションは構成ファイルで定義され、動的構成より優先されます。 `patroni.yml` は、SIGHUP を Patroni プロセスに送信するか、`POST /reload` REST-API リクエストを実行するか、[patronictl_reload](/ja/patroni/patronictl#patronictl_reload) を実行することで、実行時に (Patroni を再起動せずに) 変更および再ロードできます。ローカル構成は、単一の YAML ファイルまたはディレクトリのいずれかになります。ディレクトリの場合、そのディレクトリ内のすべての YAML ファイルがソートされた順序で 1 つずつロードされます。キーが複数のファイルで定義されている場合、最後のファイル内のキーが優先されます。

- [環境構成](/ja/patroni/config/env#env)。   環境変数を使用して、一部の「ローカル」構成パラメータを設定/上書きすることができます。環境構成は、動的環境で実行していて、一部のパラメーターが事前にわかっていない場合に非常に役立ちます (たとえば、`docker` 内で実行しているときに外部 IP アドレスを知ることはできません)。

<a id="important_configuration_rules"></a>

--------

## 重要なルール {#important-rules}

### PostgreSQL パラメータは Patroni によって制御されます {#postgresql-parameters-controlled-by-patroni}

PostgreSQL パラメーターの一部は、**プライマリーとレプリカで同じ値を保持する必要があります**。これらについては、**ローカルの patroni 設定ファイルまたは環境変数で設定された値は効果がありません**。値を変更または設定するには、DCS の共有構成を変更する必要があります。以下は、そのようなパラメータの実際のリストとデフォルト値および最小値です。

- **max_connections**: デフォルト値 100、最小値 25
- **max_locks_per_transaction**: デフォルト値 64、最小値 32
- **max_worker_processes**: デフォルト値 8、最小値 2
- **max_prepared_transactions**: デフォルト値 0、最小値 0
- **wal_level**: デフォルト値 hot_standby、受け入れられる値: hot_standby、replica、logical
- **track_commit_timestamp**: デフォルト値はオフです

以下のパラメータの場合、PostgreSQL はプライマリーとすべてのレプリカ間で同じ値を必要としません。ただし、レプリカがいつでもプライマリーになる可能性を考慮すると、これらのパラメーターを異なる値に設定することはあまり意味がありません。したがって、**Patroni は、これらの値の設定を** [動的構成](/ja/patroni/config/dynamic#dynamic) **に制限しています**。

- **max_wal_senders**: デフォルト値 10、最小値 3
- **max_replication_slots**: デフォルト値 10、最小値 4
- **wal_keep_segments**: デフォルト値 8、最小値 1
- **wal_keep_size**: デフォルト値 128MB、最小値 16MB
- **wal_log_hints**: オン

これらのパラメーターは検証され、それらが正常であるか、最小値を満たしているかが確認されます。

Patroni によって制御される Postgres パラメーターは他にもいくつかあります。

- **listen_addresses** - `postgresql.listen` または `PATRONI_POSTGRESQL_LISTEN` 環境変数から設定されます
- **port** - `postgresql.listen` または `PATRONI_POSTGRESQL_LISTEN` 環境変数から設定されます
- **cluster_name** - `scope` または `PATRONI_SCOPE` 環境変数から設定されます
- **hot_standby: on**

安全のため、上記のリストのパラメータは `postgresql.conf` に書き込まれ、引数のリストとして `postgres` に渡され、(`wal_keep_segments` と `wal_keep_size` を除き) [ALTER SYSTEM](https://www.postgresql.org/docs/current/static/sql-altersystem.html) すら超える最も高い優先順位が与えられます。

**postgresql.listen** や **postgresql.data_dir** のように、**ローカルでのみ設定可能**なパラメーターもいくつかあります。つまり、Patroni [設定ファイル](/ja/patroni/config/yaml#yaml) 内で、または[環境構成](/ja/patroni/config/env#env)の変数経由で設定します。ほとんどの場合、ローカル構成は動的構成をオーバーライドします。

ローカルまたは動的構成オプションを適用すると、次のアクションが実行されます。

- ノードはまず、`postgresql.base.conf` ファイルがあるかどうか、または `custom_conf` パラメーターが設定されているかどうかを確認します。
- `custom_conf` パラメータが設定されている場合、指定されたファイルが基本構成として使用され、`postgresql.base.conf` と `postgresql.conf` は無視されます。
- `custom_conf` パラメーターが設定されておらず、`postgresql.base.conf` が存在する場合、名前が変更された "original" 構成が含まれており、基本構成として使用されます。
- `custom_conf` も `postgresql.base.conf` もない場合、元の `postgresql.conf` は `postgresql.base.conf` に名前変更され、基本構成として使用されます。
- 動的オプション (上記の例外を除く) は `postgresql.conf` にダンプされ、インクルードは `postgresql.conf` で基本構成 (`postgresql.base.conf` または `custom_conf` のファイルのいずれか) に設定されます。したがって、インクルードが存在するかどうかを確認するために構成ファイルを再度読み取ることなく、新しいオプションを適用できます。
- Patroni がクラスターを管理するために必要な一部のパラメーターは、コマンド ラインを使用してオーバーライドされます。
- 再起動を必要とするオプションが変更された場合 (pg_settings のコンテキストとそれらのオプションの実際の値を確認する必要があります)、そのノードに pending_restart フラグが設定されます。このフラグは再起動時にリセットされます。

パラメータは次の順序で適用されます (ランタイムに最も高い優先順位が与えられます)。

1. ファイル `postgresql.base.conf` (または設定されている場合は `custom_conf` ファイル) からパラメータをロードします
2. ファイル `postgresql.conf` からパラメータをロードします
3. ファイル `postgresql.auto.conf` からパラメータをロードします
4. `-o --name=value` を使用した実行時パラメーター

これにより、すべてのノードの構成 (2)、`ALTER SYSTEM` を使用した特定のノードの構成 (3) が可能になり、Patroni の実行に不可欠なパラメーターが強制されるようになります (4)。また、Patroni (1) を介さずに `postgresql.conf` を直接管理する構成ツールの余地も残ります。

<a id="shared_memory_gucs"></a>

### 共有メモリに関わる PostgreSQL パラメータ {#postgresql-parameters-that-touch-shared-memory}

PostgreSQL には、使用される共有メモリのサイズを決定するいくつかのパラメータがあります。

- **max_connections**
- **max_prepared_transactions**
- **max_locks_per_transaction**
- **max_wal_senders**
- **max_worker_processes**

これらのパラメータを変更するには、PostgreSQL の再起動が必要であり、スタンバイ ノードの共有メモリ構造をプライマリー ノードよりも小さくすることはできません。

前に説明したように、Patroni は、これらの値の変更を [動的構成](/ja/patroni/config/dynamic#dynamic) 経由に限定します。通常、これは次のもので構成されます。

1. [patronictl_edit_config](/ja/patroni/patronictl#patronictl_edit_config) (または REST API `/config` エンドポイント経由) による変更の適用
2. [patronictl_restart](/ja/patroni/patronictl#patronictl_restart) (または REST API `/restart` エンドポイント経由) によるノードの再起動

**注:** PostgreSQL ノードの再起動は、[patronictl_restart](/ja/patroni/patronictl#patronictl_restart) コマンド、または REST API `/restart` エンドポイントを介して実行する必要があることに留意してください。Patroni デーモンの再起動による PostgreSQL の再起動の試み (たとえば `systemctl restart patroni` の実行) は、プライマリー ノードを再起動している場合、クラスター内でフェイルオーバーを引き起こす可能性があります。

ただし、これらの設定は共有メモリを管理するため、ノードを再起動するときは特に注意する必要があります。

- これらの設定のいずれかの値を**増加**させたい場合:

  > 1.  最初にすべてのスタンバイを再起動します
  > 2.  その後プライマリーを再起動します

- これらの設定のいずれかの値を**減少**させたい場合:

  > 1.  最初にプライマリーを再起動します
  > 2.  その後、すべてのスタンバイを再起動します

**注:** これらの設定のいずれかの値を**減少**させた後にすべてのノードを一度に再起動しようとすると、Patroni は変更を無視し、元の設定値でスタンバイを再起動するため、後でスタンバイを再度再起動する必要があります。Patroni は、スタンバイ ノードの `pg_controldata` で表示される値よりも低い値にこれらのパラメーターのいずれかを設定しようとすると、PostgreSQL が `FATAL` メッセージで終了するため、スタンバイが無限クラッシュ ループに陥るのを防ぐためにこれを行います。言い換えれば、プライマリーでのこれらの変更に関してスタンバイの `pg_controldata` がプライマリーと同期している場合にのみ、スタンバイの設定を減らすことができます。

詳細については、[PostgreSQL 管理者の概要](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN) を参照してください。

### Patroni 構成パラメータ {#patroni-configuration-parameters}

また、次の Patroni 構成オプションは**動的にのみ変更可能**です:

- **ttl**: 30
- **loop_wait**: 10
- **retry_timeout**: 10
- **maximum_lag_on_failover**: 1048576
- **max_timelines_history**: 0
- **check_timeline**: false
- **postgresql.use_slots**: true

これらのオプションを変更すると、Patroni は DCS に保存されている構成の関連セクションを読み取り、その実行時の値を変更します。

Patroni ノードは、構成が変更されるたびに、DCS オプションの状態を、Postgres データ ディレクトリにあるファイル `patroni.dynamic.json` にダンプします。これらのオプションが DCS に完全に存在しない場合、または無効な場合、リーダーのみがオンディスク ダンプからこれらのオプションを復元できます。

<a id="validate_generate_config"></a>

--------

## 構成の生成と検証 {#configuration-generation-and-validation}

Patroni は、Patroni [ローカル構成](/ja/patroni/config/yaml#yaml) の生成と検証のためのコマンドライン インターフェイスを提供します。 `patroni` 実行可能ファイルを使用すると、次のことが可能になります。

- サンプルのローカル Patroni 構成を作成します。
- ローカルで実行されている PostgreSQL インスタンスの Patroni 構成ファイルを作成します (例: [Patroni の統合](/ja/patroni/existing_data#existing_data) の準備ステップとして)。
- 指定された Patroni 構成ファイルを検証します。

<a id="generate_sample_config"></a>

### Patroni 構成のサンプル {#sample-patroni-configuration}

```text
patroni --generate-sample-config [configfile]
```

#### 説明 {#description}

サンプルの Patroni 構成ファイルを `yaml` 形式で生成します。パラメータ値は [環境構成](/ja/patroni/config/env#env) を使用して定義されます。設定されていない場合は、Patroni で使用されるデフォルト値、または後でユーザーが定義すべき値のための `#FIXME` 文字列が使用されます。

一部のデフォルト値はローカル設定に基づいて定義されます。

> - **postgresql.listen**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `5432` ポート。
> - **postgresql.connect_address**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `5432` ポート。
> - **postgresql.authentication.rewind**: PostgreSQL バージョンをバイナリから定義でき、そのバージョンが 11 以降である場合にのみ定義されます。
> - **restapi.listen**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `8008` ポート。
> - **restapi.connect_address**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `8008` ポート。

#### パラメータ {#parameters}

`configfile` - 結果を保存するために使用される構成ファイルへのフルパス。指定しない場合、結果は `stdout` に送信されます。

<a id="generate_config"></a>

### 実行中のインスタンスの Patroni 構成 {#patroni-configuration-for-a-running-instance}

```text
patroni --generate-config [--dsn DSN] [configfile]
```

#### 説明 {#description-1}

ローカルで実行されている PostgreSQL インスタンス用に Patroni 構成を `yaml` 形式で生成します。提供された DSN (優先されます) または PostgreSQL [環境変数](https://www.postgresql.org/docs/current/libpq-envars.html) のいずれかが PostgreSQL 接続に使用されます。パスワードが指定されていない場合は、プロンプトから入力する必要があります。

ソース Postgres インスタンスで定義されたすべての非内部 GUC は、構成ファイル、postmaster コマンドライン、または環境変数のいずれで設定されたものであるかにかかわらず、次の Patroni 構成パラメーターのソースとして使用されます:

> - **scope**: `cluster_name` GUC 値;
> - **postgresql.listen**: `listen_addresses` および `port` GUC 値。
> - **postgresql.data_dir**: `data_directory` GUC 値;
> - **postgresql.parameters**: `archive_command`、`restore_command`、`archive_cleanup_command`、`recovery_end_command`、`ssl_passphrase_command`、`hba_file`、`ident_file`、`config_file` GUC 値。
> - **bootstrap.dcs**: 収集された他のすべての PostgreSQL GUC。

`scope`、`postgresql.listen`、または `postgresql.data_dir` が Postgres GUC から設定されていない場合は、それぞれの [環境構成](/ja/patroni/config/env#env) 値が使用されます。

値の定義に適用されるその他のルールは次のとおりです。

> - **name**: `PATRONI_NAME` 環境変数値 (設定されている場合)、そうでない場合は現在のマシンのホスト名。
> - **postgresql.bin_dir**: 実行中のインスタンスから収集された Postgres バイナリへのパス。
> - **postgresql.connect_address**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと、インスタンス接続に使用されるポートまたは `port` GUC 値。
> - **postgresql.authentication.superuser**: インスタンス接続に使用される構成。
> - **postgresql.pg_hba**: ソース インスタンスの `hba_file` から収集された行。
> - **postgresql.pg_ident**: ソース インスタンスの `ident_file` から収集された行。
> - **restapi.listen**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `8008` ポート。
> - **restapi.connect_address**: `gethostname` が返す現在のマシンのホスト名を `getaddrinfo` で解決した IP アドレスと標準の `8008` ポート。

[環境構成](/ja/patroni/config/env#env) を使用して定義された他のパラメーターも構成に含まれます。

#### パラメータ {#parameters-1}

`configfile` 結果を保存するために使用される構成ファイルへのフルパス。指定しない場合、結果は `stdout` に送信されます。

`dsn` GUC 値を取得するローカル PostgreSQL インスタンスのオプションの DSN 文字列。

### Patroni 構成を検証する {#validate-patroni-configuration}

```text
patroni --validate-config [configfile] [--ignore-listen-port | -i]
```

#### 説明 {#description-2}

指定された Patroni 構成を検証し、失敗したチェックに関する情報を出力します。

#### パラメータ {#parameters-2}

`configfile` 確認する構成ファイルへのフルパス。指定されない場合、またはファイルが存在しない場合は、`PATRONI_CONFIGURATION` 環境変数からの読み取りを試みます。設定されていない場合は、[Patroni 環境変数](/ja/patroni/config/env#env) からの読み取りを試みます。

`--ignore-listen-port | -i` `configfile` を検証するときに、すでに使用されている `listen` ポートのバインド失敗を無視するためのオプションのフラグ。

`--print | -p` 正常に検証された後にローカル構成 (環境構成のオーバーライドを含む) を出力するためのオプションのフラグ。
